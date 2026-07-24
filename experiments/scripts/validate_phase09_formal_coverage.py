from __future__ import annotations

import json
from pathlib import Path

from ttc_recovery.fault_metrics import ExperimentPhase, FaultKind
from ttc_recovery.formal_coverage import (
    BOUND_STATUS,
    build_coverage_scenarios,
    build_reachability_report,
    invariant_traceability,
    run_coverage_suite,
)

STATUS = "PROVISIONAL_INTERNAL_REVIEW_ONLY"


def main() -> int:
    spec = json.loads(
        Path("spec/phase-09-adversarial-coverage-formal-model.json").read_text(
            encoding="utf-8"
        )
    )
    catalog = json.loads(
        Path("tests/scenarios/phase-09-adversarial-coverage-catalog.json").read_text(
            encoding="utf-8"
        )
    )
    if spec.get("status") != STATUS:
        raise ValueError("Phase 09 must remain provisional.")
    if spec["formal_model"]["status"] != "SCAFFOLD_NOT_FORMALLY_REVIEWED":
        raise ValueError("Formal model must remain an unreviewed scaffold.")
    if spec["review_status"]["publication_evidence_status"] != "NOT_PERMITTED":
        raise ValueError("Phase 09 output must not be publication evidence.")

    scenarios = build_coverage_scenarios()
    ids = [scenario.scenario_id for scenario in scenarios]
    if len(ids) != 24 or len(ids) != len(set(ids)):
        raise ValueError("Phase 09 requires exactly 24 unique scenarios.")
    catalog_ids = [row["id"] for row in catalog["scenarios"]]
    if catalog.get("scenario_count") != 24 or catalog_ids != ids:
        raise ValueError("Phase 09 catalog does not match implemented scenarios.")

    faults = {action.kind for scenario in scenarios for action in scenario.schedule}
    phases = {action.phase for scenario in scenarios for action in scenario.schedule}
    if faults != set(FaultKind):
        raise ValueError("Phase 09 does not cover every supported fault kind.")
    if phases != set(ExperimentPhase):
        raise ValueError("Phase 09 does not cover every protocol phase.")

    required_tags = set(spec["coverage_requirements"]["required_boundaries"])
    actual_tags = {tag for scenario in scenarios for tag in scenario.boundary_tags}
    if not required_tags.issubset(actual_tags):
        raise ValueError("Phase 09 boundary coverage is incomplete.")

    rows = run_coverage_suite(scenarios)
    by_id = {row["scenario_id"]: row for row in rows}
    expected = {
        "P09-001": "SUCCESS",
        "P09-010": "INDETERMINATE",
        "P09-012": "SECURE_DEGRADED",
        "P09-013": "EXPIRED",
        "P09-016": "SUCCESS",
        "P09-017": "EXPIRED",
    }
    for scenario_id, outcome in expected.items():
        if by_id[scenario_id]["outcome"] != outcome:
            raise ValueError(
                f"{scenario_id} expected {outcome}, got {by_id[scenario_id]['outcome']}."
            )
    if by_id["P09-015"]["unreachable_fault_actions"] != 1:
        raise ValueError("Retry-budget-plus-one scenario lost unreachable-action accounting.")

    reachability = build_reachability_report(rows)
    valid_statuses = {"REACHED", BOUND_STATUS}
    reachability_rows = reachability["states"] + reachability["outcomes"]
    if any(row["reachability"] not in valid_statuses for row in reachability_rows):
        raise ValueError("Reachability report uses unsupported claim language.")
    if BOUND_STATUS not in {row["reachability"] for row in reachability["outcomes"]}:
        raise ValueError("Bounded non-reachability must remain explicit.")

    trace = invariant_traceability()
    if len(trace) != 13:
        raise ValueError("Phase 09 requires 13 invariant traceability rows.")
    if len({row["invariant_id"] for row in trace}) != len(trace):
        raise ValueError("Invariant traceability IDs must be unique.")
    if any(row["coverage_scenario"] not in by_id for row in trace):
        raise ValueError("Invariant traceability references an unknown coverage scenario.")

    tla = Path("formal/tla/T1Recovery.tla").read_text(encoding="utf-8")
    cfg = Path("formal/tla/MC.cfg").read_text(encoding="utf-8")
    required_properties = {
        "EpochMonotonicity",
        "CandidateNotAuthority",
        "BoundedControlState",
        "NoRollback",
        "AtMostOneSpacecraftActivation",
        "SuccessRequiresEvidence",
        "DegradedNotSuccess",
        "StatusLossNotDivergence",
    }
    if any(name not in tla or name not in cfg for name in required_properties):
        raise ValueError("TLA+ scaffold and configuration property sets disagree.")

    stop_text = " ".join(spec["mandatory_external_review_stop_points"])
    for phrase in (
        "formal property set",
        "concrete cryptographic security",
        "publication evidence",
        "external security claim",
    ):
        if phrase not in stop_text:
            raise ValueError(f"Missing Phase 09 review stop point: {phrase}")

    reached_states = sum(
        row["reachability"] == "REACHED" for row in reachability["states"]
    )
    reached_outcomes = sum(
        row["reachability"] == "REACHED" for row in reachability["outcomes"]
    )
    print(
        "Phase 09 formal-coverage design valid: "
        f"{len(rows)} scenarios, {len(trace)} invariant mappings, "
        f"reached_states={reached_states}/6, reached_outcomes={reached_outcomes}/7, "
        f"status={STATUS}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
