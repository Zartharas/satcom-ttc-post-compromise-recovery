from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence

from .fault_metrics import RecoveryMetrics
from .simulator import (
    B1ActivationPolicy,
    B2CompromiseScope,
    Outcome,
    Simulation,
    b0_otar,
    b1_triple_kem,
    b2_urke_strict,
    replay_b2_update,
    restore_ground_snapshot,
)


PARITY_STATUS = "IMPLEMENTED_PENDING_VALIDATION"
RESULT_STATUS = "PROVISIONAL_INTERNAL_REVIEW_ONLY"
SHARED_METRIC_FIELDS = tuple(RecoveryMetrics.__dataclass_fields__.keys())


@dataclass(frozen=True)
class BaselineMetrics:
    treatment: str
    baseline_variant: str
    scenario_id: str
    seed: Optional[int]
    schedule_sha256: str
    outcome: str
    alignment: str
    security_state: str
    availability_state: str
    recovery_duration_contacts: int
    divergent_contact_windows: int
    degraded_contact_windows: int
    total_transmissions: int
    retry_overhead: int
    fault_count: int
    drop_count: int
    delay_count: int
    duplicate_count: int
    reorder_count: int
    contact_close_count: int
    restart_count: int
    replay_count: int
    rejection_count: int
    replay_rejection_count: int
    stale_state_rejection_count: int
    command_accepted: bool
    telemetry_complete: bool
    verification_complete: bool
    active_key_compromised: bool
    other_fault_count: int

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class BaselineExperimentResult:
    schema_version: str
    status: str
    metric_parity_status: str
    treatment: str
    baseline_variant: str
    scenario_id: str
    config: Dict[str, object]
    schedule: List[Dict[str, object]]
    metrics: BaselineMetrics
    event_log: List[Dict[str, object]]

    def to_dict(self) -> Dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "metric_parity_status": self.metric_parity_status,
            "treatment": self.treatment,
            "baseline_variant": self.baseline_variant,
            "scenario_id": self.scenario_id,
            "config": self.config,
            "schedule": self.schedule,
            "metrics": self.metrics.to_dict(),
            "event_log": self.event_log,
        }


_NORMALIZED_ACTIONS: Dict[str, List[Dict[str, object]]] = {
    "B0-04": [
        {
            "phase": "OTAR_UPLOAD",
            "attempt": 1,
            "kind": "DROP",
            "target": "spacecraft",
            "contacts": 0,
        }
    ],
    "B1-03": [
        {
            "phase": "REQUIRED_FRAGMENT",
            "attempt": 1,
            "kind": "REORDER",
            "target": "exchange",
            "contacts": 0,
        }
    ],
    "B1-04": [
        {
            "phase": "KEM_CONFIRM",
            "attempt": 1,
            "kind": "DROP",
            "target": "spacecraft",
            "contacts": 0,
        }
    ],
    "B1-06": [
        {
            "phase": "KEM_CONFIRM",
            "attempt": 1,
            "kind": "DROP",
            "target": "spacecraft",
            "contacts": 0,
        }
    ],
    "B1-07": [
        {
            "phase": "AUTHENTICATED_STATUS",
            "attempt": 1,
            "kind": "DROP",
            "target": "ground",
            "contacts": 0,
        }
    ],
    "B2-06": [
        {
            "phase": "RATCHET_UPDATE",
            "attempt": 1,
            "kind": "ACTIVE_SENDER_IMPERSONATION",
            "target": "spacecraft",
            "contacts": 0,
        }
    ],
    "B2-07": [
        {
            "phase": "RATCHET_UPDATE",
            "attempt": 1,
            "kind": "DROP",
            "target": "spacecraft",
            "contacts": 0,
        }
    ],
    "B2-08": [
        {
            "phase": "STATUS_TELEMETRY",
            "attempt": 1,
            "kind": "DROP",
            "target": "ground",
            "contacts": 0,
        }
    ],
    "B2-09": [
        {
            "phase": "RATCHET_STATE",
            "attempt": 1,
            "kind": "ENDPOINT_RESTART",
            "target": "ground",
            "contacts": 0,
            "detail": "STALE_GROUND_RESTORE",
        }
    ],
    "B2-10": [
        {
            "phase": "RATCHET_UPDATE",
            "attempt": 1,
            "kind": "STALE_REPLAY",
            "target": "spacecraft",
            "contacts": 0,
        }
    ],
}


