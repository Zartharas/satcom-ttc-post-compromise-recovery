from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec" / "phase-10-formal-model-execution.json"
MODEL = ROOT / "formal" / "tla" / "T1Recovery.tla"
POSITIVE_CONFIG = ROOT / "formal" / "tla" / "MC.cfg"
NEGATIVE_CONFIG = ROOT / "formal" / "tla" / "NegativeControl.cfg"
RUNNER = ROOT / "experiments" / "scripts" / "run_phase10_formal_execution.py"


class Phase10SpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = json.loads(SPEC.read_text(encoding="utf-8"))
        cls.model = MODEL.read_text(encoding="utf-8")
        cls.positive = POSITIVE_CONFIG.read_text(encoding="utf-8")
        cls.negative = NEGATIVE_CONFIG.read_text(encoding="utf-8")
        cls.runner = RUNNER.read_text(encoding="utf-8")

    def test_status_and_publication_boundary_remain_provisional(self) -> None:
        self.assertEqual(self.spec["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY")
        self.assertEqual(self.spec["publication_evidence_status"], "NOT_PERMITTED")

    def test_toolchain_is_pinned_to_stable_release_and_checksum(self) -> None:
        toolchain = self.spec["toolchain"]
        self.assertEqual(toolchain["release"], "1.7.4")
        self.assertEqual(toolchain["release_channel"], "STABLE")
        self.assertEqual(
            toolchain["official_sha1"],
            "bee4a54f3ee3d4afc347c3240ec2d9e93b075104",
        )
        self.assertEqual(toolchain["workers"], 1)
        self.assertGreaterEqual(toolchain["ci_java_version"], toolchain["minimum_java"])

    def test_positive_wording_is_bounded_and_not_proof_language(self) -> None:
        positive = self.spec["positive_model"]
        self.assertEqual(
            positive["result_wording"], "NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND"
        )
        for phrase in positive["prohibited_wording"]:
            self.assertNotEqual(positive["result_wording"], phrase)

    def test_negative_control_is_explicitly_testing_only(self) -> None:
        negative = self.spec["negative_control"]
        self.assertEqual(negative["invariant"], "NegativeControlNoActivation")
        self.assertEqual(negative["role"], "INTENTIONAL_PIPELINE_NEGATIVE_CONTROL")
        self.assertIn("not a discovered protocol flaw", negative["interpretation"])

    def test_model_and_configs_declare_execution_properties(self) -> None:
        self.assertIn("EXTENDS Integers", self.model)
        self.assertIn("NegativeControlNoActivation", self.model)
        self.assertIn("CHECK_DEADLOCK FALSE", self.positive)
        self.assertIn("SuccessRequiresEvidence", self.positive)
        self.assertIn("NegativeControlNoActivation", self.negative)

    def test_runner_uses_pinned_default_checksum(self) -> None:
        self.assertIn("bee4a54f3ee3d4afc347c3240ec2d9e93b075104", self.runner)
        self.assertIn("NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND", self.runner)

    def test_required_outputs_include_logs_counterexample_and_manifest(self) -> None:
        required = set(self.spec["required_outputs"])
        self.assertIn("phase10-formal-execution.json", required)
        self.assertIn("phase10-negative-control-counterexample.json", required)
        self.assertIn("phase10-sany.log", required)
        self.assertIn("phase10-tlc-positive.log", required)
        self.assertIn("phase10-tlc-negative-control.log", required)
        self.assertIn("phase10-derived-bundle.sha256", required)

    def test_external_review_stop_points_cover_claims_and_publication(self) -> None:
        joined = " ".join(self.spec["external_review_stop_points"]).lower()
        for term in ("formal property", "concrete", "post-compromise", "publication", "external"):
            self.assertIn(term, joined)


if __name__ == "__main__":
    unittest.main()
