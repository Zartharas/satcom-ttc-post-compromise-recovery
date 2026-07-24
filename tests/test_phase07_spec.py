import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Phase07SpecTests(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_phase07_status_and_parameters_remain_provisional(self):
        spec = self.load("spec/phase-07-seeded-fault-metrics.json")
        config = self.load("experiments/configs/phase-07-provisional.json")
        self.assertEqual(spec["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY")
        self.assertEqual(config["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY")
        self.assertTrue(spec["unfrozen_parameters"])
        self.assertTrue(
            all(value == "UNFROZEN" for value in config["parameter_status"].values())
        )

    def test_required_fault_classes_and_metrics_are_declared(self):
        spec = self.load("spec/phase-07-seeded-fault-metrics.json")
        required_faults = {
            "DROP",
            "DELAY",
            "DUPLICATE",
            "REORDER",
            "CONTACT_CLOSE",
            "ENDPOINT_RESTART",
        }
        self.assertTrue(required_faults.issubset(set(spec["fault_kinds"])))
        metrics = set(spec["required_metrics"])
        self.assertIn("security_state", metrics)
        self.assertIn("availability_state", metrics)
        self.assertIn("recovery_duration_contacts", metrics)
        self.assertIn("replay_rejection_count", metrics)
        self.assertIn("stale_state_rejection_count", metrics)

    def test_catalog_ids_and_test_names_are_unique(self):
        catalog = self.load("tests/scenarios/phase-07-seeded-fault-catalog.json")
        ids = [scenario["id"] for scenario in catalog["scenarios"]]
        tests = [scenario["test"] for scenario in catalog["scenarios"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(tests), len(set(tests)))
        test_source = (ROOT / "tests/test_fault_metrics.py").read_text(
            encoding="utf-8"
        )
        for test_name in tests:
            self.assertIn(f"def {test_name}(", test_source)

    def test_external_review_stop_points_remain_present(self):
        spec = self.load("spec/phase-07-seeded-fault-metrics.json")
        stops = " ".join(spec["mandatory_external_review_stop_points"])
        self.assertIn("freezing any experiment parameter", stops)
        self.assertIn("post-compromise security", stops)
        self.assertIn("manuscript submission", stops)


if __name__ == "__main__":
    unittest.main()