_TOTAL_TRANSMISSIONS = {
    "B0-01": 1,
    "B0-02": 1,
    "B0-03": 1,
    "B0-04": 1,
    "B1-01": 3,
    "B1-02": 3,
    "B1-03": 2,
    "B1-04": 3,
    "B1-05": 4,
    "B1-06": 3,
    "B1-07": 4,
    "B2-01": 2,
    "B2-02": 2,
    "B2-03": 2,
    "B2-04": 2,
    "B2-05": 2,
    "B2-06": 1,
    "B2-07": 1,
    "B2-08": 2,
    "B2-09": 2,
    "B2-10": 3,
}


_REFERENCE_TRANSMISSIONS = {
    "B0": 1,
    "B1": 3,
    "B1-STATUS-ENHANCED": 4,
    "B2-URKE": 2,
}


def treatment_for(entry: Mapping[str, object]) -> str:
    baseline = str(entry["baseline"])
    if baseline.startswith("B0"):
        return "B0"
    if baseline.startswith("B1"):
        return "B1"
    if baseline.startswith("B2"):
        return "B2"
    raise ValueError(f"Unsupported baseline variant: {baseline}")


def normalized_schedule(entry: Mapping[str, object]) -> List[Dict[str, object]]:
    return [dict(row) for row in _NORMALIZED_ACTIONS.get(str(entry["id"]), [])]


