import itertools
import unittest
from fractions import Fraction as F
from study_e.params import Params
from study_e.multi import run_distribution, outcome_probs
from study_e.sim import enumerate_distribution, run_multi
from study_e.composite import composite_outcomes


class Resume(unittest.TestCase):
    def test_default_unchanged_and_sums_to_one(self):
        P = Params(p=F(1, 2), K=2, B=6, L=2, r=F(1, 5), persist="commit", activation="local")
        a = run_distribution(P, 8, exact=True)
        self.assertEqual(a, run_distribution(P, 8, exact=True, resume=False))
        self.assertEqual(sum(run_distribution(P, 8, exact=True, resume=True).values()), 1)

    def test_dp_equals_enumeration_with_resume(self):
        n = 0
        for K, L, B, H, pers, act, r in itertools.product((1, 2), (1, 2), (3, 5), (2, 4),
                                                         ("volatile", "journal"), ("local", "gated"), (F(0), F(1, 4))):
            P = Params(p=F(1, 2), K=K, B=B, L=L, r=r, persist=pers, activation=act)
            runner = lambda Q, H=H: run_multi(Q, H, resume=True)
            self.assertEqual(run_distribution(P, H, exact=True, resume=True), enumerate_distribution(P, runner),
                             (K, L, B, H, pers, act, r))
            n += 1
        self.assertGreater(n, 50)

    def test_resume_dominates_restart_and_expired_only(self):
        P = Params(p=F(3, 10), K=3, B=8, L=3, r=F(1, 10), persist="commit", activation="gated")
        s = lambda **kw: outcome_probs(run_distribution(P, 12, exact=True, **kw)).get("SUCCESS", 0)
        base = s()
        restart = s(retry_on=("EXPIRED_OLD", "INDETERMINATE"))
        resume = s(resume=True)
        self.assertGreater(resume, base)
        self.assertGreaterEqual(resume, restart)

    def test_resume_leaves_no_indeterminate_when_horizon_is_long(self):
        P = Params(p=F(1, 4), K=3, B=12, L=4, r=0, persist="journal", activation="local")
        o = outcome_probs(run_distribution(P, 60, resume=True))
        self.assertLess(o.get("INDETERMINATE", 0), 1e-9)
        # with r=0 the only non-success end is the S-ahead window (exactly 3 steps at an attempt end)
        self.assertAlmostEqual(o.get("SUCCESS", 0) + o.get("DIVERGED_S_AHEAD", 0), 1.0, places=9)

    def test_composite_accepts_resume(self):
        P = Params(p=F(3, 10), K=3, B=8, L=3, r=F(1, 10), persist="volatile", activation="gated")
        c = composite_outcomes(P, 10, 4, 8, 3, 1, exact=True, resume=True)
        self.assertEqual(sum(c.values()), 1)
        self.assertLess(c.get("INDETERMINATE", 0), composite_outcomes(P, 10, 4, 8, 3, 1, exact=True).get("INDETERMINATE", 0))


if __name__ == "__main__":
    unittest.main()
