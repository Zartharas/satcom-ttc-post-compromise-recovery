"""Sizes a CANDIDATE grid and times a small random sample. Executes no pre-registered analysis and writes no results.
Usage: python3 -I tools/size_grid.py   (from the study_e folder)"""
import itertools, random, sys, time
sys.path.insert(0, ".")
from fractions import Fraction as F
from study_e.params import Params
from study_e.composite import composite_outcomes

GRID = dict(p=[F(1, 20), F(1, 10), F(1, 5), F(3, 10), F(1, 2)], K=[2, 3, 4, 6], B=[4, 6, 8, 12], L=[1, 2, 3, 4],
            r=[F(0), F(1, 100), F(1, 20), F(1, 10)], persist=["volatile", "commit", "journal"], activation=["local", "gated"],
            H=[4, 8, 20], policy=["expired_only", "restart_indeterminate", "resume"], detect=[1, 3, 5])
n = 1
for v in GRID.values():
    n *= len(v)
print("candidate grid points:", n)
rng = random.Random(1)
keys = list(GRID)
pts = [dict(zip(keys, [rng.choice(GRID[k]) for k in keys])) for _ in range(40)]
t0 = time.time()
for d in pts:
    P = Params(p=d["p"], K=d["K"], B=d["B"], L=d["L"], r=d["r"], persist=d["persist"], activation=d["activation"])
    ret = ("EXPIRED_OLD", "INDETERMINATE") if d["policy"] == "restart_indeterminate" else ("EXPIRED_OLD",)
    composite_outcomes(P, d["H"], 4, 8, 3, d["detect"], retry_on=ret, resume=d["policy"] == "resume")
dt = (time.time() - t0) / len(pts)
print("mean seconds per point (float arithmetic): %.4f" % dt)
print("estimated single-core hours for the full grid: %.2f" % (dt * n / 3600))
