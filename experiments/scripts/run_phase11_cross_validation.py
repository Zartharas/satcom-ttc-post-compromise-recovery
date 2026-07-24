#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from ttc_recovery.formal_cross_validation import execute_cross_validation


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SHA1 = "bee4a54f3ee3d4afc347c3240ec2d9e93b075104"
DEFAULT_VERSION = "1.7.4"


def _print_logs(output_dir: Path) -> None:
    for path in sorted(output_dir.glob("phase11-*.log")):
        print(f"\n===== {path.name} =====")
        print(path.read_text(encoding="utf-8"), end="")
        print(f"===== end {path.name} =====")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run the Phase 11 formal/Python success-trace comparison and bounded TLC panel."
        )
    )
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--java", default="java")
    parser.add_argument("--tool-version", default=DEFAULT_VERSION)
    parser.add_argument("--expected-sha1", default=DEFAULT_SHA1)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    try:
        report = execute_cross_validation(
            jar_path=args.jar,
            output_dir=args.output_dir,
            repository_root=ROOT,
            java_command=args.java,
            expected_jar_sha1=args.expected_sha1,
            tool_version=args.tool_version,
            timeout_seconds=args.timeout_seconds,
        )
    except Exception:
        _print_logs(args.output_dir)
        raise

    witness = report["success_witness"]
    comparison = report["trace_comparison"]
    bounds = report["bound_expansion"]
    print(
        "Phase 11 cross-validation complete: "
        f"status={report['status']}, "
        f"witness_states={witness['trace_state_count']}, "
        f"trace_mismatches={comparison['mismatch_count']}, "
        f"bound_cases={bounds['case_count']}, "
        f"baseline_reproduced={bounds['baseline_reproduced']}."
    )
    print(f"Output directory: {args.output_dir.resolve()}")
    print("Agreement is limited to the declared abstract projection and finite bounds.")
    print("Publication evidence status remains NOT_PERMITTED.")


if __name__ == "__main__":
    main()
