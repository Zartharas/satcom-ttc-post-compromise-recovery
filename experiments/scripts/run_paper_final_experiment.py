#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Dict, Iterable, List, Mapping, Sequence

from ttc_recovery.fault_metrics import (
    FaultAction,
    FaultKind,
    SeededExperimentConfig,
    run_seeded_experiment,
    schedule_from_dicts,
    schedule_sha256,
)
from ttc_recovery.matched_family_population import (
    execute_matched_family_population,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "experiments" / "configs" / "paper-final-experiment.json"
EXPECTED_PLAN_SHA256 = "3570834a70c76e020dada459e036786f690698125fe1d9e171e9f945748a1012"

D3_CONFIG = ROOT / "experiments" / "configs" / "phase-15-matched-family-population.json"
D4_PLAN = ROOT / "experiments" / "configs" / "phase-15-family-descriptive-plan.json"
MATRIX = ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"
BASELINE_CATALOG = ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"
T1_CATALOG = ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json"

METRIC_FIELDS = (
    "seed",
    "schedule_sha256",
    "outcome",
    "alignment",
    "security_state",
    "availability_state",
    "recovery_duration_contacts",
    "divergent_contact_windows",
    "degraded_contact_windows",
    "total_transmissions",
    "retry_overhead",
    "fault_count",
    "drop_count",
    "delay_count",
    "duplicate_count",
    "reorder_count",
    "contact_close_count",
    "restart_count",
    "replay_count",
    "rejection_count",
    "replay_rejection_count",
    "stale_state_rejection_count",
    "command_accepted",
    "telemetry_complete",
    "verification_complete",
    "active_key_compromised",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def validate_plan(config_path: Path) -> dict:
    if not config_path.is_file():
        raise FileNotFoundError(config_path)

    actual_plan_sha = sha256_file(config_path)
    if actual_plan_sha != EXPECTED_PLAN_SHA256:
        raise ValueError(
            "Final experiment plan SHA-256 mismatch: "
            f"{actual_plan_sha} != {EXPECTED_PLAN_SHA256}"
        )

    plan = load_json(config_path)
    if plan.get("status") != "PREDECLARED_PRE_RUN_NOT_EXECUTED":
        raise ValueError("Unexpected final experiment plan status")
    if plan.get("outcomes_read_during_plan_generation") is not False:
        raise ValueError("Plan must remain outcome-blind at generation time")

    for relative, expected in plan["protected_inputs_sha256"].items():
        path = ROOT / relative
        actual = sha256_file(path)
        if actual != expected:
            raise ValueError(
                f"Protected input drifted: {relative}: {actual} != {expected}"
            )

    study_b = plan["studies"]["study_b_deterministic_t1"]
    if int(study_b["schedule_count"]) != 40:
        raise ValueError("Study B schedule count drifted")
    for row in study_b["schedules"]:
        schedule = schedule_from_dicts(row["actions"])
        if schedule_sha256(schedule) != row["schedule_sha256"]:
            raise ValueError(f"Study B schedule drifted: {row['id']}")

    study_c = plan["studies"]["study_c_mixed_fault_t1"]
    if study_c["seeds"] != list(range(10001, 10101)):
        raise ValueError("Study C seed population drifted")
    if int(study_c["schedule_count"]) != 100:
        raise ValueError("Study C schedule count drifted")
    for row in study_c["schedules"]:
        schedule = schedule_from_dicts(row["actions"])
        if schedule_sha256(schedule) != row["schedule_sha256"]:
            raise ValueError(f"Study C schedule drifted: {row['id']}")

    study_d = plan["studies"]["study_d_sensitivity_t1"]
    if int(study_d["schedule_count"]) != 12:
        raise ValueError("Study D schedule count drifted")
    if int(study_d["execution_count"]) != 108:
        raise ValueError("Study D execution count drifted")
    for row in study_d["schedules"]:
        schedule = schedule_from_dicts(row["actions"])
        if schedule_sha256(schedule) != row["schedule_sha256"]:
            raise ValueError(f"Study D schedule drifted: {row['id']}")

    return plan


def execution_identity(config_path: Path) -> dict:
    if git("status", "--porcelain"):
        raise RuntimeError("Final execution requires a clean tracked working tree")

    branch = git("branch", "--show-current")
    commit = git("rev-parse", "HEAD")
    relative_config = config_path.resolve().relative_to(ROOT).as_posix()
    plan_commit = git("log", "-1", "--format=%H", "--", relative_config)

    return {
        "branch": branch,
        "commit": commit,
        "plan_commit": plan_commit,
        "plan_sha256": sha256_file(config_path),
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
    }


def seeded_config(
    plan: Mapping[str, object],
    *,
    seed: int,
    max_transmissions: int | None = None,
    candidate_lifetime_contacts: int | None = None,
) -> SeededExperimentConfig:
    base = plan["base_t1_parameters"]
    return SeededExperimentConfig(
        seed=int(seed),
        ground_epoch=int(base["ground_epoch"]),
        spacecraft_epoch=int(base["spacecraft_epoch"]),
        authority_epoch_floor=int(base["authority_epoch_floor"]),
        max_transmissions=(
            int(base["max_transmissions"])
            if max_transmissions is None
            else int(max_transmissions)
        ),
        candidate_lifetime_contacts=(
            int(base["candidate_lifetime_contacts"])
            if candidate_lifetime_contacts is None
            else int(candidate_lifetime_contacts)
        ),
        max_faults=int(base["max_faults"]),
        compromise_active_keys=bool(base["compromise_active_keys"]),
        allowed_faults=tuple(FaultKind(name) for name in base["allowed_faults"]),
    )


def result_record(
    *,
    schedule_spec: Mapping[str, object],
    result,
    extra: Mapping[str, object] | None = None,
) -> dict:
    record = {
        "schedule_id": schedule_spec["id"],
        "schedule_class": schedule_spec["schedule_class"],
        "schedule_sha256": schedule_spec["schedule_sha256"],
        "actions": list(schedule_spec["actions"]),
        "result": result.to_dict(),
    }
    if extra:
        record.update(extra)
    return record


def run_study_a(plan: Mapping[str, object]) -> tuple[dict, List[dict]]:
    payload = execute_matched_family_population(
        load_json(D3_CONFIG),
        load_json(MATRIX),
        load_json(BASELINE_CATALOG),
        load_json(T1_CATALOG),
    )

    expected = plan["studies"]["study_a_matched_families"]
    if payload["eligible_family_ids"] != expected["family_ids"]:
        raise ValueError("Study A family identity drifted")
    if int(payload["member_row_count"]) != int(expected["member_row_count"]):
        raise ValueError("Study A member count drifted")
    if int(payload["analysis_unit_count"]) != int(expected["analysis_unit_count"]):
        raise ValueError("Study A analysis-unit count drifted")

    d4 = load_json(D4_PLAN)
    d4_by_family = {row["family_id"]: row for row in d4["family_plans"]}
    rows_by_family: Dict[str, List[Mapping[str, object]]] = {}
    for row in payload["rows"]:
        rows_by_family.setdefault(str(row["family_id"]), []).append(row)

    table_rows: List[dict] = []
    for family_id in expected["family_ids"]:
        family_plan = d4_by_family[family_id]
        actual_rows = rows_by_family[family_id]
        actual_ids = {str(row["row_id"]) for row in actual_rows}
        expected_ids = set(family_plan["expected_member_row_ids"])
        if actual_ids != expected_ids:
            raise ValueError(f"Study A D4 member registry drifted for {family_id}")

        for row in actual_rows:
            if list(row["allowed_fields"]) != list(
                family_plan["expected_allowed_fields"]
            ):
                raise ValueError(
                    f"Study A allowed-field drift for {row['row_id']}"
                )
            projected = dict(row["projected_metrics"])
            common_keys = {"outcome", "alignment_class", "availability_state"}
            evidence = {
                key: projected[key]
                for key in projected
                if key not in common_keys
            }
            treatment_variant = str(row["treatment"])
            if family_id == "CF-02" and row["treatment"] == "B1":
                treatment_variant = f"B1 / {row['source_id']}"

            table_rows.append(
                {
                    "family_id": family_id,
                    "treatment_or_policy_variant": treatment_variant,
                    "source_id": row["source_id"],
                    "outcome": projected.get("outcome", ""),
                    "alignment_class": projected.get("alignment_class", ""),
                    "availability_state": projected.get(
                        "availability_state", ""
                    ),
                    "family_specific_authorized_evidence": json.dumps(
                        evidence,
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                }
            )

    return payload, table_rows


def run_study_b(plan: Mapping[str, object]) -> tuple[List[dict], List[dict]]:
    records: List[dict] = []
    table_rows: List[dict] = []

    study = plan["studies"]["study_b_deterministic_t1"]
    for row in study["schedules"]:
        schedule = schedule_from_dicts(row["actions"])
        result = run_seeded_experiment(
            seeded_config(plan, seed=0),
            schedule=schedule,
        )
        records.append(
            result_record(
                schedule_spec=row,
                result=result,
                extra={"schedule_source": "PREDECLARED_SERIALIZED_SCHEDULE"},
            )
        )
        metrics = result.metrics
        rejection_evidence = {
            "rejection_count": metrics.rejection_count,
            "replay_rejection_count": metrics.replay_rejection_count,
            "stale_state_rejection_count": metrics.stale_state_rejection_count,
        }
        table_rows.append(
            {
                "schedule_id": row["id"],
                "schedule_class": row["schedule_class"],
                "fault_kind_or_control": row.get("fault_kind", "NONE"),
                "phase_or_control": row.get("phase", "NONE"),
                "outcome": metrics.outcome,
                "alignment": metrics.alignment,
                "security_state": metrics.security_state,
                "availability_state": metrics.availability_state,
                "verification_complete": metrics.verification_complete,
                "rejection_evidence": json.dumps(
                    rejection_evidence,
                    sort_keys=True,
                    separators=(",", ":"),
                ),
            }
        )

    return records, table_rows


def run_study_c(plan: Mapping[str, object]) -> tuple[List[dict], dict, List[dict]]:
    study = plan["studies"]["study_c_mixed_fault_t1"]
    records: List[dict] = []

    for row in study["schedules"]:
        schedule = schedule_from_dicts(row["actions"])
        seed = int(row["seed"])
        result = run_seeded_experiment(
            seeded_config(plan, seed=seed),
            schedule=schedule,
        )
        records.append(
            result_record(
                schedule_spec=row,
                result=result,
                extra={
                    "seed": seed,
                    "schedule_source": "PREDECLARED_SERIALIZED_SCHEDULE",
                },
            )
        )

    metrics = [record["result"]["metrics"] for record in records]
    denominator = len(metrics)
    outcomes = Counter(str(row["outcome"]) for row in metrics)
    security = Counter(str(row["security_state"]) for row in metrics)
    availability = Counter(str(row["availability_state"]) for row in metrics)
    fault_counts = Counter(int(row["fault_count"]) for row in metrics)

    fault_kind_schedule_counts = Counter()
    for record in records:
        for kind in sorted({str(item["kind"]) for item in record["actions"]}):
            fault_kind_schedule_counts[kind] += 1

    summary = {
        "denominator": denominator,
        "outcome_counts": dict(sorted(outcomes.items())),
        "outcome_percentages": {
            key: round((count / denominator) * 100.0, 6)
            for key, count in sorted(outcomes.items())
        },
        "security_state_counts": dict(sorted(security.items())),
        "availability_state_counts": dict(sorted(availability.items())),
        "verification_complete_count": sum(
            1 for row in metrics if bool(row["verification_complete"])
        ),
        "recovery_duration_contacts": describe_numeric(
            row["recovery_duration_contacts"] for row in metrics
        ),
        "total_transmissions": describe_numeric(
            row["total_transmissions"] for row in metrics
        ),
        "retry_overhead": describe_numeric(
            row["retry_overhead"] for row in metrics
        ),
        "fault_count_schedule_counts": {
            str(key): value for key, value in sorted(fault_counts.items())
        },
        "fault_kind_schedule_counts": dict(
            sorted(fault_kind_schedule_counts.items())
        ),
        "interpretation": "DESCRIPTIVE_FIXED_SYNTHETIC_T1_POPULATION",
    }

    figure_rows = [
        {
            "outcome": outcome,
            "count": count,
            "percentage": round((count / denominator) * 100.0, 6),
            "denominator": denominator,
        }
        for outcome, count in sorted(outcomes.items())
    ]

    return records, summary, figure_rows


def run_study_d(plan: Mapping[str, object]) -> tuple[List[dict], List[dict]]:
    study = plan["studies"]["study_d_sensitivity_t1"]
    records: List[dict] = []

    for max_transmissions in study["max_transmissions_grid"]:
        for candidate_lifetime in study["candidate_lifetime_contacts_grid"]:
            for row in study["schedules"]:
                schedule = schedule_from_dicts(row["actions"])
                result = run_seeded_experiment(
                    seeded_config(
                        plan,
                        seed=0,
                        max_transmissions=int(max_transmissions),
                        candidate_lifetime_contacts=int(candidate_lifetime),
                    ),
                    schedule=schedule,
                )
                records.append(
                    result_record(
                        schedule_spec=row,
                        result=result,
                        extra={
                            "max_transmissions": int(max_transmissions),
                            "candidate_lifetime_contacts": int(
                                candidate_lifetime
                            ),
                            "schedule_source":
                                "PREDECLARED_SENSITIVITY_CHALLENGE",
                        },
                    )
                )

    if len(records) != int(study["execution_count"]):
        raise ValueError("Study D execution count drifted")

    grouped: Dict[tuple[int, int], List[Mapping[str, object]]] = {}
    for record in records:
        key = (
            int(record["max_transmissions"]),
            int(record["candidate_lifetime_contacts"]),
        )
        grouped.setdefault(key, []).append(record["result"]["metrics"])

    summary_rows: List[dict] = []
    for (max_transmissions, candidate_lifetime), metrics in sorted(
        grouped.items()
    ):
        outcomes = Counter(str(row["outcome"]) for row in metrics)
        summary_rows.append(
            {
                "max_transmissions": max_transmissions,
                "candidate_lifetime_contacts": candidate_lifetime,
                "denominator": len(metrics),
                "verification_complete_count": sum(
                    1 for row in metrics if bool(row["verification_complete"])
                ),
                "outcome_counts": json.dumps(
                    dict(sorted(outcomes.items())),
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                "recovery_duration_contacts_median": median(
                    float(row["recovery_duration_contacts"])
                    for row in metrics
                ),
                "recovery_duration_contacts_min": min(
                    int(row["recovery_duration_contacts"])
                    for row in metrics
                ),
                "recovery_duration_contacts_max": max(
                    int(row["recovery_duration_contacts"])
                    for row in metrics
                ),
                "total_transmissions_median": median(
                    float(row["total_transmissions"]) for row in metrics
                ),
                "total_transmissions_min": min(
                    int(row["total_transmissions"]) for row in metrics
                ),
                "total_transmissions_max": max(
                    int(row["total_transmissions"]) for row in metrics
                ),
                "retry_overhead_median": median(
                    float(row["retry_overhead"]) for row in metrics
                ),
                "retry_overhead_min": min(
                    int(row["retry_overhead"]) for row in metrics
                ),
                "retry_overhead_max": max(
                    int(row["retry_overhead"]) for row in metrics
                ),
                "interpretation": "DESCRIPTIVE_FIXED_CHALLENGE_SET",
            }
        )

    return records, summary_rows


def describe_numeric(values: Iterable[object]) -> dict:
    numbers = [float(value) for value in values]
    if not numbers:
        raise ValueError("Cannot describe an empty numeric collection")
    return {
        "median": median(numbers),
        "min": min(numbers),
        "max": max(numbers),
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(output_dir: Path) -> Path:
    manifest = output_dir / "manifests" / "SHA256SUMS"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for path in sorted(
        p for p in output_dir.rglob("*")
        if p.is_file() and p != manifest
    ):
        relative = path.relative_to(output_dir).as_posix()
        lines.append(f"{sha256_file(path)}  {relative}")
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def verify_manifest(output_dir: Path, manifest: Path) -> None:
    for raw in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = raw.split(maxsplit=1)
        path = output_dir / relative
        actual = sha256_file(path)
        if actual != expected:
            raise ValueError(
                f"Output manifest mismatch: {relative}: {actual} != {expected}"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the predeclared final hands-on TT&C recovery experiment."
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate the committed plan and protected inputs without executing outcomes.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = args.config.expanduser().resolve()
    plan = validate_plan(config_path)

    if args.validate_only:
        print("final_plan_sha256=" + EXPECTED_PLAN_SHA256)
        print("protected_inputs=PASS")
        print("study_b_schedule_contract=PASS")
        print("study_c_schedule_contract=PASS")
        print("study_d_schedule_contract=PASS")
        print("final_runner_validate_only=PASS")
        print("outcomes_executed=false")
        return 0

    if args.output_dir is None:
        raise SystemExit("--output-dir is required unless --validate-only is used")

    identity = execution_identity(config_path)
    output_dir = args.output_dir.expanduser().resolve()
    if output_dir.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing final-run directory: {output_dir}"
        )

    output_dir.mkdir(parents=True)
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        inputs_dir = output_dir / "inputs"
        inputs_dir.mkdir(parents=True)
        shutil.copy2(config_path, inputs_dir / config_path.name)

        study_a_raw, table_1 = run_study_a(plan)
        write_json(output_dir / "raw" / "study-a-matched-families.json", study_a_raw)
        write_csv(
            output_dir / "processed" / "table-1-matched-family-outcomes.csv",
            table_1,
        )

        study_b_raw, table_2 = run_study_b(plan)
        write_json(output_dir / "raw" / "study-b-deterministic-t1.json", study_b_raw)
        write_csv(
            output_dir / "processed" / "table-2-deterministic-t1.csv",
            table_2,
        )

        study_c_raw, study_c_summary, figure_2 = run_study_c(plan)
        write_json(output_dir / "raw" / "study-c-mixed-fault-t1.json", study_c_raw)
        write_json(
            output_dir / "processed" / "study-c-summary.json",
            study_c_summary,
        )
        write_csv(
            output_dir / "figures" / "figure-2-outcome-distribution-source.csv",
            figure_2,
        )

        study_d_raw, study_d_summary = run_study_d(plan)
        write_json(output_dir / "raw" / "study-d-sensitivity-t1.json", study_d_raw)
        write_csv(
            output_dir / "processed" / "study-d-sensitivity-summary.csv",
            study_d_summary,
        )
        write_csv(
            output_dir / "figures" / "figure-3-sensitivity-source.csv",
            [
                {
                    "max_transmissions": row["max_transmissions"],
                    "candidate_lifetime_contacts":
                        row["candidate_lifetime_contacts"],
                    "verification_complete_count":
                        row["verification_complete_count"],
                    "denominator": row["denominator"],
                }
                for row in study_d_summary
            ],
        )

        completed = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        metadata = {
            "schema_version": "1.0.0",
            "status": "COMPLETED_RETAINED_FINAL_EXPERIMENT",
            "started_utc": started,
            "completed_utc": completed,
            "execution_identity": identity,
            "command": sys.argv,
            "plan_status": plan["status"],
            "study_counts": {
                "study_a_member_rows": len(table_1),
                "study_b_schedules": len(study_b_raw),
                "study_c_schedules": len(study_c_raw),
                "study_d_executions": len(study_d_raw),
            },
            "claim_boundaries": plan["claim_boundaries"],
            "independent_validation": False,
            "publication_evidence": False,
            "result_interpretation":
                "FINAL_INTERNAL_EXPERIMENT_RESULTS_WITH_DECLARED_LIMITATIONS",
        }
        write_json(output_dir / "metadata.json", metadata)

        manifest = write_manifest(output_dir)
        verify_manifest(output_dir, manifest)

    except Exception as exc:
        failure = {
            "schema_version": "1.0.0",
            "status": "FAILED_RETAINED_EXECUTION_ATTEMPT",
            "started_utc": started,
            "failed_utc": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "execution_identity": identity,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "publication_evidence": False,
        }
        write_json(output_dir / "FAILURE.json", failure)
        raise

    print("final_experiment_status=COMPLETED_RETAINED_FINAL_EXPERIMENT")
    print(f"output_dir={output_dir}")
    print("study_a_member_rows=13")
    print("study_b_schedules=40")
    print("study_c_schedules=100")
    print("study_d_executions=108")
    print("output_manifest=PASS")
    print("outcome_values_printed=false")
    print("independent_validation=false")
    print("publication_evidence=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
