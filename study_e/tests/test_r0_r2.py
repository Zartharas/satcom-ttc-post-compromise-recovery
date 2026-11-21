import itertools
import unittest
from fractions import Fraction as F
from math import comb
from study_e import ratchet, recovery


class R2(unittest.TestCase):
    def test_cmax0_closed_form(self):
        # cmax=0: desync iff some lost frame is followed by a received frame
        # no desync <=> received prefix then all-lost suffix: sum_j q^j p^(n-j)
        for n in (1, 2, 5, 8):
            for p in (F(1, 4), F(1, 2), F(3, 4)):
                q = 1 - p
                none = sum(q**j * p ** (n - j) for j in range(n + 1))
                self.assertEqual(ratchet.desync_probability(n, p, 0, exact=True), 1 - none)

    def test_dp_equals_bruteforce(self):
        for n, cmax, p in itertools.product((1, 3, 6, 9), (0, 1, 2, 3), (F(1, 5), F(1, 2), F(4, 5))):
            self.assertEqual(ratchet.desync_probability(n, p, cmax, exact=True), ratchet.desync_enumerate(n, p, cmax))

    def test_dp_equals_bruteforce_bursty(self):
        ge = (F(1, 4), F(1, 3), F(9, 10))
        for n, cmax in itertools.product((2, 3, 4, 5), (0, 1, 2)):
            self.assertEqual(ratchet.desync_probability(n, F(1, 10), cmax, exact=True, ge=ge),
                             ratchet.desync_enumerate(n, F(1, 10), cmax, ge=ge))

    def test_monotone_in_cache_and_loss_edge_cases(self):
        prev = 2
        for cmax in range(0, 8):
            v = ratchet.desync_probability(12, F(1, 3), cmax, exact=True)
            self.assertLessEqual(v, prev)
            prev = v
        self.assertEqual(ratchet.desync_probability(10, 0, 0, exact=True), 0)   # no loss
        self.assertEqual(ratchet.desync_probability(10, 1, 0, exact=True), 0)   # nothing ever received

    def test_cache_larger_than_window_never_desyncs(self):
        self.assertEqual(ratchet.desync_probability(6, F(1, 2), 6, exact=True), 0)

    def test_mutant_off_by_one_detected(self):
        # bound check mutated to run >= cmax would change results; verify the DP differs from a cmax-1 variant
        a = ratchet.desync_probability(8, F(1, 2), 2, exact=True)
        b = ratchet.desync_probability(8, F(1, 2), 1, exact=True)
        self.assertNotEqual(a, b)


class R0(unittest.TestCase):
    def test_attempt_sums_to_one(self):
        d = recovery.attempt_distribution(F(1, 3), 2, 4, 7, 3, exact=True)
        self.assertEqual(sum(d.values()), 1)

    def test_lossless_closed_form(self):
        d = recovery.attempt_distribution(0, 2, 5, 9, 4, exact=True)
        self.assertEqual(d, {("DONE", 3): 1})
        t = recovery.recovery_time_distribution(0, 2, 5, 9, 4, detect=2, H=20, exact=True)
        self.assertEqual(t, {5: 1})

    def test_total_loss_never_recovers(self):
        t = recovery.recovery_time_distribution(1, 2, 4, 6, 3, detect=1, H=10, exact=True)
        self.assertEqual(t, {"NOT_RECOVERED": 1})

    def test_binomial_closed_form_one_contact(self):
        # K=n_msgs, L0=1, B0>=n: attempt succeeds iff all n slots succeed: q^n; geometric over contacts
        q, n, H = F(3, 4), 3, 6
        t = recovery.recovery_time_distribution(1 - q, n, n, n, 1, detect=0, H=H, exact=True)
        for k in range(1, H + 1):
            self.assertEqual(t[k], (1 - q**n) ** (k - 1) * q**n)
        self.assertEqual(t["NOT_RECOVERED"], (1 - q**n) ** H)

    def test_longer_detection_delay_cannot_help(self):
        base = None
        for detect in (0, 2, 5):
            t = recovery.recovery_time_distribution(F(1, 2), 2, 4, 8, 3, detect=detect, H=12, exact=True)
            r = 1 - t.get("NOT_RECOVERED", 0)
            if base is not None:
                self.assertLessEqual(r, base)
            base = r

    def test_sum_to_one(self):
        t = recovery.recovery_time_distribution(F(2, 5), 2, 4, 8, 3, detect=1, H=9, exact=True)
        self.assertEqual(sum(t.values()), 1)

    def test_monte_carlo_agreement(self):
        import random
        p, K, n, B0, L0, detect, H, N = 0.4, 2, 4, 7, 3, 1, 10, 40000
        exact = recovery.recovery_time_distribution(p, K, n, B0, L0, detect, H)
        rng = random.Random(20261201)
        cnt = {}
        for _ in range(N):
            c, res = detect, "NOT_RECOVERED"
            while c < H:                       # one attempt per loop, own straightforward simulation
                step = tx = 0
                done = False
                Le = min(L0, H - c)
                for k in range(1, Le + 1):
                    for _s in range(K):
                        tx += 1
                        if rng.random() >= p:
                            step += 1
                        if step >= n:
                            res, done = c + k, True
                            break
                        if tx >= B0:
                            break
                    if done or tx >= B0:
                        break
                if done:
                    break
                c += k
            cnt[res] = cnt.get(res, 0) + 1
        for key in set(cnt) | set(exact):
            pe = exact.get(key, 0)
            se = max((pe * (1 - pe) / N) ** 0.5, 1e-9)
            self.assertLessEqual(abs(cnt.get(key, 0) / N - pe), 4.5 * se + 1e-9, key)


if __name__ == "__main__":
    unittest.main()
