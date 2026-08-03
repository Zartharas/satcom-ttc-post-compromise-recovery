from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from ttc_recovery.baseline_metrics import (
    BaselineMetrics,
    PARITY_STATUS,
    SHARED_METRIC_FIELDS,
    run_baseline_catalog,
    run_baseline_scenario,
    write_baseline_results,
)
from ttc_recovery.fault_metrics import RecoveryMetrics


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"


class BaselineMetricParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        cls.entries = cls.catalog["tests"]
        cls.results = run_baseline_catalog(cls.entries)

    def test_all_21_catalog_scenarios_execute(self) -> None:
        self.assertEqual(len(self.results), 21)
        self.assertEqual(
            [result.scenario_id for result in self.results],
            [entry["id"] for entry in self.entries],
        )
        self.assertEqual(
            {result.treatment for result in self.results},
            {"B0", "B1", "B2"},
        )

    def test_shared_metric_fields_match_t1_schema(self) -> None:
        self.assertEqual(
            SHARED_METRIC_FIELDS,
            tuple(RecoveryMetrics.__dataclass_fields__.keys()),
        )
        baseline_fields = set(BaselineMetrics.__dataclass_fields__.keys())
        self.assertTrue(set(SHARED_METRIC_FIELDS).issubset(baseline_fields))

    def test_every_result_matches_existing_catalog_oracle(self) -> None:
        for entry, result in zip(self.entries, self.results):
            self.assertEqual(result.metrics.outcome, entry["expected_outcome"])
            self.assertEqual(result.metrics.alignment, entry["expected_alignment"])
            self.assertEqual(result.metric_parity_status, PARITY_STATUS)
            self.assertFalse(
                any(
                    event.get("publication_evidence") is True
                    for event in result.event_log
                )
            )

    def test_deterministic_scenarios_use_null_seed_and_unique_hashes(self) -> None:
        hashes = [result.metrics.schedule_sha256 for result in self.results]
        self.assertEqual(len(hashes), len(set(hashes)))
        self.assertTrue(all(result.metrics.seed is None for result in self.results))
        self.assertTrue(all(len(value) == 64 for value in hashes))

    def test_fault_normalization_preserves_key_catalog_cases(self) -> None:
        by_id = {result.scenario_id: result for result in self.results}
        self.assertEqual(by_id["B0-04"].metrics.drop_count, 1)
        self.assertEqual(by_id["B1-03"].metrics.reorder_count, 1)
        self.assertEqual(by_id["B2-09"].metrics.restart_count, 1)
        self.assertEqual(by_id["B2-10"].metrics.replay_count, 1)
        self.assertEqual(by_id["B2-10"].metrics.replay_rejection_count, 1)
        self.assertEqual(by_id["B2-06"].metrics.other_fault_count, 1)

    def test_adapter_security_and_availability_dimensions_are_separate(self) -> None:
        by_id = {result.scenario_id: result for result in self.results}
        self.assertEqual(by_id["B0-03"].metrics.security_state, "UNSAFE")
        self.assertEqual(by_id["B0-03"].metrics.availability_state, "DEGRADED")
        self.assertEqual(by_id["B2-07"].metrics.security_state, "NOT_ESTABLISHED")
        self.assertEqual(by_id["B2-07"].metrics.availability_state, "UNAVAILABLE")
        self.assertEqual(by_id["B2-08"].metrics.availability_state, "DEGRADED")

    def test_adapter_completion_event_is_retained(self) -> None:
        result = run_baseline_scenario(self.entries[0])
        completion = [
            event
            for event in result.event_log
            if event.get("event") == "phase15_baseline_metric_adapter_complete"
        ]
        self.assertEqual(len(completion), 1)
        self.assertEqual(completion[0]["scenario_id"], "B0-01")
        self.assertEqual(completion[0]["contact"], 1)
        self.assertFalse(completion[0]["publication_evidence"])

    def test_json_and_csv_outputs_preserve_all_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            json_path = root / "baseline-results.json"
            csv_path = root / "baseline-metrics.csv"
            write_baseline_results(self.results, json_path, csv_path)

            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["result_count"], 21)
            self.assertEqual(payload["metric_parity_status"], PARITY_STATUS)
            self.assertFalse(payload["publication_evidence"])
            self.assertEqual(
                payload["shared_metric_fields"],
                list(SHARED_METRIC_FIELDS),
            )

            with csv_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 21)
            self.assertEqual(rows[0]["scenario_id"], "B0-01")
            self.assertEqual(rows[-1]["scenario_id"], "B2-10")
            self.assertEqual(rows[0]["seed"], "")


if __name__ == "__main__":
    unittest.main()
