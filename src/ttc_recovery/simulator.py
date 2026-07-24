from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from heapq import heappush, heappop
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


@dataclass
class Endpoint:
    endpoint_id: str
    epoch: int = 0
    mode: Mode = Mode.NORMAL
    active_key: str = "K0"
    pending_key: Optional[str] = None
    pending_epoch: Optional[int] = None
    attacker_known_keys: Set[str] = field(default_factory=set)
    replay_seen: Set[str] = field(default_factory=set)
    retired_keys: Set[str] = field(default_factory=set)

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
    _queue: List[ScheduledEvent] = field(default_factory=list)
    _sequence: int = 0

    def log(self, event: str, **details: object) -> None:
        self.event_log.append({
            "event_seq": len(self.event_log),
            "event": event,
            "ground_epoch": self.ground.epoch,
            "spacecraft_epoch": self.spacecraft.epoch,
            **details
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
                raise AssertionError("Pending epoch must exceed active epoch.")
            if endpoint.active_key in endpoint.retired_keys:
                raise AssertionError("Active key cannot be retired.")

    def joint_state(self) -> str:
        if self.ground.mode == Mode.LOCKED or self.spacecraft.mode == Mode.LOCKED:
            return "LOCKED"
        if self.ground.epoch == self.spacecraft.epoch and self.ground.active_key == self.spacecraft.active_key:
            return f"SYNC({self.ground.epoch})"
        if self.ground.epoch > self.spacecraft.epoch:
            return "G_AHEAD"
        if self.spacecraft.epoch > self.ground.epoch:
            return "S_AHEAD"
        return "DIVERGED"

    def evaluate(self) -> Outcome:
        joint = self.joint_state()
        if joint == "LOCKED":
            return Outcome.LOCKED
        if joint.startswith("SYNC"):
            key = self.ground.active_key
            known = key in self.ground.attacker_known_keys or key in self.spacecraft.attacker_known_keys
            return Outcome.AVAILABLE_UNSAFE if known else Outcome.SUCCESS
        if joint in {"G_AHEAD", "S_AHEAD", "DIVERGED"}:
            return Outcome.DIVERGED
        if self.ground.mode == Mode.EXPIRED or self.spacecraft.mode == Mode.EXPIRED:
            return Outcome.EXPIRED
        return Outcome.INDETERMINATE


def b0_otar(sim: Simulation, master_compromised: bool = False, drop_upload: bool = False) -> None:
    """Abstract SDLS EP-style OTAR; no cryptographic operations."""
    target = sim.ground.epoch + 1
    new_key = f"K{target}"
    if master_compromised:
        sim.ground.attacker_known_keys.add(new_key)
        sim.spacecraft.attacker_known_keys.add(new_key)
    if drop_upload:
        sim.log("b0_upload_dropped", key_ref=new_key)
        return
    sim.spacecraft.pending_key = new_key
    sim.spacecraft.pending_epoch = target
    sim.log("b0_upload_staged", key_ref=new_key)
    sim.ground.activate(target, new_key)
    sim.spacecraft.activate(target, new_key)
    sim.log("b0_key_activated", key_ref=new_key)


def b1_triple_kem(sim: Simulation, drop_confirm: bool = False, out_of_order: bool = False) -> None:
    """Abstract Triple-KEM/PQNoise-style exchange with key confirmation."""
    target = sim.ground.epoch + 1
    new_key = f"TK{target}"
    if out_of_order:
        sim.ground.mode = Mode.EXPIRED
        sim.spacecraft.mode = Mode.EXPIRED
        sim.log("b1_abort_out_of_order")
        return
    sim.ground.mode = Mode.RECOVERING
    sim.spacecraft.mode = Mode.RECOVERING
    sim.spacecraft.pending_key = new_key
    sim.spacecraft.pending_epoch = target
    sim.log("b1_init_response_complete", key_ref=new_key)
    sim.ground.activate(target, new_key)
    sim.log("b1_ground_completed", key_ref=new_key)
    if drop_confirm:
        sim.log("b1_confirm_dropped", key_ref=new_key)
        return
    sim.spacecraft.activate(target, new_key)
    sim.log("b1_spacecraft_completed", key_ref=new_key)


def b2_strict_rke(sim: Simulation, drop_advance: bool = False, drop_ack: bool = False) -> None:
    """Abstract strict stateful evolution with deletion at advancement."""
    target = sim.ground.epoch + 1
    new_key = f"R{target}"
    if drop_advance:
        sim.log("b2_advance_dropped", key_ref=new_key)
        return
    sim.spacecraft.activate(target, new_key, retire_old=True)
    sim.log("b2_spacecraft_advanced", key_ref=new_key)
    if drop_ack:
        sim.spacecraft.mode = Mode.LOCKED
        sim.log("b2_ack_dropped_lockout", key_ref=new_key)
        return
    sim.ground.activate(target, new_key, retire_old=True)
    sim.log("b2_ground_advanced", key_ref=new_key)


def demo() -> None:
    cases = [
        ("B0 safe", lambda s: b0_otar(s)),
        ("B0 master compromised", lambda s: b0_otar(s, master_compromised=True)),
        ("B1 normal", lambda s: b1_triple_kem(s)),
        ("B1 confirm lost", lambda s: b1_triple_kem(s, drop_confirm=True)),
        ("B2 normal", lambda s: b2_strict_rke(s)),
        ("B2 ack lost", lambda s: b2_strict_rke(s, drop_ack=True))
    ]
    for label, action in cases:
        sim = Simulation(label)
        sim.schedule(0, label, lambda a=action, s=sim: a(s))
        sim.run()
        print(f"{label:24s} joint={sim.joint_state():10s} outcome={sim.evaluate().value}")


if __name__ == "__main__":
    demo()
