from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ttc_recovery.formal_execution import (
    COUNTEREXAMPLE_STATUS,
    NO_COUNTEREXAMPLE_STATUS,
    TOOL_ERROR_STATUS,
    extract_counterexample_trace,
    parse_tlc_summary,
    sha1_file,
    sha256_file,
)


POSITIVE_LOG = """
TLC2 Version 2.18 of Day Month 20??
Model checking completed. No error has been found.
125 states generated, 42 distinct states found, 0 states left on queue.
The depth of the complete state graph search is 8.
"""

NEGATIVE_LOG = r"""
Error: Invariant NegativeControlNoActivation is violated.
State 1: <Initial predicate>
/\ gMode = "NORMAL"
/\ activationCount = 0
State 2: <Prepare line 68, col 1 to line 78, col 6 of module T1Recovery>
/\ gMode = "RECOVERING"
/\ activationCount = 0
State 3: <Commit line 94, col 1 to line 107, col 6 of module T1Recovery>
/\ gMode = "CANDIDATE"
/\ activationCount = 1
3 states generated, 3 distinct states found, 0 states left on queue.
The depth of the complete state graph search is 3.
"""


class FormalExecutionTests(unittest.TestCase):
    def test_positive_summary_uses_bounded_non_claim_status(self) -> None:
        summary = parse_tlc_summary(POSITIVE_LOG, 0)
        self.assertEqual(summary.status, NO_COUNTEREXAMPLE_STATUS)
        self.assertEqual(summary.generated_states, 125)
        self.assertEqual(summary.distinct_states, 42)
        self.assertEqual(summary.queued_states, 0)
        self.assertEqual(summary.search_depth, 8)

    def test_positive_summary_accepts_comma_separated_counts(self) -> None:
        log = POSITIVE_LOG.replace("125 states", "1,125 states").replace(
            "42 distinct", "1,042 distinct"
        )
        summary = parse_tlc_summary(log, 0)
        self.assertEqual(summary.generated_states, 1125)
        self.assertEqual(summary.distinct_states, 1042)

    def test_nonzero_without_violation_is_tool_error(self) -> None:
        summary = parse_tlc_summary("Error: parse failed", 1)
        self.assertEqual(summary.status, TOOL_ERROR_STATUS)

    def test_counterexample_summary_records_invariant(self) -> None:
        summary = parse_tlc_summary(NEGATIVE_LOG, 12)
        self.assertEqual(summary.status, COUNTEREXAMPLE_STATUS)
        self.assertEqual(summary.violated_invariant, "NegativeControlNoActivation")
        self.assertEqual(summary.trace_state_count, 3)
        self.assertEqual(summary.search_depth, 3)

    def test_counterexample_trace_extracts_ordered_states(self) -> None:
        trace = extract_counterexample_trace(NEGATIVE_LOG)
        self.assertEqual([state["state_number"] for state in trace], [1, 2, 3])
        self.assertEqual(trace[0]["assignments"]["gMode"], '"NORMAL"')
        self.assertEqual(trace[2]["assignments"]["activationCount"], "1")

    def test_counterexample_trace_preserves_transition_label(self) -> None:
        trace = extract_counterexample_trace(NEGATIVE_LOG)
        self.assertIn("Commit", trace[2]["label"])

    def test_missing_trace_returns_empty_list(self) -> None:
        self.assertEqual(extract_counterexample_trace("No trace"), [])

    def test_sha_helpers_hash_exact_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.bin"
            path.write_bytes(b"abc")
            self.assertEqual(sha1_file(path), "a9993e364706816aba3e25717850c26c9cd0d89d")
            self.assertEqual(
                sha256_file(path),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )

    def test_positive_status_requires_success_marker(self) -> None:
        log = "125 states generated, 42 distinct states found, 0 states left on queue."
        self.assertEqual(parse_tlc_summary(log, 0).status, TOOL_ERROR_STATUS)

    def test_negative_control_is_not_labeled_positive_success(self) -> None:
        summary = parse_tlc_summary(NEGATIVE_LOG, 12)
        self.assertNotEqual(summary.status, NO_COUNTEREXAMPLE_STATUS)


if __name__ == "__main__":
    unittest.main()
