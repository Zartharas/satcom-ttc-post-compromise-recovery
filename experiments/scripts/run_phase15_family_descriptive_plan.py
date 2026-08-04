#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ttc_recovery.family_descriptive_plan import (
    build_family_descriptive_plan,
    verify_family_descriptive_manifest,
    write_family_descriptive_plan,
)
from ttc_recovery.matched_family_population import (
    execute_matched_family_population,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAN = (
    ROOT / "experiments" / "configs" / "phase-15-family-descriptive-plan.json"
)
DEFAULT_MATRIX = ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"
DEFAULT_POPULATION_CONFIG = (
    ROOT / "experiments" / "configs" / "phase-15-matched-family-population.json"
)
DEFAULT_BASELINE_CATALOG = ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"
DEFAULT_T1_CATALOG = ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the outcome-blind WP15-D4 family observation and "
            "denominator freeze candidate without producing comparative results."
        )
    )
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument(
        "--population-config",
        type=Path,
        default=DEFAULT_POPULATION_CONFIG,
    )
    parser.add_argument(
        "--baseline-catalog",
        type=Path,
        default=DEFAULT_BASELINE_CATALOG,
    )
    parser.add_argument("--t1-catalog", type=Path, default=DEFAULT_T1_CATALOG)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan_path = args.plan.expanduser().resolve()
    matrix_path = args.matrix.expanduser().resolve()
    population_config_path = args.population_config.expanduser().resolve()
    baseline_catalog_path = args.baseline_catalog.expanduser().resolve()
    t1_catalog_path = args.t1_catalog.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    for path in (
        plan_path,
        matrix_path,
        population_config_path,
        baseline_catalog_path,
        t1_catalog_path,
    ):
        if not path.is_file():
            raise FileNotFoundError(path)

    plan_config = load_json(plan_path)
    matrix = load_json(matrix_path)
    population_config = load_json(population_config_path)
    population_payload = execute_matched_family_population(
        population_config,
        matrix,
        load_json(baseline_catalog_path),
        load_json(t1_catalog_path),
    )
    payload = build_family_descriptive_plan(
        plan_config,
        matrix,
        population_config,
        population_payload,
    )

    json_path = output_dir / "phase-15-family-descriptive-plan-candidate.json"
    member_csv_path = output_dir / "phase-15-family-member-registry.csv"
    analysis_unit_csv_path = output_dir / "phase-15-family-analysis-units.csv"
    family_plan_csv_path = output_dir / "phase-15-family-observation-plans.csv"
    manifest_path = output_dir / "phase-15-family-descriptive-plan.sha256"

    write_family_descriptive_plan(
        payload,
        json_path,
        member_csv_path,
        analysis_unit_csv_path,
        family_plan_csv_path,
        manifest_path,
    )
    verify_family_descriptive_manifest(output_dir, manifest_path)

    print(
        "Phase 15 family descriptive plan candidate complete: "
        f"families={payload['family_count']}, "
        f"member_rows={payload['member_row_count']}, "
        f"analysis_units={payload['analysis_unit_count']}, "
        f"cutoffs={payload['observation_cutoff_count']}, "
        f"denominator_candidates={payload['denominator_candidate_count']}, "
        f"status={payload['status']}."
    )
    print("projected_metric_values_read=false")
    print("family_specific_descriptive_comparison=NOT_YET_AUTHORIZED")
    print("success_rate_denominator=NOT_DEFINED")
    print("pooled_cross_treatment_aggregation=NOT_PERMITTED")
    print("publication_evidence=false")
    print("plan_manifest=VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
