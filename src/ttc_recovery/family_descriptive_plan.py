from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence

from .matched_family_population import POPULATION_STATUS, RUN_CLASS
from .treatment_comparability import MATRIX_STATUS


PLAN_CONFIG_STATUS = (
    "PREDECLARED_FAMILY_ANALYSIS_PLAN_CANDIDATE_PENDING_VALIDATION_"
    "NOT_ANALYSIS_EVIDENCE"
)
PLAN_OUTPUT_STATUS = (
    "FAMILY_ANALYSIS_FREEZE_CANDIDATE_GENERATED_PENDING_VALIDATION_"
    "NOT_ANALYSIS_EVIDENCE"
)


def canonical_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _index_by_id(
    rows: Sequence[Mapping[str, object]],
    field: str = "id",
) -> Dict[str, Mapping[str, object]]:
    indexed: Dict[str, Mapping[str, object]] = {}
    for row in rows:
        identifier = str(row[field])
        if identifier in indexed:
            raise ValueError(f"Duplicate identifier for {field}: {identifier}")
        indexed[identifier] = row
    return indexed


def _closed_authorization(payload: Mapping[str, object]) -> None:
    authorization = payload["comparison_authorization"]
    if authorization["family_specific_descriptive_comparison"] != (
        "NOT_YET_AUTHORIZED"
    ):
        raise ValueError("D3 family comparison gate was relaxed")
    for field in (
        "pooled_cross_treatment_aggregation",
        "success_rate_or_percentage",
        "inferential_statistics",
        "treatment_superiority",
    ):
        if authorization[field] != "NOT_PERMITTED":
            raise ValueError(f"D3 authorization was relaxed: {field}")
    if authorization["publication_evidence"] is not False:
        raise ValueError("D3 payload cannot be publication evidence")


def _validate_config_boundaries(config: Mapping[str, object]) -> None:
    if config.get("status") != PLAN_CONFIG_STATUS:
        raise ValueError("Unexpected WP15-D4 configuration status")
    if config.get("run_class") != RUN_CLASS:
        raise ValueError("WP15-D4 must remain pilot-only")
    blindness = config["outcome_blindness"]
    if blindness["projected_metric_values_read"] is not False:
        raise ValueError("WP15-D4 cannot read projected metric values")
    if blindness["raw_execution_values_read"] is not False:
        raise ValueError("WP15-D4 cannot read raw execution values")
    denominator = config["denominator_policy"]
    if denominator["member_rows_are_denominator_units"] is not False:
        raise ValueError("Member rows cannot become denominator units")
    if denominator["success_rate_denominator"] != "NOT_DEFINED":
        raise ValueError("Success-rate denominator must remain undefined")
    if denominator["cross_family_denominator"] != "NOT_PERMITTED":
        raise ValueError("Cross-family denominator must remain prohibited")
    if denominator["aggregate_authorized"] is not False:
        raise ValueError("Aggregation cannot be authorized")
    boundary = config["claim_boundary"]
    if boundary["family_specific_descriptive_comparison"] != (
        "NOT_YET_AUTHORIZED"
    ):
        raise ValueError("Family comparison cannot be authorized by D4")
    if boundary["denominator_freeze"] != "CANDIDATE_NOT_FROZEN":
        raise ValueError("Denominator status must remain candidate-only")
    if boundary["observation_cutoff_freeze"] != "CANDIDATE_NOT_FROZEN":
        raise ValueError("Observation cutoff must remain candidate-only")
    for field in (
        "pooled_cross_treatment_aggregation",
        "success_rate_or_percentage",
        "inferential_statistics",
        "treatment_superiority",
        "causal_interpretation",
        "cryptographic_security_or_pcs",
        "publication_evidence",
    ):
        if boundary[field] != "NOT_PERMITTED":
            raise ValueError(f"WP15-D4 claim boundary was relaxed: {field}")


