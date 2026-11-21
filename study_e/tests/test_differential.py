import itertools
import os
import unittest
from fractions import Fraction as F
from study_e.params import Params
from study_e.model import exact_distribution
from study_e.sim import enumerate_distribution, monte_carlo
from study_e.model import outcome_probs

FULL = os.environ.get("STUDY_E_FULL") == "1"


def grid():
    ps = (F(1, 4), F(1, 2), F(3, 4)) if FULL else (F(1, 2), F(3, 4))
    Ks = (1, 2, 3) if FULL else (1, 2)
    Ls = (1, 2, 3)
    Bs = (2, 3, 4, 5, 6) if FULL else (2, 4, 6)
    rs = (F(0), F(1, 4))
    for p, K, L, B, r, pers, act in itertools.product(ps, Ks, Ls, Bs, rs,
                                                      ("volatile", "commit", "journal"),
                                                      ("local", "gated")):
        yield Params(p=p, K=K, B=B, L=L, r=r, persist=pers, activation=act)


class Differential(unittest.TestCase):
    def test_dp_equals_exhaustive_enumeration_exactly(self):
        n = 0
        for P in grid():
            self.assertEqual(exact_distribution(P, exact=True), enumerate_distribution(P), P)
            n += 1
        self.assertGreater(n, 100)

    def test_monte_carlo_agrees_within_4_5_standard_errors(self):
        pts = [Params(p=F(1, 4), K=2, B=8, L=4, r=F(1, 10), persist="volatile", activation="gated"),
               Params(p=F(1, 2), K=3, B=9, L=3, r=F(1, 5), persist="commit", activation="local"),
               Params(p=F(3, 10), K=2, B=7, L=5, r=F(1, 20), persist="journal", activation="local")]
        N = 40000
        for i, P in enumerate(pts):
            exact = outcome_probs(exact_distribution(P, exact=True))
            mc, _ = monte_carlo(P, N, seed=20261201 + i)
            mco = {}
            for (o, _t), v in mc.items():
                mco[o] = mco.get(o, 0) + v
            for o in set(exact) | set(mco):
                pe = float(exact.get(o, 0))
                se = max((pe * (1 - pe) / N) ** 0.5, 1e-9)
                self.assertLessEqual(abs(mco.get(o, 0) - pe), 4.5 * se + 1e-9, (P, o))

    def test_monte_carlo_is_reproducible_for_a_fixed_seed(self):
        P = Params(p=F(1, 3), K=2, B=7, L=4, r=F(1, 10), persist="volatile")
        self.assertEqual(monte_carlo(P, 2000, seed=7), monte_carlo(P, 2000, seed=7))


if __name__ == "__main__":
    unittest.main()
