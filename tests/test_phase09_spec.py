import json
import unittest
from pathlib import Path

from ttc_recovery.formal_coverage import build_coverage_scenarios, invariant_traceability


class Phase09SpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(
            Path("spec/phase-09-adversarial-coverage-formal-model.json").read_text(
                encoding="utf-8"
            )
        )
        cls.catalog = json.loads(
            Path("tests/scenarios/phase-09-adversarial-coverage-catalog.json").read_text(
                encoding="utf-8"
            )
        )
        cls.tla = Path("formal/tla/T1Recovery.tla").read_text(encoding="utf-8")
        cls.cfg = Path("formal/tla/MC.cfg").read_text(encoding="utf-8")
        cls.readme = Path("formal/README.md").read_text(encoding="utf-8")

    def test_phase09_status_and_claim_boundary_remain_provisional(self):
        self.assertEqual(self.spec["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY")
        self.assertEqual(
            self.spec["formal_model"]["status"],
            "SCAFFOLD_NOT_FORMALLY_REVIEWED",
        )
        self.assertEqual(
            self.spec["review_status"]["publication_evidence_status"],
            "NOT_PERMITTED",
        )

    def test_catalog_matches_implemented_scenario_ids(self):
        expected = [scenario.scenario_id for scenario in build_coverage_scenarios()]
        actual = [row["id"] for row in self.catalog["scenarios"]]
        self.assertEqual(self.catalog["scenario_count"], 24)
        self.assertEqual(actual, expected)

    def test_spec_declares_complete_fault_phase_and_boundary_coverage(self):
        coverage = self.spec["coverage_requirements"]
        self.assertEqual(len(coverage["required_fault_kinds"]), 8)
        self.assertEqual(len(coverage["required_phases"]), 6)
        self.assertEqual(len(coverage["required_boundaries"]), 8)
        self.assertEqual(coverage["explicit_schedule_count"], 24)

    def test_tla_scaffold_declares_required_actions_and_properties(self):
        required_actions = [
            "Prepare ==",
            "SelectCandidate ==",
            "Commit ==",
            "Confirm ==",
            "AcceptCommand ==",
            "ReceiveStatus ==",
            "Verify ==",
            "Retry ==",
            "ExpireBeforeActivation ==",
            "ExpireAfterSpacecraftActivation ==",
        ]
        required_properties = {
            row["formal_property"] for row in invariant_traceability()
        }
        declared_properties = {
            "EpochMonotonicity",
            "CandidateNotAuthority",
            "BoundedControlState",
            "NoRollback",
            "AtMostOneSpacecraftActivation",
            "SuccessRequiresEvidence",
            "DegradedNotSuccess",
            "StatusLossNotDivergence",
        }
        self.assertTrue(all(action in self.tla for action in required_actions))
        self.assertTrue(declared_properties.issubset(required_properties))
        self.assertTrue(all(name in self.tla for name in declared_properties))
        self.assertTrue(all(name in self.cfg for name in declared_properties))

    def test_formal_readme_rejects_concrete_security_claims(self):
        required_boundaries = [
            "concrete cryptographic primitive",
            "CCSDS or SDLS conformance",
            "flight-software behavior",
            "operational spacecraft",
            "post-compromise security",
        ]
        self.assertTrue(all(text in self.readme for text in required_boundaries))
        self.assertIn("NOT_REACHED_WITHIN_PROVISIONAL_BOUND", self.readme)

    def test_external_review_stop_points_cover_formalization_and_publication(self):
        stops = " ".join(self.spec["mandatory_external_review_stop_points"])
        for phrase in (
            "formal property set",
            "concrete cryptographic security",
            "concrete protocol implementation",
            "publication evidence",
            "external security claim",
        ):
            self.assertIn(phrase, stops)


if __name__ == "__main__":
    unittest.main()
