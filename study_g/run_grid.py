"""Study G grid (exploratory, post hoc). See docs/study_g/STUDY_G_PROTOCOL.md."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from ttc_recovery.fault_metrics import (
    ExperimentPhase as P,
    FaultAction,
    FaultKind as K,
    SeededExperimentConfig,
    _target_for,
)

from study_g.t1_retry import run_with_verification_budget

CONFIG = SeededExperimentConfig(seed=0, ground_epoch=2, spacecraft_epoch=1, authority_epoch_floor=0,
                                max_transmissions=3, candidate_lifetime_contacts=3,
                                compromise_active_keys=True)
STEPS = (P.PREPARE, P.RESPONSE, P.COMMIT, P.CONFIRM, P.TEST_COMMAND, P.STATUS_TELEMETRY)
LOSS_KINDS = (K.DROP, K.CONTACT_CLOSE)
LOST_COUNTS = (1, 2, 3)
VERIFICATION_BUDGETS = (1, 3)
REORDER_STEPS = (P.PREPARE, P.RESPONSE, P.COMMIT, P.CONFIRM)
RESTART_STEPS = (P.COMMIT, P.CONFIRM)  # targets fixed by Part I _target_for: spacecraft at COMMIT, ground at CONFIRM
# Role mapping T1 step -> Study F (flow, step); an analogy by role, not an equivalence.
ROLE_MAP: Dict[str, List[List[str]]] = {
    "RECOVERY_PREPARE": [["B0", "OTAR_UPLOAD"], ["B1_LOCAL", "KEM_INIT_RESPONSE"], ["B1_DEFERRED", "KEM_INIT_RESPONSE"], ["B2", "RATCHET_UPDATE"]],
    "RECOVERY_RESPONSE": [["B0", "OTAR_UPLOAD"], ["B1_LOCAL", "KEM_INIT_RESPONSE"], ["B1_DEFERRED", "KEM_INIT_RESPONSE"], ["B2", "RATCHET_UPDATE"]],
    "RECOVERY_COMMIT": [["B1_LOCAL", "KEM_CONFIRM"], ["B1_DEFERRED", "KEM_CONFIRM"]],
    "RECOVERY_CONFIRM": [["B1_LOCAL", "KEM_CONFIRM"], ["B1_DEFERRED", "KEM_CONFIRM"]],
    "TEST_COMMAND": [["B1_DEFERRED", "AUTHENTICATED_STATUS"], ["B2", "STATUS_TELEMETRY"]],
    "STATUS_TELEMETRY": [["B1_DEFERRED", "AUTHENTICATED_STATUS"], ["B2", "STATUS_TELEMETRY"]],
}


@dataclass(frozen=True)
class GCell:
    step: Optional[str]
    kind: str
    lost: int
    vbudget: int

    @property
    def cell_id(self) -> str:
        return f"T1|{self.step or '-'}|{self.kind}|c{self.lost}|V{self.vbudget}"

    @property
    def arm(self) -> str:
        return f"T1_V{self.vbudget}"


def enumerate_cells() -> List[GCell]:
    cells: List[GCell] = []
    for vb in VERIFICATION_BUDGETS:
        cells.append(GCell(None, "CONTROL", 0, vb))
        for s in STEPS:
            for k in LOSS_KINDS:
                for n in LOST_COUNTS:
                    cells.append(GCell(s.value, k.value, n, vb))
        for s in REORDER_STEPS:
            cells.append(GCell(s.value, "REORDER", 0, vb))
        for s in RESTART_STEPS:
            cells.append(GCell(s.value, "ENDPOINT_RESTART", 0, vb))
    return cells


def schedule_for(cell: GCell) -> List[FaultAction]:
    if cell.kind == "CONTROL":
        return []
    phase = P(cell.step)
    kind = K(cell.kind)
    if cell.kind in {k.value for k in LOSS_KINDS}:
        return [FaultAction(phase, a, kind, _target_for(phase, kind)) for a in range(1, cell.lost + 1)]
    return [FaultAction(phase, 1, kind, _target_for(phase, kind))]


def grid_definition() -> Dict[str, object]:
    return {
        "config": {"seed": CONFIG.seed, "ground_epoch": CONFIG.ground_epoch, "spacecraft_epoch": CONFIG.spacecraft_epoch,
                   "authority_epoch_floor": CONFIG.authority_epoch_floor, "max_transmissions": CONFIG.max_transmissions,
                   "candidate_lifetime_contacts": CONFIG.candidate_lifetime_contacts,
                   "compromise_active_keys": CONFIG.compromise_active_keys},
        "cell_ids": [c.cell_id for c in enumerate_cells()],
        "role_map": ROLE_MAP,
    }


def grid_sha256() -> str:
    return hashlib.sha256(json.dumps(grid_definition(), sort_keys=True).encode()).hexdigest()


FOOTER_MARK = "\n<!-- STUDY_G_FOOTER -->"


def protocol_body_sha256(path: Path) -> str:
    text = path.read_text()
    body = text.split(FOOTER_MARK)[0]
    return hashlib.sha256(body.encode()).hexdigest()


def run_cell(cell: GCell) -> Dict[str, object]:
    res = run_with_verification_budget(CONFIG, schedule_for(cell), cell.vbudget)
    res.pop("_event_log")
    row = {"cell_id": cell.cell_id, "arm": cell.arm, "step": cell.step or "-", "kind": cell.kind,
           "lost_transmissions": cell.lost, "verification_budget": cell.vbudget,
           "recovery_budget": CONFIG.max_transmissions}
    row.update(res)
    return row


def run_grid() -> List[Dict[str, object]]:
    return [run_cell(c) for c in enumerate_cells()]


def write_csv(rows, path) -> None:
    import csv
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        return ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--protocol", default="docs/study_g/STUDY_G_PROTOCOL.md")
    args = ap.parse_args(argv)
    proto = Path(args.protocol)
    footer = proto.read_text().split(FOOTER_MARK)[1] if FOOTER_MARK in proto.read_text() else ""
    p_sha, g_sha = protocol_body_sha256(proto), grid_sha256()
    if p_sha not in footer or g_sha not in footer:
        print("Protocol footer hashes do not match computed hashes; refusing to run.", file=sys.stderr)
        return 2
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = run_grid()
    res = out / "study_g_results.csv"
    write_csv(rows, res)
    manifest = {
        "study": "G (exploratory, post hoc, same-author, AI-implemented, not third-party pre-registered)",
        "protocol_body_sha256": p_sha, "grid_sha256": g_sha, "protocol_footer_matches": True,
        "cell_rows": len(rows), "results_csv_sha256": hashlib.sha256(res.read_bytes()).hexdigest(),
        "python": sys.version.split()[0], "platform": platform.platform(),
        "git_commit_base": _git("rev-parse", "HEAD"), "git_dirty_note": "study_g/ and docs/study_g/ are untracked additions",
    }
    (out / "run_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
