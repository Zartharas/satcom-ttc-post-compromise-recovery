"""Independent path simulator, written separately from rules.py/model.py.

run_path is a generator: it yields the probability of each Bernoulli draw and receives the
outcome (bool). It is driven by random draws (Monte Carlo) or by systematic replay
(exhaustive enumeration). Deterministic draws (prob 0 or 1) are not yielded.
"""
import random
from collections import defaultdict
from fractions import Fraction

_S_THRESH = {"local": 3, "gated": 5}


def _cls(step, act):
    if step >= 6:
        return "SUCCESS"
    sa, ga = step >= _S_THRESH[act], step >= 4
    return {(True, True): "INDETERMINATE", (True, False): "DIVERGED_S_AHEAD",
            (False, True): "DIVERGED_G_AHEAD", (False, False): "EXPIRED_OLD"}[(sa, ga)]


def _sim_restart(step, persist, act):
    sa, ga = step >= _S_THRESH[act], step >= 4
    survives = (persist == "journal") or (persist == "commit" and sa)
    if survives:
        return ("go", step)
    return ("end", "DIVERGED_G_AHEAD") if ga else ("go", 0)


def _draw(prob):
    """Generator helper: Bernoulli(prob); deterministic when prob is 0 or 1."""
    if prob == 0:
        return False
    if prob == 1:
        return True
    return (yield prob)


def run_path(params, step0=0, with_step=False):
    p, r = params.p, params.r
    ge = params.ge
    step, tx = step0, 0
    R = (lambda o, c: (o, c, step)) if with_step else (lambda o, c: (o, c))
    for c in range(1, params.L + 1):
        if ge is not None:
            ga, gb, gpb = ge
            bad = yield from _draw(ga / (ga + gb))
        for slot in range(params.K):
            tx += 1
            lp = p if (ge is None or not bad) else gpb
            ok = yield from _draw(1 - lp)
            step += 1 if ok else 0
            if step == 6:
                return R("SUCCESS", c)
            if tx == params.B:
                return R(_cls(step, params.activation), c)
            if ge is not None and slot < params.K - 1:
                bad = yield from _draw(ga if not bad else 1 - gb)
        if c == params.L:
            return R(_cls(step, params.activation), c)
        restart = yield from _draw(r)
        if restart:
            kind, val = _sim_restart(step, params.persist, params.activation)
            if kind == "end":
                return R(val, c)
            step = val


def _replay(params, prefix, runner=None):
    """Run the generator forcing `prefix`; returns (weight, result|None, next_prob|None)."""
    gen = (runner or run_path)(params)
    w = Fraction(1) if isinstance(params.p, Fraction) else 1.0
    try:
        pr = next(gen)
        i = 0
        while True:
            if i < len(prefix):
                d = prefix[i]
                w = w * (pr if d else 1 - pr)
                i += 1
                pr = gen.send(d)
            else:
                return w, None, pr
    except StopIteration as e:
        return w, e.value, None


def enumerate_distribution(params, runner=None):
    """Exhaustive path enumeration. Exact when p and r are Fractions."""
    out = defaultdict(lambda: 0)
    stack = [()]
    while stack:
        prefix = stack.pop()
        w, res, pr = _replay(params, prefix, runner)
        if res is not None:
            out[res] += w
        else:
            stack.append(prefix + (True,))
            stack.append(prefix + (False,))
    return dict(out)


def monte_carlo(params, n, seed, runner=None):
    rng = random.Random(seed)
    counts = defaultdict(int)
    for _ in range(n):
        gen = (runner or run_path)(params)
        try:
            pr = next(gen)
            while True:
                pr = gen.send(rng.random() < float(pr))
        except StopIteration as e:
            counts[e.value] += 1
    return {k: v / n for k, v in counts.items()}, n


def run_multi(params, H, retry_on=("EXPIRED_OLD",), resume=False):
    """Multi-attempt run (horizon H contacts). An attempt that ends EXPIRED_OLD (or any outcome in retry_on) before the
    horizon is retried from the next contact with a fresh budget/lifetime, restarting the exchange at step 0.
    If resume=True, an INDETERMINATE end is retried too but RESUMES from the step reached (resumable verification).
    Returns (outcome, end_contact, attempts)."""
    from dataclasses import replace
    s, a, step0 = 1, 1, 0
    while True:
        o, t, stp = yield from run_path(replace(params, L=min(params.L, H - s + 1)), step0, True)
        g = s + t - 1
        if g < H and resume and o == "INDETERMINATE":
            s, a, step0 = g + 1, a + 1, stp
            continue
        if o in retry_on and g < H:
            s, a, step0 = g + 1, a + 1, 0
            continue
        return (o, g, a)
