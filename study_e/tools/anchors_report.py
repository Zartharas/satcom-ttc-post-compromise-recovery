"""Builds the Study E real-data anchor report. Descriptive only: executes no pre-registered analysis and writes no
pre-registered result. Refuses to run on a SatNOGS file whose SHA-256 differs from the Study 8E freeze record.

Usage (from the study_e folder):
  python3 -I tools/anchors_report.py --satnogs PATH/satnogs_pop002_firstpage_476.jsonl --ping-dir DIR --out OUTDIR
"""
import argparse
import json
import os
import sys

sys.path.insert(0, ".")
from fractions import Fraction as F
from study_e import anchors as A

FROZEN_SATNOGS_SHA256 = "6f80a44fa6cfa63a70df49de3ba447de3d59efe0632208180f26552f37b46a8e"
GRID_P = [F(1, 20), F(1, 10), F(1, 5), F(3, 10), F(1, 2)]
GRID_K = [2, 3, 4, 6]


def verify_ping_hashes(directory):
    sums = os.path.join(directory, "SHA256SUMS.txt")
    if not os.path.exists(sums):
        return {"checked": False, "reason": "SHA256SUMS.txt absent"}
    bad, n = [], 0
    for line in open(sums):
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        name = name.strip().lstrip("*")
        n += 1
        if A.sha256_file(os.path.join(directory, name)) != digest:
            bad.append(name)
    if bad:
        raise SystemExit("ping file hash mismatch: %s" % bad)
    return {"checked": True, "files": n, "matches_local_record": True,
            "limit": "hashes were recorded locally at download; not compared with Zenodo checksums"}


def pass_table():
    rows = []
    for h in (400, 550, 800, 1200):
        for e in (5, 10, 20):
            tmax, tmean = A.max_pass_seconds(h, e), A.mean_pass_seconds(h, e)
            rows.append({"altitude_km": h, "min_elevation_deg": e, "max_pass_s": round(tmax, 1),
                         "mean_pass_s": round(tmean, 1),
                         "slots_at_30s_max": A.slots_per_pass(tmax, 30), "slots_at_30s_mean": A.slots_per_pass(tmean, 30),
                         "slots_at_60s_max": A.slots_per_pass(tmax, 60), "slots_at_60s_mean": A.slots_per_pass(tmean, 60)})
    return rows


def ge_table():
    out = []
    for p in GRID_P:
        for m in (2, 4):
            try:
                a, b, pb = A.ge_matched(p, m)
                out.append({"p_stationary": str(p), "mean_bad_sojourn_slots": m, "a_good_to_bad": str(a),
                            "b_bad_to_good": str(b), "p_bad": str(pb), "p_good": "0"})
            except ValueError as ex:
                out.append({"p_stationary": str(p), "mean_bad_sojourn_slots": m, "invalid": str(ex)})
    return out


