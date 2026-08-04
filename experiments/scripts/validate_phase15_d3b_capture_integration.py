#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
D3B_SPEC_PATH = ROOT / "spec" / "phase-15-d3b-capture-integration.json"
PROTOCOL_PATH = ROOT / "spec" / "phase-15-experiment-protocol-candidate.json"
D2_MATRIX_PATH = ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"
D3_CONFIG_PATH = (
    ROOT / "experiments" / "configs" / "phase-15-matched-family-population.json"
)
CAPTURE_PATH = ROOT / "experiments" / "scripts" / "run_phase15_pilot_capture.py"
DOC_PATH = ROOT / "docs" / "phase-15-d3b-capture-integration.md"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "phase15-comparability.yml"

EXPECTED_STATUS = (
    "IMPLEMENTED_PENDING_LOCAL_AND_CI_VALIDATION_NOT_COMPARATIVE_EVIDENCE"
)
EXPECTED_D2_STATUS = "DEFINED_PENDING_VALIDATION_NOT_COMPARATIVE_EVIDENCE"
EXPECTED_D3_CONFIG_STATUS = (
    "EXECUTABLE_POPULATION_CANDIDATE_NOT_COMPARATIVE_EVIDENCE"
)
EXPECTED_D3_OUTPUT_STATUS = (
    "EXECUTABLE_POPULATION_IMPLEMENTED_PENDING_VALIDATION_"
    "NOT_COMPARATIVE_EVIDENCE"
)
EXPECTED_FAMILIES = ["CF-01", "CF-02", "CF-05", "CF-06"]
EXPECTED_EXECUTION_ORDER = [
    "RETAIN_INPUTS",
    "RUN_T1_PILOT",
    "RUN_BASELINE_PARITY",
    "RUN_D3_IF_T1_AND_BASELINE_SUCCEED",
    "VALIDATE_D3_OUTPUTS",
    "RUN_T1_DESCRIPTIVE_ANALYSIS",
    "WRITE_GOVERNANCE_METADATA",
    "WRITE_AND_VERIFY_LAYERED_MANIFESTS",
]
EXPECTED_DERIVED_OUTPUTS = [
    "derived/phase-15-matched-family-population.json",
    "derived/phase-15-matched-family-members.csv",
    "derived/phase-15-matched-family-denominators.csv",
    "derived/phase-15-matched-family-derived.sha256",
]
EXPECTED_METADATA_FIELDS = {
    "t1_catalog_path",
    "t1_catalog_sha256",
    "comparability_matrix_path",
    "comparability_matrix_sha256",
    "matched_family_config_path",
    "matched_family_config_sha256",
    "matched_family_command",
    "matched_family_process_exit_code",
    "matched_family_exit_code",
    "matched_family_status",
    "matched_family_output_paths",
    "matched_family_internal_manifest_sha256",
    "matched_family_population_counts",
}
EXPECTED_CLAIM_BOUNDARY = {
    "family_specific_descriptive_comparison": "NOT_YET_AUTHORIZED",
    "pooled_cross_treatment_aggregation": "NOT_PERMITTED",
    "success_rate_or_percentage": "NOT_PERMITTED",
    "inferential_statistics": "NOT_PERMITTED",
    "treatment_superiority": "NOT_PERMITTED",
    "cryptographic_security_or_pcs": "NOT_PERMITTED",
    "independent_validation": "NOT_PERMITTED",
    "publication_evidence": "NOT_PERMITTED",
}


