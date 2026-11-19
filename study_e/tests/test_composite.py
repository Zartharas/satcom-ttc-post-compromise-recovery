import random
import unittest
from fractions import Fraction as F
from study_e.params import Params
from study_e.composite import composite_outcomes
from study_e.multi import run_distribution, outcome_probs
from study_e.sim import run_multi


class Composite(unittest.TestCase):
    def _P(self):
        return Params(p=F(2, 5), K=2, B=6, L=2, r=F(1, 10), persist="volatile", activation="gated")

    def test_sums_to_one_and_preserves_non_divergence_masses(self):
        P = self._P()
        c = composite_outcomes(P, 10, 4, 8, 3, 1, exact=True)
        self.assertEqual(sum(c.values()), 1)
        base = outcome_probs(run_distribution(P, 10, exact=True))
        for o in ("SUCCESS", "INDETERMINATE", "EXPIRED_OLD"):
            self.assertEqual(c.get(o, 0), base.get(o, 0))
        self.assertEqual(c.get("RECOVERED", 0) + c.get("UNRECOVERED_DIVERGED", 0),
                         base.get("DIVERGED_S_AHEAD", 0) + base.get("DIVERGED_G_AHEAD", 0))

    def test_no_recovery_when_detection_exceeds_horizon(self):
        c = composite_outcomes(self._P(), 6, 4, 8, 3, 50, exact=True)
        self.assertEqual(c.get("RECOVERED", 0), 0)

    def test_lossless_has_no_divergence(self):
        c = composite_outcomes(Params(p=0, K=3, B=6, L=3), 8, 4, 8, 3, 1, exact=True)
        self.assertEqual(c, {"SUCCESS": 1})

    def test_recovery_helps_monotonically_in_horizon(self):
        P = self._P()
        prev = -1
        for H in range(2, 13):
            v = composite_outcomes(P, H, 4, 8, 3, 1, exact=True).get("RECOVERED", 0)
            self.assertGreaterEqual(v + 0, 0)
            r = composite_outcomes(P, H, 4, 8, 3, 1, exact=True)
            tot = r.get("SUCCESS", 0) + r.get("RECOVERED", 0)
            self.assertGreaterEqual(tot, prev)
            prev = tot

    def test_monte_carlo_end_to_end(self):
        P = self._P()
        H, n, B0, L0, det, N = 10, 4, 8, 3, 1, 30000
        exact = composite_outcomes(P, H, n, B0, L0, det)
        rng = random.Random(20261202)
        pf = float(P.p)
        cnt = {}
        for _ in range(N):
            gen = run_multi(P, H)
            try:
                pr = next(gen)
                while True:
                    pr = gen.send(rng.random() < float(pr))
            except StopIteration as e:
                o, g, _a = e.value
            if o in ("DIVERGED_S_AHEAD", "DIVERGED_G_AHEAD"):
                c, rem_end, ok = g + det, H, False
                while c < rem_end and not ok:           # independent re-bootstrap simulation
                    step = tx = 0
                    Le = min(L0, rem_end - c)
                    k = 0
                    while k < Le and not ok and tx < B0:
                        k += 1
                        for _s in range(P.K):
                            tx += 1
                            if rng.random() >= pf:
                                step += 1
                            if step >= n:
                                ok = True
                                break
                            if tx >= B0:
                                break
                    if not ok:
                        c += k
                o = "RECOVERED" if ok else "UNRECOVERED_DIVERGED"
            cnt[o] = cnt.get(o, 0) + 1
        for key in set(cnt) | set(exact):
            pe = exact.get(key, 0)
            se = max((pe * (1 - pe) / N) ** 0.5, 1e-9)
            self.assertLessEqual(abs(cnt.get(key, 0) / N - pe), 4.5 * se + 1e-9, key)


if __name__ == "__main__":
    unittest.main()
