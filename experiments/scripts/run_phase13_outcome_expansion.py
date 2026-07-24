from __future__ import annotations

import argparse
from pathlib import Path

from ttc_recovery.formal_outcome_expansion import execute_outcome_expansion


DEFAULT_TLA_TOOLS_SHA1 = "bee4a54f3ee3d4afc347c3240ec2d9e93b075104"
DEFAULT_TLA_TOOLS_VERSION = "1.7.4"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate that the Phase 12 baseline model remains unchanged while an opt-in "
            "Phase 13 module adds diagnostic witnesses for DIVERGED, AVAILABLE_UNSAFE, and LOCKED."
        )
    )
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--expected-jar-sha1", default=DEFAULT_TLA_TOOLS_SHA1)
    parser.add_argument("--tool-version", default=DEFAULT_TLA_TOOLS_VERSION)
    parser.add_argument("--java-command", default="java")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[2]
    report = execute_outcome_expansion(
        jar_path=args.jar,
        output_dir=args.output_dir,
        repository_root=repository_root,
        expected_jar_sha1=args.expected_jar_sha1,
        tool_version=args.tool_version,
        java_command=args.java_command,
        timeout_seconds=args.timeout_seconds,
    )

    witnesses = report["expanded_outcomes"]["cases"]
    mismatches = sum(int(row["mismatch_count"]) for row in witnesses)
    print(
        "Phase 13 outcome expansion complete: "
        f"status={report['status']}, "
        f"baseline={report['baseline_regression']['status']}, "
        f"expanded_witnesses={len(witnesses)}, "
        f"trace_mismatches={mismatches}."
    )
    print(f"Output directory: {args.output_dir.resolve()}")
    print(
        "The original T1Recovery.tla model remains the preserved baseline; expanded outcomes are "
        "diagnostic-only and opt-in."
    )
    print("Model completeness, implementation equivalence, and publication claims remain NOT_PERMITTED.")


if __name__ == "__main__":
    main()
