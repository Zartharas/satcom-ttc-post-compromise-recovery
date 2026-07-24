#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "phase-11-formal-python-cross-validation.json"
TLA_PATH = ROOT / "formal" / "tla" / "T1Recovery.tla"
WITNESS_CONFIG = ROOT / "formal" / "tla" / "SuccessWitness.cfg"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Phase 11 validation failed: {message}")


def main() -> None:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    tla = TLA_PATH.read_text(encoding="utf-8")
    witness_cfg = WITNESS_CONFIG.read_text(encoding="utf-8")

    require(spec["phase"] == "Phase 11", "phase identifier mismatch")
    require(
        spec["status"] == "PROVISIONAL_INTERNAL_REVIEW_ONLY",
        "status must remain provisional",
    )
    require(
        spec["source_phase"]["source_commit"]
        == "a020615ed5c3a9cbe45073c2e4afce8812a2fb6e",
        "Phase 10 evidence commit changed",
    )

    toolchain = spec["toolchain"]
    require(toolchain["version"] == "1.7.4", "TLA+ tool version drifted")
    require(
        toolchain["official_sha1"]
        == "bee4a54f3ee3d4afc347c3240ec2d9e93b075104",
        "official tool checksum drifted",
    )
    require(toolchain["worker_count"] == 1, "worker count must remain one")

    witness = spec["success_witness"]
    expected_actions = [
        "Init",
        "Prepare",
        "SelectCandidate",
        "Commit",
        "Confirm",
        "AcceptCommand",
        "ReceiveStatus",
        "Verify",
    ]
    require(
        witness["testing_only_false_invariant"] == "ReachabilityWitnessNoSuccess",
        "success witness property changed",
    )
    require(witness["expected_actions"] == expected_actions, "success witness path changed")
    require("ReachabilityWitnessNoSuccess" in tla, "TLA witness property missing")
    require(
        "ReachabilityWitnessNoSuccess" in witness_cfg,
        "success witness configuration missing property",
    )

    projection = spec["trace_projection"]
    require(
        projection["status_on_match"] == "MATCH_WITHIN_DECLARED_ABSTRACTION",
        "trace match wording changed",
    )
    require(
        projection["status_on_mismatch"] == "MISMATCH_REQUIRES_REVIEW",
        "trace mismatch wording changed",
    )
    require(
        projection["equivalence_claim"] == "NOT_PERMITTED",
        "implementation equivalence claim became permitted",
    )
    require(len(projection["comparison_fields"]) == 16, "comparison field count changed")

    panel = spec["bound_panel"]
    cases = panel["cases"]
    require(len(cases) == 5, "bound panel must contain five cases")
    require(len({case["id"] for case in cases}) == 5, "bound case IDs are not unique")
    require(
        [case["id"] for case in cases]
        == ["attempts-1", "base-3-6", "attempts-5", "epoch-4", "epoch-8"],
        "bound panel order changed",
    )
    for case in cases:
        require((ROOT / case["config"]).is_file(), f"missing bound config {case['config']}")

    baseline = panel["baseline_reproduction_required"]
    require(
        baseline
        == {
            "generated_states": 50,
            "distinct_states": 28,
            "queued_states": 0,
            "search_depth": 10,
        },
        "Phase 10 baseline reproduction target changed",
    )

    outputs = spec["required_outputs"]
    require(len(outputs) == 13, "required output count changed")
    require(
        "phase11-derived-bundle.sha256" in outputs,
        "derived checksum manifest missing",
    )

    review = spec["review_status"]
    require(
        review["implementation_equivalence_claim"] == "NOT_PERMITTED",
        "implementation equivalence claim became permitted",
    )
    require(
        review["publication_evidence_status"] == "NOT_PERMITTED",
        "publication evidence became permitted",
    )
    require(
        len(spec["mandatory_external_review_stop_points"]) >= 6,
        "external review stop points are incomplete",
    )

    print(
        "Phase 11 cross-validation design valid: "
        f"actions={len(expected_actions)}, fields={len(projection['comparison_fields'])}, "
        f"bound_cases={len(cases)}, outputs={len(outputs)}, "
        f"status={spec['status']}."
    )


if __name__ == "__main__":
    main()
