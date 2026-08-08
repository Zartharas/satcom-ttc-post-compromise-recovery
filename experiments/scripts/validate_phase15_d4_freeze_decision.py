#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[2]
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
EXPECTED_STATUS = (
    "EXPLICIT_ACCEPT_DECISION_EFFECTIVE_"
    "EXACT_REVIEWED_OBJECTS_FROZEN"
)
EXPECTED_IDS = [
    f"FR-{index:02d}"
    for index in range(1, 17)
]
REQUIRED_WORKFLOWS = {
    "Phase 15 treatment comparability",
    "Python and formal-model tests",
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    decision = load_json(DECISION_PATH)
    review = load_json(REVIEW_PATH)

    require(
        decision["schema_version"] == "0.1.0",
        "Unexpected decision schema",
    )
    require(
        decision["work_package"] == "WP15-D4F",
        "Unexpected work package",
    )
    require(
        decision["record_class"]
        == "WP15_D4_EXPLICIT_FREEZE_DECISION",
        "Unexpected record class",
    )
    require(
        decision["status"] == EXPECTED_STATUS,
        "Unexpected decision status",
    )
    require(
        decision["formal_decision"] == "ACCEPT",
        "Formal decision is not ACCEPT",
    )
    require(
        decision["decision_authorized"] is True,
        "Decision is not authorized",
    )

    reviewer = decision["reviewer"]
    require(
        reviewer["authenticated_identity"]
        == "GitHub:Zartharas",
        "Unexpected authenticated reviewer identity",
    )
    require(
        reviewer["independent_validation_claimed"]
        is False,
        "Independent validation was claimed",
    )
    require(
        "not independent validation"
        in reviewer["conflict_statement"].lower(),
        "Conflict statement is incomplete",
    )

    target = decision["review_target"]
    require(
        target["validated_checkpoint_full"]
        == EXPECTED_TARGET,
        "Reviewed target drifted",
    )

    package = decision["review_package"]
    require(
        package["commit"] == EXPECTED_PACKAGE,
        "Review-package commit drifted",
    )
    require(
        package["pull_request_number"] == 13,
        "Unexpected pull-request number",
    )
    require(
        package["local_focused_tests"]
        == {"tests_run": 9, "result": "PASS"},
        "Focused-test evidence drifted",
    )
    require(
        package["local_complete_regression"]
        == {"tests_run": 245, "result": "PASS"},
        "Regression evidence drifted",
    )
    require(
        package["tracked_file_manifest"]
        == {"entries": 191, "result": "PASS"},
        "Manifest evidence drifted",
    )

    ci = package["ci_validation"]
    require(
        ci["result"] == "PASS",
        "Review-package CI is not PASS",
    )
    require(
        ci["required_workflow_count"] == 2,
        "Required workflow count drifted",
    )
    require(
        ci["successful_workflow_count"] == 2,
        "Successful workflow count drifted",
    )
    runs = ci["selected_runs"]
    require(
        {row["name"] for row in runs}
        == REQUIRED_WORKFLOWS,
        "Required workflow registry drifted",
    )
    for row in runs:
        require(
            row["status"] == "completed",
            f"CI run incomplete: {row['name']}",
        )
        require(
            row["conclusion"] == "success",
            f"CI run unsuccessful: {row['name']}",
        )
        require(
            row["head_sha"] == EXPECTED_PACKAGE,
            f"CI head drifted: {row['name']}",
        )

    blindness = decision["outcome_blind_attestation"]
    require(
        blindness["attested"] is True,
        "Outcome-blind attestation missing",
    )
    for field in (
        "projected_metric_values_viewed",
        "raw_execution_values_viewed",
        "family_outcome_values_viewed",
        "aggregate_results_viewed",
        "comparative_values_viewed",
    ):
        require(
            blindness[field] is False,
            f"Outcome-blind field opened: {field}",
        )

    responses = decision["question_responses"]
    require(
        len(responses) == 16,
        "Decision question count drifted",
    )
    require(
        [row["id"] for row in responses]
        == EXPECTED_IDS,
        "Decision question order drifted",
    )
    for row in responses:
        require(
            row["response"] == "PASS",
            f"Question is not PASS: {row['id']}",
        )
        require(
            bool(row["rationale"].strip()),
            f"Question rationale empty: {row['id']}",
        )
        require(
            bool(row["criterion"].strip()),
            f"Question criterion empty: {row['id']}",
        )

    prerequisites = decision[
        "acceptance_prerequisites"
    ]
    require(
        all(prerequisites.values()),
        "Acceptance prerequisite is false",
    )

    binding = decision[
        "decision_record_commit_binding"
    ]
    require(
        binding["mode"]
        == "EXPLICIT_DECISION_COMMIT_REFERENCE",
        "Decision-record binding drifted",
    )
    require(
        binding["decision_commit"]
        == EXPECTED_DECISION_COMMIT,
        "Decision-record commit reference drifted",
    )
    require(
        binding["decision_record_present_in_decision_commit"]
        is True,
        "Decision record is not bound to decision commit",
    )

    decision_commit = decision["decision_commit"]
    require(
        decision_commit["commit"]
        == EXPECTED_DECISION_COMMIT,
        "Decision commit drifted",
    )
    require(
        decision_commit["formal_decision"] == "ACCEPT",
        "Decision-commit decision drifted",
    )
    require(
        decision_commit["local_validation"][
            "d4f_decision_tests"
        ]
        == {"tests_run": 9, "result": "PASS"},
        "Decision-test evidence drifted",
    )
    require(
        decision_commit["local_validation"][
            "complete_regression"
        ]
        == {"tests_run": 254, "result": "PASS"},
        "Decision regression evidence drifted",
    )
    require(
        decision_commit["local_validation"][
            "tracked_file_manifest"
        ]
        == {"entries": 195, "result": "PASS"},
        "Decision manifest evidence drifted",
    )

    decision_ci = decision_commit["ci_validation"]
    require(
        decision_ci["result"] == "PASS",
        "Decision-commit CI is not PASS",
    )
    require(
        decision_ci["required_workflow_count"] == 2,
        "Decision workflow count drifted",
    )
    require(
        decision_ci["successful_workflow_count"] == 2,
        "Decision successful count drifted",
    )
    require(
        {
            row["name"]: row["id"]
            for row in decision_ci["selected_runs"]
        }
        == EXPECTED_DECISION_RUN_IDS,
        "Decision workflow identities drifted",
    )
    for row in decision_ci["selected_runs"]:
        require(
            row["status"] == "completed",
            f"Decision CI run incomplete: {row['name']}",
        )
        require(
            row["conclusion"] == "success",
            f"Decision CI run unsuccessful: {row['name']}",
        )
        require(
            row["head_sha"] == EXPECTED_DECISION_COMMIT,
            f"Decision CI head drifted: {row['name']}",
        )

    effectiveness = decision[
        "freeze_effectiveness"
    ]
    require(
        effectiveness["state"] == "EFFECTIVE",
        "Freeze is not effective",
    )
    require(
        effectiveness["reason"]
        == (
            "ACCEPT_DECISION_AND_EXACT_"
            "DECISION_COMMIT_CI_PASS"
        ),
        "Freeze-effectiveness reason drifted",
    )
    require(
        effectiveness["decision_commit"]
        == EXPECTED_DECISION_COMMIT,
        "Effectiveness commit drifted",
    )
    require(
        effectiveness[
            "decision_commit_ci_validation"
        ]
        == "PASS",
        "Effectiveness CI is not PASS",
    )
    require(
        effectiveness["effectiveness_rule_satisfied"]
        is True,
        "Effectiveness rule is not satisfied",
    )
    require(
        bool(effectiveness["effective_utc"]),
        "Effective UTC is empty",
    )
    require(
        {
            row["name"]: row["id"]
            for row in effectiveness[
                "ci_evidence"
            ]["selected_runs"]
        }
        == EXPECTED_DECISION_RUN_IDS,
        "Effectiveness CI identities drifted",
    )

    effects = decision[
        "decision_effects_on_effectiveness"
    ]
    for field in (
        "observation_cutoffs",
        "analysis_unit_denominators",
        "member_registry",
        "allowed_planning_displays",
    ):
        require(
            effects[field]
            == "EXACT_REVIEWED_OBJECT_FROZEN",
            f"Decision effect drifted: {field}",
        )
    require(
        effects["publication_analysis_plan"]
        == "NOT_FROZEN",
        "Publication plan was frozen",
    )

    boundary = decision["claim_boundary"]
    require(
        boundary["family_member_value_display"]
        == "NOT_YET_AUTHORIZED",
        "Member-value display gate opened",
    )
    require(
        boundary[
            "family_specific_descriptive_comparison"
        ]
        == "NOT_YET_AUTHORIZED",
        "Family-comparison gate opened",
    )
    require(
        boundary["success_rate_denominator"]
        == "NOT_DEFINED",
        "Success-rate denominator defined",
    )
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
        require(
            boundary[field] == "NOT_PERMITTED",
            f"Claim gate opened: {field}",
        )

    require(
        decision["publication_evidence"] is False,
        "Publication evidence was asserted",
    )

    require(
        review["current_decision"]["decision"]
        == "PENDING",
        "Immutable review package was mutated",
    )
    require(
        review["current_decision"][
            "decision_authorized"
        ]
        is False,
        "Immutable review package was authorized",
    )

    print(
        "Phase 15 D4 explicit decision valid: "
        "decision=ACCEPT, questions=16_PASS, "
        "review_package_ci=PASS, "
        "decision_commit_ci=PASS, "
        "freeze=EFFECTIVE, "
        "publication_evidence=false."
    )


if __name__ == "__main__":
    main()
