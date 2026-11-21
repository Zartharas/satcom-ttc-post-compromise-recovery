import re, sys, itertools
sys.path.insert(0, sys.argv[2])
from fractions import Fraction as F
from study_e.params import Params
from study_e.multi import run_distribution
txt = open(sys.argv[1]).read(); tla = {}
for blk in txt.split("State ")[1:]:
    d = dict(re.findall(r'/\\ (\w+) = "?([\w]+)"?', blk))
    if d['ph'] == 'done':
        tla.setdefault((int(d['K']), int(d['B']), int(d['L']), int(d['H']), d['Pers'], d['Act']), set()).add((d['out'], int(d['T']), int(d['A'])))
bad = n = 0
for K, B, L, H, pers, act in itertools.product(range(1, 4), range(1, 9), range(1, 4), range(1, 7), ("volatile", "commit", "journal"), ("local", "gated")):
    P = Params(p=F(1, 3), K=K, B=B, L=L, r=F(1, 4), persist=pers, activation=act)
    py = {k for k, v in run_distribution(P, H, exact=True).items() if v > 0}
    n += 1
    if py != tla.get((K, B, L, H, pers, act), set()):
        bad += 1
        if bad <= 3: print("DIFF", (K, B, L, H, pers, act), sorted(py ^ tla.get((K, B, L, H, pers, act), set()))[:4])
print("configs", n, "with TLC sets", len(tla), "mismatches", bad)
