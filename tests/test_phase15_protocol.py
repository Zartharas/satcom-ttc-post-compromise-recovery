from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads(
    (ROOT / "spec" / "phase-15-experiment-protocol-candidate.json").read_text(
        encoding="utf-8"
    )
)
CONFIG = json.loads(
    (ROOT / "experiments" / "configs" / "phase-15-pilot.json").read_text(
        encoding="utf-8"
    )
)


class Phase15ProtocolTests(unittest.TestCase):
    def test_status_remains_provisional_and_not_publication_evidence(self) -> None:
        self.assertEqual(
            SPEC["status"],
            "PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE",
        )
        self.assertEqual(CONFIG["run_class"], "PILOT_INTERNAL_VALIDATION_ONLY")
        self.assertFalse(SPEC["pilot_scope"]["publication_evidence"])
        self.assertFalse(SPEC["pilot_scope"]["comparative_claims_allowed"])

    def test_phase14_review_gate_remains_open(self) -> None:
        self.assertEqual(SPEC["review_gate"]["issue"], 3)
        self.assertEqual(SPEC["review_gate"]["status"], "OPEN")
        self.assertEqual(
            SPEC["source_base"]["baseline_review_status"],
            "PENDING_INDEPENDENT_REVIEW",
        )
        self.assertEqual(
            SPEC["source_base"]["oracle_freeze_status"], "NOT_PERMITTED"
        )

    def test_research_questions_are_unique_and_provisional(self) -> None:
        questions = SPEC["research_questions"]
        ids = [row["id"] for row in questions]
        self.assertEqual(ids, ["RQ-1", "RQ-2", "RQ-3"])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertNotIn("FROZEN", {row["status"] for row in questions})

    def test_baseline_metric_parity_gap_is_explicit(self) -> None:
        treatments = {row["id"]: row for row in SPEC["treatments"]}
        self.assertEqual(set(treatments), {"B0", "B1", "B2", "T1"})
        for treatment in ("B0", "B1", "B2"):
            self.assertEqual(
                treatments[treatment]["publication_metric_parity"], "MISSING"
            )
        self.assertEqual(
            treatments["T1"]["publication_metric_parity"],
            "AVAILABLE_PROVISIONALLY",
        )

    def test_pilot_parameters_match_config(self) -> None:
        candidate = SPEC["candidate_parameters"]
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
            self.assertEqual(candidate[key], CONFIG[key], key)

    def test_seed_and_fault_panels_are_complete(self) -> None:
        self.assertEqual(CONFIG["seeds"], list(range(7001, 7013)))
        self.assertEqual(len(CONFIG["seeds"]), len(set(CONFIG["seeds"])))
        self.assertEqual(
            set(CONFIG["allowed_faults"]),
            {
                "DROP",
                "DELAY",
                "DUPLICATE",
                "REORDER",
                "CONTACT_CLOSE",
                "ENDPOINT_RESTART",
                "STALE_COUNTER",
                "STALE_REPLAY",
            },
        )

    def test_exclusions_and_reruns_cannot_be_outcome_seeking(self) -> None:
        exclusions = " ".join(SPEC["exclusion_rules"])
        self.assertIn("Do not exclude a run because its outcome", exclusions)
        self.assertIn(
            "preferred outcome", SPEC["rerun_policy"]["prohibited_reason"]
        )
        self.assertIn(
            "Preserve the original failed or superseded attempt",
            SPEC["rerun_policy"]["preservation_rule"],
        )

    def test_capture_controls_are_enabled_and_outputs_are_separate(self) -> None:
        self.assertEqual(set(CONFIG["capture_controls"].values()), {True})
        self.assertTrue(CONFIG["outputs"]["json"].startswith("results/raw/"))
        self.assertTrue(CONFIG["outputs"]["csv"].startswith("results/processed/"))

    def test_hard_claim_boundaries_remain_prohibited(self) -> None:
        allowed = {"NOT_PERMITTED", "NOT_PERMITTED_FOR_PILOT"}
        self.assertFalse(set(SPEC["hard_claim_boundaries"].values()) - allowed)
        self.assertEqual(
            CONFIG["claim_boundary"]["publication_evidence"], "NOT_PERMITTED"
        )
        self.assertEqual(
            CONFIG["claim_boundary"]["cryptographic_security_or_pcs"],
            "NOT_PERMITTED",
        )

    def test_required_outputs_exist(self) -> None:
        for relative in SPEC["required_outputs"]:
            self.assertTrue((ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
