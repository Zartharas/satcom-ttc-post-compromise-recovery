"""Multi-attempt recovery: exact DP composed from the single-attempt DP (model.py). See docs/MULTI_ATTEMPT_RULES.md."""
from collections import defaultdict
from dataclasses import replace
from fractions import Fraction
from .model import exact_distribution

DEFAULT_RETRY = ("EXPIRED_OLD",)


def run_distribution(params, H, retry_on=DEFAULT_RETRY, exact=False, resume=False):
    """Returns {(outcome, end_contact, attempts): probability} for a run of at most H contacts.
    resume=True adds resumable verification: an INDETERMINATE end is retried from the next contact CONTINUING from the
    step reached (sensitivity option b); retry_on containing INDETERMINATE without resume restarts at step 0."""
    if H < 1:
        raise ValueError("H must be >= 1")
    zero = Fraction(0) if exact else 0.0
    one = Fraction(1) if exact else 1.0
    cache = {}
    pending = defaultdict(lambda: zero)  # (start_contact, attempt_no, start_step) -> probability
    pending[(1, 1, 0)] = one
    out = defaultdict(lambda: zero)
    for s in range(1, H + 1):
        for key in sorted(k for k in pending if k[0] == s):
            pr = pending.pop(key)
            a, step0 = key[1], key[2]
            Le = min(params.L, H - s + 1)
            if (Le, step0) not in cache:
                cache[(Le, step0)] = exact_distribution(replace(params, L=Le), exact=exact, start_step=step0, with_step=True)
            for (o, t, stp), w in cache[(Le, step0)].items():
                g = s + t - 1
                if g < H and resume and o == "INDETERMINATE":
                    pending[(g + 1, a + 1, stp)] += pr * w
                elif o in retry_on and g < H:
                    pending[(g + 1, a + 1, 0)] += pr * w
                else:
                    out[(o, g, a)] += pr * w
    return dict(out)


def outcome_probs(dist):
    agg = defaultdict(lambda: 0)
    for (o, _g, _a), pr in dist.items():
        agg[o] += pr
    return dict(agg)


def expected_attempts(dist):
    return sum(a * pr for (_o, _g, a), pr in dist.items()) / sum(dist.values())
