from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from .baseline_metrics import run_baseline_scenario
from .simulator import Outcome
from .t1_controller import T1Session, run_bounded_recovery
from .treatment_comparability import project_allowed_metrics


POPULATION_STATUS = (
    "EXECUTABLE_POPULATION_IMPLEMENTED_PENDING_VALIDATION_"
    "NOT_COMPARATIVE_EVIDENCE"
)
RUN_CLASS = "PILOT_INTERNAL_VALIDATION_ONLY"


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


def _active_key_compromised(session: T1Session) -> bool:
    return any(
        endpoint.active_key in endpoint.compromised_keys
        for endpoint in (session.ground, session.spacecraft)
    ) or bool(session.authority.compromised)


def _security_state(session: T1Session) -> str:
    if _active_key_compromised(session):
        return "UNSAFE"
    if session.verification_complete:
        return "SECURE_PROVISIONAL"
    return "NOT_ESTABLISHED"


def _availability_state(session: T1Session) -> str:
    outcome = session.outcome()
    if outcome == Outcome.SUCCESS:
        return "AVAILABLE"
    if outcome in {
        Outcome.INDETERMINATE,
        Outcome.SECURE_DEGRADED,
        Outcome.AVAILABLE_UNSAFE,
    }:
        return "DEGRADED"
    return "UNAVAILABLE"


def _rejection_counts(
    event_log: Iterable[Mapping[str, object]],
) -> Dict[str, int]:
    rejection_count = 0
    replay_rejection_count = 0
    stale_state_rejection_count = 0
    for event in event_log:
        if event.get("event") != "t1_message_rejected":
            continue
        rejection_count += 1
        reason = str(event.get("reason", ""))
        if "duplicate message identifier" in reason:
            replay_rejection_count += 1
        if any(
            marker in reason
            for marker in (
                "non-monotonic",
                "no exact pending candidate",
                "conflicts with activation receipt",
                "binding mismatch",
                "bounded pending capacity or binding conflict",
            )
        ):
            stale_state_rejection_count += 1
    return {
        "rejection_count": rejection_count,
        "replay_rejection_count": replay_rejection_count,
        "stale_state_rejection_count": stale_state_rejection_count,
    }


def _fault_count(
    recipe: Mapping[str, object],
    kind: str,
) -> int:
    total = 0
    for row in recipe.get("injected_faults", []):
        if str(row.get("kind")) == kind:
            total += int(row.get("count", 0))
    return total


def _execute_t1_recipe(
    source_id: str,
    recipe: Mapping[str, object],
    catalog_entry: Mapping[str, object],
) -> Tuple[Dict[str, object], Dict[str, object]]:
    if recipe.get("executor") != "run_bounded_recovery":
        raise ValueError(f"Unsupported T1 executor for {source_id}")

    parameters = dict(recipe.get("parameters", {}))
    session = run_bounded_recovery(**parameters)
    post_action = str(recipe.get("post_action", "NONE"))
    if post_action == "REPLAY_LAST_COMMIT_AFTER_SUCCESS":
        if session.outcome() != Outcome.SUCCESS or session.last_commit is None:
            raise AssertionError(
                f"{source_id} requires a successful recovery and retained commit"
            )
        before = (
            session.spacecraft.epoch,
            session.spacecraft.active_key,
        )
        replay_result = session.spacecraft_accept_commit(session.last_commit)
        after = (
            session.spacecraft.epoch,
            session.spacecraft.active_key,
        )
        if replay_result is not None or before != after:
            raise AssertionError(f"{source_id} replay changed spacecraft state")
    elif post_action != "NONE":
        raise ValueError(f"Unsupported T1 post action for {source_id}: {post_action}")

    actual_alignment = session.alignment_state()
    actual_outcome = session.outcome().value
    if actual_alignment != str(catalog_entry["expected_alignment"]):
        raise AssertionError(
            f"{source_id} alignment mismatch: {actual_alignment} != "
            f"{catalog_entry['expected_alignment']}"
        )
    if actual_outcome != str(catalog_entry["expected_outcome"]):
        raise AssertionError(
            f"{source_id} outcome mismatch: {actual_outcome} != "
            f"{catalog_entry['expected_outcome']}"
        )

    counts = _rejection_counts(session.event_log)
    raw_metrics: Dict[str, object] = {
        "seed": int(recipe["provenance_seed"]),
        "alignment": actual_alignment,
        "outcome": actual_outcome,
        "security_state": _security_state(session),
        "availability_state": _availability_state(session),
        "verification_complete": bool(session.verification_complete),
        "active_key_compromised": _active_key_compromised(session),
        "command_accepted": any(
            event.get("event") == "t1_test_command_accepted"
            for event in session.event_log
        ),
        "telemetry_complete": any(
            event.get("event") == "t1_recovery_verified"
            for event in session.event_log
        ),
        "fault_count": sum(
            int(row.get("count", 0))
            for row in recipe.get("injected_faults", [])
        ),
        "drop_count": _fault_count(recipe, "DROP"),
        "reorder_count": _fault_count(recipe, "REORDER"),
        "replay_count": _fault_count(recipe, "STALE_REPLAY"),
        "rejection_count": counts["rejection_count"],
        "replay_rejection_count": counts["replay_rejection_count"],
        "stale_state_rejection_count": counts[
            "stale_state_rejection_count"
        ],
    }
    execution = {
        "treatment": "T1",
        "source_id": source_id,
        "executor": recipe["executor"],
        "parameters": parameters,
        "post_action": post_action,
        "injected_faults": list(recipe.get("injected_faults", [])),
        "provenance_seed": recipe["provenance_seed"],
        "seed_is_comparable": False,
        "catalog_oracle": {
            "expected_alignment": catalog_entry["expected_alignment"],
            "expected_outcome": catalog_entry["expected_outcome"],
            "status": "MATCHED_INTERNAL_DESIGN_ORACLE",
        },
        "raw_metrics": raw_metrics,
        "event_log": list(session.event_log),
        "publication_evidence": False,
    }
    return raw_metrics, execution


