"""Real-data anchors for Study E. Descriptive statistics only: nothing here computes a pre-registered endpoint.

Three anchor families, each labelled by what it is and is not:
  * SatNOGS observation windows  -> SCHEDULED downlink observation windows by volunteer stations (not contacts, not loss).
  * Starlink ping bursts         -> consumer LEO BROADBAND loss/persistence example (not TT&C, not uplink telemetry).
  * Modeled pass durations       -> circular-orbit geometry, MODELED, not measured.
Pure standard library. Deterministic.
"""
import csv
import glob
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from fractions import Fraction

RE_KM = 6378.137          # WGS-84 equatorial radius
MU_KM3_S2 = 398600.4418   # Earth gravitational parameter


# ---------------------------------------------------------------- generic helpers
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def quantile(sorted_vals, q):
    """Type-7 (linear interpolation) quantile of an already sorted list; q in [0,1]."""
    n = len(sorted_vals)
    if n == 0:
        raise ValueError("empty sample")
    if n == 1:
        return float(sorted_vals[0])
    pos = (n - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    return float(sorted_vals[lo]) + (pos - lo) * (float(sorted_vals[hi]) - float(sorted_vals[lo]))


def summary(vals):
    s = sorted(vals)
    if not s:
        return {"n": 0}
    return {"n": len(s), "min": s[0], "p25": quantile(s, .25), "median": quantile(s, .5),
            "p75": quantile(s, .75), "p90": quantile(s, .9), "max": s[-1], "mean": sum(s) / len(s)}


def _ts(value):
    if not isinstance(value, str):
        raise ValueError("timestamp is not a string")
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError("timestamp lacks timezone")
    return dt.astimezone(timezone.utc)


# ---------------------------------------------------------------- SatNOGS windows
def load_satnogs_jsonl(path):
    rows, seen = [], set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            d = json.loads(line)
            for k in ("id", "start", "end", "ground_station", "norad_cat_id"):
                if k not in d:
                    raise ValueError("missing field %s" % k)
            if d["id"] in seen:
                raise ValueError("duplicate observation id %r" % d["id"])
            seen.add(d["id"])
            s, e = _ts(d["start"]), _ts(d["end"])
            if not s < e:
                raise ValueError("start not before end for id %r" % d["id"])
            rows.append((d["norad_cat_id"], d["ground_station"], s, e, d["id"]))
    return rows


def trace_stats(rows):
    """Window durations (end-start) and gaps between consecutive windows of the same satellite-station pair.
    A gap is the time from one scheduled window's end to the next window's start. It is NOT a contact gap: stations
    do not schedule every pass. Negative gaps (overlaps) are counted and excluded from gap summaries."""
    pairs = {}
    for norad, gs, s, e, oid in rows:
        pairs.setdefault((norad, gs), []).append((s, e, oid))
    all_dur, all_gap, per_pair, overlaps = [], [], [], 0
    for key in sorted(pairs):
        obs = sorted(pairs[key])
        dur = [(e - s).total_seconds() for s, e, _ in obs]
        gaps = []
        for (s0, e0, _), (s1, e1, _) in zip(obs, obs[1:]):
            g = (s1 - e0).total_seconds()
            if g < 0:
                overlaps += 1
            else:
                gaps.append(g)
        all_dur += dur
        all_gap += gaps
        per_pair.append({"norad_cat_id": key[0], "ground_station": key[1], "n_windows": len(obs),
                         "duration_s": summary(dur), "gap_s": summary(gaps)})
    return {"label": "SCHEDULED downlink observation windows; not contacts, not loss, not uplink",
            "n_rows": len(rows), "n_pairs": len(pairs), "overlaps_excluded": overlaps,
            "duration_s": summary(all_dur), "gap_s": summary(all_gap), "per_pair": per_pair}


# ---------------------------------------------------------------- Starlink ping bursts
def load_ping_dir(directory):
    """Rows of (datetime, transmitted, lost) from ping_metrics_* files (';' CSV or tab TSV).
    Rows with blank counts are returned separately as (datetime) and are never counted as loss or as success."""
    usable, blank = [], []
    files = sorted(glob.glob(os.path.join(directory, "ping_metrics_*")))
    if not files:
        raise FileNotFoundError("no ping_metrics_* files in %s" % directory)
    for f in files:
        delim = "\t" if f.endswith(".tsv") else ";"
        with open(f, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh, delimiter=delim):
                t = datetime.strptime(r["Timestamp"], "%Y-%m-%d %H:%M:%S")
                try:
                    usable.append((t, int(r["PacketTransmit"]), int(r["PacketLossCount"])))
                except ValueError:
                    blank.append(t)
    usable.sort()
    return usable, sorted(blank)


def ping_stats(usable, blank, max_spacing_s=15):
    """Burst-level loss and persistence. Consecutive means consecutive usable bursts spaced <= max_spacing_s;
    a blank row or a larger spacing breaks a run (the outage content is unknown, so it is not imputed)."""
    n = len(usable)
    if n < 2:
        raise ValueError("need at least two bursts")
    sent = sum(r[1] for r in usable)
    lost = sum(r[2] for r in usable)
    lossy = [r[2] > 0 for r in usable]
    full = sum(1 for r in usable if r[2] == r[1])
    spac = [(usable[i + 1][0] - usable[i][0]).total_seconds() for i in range(n - 1)]
    # a pair is "adjacent" only if spacing is small AND no blank row lies strictly between the two timestamps
    blank_set = sorted(blank)
    import bisect

    def has_blank_between(a, b):
        i = bisect.bisect_right(blank_set, a)
        return i < len(blank_set) and blank_set[i] < b

    adj = [spac[i] <= max_spacing_s and not has_blank_between(usable[i][0], usable[i + 1][0]) for i in range(n - 1)]
    after_ok = after_ok_lossy = after_lossy = after_lossy_lossy = 0
    runs, cur = [], 0
    for i in range(n):
        if i > 0 and adj[i - 1]:
            if lossy[i - 1]:
                after_lossy += 1
                after_lossy_lossy += lossy[i]
            else:
                after_ok += 1
                after_ok_lossy += lossy[i]
        if lossy[i]:
            if cur and not (i > 0 and adj[i - 1]):
                runs.append(cur)       # run ended by a gap or blank row, not by a clean burst
                cur = 0
            cur += 1
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    hist = {}
    for r in runs:
        hist[r] = hist.get(r, 0) + 1
    return {
        "label": "consumer LEO BROADBAND (Starlink) ICMP ping bursts; not TT&C, not telemetry, 10 s cadence",
        "usable_bursts": n, "blank_rows_excluded": len(blank), "packets_sent": sent, "packets_lost": lost,
        "mean_packet_loss": lost / sent, "share_bursts_with_loss": sum(lossy) / n, "full_loss_bursts": full,
        "adjacent_pair_rule": "spacing <= %d s and no blank row between" % max_spacing_s,
        "p_lossy_given_prev_ok": after_ok_lossy / after_ok if after_ok else None,
        "p_lossy_given_prev_lossy": after_lossy_lossy / after_lossy if after_lossy else None,
        "lossy_run_length_hist": {str(k): hist[k] for k in sorted(hist)},
        "lossy_run_mean": sum(runs) / len(runs) if runs else None, "lossy_run_max": max(runs) if runs else None,
        "resolution_note": "10 packets per 10 s: cannot resolve packet-level sojourns or a 15 s handover cycle"}


# ---------------------------------------------------------------- matched-stationary Gilbert-Elliott
def ge_matched(p_stat, mean_bad_run):
    """Pre-specified sensitivity rule (not a fit): good state never loses, bad state always loses, mean bad sojourn
    `mean_bad_run` slots, stationary loss exactly `p_stat`. Returns the study_e ge tuple (a, b, p_bad) with p_good = 0.
    Exact (Fractions). Requires mean_bad_run >= 1 and a <= 1."""
    p_stat, m = Fraction(p_stat), Fraction(mean_bad_run)
    if not (0 < p_stat < 1) or m < 1:
        raise ValueError("need 0 < p_stat < 1 and mean_bad_run >= 1")
    b = 1 / m
    a = b * p_stat / (1 - p_stat)
    if a > 1:
        raise ValueError("no valid GE channel: a=%s > 1" % a)
    return a, b, Fraction(1)


def ge_stationary_loss(a, b, p_good, p_bad):
    a, b = Fraction(a), Fraction(b)
    pi_bad = a / (a + b)
    return (1 - pi_bad) * Fraction(p_good) + pi_bad * Fraction(p_bad)


# ---------------------------------------------------------------- modeled pass durations
def orbit_rate(h_km):
    a = RE_KM + h_km
    return math.sqrt(MU_KM3_S2 / a ** 3)


def pass_half_angle(h_km, e_deg):
    """Earth-central half-angle of the visibility cap for minimum elevation e (circular orbit)."""
    a = RE_KM + h_km
    e = math.radians(e_deg)
    return math.acos(RE_KM * math.cos(e) / a) - e


def max_pass_seconds(h_km, e_deg):
    """Overhead pass (zero cross-track offset). Earth rotation, inclination, station latitude ignored."""
    return 2 * pass_half_angle(h_km, e_deg) / orbit_rate(h_km)


def pass_seconds(h_km, e_deg, beta_rad):
    """Pass with closest-approach central angle beta (0 <= beta <= half-angle); 0 beyond the cap."""
    lam = pass_half_angle(h_km, e_deg)
    if beta_rad >= lam:
        return 0.0
    g = math.acos(math.cos(lam) / math.cos(beta_rad))
    return 2 * g / orbit_rate(h_km)


def mean_pass_seconds(h_km, e_deg, steps=4000):
    """Mean duration over closest-approach angle uniform on [0, half-angle] (a modeling convention)."""
    lam = pass_half_angle(h_km, e_deg)
    tot = 0.0
    for i in range(steps):
        tot += pass_seconds(h_km, e_deg, (i + 0.5) * lam / steps)
    return tot / steps


def slots_per_pass(duration_s, slot_s):
    if slot_s <= 0:
        raise ValueError("slot length must be positive")
    return int(duration_s // slot_s)
