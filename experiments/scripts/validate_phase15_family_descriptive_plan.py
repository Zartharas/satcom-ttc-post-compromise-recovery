#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path
from typing import Mapping

from ttc_recovery.family_descriptive_plan import (
    PLAN_CONFIG_STATUS,
    PLAN_OUTPUT_STATUS,
    build_family_descriptive_plan,
    verify_family_descriptive_manifest,
    write_family_descriptive_plan,
)
from ttc_recovery.matched_family_population import (
    execute_matched_family_population,
)


ROOT = Path(__file__).resolve().parents[2]
PLAN_PATH = (
    ROOT / "experiments" / "configs" / "phase-15-family-descriptive-plan.json"
)
MATRIX_PATH = ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"
POPULATION_CONFIG_PATH = (
    ROOT / "experiments" / "configs" / "phase-15-matched-family-population.json"
)
BASELINE_CATALOG_PATH = ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"
T1_CATALOG_PATH = ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json"


def fail(message: str) -> None:
    raise SystemExit(f"Phase 15 family-plan validation failed: {message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, Mapping):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(walk_keys(child))
    return keys


def main() -> None:
    plan = load_json(PLAN_PATH)
    matrix = load_json(MATRIX_PATH)
    population_config = load_json(POPULATION_CONFIG_PATH)
    baseline_catalog = load_json(BASELINE_CATALOG_PATH)
    t1_catalog = load_json(T1_CATALOG_PATH)

    if plan.get("work_package") != "WP15-D4":
        fail("work-package identifier drifted")
    if plan.get("status") != PLAN_CONFIG_STATUS:
        fail("plan status drifted")
    if plan.get("eligible_family_ids") != ["CF-01", "CF-02", "CF-05", "CF-06"]:
        fail("eligible-family order drifted")
    if plan.get("expected_family_count") != 4:
        fail("expected family count drifted")
    if plan.get("expected_member_row_count") != 13:
        fail("expected member-row count drifted")
    if plan.get("expected_analysis_unit_count") != 12:
        fail("expected analysis-unit count drifted")

    if plan["outcome_blindness"]["projected_metric_values_read"] is not False:
        fail("projected metric values cannot be read")
    if plan["outcome_blindness"]["raw_execution_values_read"] is not False:
        fail("raw execution values cannot be read")

    family_plans = plan["family_plans"]
    if [row["family_id"] for row in family_plans] != plan["eligible_family_ids"]:
        fail("family-plan order drifted")
    cutoff_ids = [row["cutoff_id"] for row in family_plans]
    if len(cutoff_ids) != len(set(cutoff_ids)):
        fail("cutoff identifiers must be unique")
    if not all(str(row["observation_cutoff"]).startswith("Stop ") for row in family_plans):
        fail("every family must define an explicit stop rule")

    member_ids = [
        member_id
        for family in family_plans
        for member_id in family["expected_member_row_ids"]
    ]
    unit_ids = [
        unit_id
        for family in family_plans
        for unit_id in family["expected_analysis_unit_ids"]
    ]
    if len(member_ids) != 13 or len(set(member_ids)) != 13:
        fail("member registry must contain 13 unique rows")
    if len(unit_ids) != 12 or len(set(unit_ids)) != 12:
        fail("analysis-unit registry must contain 12 unique units")
    if family_plans[1]["expected_member_row_ids"].count("CF-02:B1:B1-01") != 1:
        fail("CF-02 B1 local-completion variant is missing")
    if family_plans[1]["expected_member_row_ids"].count("CF-02:B1:B1-05") != 1:
        fail("CF-02 B1 status-gated variant is missing")
    if family_plans[1]["expected_analysis_unit_ids"].count("CF-02:B1") != 1:
        fail("CF-02 B1 variants must share one analysis unit")

    denominator = plan["denominator_policy"]
    if denominator["member_rows_are_denominator_units"] is not False:
        fail("member rows cannot be denominator units")
    if denominator["success_rate_denominator"] != "NOT_DEFINED":
        fail("success-rate denominator must remain undefined")
    if denominator["cross_family_denominator"] != "NOT_PERMITTED":
        fail("cross-family denominator must remain prohibited")
    if denominator["aggregate_authorized"] is not False:
        fail("aggregate authorization must remain false")

    forbidden_outputs = {
        "outcome frequency table",
        "success count or success percentage",
        "treatment-level rate",
        "pooled family score",
        "cross-family aggregate",
        "confidence interval",
        "hypothesis test",
        "effect estimate",
        "treatment ranking",
        "superiority or effectiveness conclusion",
    }
    if set(plan["prohibited_outputs"]) != forbidden_outputs:
        fail("prohibited-output registry drifted")

    boundary = plan["claim_boundary"]
    if boundary["family_specific_descriptive_comparison"] != "NOT_YET_AUTHORIZED":
        fail("family comparison gate was opened")
    if boundary["denominator_freeze"] != "CANDIDATE_NOT_FROZEN":
        fail("denominator was improperly frozen")
    if boundary["observation_cutoff_freeze"] != "CANDIDATE_NOT_FROZEN":
        fail("observation cutoff was improperly frozen")
    for key in (
        "pooled_cross_treatment_aggregation",
        "success_rate_or_percentage",
        "inferential_statistics",
        "treatment_superiority",
        "causal_interpretation",
        "cryptographic_security_or_pcs",
        "publication_evidence",
    ):
        if boundary[key] != "NOT_PERMITTED":
            fail(f"claim boundary was relaxed: {key}")

    population_payload = execute_matched_family_population(
        population_config,
        matrix,
        baseline_catalog,
        t1_catalog,
    )
    payload = build_family_descriptive_plan(
        plan,
        matrix,
        population_config,
        population_payload,
    )

    if payload["status"] != PLAN_OUTPUT_STATUS:
        fail("generated status drifted")
    if payload["family_count"] != 4:
        fail("generated family count drifted")
    if payload["member_row_count"] != 13:
        fail("generated member count drifted")
    if payload["analysis_unit_count"] != 12:
        fail("generated unit count drifted")
    if payload["observation_cutoff_count"] != 4:
        fail("generated cutoff count drifted")
    if payload["denominator_candidate_count"] != 4:
        fail("generated denominator count drifted")
    if payload["publication_evidence"] is not False:
        fail("generated plan cannot be publication evidence")
    if len(payload["identity_contract_sha256"]) != 64:
        fail("identity-contract digest is invalid")

    generated_keys = walk_keys(payload)
    for forbidden_key in (
        "projected_metrics",
        "raw_metrics",
        "outcome_counts",
        "success_count",
        "success_rate",
        "percentage",
        "p_value",
        "confidence_interval",
        "effect_size",
        "ranking",
    ):
        if forbidden_key in generated_keys:
            fail(f"forbidden analysis key emitted: {forbidden_key}")

    if any(row["projected_metric_values_read"] is not False for row in payload["member_registry"]):
        fail("member registry claims metric values were read")
    if any(row["denominator_unit"] is not False for row in payload["member_registry"]):
        fail("member row became a denominator unit")
    if any(row["family_display_authorized"] is not False for row in payload["family_plans"]):
        fail("family display was authorized")
    for row in payload["denominator_candidates"]:
        if row["denominator_state"] != "CANDIDATE_NOT_FROZEN":
            fail("denominator state drifted")
        if row["success_rate_denominator"] != "NOT_DEFINED":
            fail("generated success-rate denominator was defined")
        if row["aggregate_authorized"] is not False:
            fail("generated aggregate was authorized")

    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary)
        json_path = output / "phase-15-family-descriptive-plan-candidate.json"
        member_csv = output / "phase-15-family-member-registry.csv"
        unit_csv = output / "phase-15-family-analysis-units.csv"
        family_csv = output / "phase-15-family-observation-plans.csv"
        manifest = output / "phase-15-family-descriptive-plan.sha256"
        write_family_descriptive_plan(
            payload,
            json_path,
            member_csv,
            unit_csv,
            family_csv,
            manifest,
        )
        verify_family_descriptive_manifest(output, manifest)

        with member_csv.open("r", encoding="utf-8", newline="") as handle:
            member_rows = list(csv.DictReader(handle))
        with unit_csv.open("r", encoding="utf-8", newline="") as handle:
            unit_rows = list(csv.DictReader(handle))
        with family_csv.open("r", encoding="utf-8", newline="") as handle:
            family_rows = list(csv.DictReader(handle))
        if len(member_rows) != 13 or len(unit_rows) != 12 or len(family_rows) != 4:
            fail("generated CSV row counts drifted")
        if "projected_metrics_json" in member_rows[0]:
            fail("member registry exposed projected metric values")
        if "outcome" in member_rows[0]:
            fail("member registry exposed an outcome column")

    print(
        "Phase 15 family descriptive plan valid: "
        "families=4, member_rows=13, analysis_units=12, "
        "cutoffs=4, denominator_candidates=4, "
        f"status={payload['status']}."
    )


if __name__ == "__main__":
    main()