def fail(message: str) -> None:
    raise SystemExit(f"Phase 15 D3B validation failed: {message}")


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def load_capture_module():
    module_spec = importlib.util.spec_from_file_location(
        "phase15_d3b_capture",
        CAPTURE_PATH,
    )
    if module_spec is None or module_spec.loader is None:
        fail("cannot load capture wrapper module")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def main() -> None:
    for path in (
        D3B_SPEC_PATH,
        PROTOCOL_PATH,
        D2_MATRIX_PATH,
        D3_CONFIG_PATH,
        CAPTURE_PATH,
        DOC_PATH,
        WORKFLOW_PATH,
    ):
        require_file(path)

    contract = load_json(D3B_SPEC_PATH)
    protocol = load_json(PROTOCOL_PATH)
    matrix = load_json(D2_MATRIX_PATH)
    d3_config = load_json(D3_CONFIG_PATH)
    capture = load_capture_module()

    if contract.get("status") != EXPECTED_STATUS:
        fail("D3B status drifted")
    if contract.get("run_class") != "PILOT_INTERNAL_VALIDATION_ONLY":
        fail("D3B escaped the pilot run class")
    if contract.get("wrapper") != (
        "experiments/scripts/run_phase15_pilot_capture.py"
    ):
        fail("capture wrapper path drifted")
    if contract.get("execution_order") != EXPECTED_EXECUTION_ORDER:
        fail("D3B execution order drifted")

    prerequisite = contract.get("d3_prerequisite", {})
    if prerequisite != {
        "t1_runner_exit_code": 0,
        "baseline_runner_exit_code": 0,
        "failure_status": "SKIPPED_PREREQUISITE_FAILURE",
    }:
        fail("D3 prerequisite gate drifted")

    retained_inputs = contract.get("retained_inputs", [])
    if len(retained_inputs) != 8:
        fail("retained-input population drifted")
    retained_sources = {row["source"] for row in retained_inputs}
    expected_sources = {
        "experiments/configs/phase-15-pilot.json",
        "experiments/configs/phase-15-baseline-parity.json",
        "experiments/configs/phase-15-matched-family-population.json",
        "spec/phase-15-treatment-comparability-matrix.json",
        "spec/phase-15-experiment-protocol-candidate.json",
        "experiments/configs/phase-08-provisional.json",
        "tests/scenarios/baseline-test-catalog.json",
        "tests/scenarios/t1-provisional-test-catalog.json",
    }
    if retained_sources != expected_sources:
        fail("retained-input source set drifted")
    if contract.get("derived_outputs") != EXPECTED_DERIVED_OUTPUTS:
        fail("derived-output contract drifted")

    acceptance = contract.get("matched_family_acceptance", {})
    if acceptance.get("status") != EXPECTED_D3_OUTPUT_STATUS:
        fail("accepted D3 output status drifted")
    if acceptance.get("eligible_family_ids") != EXPECTED_FAMILIES:
        fail("accepted family population drifted")
    for field, expected in (
        ("family_count", 4),
        ("member_row_count", 13),
        ("analysis_unit_count", 12),
        ("source_execution_count", 13),
    ):
        if acceptance.get(field) != expected:
            fail(f"D3 acceptance count drifted: {field}")
    if acceptance.get("success_rate_denominator") != "NOT_DEFINED":
        fail("success-rate denominator was opened")
    if acceptance.get("aggregate_authorized") is not False:
        fail("aggregate authorization was opened")
    if acceptance.get("publication_evidence") is not False:
        fail("D3B cannot be publication evidence")

    metadata = contract.get("metadata", {})
    if metadata.get("schema_version") != "0.2.0":
        fail("run-metadata schema version drifted")
    if set(metadata.get("required_fields", [])) != EXPECTED_METADATA_FIELDS:
        fail("D3B metadata field set drifted")

    manifest_paths = [row["path"] for row in contract.get("manifest_layers", [])]
    if manifest_paths != [
        "manifests/raw.sha256",
        "manifests/derived.sha256",
        "manifests/analysis.sha256",
        "manifests/run-bundle.sha256",
    ]:
        fail("manifest-layer order or population drifted")
    if contract.get("success_status") != "COMPLETED_AND_VERIFIED":
        fail("D3B success status drifted")
    if set(contract.get("failure_statuses", [])) != {
        "SKIPPED_PREREQUISITE_FAILURE",
        "PROCESS_FAILED",
        "OUTPUT_VALIDATION_FAILED",
    }:
        fail("D3B failure-status set drifted")
    if contract.get("claim_boundary") != EXPECTED_CLAIM_BOUNDARY:
        fail("D3B claim boundary was relaxed")

    if matrix.get("status") != EXPECTED_D2_STATUS:
        fail("D2 matrix status drifted")
    if d3_config.get("status") != EXPECTED_D3_CONFIG_STATUS:
        fail("D3 configuration status drifted")
    if d3_config.get("eligible_family_ids") != EXPECTED_FAMILIES:
        fail("D3 configuration family population drifted")
    if set(d3_config.get("claim_boundary", {}).values()) - {
        "NOT_PERMITTED",
        "NOT_YET_AUTHORIZED",
    }:
        fail("D3 configuration claim boundary was relaxed")

    matched_population = protocol.get("matched_family_population", {})
    if matched_population.get("capture_integration") != EXPECTED_STATUS:
        fail("Phase 15 protocol does not record D3B integration")
    pilot = protocol.get("pilot_scope", {})
    if pilot.get("matched_family_capture_status") != EXPECTED_STATUS:
        fail("pilot scope does not record D3B integration")
    required_outputs = set(protocol.get("required_outputs", []))
    for relative in (
        "spec/phase-15-d3b-capture-integration.json",
        "docs/phase-15-d3b-capture-integration.md",
        "experiments/scripts/validate_phase15_d3b_capture_integration.py",
    ):
        if relative not in required_outputs:
            fail(f"protocol required outputs missing {relative}")

    expected_capture_paths = {
        "DEFAULT_MATCHED_FAMILY_CONFIG": D3_CONFIG_PATH,
        "DEFAULT_COMPARABILITY_MATRIX": D2_MATRIX_PATH,
        "T1_CATALOG": ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json",
    }
    for attribute, expected in expected_capture_paths.items():
        actual = getattr(capture, attribute, None)
        if actual is None or Path(actual).resolve() != expected.resolve():
            fail(f"capture default path drifted: {attribute}")
    if not callable(getattr(capture, "validate_matched_family_outputs", None)):
        fail("capture-side D3 validation is unavailable")
    if capture.MATCHED_FAMILY_IDS != EXPECTED_FAMILIES:
        fail("capture-side family population drifted")
    if capture.MATCHED_FAMILY_STATUS != EXPECTED_D3_OUTPUT_STATUS:
        fail("capture-side D3 status drifted")

    capture_text = CAPTURE_PATH.read_text(encoding="utf-8")
    for phrase in (
        "runner_exit == 0 and baseline_exit == 0",
        "validate_matched_family_outputs(derived_dir)",
        'derived_manifest = manifests_dir / "derived.sha256"',
        '"schema_version": "0.2.0"',
        '"family_specific_descriptive_comparison": "NOT_YET_AUTHORIZED"',
    ):
        if phrase not in capture_text:
            fail(f"capture wrapper missing control: {phrase}")

    doc_text = DOC_PATH.read_text(encoding="utf-8")
    for phrase in (
        "retained copies",
        "SKIPPED_PREREQUISITE_FAILURE",
        "COMPLETED_AND_VERIFIED",
        "semantic relaxation",
        "publication_evidence=NOT_PERMITTED",
    ):
        if phrase not in doc_text:
            fail(f"D3B documentation missing phrase: {phrase}")

    workflow_text = WORKFLOW_PATH.read_text(encoding="utf-8")
    for phrase in (
        "validate_phase15_d3b_capture_integration.py",
        "phase15-d3b-ci-smoke",
        "manifests/derived.sha256",
    ):
        if phrase not in workflow_text:
            fail(f"D3B CI workflow missing control: {phrase}")

    print(
        "Phase 15 D3B capture integration valid: "
        f"retained_inputs={len(retained_inputs)}, "
        f"derived_outputs={len(EXPECTED_DERIVED_OUTPUTS)}, "
        f"manifest_layers={len(manifest_paths)}, "
        "d3_prerequisite=t1_and_baseline_success, "
        f"status={contract['status']}."
    )


if __name__ == "__main__":
    main()
