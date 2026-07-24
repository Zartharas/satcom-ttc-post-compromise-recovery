from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from ttc_recovery.provisional_analysis import (
    build_analysis,
    load_phase07_results,
    sha256_file,
    verify_checksum_manifest,
    verify_metrics_csv,
    write_analysis_outputs,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run provisional Phase 08 descriptive aggregation and sensitivity "
            "analysis over preserved Phase 07 results."
        )
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--bundle-dir",
        type=Path,
        help=(
            "Preserved Phase 07 evidence directory containing the checksum "
            "manifest, JSON results, and metrics CSV."
        ),
    )
    source.add_argument(
        "--input-json",
        type=Path,
        help="Phase 07 results JSON when bundle verification is not requested.",
    )
    parser.add_argument(
        "--metrics-csv",
        type=Path,
        default=None,
        help="Optional Phase 07 metrics CSV to cross-check against the JSON.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/configs/phase-08-provisional.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for derived Phase 08 analysis outputs.",
    )
    return parser.parse_args()


def load_config(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("status") != "PROVISIONAL_INTERNAL_REVIEW_ONLY":
        raise ValueError("Phase 08 configuration must remain provisional.")
    if payload.get("analysis_scope") != "DESCRIPTIVE_AND_SENSITIVITY_SCAFFOLD_ONLY":
        raise ValueError("Phase 08 analysis scope is not the expected provisional scope.")
    return payload


def main() -> int:
    args = parse_args()
    config = load_config(args.config)

    bundle_verification = None
    csv_verification = None
    if args.bundle_dir is not None:
        bundle_dir = args.bundle_dir.expanduser().resolve()
        bundle_verification = verify_checksum_manifest(
            bundle_dir,
            manifest_name=str(config["source_bundle"]["checksum_manifest"]),
        )
        input_json = bundle_dir / str(config["source_bundle"]["results_json"])
        metrics_csv = bundle_dir / str(config["source_bundle"]["metrics_csv"])
    else:
        input_json = args.input_json.expanduser().resolve()
        metrics_csv = args.metrics_csv.expanduser().resolve() if args.metrics_csv else None

    payload = load_phase07_results(input_json)
    if metrics_csv is not None:
        csv_verification = verify_metrics_csv(payload["results"], metrics_csv)

    sensitivity = config["sensitivity_scaffold"]
    coverage = config["coverage_expectations"]
    analysis = build_analysis(
        payload,
        source_json_sha256=sha256_file(input_json),
        min_group_size=int(config["denominator_policy"]["minimum_group_size"]),
        required_faults=[str(value) for value in coverage["required_fault_kinds"]],
        required_phases=[str(value) for value in coverage["required_fault_phases"]],
        max_transmissions_values=[
            int(value) for value in sensitivity["max_transmissions"]
        ],
        candidate_lifetime_values=[
            int(value) for value in sensitivity["candidate_lifetime_contacts"]
        ],
        bundle_verification=bundle_verification,
        csv_verification=csv_verification,
    )
    paths = write_analysis_outputs(analysis, args.output_dir.expanduser().resolve())

    outcomes = Counter(
        str(row["outcome"]) for row in analysis["annotated_results"]
    )
    print(
        "Phase 08 provisional analysis complete: "
        f"{len(analysis['annotated_results'])} source schedules, "
        f"outcomes={dict(sorted(outcomes.items()))}, "
        f"trace_anomalies={len(analysis['trace_anomalies'])}, "
        f"sensitivity_rows={len(analysis['sensitivity']['rows'])}."
    )
    print(f"Output directory: {args.output_dir.expanduser().resolve()}")
    print(f"Derived checksum manifest: {paths['checksum_manifest']}")
    print(
        "Aggregates, diagnostic labels, and sensitivity results remain "
        "descriptive, provisional, and unreviewed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
