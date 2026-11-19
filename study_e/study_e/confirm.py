"""Confirmatory runner library for Study E (written AFTER the freeze tag study-e-prereg-v1; see docs/ANALYSIS_SCRIPT_AMENDMENT.md).

It implements only the hypotheses and endpoints in the frozen pre-registration. Where the frozen text is ambiguous the
operationalisation is declared in OPERATIONALISATION below, before any run. All arithmetic is exact (Fractions).
"""
import hashlib
import itertools
from collections import defaultdict
from fractions import Fraction as F

from .anchors import ge_matched
from .composite import composite_outcomes
from .model import exact_distribution, outcome_probs
from .params import Params

PERSIST_ORDER = ("volatile", "commit", "journal")          # least to most durable (frozen text)
POLICIES = ("expired_only", "restart_indeterminate", "resume")
R0 = dict(n_msgs=4, B0=8, L0=3)                             # only specified in the frozen tools/size_grid.py

FROZEN_GRID = dict(p=[F(1, 20), F(1, 10), F(1, 5), F(3, 10), F(1, 2)], K=[2, 3, 4, 6], B=[4, 6, 8, 12], L=[1, 2, 3, 4],
                   r=[F(0), F(1, 100), F(1, 20), F(1, 10)], persist=list(PERSIST_ORDER), activation=["local", "gated"],
                   H=[4, 8, 20], policy=list(POLICIES), detect=[1, 3, 5])

OPERATIONALISATION = {
    "R0 parameters": "n_msgs=4, B0=8, L0=3 as in the frozen tools/size_grid.py; the pre-registration text gives no values.",
    "H-E1": "Not computed by the runner: established by the validation suite (88 tests) recorded alongside the run.",
    "H-E2a": "SUCCESS compared between consecutive grid values on each axis with the others fixed: non-decreasing in B, K, L and H "
             "(H on the composite grid, per policy); non-increasing in p. Divergence monotonicity is reported descriptively only.",
    "H-E2b": "Gated activation: P(DIVERGED_G_AHEAD) at volatile >= commit >= journal for every (p,K,B,L,r).",
    "H-E2c": "Journal: the full exact outcome distribution is identical across the r grid. Volatile: P(DIVERGED_S_AHEAD)+P(DIVERGED_G_AHEAD) "
             "is non-decreasing across the r grid ('fallback required' = divergence).",
    "H-E3": "Policy expired_only. dS = SUCCESS(H=20)-SUCCESS(H=4). Primary: dS < P(INDETERMINATE) at H=20, over points with that mass > 0; "
            "secondary: the same with the mass at H=4 (the frozen wording does not say which horizon). Dominant lever: "
            "S_resume(20)-S_expired(20) > dS, reported over points with INDETERMINATE mass > 0 and over all points.",
    "H-E4": "At H=20, divergence recovery fraction = RECOVERED/(RECOVERED+UNRECOVERED_DIVERGED) over points with divergence mass > 0; "
            "'almost always' is declared as >= 0.95 and the full distribution is also reported. Detection delay 'matters' if the "
            "range of UNRECOVERED_DIVERGED over detect in {1,3,5} exceeds 0.01 (absolute); reported by H and by p.",
    "H-E5": "SUCCESS under the matched-stationary Gilbert-Elliott rule (good never loses, bad always loses, mean bad run m in {2,4}) "
            "versus i.i.d. loss at the same stationary p, exchange level only (the composite scenario does not support ge). "
            "Directions counted; the hypothesis is supported if a witness exists in both directions.",
}

KEYS = ("p", "K", "B", "L", "r", "persist", "activation")


def configs(grid):
    return [dict(zip(KEYS, v)) for v in itertools.product(*(grid[k] for k in KEYS))]


def make_params(c, **over):
    d = {k: c[k] for k in KEYS}
    d.update(over)
    return Params(**d)


def ckey(c):
    return tuple(c[k] for k in KEYS)


def exchange_table(grid):
    """{config key: (outcome probs, full distribution)} single-attempt, exact."""
    out = {}
    for c in configs(grid):
        dist = exact_distribution(make_params(c), exact=True)
        out[ckey(c)] = (outcome_probs(dist), dist)
    return out


