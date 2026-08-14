from __future__ import annotations

import csv
import hashlib
import json
import random
from dataclasses import asdict, dataclass, field, replace
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

from .simulator import Outcome
from .t1_controller import (
    RecoveryMessage,
    RecoveryMessageKind,
    T1Endpoint,
    T1Mode,
    T1Session,
)


class ExperimentPhase(str, Enum):
    PREPARE = "RECOVERY_PREPARE"
    RESPONSE = "RECOVERY_RESPONSE"
    COMMIT = "RECOVERY_COMMIT"
    CONFIRM = "RECOVERY_CONFIRM"
    TEST_COMMAND = "TEST_COMMAND"
    STATUS_TELEMETRY = "STATUS_TELEMETRY"


class FaultKind(str, Enum):
    DROP = "DROP"
    DELAY = "DELAY"
    DUPLICATE = "DUPLICATE"
    REORDER = "REORDER"
    CONTACT_CLOSE = "CONTACT_CLOSE"
    ENDPOINT_RESTART = "ENDPOINT_RESTART"
    STALE_COUNTER = "STALE_COUNTER"
    STALE_REPLAY = "STALE_REPLAY"


@dataclass(frozen=True)
class FaultAction:
    phase: ExperimentPhase
    attempt: int
    kind: FaultKind
    target: str = "link"
    contacts: int = 1

    def to_dict(self) -> Dict[str, object]:
        return {
            "phase": self.phase.value,
            "attempt": self.attempt,
            "kind": self.kind.value,
            "target": self.target,
            "contacts": self.contacts,
        }


@dataclass(frozen=True)
class SeededExperimentConfig:
    seed: int
    ground_epoch: int = 2
    spacecraft_epoch: int = 1
    authority_epoch_floor: int = 0
    max_transmissions: int = 3
    candidate_lifetime_contacts: int = 3
    max_faults: int = 3
    compromise_active_keys: bool = True
    allowed_faults: Sequence[FaultKind] = (
        FaultKind.DROP,
        FaultKind.DELAY,
        FaultKind.DUPLICATE,
        FaultKind.REORDER,
        FaultKind.CONTACT_CLOSE,
        FaultKind.ENDPOINT_RESTART,
        FaultKind.STALE_COUNTER,
        FaultKind.STALE_REPLAY,
    )


@dataclass
class RecoveryMetrics:
    seed: int
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

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass
class ExperimentResult:
    schema_version: str
    status: str
    config: Dict[str, object]
    schedule: List[Dict[str, object]]
    metrics: RecoveryMetrics
    event_log: List[Dict[str, object]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "config": self.config,
            "schedule": self.schedule,
            "metrics": self.metrics.to_dict(),
            "event_log": self.event_log,
        }


_PHASE_ORDER = {
    ExperimentPhase.PREPARE: 0,
    ExperimentPhase.RESPONSE: 1,
    ExperimentPhase.COMMIT: 2,
    ExperimentPhase.CONFIRM: 3,
    ExperimentPhase.TEST_COMMAND: 4,
    ExperimentPhase.STATUS_TELEMETRY: 5,
}

_VALID_PHASES = {
    FaultKind.DROP: tuple(ExperimentPhase),
    FaultKind.DELAY: tuple(ExperimentPhase),
    FaultKind.DUPLICATE: (
        ExperimentPhase.PREPARE,
        ExperimentPhase.RESPONSE,
        ExperimentPhase.COMMIT,
        ExperimentPhase.CONFIRM,
    ),
    FaultKind.REORDER: (
        ExperimentPhase.PREPARE,
        ExperimentPhase.RESPONSE,
        ExperimentPhase.COMMIT,
        ExperimentPhase.CONFIRM,
    ),
    FaultKind.CONTACT_CLOSE: tuple(ExperimentPhase),
    FaultKind.ENDPOINT_RESTART: (
        ExperimentPhase.COMMIT,
        ExperimentPhase.CONFIRM,
    ),
    FaultKind.STALE_COUNTER: (ExperimentPhase.PREPARE,),
    FaultKind.STALE_REPLAY: (
        ExperimentPhase.COMMIT,
        ExperimentPhase.CONFIRM,
    ),
}


