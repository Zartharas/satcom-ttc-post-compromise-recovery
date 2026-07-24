import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from ttc_recovery.fault_metrics import ExperimentPhase, FaultKind
from ttc_recovery.formal_coverage import (
    BOUND_STATUS,
    build_coverage_scenarios,
    build_phase09_bundle,
    build_reachability_report,
    invariant_traceability,
    run_coverage_suite,
    write_phase09_outputs,
)


class FormalCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenarios = build_coverage_scenarios()
        cls.rows = run_coverage_suite(cls.scenarios)

    def test_catalog_has_24_unique_scenarios(self):
        ids = [scenario.scenario_id for scenario in self.scenarios]
        self.assertEqual(len(ids), 24)
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_fault_kinds_and_protocol_phases_are_covered(self):
        kinds = {
            action.kind
            for scenario in self.scenarios
            for action in scenario.schedule
        }
        phases = {
            action.phase
            for scenario in self.scenarios
            for action in scenario.schedule
        }
        self.assertEqual(kinds, set(FaultKind))
        self.assertEqual(phases, set(ExperimentPhase))

    def test_required_boundaries_are_present(self):
        tags = {
            tag
            for scenario in self.scenarios
            for tag in scenario.boundary_tags
        }
        required = {
            "retry_budget_minus_one",
            "retry_budget_equal",
            "retry_budget_plus_one",
            "candidate_lifetime_equal",
            "candidate_lifetime_plus_one",
            "spacecraft_ahead",
            "authority_epoch_floor",
            "multi_fault",
        }
        self.assertTrue(required.issubset(tags))

    def test_key_outcome_witnesses_are_reached(self):
        by_id = {row["scenario_id"]: row for row in self.rows}
        self.assertEqual(by_id["P09-001"]["outcome"], "SUCCESS")
        self.assertEqual(by_id["P09-010"]["outcome"], "INDETERMINATE")
        self.assertEqual(by_id["P09-012"]["outcome"], "SECURE_DEGRADED")
        self.assertEqual(by_id["P09-013"]["outcome"], "EXPIRED")

    def test_candidate_lifetime_boundary_is_distinguished(self):
        by_id = {row["scenario_id"]: row for row in self.rows}
        self.assertEqual(by_id["P09-016"]["outcome"], "SUCCESS")
        self.assertEqual(by_id["P09-017"]["outcome"], "EXPIRED")

    def test_unreachable_fault_actions_are_counted(self):
        row = next(row for row in self.rows if row["scenario_id"] == "P09-015")
        self.assertEqual(row["reachable_fault_actions"], 3)
        self.assertEqual(row["unreachable_fault_actions"], 1)

    def test_reachability_uses_bounded_non_claim_language(self):
        report = build_reachability_report(self.rows)
        statuses = {row["reachability"] for row in report["outcomes"]}
        self.assertTrue(statuses.issubset({"REACHED", BOUND_STATUS}))
        self.assertIn(BOUND_STATUS, statuses)
        self.assertEqual(
            report["bound_interpretation"],
            "Unreached does not mean impossible.",
        )

    def test_shortest_witness_is_selected_deterministically(self):
        report = build_reachability_report(self.rows)
        success = next(row for row in report["outcomes"] if row["value"] == "SUCCESS")
        self.assertEqual(success["witness_scenario_id"], "P09-001")
        self.assertEqual(success["witness_schedule_length"], 0)

    def test_invariant_traceability_is_complete_and_unique(self):
        rows = invariant_traceability()
        ids = [row["invariant_id"] for row in rows]
        scenario_ids = {scenario.scenario_id for scenario in self.scenarios}
        self.assertEqual(len(rows), 13)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(row["coverage_scenario"] in scenario_ids for row in rows))
        self.assertTrue(all(row["formal_property"] for row in rows))

    def test_outputs_are_complete_and_checksummed(self):
        bundle = build_phase09_bundle()
        with tempfile.TemporaryDirectory() as directory:
            paths = write_phase09_outputs(bundle, Path(directory))
            self.assertEqual(len(paths), 5)
            manifest = Path(paths["checksum_manifest"])
            lines = manifest.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 4)
            for line in lines:
                expected, name = line.split(maxsplit=1)
                actual = hashlib.sha256((Path(directory) / name).read_bytes()).hexdigest()
                self.assertEqual(actual, expected)

            with Path(paths["reachability_csv"]).open(
                "r", encoding="utf-8", newline=""
            ) as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 13)

            payload = json.loads(Path(paths["analysis_json"]).read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY")
            self.assertEqual(len(payload["coverage_rows"]), 24)


if __name__ == "__main__":
    unittest.main()