def build_family_descriptive_plan(
    config: Mapping[str, object],
    matrix: Mapping[str, object],
    population_config: Mapping[str, object],
    population_payload: Mapping[str, object],
) -> Dict[str, object]:
    """Build an outcome-blind WP15-D4 freeze candidate.

    The function intentionally uses only row identity, family membership,
    allowed-field names, analysis-unit identity, and source-execution digests.
    It never reads projected_metrics or source execution values.
    """

    _validate_config_boundaries(config)
    if matrix.get("status") != MATRIX_STATUS:
        raise ValueError("Unexpected D2 matrix status")
    if population_payload.get("status") != POPULATION_STATUS:
        raise ValueError("Unexpected D3 population status")
    if population_payload.get("run_class") != RUN_CLASS:
        raise ValueError("Unexpected D3 run class")
    _closed_authorization(population_payload)

    eligible_ids = list(config["eligible_family_ids"])
    if eligible_ids != list(population_config["eligible_family_ids"]):
        raise ValueError("D4 and D3 eligible-family order differs")
    if eligible_ids != list(population_payload["eligible_family_ids"]):
        raise ValueError("D4 and executed D3 family order differs")

    family_index = _index_by_id(matrix["comparison_families"])
    plan_index = _index_by_id(config["family_plans"], "family_id")
    rows_by_family: Dict[str, List[Mapping[str, object]]] = defaultdict(list)
    row_index: Dict[str, Mapping[str, object]] = {}

    for row in population_payload["rows"]:
        row_id = str(row["row_id"])
        if row_id in row_index:
            raise ValueError(f"Duplicate D3 row ID: {row_id}")
        row_index[row_id] = row
        rows_by_family[str(row["family_id"])].append(row)

    denominator_index = _index_by_id(
        population_payload["denominators"],
        "family_id",
    )

    member_registry: List[Dict[str, object]] = []
    analysis_unit_registry: List[Dict[str, object]] = []
    family_plan_records: List[Dict[str, object]] = []
    denominator_candidates: List[Dict[str, object]] = []

    for family_id in eligible_ids:
        family = family_index[family_id]
        plan = plan_index[family_id]
        if family["classification"] != "QUALIFIED_MATCH":
            raise ValueError(f"D4 family is not qualified: {family_id}")

        expected_allowed = list(plan["expected_allowed_fields"])
        if expected_allowed != list(family["allowed_fields"]):
            raise ValueError(f"Allowed-field order drifted for {family_id}")

        expected_row_ids = list(plan["expected_member_row_ids"])
        actual_rows = rows_by_family[family_id]
        actual_row_ids = [str(row["row_id"]) for row in actual_rows]
        if actual_row_ids != expected_row_ids:
            raise ValueError(
                f"Member registry drifted for {family_id}: "
                f"{actual_row_ids} != {expected_row_ids}"
            )

        expected_units = list(plan["expected_analysis_unit_ids"])
        actual_units: List[str] = []
        for row in actual_rows:
            unit = str(row["analysis_unit_id"])
            if unit not in actual_units:
                actual_units.append(unit)
        if actual_units != expected_units:
            raise ValueError(
                f"Analysis-unit registry drifted for {family_id}: "
                f"{actual_units} != {expected_units}"
            )

        for row in actual_rows:
            if row["family_classification"] != "QUALIFIED_MATCH":
                raise ValueError(f"Non-qualified row entered D4: {row['row_id']}")
            if list(row["allowed_fields"]) != expected_allowed:
                raise ValueError(f"Row allowed fields drifted: {row['row_id']}")
            digest = str(row["source_execution_sha256"])
            if len(digest) != 64:
                raise ValueError(f"Invalid execution digest: {row['row_id']}")
            member_registry.append(
                {
                    "row_id": row["row_id"],
                    "family_id": family_id,
                    "analysis_unit_id": row["analysis_unit_id"],
                    "treatment": row["treatment"],
                    "source_type": row["source_type"],
                    "source_id": row["source_id"],
                    "role": row["role"],
                    "allowed_fields": expected_allowed,
                    "source_execution_sha256": digest,
                    "denominator_unit": False,
                    "projected_metric_values_read": False,
                    "publication_evidence": False,
                }
            )

        members_by_unit: Dict[str, List[str]] = defaultdict(list)
        treatment_by_unit: Dict[str, str] = {}
        for row in actual_rows:
            unit = str(row["analysis_unit_id"])
            members_by_unit[unit].append(str(row["row_id"]))
            treatment_by_unit[unit] = str(row["treatment"])
        for unit in expected_units:
            analysis_unit_registry.append(
                {
                    "analysis_unit_id": unit,
                    "family_id": family_id,
                    "treatment": treatment_by_unit[unit],
                    "member_row_ids": members_by_unit[unit],
                    "member_row_count": len(members_by_unit[unit]),
                    "denominator_membership": "CANDIDATE_INCLUDED",
                    "denominator_state": "CANDIDATE_NOT_FROZEN",
                    "publication_evidence": False,
                }
            )

        d3_denominator = denominator_index[family_id]
        if d3_denominator["family_coverage_status"] != "COMPLETE":
            raise ValueError(f"Incomplete D3 family coverage: {family_id}")
        if d3_denominator["success_rate_denominator"] != "NOT_DEFINED":
            raise ValueError(f"D3 rate denominator was defined: {family_id}")
        if d3_denominator["aggregate_authorized"] is not False:
            raise ValueError(f"D3 aggregation was authorized: {family_id}")
        if int(d3_denominator["analysis_unit_count"]) != len(expected_units):
            raise ValueError(f"D3 denominator count drifted: {family_id}")

        policy_variant_count = len(expected_row_ids) - len(expected_units)
        denominator_candidates.append(
            {
                "family_id": family_id,
                "analysis_unit_ids": expected_units,
                "analysis_unit_count": len(expected_units),
                "member_row_count": len(expected_row_ids),
                "policy_variant_row_count": policy_variant_count,
                "denominator_unit": "TREATMENT_WITHIN_FAMILY",
                "denominator_state": "CANDIDATE_NOT_FROZEN",
                "missing_unit_behavior": "BLOCK_FAMILY_DISPLAY_DO_NOT_SHRINK",
                "extra_unit_behavior": "REJECT_DO_NOT_EXPAND",
                "success_rate_denominator": "NOT_DEFINED",
                "cross_family_denominator": "NOT_PERMITTED",
                "aggregate_authorized": False,
                "publication_evidence": False,
            }
        )

        family_plan_records.append(
            {
                "family_id": family_id,
                "family_name": family["name"],
                "family_classification": family["classification"],
                "cutoff_id": plan["cutoff_id"],
                "observation_cutoff": plan["observation_cutoff"],
                "member_row_ids": expected_row_ids,
                "analysis_unit_ids": expected_units,
                "allowed_fields": expected_allowed,
                "observation_cutoff_state": "CANDIDATE_NOT_FROZEN",
                "denominator_state": "CANDIDATE_NOT_FROZEN",
                "family_display_authorized": False,
                "publication_evidence": False,
            }
        )

    if len(family_plan_records) != int(config["expected_family_count"]):
        raise AssertionError("D4 family count drifted")
    if len(member_registry) != int(config["expected_member_row_count"]):
        raise AssertionError("D4 member-row count drifted")
    if len(analysis_unit_registry) != int(
        config["expected_analysis_unit_count"]
    ):
        raise AssertionError("D4 analysis-unit count drifted")

    identity_contract = {
        "family_plans": family_plan_records,
        "member_registry": member_registry,
        "analysis_unit_registry": analysis_unit_registry,
        "denominator_candidates": denominator_candidates,
    }

    return {
        "schema_version": "0.1.0",
        "phase": "Phase 15",
        "work_package": "WP15-D4",
        "status": PLAN_OUTPUT_STATUS,
        "run_class": RUN_CLASS,
        "publication_evidence": False,
        "source_status": {
            "comparability_matrix": matrix["status"],
            "matched_family_population": population_payload["status"],
            "plan_config": config["status"],
        },
        "outcome_blindness": {
            "projected_metric_values_read": False,
            "raw_execution_values_read": False,
            "outcome_dependent_branching": False,
        },
        "freeze_candidate": dict(config["freeze_candidate"]),
        "global_observation_rules": dict(config["global_observation_rules"]),
        "family_count": len(family_plan_records),
        "member_row_count": len(member_registry),
        "analysis_unit_count": len(analysis_unit_registry),
        "observation_cutoff_count": len(family_plan_records),
        "denominator_candidate_count": len(denominator_candidates),
        "identity_contract_sha256": canonical_sha256(identity_contract),
        "family_plans": family_plan_records,
        "member_registry": member_registry,
        "analysis_unit_registry": analysis_unit_registry,
        "denominator_candidates": denominator_candidates,
        "allowed_display_candidates": list(config["allowed_display_candidates"]),
        "prohibited_outputs": list(config["prohibited_outputs"]),
        "revision_policy": dict(config["revision_policy"]),
        "claim_boundary": dict(config["claim_boundary"]),
    }


