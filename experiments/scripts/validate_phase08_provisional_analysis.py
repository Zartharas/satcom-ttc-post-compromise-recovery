from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "experiments" / "configs" / "phase-08-provisional.json"
SPEC_PATH = ROOT / "spec" / "phase-08-provisional-analysis.json"
CATALOG_PATH = (
    ROOT / "tests" / "scenarios" / "phase-08-provisional-analysis-catalog.json"
)
TEST_PATH = ROOT / "tests" / "test_provisional_analysis.py"
MODULE_PATH = ROOT / "src" / "ttc_recovery" / "provisional_analysis.py"
RUNNER_PATH = ROOT / "experiments" / "scripts" / "analyze_phase07_results.py"

EXPECTED_STATUS = "PROVISIONAL_INTERNAL_REVIEW_ONLY"
EXPECTED_SCOPE = "DESCRIPTIVE_AND_SENSITIVITY_SCAFFOLD_ONLY"
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
EXPECTED_PHASES = {
    "RECOVERY_PREPARE",
    "RECOVERY_RESPONSE",
    "RECOVERY_COMMIT",
    "RECOVERY_CONFIRM",
    "TEST_COMMAND",
    "STATUS_TELEMETRY",
}
EXPECTED_OUTPUTS = {
    "phase08-analysis.json",
    "phase08-annotated-results.csv",
    "phase08-overall-summary.csv",
    "phase08-outcome-summary.csv",
    "phase08-fault-kind-summary.csv",
    "phase08-fault-phase-summary.csv",
    "phase08-fault-count-summary.csv",
    "phase08-security-availability.csv",
    "phase08-coverage-audit.csv",
    "phase08-trace-anomalies.csv",
    "phase08-adverse-cases.csv",
    "phase08-sensitivity-rows.csv",
    "phase08-sensitivity-summary.csv",
    "phase08-derived-bundle.sha256",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> int:
    for path in (
        CONFIG_PATH,
        SPEC_PATH,
        CATALOG_PATH,
        TEST_PATH,
        MODULE_PATH,
        RUNNER_PATH,
    ):
        require(path.is_file(), f"Required Phase 08 file is missing: {path}")

    config = load_json(CONFIG_PATH)
    spec = load_json(SPEC_PATH)
    catalog = load_json(CATALOG_PATH)

    require(config.get("status") == EXPECTED_STATUS, "Config status is not provisional.")
    require(spec.get("status") == EXPECTED_STATUS, "Spec status is not provisional.")
    require(catalog.get("status") == EXPECTED_STATUS, "Catalog status is not provisional.")
    require(
        config.get("analysis_scope") == EXPECTED_SCOPE,
        "Unexpected Phase 08 analysis scope.",
    )

    source_bundle = config.get("source_bundle", {})
    for key in ("results_json", "metrics_csv", "checksum_manifest"):
        value = str(source_bundle.get(key, ""))
        require(value and Path(value).name == value, f"Unsafe source bundle name: {key}")

    denominator = config.get("denominator_policy", {})
    require(int(denominator.get("minimum_group_size", 0)) > 0, "Invalid minimum group size.")
    require(bool(denominator.get("retain_low_n_groups")), "Low-n groups must remain visible.")
    require(
        bool(denominator.get("overlapping_fault_groups_must_be_declared")),
        "Overlapping fault groups must be declared.",
    )

    coverage = config.get("coverage_expectations", {})
    require(
        set(coverage.get("required_fault_kinds", [])) == EXPECTED_FAULTS,
        "Fault-kind coverage list is incomplete.",
    )
    require(
        set(coverage.get("required_fault_phases", [])) == EXPECTED_PHASES,
        "Fault-phase coverage list is incomplete.",
    )

    sensitivity = config.get("sensitivity_scaffold", {})
    transmissions = sensitivity.get("max_transmissions", [])
    lifetimes = sensitivity.get("candidate_lifetime_contacts", [])
    require(transmissions and lifetimes, "Sensitivity grid cannot be empty.")
    require(len(transmissions) == len(set(transmissions)), "Duplicate transmission grid values.")
    require(len(lifetimes) == len(set(lifetimes)), "Duplicate lifetime grid values.")
    require(all(int(value) > 0 for value in transmissions), "Invalid transmission grid value.")
    require(all(int(value) > 0 for value in lifetimes), "Invalid lifetime grid value.")
    require(sensitivity.get("grid_status") == "UNFROZEN", "Sensitivity grid is not unfrozen.")
    require(
        sensitivity.get("fixed_input") == "SERIALIZED_PHASE_07_SCHEDULES",
        "Sensitivity input is not fixed to serialized schedules.",
    )

    require(
        set(config.get("required_outputs", [])) == EXPECTED_OUTPUTS,
        "Required Phase 08 output set is incomplete.",
    )

    claim_boundary = config.get("claim_boundary", {})
    require(claim_boundary.get("causal_inference") == "NOT_PERMITTED", "Causal boundary missing.")
    require(claim_boundary.get("hypothesis_testing") == "NOT_PERFORMED", "Hypothesis boundary missing.")
    require(
        claim_boundary.get("post_compromise_security_claim") == "NOT_PERMITTED",
        "PCS claim boundary missing.",
    )

    parameter_status = config.get("parameter_status", {})
    require(
        all(value in {"UNFROZEN", "NOT_DEFINED"} for value in parameter_status.values()),
        "A Phase 08 parameter appears frozen.",
    )

    stop_points = " ".join(spec.get("mandatory_external_review_stop_points", [])).lower()
    for phrase in (
        "experiment population",
        "retry budgets",
        "denominator exclusions",
        "statistical analysis plan",
        "final treatment",
        "post-compromise security",
        "publication evidence",
    ):
        require(phrase in stop_points, f"External-review stop point is missing: {phrase}")

    scenarios = catalog.get("scenarios", [])
    require(scenarios, "Phase 08 test catalog is empty.")
    ids = [str(item.get("id")) for item in scenarios]
    tests = [str(item.get("test")) for item in scenarios]
    require(len(ids) == len(set(ids)), "Duplicate Phase 08 scenario ID.")
    require(len(tests) == len(set(tests)), "Duplicate Phase 08 test name.")
    test_source = TEST_PATH.read_text(encoding="utf-8")
    for test_name in tests:
        require(
            f"def {test_name}(" in test_source,
            f"Catalog references missing test: {test_name}",
        )

    print(
        "Phase 08 provisional analysis valid: "
        f"{len(scenarios)} analysis scenarios, "
        f"grid={len(transmissions)}x{len(lifetimes)}, "
        f"status={EXPECTED_STATUS}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
