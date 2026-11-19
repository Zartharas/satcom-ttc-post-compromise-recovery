"""R0: Recovery-SA re-bootstrap after sustained authentication failure (SDLS-DR design, Sec. on state loss and recovery).

Source text (see docs/R0_R2_SOURCES.md): the recovery association is statically keyed, always available, and used only to
re-provision the ratchet state; the ground segment detects sustained authentication failure, re-provisions a fresh root key
and identity keypair, then repeats the bootstrap stage. The paper gives NO message count, so n_msgs is a model parameter.
Model: after a detection delay of `detect` contacts, a chain of n_msgs messages is exchanged over the static recovery SA
(K slots per contact, budget B0 transmissions, lifetime L0 contacts per attempt). The recovery SA holds static state, so a
spacecraft restart cannot desynchronise it (no restart model); a failed attempt restarts at the next contact.
"""
from collections import defaultdict
from fractions import Fraction


def attempt_distribution(p, K, n_msgs, B0, L0, exact=False):
    """{('DONE'|'FAIL', contacts_used): probability} for one recovery-exchange attempt."""
    cast = Fraction if exact else float
    p = cast(p)
    q = 1 - p
    zero = cast(0)
    out = defaultdict(lambda: zero)
    state = {(0, 0): cast(1)}
    for c in range(1, L0 + 1):
        for _ in range(K):
            nxt = defaultdict(lambda: zero)
            for (step, tx), pr in state.items():
                for ok, w in ((True, q), (False, p)):
                    if w == 0:
                        continue
                    s2, t2, m = step + (1 if ok else 0), tx + 1, pr * w
                    if s2 >= n_msgs:
                        out[("DONE", c)] += m
                    elif t2 >= B0:
                        out[("FAIL", c)] += m
                    else:
                        nxt[(s2, t2)] += m
            state = nxt
        if c == L0:
            for pr in state.values():
                out[("FAIL", c)] += pr
            state = {}
    return dict(out)


def recovery_time_distribution(p, K, n_msgs, B0, L0, detect, H, exact=False):
    """Contacts after the loss event until the recovery SA has re-bootstrapped, at most H contacts in total.
    Returns {t: prob} for t = contacts elapsed at completion, plus key 'NOT_RECOVERED' for the remainder."""
    zero = Fraction(0) if exact else 0.0
    pend = defaultdict(lambda: zero)
    pend[detect] = Fraction(1) if exact else 1.0           # attempt starts after `detect` contacts
    out = defaultdict(lambda: zero)
    for s in range(detect, H):
        pr = pend.pop(s, zero)
        if pr == 0:
            continue
        Le = min(L0, H - s)
        for (o, t), w in attempt_distribution(p, K, n_msgs, B0, Le, exact).items():
            end = s + t
            if o == "DONE":
                out[end] += pr * w
            elif end < H:
                pend[end] += pr * w
            else:
                out["NOT_RECOVERED"] += pr * w
    if detect >= H:
        out["NOT_RECOVERED"] += Fraction(1) if exact else 1.0
    return dict(out)
