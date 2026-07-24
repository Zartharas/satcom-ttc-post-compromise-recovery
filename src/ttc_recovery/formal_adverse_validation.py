from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

from .formal_cross_validation import (
    COMPARISON_FIELDS,
    TRACE_MATCH_STATUS,
    TRACE_MISMATCH_STATUS,
    compare_traces,
    normalize_formal_trace,
)
from .formal_execution import (
    COUNTEREXAMPLE_STATUS,
    NO_COUNTEREXAMPLE_STATUS,
    extract_counterexample_trace,
    parse_tlc_summary,
    run_command,
    sha1_file,
    sha256_file,
)
from .t1_controller import RecoveryAuthority, T1Endpoint, T1Session


ADVERSE_WITNESS_STATUS = "EXPECTED_ADVERSE_REACHABILITY_WITNESS_CAPTURED"
NOT_REACHED_STATUS = "NOT_REACHED_WITHIN_RECORDED_BOUND"
ABSTRACTION_GAP_STATUS = "ABSENT_FROM_CURRENT_TRANSITION_ASSIGNMENTS"


@dataclass(frozen=True)
class AdverseCase:
    case_id: str
    outcome: str
    property_name: str
    config_path: str
    expect_witness: bool
    expected_actions: tuple[str, ...] = ()


ADVERSE_CASES = (
    AdverseCase(
        "indeterminate",
        "INDETERMINATE",
        "ReachabilityWitnessNoIndeterminate",
        "formal/tla/adverse/IndeterminateWitness.cfg",
        True,
        (
            "Init",
            "Prepare",
            "SelectCandidate",
            "Commit",
            "Confirm",
            "AcceptCommand",
            "DropStatus",
        ),
    ),
    AdverseCase(
        "secure-degraded",
        "SECURE_DEGRADED",
        "ReachabilityWitnessNoSecureDegraded",
        "formal/tla/adverse/SecureDegradedWitness.cfg",
        True,
        (
            "Init",
            "Prepare",
            "SelectCandidate",
            "Commit",
            "Retry",
            "Retry",
            "ExpireAfterSpacecraftActivation",
        ),
    ),
    AdverseCase(
        "expired",
        "EXPIRED",
        "ReachabilityWitnessNoExpired",
        "formal/tla/adverse/ExpiredWitness.cfg",
        True,
        (
            "Init",
            "Prepare",
            "Retry",
            "Retry",
            "ExpireBeforeActivation",
        ),
    ),
    AdverseCase(
        "diverged",
        "DIVERGED",
        "ReachabilityWitnessNoDiverged",
        "formal/tla/adverse/DivergedAbsence.cfg",
        False,
    ),
    AdverseCase(
        "available-unsafe",
        "AVAILABLE_UNSAFE",
        "ReachabilityWitnessNoAvailableUnsafe",
        "formal/tla/adverse/AvailableUnsafeAbsence.cfg",
        False,
    ),
    AdverseCase(
        "locked",
        "LOCKED",
        "ReachabilityWitnessNoLocked",
        "formal/tla/adverse/LockedAbsence.cfg",
        False,
    ),
)

CAPTURED_CASES = tuple(case for case in ADVERSE_CASES if case.expect_witness)
ABSENT_CASES = tuple(case for case in ADVERSE_CASES if not case.expect_witness)


def _python_snapshot(
    session: T1Session,
    *,
    action: str,
    initial_ground_epoch: int,
    initial_space_epoch: int,
    candidate_epoch: int,
    attempts: int,
    receipt_evidence: bool,
    command_accepted: bool,
    status_seen: bool,
    status_dropped: bool,
    outcome: str,
) -> dict[str, object]:
    return {
        "action": action,
        "state": {
            "gMode": session.ground.mode.value,
            "sMode": session.spacecraft.mode.value,
            "gEpoch": session.ground.epoch,
            "sEpoch": session.spacecraft.epoch,
            "gPrevEpoch": initial_ground_epoch,
            "sPrevEpoch": initial_space_epoch,
            "candidateEpoch": candidate_epoch,
            "pending": session.ground.pending is not None,
            "receipt": receipt_evidence,
            "attempts": attempts,
            "activationCount": int(session.spacecraft.epoch != initial_space_epoch),
            "commandAccepted": command_accepted,
            "statusSeen": status_seen,
            "statusDropped": status_dropped,
            "verified": session.verification_complete,
            "outcome": outcome,
        },
    }


