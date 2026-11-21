"""Exact forward DP over the absorbing chain. Works with floats or Fractions."""
from collections import defaultdict
from fractions import Fraction
from . import rules

_BUDGET_FUDGE = 0  # test hook for mutation testing only; must stay 0
_GE_MUT = 0        # test hook for mutation testing only; must stay 0 (1: swap channel transitions, 2: swap state losses)


def exact_distribution(params, exact=False, start_step=0, with_step=False):
    """Returns {(outcome, T): probability}, T = contact index at which the attempt ended.
    start_step: exchange step already completed when the attempt starts (resumable verification; default 0).
    with_step: if True the keys are (outcome, T, step_reached)."""
    def key(o, c, st):
        return (o, c, st) if with_step else (o, c)

    cast = Fraction if exact else float
    p, r = cast(params.p), cast(params.r)
    one, zero = cast(1), cast(0)
    B = params.B + _BUDGET_FUDGE
    out = defaultdict(lambda: zero)
    ge = params.ge
    if ge is not None:
        ga, gb, gpb = (cast(x) for x in ge)
        pi_b = ga / (ga + gb)
        trans = {0: ((0, 1 - ga), (1, ga)), 1: ((0, gb), (1, 1 - gb))}
        loss = {0: p, 1: gpb}
        if _GE_MUT == 1:
            trans = {0: ((0, ga), (1, 1 - ga)), 1: ((0, 1 - gb), (1, gb))}
        if _GE_MUT == 2:
            loss = {0: gpb, 1: p}
    state = {(start_step, 0): one}  # (step, tx_used) at start of the contact
    for c in range(1, params.L + 1):
        if ge is None:
            st = {(sp, tx, None): pr for (sp, tx), pr in state.items()}
        else:  # channel redrawn from stationary law at each contact start
            st = defaultdict(lambda: zero)
            for (sp, tx), pr in state.items():
                st[(sp, tx, 0)] += pr * (1 - pi_b)
                st[(sp, tx, 1)] += pr * pi_b
        for _ in range(params.K):
            nxt = defaultdict(lambda: zero)
            for (step, tx, ch), pr in st.items():
                tx2 = tx + 1
                lp = p if ch is None else loss[ch]
                for ok, w in ((True, 1 - lp), (False, lp)):
                    if w == 0:
                        continue
                    s2 = step + 1 if ok else step
                    mass = pr * w
                    if s2 >= rules.N_STEPS:
                        out[key("SUCCESS", c, s2)] += mass
                    elif tx2 >= B:
                        out[key(rules.classify(s2, params.activation), c, s2)] += mass
                    elif ch is None:
                        nxt[(s2, tx2, None)] += mass
                    else:
                        for ch2, wt in trans[ch]:
                            if wt != 0:
                                nxt[(s2, tx2, ch2)] += mass * wt
            st = nxt
        state = defaultdict(lambda: zero)
        for (sp, tx, _ch), pr in st.items():
            state[(sp, tx)] += pr
        if c == params.L:
            for (step, tx), pr in state.items():
                out[key(rules.classify(step, params.activation), c, step)] += pr
            state = {}
            break
        nxt = defaultdict(lambda: zero)
        for (step, tx), pr in state.items():
            for restart, w in ((True, r), (False, 1 - r)):
                if w == 0:
                    continue
                mass = pr * w
                if not restart:
                    nxt[(step, tx)] += mass
                    continue
                kind, val = rules.restart_effect(step, params.persist, params.activation)
                if kind == "TERMINAL":
                    out[key(val, c, step)] += mass
                else:
                    nxt[(val, tx)] += mass
        state = nxt
    return dict(out)


def outcome_probs(dist):
    agg = defaultdict(lambda: 0)
    for (o, _t), pr in dist.items():
        agg[o] += pr
    return dict(agg)


def lockout_prob(dist):
    o = outcome_probs(dist)
    return o.get("DIVERGED_S_AHEAD", 0) + o.get("DIVERGED_G_AHEAD", 0)


def expected_contacts(dist):
    tot = sum(dist.values())
    return sum(t * pr for (_o, t), pr in dist.items()) / tot
