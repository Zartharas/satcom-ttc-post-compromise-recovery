from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

from .formal_adverse_validation import count_outcome_assignments
from .formal_cross_validation import (
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
from .simulator import (
    B2CompromiseScope,
    Endpoint,
    Outcome,
    Simulation,
    b1_triple_kem,
    b2_urke_strict,
)


EXPANSION_WITNESS_STATUS = "EXPECTED_ABSTRACTION_GAP_WITNESS_CAPTURED"
BASELINE_PRESERVED_STATUS = "BASELINE_PRESERVED"
EXPANSION_DIAGNOSTIC_STATUS = "EXPANDED_OUTCOME_POPULATION_DIAGNOSTIC_ONLY"
BASELINE_SPEC_SHA256 = "c2a97fa0eb93b7b84a2109be67d673a0199b82e52b8baf67f16d5b137e0da754"
BASELINE_COUNTS = {
    "generated_states": 50,
    "distinct_states": 28,
    "queued_states": 0,
    "search_depth": 10,
}


@dataclass(frozen=True)
class ExpansionCase:
    case_id: str
    outcome: str
    property_name: str
    expansion_config_path: str
    baseline_config_path: str
    expected_actions: tuple[str, ...]
    initial_ground_epoch: int
    initial_space_epoch: int
    expected_gap_cause: str
    canonical_scenario: str


EXPANSION_CASES = (
    ExpansionCase(
        "diverged",
        "DIVERGED",
        "ReachabilityWitnessNoExpandedDiverged",
        "formal/tla/expansion/DivergedWitness.cfg",
        "formal/tla/adverse/DivergedAbsence.cfg",
        (
            "Init",
            "PrepareExpanded",
            "SelectCandidateExpanded",
            "DivergeOnConfirmLoss",
        ),
        2,
        1,
        "CONFIRM_LOSS",
        "B1_CONFIRM_LOSS_LOCAL_COMPLETION",
    ),
    ExpansionCase(
        "available-unsafe",
        "AVAILABLE_UNSAFE",
        "ReachabilityWitnessNoExpandedAvailableUnsafe",
        "formal/tla/expansion/AvailableUnsafeWitness.cfg",
        "formal/tla/adverse/AvailableUnsafeAbsence.cfg",
        (
            "Init",
            "PrepareExpanded",
            "SelectCandidateExpanded",
            "MarkCandidateKnown",
            "CommitExpanded",
            "ConfirmExpanded",
            "VerifyAvailableUnsafe",
        ),
        1,
        1,
        "CANDIDATE_KNOWN",
        "B2_RECEIVER_STATE_EXPOSURE",
    ),
    ExpansionCase(
        "locked",
        "LOCKED",
        "ReachabilityWitnessNoExpandedLocked",
        "formal/tla/expansion/LockedWitness.cfg",
        "formal/tla/adverse/LockedAbsence.cfg",
        (
            "Init",
            "PrepareExpanded",
            "SelectCandidateExpanded",
            "MarkSenderStateDeleted",
            "LockAfterSenderAdvance",
        ),
        1,
        1,
        "SENDER_STATE_DELETED",
        "B2_DROPPED_UPDATE_AFTER_SENDER_EVOLUTION",
    ),
)


def _snapshot(
    sim: Simulation,
    *,
    action: str,
    g_mode: str,
    s_mode: str,
    g_prev_epoch: int,
    s_prev_epoch: int,
    candidate_epoch: int,
    pending: bool,
    receipt: bool,
    attempts: int,
    activation_count: int,
    command_accepted: bool,
    status_seen: bool,
    status_dropped: bool,
    verified: bool,
    outcome: str,
) -> dict[str, object]:
    return {
        "action": action,
        "state": {
            "gMode": g_mode,
            "sMode": s_mode,
            "gEpoch": sim.ground.epoch,
            "sEpoch": sim.spacecraft.epoch,
            "gPrevEpoch": g_prev_epoch,
            "sPrevEpoch": s_prev_epoch,
            "candidateEpoch": candidate_epoch,
            "pending": pending,
            "receipt": receipt,
            "attempts": attempts,
            "activationCount": activation_count,
            "commandAccepted": command_accepted,
            "statusSeen": status_seen,
            "statusDropped": status_dropped,
            "verified": verified,
            "outcome": outcome,
        },
    }


def canonical_baseline_outcome(case: ExpansionCase) -> dict[str, object]:
    sim = Simulation(f"phase13-canonical-{case.case_id}")
    if case.case_id == "diverged":
        b1_triple_kem(sim, drop_confirm=True)
    elif case.case_id == "available-unsafe":
        b2_urke_strict(sim, compromise_scope=B2CompromiseScope.RECEIVER_STATE)
    elif case.case_id == "locked":
        b2_urke_strict(sim, drop_update=True)
    else:
        raise ValueError(f"Unsupported Phase 13 canonical case: {case.case_id}")
    sim.check_invariants()
    return {
        "scenario": case.canonical_scenario,
        "outcome": sim.evaluate().value,
        "alignment": sim.alignment_state(),
        "joint_state": sim.joint_state(),
        "event_names": [str(row["event"]) for row in sim.event_log],
    }


def replay_python_expansion(
    case: ExpansionCase,
    actions: Sequence[str],
) -> tuple[list[dict[str, object]], str]:
    if tuple(actions) != case.expected_actions:
        raise ValueError(
            f"Unexpected {case.outcome} expansion actions: {tuple(actions)!r}; "
            f"expected {case.expected_actions!r}."
        )

    same_initial = case.initial_ground_epoch == case.initial_space_epoch
    shared_key = f"K{case.initial_ground_epoch}"
    ground_key = shared_key if same_initial else f"G{case.initial_ground_epoch}"
    space_key = shared_key if same_initial else f"S{case.initial_space_epoch}"
    sim = Simulation(
        f"phase13-{case.case_id}-replay",
        ground=Endpoint("ground", epoch=case.initial_ground_epoch, active_key=ground_key),
        spacecraft=Endpoint("spacecraft", epoch=case.initial_space_epoch, active_key=space_key),
    )

    g_mode = "NORMAL"
    s_mode = "NORMAL"
    g_prev_epoch = case.initial_ground_epoch
    s_prev_epoch = case.initial_space_epoch
    candidate_epoch = -1
    candidate_key = ""
    pending = False
    receipt = False
    attempts = 0
    activation_count = 0
    command_accepted = False
    status_seen = False
    status_dropped = False
    verified = False
    outcome = "NONE"
    gap_cause = "NONE"

    snapshots = [
        _snapshot(
            sim,
            action="Init",
            g_mode=g_mode,
            s_mode=s_mode,
            g_prev_epoch=g_prev_epoch,
            s_prev_epoch=s_prev_epoch,
            candidate_epoch=candidate_epoch,
            pending=pending,
            receipt=receipt,
            attempts=attempts,
            activation_count=activation_count,
            command_accepted=command_accepted,
            status_seen=status_seen,
            status_dropped=status_dropped,
            verified=verified,
            outcome=outcome,
        )
    ]

    for action in actions[1:]:
        if action == "PrepareExpanded":
            g_mode = "RECOVERING"
            pending = True
            attempts = 1
        elif action == "SelectCandidateExpanded":
            if not pending:
                raise RuntimeError("Candidate selection requires a pending diagnostic recovery.")
            candidate_epoch = max(sim.ground.epoch, sim.spacecraft.epoch) + 1
            candidate_key = f"PX{candidate_epoch}"
            sim.ground.stage(candidate_epoch, candidate_key)
            sim.spacecraft.stage(candidate_epoch, candidate_key)
            g_mode = "CANDIDATE"
            s_mode = "CANDIDATE"
        elif action == "MarkCandidateKnown":
            if not candidate_key:
                raise RuntimeError("Candidate exposure requires an existing candidate.")
            sim.ground.attacker_known_keys.add(candidate_key)
            sim.spacecraft.attacker_known_keys.add(candidate_key)
            gap_cause = "CANDIDATE_KNOWN"
        elif action == "MarkSenderStateDeleted":
            if not candidate_key:
                raise RuntimeError("Sender-state deletion requires an existing candidate.")
            gap_cause = "SENDER_STATE_DELETED"
        elif action == "CommitExpanded":
            if not candidate_key:
                raise RuntimeError("Commit requires an existing candidate.")
            s_prev_epoch = sim.spacecraft.epoch
            sim.spacecraft.activate(candidate_epoch, candidate_key)
            s_mode = "ACTIVATED"
            receipt = True
            activation_count = 1
        elif action == "ConfirmExpanded":
            if not receipt:
                raise RuntimeError("Confirmation requires spacecraft activation evidence.")
            g_prev_epoch = sim.ground.epoch
            sim.ground.activate(candidate_epoch, candidate_key)
            g_mode = "ACTIVATED"
            pending = False
        elif action == "DivergeOnConfirmLoss":
            if not candidate_key:
                raise RuntimeError("Confirmation-loss divergence requires an existing candidate.")
            g_prev_epoch = sim.ground.epoch
            sim.ground.activate(candidate_epoch, candidate_key)
            sim.spacecraft.expire_pending()
            g_mode = "NORMAL"
            s_mode = "EXPIRED"
            pending = False
            gap_cause = "CONFIRM_LOSS"
            outcome = sim.evaluate().value
        elif action == "VerifyAvailableUnsafe":
            if gap_cause != "CANDIDATE_KNOWN":
                raise RuntimeError("Unsafe verification requires an adversary-known candidate.")
            g_mode = "VERIFIED"
            s_mode = "VERIFIED"
            receipt = False
            command_accepted = True
            status_seen = True
            verified = True
            sim.verification_complete = True
            outcome = sim.evaluate().value
        elif action == "LockAfterSenderAdvance":
            if gap_cause != "SENDER_STATE_DELETED":
                raise RuntimeError("Terminal lock requires explicit prior sender-state deletion.")
            g_prev_epoch = sim.ground.epoch
            sim.ground.activate(candidate_epoch, candidate_key)
            sim.lockout_reason = (
                "sender advanced after prior state deletion while the receiver retained the old epoch"
            )
            g_mode = "NORMAL"
            pending = False
            outcome = sim.evaluate().value
        else:
            raise ValueError(f"Unsupported Phase 13 witness action: {action}")

        sim.check_invariants()
        snapshots.append(
            _snapshot(
                sim,
                action=action,
                g_mode=g_mode,
                s_mode=s_mode,
                g_prev_epoch=g_prev_epoch,
                s_prev_epoch=s_prev_epoch,
                candidate_epoch=candidate_epoch,
                pending=pending,
                receipt=receipt,
                attempts=attempts,
                activation_count=activation_count,
                command_accepted=command_accepted,
                status_seen=status_seen,
                status_dropped=status_dropped,
                verified=verified,
                outcome=outcome,
            )
        )

    if outcome != case.outcome:
        raise RuntimeError(f"Python expansion replay ended in {outcome}, expected {case.outcome}.")
    if gap_cause != case.expected_gap_cause:
        raise RuntimeError(
            f"Python expansion replay ended with cause {gap_cause}, "
            f"expected {case.expected_gap_cause}."
        )
    return snapshots, gap_cause


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
    manifest = output_dir / "phase13-derived-bundle.sha256"
    lines = [f"{sha256_file(output_dir / name)}  {name}" for name in sorted(names)]
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def execute_outcome_expansion(
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
    baseline_spec = formal_dir / "T1Recovery.tla"
    expanded_spec = formal_dir / "T1RecoveryOutcomeExpansion.tla"

    required_paths = [jar_path, baseline_spec, expanded_spec]
    for case in EXPANSION_CASES:
        required_paths.append(repository_root / case.baseline_config_path)
        required_paths.append(repository_root / case.expansion_config_path)
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
    sany_baseline = run_command(
        [java_command, "-cp", str(jar_path), "tla2sany.SANY", baseline_spec.name],
        cwd=formal_dir,
        timeout_seconds=timeout_seconds,
    )
    sany_expanded = run_command(
        [java_command, "-cp", str(jar_path), "tla2sany.SANY", expanded_spec.name],
        cwd=formal_dir,
        timeout_seconds=timeout_seconds,
    )

    baseline_text = baseline_spec.read_text(encoding="utf-8")
    expanded_text = expanded_spec.read_text(encoding="utf-8")
    baseline_hash_matches = sha256_file(baseline_spec) == BASELINE_SPEC_SHA256

    logs: dict[str, str] = {
        "phase13-java-version.log": java_version.output,
        "phase13-sany-baseline.log": sany_baseline.output,
        "phase13-sany-expanded.log": sany_expanded.output,
    }
    baseline_rows: list[dict[str, object]] = []
    assignment_rows: list[dict[str, object]] = []
    witness_rows: list[dict[str, object]] = []
    derived_names: list[str] = []
    baseline_ok = baseline_hash_matches and sany_baseline.returncode == 0
    expansion_ok = sany_expanded.returncode == 0

    for case in EXPANSION_CASES:
        baseline_config = repository_root / case.baseline_config_path
        baseline_meta = output_dir / f"tlc-meta-baseline-{case.case_id}"
        baseline_meta.mkdir(exist_ok=True)
        baseline_result = run_command(
            _tlc_command(
                java_command=java_command,
                jar_path=jar_path,
                config_path=baseline_config,
                meta_dir=baseline_meta,
                spec_name=baseline_spec.name,
            ),
            cwd=formal_dir,
            timeout_seconds=timeout_seconds,
        )
        baseline_summary = parse_tlc_summary(
            baseline_result.output, baseline_result.returncode
        )
        baseline_trace = extract_counterexample_trace(baseline_result.output)
        baseline_assignment_count = count_outcome_assignments(baseline_text, case.outcome)
        row_baseline_ok = (
            baseline_summary.status == NO_COUNTEREXAMPLE_STATUS
            and not baseline_trace
            and baseline_assignment_count == 0
            and all(
                getattr(baseline_summary, field) == expected
                for field, expected in BASELINE_COUNTS.items()
            )
        )
        baseline_ok = baseline_ok and row_baseline_ok
        baseline_rows.append(
            {
                "case_id": case.case_id,
                "outcome": case.outcome,
                "status": BASELINE_PRESERVED_STATUS if row_baseline_ok else TRACE_MISMATCH_STATUS,
                "baseline_spec_sha256": sha256_file(baseline_spec),
                "expected_baseline_spec_sha256": BASELINE_SPEC_SHA256,
                "outcome_assignment_count": baseline_assignment_count,
                "generated_states": baseline_summary.generated_states,
                "distinct_states": baseline_summary.distinct_states,
                "queued_states": baseline_summary.queued_states,
                "search_depth": baseline_summary.search_depth,
            }
        )
        logs[f"phase13-tlc-baseline-{case.case_id}.log"] = baseline_result.output

        expansion_config = repository_root / case.expansion_config_path
        expansion_meta = output_dir / f"tlc-meta-expanded-{case.case_id}"
        expansion_meta.mkdir(exist_ok=True)
        expansion_result = run_command(
            _tlc_command(
                java_command=java_command,
                jar_path=jar_path,
                config_path=expansion_config,
                meta_dir=expansion_meta,
                spec_name=expanded_spec.name,
            ),
            cwd=formal_dir,
            timeout_seconds=timeout_seconds,
        )
        expansion_summary = parse_tlc_summary(
            expansion_result.output, expansion_result.returncode
        )
        trace_raw = extract_counterexample_trace(expansion_result.output)
        formal_trace = normalize_formal_trace(trace_raw)
        actions = [str(row["action"]) for row in formal_trace]
        expanded_assignment_count = count_outcome_assignments(expanded_text, case.outcome)

        python_trace: list[dict[str, object]] = []
        comparison_rows: list[dict[str, object]] = []
        comparison_summary = {
            "comparison_rows": 0,
            "matched_rows": 0,
            "mismatch_count": 0,
        }
        replay_error = None
        gap_cause = None
        try:
            python_trace, gap_cause = replay_python_expansion(case, actions)
            comparison_rows, comparison_summary = compare_traces(formal_trace, python_trace)
        except Exception as exc:  # retained as evidence before the final gate fails
            replay_error = f"{type(exc).__name__}: {exc}"

        canonical = canonical_baseline_outcome(case)
        canonical_match = canonical["outcome"] == case.outcome
        witness_ok = (
            expansion_summary.status == COUNTEREXAMPLE_STATUS
            and expansion_summary.violated_invariant == case.property_name
            and tuple(actions) == case.expected_actions
            and bool(trace_raw)
            and expanded_assignment_count == 1
        )
        trace_match = replay_error is None and comparison_summary["mismatch_count"] == 0
        case_ok = witness_ok and trace_match and canonical_match
        expansion_ok = expansion_ok and case_ok

        witness_record = {
            "schema_version": "0.1.0",
            "case_id": case.case_id,
            "outcome": case.outcome,
            "status": EXPANSION_WITNESS_STATUS if witness_ok else TRACE_MISMATCH_STATUS,
            "trace_comparison_status": (
                TRACE_MATCH_STATUS if trace_match else TRACE_MISMATCH_STATUS
            ),
            "testing_role": "PROVISIONAL_ABSTRACTION_GAP_OUTCOME_WITNESS",
            "violated_invariant": expansion_summary.violated_invariant,
            "trace_state_count": len(trace_raw),
            "actions": actions,
            "formal_trace": formal_trace,
            "python_trace": python_trace,
            "comparison_summary": comparison_summary,
            "gap_cause": gap_cause,
            "expected_gap_cause": case.expected_gap_cause,
            "canonical_baseline_scenario": canonical,
            "canonical_semantics_match": canonical_match,
            "replay_error": replay_error,
            "baseline_outcome_assignment_count": baseline_assignment_count,
            "expanded_outcome_assignment_count": expanded_assignment_count,
            "interpretation_boundary": (
                "This witness belongs to an opt-in diagnostic expansion module. Agreement with the "
                "Python projection and an existing baseline scenario does not prove model completeness, "
                "refinement, implementation equivalence, realism, or cryptographic security."
            ),
        }
        witness_name = f"phase13-witness-{case.case_id}.json"
        (output_dir / witness_name).write_text(
            json.dumps(witness_record, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        derived_names.append(witness_name)

        comparison_name = f"phase13-comparison-{case.case_id}.csv"
        _write_csv(
            output_dir / comparison_name,
            comparison_rows,
            ("step", "action", "field", "formal_value", "python_value", "match"),
        )
        derived_names.append(comparison_name)

        witness_rows.append(
            {
                "case_id": case.case_id,
                "outcome": case.outcome,
                "status": witness_record["status"],
                "trace_comparison_status": witness_record["trace_comparison_status"],
                "trace_state_count": len(trace_raw),
                "actions": actions,
                **comparison_summary,
                "generated_states": expansion_summary.generated_states,
                "distinct_states": expansion_summary.distinct_states,
                "search_depth": expansion_summary.search_depth,
                "gap_cause": gap_cause,
                "canonical_semantics_match": canonical_match,
                "replay_error": replay_error,
            }
        )
        assignment_rows.append(
            {
                "case_id": case.case_id,
                "outcome": case.outcome,
                "baseline_assignment_count": baseline_assignment_count,
                "expanded_assignment_count": expanded_assignment_count,
                "diagnosis": (
                    "EXPLICITLY_ADDED_IN_OPT_IN_EXPANSION"
                    if baseline_assignment_count == 0 and expanded_assignment_count == 1
                    else "ASSIGNMENT_AUDIT_REQUIRES_REVIEW"
                ),
            }
        )
        logs[f"phase13-tlc-expanded-{case.case_id}.log"] = expansion_result.output

    for name, content in logs.items():
        (output_dir / name).write_text(content, encoding="utf-8")
    derived_names.extend(logs.keys())

    baseline_name = "phase13-baseline-regression.csv"
    _write_csv(
        output_dir / baseline_name,
        baseline_rows,
        (
            "case_id",
            "outcome",
            "status",
            "baseline_spec_sha256",
            "expected_baseline_spec_sha256",
            "outcome_assignment_count",
            "generated_states",
            "distinct_states",
            "queued_states",
            "search_depth",
        ),
    )
    derived_names.append(baseline_name)

    assignment_name = "phase13-expansion-assignment-audit.csv"
    _write_csv(
        output_dir / assignment_name,
        assignment_rows,
        (
            "case_id",
            "outcome",
            "baseline_assignment_count",
            "expanded_assignment_count",
            "diagnosis",
        ),
    )
    derived_names.append(assignment_name)

    overall_ok = baseline_ok and expansion_ok
    report = {
        "schema_version": "0.1.0",
        "phase": "Phase 13",
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
            "baseline_spec": str(baseline_spec.relative_to(repository_root)),
            "baseline_spec_sha256": sha256_file(baseline_spec),
            "expected_baseline_spec_sha256": BASELINE_SPEC_SHA256,
            "expanded_spec": str(expanded_spec.relative_to(repository_root)),
            "expanded_spec_sha256": sha256_file(expanded_spec),
            "cases": [
                {
                    "case_id": case.case_id,
                    "outcome": case.outcome,
                    "baseline_config": case.baseline_config_path,
                    "baseline_config_sha256": sha256_file(
                        repository_root / case.baseline_config_path
                    ),
                    "expansion_config": case.expansion_config_path,
                    "expansion_config_sha256": sha256_file(
                        repository_root / case.expansion_config_path
                    ),
                }
                for case in EXPANSION_CASES
            ],
        },
        "sany": {
            "baseline": "PARSE_SUCCESS" if sany_baseline.returncode == 0 else "PARSE_FAILURE",
            "expanded": "PARSE_SUCCESS" if sany_expanded.returncode == 0 else "PARSE_FAILURE",
        },
        "baseline_regression": {
            "status": BASELINE_PRESERVED_STATUS if baseline_ok else TRACE_MISMATCH_STATUS,
            "expected_counts": BASELINE_COUNTS,
            "baseline_spec_hash_matches": baseline_hash_matches,
            "cases": baseline_rows,
        },
        "expanded_outcomes": {
            "status": EXPANSION_DIAGNOSTIC_STATUS,
            "witness_count": len(witness_rows),
            "cases": witness_rows,
            "assignment_audit": assignment_rows,
        },
        "mapping_boundary": (
            "Each expanded witness is compared over the existing 16-field projection and is also tied to "
            "an existing Python baseline scenario. This is a diagnostic bridge, not a refinement proof or "
            "implementation-equivalence result."
        ),
        "completeness_boundary": (
            "Adding one explicit transition path for each previously absent outcome does not establish that "
            "the expanded outcome population, transition relation, causes, or witness set is complete or realistic."
        ),
        "formal_model_completeness_claim": "NOT_PERMITTED",
        "implementation_equivalence_claim": "NOT_PERMITTED",
        "cryptographic_security_claim": "NOT_PERMITTED",
        "publication_evidence_status": "NOT_PERMITTED",
    }
    report_name = "phase13-outcome-expansion-validation.json"
    (output_dir / report_name).write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    derived_names.append(report_name)
    _write_manifest(output_dir, derived_names)

    if not overall_ok:
        raise RuntimeError(
            "Phase 13 baseline preservation or expanded-outcome cross-validation did not pass."
        )
    return report


__all__ = [
    "BASELINE_COUNTS",
    "BASELINE_PRESERVED_STATUS",
    "BASELINE_SPEC_SHA256",
    "EXPANSION_CASES",
    "EXPANSION_DIAGNOSTIC_STATUS",
    "EXPANSION_WITNESS_STATUS",
    "ExpansionCase",
    "canonical_baseline_outcome",
    "execute_outcome_expansion",
    "replay_python_expansion",
]
