from __future__ import annotations

import json
from pathlib import Path


EXPECTED_STATUS = "PROVISIONAL_INTERNAL_REVIEW_ONLY"
EXPECTED_TOOL_VERSION = "1.7.4"
EXPECTED_SHA1 = "bee4a54f3ee3d4afc347c3240ec2d9e93b075104"
EXPECTED_CAPTURED = {"INDETERMINATE", "SECURE_DEGRADED", "EXPIRED"}
EXPECTED_ABSENT = {"DIVERGED", "AVAILABLE_UNSAFE", "LOCKED"}
EXPECTED_FIELDS = {
    "gMode",
    "sMode",
    "gEpoch",
    "sEpoch",
    "gPrevEpoch",
    "sPrevEpoch",
    "candidateEpoch",
    "pending",
    "receipt",
    "attempts",
    "activationCount",
    "commandAccepted",
    "statusSeen",
    "statusDropped",
    "verified",
    "outcome",
}


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    spec_path = root / "spec" / "phase-12-adverse-outcome-witnesses.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    if spec["status"] != EXPECTED_STATUS:
        raise SystemExit("Phase 12 status must remain provisional.")
    if spec["toolchain"]["tla_tools_version"] != EXPECTED_TOOL_VERSION:
        raise SystemExit("Phase 12 tool version drifted.")
    if spec["toolchain"]["official_jar_sha1"] != EXPECTED_SHA1:
        raise SystemExit("Phase 12 official JAR checksum drifted.")
    if spec["toolchain"]["workers"] != 1:
        raise SystemExit("Phase 12 must retain one TLC worker for trace reproducibility.")

    projection = spec["projection"]
    if projection["field_count"] != 16 or set(projection["fields"]) != EXPECTED_FIELDS:
        raise SystemExit("Phase 12 projection must contain the declared 16 unique fields.")
    if projection["match_status"] != "MATCH_WITHIN_DECLARED_ABSTRACTION":
        raise SystemExit("Phase 12 match status drifted.")
    if projection["mismatch_status"] != "MISMATCH_REQUIRES_REVIEW":
        raise SystemExit("Phase 12 mismatch status drifted.")

    captured = spec["captured_witnesses"]
    absent = spec["absence_diagnostics"]
    if {row["outcome"] for row in captured} != EXPECTED_CAPTURED:
        raise SystemExit("Phase 12 captured-outcome set drifted.")
    if {row["outcome"] for row in absent} != EXPECTED_ABSENT:
        raise SystemExit("Phase 12 absent-outcome set drifted.")

    tla_text = (root / "formal" / "tla" / "T1Recovery.tla").read_text(encoding="utf-8")
    for row in captured + absent:
        config_path = root / row["config"]
        if not config_path.is_file():
            raise SystemExit(f"Missing Phase 12 config: {row['config']}")
        config_text = config_path.read_text(encoding="utf-8")
        if row["property"] not in tla_text or row["property"] not in config_text:
            raise SystemExit(f"Missing Phase 12 reachability property: {row['property']}")

    for row in absent:
        if row["expected_status"] != "NOT_REACHED_WITHIN_RECORDED_BOUND":
            raise SystemExit("Absent outcomes must use bounded non-reachability language.")
        if row["expected_diagnosis"] != "ABSENT_FROM_CURRENT_TRANSITION_ASSIGNMENTS":
            raise SystemExit("Absent outcomes must retain the abstraction-gap diagnosis.")
        assignment = f'outcome\' = "{row["outcome"]}"'
        if assignment in tla_text:
            raise SystemExit(
                f"Outcome {row['outcome']} now has a transition assignment and requires review."
            )

    if len(spec["required_outputs"]) != 17:
        raise SystemExit("Phase 12 required-output count drifted.")
    required_output_set = set(spec["required_outputs"])
    if "phase12-derived-bundle.sha256" not in required_output_set:
        raise SystemExit("Phase 12 derived checksum manifest is required.")

    boundary_values = {
        spec["formal_model_completeness_claim"],
        spec["implementation_equivalence_claim"],
        spec["cryptographic_security_claim"],
        spec["publication_evidence_status"],
    }
    if boundary_values != {"NOT_PERMITTED"}:
        raise SystemExit("Phase 12 claim boundaries must remain NOT_PERMITTED.")
    if spec["baseline_review_status"] != "PENDING_INDEPENDENT_REVIEW":
        raise SystemExit("Independent-review gate must remain open.")

    print(
        "Phase 12 adverse-outcome design valid: "
        f"captured={len(captured)}, absent={len(absent)}, fields={projection['field_count']}, "
        f"outputs={len(spec['required_outputs'])}, status={spec['status']}."
    )


if __name__ == "__main__":
    main()
