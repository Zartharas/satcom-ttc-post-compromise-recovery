from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

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


TRACE_MATCH_STATUS = "MATCH_WITHIN_DECLARED_ABSTRACTION"
TRACE_MISMATCH_STATUS = "MISMATCH_REQUIRES_REVIEW"
SUCCESS_WITNESS_STATUS = "EXPECTED_SUCCESS_REACHABILITY_WITNESS_CAPTURED"
EXPECTED_SUCCESS_PROPERTY = "ReachabilityWitnessNoSuccess"

EXPECTED_ACTIONS = (
    "Init",
    "Prepare",
    "SelectCandidate",
    "Commit",
    "Confirm",
    "AcceptCommand",
    "ReceiveStatus",
    "Verify",
)

COMPARISON_FIELDS = (
    "gMode",
    "sMode",
    "gEpoch",
    "sEpoch",
    "gPrevEpoch",
    "sPrevEpoch",
    "candidateEpoch",
    "pending",
    "receipt",
    "attempts",
    "activationCount",
    "commandAccepted",
    "statusSeen",
    "statusDropped",
    "verified",
    "outcome",
)


@dataclass(frozen=True)
class BoundCase:
    case_id: str
    config_path: str
    max_attempts: int
    max_epoch: int


BOUND_CASES = (
    BoundCase("attempts-1", "formal/tla/bounds/Attempts1.cfg", 1, 6),
    BoundCase("base-3-6", "formal/tla/MC.cfg", 3, 6),
    BoundCase("attempts-5", "formal/tla/bounds/Attempts5.cfg", 5, 6),
    BoundCase("epoch-4", "formal/tla/bounds/Epoch4.cfg", 3, 4),
    BoundCase("epoch-8", "formal/tla/bounds/Epoch8.cfg", 3, 8),
)

BASELINE_COUNTS = {
    "generated_states": 50,
    "distinct_states": 28,
    "queued_states": 0,
    "search_depth": 10,
}


def decode_tla_scalar(raw: str) -> object:
    value = raw.strip()
    if value == "TRUE":
        return True
    if value == "FALSE":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    return value


def action_from_label(label: str) -> str:
    if label == "<Initial predicate>":
        return "Init"
    match = re.match(r"<([A-Za-z][A-Za-z0-9_]*)\b", label)
    return match.group(1) if match else "UNKNOWN"


def normalize_formal_trace(trace: Sequence[dict[str, object]]) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []
    for row in trace:
        assignments = row.get("assignments", {})
        if not isinstance(assignments, dict):
            raise TypeError("Formal trace assignments must be a mapping.")
        state = {
            field: decode_tla_scalar(str(assignments[field]))
            for field in COMPARISON_FIELDS
            if field in assignments
        }
        normalized.append(
            {
                "step": int(row["state_number"]),
                "action": action_from_label(str(row["label"])),
                "state": state,
            }
        )
    return normalized


def _python_snapshot(
    session: T1Session,
    *,
    action: str,
    initial_ground_epoch: int,
    initial_space_epoch: int,
    candidate_epoch: int,
    attempts: int,
    command_accepted: bool,
    status_seen: bool,
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
            "receipt": session.spacecraft.activation_receipt is not None,
            "attempts": attempts,
            "activationCount": int(session.spacecraft.epoch != initial_space_epoch),
            "commandAccepted": command_accepted,
            "statusSeen": status_seen,
            "statusDropped": False,
            "verified": session.verification_complete,
            "outcome": outcome,
        },
    }


def replay_python_success(
    actions: Sequence[str],
    *,
    initial_ground_epoch: int = 2,
    initial_space_epoch: int = 1,
    max_attempts: int = 3,
) -> list[dict[str, object]]:
    if tuple(actions) != EXPECTED_ACTIONS:
        raise ValueError(
            f"Unexpected success witness actions: {tuple(actions)!r}; expected {EXPECTED_ACTIONS!r}."
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
    command_accepted = False
    status_seen = False
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
            command_accepted=command_accepted,
            status_seen=status_seen,
            outcome=outcome,
        )
    ]

    for action in actions[1:]:
        if action == "Prepare":
            prepare = session.start_recovery("phase11-success-witness")
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
        elif action == "ReceiveStatus":
            if not command_accepted:
                raise RuntimeError("Status witness requires command acceptance.")
            status_seen = True
        elif action == "Verify":
            if not command_accepted or not status_seen:
                raise RuntimeError("Verification witness lacks command or status evidence.")
            if not session.verify_recovery():
                raise RuntimeError("Python controller failed the formal verification witness.")
            outcome = session.outcome().value
        else:
            raise ValueError(f"Unsupported formal witness action: {action}")

        snapshots.append(
            _python_snapshot(
                session,
                action=action,
                initial_ground_epoch=initial_ground_epoch,
                initial_space_epoch=initial_space_epoch,
                candidate_epoch=candidate_epoch,
                attempts=attempts,
                command_accepted=command_accepted,
                status_seen=status_seen,
                outcome=outcome,
            )
        )

    return snapshots


