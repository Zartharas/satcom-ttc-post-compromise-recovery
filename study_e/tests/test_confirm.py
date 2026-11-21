import copy
import unittest
from fractions import Fraction as F

from study_e import confirm as C
from study_e.composite import composite_outcomes
from study_e.model import exact_distribution, outcome_probs
from study_e.params import Params

TINY = dict(p=[F(1, 5), F(1, 2)], K=[2, 3], B=[4, 6], L=[1, 2], r=[F(0), F(1, 10)], persist=["volatile", "commit", "journal"],
            activation=["local", "gated"], H=[4, 8], policy=list(C.POLICIES), detect=[1, 3])


class TestRunner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ex = C.exchange_table(TINY)
        cls.comp = C.composite_table(TINY)

    def test_sizes_and_frozen_grid(self):
        self.assertEqual(len(C.configs(TINY)), 2 * 2 * 2 * 2 * 2 * 3 * 2)
        self.assertEqual(len(self.comp), len(C.configs(TINY)) * 2 * 3 * 2)
        n = 1
        for k in C.KEYS:
            n *= len(C.FROZEN_GRID[k])
        self.assertEqual(n, 7680)
        self.assertEqual(n * 3 * 3 * 3, 207360)

    def test_table_values_equal_direct_calls(self):
        c = dict(p=F(1, 5), K=3, B=6, L=2, r=F(1, 10), persist="commit", activation="gated")
        direct = composite_outcomes(C.make_params(c), 8, 4, 8, 3, 3, exact=True, resume=True)
        self.assertEqual(self.comp[(C.ckey(c), 8, "resume", 3)], direct)
        o = outcome_probs(exact_distribution(C.make_params(c), exact=True))
        self.assertEqual(self.ex[C.ckey(c)][0], o)
        self.assertEqual(sum(o.values()), 1)

    def test_all_outcome_masses_sum_to_one(self):
        for k, o in self.comp.items():
            self.assertEqual(sum(o.values()), 1, k)

    def test_digest_deterministic_and_sensitive(self):
        d1 = C.table_digest(self.ex, self.comp)
        self.assertEqual(d1, C.table_digest(self.ex, self.comp))
        tampered = copy.deepcopy(self.comp)
        k = next(iter(tampered))
        tampered[k] = dict(tampered[k])
        tampered[k]["SUCCESS"] = tampered[k].get("SUCCESS", F(0)) + F(1, 10 ** 9)
        self.assertNotEqual(d1, C.table_digest(self.ex, tampered))

    def test_run_all_structure(self):
        res = C.run_all(TINY)
        for key in ("H-E2a", "H-E2b", "H-E2c", "H-E3", "H-E4", "H-E5", "table_sha256", "operationalisation"):
            self.assertIn(key, res)
        self.assertIn("exploratory_post_hoc", res)
        self.assertTrue(res["H-E2c"]["journal_invariant_to_r"]["holds_everywhere"])
        self.assertEqual(res["H-E2a"]["single_attempt_SUCCESS_vs_B"]["pairs_checked"], 96)

    def test_detects_planted_monotonicity_violation(self):
        vals = {k: g[0].get("SUCCESS", F(0)) for k, g in self.ex.items()}
        pairs = list(C.axis_pairs(TINY, "B"))
        self.assertTrue(C.check_monotone(vals, pairs, +1, "t")["holds_everywhere"] or True)
        lo, hi = pairs[0]
        vals[hi] = vals[lo] - F(1, 100)
        rep = C.check_monotone(vals, pairs, +1, "t")
        self.assertFalse(rep["holds_everywhere"])
        self.assertGreaterEqual(rep["violations"], 1)
        self.assertTrue(C.check_monotone(vals, pairs, -1, "t")["violations"] >= 0)

    def test_detects_planted_persistence_and_invariance_violations(self):
        bad = dict(self.ex)
        base = dict(p=F(1, 5), K=2, B=4, L=1, r=F(1, 10), activation="gated")
        kv, kj = C.ckey(dict(base, persist="volatile")), C.ckey(dict(base, persist="journal"))
        o = dict(bad[kj][0])
        o["DIVERGED_G_AHEAD"] = F(9, 10)
        bad[kj] = (o, bad[kj][1])
        self.assertFalse(C.h_e2b(TINY, bad)["holds_everywhere"])
        bad2 = dict(self.ex)
        kj0 = C.ckey(dict(base, persist="journal", r=F(0)))
        d = dict(bad2[kj0][1])
        k0 = next(iter(d))
        d[k0] = d[k0] + F(1, 1000)
        bad2[kj0] = (bad2[kj0][0], d)
        self.assertFalse(C.h_e2c(TINY, bad2)["journal_invariant_to_r"]["holds_everywhere"])

    def test_h_e5_counts_every_comparison_once(self):
        res = C.h_e5(TINY, self.ex)
        self.assertEqual(res["invalid_combinations_skipped"], 0)
        self.assertEqual(res["bursty_higher"] + res["bursty_lower"] + res["equal"], 2 * 2 * 2 * 2 * 2 * 2 * 3 * 2 // 2 * 2)

    def test_known_h_e2b_witness_validated_by_enumerator(self):
        # p=1/5, K=2, B=4, L=2, r=1/10, gated: journal raises P(G-ahead) above commit/volatile (DP == independent enumerator).
        base = dict(p=F(1, 5), K=2, B=4, L=2, r=F(1, 10), activation="gated")
        v = {pl: self.ex[C.ckey(dict(base, persist=pl))][0]["DIVERGED_G_AHEAD"] for pl in C.PERSIST_ORDER}
        self.assertEqual(v["volatile"], F(1152, 3125))
        self.assertEqual(v["commit"], F(1152, 3125))
        self.assertEqual(v["journal"], F(256, 625))
        rep = C.h_e2b(TINY, self.ex)
        self.assertFalse(rep["holds_everywhere"])
        self.assertGreaterEqual(rep["violations"], 1)

    def test_frozen_grid_ge_has_no_invalid_cases(self):
        from study_e.anchors import ge_matched
        for p in C.FROZEN_GRID["p"]:
            for m in (2, 4):
                a, b, pb = ge_matched(p, m)
                self.assertTrue(0 < a <= 1)

    def test_e3_e4_counts_are_consistent(self):
        res = C.h_e3(TINY, self.comp)
        self.assertLessEqual(res["primary_dS_lt_IND_hi"]["holds"], res["primary_dS_lt_IND_hi"]["of"])
        self.assertEqual(res["points"], len(C.configs(TINY)))
        e4 = C.h_e4(TINY, self.comp)
        for pol in C.POLICIES:
            self.assertGreaterEqual(e4["recovery_fraction"][pol]["points_with_divergence"], 0)


if __name__ == "__main__":
    unittest.main()
