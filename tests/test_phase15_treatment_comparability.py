from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from ttc_recovery.treatment_comparability import (
    MATRIX_STATUS,
    normalize_alignment,
    project_allowed_metrics,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX = json.loads(
    (ROOT / "spec" / "phase-15-treatment-comparability-matrix.json").read_text(
        encoding="utf-8"
    )
)
BASELINE = json.loads(
    (ROOT / "tests" / "scenarios" / "baseline-test-catalog.json").read_text(
        encoding="utf-8"
    )
)
T1 = json.loads(
    (ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json").read_text(
        encoding="utf-8"
    )
)


class Phase15TreatmentComparabilityTests(unittest.TestCase):
    def test_matrix_remains_provisional_and_non_evidentiary(self) -> None:
        self.assertEqual(MATRIX["status"], MATRIX_STATUS)
        self.assertFalse(MATRIX["comparison_authorization"]["publication_evidence"])
        self.assertEqual(
            MATRIX["comparison_authorization"]["pooled_cross_treatment_aggregation"],
            "NOT_PERMITTED",
        )
        self.assertEqual(
            set(MATRIX["hard_claim_boundaries"].values()), {"NOT_PERMITTED"}
        )

    def test_alignment_class_normalization_is_explicit(self) -> None:
        self.assertEqual(normalize_alignment("SYNC(0)"), "SYNC")
        self.assertEqual(normalize_alignment("SYNC(27)"), "SYNC")
        self.assertEqual(normalize_alignment("G_AHEAD"), "G_AHEAD")
        self.assertEqual(normalize_alignment("S_AHEAD"), "S_AHEAD")
        self.assertEqual(normalize_alignment("DIVERGED"), "DIVERGED")
        self.assertEqual(normalize_alignment("LOCKED"), "LOCKED")
        with self.assertRaises(ValueError):
            normalize_alignment("SYNC")
        with self.assertRaises(ValueError):
            normalize_alignment("UNKNOWN")

    def test_metric_projection_derives_alignment_without_aggregation(self) -> None:
        metrics = {
            "outcome": "SUCCESS",
            "alignment": "SYNC(3)",
            "security_state": "SECURE_PROVISIONAL",
        }
        projected = project_allowed_metrics(
            metrics,
            ["outcome", "alignment_class", "security_state"],
        )
        self.assertEqual(
            projected,
            {
                "outcome": "SUCCESS",
                "alignment_class": "SYNC",
                "security_state": "SECURE_PROVISIONAL",
            },
        )
        with self.assertRaises(KeyError):
            project_allowed_metrics(metrics, ["availability_state"])

    def test_family_population_is_four_qualified_and_four_diagnostic(self) -> None:
        families = MATRIX["comparison_families"]
        self.assertEqual(
            [row["id"] for row in families],
            [f"CF-{number:02d}" for number in range(1, 9)],
        )
        counts = Counter(row["classification"] for row in families)
        self.assertEqual(counts["QUALIFIED_MATCH"], 4)
        self.assertEqual(counts["DIAGNOSTIC_FAMILY_ONLY"], 4)
        self.assertNotIn("FULL_MATCH", counts)
        for family in families:
            self.assertGreaterEqual(
                len({member["treatment"] for member in family["members"]}),
                2,
            )
            if family["classification"] == "DIAGNOSTIC_FAMILY_ONLY":
                self.assertEqual(family["allowed_fields"], [])

    def test_all_catalog_scenarios_have_exactly_one_disposition(self) -> None:
        expected = {
            *(f"{str(row['baseline']).split('-')[0]}:{row['id']}" for row in BASELINE["tests"]),
            *(f"T1:{row['id']}" for row in T1["tests"]),
        }
        actual = [
            f"{row['treatment']}:{row['scenario_id']}"
            for row in MATRIX["scenario_disposition"]
        ]
        self.assertEqual(len(actual), len(set(actual)))
        self.assertEqual(set(actual), expected)
        self.assertEqual(len(actual), 36)

    def test_noncomparable_metrics_are_never_family_allowed(self) -> None:
        prohibited = set(
            MATRIX["metric_semantics"]["not_cross_treatment_comparable"]
        )
        self.assertTrue(
            {
                "alignment",
                "recovery_duration_contacts",
                "total_transmissions",
                "retry_overhead",
            }.issubset(prohibited)
        )
        for family in MATRIX["comparison_families"]:
            self.assertFalse(set(family["allowed_fields"]) & prohibited)

    def test_population_rules_reject_pooled_catalog_percentages(self) -> None:
        rules = " ".join(MATRIX["population_rules"])
        self.assertIn("Do not pool the 21 curated baseline catalog rows", rules)
        self.assertIn("Do not calculate treatment success percentages", rules)
        self.assertIn("not independent replicates", rules)

    def test_treatment_specific_and_guard_cases_remain_excluded(self) -> None:
        dispositions = {
            f"{row['treatment']}:{row['scenario_id']}": row["disposition"]
            for row in MATRIX["scenario_disposition"]
        }
        self.assertEqual(dispositions["B0:B0-03"], "TREATMENT_SPECIFIC")
        self.assertEqual(dispositions["B2:B2-06"], "TREATMENT_SPECIFIC")
        self.assertEqual(dispositions["T1:T1-10"], "NON_OUTCOME_GUARD")
        self.assertEqual(dispositions["T1:T1-14"], "NON_OUTCOME_GUARD")


if __name__ == "__main__":
    unittest.main()
