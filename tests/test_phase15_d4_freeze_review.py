from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = ROOT / "spec" / "phase-15-d4-freeze-review.json"
D4_PATH = (
    ROOT
    / "experiments"
    / "configs"
    / "phase-15-family-descriptive-plan.json"
)
MATRIX_PATH = ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Phase15D4FreezeReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.review = load_json(REVIEW_PATH)
        cls.d4 = load_json(D4_PATH)
        cls.matrix = load_json(MATRIX_PATH)

    def test_review_target_is_exact_validated_checkpoint(self) -> None:
        target = self.review["review_target"]
        self.assertEqual(target["validated_checkpoint"], "34d63a5")
        self.assertEqual(
            target["candidate_contract"],
            "experiments/configs/phase-15-family-descriptive-plan.json",
        )
        self.assertEqual(
            target["authoritative_comparability_matrix"],
            "spec/phase-15-treatment-comparability-matrix.json",
        )

    def test_review_remains_pending_and_cannot_implicitly_freeze(self) -> None:
        self.assertEqual(
            self.review["status"],
            "REVIEW_PACKAGE_DEFINED_DECISION_PENDING_NOT_FROZEN",
        )
        decision = self.review["current_decision"]
        self.assertEqual(decision["decision"], "PENDING")
        self.assertFalse(decision["decision_authorized"])
        self.assertEqual(decision["reviewer"], "PENDING")
        self.assertEqual(decision["reviewed_commit"], "PENDING")
        self.assertEqual(
            self.review["decision_prerequisites"]["implicit_acceptance"],
            "NOT_PERMITTED",
        )

    def test_review_is_outcome_blind(self) -> None:
        blindness = self.review["outcome_blindness"]
        self.assertTrue(blindness["required"])
        for field in (
            "projected_metric_values_read",
            "raw_execution_values_read",
            "family_outcome_values_read",
            "aggregate_results_read",
        ):
            self.assertFalse(blindness[field])
        prohibited = set(blindness["prohibited_evidence"])
        self.assertIn("family outcome distributions", prohibited)
        self.assertIn("success counts or percentages", prohibited)
        self.assertIn("hypothesis-test results", prohibited)

    def test_questions_are_complete_unique_and_unanswered(self) -> None:
        questions = self.review["review_questions"]
        self.assertEqual(len(questions), 16)
        self.assertEqual(
            [row["id"] for row in questions],
            [f"FR-{index:02d}" for index in range(1, 17)],
        )
        self.assertEqual(len({row["subject"] for row in questions}), 16)
        for row in questions:
            self.assertEqual(row["response"], "PENDING")
            self.assertEqual(row["rationale"], "PENDING")
            self.assertTrue(row["criterion"])

    def test_acceptance_requires_pass_ci_and_explicit_record(self) -> None:
        prerequisites = self.review["decision_prerequisites"]
        self.assertEqual(prerequisites["required_question_count"], 16)
        for field in (
            "accept_requires_all_questions_pass",
            "accept_requires_exact_reviewed_commit",
            "accept_requires_local_validation",
            "accept_requires_ci_validation",
            "accept_requires_explicit_decision_record",
        ):
            self.assertTrue(prerequisites[field])

    def test_d4_population_and_cutoffs_are_exact(self) -> None:
        plans = self.d4["family_plans"]
        self.assertEqual(
            [row["family_id"] for row in plans],
            ["CF-01", "CF-02", "CF-05", "CF-06"],
        )
        members = [
            member
            for row in plans
            for member in row["expected_member_row_ids"]
        ]
        units = [
            unit
            for row in plans
            for unit in row["expected_analysis_unit_ids"]
        ]
        cutoffs = [row["cutoff_id"] for row in plans]
        self.assertEqual(len(members), 13)
        self.assertEqual(len(set(members)), 13)
        self.assertEqual(len(units), 12)
        self.assertEqual(len(set(units)), 12)
        self.assertEqual(len(cutoffs), 4)
        self.assertEqual(len(set(cutoffs)), 4)
        self.assertTrue(
            all(row["observation_cutoff"].startswith("Stop ") for row in plans)
        )

    def test_d4_allowed_fields_match_d2_exactly(self) -> None:
        matrix = {
            row["id"]: row
            for row in self.matrix["comparison_families"]
        }
        for plan in self.d4["family_plans"]:
            family = matrix[plan["family_id"]]
            self.assertEqual(family["classification"], "QUALIFIED_MATCH")
            self.assertEqual(
                plan["expected_allowed_fields"],
                family["allowed_fields"],
            )

    def test_cf02_policy_variants_share_one_analysis_unit(self) -> None:
        cf02 = next(
            row
            for row in self.d4["family_plans"]
            if row["family_id"] == "CF-02"
        )
        self.assertEqual(
            cf02["expected_member_row_ids"][1:3],
            ["CF-02:B1:B1-01", "CF-02:B1:B1-05"],
        )
        self.assertEqual(
            cf02["expected_analysis_unit_ids"].count("CF-02:B1"),
            1,
        )

    def test_freeze_and_claim_gates_remain_closed(self) -> None:
        self.assertEqual(
            self.review["freeze_state"],
            {
                "observation_cutoffs": "CANDIDATE_NOT_FROZEN",
                "analysis_unit_denominators": "CANDIDATE_NOT_FROZEN",
                "member_registry": "CANDIDATE_NOT_FROZEN",
                "allowed_displays": "CANDIDATE_NOT_FROZEN",
                "publication_analysis_plan": "NOT_FROZEN",
            },
        )
        boundary = self.review["claim_boundary"]
        self.assertEqual(
            boundary["family_member_value_display"],
            "NOT_YET_AUTHORIZED",
        )
        self.assertEqual(
            boundary["family_specific_descriptive_comparison"],
            "NOT_YET_AUTHORIZED",
        )
        self.assertEqual(boundary["success_rate_denominator"], "NOT_DEFINED")
        for field in (
            "pooled_cross_treatment_aggregation",
            "success_rate_or_percentage",
            "inferential_statistics",
            "treatment_superiority",
            "causal_interpretation",
            "cryptographic_security_or_pcs",
            "independent_validation",
            "publication_evidence",
        ):
            self.assertEqual(boundary[field], "NOT_PERMITTED")


if __name__ == "__main__":
    unittest.main()
