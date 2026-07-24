#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
DESIGN_PATH = ROOT / "spec" / "t1-provisional-design.json"
CATALOG_PATH = ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json"
TEST_PATH = ROOT / "tests" / "test_t1_controller.py"

EXPECTED_FLOW = [
    "RECOVERY_PREPARE",
    "RECOVERY_RESPONSE",
    "RECOVERY_COMMIT",
    "RECOVERY_CONFIRM",
    "TEST_COMMAND_AND_STATUS",
]


def load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> List[Dict[str, object]]:
    design = load_json(DESIGN_PATH)
    catalog = load_json(CATALOG_PATH)
    test_source = TEST_PATH.read_text(encoding="utf-8")

    if design.get("status") != "PROVISIONAL_INTERNAL_REVIEW_ONLY":
        raise SystemExit("T1 design must remain PROVISIONAL_INTERNAL_REVIEW_ONLY.")

    review = design.get("review_status", {})
    if review.get("independent_cryptography_review") != "NOT_YET_PERFORMED":
        raise SystemExit("Independent-review status changed without a completed review record.")
    if review.get("baseline_oracles") != "PENDING_INDEPENDENT_REVIEW":
        raise SystemExit("Baseline oracles must remain pending during Phase 06.")

    flow = [entry.get("phase") for entry in design.get("message_flow", [])]
    if flow != EXPECTED_FLOW:
        raise SystemExit(f"Unexpected provisional T1 flow: {flow!r}")

    oracle_rule = design.get("no_hidden_oracle_rule", {})
    if "spacecraft active epoch + 1" not in oracle_rule.get("spacecraft_selection", ""):
        raise SystemExit("Spacecraft target selection rule is missing.")
    if "recovery-authority epoch floor" not in oracle_rule.get("ground_proposal", ""):
        raise SystemExit("Ground proposal rule is missing the recovery-authority epoch floor.")

    stops = set(design.get("mandatory_external_review_stop_points", []))
    required_stops = {
        "before changing the Phase 05 oracle candidate to ACCEPTED or FROZEN",
        "before freezing the final experiment protocol or parameter ranges",
        "before manuscript submission or external security claims",
    }
    missing_stops = required_stops - stops
    if missing_stops:
        raise SystemExit(f"Missing mandatory external-review stop points: {sorted(missing_stops)}")

    cases = catalog.get("tests", [])
    ids = [case.get("id") for case in cases]
    names = [case.get("test") for case in cases]
    if len(cases) != 15:
        raise SystemExit(f"Expected 15 provisional T1 scenarios, found {len(cases)}.")
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate provisional T1 scenario IDs.")
    if len(names) != len(set(names)):
        raise SystemExit("Duplicate provisional T1 test names.")

    for case in cases:
        name = case.get("test")
        if not isinstance(name, str) or f"def {name}(" not in test_source:
            raise SystemExit(f"Scenario {case.get('id')} references missing test {name!r}.")

    return cases


def emit_markdown(cases: List[Dict[str, object]]) -> None:
    print("| ID | Scenario | Initial state | Faults | Expected alignment | Expected outcome |")
    print("|---|---|---|---|---|---|")
    for case in cases:
        faults = ", ".join(case.get("faults", [])) or "none"
        print(
            f"| {case['id']} | {case['name']} | {case['initial_alignment']} | "
            f"{faults} | {case['expected_alignment']} | {case['expected_outcome']} |"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the provisional Phase 06 T1 design.")
    parser.add_argument("--markdown", action="store_true", help="Print the scenario matrix.")
    args = parser.parse_args()

    cases = validate()
    if args.markdown:
        emit_markdown(cases)
    else:
        print(
            "Provisional T1 design valid: "
            f"{len(cases)} scenarios, status=PROVISIONAL_INTERNAL_REVIEW_ONLY."
        )


if __name__ == "__main__":
    main()
