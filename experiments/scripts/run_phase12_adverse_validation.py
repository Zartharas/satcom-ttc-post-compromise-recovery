from __future__ import annotations

import argparse
from pathlib import Path

from ttc_recovery.formal_adverse_validation import execute_adverse_validation


DEFAULT_TLA_TOOLS_SHA1 = "bee4a54f3ee3d4afc347c3240ec2d9e93b075104"
DEFAULT_TLA_TOOLS_VERSION = "1.7.4"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Capture Phase 12 adverse-outcome TLC witnesses, replay them through the Python "
            "controller, and diagnose currently absent outcomes without impossibility claims."
        )
    )
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--expected-jar-sha1",
        default=DEFAULT_TLA_TOOLS_SHA1,
    )
    parser.add_argument("--tool-version", default=DEFAULT_TLA_TOOLS_VERSION)
    parser.add_argument("--java-command", default="java")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[2]
    report = execute_adverse_validation(
        jar_path=args.jar,
        output_dir=args.output_dir,
        repository_root=repository_root,
        expected_jar_sha1=args.expected_jar_sha1,
        tool_version=args.tool_version,
        java_command=args.java_command,
        timeout_seconds=args.timeout_seconds,
    )

    witnesses = report["captured_adverse_witnesses"]
    absent = report["unreached_outcomes"]
    mismatch_count = sum(int(row["mismatch_count"]) for row in witnesses)
    print(
        "Phase 12 adverse validation complete: "
        f"status={report['status']}, "
        f"captured_witnesses={len(witnesses)}, "
        f"trace_mismatches={mismatch_count}, "
        f"unreached_outcomes={len(absent)}."
    )
    print(f"Output directory: {args.output_dir.resolve()}")
    print(
        "Unreached outcomes remain NOT_REACHED_WITHIN_RECORDED_BOUND and are diagnosed "
        "as absent from current transition assignments, not impossible."
    )
    print("Publication evidence status remains NOT_PERMITTED.")


if __name__ == "__main__":
    main()