def g(o, name):
    return o.get(name, F(0))


def policy_args(pol):
    return dict(retry_on=("EXPIRED_OLD", "INDETERMINATE") if pol == "restart_indeterminate" else ("EXPIRED_OLD",),
                resume=(pol == "resume"))


def composite_table(grid):
    """{(config key, H, policy, detect): outcome dict}, exact."""
    out = {}
    for c in configs(grid):
        P = make_params(c)
        for H in grid["H"]:
            for pol in grid["policy"]:
                for d in grid["detect"]:
                    out[(ckey(c), H, pol, d)] = composite_outcomes(P, H, R0["n_msgs"], R0["B0"], R0["L0"], d, exact=True, **policy_args(pol))
    return out


def table_digest(*tables):
    h = hashlib.sha256()
    for t in tables:
        for k in sorted(t, key=repr):
            v = t[k]
            if isinstance(v, tuple):
                v = v[0]
            h.update(repr((k, sorted((a, str(b)) for a, b in v.items()))).encode())
    return h.hexdigest()


def report(violations, total, label, limit=5):
    return {"label": label, "pairs_checked": total, "violations": len(violations), "holds_everywhere": len(violations) == 0,
            "first_witnesses": [str(x) for x in violations[:limit]]}


def axis_pairs(grid, axis):
    """Yield (lower config key, higher config key) for consecutive values of one axis, others fixed."""
    vals = grid[axis]
    others = [k for k in KEYS if k != axis]
    for combo in itertools.product(*(grid[k] for k in others)):
        base = dict(zip(others, combo))
        for lo, hi in zip(vals, vals[1:]):
            a, b = dict(base, **{axis: lo}), dict(base, **{axis: hi})
            yield ckey(a), ckey(b)


def check_monotone(values, pairs, direction, label):
    """values: {key: Fraction}; direction +1 non-decreasing, -1 non-increasing from lo to hi."""
    bad, n = [], 0
    for lo, hi in pairs:
        n += 1
        d = (values[hi] - values[lo]) * direction
        if d < 0:
            bad.append((lo, hi, str(values[lo]), str(values[hi])))
    return report(bad, n, label)


def h_e2a(grid, ex, comp):
    res = {}
    succ = {k: g(v[0], "SUCCESS") for k, v in ex.items()}
    for axis, sign in (("B", 1), ("K", 1), ("L", 1), ("p", -1)):
        res["single_attempt_SUCCESS_vs_" + axis] = check_monotone(succ, list(axis_pairs(grid, axis)), sign, "SUCCESS %s in %s" % ("non-decreasing" if sign > 0 else "non-increasing", axis))
    d0 = grid["detect"][0]
    bad, n = [], 0
    for c in configs(grid):
        for pol in grid["policy"]:
            for h0, h1 in zip(grid["H"], grid["H"][1:]):
                n += 1
                a, b = g(comp[(ckey(c), h0, pol, d0)], "SUCCESS"), g(comp[(ckey(c), h1, pol, d0)], "SUCCESS")
                if b < a:
                    bad.append((ckey(c), pol, h0, h1, str(a), str(b)))
    res["composite_SUCCESS_vs_H"] = report(bad, n, "SUCCESS non-decreasing in H (per policy)")
    div = {k: g(v[0], "DIVERGED_S_AHEAD") + g(v[0], "DIVERGED_G_AHEAD") for k, v in ex.items()}
    pairs = list(axis_pairs(grid, "B"))
    inc = sum(1 for lo, hi in pairs if div[hi] > div[lo])
    res["divergence_vs_B_descriptive"] = {"pairs": len(pairs), "pairs_where_divergence_increases_with_B": inc, "note": "reported, not asserted"}
    return res


def h_e2b(grid, ex):
    bad, n = [], 0
    rest = [k for k in ("p", "K", "B", "L", "r")]
    for combo in itertools.product(*(grid[k] for k in rest)):
        base = dict(zip(rest, combo), activation="gated")
        vals = [g(ex[ckey(dict(base, persist=pl))][0], "DIVERGED_G_AHEAD") for pl in PERSIST_ORDER]
        for i in (0, 1):
            n += 1
            if vals[i] < vals[i + 1]:
                bad.append((combo, PERSIST_ORDER[i], PERSIST_ORDER[i + 1], str(vals[i]), str(vals[i + 1])))
    return report(bad, n, "gated: P(G-ahead) non-increasing with persistence durability")


