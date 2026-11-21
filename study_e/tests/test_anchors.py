import json
import math
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from fractions import Fraction as F

from study_e import anchors as A
from study_e.model import exact_distribution
from study_e.params import Params

UTC = timezone.utc
T0 = datetime(2026, 6, 1, tzinfo=UTC)


def at(sec):
    return T0 + timedelta(seconds=sec)


class TestHelpers(unittest.TestCase):
    def test_quantile_known(self):
        self.assertEqual(A.quantile([1, 2, 3, 4], .5), 2.5)
        self.assertEqual(A.quantile([1, 2, 3, 4, 5], .25), 2.0)
        self.assertEqual(A.quantile([7], .9), 7.0)
        self.assertEqual(A.quantile([1, 2, 3, 4], 0), 1.0)
        self.assertEqual(A.quantile([1, 2, 3, 4], 1), 4.0)
        with self.assertRaises(ValueError):
            A.quantile([], .5)

    def test_summary_empty_and_basic(self):
        self.assertEqual(A.summary([]), {"n": 0})
        s = A.summary([60, 60, 70, 80, 100])
        self.assertEqual((s["n"], s["min"], s["median"], s["max"], s["mean"]), (5, 60, 70.0, 100, 74.0))


class TestTrace(unittest.TestCase):
    def rows(self):
        return [(1, 10, at(0), at(100), "a1"), (1, 10, at(300), at(380), "a2"), (1, 10, at(350), at(420), "a3"),
                (2, 20, at(1000), at(1060), "b1"), (2, 20, at(2000), at(2060), "b2")]

    def test_stats_known_answer(self):
        st = A.trace_stats(self.rows())
        self.assertEqual((st["n_rows"], st["n_pairs"], st["overlaps_excluded"]), (5, 2, 1))
        self.assertEqual(st["duration_s"]["median"], 70.0)
        self.assertEqual(st["duration_s"]["mean"], 74.0)
        self.assertEqual(sorted([200.0, 940.0]), [200.0, 940.0])
        self.assertEqual((st["gap_s"]["n"], st["gap_s"]["median"]), (2, 570.0))
        self.assertIn("not contacts", st["label"])

    def test_input_order_irrelevant(self):
        r = self.rows()
        self.assertEqual(A.trace_stats(r), A.trace_stats(list(reversed(r))))

    def _write(self, lines):
        fd, p = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w") as fh:
            fh.write("\n".join(json.dumps(x) for x in lines) + "\n")
        self.addCleanup(os.remove, p)
        return p

    def rec(self, i, s="2026-06-01T00:00:00Z", e="2026-06-01T00:05:00Z"):
        return {"id": i, "start": s, "end": e, "ground_station": 1, "norad_cat_id": 2}

    def test_loader_ok_and_rejects(self):
        self.assertEqual(len(A.load_satnogs_jsonl(self._write([self.rec(1), self.rec(2)]))), 2)
        with self.assertRaises(ValueError):
            A.load_satnogs_jsonl(self._write([self.rec(1), self.rec(1)]))
        with self.assertRaises(ValueError):
            A.load_satnogs_jsonl(self._write([self.rec(1, s="2026-06-01T00:05:00Z", e="2026-06-01T00:05:00Z")]))
        with self.assertRaises(ValueError):
            A.load_satnogs_jsonl(self._write([self.rec(1, s="2026-06-01T00:00:00")]))
        bad = self.rec(1)
        del bad["end"]
        with self.assertRaises(ValueError):
            A.load_satnogs_jsonl(self._write([bad]))

    def test_frozen_trace_if_present(self):
        p = os.environ.get("STUDY_E_SATNOGS_JSONL")
        if not p or not os.path.exists(p):
            self.skipTest("set STUDY_E_SATNOGS_JSONL to the verified POP-002 trace to run this check")
        self.assertEqual(A.sha256_file(p), "6f80a44fa6cfa63a70df49de3ba447de3d59efe0632208180f26552f37b46a8e")
        st = A.trace_stats(A.load_satnogs_jsonl(p))
        self.assertEqual((st["n_rows"], st["n_pairs"]), (476, 20))


