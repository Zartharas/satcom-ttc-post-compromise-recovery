from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from .fault_metrics import (
    ExperimentPhase,
    FaultAction,
    FaultKind,
    SeededExperimentConfig,
    run_seeded_experiment,
    schedule_sha256,
)

STATUS = "PROVISIONAL_INTERNAL_REVIEW_ONLY"
BOUND_STATUS = "NOT_REACHED_WITHIN_PROVISIONAL_BOUND"


@dataclass(frozen=True)
class CoverageScenario:
    scenario_id: str
    description: str
    seed: int
    ground_epoch: int = 2
    spacecraft_epoch: int = 1
    authority_epoch_floor: int = 0
    max_transmissions: int = 3
    candidate_lifetime_contacts: int = 3
    schedule: Tuple[FaultAction, ...] = ()
    boundary_tags: Tuple[str, ...] = ()

    def config(self) -> SeededExperimentConfig:
        return SeededExperimentConfig(
            seed=self.seed,
            ground_epoch=self.ground_epoch,
            spacecraft_epoch=self.spacecraft_epoch,
            authority_epoch_floor=self.authority_epoch_floor,
            max_transmissions=self.max_transmissions,
            candidate_lifetime_contacts=self.candidate_lifetime_contacts,
            max_faults=max(4, len(self.schedule)),
            compromise_active_keys=True,
        )


def _fault(
    phase: ExperimentPhase,
    attempt: int,
    kind: FaultKind,
    *,
    target: str = "link",
    contacts: int = 1,
) -> FaultAction:
    return FaultAction(phase, attempt, kind, target=target, contacts=contacts)