def x_total_divergence_vs_persistence(grid, ex):
    """EXPLORATORY, added post hoc after a tiny-grid check showed H-E2b witnesses (journal can raise G-ahead alone because it stops
    restart-terminal losses and lets more attempts end at step 4). Not part of the frozen hypotheses; reported separately."""
    bad, n = [], 0
    rest = ("p", "K", "B", "L", "r", "activation")
    for combo in itertools.product(*(grid[k] for k in rest)):
        base = dict(zip(rest, combo))
        vals = []
        for pl in PERSIST_ORDER:
            o = ex[ckey(dict(base, persist=pl))][0]
            vals.append(g(o, "DIVERGED_S_AHEAD") + g(o, "DIVERGED_G_AHEAD"))
        for i in (0, 1):
            n += 1
            if vals[i] < vals[i + 1]:
                bad.append((combo, PERSIST_ORDER[i], PERSIST_ORDER[i + 1], str(vals[i]), str(vals[i + 1])))
    return report(bad, n, "EXPLORATORY: total divergence non-increasing with persistence durability")


def h_e2c(grid, ex):
    bad_j, nj, bad_v, nv = [], 0, [], 0
    for act in grid["activation"]:
        for combo in itertools.product(grid["p"], grid["K"], grid["B"], grid["L"]):
            base = dict(zip(("p", "K", "B", "L"), combo), activation=act)
            dists = [ex[ckey(dict(base, r=r, persist="journal"))][1] for r in grid["r"]]
            for d in dists[1:]:
                nj += 1
                if d != dists[0]:
                    bad_j.append((combo, act))
            lock = [(lambda o: g(o, "DIVERGED_S_AHEAD") + g(o, "DIVERGED_G_AHEAD"))(ex[ckey(dict(base, r=r, persist="volatile"))][0]) for r in grid["r"]]
            for a, b in zip(lock, lock[1:]):
                nv += 1
                if b < a:
                    bad_v.append((combo, act, str(a), str(b)))
    return {"journal_invariant_to_r": report(bad_j, nj, "journal distribution identical across r"),
            "volatile_divergence_nondecreasing_in_r": report(bad_v, nv, "volatile divergence non-decreasing in r")}


def h_e3(grid, comp):
    d0, Hs = grid["detect"][0], grid["H"]
    lo, hi = Hs[0], Hs[-1]
    n_all = n_ind = prim = sec = lever_ind = lever_all = 0
    ex_prim, ex_sec = [], []
    for c in configs(grid):
        k = ckey(c)
        e_lo, e_hi, r_hi = (comp[(k, lo, "expired_only", d0)], comp[(k, hi, "expired_only", d0)], comp[(k, hi, "resume", d0)])
        dS = g(e_hi, "SUCCESS") - g(e_lo, "SUCCESS")
        gain = g(r_hi, "SUCCESS") - g(e_hi, "SUCCESS")
        n_all += 1
        lever_all += gain > dS
        if g(e_hi, "INDETERMINATE") > 0:
            n_ind += 1
            prim += dS < g(e_hi, "INDETERMINATE")
            lever_ind += gain > dS
            if dS >= g(e_hi, "INDETERMINATE") and len(ex_prim) < 5:
                ex_prim.append((k, str(dS), str(g(e_hi, "INDETERMINATE"))))
        if g(e_lo, "INDETERMINATE") > 0:
            sec += dS < g(e_lo, "INDETERMINATE")
            if dS >= g(e_lo, "INDETERMINATE") and len(ex_sec) < 5:
                ex_sec.append((k, str(dS), str(g(e_lo, "INDETERMINATE"))))
    n_ind_lo = sum(1 for c in configs(grid) if g(comp[(ckey(c), lo, "expired_only", d0)], "INDETERMINATE") > 0)
    return {"points": n_all, "points_with_INDETERMINATE_mass_at_H_hi": n_ind, "primary_dS_lt_IND_hi": {"holds": prim, "of": n_ind, "counterexamples": [str(x) for x in ex_prim]},
            "secondary_dS_lt_IND_lo": {"holds": sec, "of": n_ind_lo, "counterexamples": [str(x) for x in ex_sec]},
            "resume_gain_gt_dS_over_points_with_IND_mass": {"holds": lever_ind, "of": n_ind}, "resume_gain_gt_dS_over_all_points": {"holds": lever_all, "of": n_all}}


