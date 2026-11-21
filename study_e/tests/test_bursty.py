import itertools
import os
import unittest
from fractions import Fraction as F
from study_e.params import Params
from study_e.model import exact_distribution, outcome_probs
from study_e.sim import enumerate_distribution, monte_carlo
from tests.helpers import closed_form_loss_only

FULL = os.environ.get("STUDY_E_FULL") == "1"
GES = [(F(1, 4), F(1, 2), F(9, 10)), (F(1, 10), F(3, 10), F(1, 1)), (F(1, 2), F(1, 2), F(1, 5))]


class Bursty(unittest.TestCase):
    def test_dp_equals_enumeration_with_ge(self):
        n = 0
        for ge, K, L, B, r, pers, act in itertools.product(
                GES if FULL else GES[:2], (1, 2), (1, 2, 3) if FULL else (1, 2), (2, 4, 6), (F(0), F(1, 4)),
                ("volatile", "commit", "journal") if FULL else ("volatile", "journal"), ("local", "gated")):
            P = Params(p=F(1, 10), K=K, B=B, L=L, r=r, persist=pers, activation=act, ge=ge)
            self.assertEqual(exact_distribution(P, exact=True), enumerate_distribution(P), P)
            self.assertEqual(sum(exact_distribution(P, exact=True).values()), 1)
            n += 1
        self.assertGreater(n, 50)

    def test_ge_with_equal_loss_states_is_iid(self):
        for ge in [(F(1, 4), F(1, 2), F(1, 5)), (F(3, 5), F(1, 10), F(1, 5))]:
            for K, L, B, r in [(2, 3, 6, F(1, 5)), (3, 2, 5, F(0))]:
                a = Params(p=F(1, 5), K=K, B=B, L=L, r=r, persist="volatile", ge=ge)
                b = Params(p=F(1, 5), K=K, B=B, L=L, r=r, persist="volatile")
                self.assertEqual(exact_distribution(a, exact=True), exact_distribution(b, exact=True))

    def test_never_entering_bad_state_is_iid(self):
        a = Params(p=F(1, 3), K=2, B=6, L=3, r=F(1, 5), persist="commit", ge=(F(0), F(1, 2), F(1)))
        b = Params(p=F(1, 3), K=2, B=6, L=3, r=F(1, 5), persist="commit")
        self.assertEqual(exact_distribution(a, exact=True), exact_distribution(b, exact=True))

    def test_memoryless_channel_closed_form(self):
        # b = 1-a  => state independent each slot => iid with p_eff = piG*p + piB*p_bad
        a, p, pb = F(1, 4), F(1, 10), F(7, 10)
        P = Params(p=p, K=2, B=7, L=7, r=0, activation="gated", ge=(a, 1 - a, pb))
        p_eff = (1 - a) * p + a * pb
        got = outcome_probs(exact_distribution(P, exact=True))
        for o, v in closed_form_loss_only(p_eff, 7, "gated").items():
            self.assertEqual(got.get(o, 0), v, o)

    def test_burstiness_changes_outcome_at_equal_mean_loss(self):
        # same stationary loss 1/2. Direction is NOT assumed: needing 6 consecutive-in-count successes, long good
        # bursts can RAISE success (0.164 vs 0.0156 here), so burstiness must be reported, not presumed harmful.
        memoryless = Params(p=0, K=3, B=6, L=2, ge=(F(1, 2), F(1, 2), F(1)))   # pi_B=1/2, iid p_eff=1/2
        bursty = Params(p=0, K=3, B=6, L=2, ge=(F(1, 10), F(1, 10), F(1)))     # pi_B=1/2, long bursts
        s0 = outcome_probs(exact_distribution(memoryless, exact=True)).get("SUCCESS", 0)
        s1 = outcome_probs(exact_distribution(bursty, exact=True)).get("SUCCESS", 0)
        self.assertNotEqual(s0, s1)  # report direction in the study; here only assert it matters

    def test_monte_carlo_agrees_with_ge(self):
        P = Params(p=F(1, 20), K=3, B=9, L=4, r=F(1, 10), persist="volatile", activation="gated",
                   ge=(F(1, 5), F(1, 4), F(4, 5)))
        N = 40000
        exact = outcome_probs(exact_distribution(P, exact=True))
        mc, _ = monte_carlo(P, N, seed=20261201)
        mco = {}
        for (o, _t), v in mc.items():
            mco[o] = mco.get(o, 0) + v
        for o in set(exact) | set(mco):
            pe = float(exact.get(o, 0))
            se = max((pe * (1 - pe) / N) ** 0.5, 1e-9)
            self.assertLessEqual(abs(mco.get(o, 0) - pe), 4.5 * se + 1e-9, o)


if __name__ == "__main__":
    unittest.main()


class BurstyMutants(unittest.TestCase):
    def _detected(self, mut):
        from unittest import mock
        from study_e import model
        ge = (F(1, 4), F(1, 2), F(9, 10))
        with mock.patch.object(model, "_GE_MUT", mut):
            for K, L, B in ((2, 2, 4), (2, 3, 6), (1, 3, 3)):
                P = Params(p=F(1, 10), K=K, B=B, L=L, r=F(1, 4), persist="volatile", activation="local", ge=ge)
                if exact_distribution(P, exact=True) != enumerate_distribution(P):
                    return True
        return False

    def test_unmutated_clean(self):
        self.assertFalse(self._detected(0))

    def test_mutant_swapped_transitions_detected(self):
        self.assertTrue(self._detected(1))

    def test_mutant_swapped_state_losses_detected(self):
        self.assertTrue(self._detected(2))
