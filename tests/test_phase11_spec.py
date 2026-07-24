import json
import unittest
from pathlib import Path

from ttc_recovery.formal_cross_validation import BOUND_CASES, EXPECTED_ACTIONS


class Phase11SpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(
            Path("spec/phase-11-formal-python-cross-validation.json").read_text(
                encoding="utf-8"
            )
        )
        cls.tla = Path("formal/tla/T1Recovery.tla").read_text(encoding="utf-8")
        cls.witness_cfg = Path("formal/tla/SuccessWitness.cfg").read_text(
            encoding="utf-8"
        )

    def test_phase_status_and_claim_boundaries_remain_provisional(self):
        self.assertEqual(self.spec["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY")
        review = self.spec["review_status"]
        self.assertEqual(review["implementation_equivalence_claim"], "NOT_PERMITTED")
        self.assertEqual(review["publication_evidence_status"], "NOT_PERMITTED")

    def test_success_witness_is_explicitly_testing_only(self):
        witness = self.spec["success_witness"]
        self.assertEqual(
            witness["testing_only_false_invariant"],
            "ReachabilityWitnessNoSuccess",
        )
        self.assertEqual(witness["expected_actions"], list(EXPECTED_ACTIONS))
        self.assertIn("testing-only false invariant", self.tla.lower())
        self.assertIn("ReachabilityWitnessNoSuccess", self.tla)
        self.assertIn("ReachabilityWitnessNoSuccess", self.witness_cfg)

    def test_trace_mapping_declares_macro_step_limits(self):
        projection = self.spec["trace_projection"]
        self.assertEqual(
            projection["status_on_match"], "MATCH_WITHIN_DECLARED_ABSTRACTION"
        )
        self.assertEqual(projection["equivalence_claim"], "NOT_PERMITTED")
        self.assertEqual(len(projection["comparison_fields"]), 16)
        for action in ("SelectCandidate", "AcceptCommand", "ReceiveStatus"):
            self.assertIn(action, projection["macro_step_mapping"])

    def test_bound_panel_matches_implemented_cases(self):
        expected = [case.case_id for case in BOUND_CASES]
        actual = [case["id"] for case in self.spec["bound_panel"]["cases"]]
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 5)
        for case in self.spec["bound_panel"]["cases"]:
            self.assertTrue(Path(case["config"]).is_file())

    def test_baseline_reproduction_values_match_phase10(self):
        baseline = self.spec["bound_panel"]["baseline_reproduction_required"]
        self.assertEqual(baseline["generated_states"], 50)
        self.assertEqual(baseline["distinct_states"], 28)
        self.assertEqual(baseline["queued_states"], 0)
        self.assertEqual(baseline["search_depth"], 10)

    def test_required_outputs_include_trace_bounds_logs_and_manifest(self):
        outputs = set(self.spec["required_outputs"])
        for required in (
            "phase11-cross-validation.json",
            "phase11-success-witness.json",
            "phase11-trace-comparison.csv",
            "phase11-bound-expansion.csv",
            "phase11-tlc-success-witness.log",
            "phase11-derived-bundle.sha256",
        ):
            self.assertIn(required, outputs)
        self.assertEqual(len(outputs), 13)

    def test_toolchain_remains_pinned(self):
        toolchain = self.spec["toolchain"]
        self.assertEqual(toolchain["version"], "1.7.4")
        self.assertEqual(
            toolchain["official_sha1"],
            "bee4a54f3ee3d4afc347c3240ec2d9e93b075104",
        )
        self.assertEqual(toolchain["worker_count"], 1)

    def test_external_review_stop_points_cover_equivalence_and_publication(self):
        stops = " ".join(self.spec["mandatory_external_review_stop_points"])
        for phrase in (
            "formal property set",
            "implementation equivalence",
            "concrete cryptographic protocol",
            "publication evidence",
            "post-compromise-security",
        ):
            self.assertIn(phrase, stops)


if __name__ == "__main__":
    unittest.main()
