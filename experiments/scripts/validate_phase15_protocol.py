#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "phase-15-experiment-protocol-candidate.json"
CONFIG_PATH = ROOT / "experiments" / "configs" / "phase-15-pilot.json"
BASELINE_CONFIG_PATH = (
    ROOT / "experiments" / "configs" / "phase-15-baseline-parity.json"
)
BASELINE_CATALOG_PATH = ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"
PROTOCOL_DOC = ROOT / "docs" / "phase-15-experiment-protocol.md"
DATA_DICTIONARY = ROOT / "docs" / "phase-15-data-dictionary.md"
CAPTURE_CONTROLS = ROOT / "governance" / "phase-15-data-capture-controls.md"
PHASE14_SPEC = ROOT / "spec" / "phase-14-independent-review-package.json"
ORACLE_CANDIDATE = ROOT / "spec" / "baseline-oracle-freeze-candidate.json"

EXPECTED_STATUS = "PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE"
EXPECTED_SOURCE_COMMIT = "04c086bc8f75fe6a7bf8e3eede3e24a8ebdf19a4"
EXPECTED_SEEDS = list(range(7001, 7013))
EXPECTED_FAULTS = {
    "DROP",
    "DELAY",
    "DUPLICATE",
    "REORDER",
    "CONTACT_CLOSE",
    "ENDPOINT_RESTART",
    "STALE_COUNTER",
    "STALE_REPLAY",
}
EXPECTED_TREATMENTS = {"B0", "B1", "B2", "T1"}
EXPECTED_PARITY_STATUS = "IMPLEMENTED_PENDING_VALIDATION"
EXPECTED_METRICS = {
    "seed",
    "schedule_sha256",
    "outcome",
    "alignment",
    "security_state",
    "availability_state",
    "recovery_duration_contacts",
    "divergent_contact_windows",
    "degraded_contact_windows",
    "total_transmissions",
    "retry_overhead",
    "fault_count",
    "drop_count",
    "delay_count",
    "duplicate_count",
    "reorder_count",
    "contact_close_count",
    "restart_count",
    "replay_count",
    "rejection_count",
    "replay_rejection_count",
    "stale_state_rejection_count",
    "command_accepted",
    "telemetry_complete",
    "verification_complete",
    "active_key_compromised",
}
EXPECTED_BASELINE_IDS = [
    "B0-01",
    "B0-02",
    "B0-03",
    "B0-04",
    "B1-01",
    "B1-02",
    "B1-03",
    "B1-04",
    "B1-05",
    "B1-06",
    "B1-07",
    "B2-01",
    "B2-02",
    "B2-03",
    "B2-04",
    "B2-05",
    "B2-06",
    "B2-07",
    "B2-08",
    "B2-09",
    "B2-10",
]


def fail(message: str) -> None:
    raise SystemExit(f"Phase 15 validation failed: {message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")