def h_e4(grid, comp, thr_frac=F(95, 100), thr_delay=F(1, 100)):
    Hmax = grid["H"][-1]
    out = {"thresholds": {"almost_always": str(thr_frac), "delay_matters": str(thr_delay)}, "recovery_fraction": {}, "detection_delay": {}}
    for pol in grid["policy"]:
        fr = []
        for c in configs(grid):
            o = comp[(ckey(c), Hmax, pol, grid["detect"][0])]
            den = g(o, "RECOVERED") + g(o, "UNRECOVERED_DIVERGED")
            if den > 0:
                fr.append(g(o, "RECOVERED") / den)
        fr.sort()
        n = len(fr)
        out["recovery_fraction"][pol] = {"points_with_divergence": n, "share_ge_threshold": (float(sum(1 for x in fr if x >= thr_frac)) / n if n else None),
                                          "min": float(fr[0]) if n else None, "median": float(fr[n // 2]) if n else None}
    for H in grid["H"]:
        by_p = defaultdict(lambda: [0, 0, F(0)])
        for c in configs(grid):
            for pol in grid["policy"]:
                vals = [g(comp[(ckey(c), H, pol, d)], "UNRECOVERED_DIVERGED") for d in grid["detect"]]
                rng = max(vals) - min(vals)
                s = by_p[str(c["p"])]
                s[0] += 1
                s[1] += rng > thr_delay
                s[2] = max(s[2], rng)
        out["detection_delay"]["H=%d" % H] = {p: {"points": s[0], "delay_matters": s[1], "max_range": float(s[2])} for p, s in sorted(by_p.items())}
    return out


def h_e5(grid, ex):
    higher = lower = equal = invalid = 0
    wit_hi, wit_lo, maxdiff = [], [], F(0)
    for m in (2, 4):
        for p in grid["p"]:
            try:
                a, b, pb = ge_matched(p, m)
            except ValueError:
                invalid += 1
                continue
            for K, B, L, r, pl, act in itertools.product(grid["K"], grid["B"], grid["L"], grid["r"], grid["persist"], grid["activation"]):
                base = dict(p=p, K=K, B=B, L=L, r=r, persist=pl, activation=act)
                s_iid = g(ex[ckey(base)][0], "SUCCESS")
                s_ge = g(outcome_probs(exact_distribution(Params(p=F(0), K=K, B=B, L=L, r=r, persist=pl, activation=act, ge=(a, b, pb)), exact=True)), "SUCCESS")
                d = s_ge - s_iid
                maxdiff = max(maxdiff, abs(d))
                if d > 0:
                    higher += 1
                    if len(wit_hi) < 3:
                        wit_hi.append((m, tuple(base.values()), str(d)))
                elif d < 0:
                    lower += 1
                    if len(wit_lo) < 3:
                        wit_lo.append((m, tuple(base.values()), str(d)))
                else:
                    equal += 1
    return {"bursty_higher": higher, "bursty_lower": lower, "equal": equal, "invalid_combinations_skipped": invalid, "max_abs_difference": float(maxdiff),
            "witness_in_both_directions": higher > 0 and lower > 0, "examples_higher": [str(x) for x in wit_hi], "examples_lower": [str(x) for x in wit_lo]}


def run_all(grid):
    ex = exchange_table(grid)
    comp = composite_table(grid)
    return {"grid_sizes": {k: len(v) for k, v in grid.items()}, "table_sha256": table_digest(ex, comp),
            "H-E2a": h_e2a(grid, ex, comp), "H-E2b": h_e2b(grid, ex), "H-E2c": h_e2c(grid, ex),
            "H-E3": h_e3(grid, comp), "exploratory_post_hoc": x_total_divergence_vs_persistence(grid, ex), "H-E4": h_e4(grid, comp), "H-E5": h_e5(grid, ex), "operationalisation": OPERATIONALISATION}
