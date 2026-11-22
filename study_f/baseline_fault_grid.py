"""Study F engine (DRAFT). Reuses the frozen simulator read-only; adds step-level fault injection.

Design rules (see docs/study_f/STUDY_F_PLAN_DRAFT.md):
* A cell exists only where the frozen baseline abstraction defines the fault's semantics.
  Every other (baseline, step, fault kind) is recorded NOT_DEFINED, never silently dropped.
* Two transmission budgets bracket the baselines: 1 (as specified: no retransmission is
  defined) and 3 (a named assumption favourable to baselines: the lost message is
  retransmitted, matching T1's default budget).
* On the overlapping cells the engine must reproduce the frozen catalog (tests).
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

from ttc_recovery.baseline_metrics import _active_key_compromised
from ttc_recovery.simulator import Mode, Outcome, Simulation

# (flow id) -> ordered steps
FLOWS: Dict[str, Tuple[str, ...]] = {
    "B0": ("OTAR_UPLOAD",),
    "B1_LOCAL": ("KEM_INIT_RESPONSE", "KEM_CONFIRM"),
    "B1_DEFERRED": ("KEM_INIT_RESPONSE", "KEM_CONFIRM", "AUTHENTICATED_STATUS"),
    "B2": ("RATCHET_UPDATE", "STATUS_TELEMETRY"),
}
T1_KINDS = ("DROP", "DELAY", "DUPLICATE", "REORDER", "CONTACT_CLOSE",
            "ENDPOINT_RESTART", "STALE_COUNTER", "STALE_REPLAY")
LOSS_KINDS = ("DROP", "CONTACT_CLOSE")  # equivalent in a sequential one-message-per-step flow (A-seq)
NATIVE_B2 = ("STALE_GROUND_RESTORE", "REPLAY_UPDATE")  # frozen B2-09, B2-10; not equated to T1 kinds
INITIAL_STATES = ("T1_BASE", "CATALOG", "CATALOG_COMPROMISED")


@dataclass(frozen=True)
class Cell:
    flow: str
    step: Optional[str]      # None for control
    kind: str                # CONTROL, DROP, CONTACT_CLOSE, REORDER, ENDPOINT_RESTART, native names
    lost: int                # consecutive lost transmissions of the step (loss kinds), else 0
    budget: int              # 1 or 3 transmissions

    @property
    def cell_id(self) -> str:
        return f"{self.flow}|{self.step or '-'}|{self.kind}|c{self.lost}|R{self.budget}"


def initial_sim(flow: str, initial: str) -> Simulation:
    sim = Simulation(flow)
    if initial == "T1_BASE":
        sim.ground.epoch, sim.ground.active_key = 2, "K2"
        sim.spacecraft.epoch, sim.spacecraft.active_key = 1, "K1"
    elif initial not in {"CATALOG", "CATALOG_COMPROMISED"}:
        raise ValueError(initial)
    # T1_BASE and CATALOG_COMPROMISED start post-compromise (current keys attacker-known);
    # CATALOG matches the frozen catalog scenarios that do not mark the key.
    if initial != "CATALOG":
        sim.ground.attacker_known_keys.add(sim.ground.active_key)
        sim.spacecraft.attacker_known_keys.add(sim.spacecraft.active_key)
    return sim


def _delivered(cell: Cell, step: str) -> bool:
    """True if some transmission within the budget is delivered."""
    lost = cell.lost if (cell.kind in LOSS_KINDS and cell.step == step) else 0
    return lost < cell.budget


def _run_b0(sim: Simulation, cell: Cell) -> None:
    if not _delivered(cell, "OTAR_UPLOAD"):
        sim.log("b0_upload_dropped")
        return
    t = sim.ground.epoch + 1
    k = f"K{t}"
    sim.spacecraft.stage(t, k)
    sim.ground.activate(t, k)
    sim.spacecraft.activate(t, k)


def _run_b1(sim: Simulation, cell: Cell, deferred: bool) -> None:
    t = sim.ground.epoch + 1
    k = f"TK{t}"
    if cell.kind == "REORDER" and cell.step == "KEM_INIT_RESPONSE":
        sim.attempt_expired = True
        sim.ground.mode = sim.spacecraft.mode = Mode.EXPIRED
        return
    if not _delivered(cell, "KEM_INIT_RESPONSE"):
        sim.attempt_expired = True
        sim.ground.mode = sim.spacecraft.mode = Mode.EXPIRED
        return
    sim.ground.stage(t, k)
    sim.spacecraft.stage(t, k)
    sim.ground.crypto_complete_epoch = t
    sim.completion_ambiguous = True
    if not deferred:
        sim.ground.activate(t, k)
    restarted = cell.kind == "ENDPOINT_RESTART"  # spacecraft loses volatile pending state (A-vol)
    if restarted or not _delivered(cell, "KEM_CONFIRM"):
        sim.spacecraft.expire_pending()
        if deferred:
            sim.ground.expire_pending()
            sim.attempt_expired = True
        return
    sim.spacecraft.crypto_complete_epoch = t
    sim.completion_ambiguous = False
    sim.spacecraft.activate(t, k)
    if not deferred:
        return
    if not _delivered(cell, "AUTHENTICATED_STATUS"):
        sim.ground.expire_pending()
        return
    sim.ground.activate(t, k)


def _run_b2(sim: Simulation, cell: Cell) -> None:
    from ttc_recovery.simulator import replay_b2_update, restore_ground_snapshot
    t = sim.ground.epoch + 1
    k = f"R{t}"
    sim.ground.activate(t, k, retire_old=True)
    if not _delivered(cell, "RATCHET_UPDATE"):
        sim.lockout_reason = "sender advanced and deleted prior state before receiver processed update"
        return
    sim.spacecraft.activate(t, k, retire_old=True)
    if not _delivered(cell, "STATUS_TELEMETRY"):
        sim.verification_complete = False
    if cell.kind == "STALE_GROUND_RESTORE":
        restore_ground_snapshot(sim, 0, "K0")
    elif cell.kind == "REPLAY_UPDATE":
        replay_b2_update(sim, target_epoch=t, message_id="update-replay")


def run_cell(cell: Cell, initial: str = "T1_BASE") -> Dict[str, object]:
    sim = initial_sim(cell.flow, initial)
    if cell.flow == "B0":
        _run_b0(sim, cell)
    elif cell.flow == "B1_LOCAL":
        _run_b1(sim, cell, deferred=False)
    elif cell.flow == "B1_DEFERRED":
        _run_b1(sim, cell, deferred=True)
    elif cell.flow == "B2":
        _run_b2(sim, cell)
    else:
        raise ValueError(cell.flow)
    outcome = sim.evaluate()
    unsafe = _active_key_compromised(sim)
    return {
        "cell_id": cell.cell_id, "initial_state": initial, "flow": cell.flow, "step": cell.step or "-",
        "kind": cell.kind, "lost_transmissions": cell.lost, "budget": cell.budget,
        "outcome": outcome.value, "alignment": sim.alignment_state(),
        "security_state": "UNSAFE" if unsafe else ("SECURE_PROVISIONAL" if outcome == Outcome.SUCCESS else "NOT_ESTABLISHED"),
        "verification_complete": outcome in {Outcome.SUCCESS, Outcome.AVAILABLE_UNSAFE},
    }


def enumerate_cells(budgets: Iterable[int] = (1, 3)) -> List[Cell]:
    cells: List[Cell] = []
    for b in budgets:
        for flow, steps in FLOWS.items():
            cells.append(Cell(flow, None, "CONTROL", 0, b))
            for step in steps:
                for kind in LOSS_KINDS:
                    for lost in (1, 2, 3):
                        cells.append(Cell(flow, step, kind, lost, b))
        for flow in ("B1_LOCAL", "B1_DEFERRED"):
            cells.append(Cell(flow, "KEM_INIT_RESPONSE", "REORDER", 0, b))
            cells.append(Cell(flow, "KEM_CONFIRM", "ENDPOINT_RESTART", 0, b))
        for native in NATIVE_B2:
            cells.append(Cell("B2", "RATCHET_UPDATE", native, 0, b))
    return cells


def not_defined_records() -> List[Dict[str, str]]:
    """T1 fault kinds with no defined semantics in a baseline step (recorded, never dropped)."""
    defined = {(c.flow, c.step, c.kind) for c in enumerate_cells((1,))}
    out = []
    for flow, steps in FLOWS.items():
        for step in steps:
            for kind in T1_KINDS:
                if (flow, step, kind) not in defined:
                    out.append({"flow": flow, "step": step, "kind": kind, "status": "NOT_DEFINED_BY_BASELINE"})
    return out


def plan_sha256() -> str:
    payload = json.dumps([c.cell_id for c in enumerate_cells()] + [json.dumps(r, sort_keys=True) for r in not_defined_records()])
    return hashlib.sha256(payload.encode()).hexdigest()


def run_grid(initial: str = "T1_BASE") -> List[Dict[str, object]]:
    return [run_cell(c, initial) for c in enumerate_cells()]


def write_csv(rows: List[Dict[str, object]], path: str) -> None:
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
