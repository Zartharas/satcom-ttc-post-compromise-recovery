from fractions import Fraction as F
from math import comb


def binom_pmf(n, k, q):
    return comb(n, k) * q**k * (1 - q) ** (n - k)


def binom_range(n, lo, hi, q):
    return sum(binom_pmf(n, k, q) for k in range(lo, min(hi, n) + 1))


def closed_form_loss_only(p, B, activation):
    """r=0 and K*L >= B: step reached == number of successes among B transmissions (capped at 6)."""
    q = 1 - p
    s_thr = {"local": 3, "gated": 5}[activation]
    res = {o: F(0) for o in ("SUCCESS", "INDETERMINATE", "EXPIRED_OLD", "DIVERGED_S_AHEAD", "DIVERGED_G_AHEAD")}
    for k in range(0, B + 1):
        pk = binom_pmf(B, k, q)
        step = min(k, 6)
        if step >= 6:
            o = "SUCCESS"
        else:
            s, g = step >= s_thr, step >= 4
            o = ("INDETERMINATE" if s and g else "DIVERGED_S_AHEAD" if s else
                 "DIVERGED_G_AHEAD" if g else "EXPIRED_OLD")
        res[o] += pk
    return res
