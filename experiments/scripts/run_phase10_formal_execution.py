#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from ttc_recovery.formal_execution import execute_formal_model


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SHA1 = "bee4a54f3ee3d4afc347c3240ec2d9e93b075104"
DEFAULT_VERSION = "1.7.4"
LOG_NAMES = (
    "phase10-java-version.log",
    "phase10-sany.log",
    "phase10-tlc-positive.log",
    "phase10-tlc-negative-control.log",
)


def print_failure_logs(output_dir: Path) -> None:
    for name in LOG_NAMES:
        path = output_dir / name
        if not path.is_file():
            continue
        print(f"\n===== {name} =====")
        print(path.read_text(encoding="utf-8"), end="")
        print(f"===== end {name} =====")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the Phase 10 SANY, positive TLC, and negative-control TLC gates."
    )
    parser.add_argument("--jar", type=Path, required=True, help="Path to pinned tla2tools.jar.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--java", default="java", help="Java executable.")
    parser.add_argument("--tool-version", default=DEFAULT_VERSION)
    parser.add_argument("--expected-sha1", default=DEFAULT_SHA1)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    try:
        report = execute_formal_model(
            jar_path=args.jar,
            output_dir=args.output_dir,
            repository_root=ROOT,
            java_command=args.java,
            expected_jar_sha1=args.expected_sha1,
            tool_version=args.tool_version,
            timeout_seconds=args.timeout_seconds,
        )
    except Exception:
        print_failure_logs(args.output_dir.resolve())
        raise

    positive = report["positive_model_check"]
    negative = report["negative_control"]
    print(
        "Phase 10 formal execution complete: "
        f"sany={report['sany']['status']}, "
        f"positive={positive['status']}, "
        f"negative_control={negative['status']}, "
        f"generated_states={positive['generated_states']}, "
        f"distinct_states={positive['distinct_states']}, "
        f"depth={positive['search_depth']}."
    )
    print(f"Output directory: {args.output_dir.resolve()}")
    print("Positive-model wording remains NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND.")
    print("The negative-control trace is intentional pipeline evidence, not a protocol flaw.")


if __name__ == "__main__":
    main()
