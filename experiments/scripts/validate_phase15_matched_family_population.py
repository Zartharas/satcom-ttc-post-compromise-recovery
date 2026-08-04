#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from ttc_recovery.matched_family_population import (
    POPULATION_STATUS,
    execute_matched_family_population,
)


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = (
    ROOT / "experiments" / "configs" / "phase-15-matched-family-population.json"
)
MATRIX_PATH = ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"
BASELINE_CATALOG_PATH = ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"
T1_CATALOG_PATH = ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json"
MODULE_PATH = ROOT / "src" / "ttc_recovery" / "matched_family_population.py"
RUNNER_PATH = ROOT / "experiments" / "scripts" / "run_phase15_matched_family_population.py"
DOC_PATH = ROOT / "docs" / "phase-15-matched-family-population.md"
TEST_PATH = ROOT / "tests" / "test_phase15_matched_family_population.py"

EXPECTED_CONFIG_STATUS = (
    "EXECUTABLE_POPULATION_CANDIDATE_NOT_COMPARATIVE_EVIDENCE"
)
EXPECTED_FAMILIES = ["CF-01", "CF-02", "CF-05", "CF-06"]
EXPECTED_T1_RECIPES = {"T1-01", "T1-09", "T1-13", "T1-15"}


def fail(message: str) -> None:
    raise SystemExit(f"WP15-D3 validation failed: {message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")


