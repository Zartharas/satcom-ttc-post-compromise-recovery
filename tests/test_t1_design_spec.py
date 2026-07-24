import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "spec" / "t1-provisional-design.json"
CATALOG = ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json"
TEST_FILE = ROOT / "tests" / "test_t1_controller.py"


class ProvisionalT1DesignSpecTests(unittest.TestCase):
    def setUp(self):
        self.design = json.loads(DESIGN.read_text(encoding="utf-8"))
        self.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_design_remains_provisional_and_review_gated(self):
        self.assertEqual(
            self.design["status"],
            "PROVISIONAL_INTERNAL_REVIEW_ONLY",
        )
        self.assertEqual(
            self.design["review_status"]["independent_cryptography_review"],
            "NOT_YET_PERFORMED",
        )
        self.assertIn(
            "before manuscript submission or external security claims",
            self.design["mandatory_external_review_stop_points"],
        )

    def test_scenario_ids_and_test_names_are_unique(self):
        cases = self.catalog["tests"]
        ids = [case["id"] for case in cases]
        names = [case["test"] for case in cases]
        self.assertEqual(len(ids), 15)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(names), len(set(names)))

    def test_catalog_references_implemented_tests(self):
        source = TEST_FILE.read_text(encoding="utf-8")
        for case in self.catalog["tests"]:
            self.assertIn(f"def {case['test']}(", source)


if __name__ == "__main__":
    unittest.main()