def _index_by_id(
    rows: Sequence[Mapping[str, object]],
) -> Dict[str, Mapping[str, object]]:
    indexed: Dict[str, Mapping[str, object]] = {}
    for row in rows:
        identifier = str(row["id"])
        if identifier in indexed:
            raise ValueError(f"Duplicate scenario identifier: {identifier}")
        indexed[identifier] = row
    return indexed


def execute_matched_family_population(
    config: Mapping[str, object],
    matrix: Mapping[str, object],
    baseline_catalog: Mapping[str, object],
    t1_catalog: Mapping[str, object],
) -> Dict[str, object]:
    if config.get("status") != (
        "EXECUTABLE_POPULATION_CANDIDATE_NOT_COMPARATIVE_EVIDENCE"
    ):
        raise ValueError("Unexpected WP15-D3 configuration status")
    if config.get("run_class") != RUN_CLASS:
        raise ValueError("WP15-D3 must remain a pilot-only run class")

    family_index = _index_by_id(matrix["comparison_families"])
    baseline_index = _index_by_id(baseline_catalog["tests"])
    t1_index = _index_by_id(t1_catalog["tests"])
    recipes = config["t1_execution_recipes"]
    eligible_ids = list(config["eligible_family_ids"])

    rows: List[Dict[str, object]] = []
    executions: List[Dict[str, object]] = []
    denominators: List[Dict[str, object]] = []

    for family_id in eligible_ids:
        family = family_index[family_id]
        if family.get("classification") != "QUALIFIED_MATCH":
            raise ValueError(
                f"WP15-D3 cannot execute non-qualified family {family_id}"
            )
        allowed_fields = list(family["allowed_fields"])
        family_rows: List[Dict[str, object]] = []

        for member in family["members"]:
            treatment = str(member["treatment"])
            source_id = str(member["source_id"])
            if member.get("source_type") != "CATALOG":
                raise ValueError(
                    f"Qualified family member must be catalog-backed: "
                    f"{family_id}/{source_id}"
                )

            if treatment == "T1":
                if source_id not in recipes:
                    raise KeyError(f"Missing T1 execution recipe: {source_id}")
                raw_metrics, execution = _execute_t1_recipe(
                    source_id,
                    recipes[source_id],
                    t1_index[source_id],
                )
            else:
                baseline_result = run_baseline_scenario(
                    baseline_index[source_id]
                )
                raw_metrics = baseline_result.metrics.to_dict()
                execution = baseline_result.to_dict()
                execution["catalog_oracle"] = {
                    "expected_alignment": baseline_index[source_id][
                        "expected_alignment"
                    ],
                    "expected_outcome": baseline_index[source_id][
                        "expected_outcome"
                    ],
                    "status": "MATCHED_INTERNAL_DESIGN_ORACLE",
                }
                execution["publication_evidence"] = False

            projection = project_allowed_metrics(
                raw_metrics,
                allowed_fields,
            )
            execution_digest = canonical_sha256(execution)
            row = {
                "row_id": f"{family_id}:{treatment}:{source_id}",
                "family_id": family_id,
                "family_name": family["name"],
                "family_classification": family["classification"],
                "analysis_unit_id": f"{family_id}:{treatment}",
                "treatment": treatment,
                "source_type": member["source_type"],
                "source_id": source_id,
                "role": member["role"],
                "allowed_fields": allowed_fields,
                "projected_metrics": projection,
                "source_execution_sha256": execution_digest,
                "publication_evidence": False,
            }
            family_rows.append(row)
            rows.append(row)
            executions.append(
                {
                    "row_id": row["row_id"],
                    "source_execution_sha256": execution_digest,
                    "execution": execution,
                }
            )

        analysis_units = {
            str(row["analysis_unit_id"]) for row in family_rows
        }
        treatments = {str(row["treatment"]) for row in family_rows}
        denominators.append(
            {
                "family_id": family_id,
                "member_row_count": len(family_rows),
                "analysis_unit_count": len(analysis_units),
                "treatment_count": len(treatments),
                "policy_variant_row_count": len(family_rows) - len(analysis_units),
                "family_coverage_status": "COMPLETE",
                "success_rate_denominator": "NOT_DEFINED",
                "aggregate_authorized": False,
                "publication_evidence": False,
            }
        )

    if len(rows) != int(config["expected_member_row_count"]):
        raise AssertionError("WP15-D3 member-row count drifted")
    if len(denominators) != int(config["expected_family_count"]):
        raise AssertionError("WP15-D3 family count drifted")
    analysis_unit_count = sum(
        int(row["analysis_unit_count"]) for row in denominators
    )
    if analysis_unit_count != int(config["expected_analysis_unit_count"]):
        raise AssertionError("WP15-D3 analysis-unit count drifted")

    return {
        "schema_version": "0.1.0",
        "phase": "Phase 15",
        "work_package": "WP15-D3",
        "status": POPULATION_STATUS,
        "run_class": RUN_CLASS,
        "publication_evidence": False,
        "comparability_matrix_status": matrix["status"],
        "eligible_family_ids": eligible_ids,
        "family_count": len(denominators),
        "member_row_count": len(rows),
        "analysis_unit_count": analysis_unit_count,
        "comparison_authorization": {
            "member_level_projection": "AUTHORIZED_FOR_INTERNAL_VALIDATION",
            "family_specific_descriptive_comparison": "NOT_YET_AUTHORIZED",
            "pooled_cross_treatment_aggregation": "NOT_PERMITTED",
            "success_rate_or_percentage": "NOT_PERMITTED",
            "inferential_statistics": "NOT_PERMITTED",
            "treatment_superiority": "NOT_PERMITTED",
            "publication_evidence": False,
        },
        "rows": rows,
        "denominators": denominators,
        "source_executions": executions,
    }


