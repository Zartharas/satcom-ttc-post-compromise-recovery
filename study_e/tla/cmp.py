import re, os, sys, itertools
sys.path.insert(0, sys.argv[2])
from fractions import Fraction as F
from study_e.params import Params
from study_e.model import exact_distribution
txt = open(sys.argv[1]).read(); tla = {}
for blk in txt.split("State ")[1:]:
    d = dict(re.findall(r'/\\ (\w+) = "?([\w]+)"?', blk))
    if d['ph'] == 'done':
        tla.setdefault((int(d['K']), int(d['B']), int(d['L']), d['Pers'], d['Act']), set()).add((d['out'], int(d['T'])))
bad = n = 0
for K, B, L, pers, act in itertools.product(range(1, 4), range(1, 9), range(1, 4), ("volatile", "commit", "journal"), ("local", "gated")):
    P = Params(p=F(1, 3), K=K, B=B, L=L, r=F(1, 4), persist=pers, activation=act)
    py = {k for k, v in exact_distribution(P, exact=True).items() if v > 0}
    n += 1; bad += py != tla.get((K, B, L, pers, act), set())
print("configs", n, "mismatches", bad)
