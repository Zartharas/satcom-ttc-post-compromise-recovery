"""Mutation tests: seeded bugs must be detected by the differential and closed-form checks."""
import unittest
from fractions import Fraction as F
from unittest import mock
from study_e import model, rules, sim
from study_e.params import Params
from study_e.sim import enumerate_distribution
from tests.helpers import closed_form_loss_only


def detected():
    """True if any cheap check disagrees (i.e. the mutant would be caught)."""
    pts = []
    for pers in ("volatile", "commit", "journal"):
        for act in ("local", "gated"):
            pts.append(Params(p=F(1, 3), K=2, B=6, L=3, r=F(1, 4), persist=pers, activation=act))
            pts.append(Params(p=F(1, 2), K=3, B=5, L=2, r=F(1, 2), persist=pers, activation=act))
    for P in pts:
        if model.exact_distribution(P, exact=True) != enumerate_distribution(P):
            return True
    for act in ("local", "gated"):
        P = Params(p=F(1, 3), K=2, B=7, L=7, r=0, activation=act)
        got = model.outcome_probs(model.exact_distribution(P, exact=True))
        want = closed_form_loss_only(F(1, 3), 7, act)
        if any(got.get(o, 0) != v for o, v in want.items()):
            return True
    return False


class Mutation(unittest.TestCase):
    def test_unmutated_is_clean(self):
        self.assertFalse(detected())

    def test_mutant_volatile_treated_as_commit(self):
        orig = rules.restart_effect
        def m(step, persist, act):
            return orig(step, "commit" if persist == "volatile" else persist, act)
        with mock.patch.object(rules, "restart_effect", m):
            self.assertTrue(detected())

    def test_mutant_restart_to_wrong_step(self):
        orig = rules.restart_effect
        def m(step, persist, act):
            k, v = orig(step, persist, act)
            return (k, 1) if (k == "CONTINUE" and v == 0) else (k, v)
        with mock.patch.object(rules, "restart_effect", m):
            self.assertTrue(detected())

    def test_mutant_classify_swaps_ahead_labels(self):
        orig = rules.classify
        sw = {"DIVERGED_S_AHEAD": "DIVERGED_G_AHEAD", "DIVERGED_G_AHEAD": "DIVERGED_S_AHEAD"}
        with mock.patch.object(rules, "classify", lambda s, a: sw.get(orig(s, a), orig(s, a))):
            self.assertTrue(detected())

    def test_mutant_activation_threshold(self):
        with mock.patch.dict(rules.S_ACT_STEP, {"local": 4}):
            self.assertTrue(detected())

    def test_mutant_budget_off_by_one(self):
        with mock.patch.object(model, "_BUDGET_FUDGE", 1):
            self.assertTrue(detected())

    def test_mutant_in_independent_simulator(self):
        orig = sim._sim_restart
        def m(step, persist, act):
            return ("go", step) if persist == "volatile" else orig(step, persist, act)
        with mock.patch.object(sim, "_sim_restart", m):
            self.assertTrue(detected())


if __name__ == "__main__":
    unittest.main()
