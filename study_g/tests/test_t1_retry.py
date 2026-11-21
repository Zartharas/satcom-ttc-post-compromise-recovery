import csv
import tempfile
import unittest
from pathlib import Path

from ttc_recovery.fault_metrics import run_seeded_experiment

from study_f.baseline_fault_grid import LOSS_KINDS as F_LOSS_KINDS, enumerate_cells as f_cells
from study_g import run_grid as g
from study_g.t1_retry import run_with_verification_budget

VERIF = ("TEST_COMMAND", "STATUS_TELEMETRY")


def cell(step, kind, lost, vb):
    return g.GCell(step, kind, lost, vb)


def run(c):
    return g.run_cell(c)


class WrapperEqualsPartI(unittest.TestCase):
    def test_budget1_equals_unmodified_t1_all_cells(self):
        for c in g.enumerate_cells():
            if c.vbudget != 1:
                continue
            sched = g.schedule_for(c)
            base = run_seeded_experiment(g.CONFIG, sched)
            mine = run_with_verification_budget(g.CONFIG, sched, 1)
            m = base.metrics
            self.assertEqual(mine["outcome"], m.outcome, c.cell_id)
            self.assertEqual(mine["alignment"], m.alignment, c.cell_id)
            self.assertEqual(mine["security_state"], m.security_state, c.cell_id)
            self.assertEqual(mine["total_transmissions"], m.total_transmissions, c.cell_id)
            self.assertEqual(mine["verification_complete"], m.verification_complete, c.cell_id)
            self.assertEqual(mine["_event_log"], base.event_log, c.cell_id)

    def test_part_i_canonical_verification_loss_is_indeterminate_at_budget1(self):
        for step in VERIF:
            for kind in ("DROP", "CONTACT_CLOSE"):
                r = run(cell(step, kind, 1, 1))
                self.assertEqual((r["outcome"], r["alignment"], r["security_state"]),
                                 ("INDETERMINATE", "SYNC(3)", "NOT_ESTABLISHED"))


class BudgetThree(unittest.TestCase):
    def test_absorbs_one_and_two_losses(self):
        for step in VERIF:
            for kind in ("DROP", "CONTACT_CLOSE"):
                for n in (1, 2):
                    r = run(cell(step, kind, n, 3))
                    self.assertEqual((r["outcome"], r["alignment"], r["security_state"], r["verification_complete"]),
                                     ("SUCCESS", "SYNC(3)", "SECURE_PROVISIONAL", True), (step, kind, n))

    def test_three_losses_is_indeterminate(self):
        for step in VERIF:
            for kind in ("DROP", "CONTACT_CLOSE"):
                r = run(cell(step, kind, 3, 3))
                self.assertEqual((r["outcome"], r["alignment"], r["verification_complete"]),
                                 ("INDETERMINATE", "SYNC(3)", False), (step, kind))

    def test_retransmissions_are_counted(self):
        r1 = run(cell("TEST_COMMAND", "DROP", 2, 3))
        ctrl = run(cell(None, "CONTROL", 0, 3))
        self.assertEqual(r1["total_transmissions"], ctrl["total_transmissions"] + 2)

    def test_recovery_steps_and_restart_cells_unchanged_by_budget(self):
        by = {}
        for c in g.enumerate_cells():
            if c.step in VERIF:
                continue
            by.setdefault((c.step, c.kind, c.lost), {})[c.vbudget] = run(c)
        self.assertGreater(len(by), 30)
        for key, d in by.items():
            a, b = dict(d[1]), dict(d[3])
            for r in (a, b):
                for f in ("cell_id", "arm", "verification_budget"):
                    r.pop(f)
            self.assertEqual(a, b, key)

    def test_restart_cells(self):
        r = run(cell("RECOVERY_COMMIT", "ENDPOINT_RESTART", 0, 3))
        self.assertEqual(r["alignment"], "G_AHEAD")
        r = run(cell("RECOVERY_CONFIRM", "ENDPOINT_RESTART", 0, 3))
        self.assertEqual(r["alignment"], "S_AHEAD")
        self.assertNotEqual(r["outcome"], "SUCCESS")

    def test_wrapper_rejects_bad_budget(self):
        with self.assertRaises(ValueError):
            run_with_verification_budget(g.CONFIG, [], 0)


class GridDefinition(unittest.TestCase):
    def test_reuses_study_f_axes(self):
        fc = f_cells()
        self.assertEqual({c.lost for c in fc if c.kind in {k for k in F_LOSS_KINDS}}, set(g.LOST_COUNTS))
        self.assertEqual({c.budget for c in fc}, set(g.VERIFICATION_BUDGETS))
        self.assertEqual({k.value for k in g.LOSS_KINDS}, set(F_LOSS_KINDS))

    def test_size_and_unique_ids(self):
        cells = g.enumerate_cells()
        self.assertEqual(len(cells), 86)
        self.assertEqual(len({c.cell_id for c in cells}), 86)

    def test_deterministic_repeat_identical_csv(self):
        with tempfile.TemporaryDirectory() as d:
            p1, p2 = Path(d) / "a.csv", Path(d) / "b.csv"
            g.write_csv(g.run_grid(), p1)
            g.write_csv(g.run_grid(), p2)
            self.assertEqual(p1.read_bytes(), p2.read_bytes())
            with open(p1) as fh:
                self.assertEqual(len(list(csv.DictReader(fh))), 86)

    def test_protocol_footer_hashes_match(self):
        proto = Path(__file__).resolve().parents[2] / "docs/study_g/STUDY_G_PROTOCOL.md"
        text = proto.read_text()
        footer = text.split(g.FOOTER_MARK)[1]
        self.assertIn(g.protocol_body_sha256(proto), footer)
        self.assertIn(g.grid_sha256(), footer)


if __name__ == "__main__":
    unittest.main()
