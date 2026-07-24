from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from heapq import heappop, heappush
from typing import Callable, Dict, List, Optional, Set


class Mode(str, Enum):
    NORMAL = "NORMAL"
    RECOVERING = "RECOVERING"
    CANDIDATE = "CANDIDATE"
    VERIFIED = "VERIFIED"
    EXPIRED = "EXPIRED"
    LOCKED = "LOCKED"


class Outcome(str, Enum):
    SUCCESS = "SUCCESS"
    SECURE_DEGRADED = "SECURE_DEGRADED"
    AVAILABLE_UNSAFE = "AVAILABLE_UNSAFE"
    DIVERGED = "DIVERGED"
    EXPIRED = "EXPIRED"
    LOCKED = "LOCKED"
    INDETERMINATE = "INDETERMINATE"


class B1ActivationPolicy(str, Enum):
    ACTIVATE_ON_LOCAL_COMPLETION = "ACTIVATE_ON_LOCAL_COMPLETION"
    DEFER_UNTIL_AUTHENTICATED_STATUS = "DEFER_UNTIL_AUTHENTICATED_STATUS"


class B2CompromiseScope(str, Enum):
    NONE = "NONE"
    TRAFFIC_KEY = "TRAFFIC_KEY"
    SENDER_STATE = "SENDER_STATE"
    RECEIVER_STATE = "RECEIVER_STATE"
    BOTH_ENDPOINT_STATES = "BOTH_ENDPOINT_STATES"


@dataclass
class Endpoint:
    endpoint_id: str
    epoch: int = 0
    mode: Mode = Mode.NORMAL
    active_key: str = "K0"
    pending_key: Optional[str] = None
    pending_epoch: Optional[int] = None
    crypto_complete_epoch: Optional[int] = None
    state_exposed: bool = False
    attacker_known_keys: Set[str] = field(default_factory=set)
    replay_seen: Set[str] = field(default_factory=set)
    retired_keys: Set[str] = field(default_factory=set)

    def stage(self, epoch: int, key_ref: str) -> None:
        if epoch <= self.epoch:
            raise ValueError("Pending epoch must exceed the active epoch.")
        self.pending_epoch = epoch
        self.pending_key = key_ref
        self.mode = Mode.CANDIDATE

    def activate(self, epoch: int, key_ref: str, retire_old: bool = True) -> None:
        if epoch <= self.epoch:
            raise ValueError("Epoch must increase monotonically.")
        if retire_old:
            self.retired_keys.add(self.active_key)
        self.epoch = epoch
        self.active_key = key_ref
        self.pending_key = None
        self.pending_epoch = None
        self.mode = Mode.NORMAL

    def expire_pending(self) -> None:
        self.pending_key = None
        self.pending_epoch = None
        self.mode = Mode.EXPIRED


@dataclass(order=True)
class ScheduledEvent:
    logical_time: int
    sequence: int
    name: str = field(compare=False)
    action: Callable[[], None] = field(compare=False)