def schedule_sha256(
    entry: Mapping[str, object],
    schedule: Sequence[Mapping[str, object]],
) -> str:
    payload = {
        "scenario_id": entry["id"],
        "baseline": entry["baseline"],
        "initial_state": entry.get("initial_state"),
        "compromise": entry.get("compromise"),
        "activation_policy": entry.get("activation_policy"),
        "schedule": list(schedule),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _mark_current_key_compromised(sim: Simulation) -> None:
    sim.ground.attacker_known_keys.add(sim.ground.active_key)
    sim.spacecraft.attacker_known_keys.add(sim.spacecraft.active_key)
    sim.log("phase15_baseline_current_key_marked_compromised")


def _execute(entry: Mapping[str, object]) -> Simulation:
    scenario_id = str(entry["id"])
    sim = Simulation(scenario_id)

    def action() -> None:
        if scenario_id == "B0-01":
            b0_otar(sim)
        elif scenario_id == "B0-02":
            _mark_current_key_compromised(sim)
            b0_otar(sim)
        elif scenario_id == "B0-03":
            b0_otar(sim, master_compromised=True)
        elif scenario_id == "B0-04":
            _mark_current_key_compromised(sim)
            b0_otar(sim, drop_upload=True)
        elif scenario_id in {"B1-01", "B1-02"}:
            if scenario_id == "B1-02":
                _mark_current_key_compromised(sim)
            b1_triple_kem(sim)
        elif scenario_id == "B1-03":
            b1_triple_kem(sim, out_of_order=True)
        elif scenario_id == "B1-04":
            b1_triple_kem(sim, drop_confirm=True)
        elif scenario_id == "B1-05":
            b1_triple_kem(
                sim,
                activation_policy=(
                    B1ActivationPolicy.DEFER_UNTIL_AUTHENTICATED_STATUS
                ),
            )
        elif scenario_id == "B1-06":
            b1_triple_kem(
                sim,
                drop_confirm=True,
                activation_policy=(
                    B1ActivationPolicy.DEFER_UNTIL_AUTHENTICATED_STATUS
                ),
            )
        elif scenario_id == "B1-07":
            b1_triple_kem(
                sim,
                drop_status=True,
                activation_policy=(
                    B1ActivationPolicy.DEFER_UNTIL_AUTHENTICATED_STATUS
                ),
            )
        elif scenario_id == "B2-01":
            b2_urke_strict(sim)
        elif scenario_id == "B2-02":
            b2_urke_strict(
                sim,
                compromise_scope=B2CompromiseScope.TRAFFIC_KEY,
            )
        elif scenario_id == "B2-03":
            b2_urke_strict(
                sim,
                compromise_scope=B2CompromiseScope.SENDER_STATE,
            )
        elif scenario_id == "B2-04":
            b2_urke_strict(
                sim,
                compromise_scope=B2CompromiseScope.RECEIVER_STATE,
            )
        elif scenario_id == "B2-05":
            b2_urke_strict(
                sim,
                compromise_scope=B2CompromiseScope.BOTH_ENDPOINT_STATES,
            )
        elif scenario_id == "B2-06":
            b2_urke_strict(
                sim,
                compromise_scope=B2CompromiseScope.SENDER_STATE,
                active_sender_impersonation=True,
            )
        elif scenario_id == "B2-07":
            b2_urke_strict(sim, drop_update=True)
        elif scenario_id == "B2-08":
            b2_urke_strict(sim, lose_status=True)
        elif scenario_id == "B2-09":
            b2_urke_strict(sim)
            restore_ground_snapshot(sim, 0, "K0")
        elif scenario_id == "B2-10":
            b2_urke_strict(sim)
            replay_b2_update(sim, target_epoch=1, message_id="update-1")
        else:
            raise ValueError(f"Unsupported baseline scenario: {scenario_id}")

    sim.schedule(0, scenario_id, action)
    sim.run()
    return sim


def _active_key_compromised(sim: Simulation) -> bool:
    known = sim.ground.attacker_known_keys | sim.spacecraft.attacker_known_keys
    return sim.ground.active_key in known or sim.spacecraft.active_key in known


def _availability_state(outcome: Outcome) -> str:
    if outcome == Outcome.SUCCESS:
        return "AVAILABLE"
    if outcome in {
        Outcome.INDETERMINATE,
        Outcome.SECURE_DEGRADED,
        Outcome.AVAILABLE_UNSAFE,
    }:
        return "DEGRADED"
    return "UNAVAILABLE"


def _rejection_metrics(sim: Simulation) -> Dict[str, int]:
    rejection_count = 0
    replay_rejection_count = 0
    stale_state_rejection_count = 0
    for event in sim.event_log:
        name = str(event.get("event", ""))
        if name == "b2_replay_rejected":
            rejection_count += 1
            replay_rejection_count += 1
        if "stale" in name and "rejected" in name:
            stale_state_rejection_count += 1
    return {
        "rejection_count": rejection_count,
        "replay_rejection_count": replay_rejection_count,
        "stale_state_rejection_count": stale_state_rejection_count,
    }


def _count_kind(schedule: Sequence[Mapping[str, object]], kind: str) -> int:
    return sum(1 for row in schedule if str(row.get("kind")) == kind)


def _validate_oracle(entry: Mapping[str, object], sim: Simulation) -> None:
    expected_alignment = str(entry["expected_alignment"])
    expected_outcome = str(entry["expected_outcome"])
    if sim.alignment_state() != expected_alignment:
        raise AssertionError(
            f"{entry['id']} alignment mismatch: "
            f"{sim.alignment_state()} != {expected_alignment}"
        )
    expected_joint = entry.get("expected_joint_state")
    if expected_joint is not None and sim.joint_state() != str(expected_joint):
        raise AssertionError(
            f"{entry['id']} joint-state mismatch: "
            f"{sim.joint_state()} != {expected_joint}"
        )
    if sim.evaluate().value != expected_outcome:
        raise AssertionError(
            f"{entry['id']} outcome mismatch: "
            f"{sim.evaluate().value} != {expected_outcome}"
        )


def run_baseline_scenario(
    entry: Mapping[str, object],
) -> BaselineExperimentResult:
    scenario_id = str(entry["id"])
    variant = str(entry["baseline"])
    treatment = treatment_for(entry)
    schedule = normalized_schedule(entry)
    sim = _execute(entry)
    _validate_oracle(entry, sim)

    outcome = sim.evaluate()
    alignment = sim.alignment_state()
    active_key_compromised = _active_key_compromised(sim)
    verification_complete = outcome in {
        Outcome.SUCCESS,
        Outcome.AVAILABLE_UNSAFE,
    }
    command_accepted = alignment.startswith("SYNC") and outcome not in {
        Outcome.EXPIRED,
        Outcome.LOCKED,
    }
    telemetry_complete = verification_complete
    security_state = (
        "UNSAFE"
        if active_key_compromised
        else "SECURE_PROVISIONAL"
        if verification_complete
        else "NOT_ESTABLISHED"
    )
    rejections = _rejection_metrics(sim)
    total_transmissions = _TOTAL_TRANSMISSIONS[scenario_id]
    reference_transmissions = _REFERENCE_TRANSMISSIONS[variant]
    known_kinds = {
        "DROP",
        "DELAY",
        "DUPLICATE",
        "REORDER",
        "CONTACT_CLOSE",
        "ENDPOINT_RESTART",
        "STALE_REPLAY",
    }
    other_fault_count = sum(
        1 for row in schedule if str(row.get("kind")) not in known_kinds
    )

    sim.log(
        "phase15_baseline_metric_adapter_complete",
        scenario_id=scenario_id,
        treatment=treatment,
        contact=1,
        outcome=outcome.value,
        alignment=alignment,
        command_accepted=command_accepted,
        telemetry_complete=telemetry_complete,
        publication_evidence=False,
    )

    metrics = BaselineMetrics(
        treatment=treatment,
        baseline_variant=variant,
        scenario_id=scenario_id,
        seed=None,
        schedule_sha256=schedule_sha256(entry, schedule),
        outcome=outcome.value,
        alignment=alignment,
        security_state=security_state,
        availability_state=_availability_state(outcome),
        recovery_duration_contacts=1,
        divergent_contact_windows=0 if alignment.startswith("SYNC") else 1,
        degraded_contact_windows=(
            1
            if outcome
            in {
                Outcome.INDETERMINATE,
                Outcome.SECURE_DEGRADED,
                Outcome.AVAILABLE_UNSAFE,
            }
            else 0
        ),
        total_transmissions=total_transmissions,
        retry_overhead=max(0, total_transmissions - reference_transmissions),
        fault_count=len(schedule),
        drop_count=_count_kind(schedule, "DROP"),
        delay_count=_count_kind(schedule, "DELAY"),
        duplicate_count=_count_kind(schedule, "DUPLICATE"),
        reorder_count=_count_kind(schedule, "REORDER"),
        contact_close_count=_count_kind(schedule, "CONTACT_CLOSE"),
        restart_count=_count_kind(schedule, "ENDPOINT_RESTART"),
        replay_count=_count_kind(schedule, "STALE_REPLAY"),
        rejection_count=rejections["rejection_count"],
        replay_rejection_count=rejections["replay_rejection_count"],
        stale_state_rejection_count=rejections[
            "stale_state_rejection_count"
        ],
        command_accepted=command_accepted,
        telemetry_complete=telemetry_complete,
        verification_complete=verification_complete,
        active_key_compromised=active_key_compromised,
        other_fault_count=other_fault_count,
    )
    return BaselineExperimentResult(
        schema_version="0.1.0",
        status=RESULT_STATUS,
        metric_parity_status=PARITY_STATUS,
        treatment=treatment,
        baseline_variant=variant,
        scenario_id=scenario_id,
        config={
            "initial_state": entry.get("initial_state"),
            "compromise": entry.get("compromise"),
            "activation_policy": entry.get("activation_policy"),
            "properties": list(entry.get("properties", [])),
            "adapter_semantics": (
                "One deterministic catalog scenario is represented as one "
                "discrete contact; transmission counts are declared adapter "
                "values and remain provisional."
            ),
        },
        schedule=schedule,
        metrics=metrics,
        event_log=list(sim.event_log),
    )


def run_baseline_catalog(
    entries: Sequence[Mapping[str, object]],
) -> List[BaselineExperimentResult]:
    return [run_baseline_scenario(entry) for entry in entries]


def write_baseline_results(
    results: Sequence[BaselineExperimentResult],
    json_path: Path,
    csv_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "0.1.0",
        "status": RESULT_STATUS,
        "metric_parity_status": PARITY_STATUS,
        "publication_evidence": False,
        "result_count": len(results),
        "shared_metric_fields": list(SHARED_METRIC_FIELDS),
        "results": [result.to_dict() for result in results],
    }
    json_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    rows = [result.metrics.to_dict() for result in results]
    fieldnames = list(BaselineMetrics.__dataclass_fields__.keys())
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


__all__ = [
    "BaselineExperimentResult",
    "BaselineMetrics",
    "PARITY_STATUS",
    "RESULT_STATUS",
    "SHARED_METRIC_FIELDS",
    "normalized_schedule",
    "run_baseline_catalog",
    "run_baseline_scenario",
    "schedule_sha256",
    "treatment_for",
    "write_baseline_results",
]
