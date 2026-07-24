from __future__ import annotations

import hashlib
import json
from pathlib import Path


EXPECTED_STATUS = "PROVISIONAL_INTERNAL_REVIEW_ONLY"
EXPECTED_TOOL_VERSION = "1.7.4"
EXPECTED_SHA1 = "bee4a54f3ee3d4afc347c3240ec2d9e93b075104"
EXPECTED_BASELINE_SHA256 = "c2a97fa0eb93b7b84a2109be67d673a0199b82e52b8baf67f16d5b137e0da754"
EXPECTED_OUTCOMES = {"DIVERGED", "AVAILABLE_UNSAFE", "LOCKED"}
EXPECTED_CAUSES = {"NONE", "CANDIDATE_KNOWN", "CONFIRM_LOSS", "SENDER_STATE_DELETED"}
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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    spec_path = root / "spec" / "phase-13-abstraction-gap-outcomes.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    if spec["status"] != EXPECTED_STATUS:
        raise SystemExit("Phase 13 status must remain provisional.")
    if spec["toolchain"]["tla_tools_version"] != EXPECTED_TOOL_VERSION:
        raise SystemExit("Phase 13 tool version drifted.")
    if spec["toolchain"]["official_jar_sha1"] != EXPECTED_SHA1:
        raise SystemExit("Phase 13 official JAR checksum drifted.")
    if spec["toolchain"]["workers"] != 1:
        raise SystemExit("Phase 13 must retain one TLC worker for trace reproducibility.")

    baseline = spec["baseline_preservation"]
    baseline_path = root / baseline["module"]
    if sha256_file(baseline_path) != EXPECTED_BASELINE_SHA256:
        raise SystemExit("The preserved Phase 12 TLA+ baseline changed.")
    if baseline["expected_sha256"] != EXPECTED_BASELINE_SHA256:
        raise SystemExit("Phase 13 baseline hash contract drifted.")
    if baseline["expected_status"] != "BASELINE_PRESERVED":
        raise SystemExit("Phase 13 baseline status drifted.")
    if baseline["expected_state_counts"] != {
        "generated_states": 50,
        "distinct_states": 28,
        "queued_states": 0,
        "search_depth": 10,
    }:
        raise SystemExit("Phase 13 baseline state-count contract drifted.")

    expansion = spec["expansion"]
    expanded_path = root / expansion["module"]
    if not expanded_path.is_file():
        raise SystemExit("Phase 13 expanded TLA+ module is missing.")
    expanded_text = expanded_path.read_text(encoding="utf-8")
    if expansion["status"] != "EXPANDED_OUTCOME_POPULATION_DIAGNOSTIC_ONLY":
        raise SystemExit("Phase 13 expansion status drifted.")
    if set(expansion["causes"]) != EXPECTED_CAUSES:
        raise SystemExit("Phase 13 cause vocabulary drifted.")

    projection = spec["projection"]
    if projection["field_count"] != 16 or set(projection["fields"]) != EXPECTED_FIELDS:
        raise SystemExit("Phase 13 projection must retain the declared 16 unique fields.")
    if projection["match_status"] != "MATCH_WITHIN_DECLARED_ABSTRACTION":
        raise SystemExit("Phase 13 match status drifted.")
    if projection["mismatch_status"] != "MISMATCH_REQUIRES_REVIEW":
        raise SystemExit("Phase 13 mismatch status drifted.")
    if projection["canonical_baseline_check_required"] is not True:
        raise SystemExit("Phase 13 canonical baseline checks must remain mandatory.")

    witnesses = spec["expanded_witnesses"]
    if {row["outcome"] for row in witnesses} != EXPECTED_OUTCOMES:
        raise SystemExit("Phase 13 expanded-outcome population drifted.")
    if len({row["case_id"] for row in witnesses}) != len(witnesses):
        raise SystemExit("Phase 13 case identifiers must be unique.")

    baseline_text = baseline_path.read_text(encoding="utf-8")
    for row in witnesses:
        expansion_config = root / row["config"]
        baseline_config = root / row["baseline_config"]
        if not expansion_config.is_file() or not baseline_config.is_file():
            raise SystemExit(f"Missing Phase 13 config for {row['case_id']}.")
        config_text = expansion_config.read_text(encoding="utf-8")
        if row["property"] not in expanded_text or row["property"] not in config_text:
            raise SystemExit(f"Missing Phase 13 property: {row['property']}")
        baseline_assignment = f'outcome\' = "{row["outcome"]}"'
        if baseline_assignment in baseline_text:
            raise SystemExit(f"Preserved baseline unexpectedly assigns {row['outcome']}.")
        if baseline_assignment not in expanded_text:
            raise SystemExit(f"Expanded module does not assign {row['outcome']}.")
        if row["cause"] not in expanded_text:
            raise SystemExit(f"Expanded cause {row['cause']} is not declared.")
        if not row["expected_actions"] or row["expected_actions"][0] != "Init":
            raise SystemExit("Every Phase 13 witness must declare an explicit path from Init.")

    if len(spec["required_outputs"]) != 19:
        raise SystemExit("Phase 13 required-output count drifted.")
    if "phase13-derived-bundle.sha256" not in set(spec["required_outputs"]):
        raise SystemExit("Phase 13 derived checksum manifest is required.")

    boundary_values = {
        spec["formal_model_completeness_claim"],
        spec["implementation_equivalence_claim"],
        spec["cryptographic_security_claim"],
        spec["publication_evidence_status"],
    }
    if boundary_values != {"NOT_PERMITTED"}:
        raise SystemExit("Phase 13 claim boundaries must remain NOT_PERMITTED.")
    if spec["baseline_review_status"] != "PENDING_INDEPENDENT_REVIEW":
        raise SystemExit("Independent-review gate must remain open.")

    print(
        "Phase 13 outcome-expansion design valid: "
        f"baseline_hash={baseline['expected_sha256'][:12]}, expanded={len(witnesses)}, "
        f"causes={len(expansion['causes'])}, fields={projection['field_count']}, "
        f"outputs={len(spec['required_outputs'])}, status={spec['status']}."
    )


if __name__ == "__main__":
    main()