def write_matched_family_population(
    payload: Mapping[str, object],
    json_path: Path,
    member_csv_path: Path,
    denominator_csv_path: Path,
    manifest_path: Path,
) -> None:
    for path in (
        json_path,
        member_csv_path,
        denominator_csv_path,
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
        "family_name",
        "family_classification",
        "analysis_unit_id",
        "treatment",
        "source_type",
        "source_id",
        "role",
        "allowed_fields_json",
        "projected_metrics_json",
        "source_execution_sha256",
        "publication_evidence",
    ]
    with member_csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=member_fields)
        writer.writeheader()
        for row in payload["rows"]:
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
                    "projected_metrics_json": json.dumps(
                        row["projected_metrics"],
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                }
            )

    denominator_fields = [
        "family_id",
        "member_row_count",
        "analysis_unit_count",
        "treatment_count",
        "policy_variant_row_count",
        "family_coverage_status",
        "success_rate_denominator",
        "aggregate_authorized",
        "publication_evidence",
    ]
    with denominator_csv_path.open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=denominator_fields)
        writer.writeheader()
        writer.writerows(payload["denominators"])

    base = manifest_path.parent
    manifest_lines = []
    for path in sorted(
        (json_path, member_csv_path, denominator_csv_path),
        key=lambda value: value.name,
    ):
        relative = path.relative_to(base).as_posix()
        manifest_lines.append(f"{sha256_file(path)}  {relative}")
    manifest_path.write_text(
        "\n".join(manifest_lines) + "\n",
        encoding="utf-8",
    )


def verify_derived_manifest(base: Path, manifest_path: Path) -> None:
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        path = base / relative
        if not path.is_file():
            raise RuntimeError(f"Derived manifest path missing: {relative}")
        if sha256_file(path) != expected:
            raise RuntimeError(f"Derived checksum mismatch: {relative}")


__all__ = [
    "POPULATION_STATUS",
    "RUN_CLASS",
    "canonical_sha256",
    "execute_matched_family_population",
    "verify_derived_manifest",
    "write_matched_family_population",
]