def replay_python_adverse(
    case: AdverseCase,
    actions: Sequence[str],
    *,
    initial_ground_epoch: int = 2,
    initial_space_epoch: int = 1,
    max_attempts: int = 3,
) -> list[dict[str, object]]:
    if not case.expect_witness:
        raise ValueError(f"Case {case.case_id} is an absence diagnostic, not a replay witness.")
    if tuple(actions) != case.expected_actions:
        raise ValueError(
            f"Unexpected {case.outcome} witness actions: {tuple(actions)!r}; "
            f"expected {case.expected_actions!r}."
        )

    session = T1Session(
        ground=T1Endpoint("ground", epoch=initial_ground_epoch, active_key=f"G{initial_ground_epoch}"),
        spacecraft=T1Endpoint(
            "spacecraft", epoch=initial_space_epoch, active_key=f"S{initial_space_epoch}"
        ),
        authority=RecoveryAuthority(),
        max_transmissions=max_attempts,
    )

    candidate_epoch = -1
    attempts = 0
    receipt_evidence = False
    command_accepted = False
    status_seen = False
    status_dropped = False
    outcome = "NONE"
    prepare = None
    commit = None
    confirm = None

    snapshots = [
        _python_snapshot(
            session,
            action="Init",
            initial_ground_epoch=initial_ground_epoch,
            initial_space_epoch=initial_space_epoch,
            candidate_epoch=candidate_epoch,
            attempts=attempts,
            receipt_evidence=receipt_evidence,
            command_accepted=command_accepted,
            status_seen=status_seen,
            status_dropped=status_dropped,
            outcome=outcome,
        )
    ]

    for action in actions[1:]:
        if action == "Prepare":
            prepare = session.start_recovery(f"phase12-{case.case_id}-witness")
            attempts = 1
        elif action == "SelectCandidate":
            if prepare is None:
                raise RuntimeError("Prepare must precede candidate selection.")
            response = session.spacecraft_accept_prepare(prepare)
            if response is None:
                raise RuntimeError("Python controller rejected the formal prepare witness.")
            commit = session.ground_accept_response(response)
            if commit is None:
                raise RuntimeError("Python controller rejected the formal response witness.")
            candidate_epoch = commit.target_epoch
        elif action == "Commit":
            if commit is None:
                raise RuntimeError("Candidate selection must precede commit.")
            confirm = session.spacecraft_accept_commit(commit)
            if confirm is None:
                raise RuntimeError("Python controller rejected the formal commit witness.")
            receipt_evidence = True
        elif action == "Confirm":
            if confirm is None or not session.ground_accept_confirm(confirm):
                raise RuntimeError("Python controller rejected the formal confirm witness.")
        elif action == "AcceptCommand":
            active = session.ground.active_key
            if not session.alignment_state().startswith("SYNC"):
                raise RuntimeError("Formal command witness reached Python before convergence.")
            if not session.candidate_can_authorize(session.spacecraft, active):
                raise RuntimeError("Formal command witness could not authorize in Python.")
            command_accepted = True
        elif action == "DropStatus":
            if not command_accepted:
                raise RuntimeError("Status-loss witness requires command acceptance.")
            if session.verify_recovery(drop_status=True):
                raise RuntimeError("Status-loss witness unexpectedly verified.")
            status_dropped = True
            outcome = session.outcome().value
        elif action == "Retry":
            if attempts >= max_attempts:
                raise RuntimeError("Formal retry exceeded the Python replay bound.")
            if commit is not None and session.spacecraft.activation_receipt is not None:
                session.retry_commit()
            elif prepare is not None:
                session.retry_prepare()
            else:
                raise RuntimeError("Retry witness has no pending Python message.")
            attempts += 1
        elif action == "ExpireBeforeActivation":
            session.expire_attempt()
            outcome = session.outcome().value
        elif action == "ExpireAfterSpacecraftActivation":
            if not receipt_evidence:
                raise RuntimeError("Post-activation expiry witness lacks activation evidence.")
            session.expire_attempt()
            outcome = session.outcome().value
        else:
            raise ValueError(f"Unsupported adverse witness action: {action}")

        snapshots.append(
            _python_snapshot(
                session,
                action=action,
                initial_ground_epoch=initial_ground_epoch,
                initial_space_epoch=initial_space_epoch,
                candidate_epoch=candidate_epoch,
                attempts=attempts,
                receipt_evidence=receipt_evidence,
                command_accepted=command_accepted,
                status_seen=status_seen,
                status_dropped=status_dropped,
                outcome=outcome,
            )
        )

    if outcome != case.outcome:
        raise RuntimeError(
            f"Python replay ended in {outcome}, expected adverse outcome {case.outcome}."
        )
    return snapshots


