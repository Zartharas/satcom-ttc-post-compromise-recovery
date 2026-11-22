import unittest
from fractions import Fraction as F
from study_e.params import Params
from study_e.model import exact_distribution, outcome_probs, expected_contacts
from tests.helpers import closed_form_loss_only


class KnownAnswer(unittest.TestCase):
    def test_probabilities_sum_to_one(self):
        for pers in ("volatile", "commit", "journal"):
            for act in ("local", "gated"):
                P = Params(p=F(1, 3), K=2, B=7, L=4, r=F(1, 5), persist=pers, activation=act)
                self.assertEqual(sum(exact_distribution(P, exact=True).values()), 1)

    def test_lossless_no_restart_succeeds_in_ceil_6_over_K_contacts(self):
        for K in (1, 2, 3, 6):
            P = Params(p=0, K=K, B=6, L=6)
            d = exact_distribution(P, exact=True)
            self.assertEqual(d, {("SUCCESS", -(-6 // K)): F(1)})

    def test_total_loss_never_progresses(self):
        P = Params(p=1, K=2, B=5, L=3, r=F(1, 2), persist="volatile")
        self.assertEqual(outcome_probs(exact_distribution(P, exact=True)), {"EXPIRED_OLD": 1})

    def test_loss_only_closed_forms_binomial(self):
        for act in ("local", "gated"):
            for p in (F(1, 4), F(1, 2), F(3, 4)):
                for B in (3, 4, 5, 6, 8, 10):
                    P = Params(p=p, K=2, B=B, L=B, r=0, activation=act)  # K*L >= B
                    got = outcome_probs(exact_distribution(P, exact=True))
                    want = closed_form_loss_only(p, B, act)
                    for o, v in want.items():
                        self.assertEqual(got.get(o, 0), v, (act, p, B, o))

    def test_journal_persistence_is_invariant_to_restart_rate(self):
        base = Params(p=F(1, 3), K=2, B=8, L=4, r=0, persist="journal")
        want = exact_distribution(base, exact=True)
        for r in (F(1, 10), F(1, 2), 1):
            P = Params(p=F(1, 3), K=2, B=8, L=4, r=r, persist="journal")
            self.assertEqual(exact_distribution(P, exact=True), want)

    def test_time_with_K1_equals_transmissions(self):
        P = Params(p=0, K=1, B=6, L=6)
        self.assertEqual(expected_contacts(exact_distribution(P, exact=True)), 6)

    def test_restart_at_boundary_after_commit_gated_diverges_ground_ahead_when_not_journaled(self):
        # p=0, K=4: contact 1 delivers m1..m4 (G active, gated S not active); restart then.
        for pers, expect in (("volatile", "DIVERGED_G_AHEAD"), ("commit", "DIVERGED_G_AHEAD"),
                             ("journal", "SUCCESS")):
            P = Params(p=0, K=4, B=6, L=2, r=1, persist=pers, activation="gated")
            self.assertEqual(list(outcome_probs(exact_distribution(P, exact=True))), [expect], pers)

    def test_local_activation_commit_persistence_survives_restart_after_m3(self):
        P = Params(p=0, K=3, B=6, L=3, r=1, persist="commit", activation="local")
        # contact1 delivers m1..m3 (S active, persisted); restart: continues; contact2 m4..m6 -> SUCCESS
        self.assertEqual(outcome_probs(exact_distribution(P, exact=True)), {"SUCCESS": 1})


if __name__ == "__main__":
    unittest.main()
