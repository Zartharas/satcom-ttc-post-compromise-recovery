#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ttc_recovery.matched_family_population import (
    execute_matched_family_population,
    verify_derived_manifest,
    write_matched_family_population,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = (
    ROOT / "experiments" / "configs" / "phase-15-matched-family-population.json"
)
DEFAULT_MATRIX = ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"
DEFAULT_BASELINE_CATALOG = ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"
DEFAULT_T1_CATALOG = ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Execute the four qualified WP15-D2 families and emit a "
            "non-pooled WP15-D3 member-level derived dataset."
        )
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
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
    config_path = args.config.expanduser().resolve()
    matrix_path = args.matrix.expanduser().resolve()
    baseline_catalog_path = args.baseline_catalog.expanduser().resolve()
    t1_catalog_path = args.t1_catalog.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    for path in (
        config_path,
        matrix_path,
        baseline_catalog_path,
        t1_catalog_path,
    ):
        if not path.is_file():
            raise FileNotFoundError(path)

    payload = execute_matched_family_population(
        load_json(config_path),
        load_json(matrix_path),
        load_json(baseline_catalog_path),
        load_json(t1_catalog_path),
    )

    json_path = output_dir / "phase-15-matched-family-population.json"
    member_csv_path = output_dir / "phase-15-matched-family-members.csv"
    denominator_csv_path = (
        output_dir / "phase-15-matched-family-denominators.csv"
    )
    manifest_path = output_dir / "phase-15-matched-family-derived.sha256"

    write_matched_family_population(
        payload,
        json_path,
        member_csv_path,
        denominator_csv_path,
        manifest_path,
    )
    verify_derived_manifest(output_dir, manifest_path)

    print(
        "Phase 15 matched-family population complete: "
        f"families={payload['family_count']}, "
        f"member_rows={payload['member_row_count']}, "
        f"analysis_units={payload['analysis_unit_count']}, "
        f"status={payload['status']}."
    )
    print(f"JSON: {json_path}")
    print(f"Members CSV: {member_csv_path}")
    print(f"Denominators CSV: {denominator_csv_path}")
    print("family_specific_descriptive_comparison=NOT_YET_AUTHORIZED")
    print("pooled_cross_treatment_aggregation=NOT_PERMITTED")
    print("publication_evidence=false")
    print("derived_manifest=VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