def main() -> None:
    for path in (
        SPEC_PATH,
        CONFIG_PATH,
        BASELINE_CONFIG_PATH,
        BASELINE_CATALOG_PATH,
        PROTOCOL_DOC,
        DATA_DICTIONARY,
        CAPTURE_CONTROLS,
        PHASE14_SPEC,
        ORACLE_CANDIDATE,
    ):
        require_file(path)

    spec = load_json(SPEC_PATH)
    config = load_json(CONFIG_PATH)
    baseline_config = load_json(BASELINE_CONFIG_PATH)
    baseline_catalog = load_json(BASELINE_CATALOG_PATH)
    phase14 = load_json(PHASE14_SPEC)
    oracle = load_json(ORACLE_CANDIDATE)

    if spec.get("status") != EXPECTED_STATUS:
        fail("protocol status must remain provisional and not publication evidence")
    if spec.get("source_base", {}).get("commit") != EXPECTED_SOURCE_COMMIT:
        fail("Phase 14 source commit drifted")
    if spec["source_base"]["baseline_review_status"] != "PENDING_INDEPENDENT_REVIEW":
        fail("baseline review status must remain pending")
    if spec["source_base"]["oracle_freeze_status"] != "NOT_PERMITTED":
        fail("oracle freeze must remain prohibited")

    gate = spec["review_gate"]
    if gate["issue"] != 3 or gate["status"] != "OPEN":
        fail("issue #3 must remain the open external-review tracker")
    if "publication-grade comparative conclusions" not in gate["blocking_for"]:
        fail("publication conclusions must remain review-gated")

    rq_ids = [row["id"] for row in spec["research_questions"]]
    if rq_ids != ["RQ-1", "RQ-2", "RQ-3"]:
        fail("research-question identifiers or order drifted")
    if len(rq_ids) != len(set(rq_ids)):
        fail("research-question identifiers must be unique")

    treatments = {row["id"]: row for row in spec["treatments"]}
    if set(treatments) != EXPECTED_TREATMENTS:
        fail("treatment set must remain B0, B1, B2, and T1")
    for treatment in ("B0", "B1", "B2"):
        if treatments[treatment]["publication_metric_parity"] != EXPECTED_PARITY_STATUS:
            fail(f"{treatment} metric parity must remain pending validation")
        if treatments[treatment]["current_execution_support"] != (
            "DETERMINISTIC_CATALOG_METRIC_ADAPTER"
        ):
            fail(f"{treatment} execution-support label drifted")
    if treatments["T1"]["publication_metric_parity"] != "AVAILABLE_PROVISIONALLY":
        fail("T1 metric support must remain provisional")

    parity = spec["baseline_metric_parity"]
    if parity["status"] != EXPECTED_PARITY_STATUS:
        fail("baseline parity status drifted")
    if parity["scenario_count"] != len(EXPECTED_BASELINE_IDS):
        fail("baseline parity scenario count drifted")
    if "does not establish" not in " ".join(parity["limits"]):
        fail("baseline parity limits must reject comparability inference")

    pilot = spec["pilot_scope"]
    if pilot["label"] != "PILOT_INTERNAL_VALIDATION_ONLY":
        fail("pilot label drifted")
    if pilot["publication_evidence"] is not False:
        fail("pilot cannot be publication evidence")
    if pilot["comparative_claims_allowed"] is not False:
        fail("pilot cannot authorize comparative claims")
    if pilot["pilot_config"] != "experiments/configs/phase-15-pilot.json":
        fail("pilot config path drifted")
    if pilot["baseline_parity_config"] != (
        "experiments/configs/phase-15-baseline-parity.json"
    ):
        fail("baseline parity config path drifted")

    if config.get("status") != "PROVISIONAL_INTERNAL_REVIEW_ONLY":
        fail("pilot config must remain compatible with the provisional runner")
    if config.get("run_class") != "PILOT_INTERNAL_VALIDATION_ONLY":
        fail("pilot config run class drifted")
    if config.get("protocol") != "spec/phase-15-experiment-protocol-candidate.json":
        fail("pilot config protocol link drifted")

    if config["seeds"] != EXPECTED_SEEDS:
        fail("pilot seed panel drifted")
    if len(config["seeds"]) != len(set(config["seeds"])):
        fail("pilot seeds must be unique")
    if set(config["allowed_faults"]) != EXPECTED_FAULTS:
        fail("pilot fault set drifted")

    candidate = spec["candidate_parameters"]
    for key in (
        "seeds",
        "ground_epoch",
        "spacecraft_epoch",
        "authority_epoch_floor",
        "max_transmissions",
        "candidate_lifetime_contacts",
        "max_faults",
        "compromise_active_keys",
        "allowed_faults",
    ):
        if candidate[key] != config[key]:
            fail(f"spec/config mismatch for {key}")

    outputs = config["outputs"]
    if outputs != {
        "json": "results/raw/phase-15-pilot-results.json",
        "csv": "results/processed/phase-15-pilot-metrics.csv",
    }:
        fail("pilot output paths drifted")

    controls = config["capture_controls"]
    if not controls or set(controls.values()) != {True}:
        fail("all pilot capture controls must be enabled")

    if baseline_config.get("status") != "PROVISIONAL_INTERNAL_REVIEW_ONLY":
        fail("baseline parity config must remain provisional")
    if baseline_config.get("run_class") != "PILOT_INTERNAL_VALIDATION_ONLY":
        fail("baseline parity run class drifted")
    if baseline_config.get("metric_parity_status") != EXPECTED_PARITY_STATUS:
        fail("baseline parity configuration status drifted")
    if baseline_config["scenario_ids"] != EXPECTED_BASELINE_IDS:
        fail("baseline parity scenario population or order drifted")
    catalog_ids = [row["id"] for row in baseline_catalog["tests"]]
    if catalog_ids != EXPECTED_BASELINE_IDS:
        fail("baseline test catalog population or order drifted")
    if set(baseline_config["shared_metric_fields"]) != EXPECTED_METRICS:
        fail("baseline shared metric field set drifted")
    if baseline_config["treatments"] != ["B0", "B1", "B2"]:
        fail("baseline treatment order drifted")
    if set(baseline_config["claim_boundary"].values()) != {"NOT_PERMITTED"}:
        fail("baseline parity claim boundary was relaxed")

    for rule in (
        "Include every successfully parsed run produced from the exact recorded configuration and serialized schedule.",
        "Do not exclude a run because its outcome is unexpected, unfavorable, or inconvenient.",
    ):
        population = spec["inclusion_rules"] + spec["exclusion_rules"]
        if rule not in population:
            fail(f"missing population-integrity rule: {rule}")

    allowed_reruns = set(spec["rerun_policy"]["allowed_reasons"])
    if len(allowed_reruns) != 5:
        fail("rerun reason set drifted")
    if "preferred outcome" not in spec["rerun_policy"]["prohibited_reason"]:
        fail("outcome-seeking reruns must remain prohibited")

    if set(spec["hard_claim_boundaries"].values()) - {
        "NOT_PERMITTED",
        "NOT_PERMITTED_FOR_PILOT",
    }:
        fail("hard claim boundary was relaxed")

    for relative in spec["required_outputs"]:
        require_file(ROOT / relative)

    protocol_text = PROTOCOL_DOC.read_text(encoding="utf-8")
    dictionary_text = DATA_DICTIONARY.read_text(encoding="utf-8")
    controls_text = CAPTURE_CONTROLS.read_text(encoding="utf-8")

    for phrase in (
        "metric parity",
        "PILOT_INTERNAL_VALIDATION_ONLY",
        "publication-candidate",
        "Issue #3 remains open",
    ):
        if phrase not in protocol_text:
            fail(f"protocol document missing required phrase: {phrase}")

    for metric in EXPECTED_METRICS:
        if f"`{metric}`" not in dictionary_text:
            fail(f"data dictionary missing metric: {metric}")

    for phrase in (
        "Raw-data immutability",
        "An unexpected or unfavorable outcome is not an exclusion reason.",
        "Treatment-parity gate",
        "AI-assisted development record",
    ):
        if phrase not in controls_text:
            fail(f"capture controls missing required phrase: {phrase}")

    if phase14["status"] != "READY_FOR_OUTREACH_NOT_REVIEWED":
        fail("Phase 14 review package status changed unexpectedly")
    if oracle["status"] != "PENDING_INDEPENDENT_REVIEW":
        fail("baseline oracle candidate no longer pending")
    if oracle["review"]["decision"] != "PENDING":
        fail("unsupported oracle review decision detected")

    print(
        "Phase 15 protocol valid: "
        f"research_questions={len(rq_ids)}, treatments={len(treatments)}, "
        f"pilot_seeds={len(config['seeds'])}, faults={len(EXPECTED_FAULTS)}, "
        f"baseline_scenarios={len(EXPECTED_BASELINE_IDS)}, "
        "baseline_metric_parity=3_implemented_pending_validation, "
        f"status={spec['status']}."
    )


if __name__ == "__main__":
    main()