def count_outcome_assignments(spec_text: str, outcome: str) -> int:
    pattern = re.compile(rf"outcome'\s*=\s*\"{re.escape(outcome)}\"")
    return len(pattern.findall(spec_text))


def _tlc_command(
    *,
    java_command: str,
    jar_path: Path,
    config_path: Path,
    meta_dir: Path,
    spec_name: str,
) -> list[str]:
    return [
        java_command,
        "-XX:+UseParallelGC",
        "-cp",
        str(jar_path),
        "tlc2.TLC",
        "-workers",
        "1",
        "-config",
        str(config_path),
        "-metadir",
        str(meta_dir),
        spec_name,
    ]


def _write_csv(path: Path, rows: Sequence[dict[str, object]], fields: Sequence[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        for row in rows:
            rendered = {
                key: json.dumps(row.get(key), sort_keys=True)
                if isinstance(row.get(key), (dict, list, bool)) or row.get(key) is None
                else row.get(key)
                for key in fields
            }
            writer.writerow(rendered)


def _write_manifest(output_dir: Path, names: Iterable[str]) -> Path:
    manifest = output_dir / "phase12-derived-bundle.sha256"
    lines = [f"{sha256_file(output_dir / name)}  {name}" for name in sorted(names)]
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def execute_adverse_validation(
    *,
    jar_path: Path,
    output_dir: Path,
    repository_root: Path,
    expected_jar_sha1: str,
    tool_version: str,
    java_command: str = "java",
    timeout_seconds: int = 120,
) -> dict[str, object]:
    jar_path = jar_path.resolve()
    output_dir = output_dir.resolve()
    repository_root = repository_root.resolve()
    formal_dir = repository_root / "formal" / "tla"
    spec_path = formal_dir / "T1Recovery.tla"

    required_paths = [jar_path, spec_path]
    required_paths.extend(repository_root / case.config_path for case in ADVERSE_CASES)
    for required in required_paths:
        if not required.is_file():
            raise FileNotFoundError(required)

    actual_sha1 = sha1_file(jar_path)
    if actual_sha1.lower() != expected_jar_sha1.lower():
        raise ValueError(
            f"tla2tools.jar SHA-1 mismatch: expected {expected_jar_sha1}, got {actual_sha1}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    java_version = run_command(
        [java_command, "-version"], cwd=formal_dir, timeout_seconds=timeout_seconds
    )
    sany = run_command(
        [java_command, "-cp", str(jar_path), "tla2sany.SANY", spec_path.name],
        cwd=formal_dir,
        timeout_seconds=timeout_seconds,
    )
    spec_text = spec_path.read_text(encoding="utf-8")

    logs: dict[str, str] = {
        "phase12-java-version.log": java_version.output,
        "phase12-sany.log": sany.output,
    }
    witness_records: list[dict[str, object]] = []
    absence_rows: list[dict[str, object]] = []
    derived_names: list[str] = []
    all_captured_match = True
    all_absence_checks_pass = True

    for case in ADVERSE_CASES:
        config_path = repository_root / case.config_path
        meta_dir = output_dir / f"tlc-meta-{case.case_id}"
        meta_dir.mkdir(exist_ok=True)
        result = run_command(
            _tlc_command(
                java_command=java_command,
                jar_path=jar_path,
                config_path=config_path,
                meta_dir=meta_dir,
                spec_name=spec_path.name,
            ),
            cwd=formal_dir,
            timeout_seconds=timeout_seconds,
        )
        summary = parse_tlc_summary(result.output, result.returncode)
        trace_raw = extract_counterexample_trace(result.output)
        log_name = f"phase12-tlc-{case.case_id}.log"
        logs[log_name] = result.output

        assignment_count = count_outcome_assignments(spec_text, case.outcome)
        if case.expect_witness:
            formal_trace = normalize_formal_trace(trace_raw)
            formal_actions = [str(row["action"]) for row in formal_trace]
            python_trace: list[dict[str, object]] = []
            comparison_rows: list[dict[str, object]] = []
            comparison_summary = {
                "comparison_rows": 0,
                "matched_rows": 0,
                "mismatch_count": 0,
            }
            replay_error = None
            try:
                python_trace = replay_python_adverse(case, formal_actions)
                comparison_rows, comparison_summary = compare_traces(formal_trace, python_trace)
            except Exception as exc:  # retained in the output before the final gate fails
                replay_error = f"{type(exc).__name__}: {exc}"

            witness_ok = (
                summary.status == COUNTEREXAMPLE_STATUS
                and summary.violated_invariant == case.property_name
                and tuple(formal_actions) == case.expected_actions
                and bool(trace_raw)
            )
            trace_match = replay_error is None and comparison_summary["mismatch_count"] == 0
            all_captured_match = all_captured_match and witness_ok and trace_match

            witness_record = {
                "schema_version": "0.1.0",
                "case_id": case.case_id,
                "outcome": case.outcome,
                "status": ADVERSE_WITNESS_STATUS if witness_ok else TRACE_MISMATCH_STATUS,
                "trace_comparison_status": (
                    TRACE_MATCH_STATUS if trace_match else TRACE_MISMATCH_STATUS
                ),
                "testing_role": "INTENTIONAL_ADVERSE_OUTCOME_REACHABILITY_WITNESS",
                "violated_invariant": summary.violated_invariant,
                "trace_state_count": len(trace_raw),
                "actions": formal_actions,
                "formal_trace": formal_trace,
                "python_trace": python_trace,
                "comparison_summary": comparison_summary,
                "replay_error": replay_error,
                "outcome_assignment_count": assignment_count,
                "mapping_boundary": (
                    "The formal receipt field is projected as retained activation evidence. The Python "
                    "controller may clear its live receipt object during terminal cleanup. This declared "
                    "evidence projection is not an implementation-equivalence claim."
                ),
            }
            witness_name = f"phase12-witness-{case.case_id}.json"
            (output_dir / witness_name).write_text(
                json.dumps(witness_record, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            derived_names.append(witness_name)

            comparison_name = f"phase12-comparison-{case.case_id}.csv"
            _write_csv(
                output_dir / comparison_name,
                comparison_rows,
                ("step", "action", "field", "formal_value", "python_value", "match"),
            )
            derived_names.append(comparison_name)
            witness_records.append(
                {
                    "case_id": case.case_id,
                    "outcome": case.outcome,
                    "status": witness_record["status"],
                    "trace_comparison_status": witness_record["trace_comparison_status"],
                    "trace_state_count": len(trace_raw),
                    "actions": formal_actions,
                    **comparison_summary,
                    "generated_states": summary.generated_states,
                    "distinct_states": summary.distinct_states,
                    "search_depth": summary.search_depth,
                    "replay_error": replay_error,
                }
            )
        else:
            no_witness = summary.status == NO_COUNTEREXAMPLE_STATUS and not trace_raw
            abstraction_gap = assignment_count == 0
            all_absence_checks_pass = (
                all_absence_checks_pass and no_witness and abstraction_gap
            )
            absence_rows.append(
                {
                    "case_id": case.case_id,
                    "outcome": case.outcome,
                    "status": NOT_REACHED_STATUS if no_witness else TRACE_MISMATCH_STATUS,
                    "diagnosis": (
                        ABSTRACTION_GAP_STATUS
                        if abstraction_gap
                        else "TRANSITION_ASSIGNMENT_PRESENT_REQUIRES_REVIEW"
                    ),
                    "outcome_assignment_count": assignment_count,
                    "generated_states": summary.generated_states,
                    "distinct_states": summary.distinct_states,
                    "queued_states": summary.queued_states,
                    "search_depth": summary.search_depth,
                    "interpretation": (
                        "No witness was found in the recorded finite configuration. The outcome is not "
                        "assigned by any current transition, so this is an abstraction-coverage gap, not "
                        "an impossibility result."
                    ),
                }
            )

    for name, content in logs.items():
        (output_dir / name).write_text(content, encoding="utf-8")
    derived_names.extend(logs.keys())

    absence_name = "phase12-unreached-outcomes.csv"
    _write_csv(
        output_dir / absence_name,
        absence_rows,
        (
            "case_id",
            "outcome",
            "status",
            "diagnosis",
            "outcome_assignment_count",
            "generated_states",
            "distinct_states",
            "queued_states",
            "search_depth",
            "interpretation",
        ),
    )
    derived_names.append(absence_name)

    overall_ok = sany.returncode == 0 and all_captured_match and all_absence_checks_pass
    report = {
        "schema_version": "0.1.0",
        "phase": "Phase 12",
        "status": TRACE_MATCH_STATUS if overall_ok else TRACE_MISMATCH_STATUS,
        "claim_status": "PROVISIONAL_INTERNAL_REVIEW_ONLY",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "toolchain": {
            "tool_version": tool_version,
            "jar_sha1": actual_sha1,
            "jar_sha256": sha256_file(jar_path),
            "java_version_output": java_version.output.strip(),
            "worker_count": 1,
        },
        "inputs": {
            "spec": str(spec_path.relative_to(repository_root)),
            "spec_sha256": sha256_file(spec_path),
            "configs": [
                {
                    "case_id": case.case_id,
                    "outcome": case.outcome,
                    "expect_witness": case.expect_witness,
                    "path": case.config_path,
                    "sha256": sha256_file(repository_root / case.config_path),
                }
                for case in ADVERSE_CASES
            ],
        },
        "sany_status": "PARSE_SUCCESS" if sany.returncode == 0 else "PARSE_FAILURE",
        "captured_adverse_witnesses": witness_records,
        "unreached_outcomes": absence_rows,
        "captured_case_count": len(witness_records),
        "absence_case_count": len(absence_rows),
        "mapping_boundary": (
            "Every captured witness is replayed through Python under the declared 16-field projection. "
            "A match is not a refinement proof or implementation-equivalence result."
        ),
        "absence_boundary": (
            "DIVERGED, AVAILABLE_UNSAFE, and LOCKED are not assigned by any current TLA+ transition. "
            "Their bounded absence therefore identifies an abstraction gap and does not establish "
            "impossibility."
        ),
        "formal_model_completeness_claim": "NOT_PERMITTED",
        "implementation_equivalence_claim": "NOT_PERMITTED",
        "cryptographic_security_claim": "NOT_PERMITTED",
        "publication_evidence_status": "NOT_PERMITTED",
    }
    report_name = "phase12-adverse-outcome-validation.json"
    (output_dir / report_name).write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    derived_names.append(report_name)
    _write_manifest(output_dir, derived_names)

    if not overall_ok:
        raise RuntimeError(
            "Phase 12 adverse witness replay or abstraction-gap diagnosis did not pass."
        )
    return report


__all__ = [
    "ABSTRACTION_GAP_STATUS",
    "ABSENT_CASES",
    "ADVERSE_CASES",
    "ADVERSE_WITNESS_STATUS",
    "CAPTURED_CASES",
    "NOT_REACHED_STATUS",
    "AdverseCase",
    "count_outcome_assignments",
    "execute_adverse_validation",
    "replay_python_adverse",
]
