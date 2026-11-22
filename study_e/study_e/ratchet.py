"""R2: bounded skipped-key cache desynchronisation (frame-level), exact DP.

Model (docs/R0_R2_SOURCES.md): frames 1..n are sent in order; each is lost independently (probability p) or, with a
Gilbert-Elliott channel, per channel state. The receiver can skip at most `cmax` missing frames between two received
frames. If a received frame follows a gap of more than `cmax` consecutive lost frames, it is rejected, the live state is
not advanced, and every later frame shows an even larger gap, so the association is desynchronised until recovery.
Trailing losses at the end of the window are not yet observable. cmax is a MODEL PARAMETER (SDLS-DR only says the
cache is bounded).
"""
from collections import defaultdict
from fractions import Fraction


def desync_probability(n, p, cmax, exact=False, ge=None):
    """P(a desynchronising gap occurs within n frames). State = current run of consecutive lost frames (0..cmax+1 capped)."""
    cast = Fraction if exact else float
    p = cast(p)
    zero = cast(0)
    if ge is None:
        st = {(0, None): cast(1)}
        loss = {None: p}
        trans = {None: ((None, cast(1)),)}
    else:
        a, b, pb = (cast(x) for x in ge)
        pi_b = a / (a + b)
        st = {(0, 0): 1 - pi_b, (0, 1): pi_b}
        loss = {0: p, 1: pb}
        trans = {0: ((0, 1 - a), (1, a)), 1: ((0, b), (1, 1 - b))}
    bad = zero
    for _ in range(n):
        nxt = defaultdict(lambda: zero)
        for (run, ch), pr in st.items():
            lp = loss[ch]
            if 1 - lp != 0:           # received
                if run > cmax:
                    bad += pr * (1 - lp)
                else:
                    for ch2, w in trans[ch]:
                        if w != 0:
                            nxt[(0, ch2)] += pr * (1 - lp) * w
            if lp != 0:               # lost
                for ch2, w in trans[ch]:
                    if w != 0:
                        nxt[(min(run + 1, cmax + 1), ch2)] += pr * lp * w
        st = nxt
    return bad


def desync_enumerate(n, p, cmax, ge=None):
    """Independent brute force over all loss patterns (2^n, or 4^n with a GE channel). Exact (Fractions)."""
    from itertools import product
    p = Fraction(p)
    if ge is not None:
        return _enumerate_ge(n, p, cmax, ge)
    total = Fraction(0)
    for pattern in product((True, False), repeat=n):          # True = received
        w = Fraction(1)
        run, bad = 0, False
        for rec in pattern:
            w *= (1 - p) if rec else p
            if rec:
                if run > cmax:
                    bad = True
                run = 0
            else:
                run += 1
        if bad:
            total += w
    return total


def _enumerate_ge(n, p, cmax, ge):
    from itertools import product
    a, b, pb = (Fraction(x) for x in ge)
    pi_b = a / (a + b)
    total = Fraction(0)
    for chans in product((0, 1), repeat=n):                   # channel state per frame
        w = pi_b if chans[0] else 1 - pi_b
        for i in range(1, n):
            cur, prev = chans[i], chans[i - 1]
            w *= (a if cur else 1 - a) if prev == 0 else ((1 - b) if cur else b)
        if w == 0:
            continue
        for pattern in product((True, False), repeat=n):
            wp = w
            for rec, ch in zip(pattern, chans):
                lp = pb if ch else p
                wp *= (1 - lp) if rec else lp
            if wp == 0:
                continue
            run, bad = 0, False
            for rec in pattern:
                if rec:
                    if run > cmax:
                        bad = True
                        break
                    run = 0
                else:
                    run += 1
            if bad:
                total += wp
    return total