class TestPing(unittest.TestCase):
    def burst(self, lost, blank_after=()):
        base = datetime(2024, 5, 9, 0, 0, 0)
        usable = [(base + timedelta(seconds=10 * i), 10, x) for i, x in enumerate(lost)]
        blank = [base + timedelta(seconds=10 * i + 5) for i in blank_after]
        return usable, blank

    LOST = [0, 3, 10, 0, 0, 1, 0, 2, 2, 0]

    def test_known_answer(self):
        u, b = self.burst(self.LOST)
        s = A.ping_stats(u, b)
        self.assertEqual((s["packets_sent"], s["packets_lost"]), (100, 18))
        self.assertAlmostEqual(s["mean_packet_loss"], .18)
        self.assertAlmostEqual(s["share_bursts_with_loss"], .5)
        self.assertEqual(s["full_loss_bursts"], 1)
        self.assertAlmostEqual(s["p_lossy_given_prev_ok"], 3 / 4)
        self.assertAlmostEqual(s["p_lossy_given_prev_lossy"], 2 / 5)
        self.assertEqual(s["lossy_run_length_hist"], {"1": 1, "2": 2})
        self.assertEqual(s["lossy_run_max"], 2)
        self.assertAlmostEqual(s["lossy_run_mean"], 5 / 3)

    def test_blank_row_breaks_runs_and_is_not_loss(self):
        u, b = self.burst(self.LOST, blank_after=(1,))      # blank between burst 1 and 2
        s = A.ping_stats(u, b)
        self.assertEqual(s["blank_rows_excluded"], 1)
        self.assertEqual(s["packets_lost"], 18)              # blank never counted as loss
        self.assertEqual(s["lossy_run_length_hist"], {"1": 3, "2": 1})
        self.assertAlmostEqual(s["p_lossy_given_prev_lossy"], 1 / 4)
        self.assertAlmostEqual(s["p_lossy_given_prev_ok"], 3 / 4)

    def test_large_spacing_breaks_adjacency(self):
        u, b = self.burst(self.LOST)
        # shift bursts 3.. by 60 s: the pair (2,3) is now 70 s apart and no longer adjacent
        u = [(t + timedelta(seconds=60), n, x) if i >= 3 else (t, n, x) for i, (t, n, x) in enumerate(u)]
        s = A.ping_stats(u, b)
        self.assertAlmostEqual(s["p_lossy_given_prev_lossy"], 2 / 4)     # transitions i=2,6,8,9 only
        self.assertAlmostEqual(s["p_lossy_given_prev_ok"], 3 / 4)
        self.assertEqual(s["lossy_run_length_hist"], {"1": 1, "2": 2})

    def test_two_lossy_bursts_far_apart_are_two_runs(self):
        u, b = self.burst([2, 2, 0])
        u[1] = (u[1][0] + timedelta(seconds=100), u[1][1], u[1][2])
        u[2] = (u[2][0] + timedelta(seconds=100), u[2][1], u[2][2])
        self.assertEqual(A.ping_stats(u, b)["lossy_run_length_hist"], {"1": 2})

    def test_loader_both_formats_and_blanks(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "ping_metrics_2024-05-09.csv"), "w") as fh:
                fh.write("Timestamp;PacketTransmit;PacketReceive;PacketLossCount;PacketLossRate;RTTMin;RTTAvg;RTTMax;RTTMdev\n"
                         "2024-05-09 00:00:00;10;10;0;0.0;1;1;1;1\n"
                         "2024-05-09 00:00:10;;;;;;;;\n")
            with open(os.path.join(d, "ping_metrics_2024-05-10.tsv"), "w") as fh:
                fh.write("Timestamp\tPacketTransmit\tPacketReceive\tPacketLossCount\tPacketLossRate\tRTTMin\tRTTAvg\tRTTMax\tRTTMdev\n"
                         "2024-05-10 00:00:00\t10\t9\t1\t10.0\t1\t1\t1\t1\n")
            u, b = A.load_ping_dir(d)
            self.assertEqual(len(u), 2)
            self.assertEqual(len(b), 1)
            self.assertEqual(u[1][2], 1)
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                A.load_ping_dir(d)


