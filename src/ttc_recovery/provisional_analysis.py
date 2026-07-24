from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from .fault_metrics import (
    FaultKind,
    SeededExperimentConfig,
    run_seeded_experiment,
    schedule_from_dicts,
    schedule_sha256,
)


PROVISIONAL_STATUS = "PROVISIONAL_INTERNAL_REVIEW_ONLY"

_NUMERIC_METRICS = (
    "recovery_duration_contacts",
    "divergent_contact_windows",
    "degraded_contact_windows",
    "total_transmissions",
    "retry_overhead",
    "fault_count",
    "rejection_count",
    "replay_rejection_count",
    "stale_state_rejection_count",
)

_REQUIRED_METRICS = {
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
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_phase07_results(path: Path) -> Dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("status") != PROVISIONAL_STATUS:
        raise ValueError("Phase 07 results must remain provisional.")
    results = payload.get("results")
    if not isinstance(results, list) or not results:
        raise ValueError("Phase 07 results must contain at least one record.")
    for index, record in enumerate(results):
        if not isinstance(record, dict):
            raise ValueError(f"Result {index} is not an object.")
        if record.get("status") != PROVISIONAL_STATUS:
            raise ValueError(f"Result {index} is not marked provisional.")
        if not isinstance(record.get("config"), dict):
            raise ValueError(f"Result {index} has no configuration object.")
        if not isinstance(record.get("schedule"), list):
            raise ValueError(f"Result {index} has no serialized schedule.")
        metrics = record.get("metrics")
        if not isinstance(metrics, dict):
            raise ValueError(f"Result {index} has no metrics object.")
        missing = sorted(_REQUIRED_METRICS - set(metrics))
        if missing:
            raise ValueError(
                f"Result {index} is missing metrics: {', '.join(missing)}"
            )
        if not isinstance(record.get("event_log"), list):
            raise ValueError(f"Result {index} has no event log.")
    return payload


def verify_checksum_manifest(
    bundle_dir: Path,
    manifest_name: str = "phase07-run-bundle.sha256",
) -> Dict[str, object]:
    manifest_path = bundle_dir / manifest_name
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Checksum manifest not found: {manifest_path}")

    verified: List[Dict[str, str]] = []
    for line_number, raw_line in enumerate(
        manifest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Malformed checksum line {line_number}.")
        expected, relative_name = parts
        relative_name = relative_name.lstrip("*")
        relative_path = Path(relative_name)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"Unsafe checksum path on line {line_number}.")
        target = bundle_dir / relative_path
        if not target.is_file():
            raise FileNotFoundError(f"Bundle file not found: {target}")
        actual = sha256_file(target)
        if actual != expected:
            raise ValueError(
                f"Checksum mismatch for {relative_name}: {actual} != {expected}"
            )
        verified.append(
            {"path": relative_name, "sha256": actual}
        )

    if not verified:
        raise ValueError("Checksum manifest contains no file records.")
    return {
        "manifest": manifest_name,
        "verified_file_count": len(verified),
        "files": verified,
    }


def _normalize_csv_value(value: object) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def verify_metrics_csv(
    results: Sequence[Mapping[str, object]],
    csv_path: Path,
) -> Dict[str, object]:
    if not csv_path.is_file():
        raise FileNotFoundError(f"Metrics CSV not found: {csv_path}")
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != len(results):
        raise ValueError(
            f"Metrics CSV contains {len(rows)} rows; JSON contains {len(results)} results."
        )

    expected_by_key: Dict[Tuple[str, str], Mapping[str, object]] = {}
    for record in results:
        metrics = record["metrics"]
        key = (str(metrics["seed"]), str(metrics["schedule_sha256"]))
        if key in expected_by_key:
            raise ValueError(f"Duplicate JSON metric identity: {key}")
        expected_by_key[key] = metrics

    seen = set()
    for row in rows:
        key = (str(row.get("seed", "")), str(row.get("schedule_sha256", "")))
        if key not in expected_by_key:
            raise ValueError(f"CSV metric identity not present in JSON: {key}")
        if key in seen:
            raise ValueError(f"Duplicate CSV metric identity: {key}")
        seen.add(key)
        expected = expected_by_key[key]
        for field, expected_value in expected.items():
            if field not in row:
                raise ValueError(f"CSV is missing metric column: {field}")
            if row[field] != _normalize_csv_value(expected_value):
                raise ValueError(
                    f"CSV mismatch for {key}, field {field}: "
                    f"{row[field]!r} != {_normalize_csv_value(expected_value)!r}"
                )

    return {
        "row_count": len(rows),
        "json_csv_consistent": True,
        "csv_sha256": sha256_file(csv_path),
    }


def _fault_kinds(record: Mapping[str, object]) -> List[str]:
    return sorted({str(action["kind"]) for action in record["schedule"]})


def _fault_phases(record: Mapping[str, object]) -> List[str]:
    return sorted({str(action["phase"]) for action in record["schedule"]})


def _event_names(record: Mapping[str, object]) -> List[str]:
    return [str(event.get("event", "")) for event in record["event_log"]]


def diagnostic_label(record: Mapping[str, object]) -> str:
    metrics = record["metrics"]
    outcome = str(metrics["outcome"])
    events = set(_event_names(record))

    if outcome == "SUCCESS":
        return "VERIFIED_RECOVERY"
    if outcome == "INDETERMINATE":
        if "t1_test_command_dropped" in events:
            return "TEST_COMMAND_EVIDENCE_LOSS"
        if "t1_status_telemetry_dropped" in events:
            return "STATUS_TELEMETRY_LOSS"
        return "INCOMPLETE_VERIFICATION_EVIDENCE"
    if outcome == "SECURE_DEGRADED":
        if (
            "phase07_unconfirmed_spacecraft_activation" in events
            or "t1_confirmation_budget_exhausted" in events
        ):
            return "CONFIRMATION_PATH_EXHAUSTION"
        return "UNVERIFIED_DEGRADED_ALIGNMENT"
    if outcome == "EXPIRED":
        if "phase07_endpoint_restarted" in events:
            return "ENDPOINT_RESTART_BEFORE_ACTIVATION"
        return "PRE_ACTIVATION_DELIVERY_EXHAUSTION"
    if outcome == "AVAILABLE_UNSAFE":
        return "ACTIVE_STATE_REMAINS_COMPROMISED"
    if outcome == "LOCKED":
        return "NO_AUTHORIZED_RECOVERY_TRANSITION"
    if outcome == "DIVERGED":
        return "INCOMPATIBLE_ENDPOINT_STATE"
    return "UNCLASSIFIED_PROVISIONAL_OUTCOME"


def annotate_results(
    results: Sequence[Mapping[str, object]],
) -> List[Dict[str, object]]:
    annotated = []
    for record in results:
        metrics = dict(record["metrics"])
        kinds = _fault_kinds(record)
        phases = _fault_phases(record)
        annotated.append(
            {
                **metrics,
                "fault_kinds": ";".join(kinds) if kinds else "NONE",
                "fault_phases": ";".join(phases) if phases else "NONE",
                "fault_signature": "+".join(kinds) if kinds else "NO_FAULT",
                "phase_signature": "+".join(phases) if phases else "NO_FAULT",
                "diagnostic_label": diagnostic_label(record),
                "diagnostic_status": "DESCRIPTIVE_NOT_CAUSAL",
            }
        )
    return annotated


def trace_anomalies(
    results: Sequence[Mapping[str, object]],
) -> List[Dict[str, object]]:
    anomalies: List[Dict[str, object]] = []

    def add(record: Mapping[str, object], code: str, detail: str) -> None:
        metrics = record["metrics"]
        anomalies.append(
            {
                "seed": metrics["seed"],
                "schedule_sha256": metrics["schedule_sha256"],
                "code": code,
                "detail": detail,
            }
        )

    for record in results:
        metrics = record["metrics"]
        config = record["config"]
        schedule = schedule_from_dicts(record["schedule"])
        actual_hash = schedule_sha256(schedule)
        if actual_hash != metrics["schedule_sha256"]:
            add(record, "SCHEDULE_HASH_MISMATCH", actual_hash)
        if int(metrics["seed"]) != int(config["seed"]):
            add(record, "SEED_MISMATCH", "metrics seed differs from config seed")
        if int(metrics["fault_count"]) != len(schedule):
            add(record, "FAULT_COUNT_MISMATCH", "fault_count differs from schedule length")

        expected_counts = {
            "drop_count": "DROP",
            "delay_count": "DELAY",
            "duplicate_count": "DUPLICATE",
            "reorder_count": "REORDER",
            "contact_close_count": "CONTACT_CLOSE",
            "restart_count": "ENDPOINT_RESTART",
            "replay_count": "STALE_REPLAY",
        }
        schedule_counts = Counter(action.kind.value for action in schedule)
        for metric_name, fault_name in expected_counts.items():
            if int(metrics[metric_name]) != schedule_counts[fault_name]:
                add(
                    record,
                    "FAULT_KIND_COUNT_MISMATCH",
                    f"{metric_name} differs from serialized schedule",
                )

        event_log = record["event_log"]
        expected_sequence = list(range(len(event_log)))
        actual_sequence = [event.get("event_seq") for event in event_log]
        if actual_sequence != expected_sequence:
            add(record, "EVENT_SEQUENCE_INVALID", "event_seq is not contiguous")

        if int(metrics["recovery_duration_contacts"]) < 1:
            add(record, "INVALID_DURATION", "recovery duration is below one contact")
        if int(metrics["retry_overhead"]) != max(
            0, int(metrics["total_transmissions"]) - 6
        ):
            add(record, "RETRY_OVERHEAD_MISMATCH", "retry overhead is inconsistent")

        outcome = str(metrics["outcome"])
        alignment = str(metrics["alignment"])
        verified = bool(metrics["verification_complete"])
        command = bool(metrics["command_accepted"])
        telemetry = bool(metrics["telemetry_complete"])
        compromised = bool(metrics["active_key_compromised"])
        security = str(metrics["security_state"])
        availability = str(metrics["availability_state"])

        if outcome == "SUCCESS":
            if not (
                verified
                and command
                and telemetry
                and alignment.startswith("SYNC")
                and not compromised
                and security == "SECURE_PROVISIONAL"
                and availability == "AVAILABLE"
            ):
                add(record, "SUCCESS_INVARIANT_VIOLATION", "success fields disagree")
        elif outcome == "INDETERMINATE":
            if verified or not alignment.startswith("SYNC") or availability != "DEGRADED":
                add(
                    record,
                    "INDETERMINATE_INVARIANT_VIOLATION",
                    "indeterminate fields disagree",
                )
        elif outcome == "SECURE_DEGRADED":
            if availability != "DEGRADED" or verified:
                add(
                    record,
                    "DEGRADED_INVARIANT_VIOLATION",
                    "secure-degraded fields disagree",
                )
        elif outcome == "AVAILABLE_UNSAFE":
            if not compromised or security != "UNSAFE":
                add(record, "UNSAFE_INVARIANT_VIOLATION", "unsafe fields disagree")
        elif verified:
            add(record, "NON_SUCCESS_VERIFIED", "non-success result is marked verified")

    return anomalies


def _average(rows: Sequence[Mapping[str, object]], field: str) -> float:
    return round(fmean(float(row[field]) for row in rows), 6) if rows else 0.0


def _summary_row(
    group_type: str,
    group_value: str,
    rows: Sequence[Mapping[str, object]],
    *,
    membership: str,
    overlapping_groups: bool,
    min_group_size: int,
) -> Dict[str, object]:
    outcomes = Counter(str(row["outcome"]) for row in rows)
    security = Counter(str(row["security_state"]) for row in rows)
    availability = Counter(str(row["availability_state"]) for row in rows)
    count = len(rows)
    success_count = outcomes.get("SUCCESS", 0)
    return {
        "group_type": group_type,
        "group_value": group_value,
        "membership": membership,
        "overlapping_groups": overlapping_groups,
        "n": count,
        "success_count": success_count,
        "success_fraction": round(success_count / count, 6) if count else 0.0,
        "outcome_counts": json.dumps(dict(sorted(outcomes.items())), sort_keys=True),
        "security_counts": json.dumps(dict(sorted(security.items())), sort_keys=True),
        "availability_counts": json.dumps(
            dict(sorted(availability.items())), sort_keys=True
        ),
        "mean_recovery_duration_contacts": _average(
            rows, "recovery_duration_contacts"
        ),
        "mean_total_transmissions": _average(rows, "total_transmissions"),
        "mean_retry_overhead": _average(rows, "retry_overhead"),
        "mean_divergent_contact_windows": _average(
            rows, "divergent_contact_windows"
        ),
        "mean_degraded_contact_windows": _average(
            rows, "degraded_contact_windows"
        ),
        "denominator_status": (
            "LOW_N_DESCRIPTIVE_ONLY" if count < min_group_size else "DESCRIPTIVE_ONLY"
        ),
    }


def aggregate_results(
    annotated: Sequence[Mapping[str, object]],
    min_group_size: int,
) -> Dict[str, List[Dict[str, object]]]:
    outcome_groups: Dict[str, List[Mapping[str, object]]] = defaultdict(list)
    fault_groups: Dict[str, List[Mapping[str, object]]] = defaultdict(list)
    phase_groups: Dict[str, List[Mapping[str, object]]] = defaultdict(list)
    fault_count_groups: Dict[str, List[Mapping[str, object]]] = defaultdict(list)

    for row in annotated:
        outcome_groups[str(row["outcome"])].append(row)
        fault_count_groups[str(row["fault_count"])].append(row)
        kinds = str(row["fault_kinds"]).split(";")
        phases = str(row["fault_phases"]).split(";")
        for kind in kinds:
            fault_groups[kind].append(row)
        for phase in phases:
            phase_groups[phase].append(row)

    overall = [
        _summary_row(
            "overall",
            "ALL_RESULTS",
            annotated,
            membership="each schedule exactly once",
            overlapping_groups=False,
            min_group_size=min_group_size,
        )
    ]
    by_outcome = [
        _summary_row(
            "outcome",
            key,
            rows,
            membership="each schedule exactly once",
            overlapping_groups=False,
            min_group_size=min_group_size,
        )
        for key, rows in sorted(outcome_groups.items())
    ]
    by_fault = [
        _summary_row(
            "fault_kind",
            key,
            rows,
            membership="schedule contains fault kind",
            overlapping_groups=True,
            min_group_size=min_group_size,
        )
        for key, rows in sorted(fault_groups.items())
    ]
    by_phase = [
        _summary_row(
            "fault_phase",
            key,
            rows,
            membership="schedule contains a fault in phase",
            overlapping_groups=True,
            min_group_size=min_group_size,
        )
        for key, rows in sorted(phase_groups.items())
    ]
    by_fault_count = [
        _summary_row(
            "fault_count",
            key,
            rows,
            membership="each schedule exactly once",
            overlapping_groups=False,
            min_group_size=min_group_size,
        )
        for key, rows in sorted(
            fault_count_groups.items(), key=lambda item: int(item[0])
        )
    ]

    cross_counter = Counter(
        (str(row["security_state"]), str(row["availability_state"]))
        for row in annotated
    )
    security_availability = [
        {
            "security_state": security,
            "availability_state": availability,
            "n": count,
            "denominator": len(annotated),
            "fraction": round(count / len(annotated), 6) if annotated else 0.0,
            "status": "DESCRIPTIVE_ONLY",
        }
        for (security, availability), count in sorted(cross_counter.items())
    ]

    return {
        "overall": overall,
        "by_outcome": by_outcome,
        "by_fault_kind": by_fault,
        "by_fault_phase": by_phase,
        "by_fault_count": by_fault_count,
        "security_availability": security_availability,
    }


def coverage_audit(
    results: Sequence[Mapping[str, object]],
    required_faults: Sequence[str],
    required_phases: Sequence[str],
    min_group_size: int,
) -> List[Dict[str, object]]:
    fault_counter = Counter()
    phase_counter = Counter()
    schedule_hashes = Counter()
    seeds = Counter()
    outcomes = Counter()

    for record in results:
        metrics = record["metrics"]
        schedule_hashes[str(metrics["schedule_sha256"])] += 1
        seeds[str(metrics["seed"])] += 1
        outcomes[str(metrics["outcome"])] += 1
        for fault in _fault_kinds(record):
            fault_counter[fault] += 1
        for phase in _fault_phases(record):
            phase_counter[phase] += 1

    rows: List[Dict[str, object]] = []
    for fault in required_faults:
        count = fault_counter[fault]
        rows.append(
            {
                "dimension": "fault_kind",
                "value": fault,
                "n": count,
                "status": (
                    "MISSING"
                    if count == 0
                    else "LOW_N"
                    if count < min_group_size
                    else "PRESENT"
                ),
            }
        )
    for phase in required_phases:
        count = phase_counter[phase]
        rows.append(
            {
                "dimension": "fault_phase",
                "value": phase,
                "n": count,
                "status": (
                    "MISSING"
                    if count == 0
                    else "LOW_N"
                    if count < min_group_size
                    else "PRESENT"
                ),
            }
        )
    rows.extend(
        [
            {
                "dimension": "identity",
                "value": "duplicate_schedule_hashes",
                "n": sum(count - 1 for count in schedule_hashes.values() if count > 1),
                "status": (
                    "REVIEW" if any(count > 1 for count in schedule_hashes.values()) else "CLEAR"
                ),
            },
            {
                "dimension": "identity",
                "value": "duplicate_seeds",
                "n": sum(count - 1 for count in seeds.values() if count > 1),
                "status": "REVIEW" if any(count > 1 for count in seeds.values()) else "CLEAR",
            },
            {
                "dimension": "outcome",
                "value": "observed_outcome_classes",
                "n": len(outcomes),
                "status": "DESCRIPTIVE_ONLY",
            },
        ]
    )
    return rows


def adverse_cases(
    annotated: Sequence[Mapping[str, object]],
) -> List[Dict[str, object]]:
    return [
        {
            "seed": row["seed"],
            "schedule_sha256": row["schedule_sha256"],
            "outcome": row["outcome"],
            "alignment": row["alignment"],
            "security_state": row["security_state"],
            "availability_state": row["availability_state"],
            "fault_kinds": row["fault_kinds"],
            "fault_phases": row["fault_phases"],
            "diagnostic_label": row["diagnostic_label"],
            "diagnostic_status": row["diagnostic_status"],
            "recovery_duration_contacts": row["recovery_duration_contacts"],
            "total_transmissions": row["total_transmissions"],
            "retry_overhead": row["retry_overhead"],
        }
        for row in annotated
        if row["outcome"] != "SUCCESS"
    ]


def _config_from_record(
    record: Mapping[str, object],
    *,
    max_transmissions: int,
    candidate_lifetime_contacts: int,
) -> SeededExperimentConfig:
    config = record["config"]
    allowed_faults = tuple(
        FaultKind(str(name)) for name in config.get("allowed_faults", [])
    )
    return SeededExperimentConfig(
        seed=int(config["seed"]),
        ground_epoch=int(config["ground_epoch"]),
        spacecraft_epoch=int(config["spacecraft_epoch"]),
        authority_epoch_floor=int(config["authority_epoch_floor"]),
        max_transmissions=int(max_transmissions),
        candidate_lifetime_contacts=int(candidate_lifetime_contacts),
        max_faults=int(config["max_faults"]),
        compromise_active_keys=bool(config["compromise_active_keys"]),
        allowed_faults=allowed_faults,
    )


def run_sensitivity_scaffold(
    results: Sequence[Mapping[str, object]],
    max_transmissions_values: Sequence[int],
    candidate_lifetime_values: Sequence[int],
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    rows: List[Dict[str, object]] = []
    for record in results:
        source_metrics = record["metrics"]
        schedule = schedule_from_dicts(record["schedule"])
        for max_transmissions in max_transmissions_values:
            for candidate_lifetime in candidate_lifetime_values:
                config = _config_from_record(
                    record,
                    max_transmissions=int(max_transmissions),
                    candidate_lifetime_contacts=int(candidate_lifetime),
                )
                result = run_seeded_experiment(config, schedule=schedule)
                unreachable_actions = sum(
                    1
                    for action in schedule
                    if action.attempt > config.max_transmissions
                )
                rows.append(
                    {
                        "source_seed": source_metrics["seed"],
                        "source_schedule_sha256": source_metrics["schedule_sha256"],
                        "max_transmissions": config.max_transmissions,
                        "candidate_lifetime_contacts": config.candidate_lifetime_contacts,
                        "unreachable_fault_actions": unreachable_actions,
                        "outcome": result.metrics.outcome,
                        "alignment": result.metrics.alignment,
                        "security_state": result.metrics.security_state,
                        "availability_state": result.metrics.availability_state,
                        "recovery_duration_contacts": result.metrics.recovery_duration_contacts,
                        "total_transmissions": result.metrics.total_transmissions,
                        "retry_overhead": result.metrics.retry_overhead,
                        "verification_complete": result.metrics.verification_complete,
                        "status": "PROVISIONAL_SENSITIVITY_SCAFFOLD",
                    }
                )

    grouped: Dict[Tuple[int, int], List[Dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[
            (int(row["max_transmissions"]), int(row["candidate_lifetime_contacts"]))
        ].append(row)

    summary = []
    for (max_transmissions, candidate_lifetime), group_rows in sorted(grouped.items()):
        outcomes = Counter(str(row["outcome"]) for row in group_rows)
        success_count = outcomes.get("SUCCESS", 0)
        summary.append(
            {
                "max_transmissions": max_transmissions,
                "candidate_lifetime_contacts": candidate_lifetime,
                "n": len(group_rows),
                "success_count": success_count,
                "success_fraction": round(success_count / len(group_rows), 6),
                "outcome_counts": json.dumps(
                    dict(sorted(outcomes.items())), sort_keys=True
                ),
                "mean_recovery_duration_contacts": _average(
                    group_rows, "recovery_duration_contacts"
                ),
                "mean_total_transmissions": _average(
                    group_rows, "total_transmissions"
                ),
                "mean_retry_overhead": _average(group_rows, "retry_overhead"),
                "status": "DESCRIPTIVE_UNFROZEN_GRID",
            }
        )
    return rows, summary


def build_analysis(
    payload: Mapping[str, object],
    *,
    source_json_sha256: str,
    min_group_size: int,
    required_faults: Sequence[str],
    required_phases: Sequence[str],
    max_transmissions_values: Sequence[int],
    candidate_lifetime_values: Sequence[int],
    bundle_verification: Optional[Mapping[str, object]] = None,
    csv_verification: Optional[Mapping[str, object]] = None,
) -> Dict[str, object]:
    results = payload["results"]
    annotated = annotate_results(results)
    anomalies = trace_anomalies(results)
    aggregates = aggregate_results(annotated, min_group_size)
    coverage = coverage_audit(
        results,
        required_faults,
        required_phases,
        min_group_size,
    )
    sensitivity_rows, sensitivity_summary = run_sensitivity_scaffold(
        results,
        max_transmissions_values,
        candidate_lifetime_values,
    )

    return {
        "schema_version": "0.1.0",
        "status": PROVISIONAL_STATUS,
        "analysis_scope": "DESCRIPTIVE_AND_SENSITIVITY_SCAFFOLD_ONLY",
        "source": {
            "phase": "Phase 07",
            "result_count": len(results),
            "json_sha256": source_json_sha256,
            "bundle_verification": dict(bundle_verification or {}),
            "csv_verification": dict(csv_verification or {}),
        },
        "denominator_policy": {
            "minimum_descriptive_group_size": min_group_size,
            "fault_kind_and_phase_groups_overlap": True,
            "outcome_and_fault_count_groups_are_mutually_exclusive": True,
            "low_n_groups_are_retained_but_flagged": True,
        },
        "claim_boundary": {
            "causal_inference": "NOT_PERMITTED",
            "hypothesis_testing": "NOT_PERFORMED",
            "confidence_intervals": "NOT_PERFORMED",
            "treatment_effectiveness_claim": "NOT_PERMITTED",
            "post_compromise_security_claim": "NOT_PERMITTED",
        },
        "annotated_results": annotated,
        "aggregates": aggregates,
        "coverage_audit": coverage,
        "trace_anomalies": anomalies,
        "adverse_cases": adverse_cases(annotated),
        "sensitivity": {
            "status": "PROVISIONAL_UNFROZEN_GRID",
            "fixed_input": "serialized Phase 07 schedules",
            "varied_parameters": [
                "max_transmissions",
                "candidate_lifetime_contacts",
            ],
            "rows": sensitivity_rows,
            "summary": sensitivity_summary,
        },
    }


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("status\nNO_ROWS\n", encoding="utf-8")
        return
    fieldnames: List[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_analysis_outputs(
    analysis: Mapping[str, object],
    output_dir: Path,
) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "analysis_json": output_dir / "phase08-analysis.json",
        "annotated_results_csv": output_dir / "phase08-annotated-results.csv",
        "overall_summary_csv": output_dir / "phase08-overall-summary.csv",
        "outcome_summary_csv": output_dir / "phase08-outcome-summary.csv",
        "fault_kind_summary_csv": output_dir / "phase08-fault-kind-summary.csv",
        "fault_phase_summary_csv": output_dir / "phase08-fault-phase-summary.csv",
        "fault_count_summary_csv": output_dir / "phase08-fault-count-summary.csv",
        "security_availability_csv": output_dir / "phase08-security-availability.csv",
        "coverage_audit_csv": output_dir / "phase08-coverage-audit.csv",
        "trace_anomalies_csv": output_dir / "phase08-trace-anomalies.csv",
        "adverse_cases_csv": output_dir / "phase08-adverse-cases.csv",
        "sensitivity_rows_csv": output_dir / "phase08-sensitivity-rows.csv",
        "sensitivity_summary_csv": output_dir / "phase08-sensitivity-summary.csv",
    }

    paths["analysis_json"].write_text(
        json.dumps(analysis, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_csv(paths["annotated_results_csv"], analysis["annotated_results"])
    aggregates = analysis["aggregates"]
    _write_csv(paths["overall_summary_csv"], aggregates["overall"])
    _write_csv(paths["outcome_summary_csv"], aggregates["by_outcome"])
    _write_csv(paths["fault_kind_summary_csv"], aggregates["by_fault_kind"])
    _write_csv(paths["fault_phase_summary_csv"], aggregates["by_fault_phase"])
    _write_csv(paths["fault_count_summary_csv"], aggregates["by_fault_count"])
    _write_csv(
        paths["security_availability_csv"],
        aggregates["security_availability"],
    )
    _write_csv(paths["coverage_audit_csv"], analysis["coverage_audit"])
    _write_csv(paths["trace_anomalies_csv"], analysis["trace_anomalies"])
    _write_csv(paths["adverse_cases_csv"], analysis["adverse_cases"])
    _write_csv(paths["sensitivity_rows_csv"], analysis["sensitivity"]["rows"])
    _write_csv(
        paths["sensitivity_summary_csv"],
        analysis["sensitivity"]["summary"],
    )

    checksum_rows = []
    for name, path in sorted(paths.items()):
        checksum_rows.append(f"{sha256_file(path)}  {path.name}")
    checksum_path = output_dir / "phase08-derived-bundle.sha256"
    checksum_path.write_text("\n".join(checksum_rows) + "\n", encoding="utf-8")
    paths["checksum_manifest"] = checksum_path
    return {name: str(path) for name, path in paths.items()}


__all__ = [
    "PROVISIONAL_STATUS",
    "adverse_cases",
    "aggregate_results",
    "annotate_results",
    "build_analysis",
    "coverage_audit",
    "diagnostic_label",
    "load_phase07_results",
    "run_sensitivity_scaffold",
    "sha256_file",
    "trace_anomalies",
    "verify_checksum_manifest",
    "verify_metrics_csv",
    "write_analysis_outputs",
]