def _target_for(phase: ExperimentPhase, kind: FaultKind) -> str:
    if kind == FaultKind.ENDPOINT_RESTART:
        return "spacecraft" if phase == ExperimentPhase.COMMIT else "ground"
    if phase in {ExperimentPhase.PREPARE, ExperimentPhase.COMMIT, ExperimentPhase.TEST_COMMAND}:
        return "spacecraft"
    if phase in {ExperimentPhase.RESPONSE, ExperimentPhase.CONFIRM, ExperimentPhase.STATUS_TELEMETRY}:
        return "ground"
    return "link"


def generate_fault_schedule(config: SeededExperimentConfig) -> List[FaultAction]:
    rng = random.Random(config.seed)
    max_faults = max(0, config.max_faults)
    fault_count = rng.randint(0, max_faults)
    candidates: List[FaultAction] = []
    seen = set()

    for _ in range(fault_count * 4 + 4):
        if len(candidates) >= fault_count:
            break
        kind = rng.choice(tuple(config.allowed_faults))
        phase = rng.choice(_VALID_PHASES[kind])
        attempt = 1
        if phase in {
            ExperimentPhase.PREPARE,
            ExperimentPhase.RESPONSE,
            ExperimentPhase.COMMIT,
            ExperimentPhase.CONFIRM,
        }:
            attempt = rng.randint(1, max(1, config.max_transmissions))
        contacts = rng.randint(1, 2) if kind == FaultKind.DELAY else 1
        key = (phase.value, attempt, kind.value)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(
            FaultAction(
                phase=phase,
                attempt=attempt,
                kind=kind,
                target=_target_for(phase, kind),
                contacts=contacts,
            )
        )

    return sorted(
        candidates,
        key=lambda action: (
            _PHASE_ORDER[action.phase],
            action.attempt,
            action.kind.value,
        ),
    )


def serialize_schedule(schedule: Sequence[FaultAction]) -> str:
    payload = [action.to_dict() for action in schedule]
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def schedule_sha256(schedule: Sequence[FaultAction]) -> str:
    return hashlib.sha256(serialize_schedule(schedule).encode("utf-8")).hexdigest()


def schedule_from_dicts(
    rows: Sequence[Dict[str, object]],
) -> List[FaultAction]:
    actions = []
    for row in rows:
        actions.append(
            FaultAction(
                phase=ExperimentPhase(str(row["phase"])),
                attempt=int(row["attempt"]),
                kind=FaultKind(str(row["kind"])),
                target=str(row.get("target", "link")),
                contacts=int(row.get("contacts", 1)),
            )
        )
    return sorted(
        actions,
        key=lambda action: (
            _PHASE_ORDER[action.phase],
            action.attempt,
            action.kind.value,
        ),
    )


def _actions(
    schedule: Sequence[FaultAction],
    phase: ExperimentPhase,
    attempt: int,
) -> List[FaultAction]:
    return [
        action
        for action in schedule
        if action.phase == phase and action.attempt == attempt
    ]