@dataclass
class Simulation:
    baseline: str
    ground: Endpoint = field(default_factory=lambda: Endpoint("ground"))
    spacecraft: Endpoint = field(default_factory=lambda: Endpoint("spacecraft"))
    event_log: List[Dict[str, object]] = field(default_factory=list)
    attempt_expired: bool = False
    completion_ambiguous: bool = False
    verification_complete: bool = True
    lockout_reason: Optional[str] = None
    b2_compromise_scope: B2CompromiseScope = B2CompromiseScope.NONE
    attacker_impersonated_sender: bool = False
    _queue: List[ScheduledEvent] = field(default_factory=list)
    _sequence: int = 0

    def log(self, event: str, **details: object) -> None:
        self.event_log.append({
            "event_seq": len(self.event_log),
            "event": event,
            "ground_epoch": self.ground.epoch,
            "spacecraft_epoch": self.spacecraft.epoch,
            **details,
        })

    def schedule(self, logical_time: int, name: str, action: Callable[[], None]) -> None:
        self._sequence += 1
        heappush(self._queue, ScheduledEvent(logical_time, self._sequence, name, action))

    def run(self) -> None:
        while self._queue:
            item = heappop(self._queue)
            self.log("dispatch", logical_time=item.logical_time, name=item.name)
            item.action()
            self.check_invariants()

    def check_invariants(self) -> None:
        for endpoint in (self.ground, self.spacecraft):
            if endpoint.epoch < 0:
                raise AssertionError("Negative epoch.")
            if endpoint.pending_epoch is not None and endpoint.pending_epoch <= endpoint.epoch:
                raise AssertionError("Pending epoch must exceed the active epoch.")
            if endpoint.active_key in endpoint.retired_keys:
                raise AssertionError("Active key cannot be retired.")

    def alignment_state(self) -> str:
        if self.ground.epoch == self.spacecraft.epoch and self.ground.active_key == self.spacecraft.active_key:
            return f"SYNC({self.ground.epoch})"
        if self.ground.epoch > self.spacecraft.epoch:
            return "G_AHEAD"
        if self.spacecraft.epoch > self.ground.epoch:
            return "S_AHEAD"
        return "DIVERGED"

    def joint_state(self) -> str:
        return "LOCKED" if self.lockout_reason else self.alignment_state()

    def evaluate(self) -> Outcome:
        if self.lockout_reason:
            return Outcome.LOCKED
        if self.attempt_expired:
            return Outcome.EXPIRED

        alignment = self.alignment_state()
        if alignment.startswith("SYNC"):
            if not self.verification_complete:
                return Outcome.INDETERMINATE
            key = self.ground.active_key
            known = key in self.ground.attacker_known_keys or key in self.spacecraft.attacker_known_keys
            return Outcome.AVAILABLE_UNSAFE if known else Outcome.SUCCESS
        if alignment in {"G_AHEAD", "S_AHEAD", "DIVERGED"}:
            return Outcome.DIVERGED
        return Outcome.INDETERMINATE


def b0_otar(sim: Simulation, master_compromised: bool = False, drop_upload: bool = False) -> None:
    target = sim.ground.epoch + 1
    new_key = f"K{target}"
    if master_compromised:
        sim.ground.attacker_known_keys.add(new_key)
        sim.spacecraft.attacker_known_keys.add(new_key)
    if drop_upload:
        sim.log("b0_upload_dropped", key_ref=new_key)
        return
    sim.spacecraft.stage(target, new_key)
    sim.log("b0_upload_staged", key_ref=new_key)
    sim.ground.activate(target, new_key)
    sim.spacecraft.activate(target, new_key)
    sim.log("b0_key_activated", key_ref=new_key)


def b1_triple_kem(
    sim: Simulation,
    drop_confirm: bool = False,
    out_of_order: bool = False,
    activation_policy: B1ActivationPolicy = B1ActivationPolicy.ACTIVATE_ON_LOCAL_COMPLETION,
    drop_status: bool = False,
) -> None:
    target = sim.ground.epoch + 1
    new_key = f"TK{target}"

    if out_of_order:
        sim.attempt_expired = True
        sim.ground.mode = Mode.EXPIRED
        sim.spacecraft.mode = Mode.EXPIRED
        sim.log("b1_abort_out_of_order")
        return

    sim.ground.stage(target, new_key)
    sim.spacecraft.stage(target, new_key)
    sim.log("b1_init_response_complete", key_ref=new_key)

    sim.ground.crypto_complete_epoch = target
    sim.completion_ambiguous = True
    sim.log("b1_initiator_crypto_complete", key_ref=new_key)

    if activation_policy == B1ActivationPolicy.ACTIVATE_ON_LOCAL_COMPLETION:
        sim.ground.activate(target, new_key)
        sim.log("b1_initiator_activated_locally", key_ref=new_key)

    if drop_confirm:
        sim.log("b1_confirm_dropped", key_ref=new_key)
        sim.spacecraft.expire_pending()
        if activation_policy == B1ActivationPolicy.DEFER_UNTIL_AUTHENTICATED_STATUS:
            sim.ground.expire_pending()
            sim.attempt_expired = True
        return

    sim.spacecraft.crypto_complete_epoch = target
    sim.completion_ambiguous = False
    sim.log("b1_responder_crypto_complete", key_ref=new_key)

    if activation_policy == B1ActivationPolicy.ACTIVATE_ON_LOCAL_COMPLETION:
        sim.spacecraft.activate(target, new_key)
        sim.log("b1_responder_activated_locally", key_ref=new_key)
        return

    sim.spacecraft.activate(target, new_key)
    sim.log("b1_authenticated_status_sent", key_ref=new_key)

    if drop_status:
        sim.ground.expire_pending()
        sim.log("b1_authenticated_status_dropped", key_ref=new_key)
        return

    sim.ground.activate(target, new_key)
    sim.log("b1_authenticated_status_received", key_ref=new_key)