def main() -> None:
    for path in (
        CONFIG_PATH,
        MATRIX_PATH,
        BASELINE_CATALOG_PATH,
        T1_CATALOG_PATH,
        MODULE_PATH,
        RUNNER_PATH,
        DOC_PATH,
        TEST_PATH,
    ):
        require_file(path)

    config = load_json(CONFIG_PATH)
    matrix = load_json(MATRIX_PATH)
    baseline_catalog = load_json(BASELINE_CATALOG_PATH)
    t1_catalog = load_json(T1_CATALOG_PATH)

    if config.get("status") != EXPECTED_CONFIG_STATUS:
        fail("configuration status drifted")
    if config.get("run_class") != "PILOT_INTERNAL_VALIDATION_ONLY":
        fail("run class must remain pilot-only")
    if config.get("eligible_family_ids") != EXPECTED_FAMILIES:
        fail("eligible family order or population drifted")
    if int(config.get("expected_family_count", -1)) != 4:
        fail("expected family count drifted")
    if int(config.get("expected_member_row_count", -1)) != 13:
        fail("expected member-row count drifted")
    if int(config.get("expected_analysis_unit_count", -1)) != 12:
        fail("expected analysis-unit count drifted")

    if set(config.get("t1_execution_recipes", {})) != EXPECTED_T1_RECIPES:
        fail("T1 execution recipe population drifted")
    for source_id, recipe in config["t1_execution_recipes"].items():
        if recipe.get("executor") != "run_bounded_recovery":
            fail(f"unsupported T1 executor for {source_id}")
        if recipe.get("seed_is_comparable") is not False:
            fail(f"T1 provenance seed became comparable for {source_id}")
        if not isinstance(recipe.get("provenance_seed"), int):
            fail(f"missing integer provenance seed for {source_id}")

    denominator = config["denominator_policy"]
    if denominator.get("success_rate_denominator") != "NOT_DEFINED":
        fail("success-rate denominator must remain undefined")
    if denominator.get("cross_family_denominator") != "NOT_PERMITTED":
        fail("cross-family denominator must remain prohibited")
    if denominator.get("aggregate_authorized") is not False:
        fail("aggregate authorization must remain false")

    if set(config["claim_boundary"].values()) != {
        "NOT_YET_AUTHORIZED",
        "NOT_PERMITTED",
    }:
        fail("claim boundary was relaxed")

    family_index = {
        row["id"]: row for row in matrix["comparison_families"]
    }
    for family_id in EXPECTED_FAMILIES:
        family = family_index.get(family_id)
        if family is None:
            fail(f"matrix family missing: {family_id}")
        if family.get("classification") != "QUALIFIED_MATCH":
            fail(f"non-qualified family admitted: {family_id}")
        if not family.get("allowed_fields"):
            fail(f"qualified family has no allowed fields: {family_id}")
        if set(family["allowed_fields"]) & set(family["blocked_fields"]):
            fail(f"allowed and blocked fields overlap: {family_id}")

    diagnostic_ids = {
        row["id"]
        for row in matrix["comparison_families"]
        if row["classification"] == "DIAGNOSTIC_FAMILY_ONLY"
    }
    if diagnostic_ids & set(EXPECTED_FAMILIES):
        fail("diagnostic family admitted to executable population")

    payload = execute_matched_family_population(
        config,
        matrix,
        baseline_catalog,
        t1_catalog,
    )
    if payload.get("status") != POPULATION_STATUS:
        fail("runtime payload status drifted")
    if payload.get("publication_evidence") is not False:
        fail("runtime payload became publication evidence")
    if payload.get("family_count") != 4:
        fail("runtime family count drifted")
    if payload.get("member_row_count") != 13:
        fail("runtime member-row count drifted")
    if payload.get("analysis_unit_count") != 12:
        fail("runtime analysis-unit count drifted")

    row_ids = [row["row_id"] for row in payload["rows"]]
    if len(row_ids) != len(set(row_ids)):
        fail("runtime row identifiers are not unique")
    if any(row["publication_evidence"] for row in payload["rows"]):
        fail("member row became publication evidence")

    expected_members = {
        (
            family["id"],
            member["treatment"],
            member["source_id"],
        )
        for family in matrix["comparison_families"]
        if family["id"] in EXPECTED_FAMILIES
        for member in family["members"]
    }
    actual_members = {
        (row["family_id"], row["treatment"], row["source_id"])
        for row in payload["rows"]
    }
    if actual_members != expected_members:
        fail("runtime member population does not match qualified matrix members")

    for row in payload["rows"]:
        family = family_index[row["family_id"]]
        if set(row["projected_metrics"]) != set(family["allowed_fields"]):
            fail(f"projection field mismatch for {row['row_id']}")
        if "alignment" in row["projected_metrics"]:
            fail(f"raw alignment leaked into projection for {row['row_id']}")
        if row["source_execution_sha256"] is None or len(
            row["source_execution_sha256"]
        ) != 64:
            fail(f"invalid source execution digest for {row['row_id']}")

    denominator_index = {
        row["family_id"]: row for row in payload["denominators"]
    }
    cf02 = denominator_index["CF-02"]
    if cf02["member_row_count"] != 5:
        fail("CF-02 must retain five member rows")
    if cf02["analysis_unit_count"] != 4:
        fail("CF-02 B1 variants must share one analysis unit")
    if cf02["policy_variant_row_count"] != 1:
        fail("CF-02 policy-variant count drifted")

    for row in payload["denominators"]:
        if row["aggregate_authorized"] is not False:
            fail(f"aggregate authorization relaxed for {row['family_id']}")
        if row["success_rate_denominator"] != "NOT_DEFINED":
            fail(f"success-rate denominator defined for {row['family_id']}")
        if row["family_coverage_status"] != "COMPLETE":
            fail(f"incomplete family coverage for {row['family_id']}")

    authorization = payload["comparison_authorization"]
    if authorization["family_specific_descriptive_comparison"] != (
        "NOT_YET_AUTHORIZED"
    ):
        fail("family comparison was prematurely authorized")
    if authorization["pooled_cross_treatment_aggregation"] != (
        "NOT_PERMITTED"
    ):
        fail("pooled aggregation was permitted")
    if authorization["success_rate_or_percentage"] != "NOT_PERMITTED":
        fail("success-rate output was permitted")
    if authorization["publication_evidence"] is not False:
        fail("publication evidence flag changed")

    outcome_counts = Counter(
        row["projected_metrics"].get("outcome")
        for row in payload["rows"]
        if "outcome" in row["projected_metrics"]
    )
    print(
        "Phase 15 matched-family population valid: "
        f"families={payload['family_count']}, "
        f"member_rows={payload['member_row_count']}, "
        f"analysis_units={payload['analysis_unit_count']}, "
        f"outcome_categories={len(outcome_counts)}, "
        f"status={payload['status']}."
    )


if __name__ == "__main__":
    main()
