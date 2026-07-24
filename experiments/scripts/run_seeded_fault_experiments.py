from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from ttc_recovery.fault_metrics import (
    FaultKind,
    SeededExperimentConfig,
    run_seeded_experiment,
    write_results,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run provisional seeded T1 fault experiments."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/configs/phase-07-provisional.json"),
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=None,
    )
    return parser.parse_args()


def load_config(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("status") != "PROVISIONAL_INTERNAL_REVIEW_ONLY":
        raise ValueError("Phase 07 configuration must remain provisional.")
    return payload


def main() -> int:
    args = parse_args()
    payload = load_config(args.config)
    allowed_faults = tuple(FaultKind(name) for name in payload["allowed_faults"])
    results = []
    for seed in payload["seeds"]:
        config = SeededExperimentConfig(
            seed=int(seed),
            ground_epoch=int(payload["ground_epoch"]),
            spacecraft_epoch=int(payload["spacecraft_epoch"]),
            authority_epoch_floor=int(payload["authority_epoch_floor"]),
            max_transmissions=int(payload["max_transmissions"]),
            candidate_lifetime_contacts=int(
                payload["candidate_lifetime_contacts"]
            ),
            max_faults=int(payload["max_faults"]),
            compromise_active_keys=bool(payload["compromise_active_keys"]),
            allowed_faults=allowed_faults,
        )
        results.append(run_seeded_experiment(config))

    json_output = args.json_output or Path(payload["outputs"]["json"])
    csv_output = args.csv_output or Path(payload["outputs"]["csv"])
    write_results(results, json_output, csv_output)

    outcomes = Counter(result.metrics.outcome for result in results)
    print(
        "Phase 07 provisional run complete: "
        f"{len(results)} schedules, outcomes={dict(sorted(outcomes.items()))}."
    )
    print(f"JSON: {json_output}")
    print(f"CSV: {csv_output}")
    print("Parameters and results remain provisional and unreviewed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
