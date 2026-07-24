import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "experiments" / "configs" / "phase-08-provisional.json"
SPEC_PATH = ROOT / "spec" / "phase-08-provisional-analysis.json"
CATALOG_PATH = (
    ROOT / "tests" / "scenarios" / "phase-08-provisional-analysis-catalog.json"
)
TEST_PATH = ROOT / "tests" / "test_provisional_analysis.py"


class Phase08SpecTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        self.spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        self.catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        self.test_source = TEST_PATH.read_text(encoding="utf-8")

    def test_phase08_status_and_claim_boundaries_remain_provisional(self):
        self.assertEqual(
            self.config["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY"
        )
        self.assertEqual(
            self.spec["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY"
        )
        self.assertEqual(
            self.config["analysis_scope"],
            "DESCRIPTIVE_AND_SENSITIVITY_SCAFFOLD_ONLY",
        )
        self.assertEqual(
            self.config["claim_boundary"]["causal_inference"], "NOT_PERMITTED"
        )
        self.assertEqual(
            self.config["claim_boundary"]["hypothesis_testing"], "NOT_PERFORMED"
        )
        self.assertEqual(
            self.config["claim_boundary"]["post_compromise_security_claim"],
            "NOT_PERMITTED",
        )

    def test_analysis_grid_and_denominator_rules_are_unfrozen(self):
        parameter_status = self.config["parameter_status"]
        self.assertTrue(
            all(
                value in {"UNFROZEN", "NOT_DEFINED"}
                for value in parameter_status.values()
            )
        )
        self.assertTrue(
            self.config["denominator_policy"]["overlapping_fault_groups_must_be_declared"]
        )
        self.assertTrue(self.config["denominator_policy"]["retain_low_n_groups"])
        self.assertEqual(
            self.config["sensitivity_scaffold"]["fixed_input"],
            "SERIALIZED_PHASE_07_SCHEDULES",
        )
        self.assertEqual(
            self.config["sensitivity_scaffold"]["grid_status"], "UNFROZEN"
        )

    def test_external_review_stop_points_cover_finalization_and_claims(self):
        stop_points = " ".join(
            self.spec["mandatory_external_review_stop_points"]
        ).lower()
        for phrase in (
            "experiment population",
            "retry budgets",
            "denominator exclusions",
            "statistical analysis plan",
            "final treatment",
            "post-compromise security",
            "publication evidence",
        ):
            self.assertIn(phrase, stop_points)

    def test_catalog_ids_and_test_names_are_unique_and_implemented(self):
        scenarios = self.catalog["scenarios"]
        ids = [scenario["id"] for scenario in scenarios]
        test_names = [scenario["test"] for scenario in scenarios]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(test_names), len(set(test_names)))
        for test_name in test_names:
            self.assertIn(f"def {test_name}(", self.test_source)

    def test_required_outputs_include_a_derived_checksum_manifest(self):
        outputs = set(self.config["required_outputs"])
        self.assertIn("phase08-analysis.json", outputs)
        self.assertIn("phase08-trace-anomalies.csv", outputs)
        self.assertIn("phase08-adverse-cases.csv", outputs)
        self.assertIn("phase08-sensitivity-summary.csv", outputs)
        self.assertIn("phase08-derived-bundle.sha256", outputs)


if __name__ == "__main__":
    unittest.main()
