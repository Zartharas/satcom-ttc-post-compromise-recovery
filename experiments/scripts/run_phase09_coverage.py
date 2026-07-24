from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from ttc_recovery.formal_coverage import build_phase09_bundle, write_phase09_outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run provisional Phase 09 adversarial coverage and bounded reachability analysis."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/processed/phase-09-provisional"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bundle = build_phase09_bundle()
    paths = write_phase09_outputs(bundle, args.output_dir)
    outcomes = Counter(row["outcome"] for row in bundle["coverage_rows"])
    reached_states = sum(
        row["reachability"] == "REACHED"
        for row in bundle["reachability"]["states"]
    )
    reached_outcomes = sum(
        row["reachability"] == "REACHED"
        for row in bundle["reachability"]["outcomes"]
    )
    print(
        "Phase 09 provisional coverage complete: "
        f"{len(bundle['coverage_rows'])} schedules, outcomes={dict(sorted(outcomes.items()))}, "
        f"reached_states={reached_states}/6, reached_outcomes={reached_outcomes}/7."
    )
    print(f"Output directory: {args.output_dir}")
    print(f"Derived checksum manifest: {paths['checksum_manifest']}")
    print(
        "Unreached states or outcomes are labeled NOT_REACHED_WITHIN_PROVISIONAL_BOUND; "
        "they are not claimed impossible."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