def build_coverage_scenarios() -> List[CoverageScenario]:
    scenarios = [
        CoverageScenario("P09-001", "No-fault verified recovery", 9001),
        CoverageScenario(
            "P09-002",
            "Prepare drop with bounded retry",
            9002,
            schedule=(_fault(ExperimentPhase.PREPARE, 1, FaultKind.DROP, target="spacecraft"),),
        ),
        CoverageScenario(
            "P09-003",
            "Response delay across one contact",
            9003,
            schedule=(_fault(ExperimentPhase.RESPONSE, 1, FaultKind.DELAY, target="ground"),),
        ),
        CoverageScenario(
            "P09-004",
            "Duplicate commit rejection without second activation",
            9004,
            schedule=(_fault(ExperimentPhase.COMMIT, 1, FaultKind.DUPLICATE, target="spacecraft"),),
        ),
        CoverageScenario(
            "P09-005",
            "Reordered response injection",
            9005,
            schedule=(_fault(ExperimentPhase.RESPONSE, 1, FaultKind.REORDER, target="ground"),),
        ),
        CoverageScenario(
            "P09-006",
            "Prepare contact closure with retry",
            9006,
            schedule=(_fault(ExperimentPhase.PREPARE, 1, FaultKind.CONTACT_CLOSE),),
        ),
        CoverageScenario(
            "P09-007",
            "Spacecraft restart before commit",
            9007,
            schedule=(_fault(ExperimentPhase.COMMIT, 1, FaultKind.ENDPOINT_RESTART, target="spacecraft"),),
        ),
        CoverageScenario(
            "P09-008",
            "Stale authority counter injection",
            9008,
            schedule=(_fault(ExperimentPhase.PREPARE, 1, FaultKind.STALE_COUNTER, target="spacecraft"),),
        ),
        CoverageScenario(
            "P09-009",
            "Stale commit replay injection",
            9009,
            schedule=(_fault(ExperimentPhase.COMMIT, 1, FaultKind.STALE_REPLAY, target="spacecraft"),),
        ),
        CoverageScenario(
            "P09-010",
            "Status telemetry loss after convergence",
            9010,
            schedule=(_fault(ExperimentPhase.STATUS_TELEMETRY, 1, FaultKind.DROP, target="ground"),),
        ),
        CoverageScenario(
            "P09-011",
            "Test command loss after convergence",
            9011,
            schedule=(_fault(ExperimentPhase.TEST_COMMAND, 1, FaultKind.DROP, target="spacecraft"),),
        ),
        CoverageScenario(
            "P09-012",
            "Confirmation delivery exhausted after spacecraft activation",
            9012,
            schedule=tuple(
                _fault(ExperimentPhase.CONFIRM, attempt, FaultKind.DROP, target="ground")
                for attempt in (1, 2, 3)
            ),
            boundary_tags=("retry_budget_equal", "post_activation_exhaustion"),
        ),
        CoverageScenario(
            "P09-013",
            "Prepare delivery exhausted before activation",
            9013,
            schedule=tuple(
                _fault(ExperimentPhase.PREPARE, attempt, FaultKind.DROP, target="spacecraft")
                for attempt in (1, 2, 3)
            ),
            boundary_tags=("retry_budget_equal", "pre_activation_exhaustion"),
        ),
        CoverageScenario(
            "P09-014",
            "Prepare loss at retry budget minus one",
            9014,
            schedule=tuple(
                _fault(ExperimentPhase.PREPARE, attempt, FaultKind.DROP, target="spacecraft")
                for attempt in (1, 2)
            ),
            boundary_tags=("retry_budget_minus_one",),
        ),
        CoverageScenario(
            "P09-015",
            "Prepare schedule includes one action beyond retry budget",
            9015,
            schedule=tuple(
                _fault(ExperimentPhase.PREPARE, attempt, FaultKind.DROP, target="spacecraft")
                for attempt in (1, 2, 3, 4)
            ),
            boundary_tags=("retry_budget_plus_one", "contains_unreachable_fault_action"),
        ),
        CoverageScenario(
            "P09-016",
            "Commit arrives exactly at candidate lifetime boundary",
            9016,
            candidate_lifetime_contacts=1,
            schedule=(_fault(ExperimentPhase.COMMIT, 1, FaultKind.DELAY, contacts=1),),
            boundary_tags=("candidate_lifetime_equal",),
        ),
        CoverageScenario(
            "P09-017",
            "Commit arrives after candidate lifetime boundary",
            9017,
            candidate_lifetime_contacts=1,
            schedule=(_fault(ExperimentPhase.COMMIT, 1, FaultKind.DELAY, contacts=2),),
            boundary_tags=("candidate_lifetime_plus_one",),
        ),
        CoverageScenario(
            "P09-018",
            "Spacecraft starts ahead and selects a further forward epoch",
            9018,
            ground_epoch=0,
            spacecraft_epoch=3,
            boundary_tags=("spacecraft_ahead", "no_hidden_peer_oracle"),
        ),
        CoverageScenario(
            "P09-019",
            "Recovery authority floor exceeds endpoint epochs",
            9019,
            ground_epoch=1,
            spacecraft_epoch=1,
            authority_epoch_floor=5,
            boundary_tags=("authority_epoch_floor",),
        ),
        CoverageScenario(
            "P09-020",
            "Delay followed by contact closure during response",
            9020,
            schedule=(
                _fault(ExperimentPhase.RESPONSE, 1, FaultKind.DELAY, target="ground", contacts=1),
                _fault(ExperimentPhase.RESPONSE, 1, FaultKind.CONTACT_CLOSE, target="link"),
            ),
            boundary_tags=("multi_fault",),
        ),
        CoverageScenario(
            "P09-021",
            "Duplicate prepare is rejected or handled idempotently",
            9021,
            schedule=(_fault(ExperimentPhase.PREPARE, 1, FaultKind.DUPLICATE, target="spacecraft"),),
        ),
        CoverageScenario(
            "P09-022",
            "Reordered confirmation injection",
            9022,
            schedule=(_fault(ExperimentPhase.CONFIRM, 1, FaultKind.REORDER, target="ground"),),
        ),
        CoverageScenario(
            "P09-023",
            "Ground restart while confirmation is in flight",
            9023,
            schedule=(_fault(ExperimentPhase.CONFIRM, 1, FaultKind.ENDPOINT_RESTART, target="ground"),),
        ),
        CoverageScenario(
            "P09-024",
            "Confirmation contact closure followed by receipt-based retry",
            9024,
            schedule=(_fault(ExperimentPhase.CONFIRM, 1, FaultKind.CONTACT_CLOSE, target="link"),),
        ),
    ]
    return scenarios


_EVENT_STATE = {
    "t1_prepare_sent": "RECOVERING",
    "t1_prepare_accepted": "CANDIDATE",
    "t1_prepare_retry_accepted": "CANDIDATE",
    "t1_response_accepted": "CANDIDATE",
    "t1_spacecraft_activated": "ACTIVATED",
    "t1_ground_activated": "ACTIVATED",
    "t1_recovery_verified": "VERIFIED",
    "t1_attempt_expired_without_activation": "EXPIRED",
    "t1_confirmation_budget_exhausted": "EXPIRED",
    "phase07_unconfirmed_spacecraft_activation": "EXPIRED",
}


def _state_trace(events: Sequence[Dict[str, object]]) -> List[str]:
    states = ["NORMAL"]
    for event in events:
        state = _EVENT_STATE.get(str(event.get("event")))
        if state and state != states[-1]:
            states.append(state)
    return states


