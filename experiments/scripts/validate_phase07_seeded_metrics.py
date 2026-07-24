from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> int:
    spec = load("spec/phase-07-seeded-fault-metrics.json")
    config = load("experiments/configs/phase-07-provisional.json")
    catalog = load("tests/scenarios/phase-07-seeded-fault-catalog.json")

    expected_status = "PROVISIONAL_INTERNAL_REVIEW_ONLY"
    if spec.get("status") != expected_status:
        raise SystemExit("Phase 07 specification is not provisional.")
    if config.get("status") != expected_status:
        raise SystemExit("Phase 07 configuration is not provisional.")
    if catalog.get("status") != expected_status:
        raise SystemExit("Phase 07 scenario catalog is not provisional.")

    required_faults = {
        "DROP",
        "DELAY",
        "DUPLICATE",
        "REORDER",
        "CONTACT_CLOSE",
        "ENDPOINT_RESTART",
    }
    declared_faults = set(spec.get("fault_kinds", []))
    configured_faults = set(config.get("allowed_faults", []))
    if not required_faults.issubset(declared_faults):
        raise SystemExit("Phase 07 specification omits a required fault class.")
    if not required_faults.issubset(configured_faults):
        raise SystemExit("Phase 07 configuration omits a required fault class.")

    required_metrics = {
        "outcome",
        "alignment",
        "security_state",
        "availability_state",
        "recovery_duration_contacts",
        "total_transmissions",
        "retry_overhead",
        "replay_rejection_count",
        "stale_state_rejection_count",
        "command_accepted",
        "telemetry_complete",
    }
    if not required_metrics.issubset(set(spec.get("required_metrics", []))):
        raise SystemExit("Phase 07 specification omits a required metric.")

    parameter_status = config.get("parameter_status", {})
    if not parameter_status or any(
        value != "UNFROZEN" for value in parameter_status.values()
    ):
        raise SystemExit("Every Phase 07 experiment parameter must remain UNFROZEN.")

    scenarios = catalog.get("scenarios", [])
    ids = [scenario.get("id") for scenario in scenarios]
    tests = [scenario.get("test") for scenario in scenarios]
    if len(ids) != len(set(ids)):
        raise SystemExit("Phase 07 scenario IDs are not unique.")
    if len(tests) != len(set(tests)):
        raise SystemExit("Phase 07 scenario test names are not unique.")

    test_source = (ROOT / "tests/test_fault_metrics.py").read_text(
        encoding="utf-8"
    )
    missing = [name for name in tests if f"def {name}(" not in test_source]
    if missing:
        raise SystemExit(f"Catalog references missing tests: {missing}")

    runner = ROOT / "experiments/scripts/run_seeded_fault_experiments.py"
    module = ROOT / "src/ttc_recovery/fault_metrics.py"
    if not runner.exists() or not module.exists():
        raise SystemExit("Phase 07 runner or metric module is missing.")

    stops = " ".join(spec.get("mandatory_external_review_stop_points", []))
    for phrase in (
        "freezing any experiment parameter",
        "post-compromise security",
        "manuscript submission",
    ):
        if phrase not in stops:
            raise SystemExit(f"Missing mandatory external-review stop point: {phrase}")

    print(
        "Phase 07 seeded-metric design valid: "
        f"{len(config['seeds'])} provisional seeds, "
        f"{len(scenarios)} regression scenarios, status={expected_status}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
