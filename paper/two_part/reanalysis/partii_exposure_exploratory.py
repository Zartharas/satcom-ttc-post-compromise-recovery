#!/usr/bin/env python3
"""EXPLORATORY exposure metric for the Part II Recovery-SA fallback (R0).

Not part of the frozen confirmatory analysis and not pre-registered. Uses the
frozen model code unchanged (study_e.recovery.recovery_time_distribution) and
the frozen R0 parameters. For a divergence that triggers the R0 re-bootstrap it
reports contacts elapsed until restored command authority, capped at the
horizon H, over the frozen p, K and detection-delay values. Exact arithmetic
is not used here; floats suffice for a descriptive table.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "study_e"))
from study_e.recovery import recovery_time_distribution  # noqa: E402

P = [0.05, 0.1, 0.2, 0.3, 0.5]
K = [2, 3, 4, 6]
DETECT = [1, 3, 5]
H = 20
R0 = dict(n_msgs=4, B0=8, L0=3)


def row(p, k, d):
    dist = recovery_time_distribution(p, k, R0["n_msgs"], R0["B0"], R0["L0"], d, H)
    nr = dist.pop("NOT_RECOVERED", 0.0)
    done = sum(dist.values())
    assert abs(done + nr - 1.0) < 1e-9
    exp_capped = sum(t * w for t, w in dist.items()) + nr * H
    return {"p": p, "K": k, "detect": d, "p_restored_within_H": done,
            "p_not_restored": nr, "expected_contacts_capped_at_H": exp_capped}


def main():
    rows = [row(p, k, d) for p in P for k in K for d in DETECT]
    out = {"status": "EXPLORATORY_NOT_PREREGISTERED", "H": H, "R0": R0, "rows": rows}
    path = pathlib.Path(sys.argv[1])
    path.write_text(json.dumps(out, indent=1) + "\n")
    for p in P:
        sel = [r for r in rows if r["p"] == p and r["K"] == 4]
        print("p=%.2f K=4:" % p, " ".join("d%d: E=%.2f notrec=%.4f" % (r["detect"], r["expected_contacts_capped_at_H"], r["p_not_restored"]) for r in sel))
    return 0


if __name__ == "__main__":
    sys.exit(main())