class TestGE(unittest.TestCase):
    def test_stationary_loss_exact(self):
        for ps in (F(1, 20), F(1, 10), F(1, 5), F(3, 10), F(1, 2)):
            for m in (1, 2, 4):
                try:
                    a, b, pb = A.ge_matched(ps, m)
                except ValueError:
                    self.assertGreater(F(1, m) * ps / (1 - ps), 1)
                    continue
                self.assertEqual(A.ge_stationary_loss(a, b, 0, pb), ps)
                self.assertEqual(1 / b, m)
                self.assertTrue(0 < a <= 1 and 0 < b <= 1)

    def test_rejects(self):
        for bad in ((0, 2), (1, 2), (F(1, 2), F(1, 2))):
            with self.assertRaises(ValueError):
                A.ge_matched(*bad)
        with self.assertRaises(ValueError):
            A.ge_matched(F(9, 10), 1)        # a = 9 > 1

    def test_runs_in_exact_model(self):
        a, b, pb = A.ge_matched(F(1, 5), 2)
        P = Params(p=F(0), K=2, B=4, L=2, r=F(0), ge=(a, b, pb))
        dist = exact_distribution(P, exact=True)
        self.assertEqual(sum(dist.values()), 1)


def independent_pass_seconds(h, e_deg, beta):
    """Vector geometry + bisection; shares no formula with study_e.anchors."""
    a = A.RE_KM + h
    e = math.radians(e_deg)

    def elev(g):
        p = (a * math.cos(beta) * math.cos(g), a * math.sin(beta) * math.cos(g), a * math.sin(g))
        d = (p[0] - A.RE_KM, p[1], p[2])
        return math.asin(d[0] / math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2))

    if elev(0.0) < e:
        return 0.0
    lo, hi = 0.0, math.pi / 2
    for _ in range(200):
        mid = (lo + hi) / 2
        if elev(mid) >= e:
            lo = mid
        else:
            hi = mid
    return 2 * lo / math.sqrt(A.MU_KM3_S2 / a ** 3)


class TestPass(unittest.TestCase):
    def test_matches_independent_geometry(self):
        for h in (400, 550, 800, 1200):
            for e in (0, 5, 10, 20, 40):
                lam = A.pass_half_angle(h, e)
                for frac in (0.0, 0.25, 0.5, 0.9):
                    beta = frac * lam
                    self.assertAlmostEqual(A.pass_seconds(h, e, beta), independent_pass_seconds(h, e, beta), delta=1e-5,
                                           msg=(h, e, frac))

    def test_beyond_cap_is_zero(self):
        lam = A.pass_half_angle(550, 10)
        self.assertEqual(A.pass_seconds(550, 10, lam), 0.0)
        self.assertEqual(A.pass_seconds(550, 10, lam * 1.2), 0.0)

    def test_overhead_550_horizon_known_order(self):
        t = A.max_pass_seconds(550, 0)
        self.assertGreater(t, 700)
        self.assertLess(t, 750)          # about 12 minutes horizon to horizon

    def test_monotone(self):
        for h in (400, 800):
            self.assertGreater(A.max_pass_seconds(h, 5), A.max_pass_seconds(h, 20))
        self.assertGreater(A.max_pass_seconds(1200, 10), A.max_pass_seconds(400, 10))
        for h, e in ((550, 10), (800, 5)):
            self.assertLess(A.mean_pass_seconds(h, e), A.max_pass_seconds(h, e))
            self.assertGreater(A.mean_pass_seconds(h, e), 0)

    def test_mean_converges(self):
        self.assertAlmostEqual(A.mean_pass_seconds(550, 10, 2000), A.mean_pass_seconds(550, 10, 8000), delta=0.5)

    def test_slots(self):
        self.assertEqual(A.slots_per_pass(725, 60), 12)
        self.assertEqual(A.slots_per_pass(59, 60), 0)
        with self.assertRaises(ValueError):
            A.slots_per_pass(100, 0)


if __name__ == "__main__":
    unittest.main()
