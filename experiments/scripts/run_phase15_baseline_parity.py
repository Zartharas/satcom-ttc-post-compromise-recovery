#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from ttc_recovery.baseline_metrics import (
    PARITY_STATUS,
    run_baseline_catalog,
    write_baseline_results,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "experiments" / "configs" / "phase-15-baseline-parity.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run deterministic B0/B1/B2 catalog scenarios with the shared "
            "Phase 15 metric-parity schema."
        )
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--csv-output", type=Path, default=None)
    return parser.parse_args()


def load_config(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("status") != "PROVISIONAL_INTERNAL_REVIEW_ONLY":
        raise ValueError("Baseline parity configuration must remain provisional.")
    if payload.get("metric_parity_status") != PARITY_STATUS:
        raise ValueError("Unexpected baseline metric-parity status.")
    if payload.get("run_class") != "PILOT_INTERNAL_VALIDATION_ONLY":
        raise ValueError("Baseline parity runner is restricted to the pilot class.")
    return payload


def main() -> int:
    args = parse_args()
    config_path = args.config.expanduser().resolve()
    config = load_config(config_path)

    catalog_path = ROOT / str(config["catalog"])
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    entries = catalog["tests"]
    expected_ids = [str(value) for value in config["scenario_ids"]]
    actual_ids = [str(entry["id"]) for entry in entries]
    if actual_ids != expected_ids:
        raise ValueError("Baseline catalog order or population drifted.")

    results = run_baseline_catalog(entries)
    json_output = args.json_output or ROOT / str(config["outputs"]["json"])
    csv_output = args.csv_output or ROOT / str(config["outputs"]["csv"])
    write_baseline_results(results, json_output, csv_output)

    outcomes = Counter(result.metrics.outcome for result in results)
    treatments = Counter(result.treatment for result in results)
    print(
        "Phase 15 baseline metric parity run complete: "
        f"scenarios={len(results)}, treatments={dict(sorted(treatments.items()))}, "
        f"outcomes={dict(sorted(outcomes.items()))}."
    )
    print(f"JSON: {json_output}")
    print(f"CSV: {csv_output}")
    print(f"metric_parity_status={PARITY_STATUS}")
    print("publication_evidence=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
