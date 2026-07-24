#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "phase-14-independent-review-package.json"
CLAIMS_CSV = ROOT / "governance" / "phase-14-claims-traceability.csv"
EVIDENCE_CSV = ROOT / "governance" / "phase-14-evidence-index.csv"
RESPONSE_TEMPLATE = ROOT / "governance" / "phase-14-reviewer-response-template.md"

EXPECTED_STATUS = "READY_FOR_OUTREACH_NOT_REVIEWED"
EXPECTED_SOURCE_COMMIT = "fee83236c12f19226a1b0de404a965cc8fbba005"
EXPECTED_CLAIM_COUNT = 20
EXPECTED_QUESTION_COUNT = 24
EXPECTED_ORACLE_COUNT = 21
EXPECTED_EVIDENCE_COUNT = 21

ALLOWED_CLAIM_STATUSES = {
    "PENDING_INDEPENDENT_REVIEW",
    "PERMITTED_WITH_QUALIFIER",
    "DIAGNOSTIC_ONLY",
    "NOT_PERMITTED",
    "GOVERNANCE_EXCEPTION_REQUIRES_REVIEW",
}


def fail(message: str) -> None:
    raise SystemExit(f"Phase 14 validation failed: {message}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def require_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        fail(f"{label} must be unique.")


def main() -> None:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))

    if spec["status"] != EXPECTED_STATUS:
        fail("package status must remain ready for outreach and not reviewed.")
    if spec["source_base"]["commit"] != EXPECTED_SOURCE_COMMIT:
        fail("Phase 13 source-base commit drifted.")
    if spec["source_base"]["baseline_review_status"] != "PENDING_INDEPENDENT_REVIEW":
        fail("baseline review gate must remain pending.")
    if spec["review_issue"]["number"] != 3 or spec["review_issue"]["status"] != "OPEN":
        fail("issue #3 must remain the open review tracker.")
    if spec["review_issue"]["completion_boxes_must_remain_unchecked_until_evidence_exists"] is not True:
        fail("review issue completion boxes must remain evidence-gated.")

    questions = [
        question
        for group in spec["question_groups"]
        for question in group["questions"]
    ]
    question_ids = [row["id"] for row in questions]
    if len(questions) != EXPECTED_QUESTION_COUNT:
        fail("required review-question count drifted.")
    require_unique(question_ids, "review question IDs")
    if "B1-R5" not in question_ids:
        fail("the omitted Phase 05 endpoint-knowledge question must be restored.")

    oracle_ids = spec["scenario_oracle_review"]["oracle_ids"]
    if len(oracle_ids) != EXPECTED_ORACLE_COUNT:
        fail("scenario-oracle count drifted.")
    require_unique(oracle_ids, "oracle IDs")
    if spec["scenario_oracle_review"]["status"] != "PENDING":
        fail("scenario-oracle review must remain pending.")

    claims = spec["claims"]
    claim_ids = [row["id"] for row in claims]
    if len(claims) != EXPECTED_CLAIM_COUNT:
        fail("claim count drifted.")
    require_unique(claim_ids, "claim IDs")
    if {row["status"] for row in claims} - ALLOWED_CLAIM_STATUSES:
        fail("claims contain an unsupported status.")

    valid_review_ids = set(question_ids) | {"O-ALL"}
    for claim in claims:
        if not claim["evidence_paths"]:
            fail(f"{claim['id']} has no evidence path.")
        if not set(claim["review_question_ids"]).issubset(valid_review_ids):
            fail(f"{claim['id']} references an unknown review question.")
        for relative in claim["evidence_paths"]:
            if not (ROOT / relative).is_file():
                fail(f"{claim['id']} references missing evidence: {relative}")

    evidence = spec["evidence_index"]
    evidence_ids = [row["id"] for row in evidence]
    if len(evidence) != EXPECTED_EVIDENCE_COUNT:
        fail("evidence-index count drifted.")
    require_unique(evidence_ids, "evidence IDs")
    for row in evidence:
        if not (ROOT / row["path"]).is_file():
            fail(f"evidence index references missing path: {row['path']}")

    findings = spec["governance_findings"]
    if len(findings) != 4:
        fail("governance-finding count drifted.")
    if {row["status"] for row in findings} != {"OPEN_REQUIRES_REVIEW"}:
        fail("all governance findings must remain open.")

    gate_text = (ROOT / "governance" / "phase-04-independent-review-gate.md").read_text(
        encoding="utf-8"
    )
    old_template = (
        ROOT / "governance" / "phase-05-reviewer-response-template.md"
    ).read_text(encoding="utf-8")
    if "Does any B1 test rely on information unavailable" not in gate_text:
        fail("Phase 04 endpoint-knowledge question is missing.")
    if "B1-R5" in old_template:
        fail("historical Phase 05 template unexpectedly changed; Phase 14 should document the gap.")

    oracle_candidate = json.loads(
        (ROOT / "spec" / "baseline-oracle-freeze-candidate.json").read_text(
            encoding="utf-8"
        )
    )
    if oracle_candidate["status"] != "PENDING_INDEPENDENT_REVIEW":
        fail("oracle candidate must remain pending.")
    review = oracle_candidate["review"]
    if review["reviewer_name"] is not None or review["approved_commit"] is not None:
        fail("oracle candidate contains unsupported reviewer approval.")
    if review["decision"] != "PENDING" or review["manifest_verified"] is not False:
        fail("oracle candidate review record must remain incomplete.")

    phase13 = json.loads(
        (ROOT / "spec" / "phase-13-abstraction-gap-outcomes.json").read_text(
            encoding="utf-8"
        )
    )
    if phase13["baseline_review_status"] != "PENDING_INDEPENDENT_REVIEW":
        fail("Phase 13 baseline review status drifted.")
    for key in (
        "formal_model_completeness_claim",
        "implementation_equivalence_claim",
        "cryptographic_security_claim",
        "publication_evidence_status",
    ):
        if phase13[key] != "NOT_PERMITTED":
            fail(f"Phase 13 boundary drifted: {key}")

    if set(spec["claim_boundaries"].values()) != {"NOT_PERMITTED"}:
        fail("all Phase 14 hard claim boundaries must remain NOT_PERMITTED.")

    required_outputs = spec["required_outputs"]
    for relative in required_outputs:
        if not (ROOT / relative).is_file():
            fail(f"missing required Phase 14 output: {relative}")

    claims_csv = read_csv(CLAIMS_CSV)
    if [row["id"] for row in claims_csv] != claim_ids:
        fail("claims CSV does not match JSON claim order.")
    for json_row, csv_row in zip(claims, claims_csv):
        for key in ("id", "category", "status", "permitted_wording",
                    "required_qualifier", "prohibited_overstatement"):
            if str(json_row[key]) != csv_row[key]:
                fail(f"claims CSV mismatch for {json_row['id']} field {key}")
        if ";".join(json_row["evidence_paths"]) != csv_row["evidence_paths"]:
            fail(f"claims CSV evidence mismatch for {json_row['id']}")
        if ";".join(json_row["review_question_ids"]) != csv_row["review_question_ids"]:
            fail(f"claims CSV question mismatch for {json_row['id']}")

    evidence_csv = read_csv(EVIDENCE_CSV)
    if [row["id"] for row in evidence_csv] != evidence_ids:
        fail("evidence CSV does not match JSON evidence order.")
    for json_row, csv_row in zip(evidence, evidence_csv):
        for key in ("id", "scope", "path", "role", "reviewer_action"):
            if str(json_row[key]) != csv_row[key]:
                fail(f"evidence CSV mismatch for {json_row['id']} field {key}")
        if csv_row["pin_method"] != "REVIEW_TARGET_COMMIT":
            fail("evidence must be pinned by exact review-target commit.")

    response_text = RESPONSE_TEMPLATE.read_text(encoding="utf-8")
    for identifier in question_ids + oracle_ids:
        if identifier not in response_text:
            fail(f"response template is missing {identifier}")

    print(
        "Phase 14 independent-review package valid: "
        f"questions={len(questions)}, oracles={len(oracle_ids)}, "
        f"claims={len(claims)}, evidence={len(evidence)}, "
        f"governance_findings={len(findings)}, status={spec['status']}."
    )


if __name__ == "__main__":
    main()
