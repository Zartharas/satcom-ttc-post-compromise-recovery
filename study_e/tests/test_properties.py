import unittest
from fractions import Fraction as F
from study_e.params import Params
from study_e.model import exact_distribution, outcome_probs, lockout_prob


def P_of(**kw):
    d = dict(p=F(1, 3), K=2, B=6, L=4, r=F(1, 10), persist="commit", activation="local")
    d.update(kw)
    return Params(**d)


def prob(P, o):
    return outcome_probs(exact_distribution(P, exact=True)).get(o, 0)


class Properties(unittest.TestCase):
    def test_success_monotone_in_budget_slots_and_lifetime(self):
        for pers in ("volatile", "commit", "journal"):
            prev = -1
            for B in range(1, 13):
                v = prob(P_of(B=B, L=6, persist=pers), "SUCCESS")
                self.assertGreaterEqual(v, prev)
                prev = v
            for key, vals in (("K", (1, 2, 3, 4)), ("L", (1, 2, 3, 4, 5))):
                prev = -1
                for x in vals:
                    v = prob(P_of(B=12, persist=pers, **{key: x}), "SUCCESS")
                    self.assertGreaterEqual(v, prev, (pers, key, x))
                    prev = v

    def test_success_nonincreasing_in_loss(self):
        prev = 2
        for p in (F(0), F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(1)):
            v = prob(P_of(p=p, B=10, L=5), "SUCCESS")
            self.assertLessEqual(v, prev)
            prev = v

    def test_volatile_lockout_nondecreasing_in_restart_rate(self):
        prev = -1
        for r in (F(0), F(1, 20), F(1, 10), F(1, 4), F(1, 2)):
            v = lockout_prob(exact_distribution(P_of(r=r, persist="volatile", B=10, L=5), exact=True))
            self.assertGreaterEqual(v, prev)
            prev = v

    def test_persistence_ordering_of_ground_ahead_gated(self):
        # more durable persistence never increases ground-ahead divergence (gated activation)
        r = F(1, 5)
        vals = [prob(P_of(persist=pl, activation="gated", r=r, B=10, L=5), "DIVERGED_G_AHEAD")
                for pl in ("volatile", "commit", "journal")]
        self.assertGreaterEqual(vals[0], vals[1])
        self.assertGreaterEqual(vals[1], vals[2])

    def test_divergence_is_NOT_monotone_in_budget_witness(self):
        """Documented correction of an earlier hypothesis: with loss only, P(S-ahead divergence)
        equals P(exactly 3 successes in B transmissions), which first rises with B."""
        q = F(1, 2)
        vals = [prob(Params(p=1 - q, K=2, B=B, L=B, r=0, activation="local"), "DIVERGED_S_AHEAD")
                for B in (3, 4, 5, 6)]
        self.assertLess(vals[0], vals[1])
        self.assertLess(vals[1], vals[2])


if __name__ == "__main__":
    unittest.main()
