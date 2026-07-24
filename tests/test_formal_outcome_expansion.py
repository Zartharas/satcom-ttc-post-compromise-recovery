from __future__ import annotations

import unittest
from pathlib import Path

from ttc_recovery.formal_adverse_validation import count_outcome_assignments
from ttc_recovery.formal_cross_validation import compare_traces
from ttc_recovery.formal_outcome_expansion import (
    BASELINE_PRESERVED_STATUS,
    BASELINE_SPEC_SHA256,
    EXPANSION_CASES,
    EXPANSION_DIAGNOSTIC_STATUS,
    EXPANSION_WITNESS_STATUS,
    canonical_baseline_outcome,
    replay_python_expansion,
)
from ttc_recovery.formal_execution import sha256_file


class FormalOutcomeExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.baseline_path = cls.root / "formal" / "tla" / "T1Recovery.tla"
        cls.expanded_path = cls.root / "formal" / "tla" / "T1RecoveryOutcomeExpansion.tla"
        cls.baseline_text = cls.baseline_path.read_text(encoding="utf-8")
        cls.expanded_text = cls.expanded_path.read_text(encoding="utf-8")

    def test_case_population_is_three_unique_previously_absent_outcomes(self):
        self.assertEqual(
            {case.outcome for case in EXPANSION_CASES},
            {"DIVERGED", "AVAILABLE_UNSAFE", "LOCKED"},
        )
        self.assertEqual(len({case.case_id for case in EXPANSION_CASES}), 3)
        self.assertEqual(len({case.expected_actions for case in EXPANSION_CASES}), 3)

    def test_preserved_baseline_hash_is_exact(self):
        self.assertEqual(sha256_file(self.baseline_path), BASELINE_SPEC_SHA256)

    def test_assignments_are_absent_from_baseline_and_explicit_in_expansion(self):
        for case in EXPANSION_CASES:
            with self.subTest(case=case.case_id):
                self.assertEqual(count_outcome_assignments(self.baseline_text, case.outcome), 0)
                self.assertEqual(count_outcome_assignments(self.expanded_text, case.outcome), 1)

    def test_every_expansion_has_an_explicit_cause(self):
        for case in EXPANSION_CASES:
            with self.subTest(case=case.case_id):
                self.assertIn(case.expected_gap_cause, self.expanded_text)
                self.assertNotEqual(case.expected_gap_cause, "NONE")

    def test_canonical_baseline_scenarios_reach_expected_outcomes(self):
        for case in EXPANSION_CASES:
            with self.subTest(case=case.case_id):
                result = canonical_baseline_outcome(case)
                self.assertEqual(result["outcome"], case.outcome)
                self.assertEqual(result["scenario"], case.canonical_scenario)
                self.assertTrue(result["event_names"])

    def test_python_expansion_replays_reach_expected_outcomes(self):
        for case in EXPANSION_CASES:
            with self.subTest(case=case.case_id):
                trace, cause = replay_python_expansion(case, case.expected_actions)
                self.assertEqual(trace[-1]["state"]["outcome"], case.outcome)
                self.assertEqual(cause, case.expected_gap_cause)
                self.assertEqual(len(trace), len(case.expected_actions))

    def test_python_projection_self_comparison_matches_all_fields(self):
        for case in EXPANSION_CASES:
            with self.subTest(case=case.case_id):
                trace, _ = replay_python_expansion(case, case.expected_actions)
                rows, summary = compare_traces(trace, trace)
                self.assertEqual(summary["mismatch_count"], 0)
                self.assertEqual(summary["comparison_rows"], len(trace) * 17)
                self.assertTrue(all(bool(row["match"]) for row in rows))

    def test_replay_rejects_action_drift(self):
        case = EXPANSION_CASES[0]
        with self.assertRaises(ValueError):
            replay_python_expansion(case, case.expected_actions[:-1])

    def test_diverged_path_is_not_terminal_lock(self):
        case = next(row for row in EXPANSION_CASES if row.case_id == "diverged")
        trace, _ = replay_python_expansion(case, case.expected_actions)
        final = trace[-1]["state"]
        self.assertEqual(final["outcome"], "DIVERGED")
        self.assertEqual(final["gMode"], "NORMAL")
        self.assertEqual(final["sMode"], "EXPIRED")

    def test_available_unsafe_path_is_aligned_and_verified(self):
        case = next(row for row in EXPANSION_CASES if row.case_id == "available-unsafe")
        trace, _ = replay_python_expansion(case, case.expected_actions)
        final = trace[-1]["state"]
        self.assertEqual(final["gEpoch"], final["sEpoch"])
        self.assertTrue(final["verified"])
        self.assertTrue(final["commandAccepted"])
        self.assertTrue(final["statusSeen"])

    def test_locked_path_advances_only_ground_epoch(self):
        case = next(row for row in EXPANSION_CASES if row.case_id == "locked")
        trace, _ = replay_python_expansion(case, case.expected_actions)
        final = trace[-1]["state"]
        self.assertGreater(final["gEpoch"], final["sEpoch"])
        self.assertEqual(final["outcome"], "LOCKED")
        self.assertFalse(final["verified"])

    def test_status_vocabulary_does_not_claim_completeness_or_proof(self):
        values = {
            BASELINE_PRESERVED_STATUS,
            EXPANSION_DIAGNOSTIC_STATUS,
            EXPANSION_WITNESS_STATUS,
        }
        joined = " ".join(values).lower()
        self.assertNotIn("proved", joined)
        self.assertNotIn("complete model", joined)
        self.assertNotIn("formally secure", joined)


if __name__ == "__main__":
    unittest.main()
