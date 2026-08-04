#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from ttc_recovery.treatment_comparability import (
    ALLOWED_CLASSIFICATIONS,
    MATRIX_STATUS,
    catalog_member_key,
)


ROOT = Path(__file__).resolve().parents[2]
MATRIX_PATH = ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"
BASELINE_CATALOG_PATH = ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"
T1_CATALOG_PATH = ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json"
T1_EXPLICIT_TEST_PATH = ROOT / "tests" / "test_fault_metrics.py"


def fail(message: str) -> None:
    raise SystemExit(f"Phase 15 treatment-comparability validation failed: {message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    matrix = load_json(MATRIX_PATH)
    baseline_catalog = load_json(BASELINE_CATALOG_PATH)
    t1_catalog = load_json(T1_CATALOG_PATH)
    explicit_test_text = T1_EXPLICIT_TEST_PATH.read_text(encoding="utf-8")

    if matrix.get("status") != MATRIX_STATUS:
        fail("matrix status drifted")
    if matrix.get("work_package") != "WP15-D2":
        fail("work-package identifier drifted")
    if matrix["comparison_authorization"]["publication_evidence"] is not False:
        fail("matrix cannot be publication evidence")
    for key in (
        "pooled_cross_treatment_aggregation",
        "inferential_statistics",
        "treatment_superiority_claim",
    ):
        if matrix["comparison_authorization"][key] != "NOT_PERMITTED":
            fail(f"comparison authorization relaxed: {key}")

    definitions = set(matrix["classification_definitions"])
    if "FULL_MATCH" in definitions:
        fail("FULL_MATCH classification is not permitted")
    if not ALLOWED_CLASSIFICATIONS.issubset(definitions):
        fail("required family classifications are missing")

    families = matrix["comparison_families"]
    family_ids = [family["id"] for family in families]
    if family_ids != [f"CF-{number:02d}" for number in range(1, 9)]:
        fail("comparison-family identifiers or order drifted")
    if len(family_ids) != len(set(family_ids)):
        fail("comparison-family identifiers must be unique")

    categorical = set(matrix["metric_semantics"]["categorical_candidates"])
    conditional = set(matrix["metric_semantics"]["family_conditional_candidates"])
    prohibited = set(matrix["metric_semantics"]["not_cross_treatment_comparable"])
    permitted_fields = categorical | conditional
    if permitted_fields & prohibited:
        fail("metric appears in both permitted and prohibited sets")
    for required in (
        "recovery_duration_contacts",
        "total_transmissions",
        "retry_overhead",
        "alignment",
    ):
        if required not in prohibited:
            fail(f"required noncomparable metric missing: {required}")

    family_catalog_members: dict[str, str] = {}
    explicit_members = 0
    classification_counts = Counter()
    for family in families:
        classification = family["classification"]
        classification_counts[classification] += 1
        if classification not in ALLOWED_CLASSIFICATIONS:
            fail(f"unsupported classification: {classification}")
        treatments = {member["treatment"] for member in family["members"]}
        if len(treatments) < 2:
            fail(f"{family['id']} must contain at least two treatments")
        allowed = set(family["allowed_fields"])
        if not allowed.issubset(permitted_fields):
            fail(f"{family['id']} authorizes an undeclared field")
        if allowed & prohibited:
            fail(f"{family['id']} authorizes a prohibited field")
        if classification == "DIAGNOSTIC_FAMILY_ONLY" and allowed:
            fail(f"{family['id']} diagnostic family cannot authorize metrics")
        if classification == "QUALIFIED_MATCH" and not allowed:
            fail(f"{family['id']} qualified family must identify allowed fields")
        if not family.get("qualifiers"):
            fail(f"{family['id']} lacks qualifiers")

        for member in family["members"]:
            source_type = member["source_type"]
            if source_type == "CATALOG":
                key = catalog_member_key(member["treatment"], member["source_id"])
                if key in family_catalog_members:
                    fail(f"catalog scenario assigned to multiple families: {key}")
                family_catalog_members[key] = family["id"]
            elif source_type == "EXPLICIT_TEST":
                explicit_members += 1
                evidence = str(member.get("evidence", ""))
                if "::" not in evidence:
                    fail(f"explicit member lacks test evidence: {member['source_id']}")
                test_name = evidence.rsplit("::", 1)[1]
                if f"def {test_name}(" not in explicit_test_text:
                    fail(f"explicit test not found: {test_name}")
            else:
                fail(f"unsupported source type: {source_type}")

    expected_baseline = {
        catalog_member_key(str(row["baseline"]).split("-")[0], str(row["id"]))
        for row in baseline_catalog["tests"]
    }
    expected_t1 = {
        catalog_member_key("T1", str(row["id"])) for row in t1_catalog["tests"]
    }
    expected_catalog = expected_baseline | expected_t1

    dispositions = matrix["scenario_disposition"]
    disposition_keys = [
        catalog_member_key(str(row["treatment"]), str(row["scenario_id"]))
        for row in dispositions
    ]
    if len(disposition_keys) != len(set(disposition_keys)):
        fail("scenario disposition contains duplicates")
    if set(disposition_keys) != expected_catalog:
        missing = sorted(expected_catalog - set(disposition_keys))
        extra = sorted(set(disposition_keys) - expected_catalog)
        fail(f"scenario disposition coverage mismatch: missing={missing}, extra={extra}")

    family_ids_set = set(family_ids)
    for row in dispositions:
        key = catalog_member_key(str(row["treatment"]), str(row["scenario_id"]))
        disposition = row["disposition"]
        if disposition == "COMPARISON_FAMILY":
            family_id = row.get("family_id")
            if family_id not in family_ids_set:
                fail(f"unknown family in disposition: {key}")
            if family_catalog_members.get(key) != family_id:
                fail(f"family/disposition mismatch: {key}")
            if "reason" in row:
                fail(f"comparison-family disposition should not include reason: {key}")
        elif disposition in {"TREATMENT_SPECIFIC", "NON_OUTCOME_GUARD"}:
            if not row.get("reason"):
                fail(f"non-family disposition lacks reason: {key}")
            if key in family_catalog_members:
                fail(f"non-family scenario appears in family: {key}")
        else:
            fail(f"unsupported scenario disposition: {disposition}")

    family_disposition_keys = {
        key
        for key, family_id in family_catalog_members.items()
        if family_id in family_ids_set
    }
    disposition_family_keys = {
        catalog_member_key(str(row["treatment"]), str(row["scenario_id"]))
        for row in dispositions
        if row["disposition"] == "COMPARISON_FAMILY"
    }
    if family_disposition_keys != disposition_family_keys:
        fail("family catalog members and scenario dispositions differ")

    rules = " ".join(matrix["population_rules"])
    for phrase in (
        "Do not pool the 21 curated baseline catalog rows with the 12 seeded T1 pilot rows.",
        "Do not calculate treatment success percentages",
        "Any field not explicitly allowed by a family",
    ):
        if phrase not in rules:
            fail(f"population rule missing: {phrase}")

    blockers = matrix["remaining_blockers"]
    if len(blockers) < 5:
        fail("remaining blocker set is incomplete")
    if not any("executable matched-family population" in value for value in blockers):
        fail("executable matched-family population blocker is missing")

    if set(matrix["hard_claim_boundaries"].values()) != {"NOT_PERMITTED"}:
        fail("hard claim boundary was relaxed")

    print(
        "Phase 15 treatment comparability valid: "
        f"families={len(families)}, "
        f"qualified={classification_counts['QUALIFIED_MATCH']}, "
        f"diagnostic={classification_counts['DIAGNOSTIC_FAMILY_ONLY']}, "
        f"baseline_catalog={len(expected_baseline)}, "
        f"t1_catalog={len(expected_t1)}, "
        f"explicit_tests={explicit_members}, "
        f"status={matrix['status']}."
    )


if __name__ == "__main__":
    main()