class _ExperimentRunner:
    def __init__(
        self,
        config: SeededExperimentConfig,
        schedule: Sequence[FaultAction],
    ) -> None:
        self.config = config
        self.schedule = list(schedule)
        same_state = config.ground_epoch == config.spacecraft_epoch
        ground_key = (
            f"K{config.ground_epoch}"
            if same_state
            else f"G{config.ground_epoch}"
        )
        spacecraft_key = (
            f"K{config.spacecraft_epoch}"
            if same_state
            else f"S{config.spacecraft_epoch}"
        )
        self.session = T1Session(
            ground=T1Endpoint(
                "ground",
                epoch=config.ground_epoch,
                active_key=ground_key,
            ),
            spacecraft=T1Endpoint(
                "spacecraft",
                epoch=config.spacecraft_epoch,
                active_key=spacecraft_key,
            ),
            max_transmissions=config.max_transmissions,
            candidate_lifetime_contacts=config.candidate_lifetime_contacts,
        )
        self.session.authority.epoch_floor = config.authority_epoch_floor
        if config.compromise_active_keys:
            self.session.ground.compromised_keys.add(self.session.ground.active_key)
            self.session.spacecraft.compromised_keys.add(
                self.session.spacecraft.active_key
            )
        self.transmissions: Dict[ExperimentPhase, int] = {
            phase: 0 for phase in ExperimentPhase
        }
        self.divergent_contacts = 0
        self.degraded_contacts = 0

    def _advance_contacts(self, contacts: int, reason: str) -> None:
        for _ in range(max(0, contacts)):
            alignment = self.session.alignment_state()
            if not alignment.startswith("SYNC"):
                self.divergent_contacts += 1
            if self.session.secure_degraded:
                self.degraded_contacts += 1
            self.session.current_contact += 1
            self.session.log(
                "phase07_contact_advanced",
                contact=self.session.current_contact,
                reason=reason,
                alignment=alignment,
            )

    def _restart(self, target: str, phase: ExperimentPhase) -> None:
        endpoint = (
            self.session.spacecraft if target == "spacecraft" else self.session.ground
        )
        endpoint.pending = None
        endpoint.activation_receipt = None
        self.session.log(
            "phase07_endpoint_restarted",
            endpoint=endpoint.endpoint_id,
            phase=phase.value,
        )

    def _pre_delivery(
        self,
        phase: ExperimentPhase,
        attempt: int,
        message: Optional[RecoveryMessage],
    ) -> bool:
        deliver = True
        for action in _actions(self.schedule, phase, attempt):
            self.session.log(
                "phase07_fault_applied",
                phase=phase.value,
                attempt=attempt,
                kind=action.kind.value,
                target=action.target,
            )
            if action.kind == FaultKind.DELAY:
                self._advance_contacts(action.contacts, "DELAY")
            elif action.kind == FaultKind.CONTACT_CLOSE:
                self._advance_contacts(1, "CONTACT_CLOSE")
                deliver = False
            elif action.kind == FaultKind.DROP:
                deliver = False
            elif action.kind == FaultKind.ENDPOINT_RESTART:
                self._restart(action.target, phase)
            elif action.kind == FaultKind.REORDER and message is not None:
                self._inject_reordered(phase, message)
            elif action.kind == FaultKind.STALE_COUNTER and message is not None:
                self._inject_stale_counter(message)
        return deliver

    def _post_delivery(
        self,
        phase: ExperimentPhase,
        attempt: int,
        message: Optional[RecoveryMessage],
    ) -> None:
        if message is None:
            return
        for action in _actions(self.schedule, phase, attempt):
            if action.kind == FaultKind.DUPLICATE:
                self._deliver_duplicate(phase, message)
            elif action.kind == FaultKind.STALE_REPLAY:
                self._deliver_stale_replay(phase, message)

    def _inject_reordered(
        self,
        phase: ExperimentPhase,
        message: RecoveryMessage,
    ) -> None:
        wrong_kind = {
            ExperimentPhase.PREPARE: RecoveryMessageKind.RESPONSE,
            ExperimentPhase.RESPONSE: RecoveryMessageKind.COMMIT,
            ExperimentPhase.COMMIT: RecoveryMessageKind.CONFIRM,
            ExperimentPhase.CONFIRM: RecoveryMessageKind.COMMIT,
        }[phase]
        forged = replace(
            message,
            message_id=f"reordered-{message.message_id}",
            kind=wrong_kind,
        )
        if phase in {ExperimentPhase.PREPARE, ExperimentPhase.COMMIT}:
            if phase == ExperimentPhase.PREPARE:
                self.session.spacecraft_accept_prepare(forged)
            else:
                self.session.spacecraft_accept_commit(forged)
        else:
            if phase == ExperimentPhase.RESPONSE:
                self.session.ground_accept_response(forged)
            else:
                self.session.ground_accept_confirm(forged)

    def _inject_stale_counter(self, message: RecoveryMessage) -> None:
        forged = replace(
            message,
            message_id=f"stale-counter-{message.message_id}",
            counter=0,
        )
        self.session.spacecraft_accept_prepare(forged)

    def _deliver_duplicate(
        self,
        phase: ExperimentPhase,
        message: RecoveryMessage,
    ) -> None:
        if phase == ExperimentPhase.PREPARE:
            self.session.spacecraft_accept_prepare(message)
        elif phase == ExperimentPhase.RESPONSE:
            self.session.ground_accept_response(message)
        elif phase == ExperimentPhase.COMMIT:
            self.session.spacecraft_accept_commit(message)
        elif phase == ExperimentPhase.CONFIRM:
            self.session.ground_accept_confirm(message)
        else:
            self.session.log(
                "phase07_evidence_duplicate",
                phase=phase.value,
                message_id=message.message_id,
            )

    def _deliver_stale_replay(
        self,
        phase: ExperimentPhase,
        message: RecoveryMessage,
    ) -> None:
        replay = replace(
            message,
            message_id=f"stale-replay-{message.message_id}",
            counter=max(0, message.counter - 1),
        )
        if phase == ExperimentPhase.COMMIT:
            self.session.spacecraft_accept_commit(replay)
        elif phase == ExperimentPhase.CONFIRM:
            self.session.ground_accept_confirm(replay)

    def _finish_unconfirmed(self) -> None:
        if (
            self.session.spacecraft.activation_receipt is not None
            or self.session.spacecraft.epoch > self.session.ground.epoch
        ):
            self.session.ground.pending = None
            self.session.ground.mode = T1Mode.EXPIRED
            self.session.secure_degraded = True
            self.session.log(
                "phase07_unconfirmed_spacecraft_activation",
                alignment=self.session.alignment_state(),
            )
            self.session.check_invariants()
            return
        self.session.expire_attempt()

    def run(self) -> T1Session:
        prepare = self.session.start_recovery(
            f"seed-{self.config.seed}",
            transcript_ref=f"schedule:{schedule_sha256(self.schedule)}",
        )
        response: Optional[RecoveryMessage] = None

        for attempt in range(1, self.config.max_transmissions + 1):
            if attempt > 1:
                try:
                    prepare = self.session.retry_prepare()
                except RuntimeError:
                    break
            self.transmissions[ExperimentPhase.PREPARE] += 1
            if not self._pre_delivery(
                ExperimentPhase.PREPARE, attempt, prepare
            ):
                continue
            response = self.session.spacecraft_accept_prepare(prepare)
            self._post_delivery(ExperimentPhase.PREPARE, attempt, prepare)
            if response is None:
                break

            self.transmissions[ExperimentPhase.RESPONSE] += 1
            if not self._pre_delivery(
                ExperimentPhase.RESPONSE, attempt, response
            ):
                response = None
                continue
            delivered_response = response
            commit = self.session.ground_accept_response(delivered_response)
            self._post_delivery(
                ExperimentPhase.RESPONSE, attempt, delivered_response
            )
            if commit is None:
                response = None
                break
            response = delivered_response
            break

        if response is None or self.session.last_commit is None:
            self.session.expire_attempt()
            return self.session

        commit = self.session.last_commit
        confirmed = False
        for attempt in range(1, self.config.max_transmissions + 1):
            if attempt > 1:
                try:
                    commit = self.session.retry_commit()
                except RuntimeError:
                    break
            self.transmissions[ExperimentPhase.COMMIT] += 1
            if not self._pre_delivery(
                ExperimentPhase.COMMIT, attempt, commit
            ):
                continue
            confirm = self.session.spacecraft_accept_commit(commit)
            self._post_delivery(ExperimentPhase.COMMIT, attempt, commit)
            if confirm is None:
                break

            self.transmissions[ExperimentPhase.CONFIRM] += 1
            if not self._pre_delivery(
                ExperimentPhase.CONFIRM, attempt, confirm
            ):
                continue
            confirmed = self.session.ground_accept_confirm(confirm)
            self._post_delivery(ExperimentPhase.CONFIRM, attempt, confirm)
            if confirmed:
                break

        if not confirmed:
            self._finish_unconfirmed()
            return self.session

        drop_test = False
        drop_status = False
        self.transmissions[ExperimentPhase.TEST_COMMAND] += 1
        if not self._pre_delivery(
            ExperimentPhase.TEST_COMMAND, 1, None
        ):
            drop_test = True
        self.transmissions[ExperimentPhase.STATUS_TELEMETRY] += 1
        if not self._pre_delivery(
            ExperimentPhase.STATUS_TELEMETRY, 1, None
        ):
            drop_status = True

        self.session.verify_recovery(
            drop_test_command=drop_test,
            drop_status=drop_status,
        )
        return self.session


