#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "phase-10-formal-model-execution.json"
MODEL_PATH = ROOT / "formal" / "tla" / "T1Recovery.tla"
POSITIVE_CONFIG = ROOT / "formal" / "tla" / "MC.cfg"
NEGATIVE_CONFIG = ROOT / "formal" / "tla" / "NegativeControl.cfg"
RUNNER = ROOT / "experiments" / "scripts" / "run_phase10_formal_execution.py"
MODULE = ROOT / "src" / "ttc_recovery" / "formal_execution.py"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    for path in (
        SPEC_PATH,
        MODEL_PATH,
        POSITIVE_CONFIG,
        NEGATIVE_CONFIG,
        RUNNER,
        MODULE,
    ):
        if not path.is_file():
            fail(f"Missing required Phase 10 file: {path.relative_to(ROOT)}")

    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    model = MODEL_PATH.read_text(encoding="utf-8")
    positive = POSITIVE_CONFIG.read_text(encoding="utf-8")
    negative = NEGATIVE_CONFIG.read_text(encoding="utf-8")
    runner = RUNNER.read_text(encoding="utf-8")
    module = MODULE.read_text(encoding="utf-8")

    if spec.get("status") != "PROVISIONAL_INTERNAL_REVIEW_ONLY":
        fail("Phase 10 status must remain PROVISIONAL_INTERNAL_REVIEW_ONLY.")
    if spec.get("publication_evidence_status") != "NOT_PERMITTED":
        fail("Phase 10 publication evidence must remain NOT_PERMITTED.")

    toolchain = spec.get("toolchain", {})
    if toolchain.get("release") != "1.7.4":
        fail("Phase 10 must pin TLA+ command-line tools release 1.7.4.")
    if toolchain.get("release_channel") != "STABLE":
        fail("Phase 10 must identify the pinned release as stable.")
    if toolchain.get("official_sha1") != "bee4a54f3ee3d4afc347c3240ec2d9e93b075104":
        fail("Phase 10 official tla2tools.jar checksum is incorrect.")
    if toolchain.get("workers") != 1:
        fail("Phase 10 reproducibility gate requires one TLC worker.")

    required_gates = {
        "SANY_PARSE_SUCCESS",
        "POSITIVE_TLC_NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND",
        "EXPECTED_NEGATIVE_CONTROL_COUNTEREXAMPLE_CAPTURED",
        "DERIVED_SHA256_MANIFEST_VALID",
    }
    if set(spec.get("execution_gates", [])) != required_gates:
        fail("Phase 10 execution gates are incomplete or unexpected.")

    positive_model = spec.get("positive_model", {})
    if positive_model.get("result_wording") != "NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND":
        fail("Phase 10 positive result wording is not bounded.")
    if "CHECK_DEADLOCK FALSE" not in positive:
        fail("Phase 10 positive TLC configuration must declare terminal deadlock handling.")

    negative_control = spec.get("negative_control", {})
    if negative_control.get("role") != "INTENTIONAL_PIPELINE_NEGATIVE_CONTROL":
        fail("Phase 10 negative control is not clearly testing-only.")
    if negative_control.get("invariant") != "NegativeControlNoActivation":
        fail("Phase 10 negative-control invariant does not match the model.")
    if "NegativeControlNoActivation" not in model or "NegativeControlNoActivation" not in negative:
        fail("Phase 10 negative-control property is not wired into model and configuration.")

    required_model_tokens = (
        "EXTENDS Integers",
        "Spec == Init /\\ [][Next]_vars",
        "TypeOK",
        "EpochMonotonicity",
        "SuccessRequiresEvidence",
        "StatusLossNotDivergence",
    )
    for token in required_model_tokens:
        if token not in model:
            fail(f"Phase 10 model is missing required token: {token}")

    required_module_tokens = (
        "FORMAL_EXECUTION_GATES_PASSED",
        "NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND",
        "EXPECTED_NEGATIVE_CONTROL_COUNTEREXAMPLE_CAPTURED",
        "phase10-derived-bundle.sha256",
        "publication_evidence_status",
    )
    for token in required_module_tokens:
        if token not in module:
            fail(f"Phase 10 execution module is missing required token: {token}")

    if "bee4a54f3ee3d4afc347c3240ec2d9e93b075104" not in runner:
        fail("Phase 10 runner does not pin the official release checksum.")

    required_outputs = set(spec.get("required_outputs", []))
    if len(required_outputs) != 7 or "phase10-derived-bundle.sha256" not in required_outputs:
        fail("Phase 10 required output set is incomplete.")

    stop_text = " ".join(spec.get("external_review_stop_points", [])).lower()
    for required in ("formal property", "concrete", "post-compromise", "publication", "external"):
        if required not in stop_text:
            fail(f"Phase 10 review boundary is missing: {required}")

    print(
        "Phase 10 formal-execution design valid: "
        "tool=1.7.4, gates=4, outputs=7, "
        "status=PROVISIONAL_INTERNAL_REVIEW_ONLY."
    )


if __name__ == "__main__":
    main()
