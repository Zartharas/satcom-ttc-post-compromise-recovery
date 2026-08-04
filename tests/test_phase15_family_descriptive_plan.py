from __future__ import annotations

import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path

from ttc_recovery.family_descriptive_plan import (
    PLAN_OUTPUT_STATUS,
    build_family_descriptive_plan,
    verify_family_descriptive_manifest,
    write_family_descriptive_plan,
)
from ttc_recovery.matched_family_population import (
    execute_matched_family_population,
)


ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = (
    ROOT / "experiments" / "configs" / "phase-15-family-descriptive-plan.json"
)
MATRIX_PATH = ROOT / "spec" / "phase-15-treatment-comparability-matrix.json"
POPULATION_CONFIG_PATH = (
    ROOT / "experiments" / "configs" / "phase-15-matched-family-population.json"
)
BASELINE_CATALOG_PATH = ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"
T1_CATALOG_PATH = ROOT / "tests" / "scenarios" / "t1-provisional-test-catalog.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Phase15FamilyDescriptivePlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = load_json(PLAN_PATH)
        cls.matrix = load_json(MATRIX_PATH)
        cls.population_config = load_json(POPULATION_CONFIG_PATH)
        cls.population = execute_matched_family_population(
            cls.population_config,
            cls.matrix,
            load_json(BASELINE_CATALOG_PATH),
            load_json(T1_CATALOG_PATH),
        )
        cls.payload = build_family_descriptive_plan(
            cls.plan,
            cls.matrix,
            cls.population_config,
            cls.population,
        )

    def test_status_and_counts_remain_candidate_only(self) -> None:
        self.assertEqual(self.payload["status"], PLAN_OUTPUT_STATUS)
        self.assertEqual(self.payload["family_count"], 4)
        self.assertEqual(self.payload["member_row_count"], 13)
        self.assertEqual(self.payload["analysis_unit_count"], 12)
        self.assertEqual(self.payload["observation_cutoff_count"], 4)
        self.assertEqual(self.payload["denominator_candidate_count"], 4)
        self.assertFalse(self.payload["publication_evidence"])

    def test_exact_family_order_and_unique_cutoffs(self) -> None:
        self.assertEqual(
            [row["family_id"] for row in self.payload["family_plans"]],
            ["CF-01", "CF-02", "CF-05", "CF-06"],
        )
        cutoff_ids = [row["cutoff_id"] for row in self.payload["family_plans"]]
        self.assertEqual(len(cutoff_ids), len(set(cutoff_ids)))
        self.assertTrue(
            all(
                row["observation_cutoff"].startswith("Stop ")
                for row in self.payload["family_plans"]
            )
        )

    def test_member_and_analysis_unit_registries_are_exact(self) -> None:
        row_ids = [row["row_id"] for row in self.payload["member_registry"]]
        unit_ids = [
            row["analysis_unit_id"]
            for row in self.payload["analysis_unit_registry"]
        ]
        self.assertEqual(len(row_ids), 13)
        self.assertEqual(len(set(row_ids)), 13)
        self.assertEqual(len(unit_ids), 12)
        self.assertEqual(len(set(unit_ids)), 12)

    def test_cf02_policy_variants_share_one_denominator_unit(self) -> None:
        unit = next(
            row
            for row in self.payload["analysis_unit_registry"]
            if row["analysis_unit_id"] == "CF-02:B1"
        )
        self.assertEqual(
            unit["member_row_ids"],
            ["CF-02:B1:B1-01", "CF-02:B1:B1-05"],
        )
        self.assertEqual(unit["member_row_count"], 2)
        denominator = next(
            row
            for row in self.payload["denominator_candidates"]
            if row["family_id"] == "CF-02"
        )
        self.assertEqual(denominator["analysis_unit_count"], 4)
        self.assertEqual(denominator["member_row_count"], 5)
        self.assertEqual(denominator["policy_variant_row_count"], 1)

    def test_allowed_fields_match_the_d2_matrix_exactly(self) -> None:
        matrix_by_id = {
            row["id"]: row for row in self.matrix["comparison_families"]
        }
        for row in self.payload["family_plans"]:
            self.assertEqual(
                row["allowed_fields"],
                matrix_by_id[row["family_id"]]["allowed_fields"],
            )
        plan_by_family = {
            row["family_id"]: row for row in self.payload["family_plans"]
        }
        for member in self.payload["member_registry"]:
            self.assertEqual(
                member["allowed_fields"],
                plan_by_family[member["family_id"]]["allowed_fields"],
            )

    def test_plan_generation_is_outcome_blind(self) -> None:
        changed = copy.deepcopy(self.population)
        for index, row in enumerate(changed["rows"]):
            row["projected_metrics"] = {
                "synthetic_unread_value": f"mutated-{index}",
                "outcome": "POST_HOC_VALUE_THAT_MUST_NOT_BE_READ",
            }
        mutated_payload = build_family_descriptive_plan(
            self.plan,
            self.matrix,
            self.population_config,
            changed,
        )
        for field in (
            "identity_contract_sha256",
            "family_plans",
            "member_registry",
            "analysis_unit_registry",
            "denominator_candidates",
        ):
            self.assertEqual(mutated_payload[field], self.payload[field])
        self.assertFalse(
            mutated_payload["outcome_blindness"]["projected_metric_values_read"]
        )

    def test_denominator_and_claim_gates_remain_closed(self) -> None:
        for row in self.payload["denominator_candidates"]:
            self.assertEqual(row["denominator_state"], "CANDIDATE_NOT_FROZEN")
            self.assertEqual(row["success_rate_denominator"], "NOT_DEFINED")
            self.assertEqual(row["cross_family_denominator"], "NOT_PERMITTED")
            self.assertFalse(row["aggregate_authorized"])
        boundary = self.payload["claim_boundary"]
        self.assertEqual(
            boundary["family_specific_descriptive_comparison"],
            "NOT_YET_AUTHORIZED",
        )
        self.assertEqual(boundary["denominator_freeze"], "CANDIDATE_NOT_FROZEN")
        self.assertEqual(
            boundary["observation_cutoff_freeze"],
            "CANDIDATE_NOT_FROZEN",
        )
        for field in (
            "pooled_cross_treatment_aggregation",
            "success_rate_or_percentage",
            "inferential_statistics",
            "treatment_superiority",
            "causal_interpretation",
            "cryptographic_security_or_pcs",
            "publication_evidence",
        ):
            self.assertEqual(boundary[field], "NOT_PERMITTED")

    def test_no_result_or_aggregate_fields_are_emitted(self) -> None:
        serialized = json.dumps(self.payload, sort_keys=True)
        for forbidden_key in (
            '"projected_metrics"',
            '"raw_metrics"',
            '"outcome_counts"',
            '"success_count"',
            '"success_rate"',
            '"p_value"',
            '"confidence_interval"',
            '"effect_size"',
            '"ranking"',
        ):
            self.assertNotIn(forbidden_key, serialized)
        self.assertTrue(
            all(
                member["projected_metric_values_read"] is False
                for member in self.payload["member_registry"]
            )
        )

    def test_json_csv_and_manifest_outputs_verify(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            json_path = root / "phase-15-family-descriptive-plan-candidate.json"
            member_csv = root / "phase-15-family-member-registry.csv"
            unit_csv = root / "phase-15-family-analysis-units.csv"
            family_csv = root / "phase-15-family-observation-plans.csv"
            manifest = root / "phase-15-family-descriptive-plan.sha256"
            write_family_descriptive_plan(
                self.payload,
                json_path,
                member_csv,
                unit_csv,
                family_csv,
                manifest,
            )
            verify_family_descriptive_manifest(root, manifest)
            with member_csv.open("r", encoding="utf-8", newline="") as handle:
                members = list(csv.DictReader(handle))
            with unit_csv.open("r", encoding="utf-8", newline="") as handle:
                units = list(csv.DictReader(handle))
            with family_csv.open("r", encoding="utf-8", newline="") as handle:
                families = list(csv.DictReader(handle))
            self.assertEqual(len(members), 13)
            self.assertEqual(len(units), 12)
            self.assertEqual(len(families), 4)
            self.assertNotIn("outcome", members[0])
            self.assertNotIn("projected_metrics_json", members[0])

    def test_manifest_detects_tampering_and_incomplete_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            json_path = root / "phase-15-family-descriptive-plan-candidate.json"
            member_csv = root / "phase-15-family-member-registry.csv"
            unit_csv = root / "phase-15-family-analysis-units.csv"
            family_csv = root / "phase-15-family-observation-plans.csv"
            manifest = root / "phase-15-family-descriptive-plan.sha256"
            write_family_descriptive_plan(
                self.payload,
                json_path,
                member_csv,
                unit_csv,
                family_csv,
                manifest,
            )
            member_csv.write_text("tampered\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "D4 checksum mismatch"):
                verify_family_descriptive_manifest(root, manifest)

            write_family_descriptive_plan(
                self.payload,
                json_path,
                member_csv,
                unit_csv,
                family_csv,
                manifest,
            )
            lines = manifest.read_text(encoding="utf-8").splitlines()
            manifest.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "coverage mismatch"):
                verify_family_descriptive_manifest(root, manifest)


if __name__ == "__main__":
    unittest.main()