def _apply_b2_compromise(sim: Simulation, scope: B2CompromiseScope) -> None:
    sim.b2_compromise_scope = scope
    if scope == B2CompromiseScope.TRAFFIC_KEY:
        sim.ground.attacker_known_keys.add(sim.ground.active_key)
        sim.spacecraft.attacker_known_keys.add(sim.spacecraft.active_key)
    elif scope == B2CompromiseScope.SENDER_STATE:
        sim.ground.state_exposed = True
    elif scope == B2CompromiseScope.RECEIVER_STATE:
        sim.spacecraft.state_exposed = True
    elif scope == B2CompromiseScope.BOTH_ENDPOINT_STATES:
        sim.ground.state_exposed = True
        sim.spacecraft.state_exposed = True


def b2_urke_strict(
    sim: Simulation,
    drop_update: bool = False,
    compromise_scope: B2CompromiseScope = B2CompromiseScope.NONE,
    lose_status: bool = False,
    active_sender_impersonation: bool = False,
) -> None:
    _apply_b2_compromise(sim, compromise_scope)

    if active_sender_impersonation:
        if compromise_scope not in {B2CompromiseScope.SENDER_STATE, B2CompromiseScope.BOTH_ENDPOINT_STATES}:
            raise ValueError("Active sender impersonation requires exposed sender state.")
        target = sim.spacecraft.epoch + 1
        attacker_key = f"A{target}"
        sim.spacecraft.activate(target, attacker_key, retire_old=True)
        sim.spacecraft.attacker_known_keys.add(attacker_key)
        sim.attacker_impersonated_sender = True
        sim.lockout_reason = "exposed sender state was used to advance the receiver on an attacker-known branch"
        sim.log("b2_sender_state_impersonation_lockout", key_ref=attacker_key)
        return

    target = sim.ground.epoch + 1
    new_key = f"R{target}"
    sim.ground.activate(target, new_key, retire_old=True)
    sim.log("b2_sender_advanced", key_ref=new_key)

    receiver_exposed = compromise_scope in {B2CompromiseScope.RECEIVER_STATE, B2CompromiseScope.BOTH_ENDPOINT_STATES}
    if receiver_exposed:
        sim.ground.attacker_known_keys.add(new_key)

    if drop_update:
        sim.lockout_reason = "sender advanced and deleted prior state before receiver processed update"
        sim.log("b2_update_dropped_lockout", key_ref=new_key)
        return

    sim.spacecraft.activate(target, new_key, retire_old=True)
    if receiver_exposed:
        sim.spacecraft.attacker_known_keys.add(new_key)
    sim.log("b2_receiver_advanced", key_ref=new_key)

    if lose_status:
        sim.verification_complete = False
        sim.log("b2_status_telemetry_lost", key_ref=new_key)
    else:
        sim.log("b2_status_verified", key_ref=new_key)


def restore_ground_snapshot(sim: Simulation, epoch: int, key_ref: str) -> None:
    if epoch >= sim.ground.epoch:
        raise ValueError("The restored snapshot must be older than the current ground state.")
    sim.ground.epoch = epoch
    sim.ground.active_key = key_ref
    sim.ground.pending_key = None
    sim.ground.pending_epoch = None
    sim.ground.crypto_complete_epoch = None
    sim.ground.retired_keys.discard(key_ref)
    sim.lockout_reason = "stale ground snapshot no longer matches spacecraft ratchet state"
    sim.log("b2_stale_ground_snapshot_restored", restored_epoch=epoch, key_ref=key_ref)


def replay_b2_update(sim: Simulation, target_epoch: int, message_id: str) -> bool:
    if message_id in sim.spacecraft.replay_seen or target_epoch <= sim.spacecraft.epoch:
        sim.log("b2_replay_rejected", target_epoch=target_epoch, message_id=message_id)
        return False
    sim.spacecraft.replay_seen.add(message_id)
    sim.log("b2_update_not_replay", target_epoch=target_epoch, message_id=message_id)
    return True


b2_strict_rke = b2_urke_strict