def _final_modes(outcome: str, events: Sequence[Dict[str, object]]) -> Tuple[str, str]:
    names = {str(event.get("event")) for event in events}
    if outcome == "SUCCESS":
        return "VERIFIED", "VERIFIED"
    if outcome == "SECURE_DEGRADED":
        return "EXPIRED", "ACTIVATED"
    if outcome == "EXPIRED":
        return "EXPIRED", "EXPIRED"
    if "t1_ground_activated" in names and "t1_spacecraft_activated" in names:
        return "ACTIVATED", "ACTIVATED"
    if "t1_spacecraft_activated" in names:
        return "RECOVERING", "ACTIVATED"
    return "RECOVERING", "CANDIDATE"


def run_coverage_suite(
    scenarios: Sequence[CoverageScenario] | None = None,
) -> List[Dict[str, object]]:
    rows = []
    for scenario in scenarios or build_coverage_scenarios():
        result = run_seeded_experiment(scenario.config(), schedule=scenario.schedule)
        metrics = result.metrics.to_dict()
        ground_mode, spacecraft_mode = _final_modes(metrics["outcome"], result.event_log)
        reachable_faults = sum(
            1
            for action in scenario.schedule
            if action.attempt <= scenario.max_transmissions
        )
        rows.append(
            {
                "scenario_id": scenario.scenario_id,
                "description": scenario.description,
                "status": STATUS,
                "schedule_sha256": schedule_sha256(scenario.schedule),
                "schedule": [action.to_dict() for action in scenario.schedule],
                "schedule_length": len(scenario.schedule),
                "reachable_fault_actions": reachable_faults,
                "unreachable_fault_actions": len(scenario.schedule) - reachable_faults,
                "boundary_tags": list(scenario.boundary_tags),
                "outcome": metrics["outcome"],
                "alignment": metrics["alignment"],
                "security_state": metrics["security_state"],
                "availability_state": metrics["availability_state"],
                "ground_mode": ground_mode,
                "spacecraft_mode": spacecraft_mode,
                "state_trace": _state_trace(result.event_log),
                "event_count": len(result.event_log),
                "verification_complete": metrics["verification_complete"],
                "command_accepted": metrics["command_accepted"],
                "telemetry_complete": metrics["telemetry_complete"],
                "rejection_count": metrics["rejection_count"],
                "retry_overhead": metrics["retry_overhead"],
                "recovery_duration_contacts": metrics["recovery_duration_contacts"],
                "event_log": result.event_log,
            }
        )
    return rows


def _shortest(rows: Iterable[Dict[str, object]]) -> Dict[str, object] | None:
    ordered = sorted(
        rows,
        key=lambda row: (
            int(row["schedule_length"]),
            str(row["schedule_sha256"]),
            str(row["scenario_id"]),
        ),
    )
    return ordered[0] if ordered else None


def build_reachability_report(rows: Sequence[Dict[str, object]]) -> Dict[str, object]:
    states = ["NORMAL", "RECOVERING", "CANDIDATE", "ACTIVATED", "VERIFIED", "EXPIRED"]
    outcomes = [
        "SUCCESS",
        "INDETERMINATE",
        "SECURE_DEGRADED",
        "EXPIRED",
        "DIVERGED",
        "AVAILABLE_UNSAFE",
        "LOCKED",
    ]
    state_rows = []
    for state in states:
        witnesses = [row for row in rows if state in row["state_trace"]]
        witness = _shortest(witnesses)
        state_rows.append(
            {
                "kind": "state",
                "value": state,
                "reachability": "REACHED" if witness else BOUND_STATUS,
                "witness_scenario_id": witness["scenario_id"] if witness else "",
                "witness_schedule_sha256": witness["schedule_sha256"] if witness else "",
                "witness_schedule_length": witness["schedule_length"] if witness else "",
            }
        )
    outcome_rows = []
    for outcome in outcomes:
        witnesses = [row for row in rows if row["outcome"] == outcome]
        witness = _shortest(witnesses)
        outcome_rows.append(
            {
                "kind": "outcome",
                "value": outcome,
                "reachability": "REACHED" if witness else BOUND_STATUS,
                "witness_scenario_id": witness["scenario_id"] if witness else "",
                "witness_schedule_sha256": witness["schedule_sha256"] if witness else "",
                "witness_schedule_length": witness["schedule_length"] if witness else "",
            }
        )
    return {
        "schema_version": "0.1.0",
        "status": STATUS,
        "bound_interpretation": "Unreached does not mean impossible.",
        "scenario_count": len(rows),
        "states": state_rows,
        "outcomes": outcome_rows,
    }


