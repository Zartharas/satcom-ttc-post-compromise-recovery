from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec" / "phase-12-adverse-outcome-witnesses.json"


class Phase12SpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))

    def test_status_and_claim_boundaries_remain_provisional(self) -> None:
        self.assertEqual(self.spec["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY")
        self.assertEqual(self.spec["formal_model_completeness_claim"], "NOT_PERMITTED")
        self.assertEqual(self.spec["implementation_equivalence_claim"], "NOT_PERMITTED")
        self.assertEqual(self.spec["cryptographic_security_claim"], "NOT_PERMITTED")
        self.assertEqual(self.spec["publication_evidence_status"], "NOT_PERMITTED")
        self.assertEqual(self.spec["baseline_review_status"], "PENDING_INDEPENDENT_REVIEW")

    def test_projection_matches_phase11_field_set(self) -> None:
        projection = self.spec["projection"]
        self.assertEqual(projection["field_count"], 16)
        self.assertEqual(len(projection["fields"]), len(set(projection["fields"])))
        self.assertIn("receipt", projection["fields"])
        self.assertIn("outcome", projection["fields"])
        self.assertEqual(projection["mismatch_status"], "MISMATCH_REQUIRES_REVIEW")

    def test_captured_and_absent_outcome_sets_are_explicit(self) -> None:
        self.assertEqual(
            {row["outcome"] for row in self.spec["captured_witnesses"]},
            {"INDETERMINATE", "SECURE_DEGRADED", "EXPIRED"},
        )
        self.assertEqual(
            {row["outcome"] for row in self.spec["absence_diagnostics"]},
            {"DIVERGED", "AVAILABLE_UNSAFE", "LOCKED"},
        )

    def test_absence_language_is_bounded_and_abstraction_specific(self) -> None:
        for row in self.spec["absence_diagnostics"]:
            self.assertEqual(row["expected_status"], "NOT_REACHED_WITHIN_RECORDED_BOUND")
            self.assertEqual(
                row["expected_diagnosis"],
                "ABSENT_FROM_CURRENT_TRANSITION_ASSIGNMENTS",
            )

    def test_reachability_properties_and_configs_exist(self) -> None:
        tla_text = (ROOT / "formal" / "tla" / "T1Recovery.tla").read_text(encoding="utf-8")
        for row in self.spec["captured_witnesses"] + self.spec["absence_diagnostics"]:
            self.assertIn(row["property"], tla_text)
            config_path = ROOT / row["config"]
            self.assertTrue(config_path.is_file())
            self.assertIn(row["property"], config_path.read_text(encoding="utf-8"))

    def test_required_outputs_cover_witnesses_comparisons_logs_and_manifest(self) -> None:
        outputs = set(self.spec["required_outputs"])
        self.assertEqual(len(outputs), 17)
        self.assertIn("phase12-adverse-outcome-validation.json", outputs)
        self.assertIn("phase12-unreached-outcomes.csv", outputs)
        self.assertIn("phase12-derived-bundle.sha256", outputs)
        for case_id in ("indeterminate", "secure-degraded", "expired"):
            self.assertIn(f"phase12-witness-{case_id}.json", outputs)
            self.assertIn(f"phase12-comparison-{case_id}.csv", outputs)

    def test_external_review_stop_points_cover_equivalence_completeness_and_publication(self) -> None:
        joined = " ".join(self.spec["external_review_stop_points"]).lower()
        self.assertIn("implementation equivalence", joined)
        self.assertIn("model completeness", joined)
        self.assertIn("impossibility", joined)
        self.assertIn("publication evidence", joined)


if __name__ == "__main__":
    unittest.main()
