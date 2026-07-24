import unittest

from ttc_recovery.formal_cross_validation import (
    BASELINE_COUNTS,
    BOUND_CASES,
    COMPARISON_FIELDS,
    EXPECTED_ACTIONS,
    TRACE_MATCH_STATUS,
    action_from_label,
    compare_traces,
    decode_tla_scalar,
    normalize_formal_trace,
    replay_python_success,
)


class FormalCrossValidationTests(unittest.TestCase):
    def test_tla_scalar_decoder_handles_supported_values(self):
        self.assertIs(decode_tla_scalar("TRUE"), True)
        self.assertIs(decode_tla_scalar("FALSE"), False)
        self.assertEqual(decode_tla_scalar("-1"), -1)
        self.assertEqual(decode_tla_scalar('"SUCCESS"'), "SUCCESS")

    def test_action_label_decoder_handles_initial_and_transition_labels(self):
        self.assertEqual(action_from_label("<Initial predicate>"), "Init")
        self.assertEqual(
            action_from_label("<SelectCandidate line 80, col 5 of module T1Recovery>"),
            "SelectCandidate",
        )
        self.assertEqual(action_from_label("unrecognized"), "UNKNOWN")

    def test_normalize_formal_trace_decodes_assignments(self):
        trace = [
            {
                "state_number": 1,
                "label": "<Initial predicate>",
                "assignments": {
                    "gMode": '"NORMAL"',
                    "sMode": '"NORMAL"',
                    "gEpoch": "2",
                    "sEpoch": "1",
                    "pending": "FALSE",
                    "verified": "FALSE",
                },
            }
        ]
        normalized = normalize_formal_trace(trace)
        self.assertEqual(normalized[0]["action"], "Init")
        self.assertEqual(normalized[0]["state"]["gEpoch"], 2)
        self.assertIs(normalized[0]["state"]["pending"], False)

    def test_python_replay_matches_expected_action_sequence(self):
        trace = replay_python_success(EXPECTED_ACTIONS)
        self.assertEqual([row["action"] for row in trace], list(EXPECTED_ACTIONS))
        self.assertEqual(trace[-1]["state"]["outcome"], "SUCCESS")
        self.assertIs(trace[-1]["state"]["verified"], True)
        self.assertEqual(trace[-1]["state"]["gEpoch"], 3)
        self.assertEqual(trace[-1]["state"]["sEpoch"], 3)

    def test_python_replay_rejects_unexpected_formal_path(self):
        with self.assertRaises(ValueError):
            replay_python_success(("Init", "Prepare", "Retry"))

    def test_trace_comparison_reports_exact_match(self):
        trace = replay_python_success(EXPECTED_ACTIONS)
        rows, summary = compare_traces(trace, trace)
        self.assertEqual(summary["mismatch_count"], 0)
        self.assertEqual(summary["comparison_rows"], len(EXPECTED_ACTIONS) * 17)
        self.assertTrue(all(row["match"] for row in rows))

    def test_trace_comparison_exposes_field_mismatch(self):
        formal = replay_python_success(EXPECTED_ACTIONS)
        python = replay_python_success(EXPECTED_ACTIONS)
        python[3]["state"]["sEpoch"] = 99
        rows, summary = compare_traces(formal, python)
        self.assertEqual(summary["mismatch_count"], 1)
        mismatch = [row for row in rows if not row["match"]]
        self.assertEqual(mismatch[0]["field"], "sEpoch")

    def test_comparison_field_set_is_complete_and_unique(self):
        self.assertEqual(len(COMPARISON_FIELDS), 16)
        self.assertEqual(len(set(COMPARISON_FIELDS)), len(COMPARISON_FIELDS))
        for required in ("gMode", "sMode", "candidateEpoch", "verified", "outcome"):
            self.assertIn(required, COMPARISON_FIELDS)

    def test_bound_panel_is_small_unique_and_contains_baseline(self):
        ids = [case.case_id for case in BOUND_CASES]
        self.assertEqual(len(ids), 5)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("base-3-6", ids)
        self.assertEqual(BASELINE_COUNTS["generated_states"], 50)
        self.assertEqual(BASELINE_COUNTS["distinct_states"], 28)

    def test_status_vocabulary_does_not_claim_proof(self):
        self.assertEqual(TRACE_MATCH_STATUS, "MATCH_WITHIN_DECLARED_ABSTRACTION")
        self.assertNotIn("PROOF", TRACE_MATCH_STATUS)
        self.assertNotIn("EQUIVALENT", TRACE_MATCH_STATUS)


if __name__ == "__main__":
    unittest.main()