def write_family_descriptive_plan(
    payload: Mapping[str, object],
    json_path: Path,
    member_csv_path: Path,
    analysis_unit_csv_path: Path,
    family_plan_csv_path: Path,
    manifest_path: Path,
) -> None:
    for path in (
        json_path,
        member_csv_path,
        analysis_unit_csv_path,
        family_plan_csv_path,
        manifest_path,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)

    json_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    member_fields = [
        "row_id",
        "family_id",
        "analysis_unit_id",
        "treatment",
        "source_type",
        "source_id",
        "role",
        "allowed_fields_json",
        "source_execution_sha256",
        "denominator_unit",
        "projected_metric_values_read",
        "publication_evidence",
    ]
    with member_csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=member_fields)
        writer.writeheader()
        for row in payload["member_registry"]:
            writer.writerow(
                {
                    **{
                        field: row[field]
                        for field in member_fields
                        if field in row
                    },
                    "allowed_fields_json": json.dumps(
                        row["allowed_fields"],
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                }
            )

    unit_fields = [
        "analysis_unit_id",
        "family_id",
        "treatment",
        "member_row_ids_json",
        "member_row_count",
        "denominator_membership",
        "denominator_state",
        "publication_evidence",
    ]
    with analysis_unit_csv_path.open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=unit_fields)
        writer.writeheader()
        for row in payload["analysis_unit_registry"]:
            writer.writerow(
                {
                    **{
                        field: row[field]
                        for field in unit_fields
                        if field in row
                    },
                    "member_row_ids_json": json.dumps(
                        row["member_row_ids"],
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                }
            )

    family_fields = [
        "family_id",
        "family_name",
        "family_classification",
        "cutoff_id",
        "observation_cutoff",
        "member_row_ids_json",
        "analysis_unit_ids_json",
        "allowed_fields_json",
        "observation_cutoff_state",
        "denominator_state",
        "family_display_authorized",
        "publication_evidence",
    ]
    with family_plan_csv_path.open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=family_fields)
        writer.writeheader()
        for row in payload["family_plans"]:
            writer.writerow(
                {
                    **{
                        field: row[field]
                        for field in family_fields
                        if field in row
                    },
                    "member_row_ids_json": json.dumps(
                        row["member_row_ids"],
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                    "analysis_unit_ids_json": json.dumps(
                        row["analysis_unit_ids"],
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                    "allowed_fields_json": json.dumps(
                        row["allowed_fields"],
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                }
            )

    base = manifest_path.parent
    data_paths = sorted(
        (
            json_path,
            member_csv_path,
            analysis_unit_csv_path,
            family_plan_csv_path,
        ),
        key=lambda value: value.name,
    )
    manifest_path.write_text(
        "\n".join(
            f"{sha256_file(path)}  {path.relative_to(base).as_posix()}"
            for path in data_paths
        )
        + "\n",
        encoding="utf-8",
    )


def verify_family_descriptive_manifest(
    base: Path,
    manifest_path: Path,
) -> None:
    expected_names = {
        "phase-15-family-descriptive-plan-candidate.json",
        "phase-15-family-member-registry.csv",
        "phase-15-family-analysis-units.csv",
        "phase-15-family-observation-plans.csv",
    }
    seen: set[str] = set()
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        path = base / relative
        if not path.is_file():
            raise RuntimeError(f"D4 manifest path is missing: {relative}")
        if path.name in seen:
            raise RuntimeError(f"Duplicate D4 manifest path: {relative}")
        seen.add(path.name)
        if sha256_file(path) != expected:
            raise RuntimeError(f"D4 checksum mismatch: {relative}")
    if seen != expected_names:
        raise RuntimeError(
            f"D4 manifest coverage mismatch: {sorted(seen)} != "
            f"{sorted(expected_names)}"
        )