def compare_traces(
    formal_trace: Sequence[dict[str, object]],
    python_trace: Sequence[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, int]]:
    rows: list[dict[str, object]] = []
    max_steps = max(len(formal_trace), len(python_trace))

    for index in range(max_steps):
        formal = formal_trace[index] if index < len(formal_trace) else None
        python = python_trace[index] if index < len(python_trace) else None
        formal_action = formal.get("action") if formal else None
        python_action = python.get("action") if python else None
        action_match = formal_action == python_action
        rows.append(
            {
                "step": index + 1,
                "action": formal_action or python_action or "MISSING",
                "field": "__action__",
                "formal_value": formal_action,
                "python_value": python_action,
                "match": action_match,
            }
        )

        formal_state = formal.get("state", {}) if formal else {}
        python_state = python.get("state", {}) if python else {}
        for field in COMPARISON_FIELDS:
            formal_value = formal_state.get(field) if isinstance(formal_state, dict) else None
            python_value = python_state.get(field) if isinstance(python_state, dict) else None
            rows.append(
                {
                    "step": index + 1,
                    "action": formal_action or python_action or "MISSING",
                    "field": field,
                    "formal_value": formal_value,
                    "python_value": python_value,
                    "match": formal_value == python_value,
                }
            )

    mismatch_count = sum(not bool(row["match"]) for row in rows)
    return rows, {
        "comparison_rows": len(rows),
        "matched_rows": len(rows) - mismatch_count,
        "mismatch_count": mismatch_count,
    }


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
    manifest = output_dir / "phase11-derived-bundle.sha256"
    lines = [f"{sha256_file(output_dir / name)}  {name}" for name in sorted(names)]
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def execute_cross_validation(
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
    witness_config = formal_dir / "SuccessWitness.cfg"

    required_paths = [jar_path, spec_path, witness_config]
    required_paths.extend(repository_root / case.config_path for case in BOUND_CASES)
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

    witness_meta = output_dir / "tlc-meta-success-witness"
    witness_meta.mkdir(exist_ok=True)
    witness_result = run_command(
        _tlc_command(
            java_command=java_command,
            jar_path=jar_path,
            config_path=witness_config,
            meta_dir=witness_meta,
            spec_name=spec_path.name,
        ),
        cwd=formal_dir,
        timeout_seconds=timeout_seconds,
    )
    witness_summary = parse_tlc_summary(witness_result.output, witness_result.returncode)
    witness_trace_raw = extract_counterexample_trace(witness_result.output)
    formal_trace = normalize_formal_trace(witness_trace_raw)
    formal_actions = [str(row["action"]) for row in formal_trace]

    python_trace: list[dict[str, object]] = []
    comparison_rows: list[dict[str, object]] = []
    comparison_summary = {"comparison_rows": 0, "matched_rows": 0, "mismatch_count": 0}
    replay_error = None
    try:
        python_trace = replay_python_success(formal_actions)
        comparison_rows, comparison_summary = compare_traces(formal_trace, python_trace)
    except Exception as exc:  # captured as evidence before the final gate fails
        replay_error = f"{type(exc).__name__}: {exc}"

    bound_rows: list[dict[str, object]] = []
    logs: dict[str, str] = {
        "phase11-java-version.log": java_version.output,
        "phase11-sany.log": sany.output,
        "phase11-tlc-success-witness.log": witness_result.output,
    }

    for case in BOUND_CASES:
        config_path = repository_root / case.config_path
        meta_dir = output_dir / f"tlc-meta-bound-{case.case_id}"
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
        bound_rows.append(
            {
                "case_id": case.case_id,
                "config_path": case.config_path,
                "max_attempts": case.max_attempts,
                "max_epoch": case.max_epoch,
                "status": summary.status,
                "returncode": result.returncode,
                "generated_states": summary.generated_states,
                "distinct_states": summary.distinct_states,
                "queued_states": summary.queued_states,
                "search_depth": summary.search_depth,
            }
        )
        logs[f"phase11-tlc-bound-{case.case_id}.log"] = result.output

    for name, content in logs.items():
        (output_dir / name).write_text(content, encoding="utf-8")

    witness_ok = (
        witness_summary.status == COUNTEREXAMPLE_STATUS
        and witness_summary.violated_invariant == EXPECTED_SUCCESS_PROPERTY
        and tuple(formal_actions) == EXPECTED_ACTIONS
        and bool(witness_trace_raw)
    )
    trace_match = replay_error is None and comparison_summary["mismatch_count"] == 0
    bounds_ok = all(row["status"] == NO_COUNTEREXAMPLE_STATUS for row in bound_rows)
    base_row = next(row for row in bound_rows if row["case_id"] == "base-3-6")
    baseline_reproduced = all(base_row[key] == value for key, value in BASELINE_COUNTS.items())
    overall_status = (
        TRACE_MATCH_STATUS
        if sany.returncode == 0 and witness_ok and trace_match and bounds_ok and baseline_reproduced
        else TRACE_MISMATCH_STATUS
    )

    witness_record = {
        "schema_version": "0.1.0",
        "status": SUCCESS_WITNESS_STATUS if witness_ok else TRACE_MISMATCH_STATUS,
        "testing_role": "INTENTIONAL_SUCCESS_REACHABILITY_WITNESS",
        "violated_invariant": witness_summary.violated_invariant,
        "trace_state_count": len(witness_trace_raw),
        "actions": formal_actions,
        "formal_trace": formal_trace,
        "python_trace": python_trace,
        "replay_error": replay_error,
        "interpretation_boundary": (
            "The false witness invariant is used only to obtain a shortest bounded SUCCESS path for "
            "cross-validation; it is not a protocol property or a security claim."
        ),
    }
    witness_name = "phase11-success-witness.json"
    (output_dir / witness_name).write_text(
        json.dumps(witness_record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    comparison_name = "phase11-trace-comparison.csv"
    _write_csv(
        output_dir / comparison_name,
        comparison_rows,
        ("step", "action", "field", "formal_value", "python_value", "match"),
    )

    bounds_name = "phase11-bound-expansion.csv"
    _write_csv(
        output_dir / bounds_name,
        bound_rows,
        (
            "case_id",
            "config_path",
            "max_attempts",
            "max_epoch",
            "status",
            "returncode",
            "generated_states",
            "distinct_states",
            "queued_states",
            "search_depth",
        ),
    )

    report = {
        "schema_version": "0.1.0",
        "phase": "Phase 11",
        "status": overall_status,
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
            "success_witness_config": str(witness_config.relative_to(repository_root)),
            "success_witness_config_sha256": sha256_file(witness_config),
            "bound_configs": [
                {
                    "case_id": case.case_id,
                    "path": case.config_path,
                    "sha256": sha256_file(repository_root / case.config_path),
                }
                for case in BOUND_CASES
            ],
        },
        "sany_status": "PARSE_SUCCESS" if sany.returncode == 0 else "PARSE_FAILURE",
        "success_witness": {
            "status": witness_record["status"],
            "trace_state_count": len(witness_trace_raw),
            "actions": formal_actions,
            "generated_states": witness_summary.generated_states,
            "distinct_states": witness_summary.distinct_states,
            "search_depth": witness_summary.search_depth,
        },
        "trace_comparison": {
            "status": TRACE_MATCH_STATUS if trace_match else TRACE_MISMATCH_STATUS,
            **comparison_summary,
            "mapping_granularity": (
                "SelectCandidate maps to Python prepare acceptance plus response acceptance; "
                "AcceptCommand and ReceiveStatus are projected as evidence substeps before the "
                "Python verification call."
            ),
            "replay_error": replay_error,
        },
        "bound_expansion": {
            "status": NO_COUNTEREXAMPLE_STATUS if bounds_ok else TRACE_MISMATCH_STATUS,
            "case_count": len(bound_rows),
            "baseline_reproduced": baseline_reproduced,
            "baseline_expected": BASELINE_COUNTS,
            "cases": bound_rows,
        },
        "review_boundary": (
            "Trace agreement is limited to the declared abstract projection and finite configurations. "
            "It does not prove implementation equivalence, cryptographic security, or completeness."
        ),
        "publication_evidence_status": "NOT_PERMITTED",
    }
    report_name = "phase11-cross-validation.json"
    (output_dir / report_name).write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    derived_names = [report_name, witness_name, comparison_name, bounds_name, *logs.keys()]
    _write_manifest(output_dir, derived_names)

    if overall_status != TRACE_MATCH_STATUS:
        raise RuntimeError(
            "Phase 11 formal/Python trace cross-validation or bound expansion did not pass."
        )
    return report


__all__ = [
    "BASELINE_COUNTS",
    "BOUND_CASES",
    "COMPARISON_FIELDS",
    "EXPECTED_ACTIONS",
    "SUCCESS_WITNESS_STATUS",
    "TRACE_MATCH_STATUS",
    "TRACE_MISMATCH_STATUS",
    "action_from_label",
    "compare_traces",
    "decode_tla_scalar",
    "execute_cross_validation",
    "normalize_formal_trace",
    "replay_python_success",
]