def md(rep):
    s, ping = rep["satnogs"], rep["ping"]
    L = ["# Study E anchor report (descriptive; DRAFT; no pre-registered analysis executed)", "",
         "## Inspection order (read this first)",
         rep["inspection_order_note"], "",
         "## 1. SatNOGS POP-002 trace (from Study 8E, re-materialized and hash-verified)",
         "Label: %s." % s["label"],
         "Rows %d, pairs %d, overlaps excluded %d. Source file SHA-256 %s (equals the Study 8E freeze record)." % (
             s["n_rows"], s["n_pairs"], s["overlaps_excluded"], rep["satnogs_sha256"]), "",
         "| | n | min | p25 | median | p75 | p90 | max | mean |", "|---|---|---|---|---|---|---|---|---|"]
    for k, nm in (("duration_s", "window duration (s)"), ("gap_s", "gap between windows (s)")):
        v = s[k]
        L.append("| %s | %d | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f |" % (
            nm, v["n"], v["min"], v["p25"], v["median"], v["p75"], v["p90"], v["max"], v["mean"]))
    L += ["", "First-page records only (latest 25 per pair, June 2026 window): not representative, not a full history.", "",
          "## 2. Starlink ping bursts (Zenodo 10.5281/zenodo.14987305, CC BY 4.0)", "Label: %s." % ping["label"], "",
          "- usable bursts %d; blank rows excluded %d (unknown content, never counted as loss)" % (
              ping["usable_bursts"], ping["blank_rows_excluded"]),
          "- packets sent %d, lost %d, mean loss %.3f%%" % (ping["packets_sent"], ping["packets_lost"], 100 * ping["mean_packet_loss"]),
          "- bursts with any loss %.2f%%; bursts losing all packets %d" % (100 * ping["share_bursts_with_loss"], ping["full_loss_bursts"]),
          "- P(lossy | previous burst lossy) = %.3f; P(lossy | previous ok) = %.3f (adjacent = %s)" % (
              ping["p_lossy_given_prev_lossy"], ping["p_lossy_given_prev_ok"], ping["adjacent_pair_rule"]),
          "- lossy run lengths (bursts: count) %s; mean %.3f, max %d" % (
              ping["lossy_run_length_hist"], ping["lossy_run_mean"], ping["lossy_run_max"]),
          "- %s" % ping["resolution_note"],
          "- file hashes: %s" % json.dumps(rep["ping_hash_check"]), "",
          "## 3. Modeled pass durations (circular orbit, Earth rotation ignored; MODELED, not measured)", "",
          "| altitude km | min elev deg | max pass s | mean pass s | slots@30s max/mean | slots@60s max/mean |",
          "|---|---|---|---|---|---|"]
    for r in rep["pass_table"]:
        L.append("| %d | %d | %.1f | %.1f | %d / %d | %d / %d |" % (
            r["altitude_km"], r["min_elevation_deg"], r["max_pass_s"], r["mean_pass_s"], r["slots_at_30s_max"],
            r["slots_at_30s_mean"], r["slots_at_60s_max"], r["slots_at_60s_mean"]))
    L += ["", "Mean assumes closest-approach angle uniform on [0, visibility half-angle] (a convention). The candidate K grid "
          "%s is therefore conservative relative to full geometric passes; K is a count of message slots usable for this "
          "exchange, which may be far fewer than geometric slots (command windows, scheduling, contention)." % GRID_K, "",
          "## 4. Matched-stationary Gilbert-Elliott sensitivity cases (pre-specified rule, not a fit)",
          "Good state never loses, bad state always loses, mean bad sojourn m slots, stationary loss equal to the i.i.d. "
          "grid value. Invalid combinations (a > 1) are reported as such.", "",
          "| p stationary | m | a (good->bad) | b (bad->good) |", "|---|---|---|---|"]
    for r in rep["ge_table"]:
        L.append("| %s | %d | %s | %s |" % (r["p_stationary"], r["mean_bad_sojourn_slots"],
                                           r.get("a_good_to_bad", "invalid: " + r.get("invalid", "")),
                                           r.get("b_bad_to_good", "")))
    L += ["", "## 5. What these anchors do and do not support", *["- " + x for x in rep["claims"]]]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--satnogs", required=True)
    ap.add_argument("--ping-dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sha = A.sha256_file(a.satnogs)
    if sha != FROZEN_SATNOGS_SHA256:
        raise SystemExit("SatNOGS file hash %s != Study 8E freeze record; refusing to analyse" % sha)
    usable, blank = A.load_ping_dir(a.ping_dir)
    rep = {
        "inspection_order_note": ("The Starlink ping summary statistics were inspected BEFORE this report's fitting rule "
                                  "was written, so they cannot be presented as blind. The SatNOGS timing summaries were "
                                  "computed by this tool for the first time; Study 8E's own results (frozen separately) "
                                  "used the same trace, so the author is not blind to its timing behaviour either. The "
                                  "Gilbert-Elliott cases below are therefore a stated sensitivity rule with stress-test "
                                  "values, not parameters fitted to these files."),
        "satnogs_sha256": sha, "satnogs": A.trace_stats(A.load_satnogs_jsonl(a.satnogs)),
        "ping": A.ping_stats(usable, blank), "ping_hash_check": verify_ping_hashes(a.ping_dir),
        "pass_table": pass_table(), "ge_table": ge_table(),
        "claims": ["SatNOGS windows: scheduled observation windows by volunteer downlink stations. They bracket plausible "
                   "window lengths and show uneven scheduling; they say nothing about loss, command uplink or contact gaps.",
                   "Starlink bursts: one consumer broadband link; low average loss with occasional total-loss bursts and mild "
                   "burst-to-burst persistence at 10 s resolution. Not spacecraft TT&C.",
                   "Pass table: geometry only; real contacts are shorter (masks, terrain, scheduling).",
                   "None of these is a measured TT&C uplink dataset. The paper must call the study parametric, anchored to "
                   "downlink proxies and published ranges."]}
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "anchors_report.json"), "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(a.out, "ANCHORS_REPORT.md"), "w") as fh:
        fh.write(md(rep))
    print("wrote", os.path.join(a.out, "ANCHORS_REPORT.md"))


if __name__ == "__main__":
    main()
