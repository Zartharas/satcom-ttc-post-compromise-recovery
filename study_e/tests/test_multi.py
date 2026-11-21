import itertools
import os
import unittest
from fractions import Fraction as F
from math import comb, ceil
from study_e.params import Params
from study_e.multi import run_distribution, outcome_probs, expected_attempts
from study_e.sim import enumerate_distribution, monte_carlo, run_multi
from study_e import model


FULL = os.environ.get("STUDY_E_FULL") == "1"


class Multi(unittest.TestCase):
    def test_probabilities_sum_to_one(self):
        P = Params(p=F(1, 3), K=2, B=5, L=2, r=F(1, 5), persist="volatile", activation="gated")
        self.assertEqual(sum(run_distribution(P, 6, exact=True).values()), 1)

    def test_H_equal_L_matches_single_attempt_when_no_retry_possible(self):
        P = Params(p=F(1, 3), K=2, B=6, L=3, r=F(1, 4), persist="commit")
        multi = run_distribution(P, 3, exact=True)
        single = model.exact_distribution(P, exact=True)
        self.assertEqual({(o, t): v for (o, t, a), v in multi.items() if a == 1} , single)
        self.assertTrue(all(a == 1 for (_o, _t, a) in multi))

    def test_total_loss_closed_form(self):
        for K, B, L, H in [(2, 4, 3, 7), (1, 5, 2, 6), (3, 3, 5, 4)]:
            P = Params(p=1, K=K, B=B, L=L)
            d = run_distribution(P, H, exact=True)
            alen = min(L, ceil(B / K))
            self.assertEqual(d, {("EXPIRED_OLD", H, ceil(H / alen)): F(1)})

    def test_lossless_success_first_attempt(self):
        P = Params(p=0, K=2, B=6, L=3)
        self.assertEqual(run_distribution(P, 9, exact=True), {("SUCCESS", 3, 1): F(1)})

    def test_one_contact_attempts_geometric_closed_form(self):
        # K=6, L=1, B>=6, local activation, r irrelevant (single contact). Per attempt: success q^6;
        # EXPIRED_OLD iff <=2 of 6 slots succeed; otherwise terminal (S-ahead at 3, INDETERMINATE at 4-5).
        q = F(2, 3)
        pmf = lambda k: comb(6, k) * q**k * (1 - q) ** (6 - k)
        succ, exp = pmf(6), sum(pmf(k) for k in range(0, 3))
        for H in (1, 2, 5):
            d = run_distribution(Params(p=1 - q, K=6, B=6, L=1, r=F(1, 2), persist="volatile"), H, exact=True)
            got = outcome_probs(d)
            self.assertEqual(got.get("SUCCESS", 0), sum(exp ** (n - 1) * succ for n in range(1, H + 1)))
            self.assertEqual(got.get("EXPIRED_OLD", 0), exp ** H)
            self.assertEqual(got.get("DIVERGED_S_AHEAD", 0), sum(exp ** (n - 1) * pmf(3) for n in range(1, H + 1)))

    def test_success_nondecreasing_in_horizon(self):
        P = Params(p=F(1, 2), K=2, B=6, L=2, r=F(1, 10), persist="commit", activation="gated")
        prev = -1
        for H in range(1, 9):
            v = outcome_probs(run_distribution(P, H, exact=True)).get("SUCCESS", 0)
            self.assertGreaterEqual(v, prev)
            prev = v

    def test_retry_policy_matters(self):
        P = Params(p=F(1, 2), K=2, B=6, L=2, r=0, persist="journal", activation="local")
        a = run_distribution(P, 6, exact=True)
        b = run_distribution(P, 6, retry_on=("EXPIRED_OLD", "INDETERMINATE"), exact=True)
        self.assertNotEqual(a, b)

    def test_dp_equals_enumeration(self):
        n = 0
        for K, L, B, H, pers, act, r in itertools.product((1, 2), (1, 2), (2, 4, 6), (1, 3, 4) if FULL else (1, 3),
                                                         ("volatile", "commit", "journal"),
                                                         ("local", "gated"), (F(0), F(1, 4))):
            P = Params(p=F(1, 2), K=K, B=B, L=L, r=r, persist=pers, activation=act)
            runner = lambda Q, H=H: run_multi(Q, H)
            self.assertEqual(run_distribution(P, H, exact=True), enumerate_distribution(P, runner), (K, L, B, H, pers, act, r))
            n += 1
        self.assertGreater(n, 100)

    def test_dp_equals_enumeration_bursty(self):
        ge = (F(1, 5), F(1, 3), F(4, 5))
        for K, L, B, H in itertools.product((1, 2), (1, 2), (3, 5), (2, 4)):
            P = Params(p=F(1, 10), K=K, B=B, L=L, r=F(1, 5), persist="volatile", activation="gated", ge=ge)
            runner = lambda Q, H=H: run_multi(Q, H)
            self.assertEqual(run_distribution(P, H, exact=True), enumerate_distribution(P, runner))

    def test_monte_carlo_agreement(self):
        P = Params(p=F(2, 5), K=2, B=6, L=2, r=F(1, 10), persist="volatile", activation="local")
        H, N = 6, 40000
        runner = lambda Q: run_multi(Q, H)
        exact = run_distribution(P, H, exact=True)
        mc, _ = monte_carlo(P, N, seed=20261201, runner=runner)
        for k in set(exact) | set(mc):
            pe = float(exact.get(k, 0))
            se = max((pe * (1 - pe) / N) ** 0.5, 1e-9)
            self.assertLessEqual(abs(mc.get(k, 0) - pe), 4.5 * se + 1e-9, k)

    def test_expected_attempts_lossless_is_one(self):
        self.assertEqual(expected_attempts(run_distribution(Params(p=0, K=3, B=6, L=3), 5, exact=True)), 1)


if __name__ == "__main__":
    unittest.main()
