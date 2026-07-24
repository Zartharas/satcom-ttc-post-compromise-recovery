from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


class Phase13SpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.spec = json.loads(
            (cls.root / "spec" / "phase-13-abstraction-gap-outcomes.json").read_text(
                encoding="utf-8"
            )
        )
        cls.baseline_path = cls.root / cls.spec["baseline_preservation"]["module"]
        cls.expanded_path = cls.root / cls.spec["expansion"]["module"]
        cls.baseline_text = cls.baseline_path.read_text(encoding="utf-8")
        cls.expanded_text = cls.expanded_path.read_text(encoding="utf-8")

    def test_status_and_claim_boundaries_remain_provisional(self):
        self.assertEqual(self.spec["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY")
        self.assertEqual(self.spec["baseline_review_status"], "PENDING_INDEPENDENT_REVIEW")
        self.assertEqual(
            {
                self.spec["formal_model_completeness_claim"],
                self.spec["implementation_equivalence_claim"],
                self.spec["cryptographic_security_claim"],
                self.spec["publication_evidence_status"],
            },
            {"NOT_PERMITTED"},
        )

    def test_preserved_baseline_hash_matches_contract(self):
        actual = hashlib.sha256(self.baseline_path.read_bytes()).hexdigest()
        self.assertEqual(actual, self.spec["baseline_preservation"]["expected_sha256"])
        self.assertEqual(self.spec["baseline_preservation"]["expected_status"], "BASELINE_PRESERVED")

    def test_expansion_is_separate_and_diagnostic_only(self):
        self.assertNotEqual(self.baseline_path, self.expanded_path)
        self.assertEqual(
            self.spec["expansion"]["status"],
            "EXPANDED_OUTCOME_POPULATION_DIAGNOSTIC_ONLY",
        )
        self.assertIn("EXTENDS T1Recovery", self.expanded_text)
        self.assertIn("VARIABLE gapCause", self.expanded_text)

    def test_witnesses_have_unique_outcomes_causes_and_paths(self):
        rows = self.spec["expanded_witnesses"]
        self.assertEqual({row["outcome"] for row in rows}, {"DIVERGED", "AVAILABLE_UNSAFE", "LOCKED"})
        self.assertEqual(len({row["cause"] for row in rows}), 3)
        self.assertEqual(len({tuple(row["expected_actions"]) for row in rows}), 3)

    def test_baseline_has_zero_assignments_and_expansion_has_one(self):
        for row in self.spec["expanded_witnesses"]:
            assignment = f'outcome\' = "{row["outcome"]}"'
            with self.subTest(outcome=row["outcome"]):
                self.assertNotIn(assignment, self.baseline_text)
                self.assertEqual(self.expanded_text.count(assignment), 1)

    def test_properties_and_configs_are_present(self):
        for row in self.spec["expanded_witnesses"]:
            with self.subTest(case=row["case_id"]):
                config = self.root / row["config"]
                baseline_config = self.root / row["baseline_config"]
                self.assertTrue(config.is_file())
                self.assertTrue(baseline_config.is_file())
                self.assertIn(row["property"], self.expanded_text)
                self.assertIn(row["property"], config.read_text(encoding="utf-8"))

    def test_projection_matches_phase12_field_set(self):
        phase12 = json.loads(
            (self.root / "spec" / "phase-12-adverse-outcome-witnesses.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(self.spec["projection"]["fields"], phase12["projection"]["fields"])
        self.assertEqual(self.spec["projection"]["field_count"], 16)

    def test_required_outputs_cover_baseline_expansion_and_manifest(self):
        outputs = set(self.spec["required_outputs"])
        self.assertEqual(len(outputs), 19)
        self.assertIn("phase13-baseline-regression.csv", outputs)
        self.assertIn("phase13-expansion-assignment-audit.csv", outputs)
        self.assertIn("phase13-derived-bundle.sha256", outputs)
        for case_id in ("diverged", "available-unsafe", "locked"):
            self.assertIn(f"phase13-witness-{case_id}.json", outputs)
            self.assertIn(f"phase13-comparison-{case_id}.csv", outputs)

    def test_external_review_stop_points_cover_completeness_and_publication(self):
        text = " ".join(self.spec["external_review_stop_points"]).lower()
        for phrase in (
            "complete or realistic",
            "refinement proof",
            "replacing the preserved baseline",
            "concrete cryptographic protocol",
            "publication evidence",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
