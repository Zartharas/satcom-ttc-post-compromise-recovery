import dataclasses
import json
import unittest
from pathlib import Path

from study_f.baseline_fault_grid import (Cell, enumerate_cells, not_defined_records, plan_sha256, run_cell)
from ttc_recovery import baseline_metrics as bm

ROOT = Path(__file__).resolve().parents[2]
CATALOG = {e["id"]: e for e in json.loads((ROOT / "tests/scenarios/baseline-test-catalog.json").read_text())["tests"]}

# frozen catalog scenario -> equivalent Study F cell (single transmission, catalog initial state)
REDUCTION = {
    "B0-01": Cell("B0", None, "CONTROL", 0, 1),
    "B0-04": Cell("B0", "OTAR_UPLOAD", "DROP", 1, 1),
    "B1-01": Cell("B1_LOCAL", None, "CONTROL", 0, 1),
    "B1-03": Cell("B1_LOCAL", "KEM_INIT_RESPONSE", "REORDER", 0, 1),
    "B1-04": Cell("B1_LOCAL", "KEM_CONFIRM", "DROP", 1, 1),
    "B1-05": Cell("B1_DEFERRED", None, "CONTROL", 0, 1),
    "B1-06": Cell("B1_DEFERRED", "KEM_CONFIRM", "DROP", 1, 1),
    "B1-07": Cell("B1_DEFERRED", "AUTHENTICATED_STATUS", "DROP", 1, 1),
    "B2-01": Cell("B2", None, "CONTROL", 0, 1),
    "B2-07": Cell("B2", "RATCHET_UPDATE", "DROP", 1, 1),
    "B2-08": Cell("B2", "STATUS_TELEMETRY", "DROP", 1, 1),
    "B2-09": Cell("B2", "RATCHET_UPDATE", "STALE_GROUND_RESTORE", 0, 1),
    "B2-10": Cell("B2", "RATCHET_UPDATE", "REPLAY_UPDATE", 0, 1),
}


class ReductionToFrozenCatalog(unittest.TestCase):
    def test_engine_reproduces_frozen_baseline_outcomes(self):
        for sid, cell in REDUCTION.items():
            with self.subTest(scenario=sid):
                frozen = dataclasses.asdict(bm.run_baseline_scenario(CATALOG[sid]))["metrics"]
                init = "CATALOG_COMPROMISED" if sid == "B0-04" else "CATALOG"
                got = run_cell(cell, init)
                self.assertEqual(got["outcome"], frozen["outcome"])
                self.assertEqual(got["alignment"], frozen["alignment"])
                self.assertEqual(got["security_state"], frozen["security_state"])


class GridProperties(unittest.TestCase):
    def test_cell_ids_unique_and_plan_hash_stable(self):
        ids = [c.cell_id for c in enumerate_cells()]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(plan_sha256(), plan_sha256())

    def test_not_defined_cells_are_recorded(self):
        nd = not_defined_records()
        self.assertTrue(any(r["kind"] == "DELAY" and r["flow"] == "B0" for r in nd))
        self.assertFalse(any(r["kind"] == "DROP" for r in nd))

    def test_retry_budget_absorbs_only_fewer_losses(self):
        absorbed = run_cell(Cell("B0", "OTAR_UPLOAD", "DROP", 2, 3))
        exhausted = run_cell(Cell("B0", "OTAR_UPLOAD", "DROP", 3, 3))
        self.assertEqual(absorbed["outcome"], "SUCCESS")
        self.assertNotEqual(exhausted["outcome"], "SUCCESS")

    def test_every_cell_runs_from_both_initial_states(self):
        for init in ("T1_BASE", "CATALOG", "CATALOG_COMPROMISED"):
            for c in enumerate_cells():
                row = run_cell(c, init)
                self.assertIn(row["security_state"], {"UNSAFE", "SECURE_PROVISIONAL", "NOT_ESTABLISHED"})


class RunnerDeterminism(unittest.TestCase):
    def test_two_runs_have_identical_result_hashes(self):
        import tempfile
        from study_f.run_grid import main
        hashes = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as d:
                main(["--out", d])
                hashes.append(json.loads((Path(d) / "run_manifest.json").read_text())["results_csv_sha256"])
        self.assertEqual(hashes[0], hashes[1])


if __name__ == "__main__":
    unittest.main()
