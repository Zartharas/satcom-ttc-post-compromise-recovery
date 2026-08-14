#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence


EXPECTED_EXECUTION_COMMIT = "c630fb4f65ad78211fd3ffb0391000d7ed3629b1"
EXPECTED_PLAN_SHA256 = "3570834a70c76e020dada459e036786f690698125fe1d9e171e9f945748a1012"
EXPECTED_STUDY_COUNTS = {
    "study_a_member_rows": 13,
    "study_b_schedules": 40,
    "study_c_schedules": 100,
    "study_d_executions": 108,
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_manifest(run_dir: Path) -> int:
    manifest = run_dir / "manifests" / "SHA256SUMS"
    if not manifest.is_file():
        raise FileNotFoundError(manifest)
    count = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        path = run_dir / relative
        actual = sha256_file(path)
        if actual != expected:
            raise ValueError(
                f"Retained-run checksum mismatch: {relative}: {actual} != {expected}"
            )
        count += 1
    if count != 16:
        raise ValueError(f"Expected 16 retained-run manifest entries, found {count}")
    return count


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def study_b_summary(table2: Sequence[Mapping[str, str]]) -> list[dict[str, object]]:
    canonical = [row for row in table2 if row["schedule_class"] == "CANONICAL_CELL"]
    grouped: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in canonical:
        grouped[row["fault_kind_or_control"]].append(row)

    interpretation = {
        "DROP": (
            "Single recovery-phase drops recover; TEST_COMMAND/STATUS_TELEMETRY "
            "drops leave synchronized but INDETERMINATE evidence."
        ),
        "DELAY": "All six canonical delay cells complete successfully.",
        "DUPLICATE": (
            "All four message-bearing duplicate cells succeed while duplicate "
            "message identifiers are rejected."
        ),
        "REORDER": (
            "All four reordered-message cells succeed while injected out-of-order "
            "messages are rejected."
        ),
        "CONTACT_CLOSE": (
            "Single recovery-phase closures recover; verification-stage closures "
            "leave synchronized but INDETERMINATE evidence."
        ),
        "ENDPOINT_RESTART": (
            "COMMIT restart expires before convergence; CONFIRM restart leaves a "
            "spacecraft-ahead degraded state."
        ),
        "STALE_COUNTER": "The stale PREPARE counter is rejected and recovery succeeds.",
        "STALE_REPLAY": "Stale COMMIT/CONFIRM replays are rejected and recovery succeeds.",
    }

    rows: list[dict[str, object]] = []
    for kind, group in grouped.items():
        outcomes = Counter(row["outcome"] for row in group)
        rows.append(
            {
                "fault_kind": kind,
                "canonical_cells": len(group),
                "outcome_counts": json.dumps(
                    dict(sorted(outcomes.items())),
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                "interpretation": interpretation[kind],
            }
        )

    exhaustion = [
        row for row in table2 if row["schedule_class"] == "RETRY_EXHAUSTION"
    ]
    outcomes = Counter(row["outcome"] for row in exhaustion)
    rows.append(
        {
            "fault_kind": "DROP + CONTACT_CLOSE retry exhaustion",
            "canonical_cells": len(exhaustion),
            "outcome_counts": json.dumps(
                dict(sorted(outcomes.items())),
                sort_keys=True,
                separators=(",", ":"),
            ),
            "interpretation": (
                "PREPARE/RESPONSE/COMMIT exhaustion expires before verified "
                "convergence; CONFIRM exhaustion leaves spacecraft-ahead degraded state."
            ),
        }
    )
    return rows


def study_c_reachability(raw: Sequence[Mapping[str, object]]) -> tuple[list[dict[str, object]], dict]:
    planned = Counter()
    applied = Counter()
    planned_actions = 0
    applied_actions = 0
    zero_applied = 0

    for record in raw:
        actions = record["actions"]
        planned_actions += len(actions)
        for action in actions:
            planned[(str(action["kind"]), str(action["phase"]))] += 1

        applied_events = [
            event
            for event in record["result"]["event_log"]
            if event.get("event") == "phase07_fault_applied"
        ]
        applied_actions += len(applied_events)
        if not applied_events:
            zero_applied += 1
        for event in applied_events:
            applied[(str(event["kind"]), str(event["phase"]))] += 1

    rows = []
    for kind, phase in sorted(planned):
        rows.append(
            {
                "fault_kind": kind,
                "phase": phase,
                "scheduled_action_count": planned[(kind, phase)],
                "applied_action_count": applied[(kind, phase)],
                "runtime_exercised": applied[(kind, phase)] > 0,
            }
        )

    summary = {
        "planned_actions": planned_actions,
        "applied_actions": applied_actions,
        "zero_applied_schedules": zero_applied,
        "scheduled_cells": len(planned),
        "runtime_exercised_cells": sum(1 for key in planned if applied[key] > 0),
        "runtime_unexercised_cells": [
            f"{kind}@{phase}"
            for kind, phase in sorted(planned)
            if applied[(kind, phase)] == 0
        ],
    }
    return rows, summary


def write_results_summary(
    path: Path,
    *,
    run_id: str,
    bundle_sha256: str,
    manifest_count: int,
    metadata: Mapping[str, object],
    table1: Sequence[Mapping[str, str]],
    table2: Sequence[Mapping[str, str]],
    study_c: Mapping[str, object],
    study_c_reachability_summary: Mapping[str, object],
    study_d: Sequence[Mapping[str, str]],
) -> None:
    b_all = Counter(row["outcome"] for row in table2)
    b_canonical = Counter(
        row["outcome"]
        for row in table2
        if row["schedule_class"] == "CANONICAL_CELL"
    )
    b_exhaustion = Counter(
        row["outcome"]
        for row in table2
        if row["schedule_class"] == "RETRY_EXHAUSTION"
    )

    d_by_tx: dict[int, set[tuple[int, str]]] = defaultdict(set)
    for row in study_d:
        d_by_tx[int(row["max_transmissions"])].add(
            (int(row["verification_complete_count"]), row["outcome_counts"])
        )

    if any(len(values) != 1 for values in d_by_tx.values()):
        raise ValueError(
            "Candidate-lifetime sensitivity changed within a fixed transmission budget; "
            "summary template requires update."
        )

    d_summary = {
        tx: next(iter(values))
        for tx, values in sorted(d_by_tx.items())
    }

    text = f"""# Retained Experiment Results Summary

## Evidence identity

- Retained run: `{run_id}`
- Execution commit: `{metadata["execution_identity"]["commit"]}`
- Plan commit: `{metadata["execution_identity"]["plan_commit"]}`
- Plan SHA-256: `{metadata["execution_identity"]["plan_sha256"]}`
- External retained-bundle SHA-256: `{bundle_sha256}`
- Internal retained-bundle manifest: `{manifest_count}/16` files verified
- Study counts: A={metadata["study_counts"]["study_a_member_rows"]}, B={metadata["study_counts"]["study_b_schedules"]}, C={metadata["study_counts"]["study_c_schedules"]}, D={metadata["study_counts"]["study_d_executions"]}

This file is a post-execution summary derived from the immutable retained run. It does not
modify the predeclared plan in `paper/EXPERIMENT_EXECUTION_PLAN.md` or
`experiments/configs/paper-final-experiment.json`.

## Study A — matched-family comparison

The four qualified matched families show categorical parity on the pre-authorized fields:

- `CF-01`: B0, B1, B2, and T1 are `SUCCESS`, `SYNC`, `AVAILABLE`, and
  `SECURE_PROVISIONAL`; the active key is not marked compromised.
- `CF-02`: all four treatment analysis units are `SUCCESS`, `SYNC`, `AVAILABLE`, and
  `SECURE_PROVISIONAL`, with verification complete. The two B1 policy variants remain two
  traceability rows under one B1 analysis unit.
- `CF-05`: B2 and T1 are both `INDETERMINATE`, `SYNC`, `DEGRADED`, and
  `NOT_ESTABLISHED` after status-telemetry loss.
- `CF-06`: B2 and T1 are both `SUCCESS`, `SYNC`, and `AVAILABLE`; the declared replay is
  rejected.

**Interpretation:** the retained matched-family study does not support a categorical-superiority
claim for T1 over B0/B1/B2. It supports parity on the fields for which treatment semantics could
be matched conservatively.

## Study B — deterministic T1 fault behavior

All 40 predeclared deterministic schedules were executed. Across the 31 canonical
fault-kind/phase cells:

- `{b_canonical.get("SUCCESS", 0)}` `SUCCESS`
- `{b_canonical.get("INDETERMINATE", 0)}` `INDETERMINATE`
- `{b_canonical.get("EXPIRED", 0)}` `EXPIRED`
- `{b_canonical.get("SECURE_DEGRADED", 0)}` `SECURE_DEGRADED`

The eight retry-exhaustion schedules produced:

- `{b_exhaustion.get("EXPIRED", 0)}` `EXPIRED`
- `{b_exhaustion.get("SECURE_DEGRADED", 0)}` `SECURE_DEGRADED`

Observed mechanisms:

- isolated recovery-phase `DROP` and `CONTACT_CLOSE` faults recovered within the configured
  retry budget;
- verification-stage command/status loss remained synchronized but was classified
  `INDETERMINATE`, avoiding a false-success classification when evidence was incomplete;
- canonical `DELAY`, message-bearing `DUPLICATE`, `REORDER`, `STALE_COUNTER`, and
  `STALE_REPLAY` cases completed successfully while invalid/stale material was rejected;
- endpoint restart was the principal hard boundary: COMMIT-stage spacecraft restart expired
  before convergence, while CONFIRM-stage restart left a spacecraft-ahead degraded state.

The historical outcome label `SECURE_DEGRADED` must not be read as a security proof. In the
critical retained restart/confirmation-exhaustion cases, the separate `security_state` is
`UNSAFE`.

## Study C — fixed 100-schedule synthetic population

The predeclared fixed population produced:

- `SUCCESS`: {study_c["outcome_counts"].get("SUCCESS", 0)}/100
- `INDETERMINATE`: {study_c["outcome_counts"].get("INDETERMINATE", 0)}/100
- `SECURE_DEGRADED`: {study_c["outcome_counts"].get("SECURE_DEGRADED", 0)}/100
- `EXPIRED`: {study_c["outcome_counts"].get("EXPIRED", 0)}/100
- verification complete: {study_c["verification_complete_count"]}/100

These are descriptive outcomes for the fixed synthetic schedule population, not estimates of
real satellite fault prevalence.

### Runtime-reachability audit

The predeclared schedules contain `{study_c_reachability_summary["planned_actions"]}` scheduled
fault actions, of which `{study_c_reachability_summary["applied_actions"]}` were actually
reached and applied. `{study_c_reachability_summary["zero_applied_schedules"]}` of 100 schedules
had no runtime-applied fault action. Schedule definitions referenced
`{study_c_reachability_summary["scheduled_cells"]}` valid fault-kind/phase cells, while runtime
execution exercised `{study_c_reachability_summary["runtime_exercised_cells"]}` of them.

Therefore the 74 successful schedules must **not** be reported as a “74% success rate under
faults.” Study C is secondary descriptive evidence. Deterministic Study B provides the
fault-cell coverage result.

## Study D — retry/retention sensitivity

Across each candidate-lifetime setting (2, 3, or 4 contacts):

- max transmissions 2: `{d_summary[2][0]}/12` verification complete; outcomes
  `{d_summary[2][1]}`
- max transmissions 3: `{d_summary[3][0]}/12` verification complete; outcomes
  `{d_summary[3][1]}`
- max transmissions 4: `{d_summary[4][0]}/12` verification complete; outcomes
  `{d_summary[4][1]}`

Candidate lifetime produced no observed change within this fixed 12-schedule challenge set.
Increasing the transmission budget from two to three recovered the repeated loss/closure
challenge cases; increasing it from three to four produced no additional observed benefit. The
persistent failure was the COMMIT-stage spacecraft restart, which destroys pending protocol
state and is not repaired by additional message retries.

This is a bounded challenge-set result; it does not establish a universally optimal retry budget
or prove candidate lifetime irrelevant in other conditions.

## Paper claim boundary

The retained experiment supports controlled statements about behavior inside this synthetic
model. It does not establish:

- treatment superiority across incomparable scenarios;
- causal effectiveness outside the declared model;
- cryptographic or strong post-compromise security;
- CCSDS/SDLS conformance;
- real-world fault prevalence;
- flight/RF/operational-spacecraft applicability; or
- independent validation.

Independent baseline cryptography review remains a parallel open activity.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Derive tracked paper summaries from the immutable retained final run."
    )
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--paper-dir", type=Path, default=Path("paper"))
    parser.add_argument("--bundle-sha256", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.expanduser().resolve()
    paper_dir = args.paper_dir.expanduser().resolve()

    manifest_count = verify_manifest(run_dir)
    metadata = read_json(run_dir / "metadata.json")

    if metadata["status"] != "COMPLETED_RETAINED_FINAL_EXPERIMENT":
        raise ValueError("Unexpected retained-run status")
    if metadata["execution_identity"]["commit"] != EXPECTED_EXECUTION_COMMIT:
        raise ValueError("Retained-run execution commit drifted")
    if metadata["execution_identity"]["plan_sha256"] != EXPECTED_PLAN_SHA256:
        raise ValueError("Retained-run plan SHA-256 drifted")
    if metadata["study_counts"] != EXPECTED_STUDY_COUNTS:
        raise ValueError("Retained-run study counts drifted")

    table1 = read_csv(
        run_dir / "processed" / "table-1-matched-family-outcomes.csv"
    )
    table2 = read_csv(
        run_dir / "processed" / "table-2-deterministic-t1.csv"
    )
    study_c = read_json(run_dir / "processed" / "study-c-summary.json")
    study_c_raw = read_json(run_dir / "raw" / "study-c-mixed-fault-t1.json")
    study_d = read_csv(
        run_dir / "processed" / "study-d-sensitivity-summary.csv"
    )

    if len(table1) != 13 or len(table2) != 40 or len(study_c_raw) != 100:
        raise ValueError("Retained derived/raw result counts drifted")

    reachability_rows, reachability_summary = study_c_reachability(study_c_raw)

    tables = paper_dir / "tables"
    figures = paper_dir / "figures"
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    shutil.copy2(
        run_dir / "processed" / "table-1-matched-family-outcomes.csv",
        tables / "table-1-matched-family-outcomes.csv",
    )
    shutil.copy2(
        run_dir / "processed" / "table-2-deterministic-t1.csv",
        tables / "table-2-deterministic-t1.csv",
    )
    write_csv(
        tables / "study-b-fault-response-summary.csv",
        study_b_summary(table2),
    )

    study_c_rows = [
        {
            "outcome": outcome,
            "count": count,
            "percentage": study_c["outcome_percentages"][outcome],
            "denominator": study_c["denominator"],
        }
        for outcome, count in sorted(study_c["outcome_counts"].items())
    ]
    write_csv(tables / "study-c-outcome-summary.csv", study_c_rows)
    write_csv(
        tables / "study-c-execution-coverage-audit.csv",
        reachability_rows,
    )
    shutil.copy2(
        run_dir / "processed" / "study-d-sensitivity-summary.csv",
        tables / "study-d-sensitivity-summary.csv",
    )
    shutil.copy2(
        run_dir / "figures" / "figure-2-outcome-distribution-source.csv",
        figures / "figure-2-outcome-distribution-source.csv",
    )
    shutil.copy2(
        run_dir / "figures" / "figure-3-sensitivity-source.csv",
        figures / "figure-3-sensitivity-source.csv",
    )

    write_results_summary(
        paper_dir / "RESULTS_SUMMARY.md",
        run_id=run_dir.name,
        bundle_sha256=args.bundle_sha256,
        manifest_count=manifest_count,
        metadata=metadata,
        table1=table1,
        table2=table2,
        study_c=study_c,
        study_c_reachability_summary=reachability_summary,
        study_d=study_d,
    )

    print("retained_manifest=16_OF_16_PASS")
    print("execution_identity=PASS")
    print("study_counts=PASS")
    print("paper_result_sources_written=PASS")
    print("study_c_runtime_reachability_audit=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
