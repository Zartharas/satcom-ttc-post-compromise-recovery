from __future__ import annotations

import unittest

from ttc_recovery.formal_adverse_validation import (
    ABSENT_CASES,
    ADVERSE_CASES,
    ADVERSE_WITNESS_STATUS,
    CAPTURED_CASES,
    NOT_REACHED_STATUS,
    count_outcome_assignments,
    replay_python_adverse,
)
from ttc_recovery.formal_cross_validation import COMPARISON_FIELDS, compare_traces


class FormalAdverseValidationTests(unittest.TestCase):
    def test_case_population_is_three_captured_and_three_absent(self) -> None:
        self.assertEqual(len(ADVERSE_CASES), 6)
        self.assertEqual(len(CAPTURED_CASES), 3)
        self.assertEqual(len(ABSENT_CASES), 3)
        self.assertEqual(
            {case.outcome for case in CAPTURED_CASES},
            {"INDETERMINATE", "SECURE_DEGRADED", "EXPIRED"},
        )
        self.assertEqual(
            {case.outcome for case in ABSENT_CASES},
            {"DIVERGED", "AVAILABLE_UNSAFE", "LOCKED"},
        )

    def test_captured_cases_have_unique_explicit_action_paths(self) -> None:
        paths = [case.expected_actions for case in CAPTURED_CASES]
        self.assertEqual(len(paths), len(set(paths)))
        for case in CAPTURED_CASES:
            self.assertEqual(case.expected_actions[0], "Init")
            self.assertTrue(case.expected_actions[-1].startswith(("Drop", "Expire")))

    def test_indeterminate_replay_reaches_declared_outcome(self) -> None:
        case = next(case for case in CAPTURED_CASES if case.outcome == "INDETERMINATE")
        trace = replay_python_adverse(case, case.expected_actions)
        self.assertEqual(trace[-1]["state"]["outcome"], "INDETERMINATE")
        self.assertTrue(trace[-1]["state"]["statusDropped"])
        self.assertFalse(trace[-1]["state"]["verified"])

    def test_secure_degraded_replay_retains_receipt_evidence_projection(self) -> None:
        case = next(case for case in CAPTURED_CASES if case.outcome == "SECURE_DEGRADED")
        trace = replay_python_adverse(case, case.expected_actions)
        terminal = trace[-1]["state"]
        self.assertEqual(terminal["outcome"], "SECURE_DEGRADED")
        self.assertEqual(terminal["gMode"], "EXPIRED")
        self.assertEqual(terminal["sMode"], "ACTIVATED")
        self.assertTrue(terminal["receipt"])

    def test_expired_replay_ends_before_activation(self) -> None:
        case = next(case for case in CAPTURED_CASES if case.outcome == "EXPIRED")
        trace = replay_python_adverse(case, case.expected_actions)
        terminal = trace[-1]["state"]
        self.assertEqual(terminal["outcome"], "EXPIRED")
        self.assertEqual(terminal["activationCount"], 0)
        self.assertFalse(terminal["receipt"])

    def test_replay_rejects_absence_diagnostic(self) -> None:
        with self.assertRaises(ValueError):
            replay_python_adverse(ABSENT_CASES[0], ("Init",))

    def test_replay_rejects_action_drift(self) -> None:
        case = CAPTURED_CASES[0]
        with self.assertRaises(ValueError):
            replay_python_adverse(case, (*case.expected_actions[:-1], "Verify"))

    def test_python_projection_self_comparison_matches_all_fields(self) -> None:
        case = CAPTURED_CASES[0]
        python_trace = replay_python_adverse(case, case.expected_actions)
        formal_trace = [
            {"step": index + 1, "action": row["action"], "state": dict(row["state"])}
            for index, row in enumerate(python_trace)
        ]
        rows, summary = compare_traces(formal_trace, python_trace)
        expected_rows = len(python_trace) * (len(COMPARISON_FIELDS) + 1)
        self.assertEqual(summary["comparison_rows"], expected_rows)
        self.assertEqual(summary["mismatch_count"], 0)
        self.assertTrue(all(row["match"] for row in rows))

    def test_outcome_assignment_audit_distinguishes_modeled_and_absent(self) -> None:
        text = '\n'.join(
            [
                'outcome\' = "INDETERMINATE"',
                'outcome\' = "SECURE_DEGRADED"',
                'outcome\' = "EXPIRED"',
            ]
        )
        self.assertEqual(count_outcome_assignments(text, "INDETERMINATE"), 1)
        self.assertEqual(count_outcome_assignments(text, "DIVERGED"), 0)

    def test_status_vocabulary_does_not_claim_proof(self) -> None:
        combined = f"{ADVERSE_WITNESS_STATUS} {NOT_REACHED_STATUS}".lower()
        self.assertNotIn("proved", combined)
        self.assertNotIn("formally verified", combined)
        self.assertNotIn("impossible", combined)


if __name__ == "__main__":
    unittest.main()
