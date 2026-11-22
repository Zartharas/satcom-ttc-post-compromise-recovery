"""Composite scenario: multi-attempt exchange (multi.py) followed, on a divergence, by Recovery-SA re-bootstrap (recovery.py).

Single total horizon H_total contacts. The exchange runs as in multi.py (retry EXPIRED_OLD only). A DIVERGED_* end at contact g
(fallback required) triggers R0: after `detect` contacts the ground starts the re-bootstrap over the static Recovery SA with
the same loss probability and slot structure. INDETERMINATE and EXPIRED_OLD-at-horizon stay as they are (no recovery model).
Outcomes: SUCCESS, RECOVERED, UNRECOVERED_DIVERGED, INDETERMINATE, EXPIRED_OLD.
"""
from collections import defaultdict
from fractions import Fraction
from .multi import run_distribution
from .recovery import recovery_time_distribution


def composite_outcomes(params, H, n_msgs, B0, L0, detect, retry_on=("EXPIRED_OLD",), exact=False, resume=False):
    if params.ge is not None:
        raise ValueError("composite scenario uses i.i.d. loss for the recovery chain; ge not supported here")
    zero = Fraction(0) if exact else 0.0
    out = defaultdict(lambda: zero)
    cache = {}
    for (o, g, _a), pr in run_distribution(params, H, retry_on, exact, resume).items():
        if o in ("DIVERGED_S_AHEAD", "DIVERGED_G_AHEAD"):
            rem = H - g
            if rem not in cache:
                cache[rem] = recovery_time_distribution(params.p, params.K, n_msgs, B0, L0, detect, rem, exact) if rem > 0 else {"NOT_RECOVERED": Fraction(1) if exact else 1.0}
            nr = cache[rem].get("NOT_RECOVERED", zero)
            out["UNRECOVERED_DIVERGED"] += pr * nr
            out["RECOVERED"] += pr * (sum(cache[rem].values()) - nr)
        else:
            out[o] += pr
    return dict(out)
