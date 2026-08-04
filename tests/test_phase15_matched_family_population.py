from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from ttc_recovery.matched_family_population import (
    POPULATION_STATUS,
    execute_matched_family_population,
    verify_derived_manifest,
    write_matched_family_population,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads(
    (
        ROOT
        / "experiments"
        / "configs"
        / "phase-15-matched-family-population.json"
    ).read_text(encoding="utf-8")
)
MATRIX = json.loads(
    (
        ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"
    ).read_text(encoding="utf-8")
)
BASELINE = json.loads(
    (
        ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"
    ).read_text(encoding="utf-8")
)
T1 = json.loads(
    (
        ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json"
    ).read_text(encoding="utf-8")
)


class Phase15MatchedFamilyPopulationTests(unittest.TestCase):
    def payload(self) -> dict:
        return execute_matched_family_population(
            CONFIG,
            MATRIX,
            BASELINE,
            T1,
        )

    def test_population_counts_and_status_remain_provisional(self) -> None:
        payload = self.payload()
        self.assertEqual(payload["status"], POPULATION_STATUS)
        self.assertEqual(payload["family_count"], 4)
        self.assertEqual(payload["member_row_count"], 13)
        self.assertEqual(payload["analysis_unit_count"], 12)
        self.assertFalse(payload["publication_evidence"])

    def test_only_qualified_families_are_executed(self) -> None:
        payload = self.payload()
        self.assertEqual(
            payload["eligible_family_ids"],
            ["CF-01", "CF-02", "CF-05", "CF-06"],
        )
        self.assertEqual(
            {row["family_classification"] for row in payload["rows"]},
            {"QUALIFIED_MATCH"},
        )
        self.assertFalse(
            {"CF-03", "CF-04", "CF-07", "CF-08"}
            & {row["family_id"] for row in payload["rows"]}
        )

    def test_runtime_members_match_the_matrix_exactly(self) -> None:
        payload = self.payload()
        expected = {
            (
                family["id"],
                member["treatment"],
                member["source_id"],
            )
            for family in MATRIX["comparison_families"]
            if family["id"] in CONFIG["eligible_family_ids"]
            for member in family["members"]
        }
        actual = {
            (row["family_id"], row["treatment"], row["source_id"])
            for row in payload["rows"]
        }
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 13)

    def test_every_projection_contains_exactly_the_family_allowed_fields(self) -> None:
        payload = self.payload()
        family_index = {
            row["id"]: row for row in MATRIX["comparison_families"]
        }
        prohibited = {
            "alignment",
            "recovery_duration_contacts",
            "total_transmissions",
            "retry_overhead",
        }
        for row in payload["rows"]:
            expected = set(family_index[row["family_id"]]["allowed_fields"])
            actual = set(row["projected_metrics"])
            self.assertEqual(actual, expected)
            self.assertFalse(actual & prohibited)
            self.assertEqual(len(row["source_execution_sha256"]), 64)

    def test_t1_catalog_members_match_internal_design_oracles(self) -> None:
        payload = self.payload()
        t1_rows = {
            row["row_id"]: row
            for row in payload["source_executions"]
            if row["execution"].get("treatment") == "T1"
        }
        self.assertEqual(len(t1_rows), 4)
        for row in t1_rows.values():
            oracle = row["execution"]["catalog_oracle"]
            self.assertEqual(
                oracle["status"], "MATCHED_INTERNAL_DESIGN_ORACLE"
            )
            self.assertFalse(row["execution"]["publication_evidence"])
            self.assertFalse(row["execution"]["seed_is_comparable"])

    def test_cf02_b1_variants_share_one_analysis_unit(self) -> None:
        payload = self.payload()
        cf02_rows = [
            row for row in payload["rows"] if row["family_id"] == "CF-02"
        ]
        b1_rows = [row for row in cf02_rows if row["treatment"] == "B1"]
        self.assertEqual(len(cf02_rows), 5)
        self.assertEqual(len(b1_rows), 2)
        self.assertEqual(
            {row["analysis_unit_id"] for row in b1_rows}, {"CF-02:B1"}
        )
        denominator = next(
            row
            for row in payload["denominators"]
            if row["family_id"] == "CF-02"
        )
        self.assertEqual(denominator["member_row_count"], 5)
        self.assertEqual(denominator["analysis_unit_count"], 4)
        self.assertEqual(denominator["policy_variant_row_count"], 1)

    def test_comparison_and_rate_authorizations_remain_closed(self) -> None:
        payload = self.payload()
        authorization = payload["comparison_authorization"]
        self.assertEqual(
            authorization["family_specific_descriptive_comparison"],
            "NOT_YET_AUTHORIZED",
        )
        self.assertEqual(
            authorization["pooled_cross_treatment_aggregation"],
            "NOT_PERMITTED",
        )
        self.assertEqual(
            authorization["success_rate_or_percentage"], "NOT_PERMITTED"
        )
        self.assertEqual(
            authorization["inferential_statistics"], "NOT_PERMITTED"
        )
        self.assertFalse(authorization["publication_evidence"])
        for row in payload["denominators"]:
            self.assertFalse(row["aggregate_authorized"])
            self.assertEqual(
                row["success_rate_denominator"], "NOT_DEFINED"
            )

    def test_repeat_execution_has_identical_source_digests(self) -> None:
        first = self.payload()
        second = self.payload()
        first_digests = {
            row["row_id"]: row["source_execution_sha256"]
            for row in first["rows"]
        }
        second_digests = {
            row["row_id"]: row["source_execution_sha256"]
            for row in second["rows"]
        }
        self.assertEqual(first_digests, second_digests)

    def test_json_csv_and_manifest_outputs_verify(self) -> None:
        payload = self.payload()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "phase-15-matched-family-population.json"
            member_csv = root / "phase-15-matched-family-members.csv"
            denominator_csv = (
                root / "phase-15-matched-family-denominators.csv"
            )
            manifest = root / "phase-15-matched-family-derived.sha256"

            write_matched_family_population(
                payload,
                json_path,
                member_csv,
                denominator_csv,
                manifest,
            )
            verify_derived_manifest(root, manifest)

            loaded = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["member_row_count"], 13)
            with member_csv.open(
                "r", encoding="utf-8", newline=""
            ) as handle:
                member_rows = list(csv.DictReader(handle))
            with denominator_csv.open(
                "r", encoding="utf-8", newline=""
            ) as handle:
                denominator_rows = list(csv.DictReader(handle))
            self.assertEqual(len(member_rows), 13)
            self.assertEqual(len(denominator_rows), 4)
            self.assertNotIn("outcome", member_rows[0])
            self.assertIn("projected_metrics_json", member_rows[0])

            member_csv.write_text(
                member_csv.read_text(encoding="utf-8") + "tamper\n",
                encoding="utf-8",
            )
            with self.assertRaises(RuntimeError):
                verify_derived_manifest(root, manifest)


if __name__ == "__main__":
    unittest.main()
