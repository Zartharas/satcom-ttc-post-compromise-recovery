from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec" / "phase-14-independent-review-package.json"


class Phase14ReviewPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))

    def test_package_remains_ready_for_outreach_not_reviewed(self):
        self.assertEqual(self.spec["status"], "READY_FOR_OUTREACH_NOT_REVIEWED")
        self.assertEqual(
            self.spec["source_base"]["baseline_review_status"],
            "PENDING_INDEPENDENT_REVIEW",
        )
        self.assertEqual(self.spec["review_issue"]["number"], 3)
        self.assertEqual(self.spec["review_issue"]["status"], "OPEN")

    def test_review_questions_are_complete_and_unique(self):
        questions = [
            q for group in self.spec["question_groups"] for q in group["questions"]
        ]
        ids = [q["id"] for q in questions]
        self.assertEqual(len(ids), 24)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("B1-R5", ids)

    def test_scenario_oracle_population_is_complete_and_pending(self):
        review = self.spec["scenario_oracle_review"]
        self.assertEqual(review["status"], "PENDING")
        self.assertEqual(len(review["oracle_ids"]), 21)
        self.assertEqual(len(review["oracle_ids"]), len(set(review["oracle_ids"])))

    def test_governance_findings_remain_open(self):
        findings = self.spec["governance_findings"]
        self.assertEqual(len(findings), 4)
        self.assertEqual(
            {row["status"] for row in findings}, {"OPEN_REQUIRES_REVIEW"}
        )

    def test_claim_statuses_preserve_prohibited_boundaries(self):
        claims = self.spec["claims"]
        self.assertEqual(len(claims), 20)
        self.assertIn(
            "GOVERNANCE_EXCEPTION_REQUIRES_REVIEW",
            {row["status"] for row in claims},
        )
        self.assertEqual(
            set(self.spec["claim_boundaries"].values()), {"NOT_PERMITTED"}
        )

    def test_all_claim_evidence_paths_exist(self):
        for claim in self.spec["claims"]:
            self.assertTrue(claim["evidence_paths"], claim["id"])
            for relative in claim["evidence_paths"]:
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_phase05_gap_is_documented_without_rewriting_history(self):
        gate = (
            ROOT / "governance" / "phase-04-independent-review-gate.md"
        ).read_text(encoding="utf-8")
        old_template = (
            ROOT / "governance" / "phase-05-reviewer-response-template.md"
        ).read_text(encoding="utf-8")
        new_template = (
            ROOT / "governance" / "phase-14-reviewer-response-template.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Does any B1 test rely on information unavailable", gate)
        self.assertNotIn("B1-R5", old_template)
        self.assertIn("B1-R5", new_template)

    def test_oracle_candidate_contains_no_unsupported_approval(self):
        candidate = json.loads(
            (ROOT / "spec" / "baseline-oracle-freeze-candidate.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(candidate["status"], "PENDING_INDEPENDENT_REVIEW")
        self.assertEqual(candidate["review"]["decision"], "PENDING")
        self.assertIsNone(candidate["review"]["reviewer_name"])
        self.assertIsNone(candidate["review"]["approved_commit"])
        self.assertFalse(candidate["review"]["manifest_verified"])

    def test_claim_and_evidence_csv_ids_match_json(self):
        with (
            ROOT / "governance" / "phase-14-claims-traceability.csv"
        ).open("r", encoding="utf-8", newline="") as handle:
            claim_rows = list(csv.DictReader(handle))
        with (
            ROOT / "governance" / "phase-14-evidence-index.csv"
        ).open("r", encoding="utf-8", newline="") as handle:
            evidence_rows = list(csv.DictReader(handle))
        self.assertEqual(
            [row["id"] for row in claim_rows],
            [row["id"] for row in self.spec["claims"]],
        )
        self.assertEqual(
            [row["id"] for row in evidence_rows],
            [row["id"] for row in self.spec["evidence_index"]],
        )
        self.assertEqual(
            {row["pin_method"] for row in evidence_rows},
            {"REVIEW_TARGET_COMMIT"},
        )


if __name__ == "__main__":
    unittest.main()
