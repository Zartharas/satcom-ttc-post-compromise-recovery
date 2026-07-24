from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments/scripts/validate_review_handoff.py"
SPEC = importlib.util.spec_from_file_location("validate_review_handoff", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReviewHandoffTests(unittest.TestCase):
    def test_candidate_matches_scenario_catalog(self):
        self.assertEqual(MODULE.validate_candidate(ROOT), [])

    def test_candidate_contains_unique_oracle_ids(self):
        candidate = json.loads(
            (ROOT / "spec/baseline-oracle-freeze-candidate.json").read_text(
                encoding="utf-8"
            )
        )
        ids = [item["id"] for item in candidate["oracles"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 21)

    def test_candidate_requires_independent_review(self):
        candidate = json.loads(
            (ROOT / "spec/baseline-oracle-freeze-candidate.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(candidate["status"], "PENDING_INDEPENDENT_REVIEW")
        self.assertEqual(candidate["review"]["decision"], "PENDING")
        self.assertIsNone(candidate["review"]["reviewer_name"])
        self.assertFalse(candidate["review"]["manifest_verified"])


if __name__ == "__main__":
    unittest.main()