def invariant_traceability() -> List[Dict[str, str]]:
    rows = [
        ("I-S02", "T1Endpoint.activate", "test_spacecraft_ahead_selects_epoch_above_spacecraft_without_oracle", "P09-018", "EpochMonotonicity"),
        ("I-S03", "T1Session.candidate_can_authorize", "test_candidate_cannot_authorize_before_activation", "P09-001", "CandidateNotAuthority"),
        ("I-S05", "T1Session._reject and exact message guards", "test_replayed_commit_after_success_is_rejected_without_state_change", "P09-009", "ReplayNoAdvance"),
        ("I-S08", "PendingRecovery.matches_selected", "test_conflicting_commit_is_rejected", "P09-009", "ExactBinding"),
        ("I-S09", "max_transmissions and bounded pending/receipt fields", "test_prepare_budget_exhaustion_expires_without_activation", "P09-013", "BoundedControlState"),
        ("I-S10", "forward-only activation without fallback transition", "test_compromised_operational_keys_are_replaced", "P09-001", "NoRollback"),
        ("I-S11", "ground proposal and spacecraft target selection", "test_spacecraft_ahead_selects_epoch_above_spacecraft_without_oracle", "P09-018", "NoHiddenPeerOracle"),
        ("I-S12", "spacecraft activation receipt retry path", "test_confirm_loss_uses_activation_receipt_for_idempotent_retry", "P09-004", "AtMostOneSpacecraftActivation"),
        ("I-S13", "monotonic_counter guard", "test_stale_counter_is_rejected_and_counted", "P09-008", "CounterMonotonicity"),
        ("I-L01", "bounded run loops and explicit expiry", "test_prepare_budget_exhaustion_expires_without_activation", "P09-013", "BoundedTermination"),
        ("I-E02", "T1Session.verify_recovery", "test_normal_ground_ahead_recovery_succeeds", "P09-001", "SuccessRequiresEvidence"),
        ("I-E03", "status-loss outcome classification", "test_status_loss_is_indeterminate_after_convergence", "P09-010", "StatusLossNotDivergence"),
        ("I-E05", "secure_degraded outcome precedence", "test_confirmation_budget_exhaustion_is_secure_degraded_not_locked", "P09-012", "DegradedNotSuccess"),
    ]
    return [
        {
            "invariant_id": invariant_id,
            "implementation_guard": implementation,
            "unit_test": test,
            "coverage_scenario": scenario,
            "formal_property": formal_property,
            "status": "PROVISIONAL_TRACEABILITY_ONLY",
        }
        for invariant_id, implementation, test, scenario, formal_property in rows
    ]


def build_phase09_bundle() -> Dict[str, object]:
    rows = run_coverage_suite()
    return {
        "schema_version": "0.1.0",
        "status": STATUS,
        "claim_boundary": "Internal bounded exploration of an abstract controller; not proof of concrete cryptographic security.",
        "coverage_rows": rows,
        "reachability": build_reachability_report(rows),
        "invariant_traceability": invariant_traceability(),
    }


def _write_csv(path: Path, rows: Sequence[Dict[str, object]], fields: Sequence[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_phase09_outputs(bundle: Dict[str, object], output_dir: Path) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    analysis_path = output_dir / "phase09-coverage-reachability.json"
    analysis_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    coverage_path = output_dir / "phase09-coverage-results.csv"
    _write_csv(
        coverage_path,
        bundle["coverage_rows"],
        [
            "scenario_id", "description", "status", "schedule_sha256", "schedule_length",
            "reachable_fault_actions", "unreachable_fault_actions", "boundary_tags", "outcome",
            "alignment", "security_state", "availability_state", "ground_mode", "spacecraft_mode",
            "state_trace", "event_count", "verification_complete", "command_accepted",
            "telemetry_complete", "rejection_count", "retry_overhead", "recovery_duration_contacts",
        ],
    )

    reachability_rows = bundle["reachability"]["states"] + bundle["reachability"]["outcomes"]
    reachability_path = output_dir / "phase09-reachability.csv"
    _write_csv(
        reachability_path,
        reachability_rows,
        ["kind", "value", "reachability", "witness_scenario_id", "witness_schedule_sha256", "witness_schedule_length"],
    )

    traceability_path = output_dir / "phase09-invariant-traceability.csv"
    _write_csv(
        traceability_path,
        bundle["invariant_traceability"],
        ["invariant_id", "implementation_guard", "unit_test", "coverage_scenario", "formal_property", "status"],
    )

    files = [analysis_path, coverage_path, reachability_path, traceability_path]
    manifest_path = output_dir / "phase09-derived-bundle.sha256"
    manifest_path.write_text(
        "".join(
            f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
            for path in files
        ),
        encoding="utf-8",
    )
    return {
        "analysis_json": str(analysis_path),
        "coverage_csv": str(coverage_path),
        "reachability_csv": str(reachability_path),
        "traceability_csv": str(traceability_path),
        "checksum_manifest": str(manifest_path),
    }


__all__ = [
    "BOUND_STATUS",
    "CoverageScenario",
    "build_coverage_scenarios",
    "build_phase09_bundle",
    "build_reachability_report",
    "invariant_traceability",
    "run_coverage_suite",
    "write_phase09_outputs",
]