def _count_faults(
    schedule: Sequence[FaultAction],
    kind: FaultKind,
) -> int:
    return sum(1 for action in schedule if action.kind == kind)


def _active_key_compromised(session: T1Session) -> bool:
    active = session.ground.active_key
    return (
        active in session.ground.compromised_keys
        or active in session.spacecraft.compromised_keys
        or session.authority.compromised
    )


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


def _rejection_metrics(
    event_log: Iterable[Dict[str, object]],
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


def run_seeded_experiment(
    config: SeededExperimentConfig,
    schedule: Optional[Sequence[FaultAction]] = None,
) -> ExperimentResult:
    chosen_schedule = (
        list(schedule) if schedule is not None else generate_fault_schedule(config)
    )
    runner = _ExperimentRunner(config, chosen_schedule)
    session = runner.run()
    rejection_metrics = _rejection_metrics(session.event_log)
    total_transmissions = sum(runner.transmissions.values())
    baseline_transmissions = 6
    metrics = RecoveryMetrics(
        seed=config.seed,
        schedule_sha256=schedule_sha256(chosen_schedule),
        outcome=session.outcome().value,
        alignment=session.alignment_state(),
        security_state=_security_state(session),
        availability_state=_availability_state(session),
        recovery_duration_contacts=session.current_contact + 1,
        divergent_contact_windows=runner.divergent_contacts,
        degraded_contact_windows=runner.degraded_contacts,
        total_transmissions=total_transmissions,
        retry_overhead=max(0, total_transmissions - baseline_transmissions),
        fault_count=len(chosen_schedule),
        drop_count=_count_faults(chosen_schedule, FaultKind.DROP),
        delay_count=_count_faults(chosen_schedule, FaultKind.DELAY),
        duplicate_count=_count_faults(chosen_schedule, FaultKind.DUPLICATE),
        reorder_count=_count_faults(chosen_schedule, FaultKind.REORDER),
        contact_close_count=_count_faults(
            chosen_schedule, FaultKind.CONTACT_CLOSE
        ),
        restart_count=_count_faults(
            chosen_schedule, FaultKind.ENDPOINT_RESTART
        ),
        replay_count=_count_faults(
            chosen_schedule, FaultKind.STALE_REPLAY
        ),
        rejection_count=rejection_metrics["rejection_count"],
        replay_rejection_count=rejection_metrics[
            "replay_rejection_count"
        ],
        stale_state_rejection_count=rejection_metrics[
            "stale_state_rejection_count"
        ],
        command_accepted=any(
            event.get("event") == "t1_test_command_accepted"
            for event in session.event_log
        ),
        telemetry_complete=any(
            event.get("event") == "t1_recovery_verified"
            for event in session.event_log
        ),
        verification_complete=session.verification_complete,
        active_key_compromised=_active_key_compromised(session),
    )
    return ExperimentResult(
        schema_version="0.1.0",
        status="PROVISIONAL_INTERNAL_REVIEW_ONLY",
        config={
            "seed": config.seed,
            "ground_epoch": config.ground_epoch,
            "spacecraft_epoch": config.spacecraft_epoch,
            "authority_epoch_floor": config.authority_epoch_floor,
            "max_transmissions": config.max_transmissions,
            "candidate_lifetime_contacts": config.candidate_lifetime_contacts,
            "max_faults": config.max_faults,
            "compromise_active_keys": config.compromise_active_keys,
            "allowed_faults": [
                fault.value for fault in config.allowed_faults
            ],
        },
        schedule=[action.to_dict() for action in chosen_schedule],
        metrics=metrics,
        event_log=session.event_log,
    )


def write_results(
    results: Sequence[ExperimentResult],
    json_path: Path,
    csv_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "0.1.0",
        "status": "PROVISIONAL_INTERNAL_REVIEW_ONLY",
        "result_count": len(results),
        "results": [result.to_dict() for result in results],
    }
    json_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    rows = [result.metrics.to_dict() for result in results]
    fieldnames = list(RecoveryMetrics.__dataclass_fields__.keys())
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


__all__ = [
    "ExperimentPhase",
    "ExperimentResult",
    "FaultAction",
    "FaultKind",
    "RecoveryMetrics",
    "SeededExperimentConfig",
    "generate_fault_schedule",
    "run_seeded_experiment",
    "schedule_from_dicts",
    "schedule_sha256",
    "serialize_schedule",
    "write_results",
]
