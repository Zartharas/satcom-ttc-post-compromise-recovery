from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION_PATH = (
    ROOT / "spec" / "phase-15-d4-freeze-decision.json"
)
REVIEW_PATH = (
    ROOT / "spec" / "phase-15-d4-freeze-review.json"
)
EXPECTED_TARGET = (
    "34d63a554646baddd9fadf58678cfe70392fc41d"
)
EXPECTED_PACKAGE = (
    "d321f927aff20636490ae8c8cf407410e42c6fbe"
)
EXPECTED_DECISION_COMMIT = (
    "307f685389d799fb5b22d481763bd171393085db"
)
EXPECTED_DECISION_RUN_IDS = {
    "Phase 15 treatment comparability": 30942565654,
    "Python and formal-model tests": 30942565653,
}


class Phase15D4FreezeDecisionTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.decision = json.loads(
            DECISION_PATH.read_text(
                encoding="utf-8"
            )
        )
        cls.review = json.loads(
            REVIEW_PATH.read_text(
                encoding="utf-8"
            )
        )

    def test_formal_decision_is_exact_accept(self) -> None:
        self.assertEqual(
            self.decision["formal_decision"],
            "ACCEPT",
        )
        self.assertTrue(
            self.decision["decision_authorized"]
        )

    def test_exact_review_identities_are_bound(
        self,
    ) -> None:
        self.assertEqual(
            self.decision["review_target"][
                "validated_checkpoint_full"
            ],
            EXPECTED_TARGET,
        )
        self.assertEqual(
            self.decision["review_package"][
                "commit"
            ],
            EXPECTED_PACKAGE,
        )
        self.assertEqual(
            self.decision["decision_commit"][
                "commit"
            ],
            EXPECTED_DECISION_COMMIT,
        )

    def test_all_sixteen_questions_pass(
        self,
    ) -> None:
        responses = self.decision[
            "question_responses"
        ]
        self.assertEqual(len(responses), 16)
        self.assertEqual(
            [row["id"] for row in responses],
            [
                f"FR-{index:02d}"
                for index in range(1, 17)
            ],
        )
        self.assertTrue(
            all(
                row["response"] == "PASS"
                and row["rationale"].strip()
                for row in responses
            )
        )

    def test_review_package_ci_is_exact(
        self,
    ) -> None:
        ci = self.decision["review_package"][
            "ci_validation"
        ]
        self.assertEqual(ci["result"], "PASS")
        self.assertEqual(
            ci["required_workflow_count"],
            2,
        )
        self.assertEqual(
            ci["successful_workflow_count"],
            2,
        )
        self.assertEqual(
            {
                row["name"]
                for row in ci["selected_runs"]
            },
            {
                "Phase 15 treatment comparability",
                "Python and formal-model tests",
            },
        )
        self.assertTrue(
            all(
                row["status"] == "completed"
                and row["conclusion"] == "success"
                and row["head_sha"]
                == EXPECTED_PACKAGE
                for row in ci["selected_runs"]
            )
        )

    def test_outcome_blindness_is_preserved(
        self,
    ) -> None:
        attestation = self.decision[
            "outcome_blind_attestation"
        ]
        self.assertTrue(attestation["attested"])
        for field in (
            "projected_metric_values_viewed",
            "raw_execution_values_viewed",
            "family_outcome_values_viewed",
            "aggregate_results_viewed",
            "comparative_values_viewed",
        ):
            self.assertFalse(attestation[field])

    def test_decision_commit_ci_is_exact_and_effective(
        self,
    ) -> None:
        ci = self.decision["decision_commit"][
            "ci_validation"
        ]
        self.assertEqual(ci["result"], "PASS")
        self.assertEqual(
            {
                row["name"]: row["id"]
                for row in ci["selected_runs"]
            },
            EXPECTED_DECISION_RUN_IDS,
        )
        self.assertTrue(
            all(
                row["status"] == "completed"
                and row["conclusion"] == "success"
                and row["head_sha"]
                == EXPECTED_DECISION_COMMIT
                for row in ci["selected_runs"]
            )
        )

        effectiveness = self.decision[
            "freeze_effectiveness"
        ]
        self.assertEqual(
            effectiveness["state"],
            "EFFECTIVE",
        )
        self.assertEqual(
            effectiveness[
                "decision_commit_ci_validation"
            ],
            "PASS",
        )
        self.assertTrue(
            effectiveness[
                "effectiveness_rule_satisfied"
            ]
        )

        effects = self.decision[
            "decision_effects_on_effectiveness"
        ]
        for field in (
            "observation_cutoffs",
            "analysis_unit_denominators",
            "member_registry",
            "allowed_planning_displays",
        ):
            self.assertEqual(
                effects[field],
                "EXACT_REVIEWED_OBJECT_FROZEN",
            )
        self.assertEqual(
            effects["publication_analysis_plan"],
            "NOT_FROZEN",
        )

    def test_decision_commit_binding_is_explicit(
        self,
    ) -> None:
        binding = self.decision[
            "decision_record_commit_binding"
        ]
        self.assertEqual(
            binding["mode"],
            "EXPLICIT_DECISION_COMMIT_REFERENCE",
        )
        self.assertEqual(
            binding["decision_commit"],
            EXPECTED_DECISION_COMMIT,
        )
        self.assertTrue(
            binding[
                "decision_record_present_in_decision_commit"
            ]
        )

    def test_claim_and_publication_gates_remain_closed(
        self,
    ) -> None:
        boundary = self.decision[
            "claim_boundary"
        ]
        self.assertEqual(
            boundary[
                "family_member_value_display"
            ],
            "NOT_YET_AUTHORIZED",
        )
        self.assertEqual(
            boundary[
                "family_specific_descriptive_comparison"
            ],
            "NOT_YET_AUTHORIZED",
        )
        self.assertEqual(
            boundary["success_rate_denominator"],
            "NOT_DEFINED",
        )
        self.assertFalse(
            self.decision["publication_evidence"]
        )

    def test_review_package_remains_immutable_pending(
        self,
    ) -> None:
        current = self.review[
            "current_decision"
        ]
        self.assertEqual(
            current["decision"],
            "PENDING",
        )
        self.assertFalse(
            current["decision_authorized"]
        )


if __name__ == "__main__":
    unittest.main()
