#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[2]
REVIEW_PATH = ROOT / "spec" / "phase-15-d4-freeze-review.json"
D4_PATH = (
    ROOT
    / "experiments"
    / "configs"
    / "phase-15-family-descriptive-plan.json"
)
MATRIX_PATH = ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"

EXPECTED_STATUS = "REVIEW_PACKAGE_DEFINED_DECISION_PENDING_NOT_FROZEN"
EXPECTED_REVIEW_CLASS = "OUTCOME_BLIND_INTERNAL_PROTOCOL_REVIEW"
EXPECTED_FAMILIES = ["CF-01", "CF-02", "CF-05", "CF-06"]
EXPECTED_DECISIONS = ["ACCEPT", "REVISE", "REJECT", "DEFER"]
EXPECTED_QUESTION_IDS = [f"FR-{index:02d}" for index in range(1, 17)]
EXPECTED_FREEZE_STATE = {
    "observation_cutoffs": "CANDIDATE_NOT_FROZEN",
    "analysis_unit_denominators": "CANDIDATE_NOT_FROZEN",
    "member_registry": "CANDIDATE_NOT_FROZEN",
    "allowed_displays": "CANDIDATE_NOT_FROZEN",
    "publication_analysis_plan": "NOT_FROZEN",
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def indexed(rows: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        value = str(row[key])
        require(value not in result, f"Duplicate {key}: {value}")
        result[value] = row
    return result


def main() -> None:
    review = load_json(REVIEW_PATH)
    d4 = load_json(D4_PATH)
    matrix = load_json(MATRIX_PATH)

    require(review["schema_version"] == "0.1.0", "Unexpected review schema")
    require(review["phase"] == "Phase 15", "Unexpected phase")
    require(review["work_package"] == "WP15-D4R", "Unexpected work package")
    require(review["status"] == EXPECTED_STATUS, "Unexpected review status")
    require(
        review["review_class"] == EXPECTED_REVIEW_CLASS,
        "Unexpected review class",
    )

    target = review["review_target"]
    require(
        target["validated_checkpoint"] == "34d63a5",
        "Review target is not the locally validated D4 checkpoint",
    )
    require(
        target["candidate_contract"]
        == "experiments/configs/phase-15-family-descriptive-plan.json",
        "Unexpected D4 candidate path",
    )
    require(
        target["authoritative_comparability_matrix"]
        == "spec/phase-15-treatment-comparability-matrix.json",
        "Unexpected D2 matrix path",
    )

    scope = review["review_scope"]
    require(scope["eligible_family_ids"] == EXPECTED_FAMILIES, "Family order drift")
    require(scope["expected_family_count"] == 4, "Family count drift")
    require(scope["expected_member_row_count"] == 13, "Member count drift")
    require(scope["expected_analysis_unit_count"] == 12, "Unit count drift")
    require(scope["expected_cutoff_count"] == 4, "Cutoff count drift")

    blindness = review["outcome_blindness"]
    require(blindness["required"] is True, "Outcome blindness is not required")
    for field in (
        "projected_metric_values_read",
        "raw_execution_values_read",
        "family_outcome_values_read",
        "aggregate_results_read",
    ):
        require(blindness[field] is False, f"Outcome-blind field opened: {field}")

    prohibited_evidence = set(blindness["prohibited_evidence"])
    required_prohibitions = {
        "projected metric values",
        "raw execution values",
        "family outcome distributions",
        "success counts or percentages",
        "treatment rankings",
        "effect estimates",
        "confidence intervals",
        "hypothesis-test results",
    }
    require(
        prohibited_evidence == required_prohibitions,
        "Prohibited evidence registry drifted",
    )

    require(review["decision_options"] == EXPECTED_DECISIONS, "Decision options drift")
    decision = review["current_decision"]
    require(decision["decision"] == "PENDING", "Review decision is not pending")
    require(decision["decision_authorized"] is False, "Decision was implicitly authorized")
    require(decision["reviewer"] == "PENDING", "Reviewer was predeclared")
    require(decision["reviewed_commit"] == "PENDING", "Reviewed commit was prefilled")
    require(decision["decision_date_utc"] == "PENDING", "Decision date was prefilled")
    require(decision["rationale"] == "PENDING", "Rationale was prefilled")
    require(decision["conditions"] == [], "Decision conditions were prefilled")
    require(
        decision["superseded_candidate_preserved"] is True,
        "Superseded-candidate preservation disabled",
    )

    questions = review["review_questions"]
    require(len(questions) == 16, "Review question count drifted")
    require(
        [row["id"] for row in questions] == EXPECTED_QUESTION_IDS,
        "Review question identity or order drifted",
    )
    require(
        len({row["subject"] for row in questions}) == 16,
        "Review question subjects are not unique",
    )
    for row in questions:
        require(row["response"] == "PENDING", f"Question preanswered: {row['id']}")
        require(row["rationale"] == "PENDING", f"Question rationale prefilled: {row['id']}")
        require(bool(row["criterion"].strip()), f"Empty criterion: {row['id']}")

    prerequisites = review["decision_prerequisites"]
    require(prerequisites["required_question_count"] == 16, "Question gate drift")
    require(
        prerequisites["allowed_responses"]
        == ["PASS", "FAIL", "NEEDS_REVISION", "DEFER"],
        "Allowed responses drifted",
    )
    for field in (
        "accept_requires_all_questions_pass",
        "accept_requires_exact_reviewed_commit",
        "accept_requires_local_validation",
        "accept_requires_ci_validation",
        "accept_requires_explicit_decision_record",
    ):
        require(prerequisites[field] is True, f"Acceptance prerequisite disabled: {field}")
    require(
        prerequisites["implicit_acceptance"] == "NOT_PERMITTED",
        "Implicit acceptance was enabled",
    )

    require(review["freeze_state"] == EXPECTED_FREEZE_STATE, "Freeze state drifted")

    boundary = review["claim_boundary"]
    require(
        boundary["family_member_value_display"] == "NOT_YET_AUTHORIZED",
        "Member-value display gate opened",
    )
    require(
        boundary["family_specific_descriptive_comparison"]
        == "NOT_YET_AUTHORIZED",
        "Family comparison gate opened",
    )
    require(boundary["success_rate_denominator"] == "NOT_DEFINED", "Rate denominator defined")
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
        require(boundary[field] == "NOT_PERMITTED", f"Claim gate opened: {field}")

    require(d4["eligible_family_ids"] == EXPECTED_FAMILIES, "D4 family order drifted")
    require(d4["expected_family_count"] == 4, "D4 family count drifted")
    require(d4["expected_member_row_count"] == 13, "D4 member count drifted")
    require(d4["expected_analysis_unit_count"] == 12, "D4 unit count drifted")
    require(d4["freeze_candidate"] == EXPECTED_FREEZE_STATE, "D4 freeze state drifted")

    matrix_index = indexed(matrix["comparison_families"], "id")
    d4_index = indexed(d4["family_plans"], "family_id")
    require(list(d4_index) == EXPECTED_FAMILIES, "D4 family-plan order drifted")

    member_ids: List[str] = []
    unit_ids: List[str] = []
    cutoff_ids: List[str] = []
    for family_id in EXPECTED_FAMILIES:
        family = matrix_index[family_id]
        plan = d4_index[family_id]
        require(family["classification"] == "QUALIFIED_MATCH", f"Nonqualified family: {family_id}")
        require(
            plan["expected_allowed_fields"] == family["allowed_fields"],
            f"D2/D4 allowed-field drift: {family_id}",
        )
        cutoff_ids.append(plan["cutoff_id"])
        member_ids.extend(plan["expected_member_row_ids"])
        unit_ids.extend(plan["expected_analysis_unit_ids"])
        require(
            plan["observation_cutoff"].startswith("Stop "),
            f"Nonterminal cutoff wording: {family_id}",
        )

    require(len(member_ids) == 13, "D4 member registry count drifted")
    require(len(set(member_ids)) == 13, "D4 member registry is not unique")
    require(len(unit_ids) == 12, "D4 analysis-unit count drifted")
    require(len(set(unit_ids)) == 12, "D4 analysis-unit registry is not unique")
    require(len(cutoff_ids) == 4, "D4 cutoff count drifted")
    require(len(set(cutoff_ids)) == 4, "D4 cutoffs are not unique")

    cf02 = d4_index["CF-02"]
    require(
        cf02["expected_member_row_ids"][1:3]
        == ["CF-02:B1:B1-01", "CF-02:B1:B1-05"],
        "CF-02 B1 policy rows drifted",
    )
    require(
        cf02["expected_analysis_unit_ids"].count("CF-02:B1") == 1,
        "CF-02 B1 denominator unit drifted",
    )

    denominator = d4["denominator_policy"]
    require(denominator["member_rows_are_denominator_units"] is False, "Member rows became denominator units")
    require(
        denominator["family_denominator_state"] == "CANDIDATE_NOT_FROZEN",
        "D4 denominator was frozen",
    )
    require(denominator["success_rate_denominator"] == "NOT_DEFINED", "D4 rate denominator defined")
    require(denominator["cross_family_denominator"] == "NOT_PERMITTED", "Cross-family denominator enabled")
    require(denominator["aggregate_authorized"] is False, "D4 aggregate was authorized")

    print(
        "Phase 15 D4 freeze review valid: "
        "questions=16, families=4, member_rows=13, analysis_units=12, "
        "cutoffs=4, decision=PENDING, freeze=NOT_FROZEN, "
        f"status={EXPECTED_STATUS}."
    )


if __name__ == "__main__":
    main()
