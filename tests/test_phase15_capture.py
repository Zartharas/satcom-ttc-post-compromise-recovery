from __future__ import annotations

import csv
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "scripts" / "run_phase15_pilot_capture.py"
SPEC = importlib.util.spec_from_file_location("phase15_capture", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
CAPTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CAPTURE)


def write_valid_matched_family_fixture(root: Path) -> None:
    families = ["CF-01", "CF-02", "CF-05", "CF-06"]
    rows = []
    for index in range(13):
        family = families[min(index // 4, 3)]
        rows.append(
            {
                "row_id": f"{family}:T{index:02d}:S{index:02d}",
                "family_classification": "QUALIFIED_MATCH",
                "source_execution_sha256": f"{index:064x}",
                "publication_evidence": False,
            }
        )
    denominators = [
        {
            "family_id": family,
            "family_coverage_status": "COMPLETE",
            "success_rate_denominator": "NOT_DEFINED",
            "aggregate_authorized": False,
            "publication_evidence": False,
        }
        for family in families
    ]
    payload = {
        "status": CAPTURE.MATCHED_FAMILY_STATUS,
        "run_class": "PILOT_INTERNAL_VALIDATION_ONLY",
        "publication_evidence": False,
        "eligible_family_ids": families,
        "family_count": 4,
        "member_row_count": 13,
        "analysis_unit_count": 12,
        "rows": rows,
        "denominators": denominators,
        "source_executions": [
            {"row_id": row["row_id"], "execution": {}} for row in rows
        ],
        "comparison_authorization": {
            "family_specific_descriptive_comparison": "NOT_YET_AUTHORIZED",
            "pooled_cross_treatment_aggregation": "NOT_PERMITTED",
            "success_rate_or_percentage": "NOT_PERMITTED",
            "inferential_statistics": "NOT_PERMITTED",
            "treatment_superiority": "NOT_PERMITTED",
            "publication_evidence": False,
        },
    }

    json_path = root / CAPTURE.MATCHED_FAMILY_JSON
    member_path = root / CAPTURE.MATCHED_FAMILY_MEMBER_CSV
    denominator_path = root / CAPTURE.MATCHED_FAMILY_DENOMINATOR_CSV
    manifest_path = root / CAPTURE.MATCHED_FAMILY_INTERNAL_MANIFEST

    json_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with member_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["row_id"])
        writer.writeheader()
        for row in rows:
            writer.writerow({"row_id": row["row_id"]})
    with denominator_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["family_id"])
        writer.writeheader()
        for row in denominators:
            writer.writerow({"family_id": row["family_id"]})

    CAPTURE.write_manifest(
        root,
        [json_path, member_path, denominator_path],
        manifest_path,
    )


class Phase15CaptureTests(unittest.TestCase):
    def test_run_id_is_utc_and_commit_pinned(self) -> None:
        timestamp = datetime(2026, 8, 4, 2, 15, 30, tzinfo=timezone.utc)
        self.assertEqual(
            CAPTURE.build_run_id(
                timestamp,
                "10148d0fadb970c59f31bf75d05880c1f460ffd9",
            ),
            "phase15-pilot-20260804T021530Z-g10148d0",
        )

    def test_unknown_commit_has_explicit_run_id_marker(self) -> None:
        timestamp = datetime(2026, 8, 4, 2, 15, 30, tzinfo=timezone.utc)
        self.assertEqual(
            CAPTURE.build_run_id(timestamp, "UNKNOWN"),
            "phase15-pilot-20260804T021530Z-gunknown",
        )

    def test_new_run_directory_cannot_be_reused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            CAPTURE.ensure_new_directory(run_dir)
            self.assertTrue(run_dir.is_dir())
            with self.assertRaises(FileExistsError):
                CAPTURE.ensure_new_directory(run_dir)

    def test_manifest_round_trip_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "raw" / "a.txt"
            second = root / "config" / "b.json"
            first.parent.mkdir(parents=True)
            second.parent.mkdir(parents=True)
            first.write_text("alpha\n", encoding="utf-8")
            second.write_text('{"value": 1}\n', encoding="utf-8")
            manifest = root / "manifests" / "raw.sha256"

            CAPTURE.write_manifest(root, [first, second], manifest)
            CAPTURE.verify_manifest(root, manifest)

            lines = manifest.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertTrue(lines[0].endswith("  config/b.json"))
            self.assertTrue(lines[1].endswith("  raw/a.txt"))

    def test_manifest_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            payload = root / "raw.json"
            payload.write_text("before\n", encoding="utf-8")
            manifest = root / "manifest.sha256"
            CAPTURE.write_manifest(root, [payload], manifest)
            payload.write_text("after\n", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "Checksum mismatch"):
                CAPTURE.verify_manifest(root, manifest)

    def test_matched_family_output_validation_accepts_complete_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_valid_matched_family_fixture(root)
            payload = CAPTURE.validate_matched_family_outputs(root)
            self.assertEqual(payload["family_count"], 4)
            self.assertEqual(payload["member_row_count"], 13)
            self.assertEqual(payload["analysis_unit_count"], 12)

    def test_matched_family_output_validation_rejects_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_valid_matched_family_fixture(root)
            (root / CAPTURE.MATCHED_FAMILY_DENOMINATOR_CSV).unlink()
            with self.assertRaisesRegex(RuntimeError, "output is incomplete"):
                CAPTURE.validate_matched_family_outputs(root)

    def test_matched_family_output_validation_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_valid_matched_family_fixture(root)
            member_path = root / CAPTURE.MATCHED_FAMILY_MEMBER_CSV
            member_path.write_text("row_id\ntampered\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "Checksum mismatch"):
                CAPTURE.validate_matched_family_outputs(root)

    def test_matched_family_output_validation_rejects_relaxed_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_valid_matched_family_fixture(root)
            json_path = root / CAPTURE.MATCHED_FAMILY_JSON
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            payload["comparison_authorization"][
                "family_specific_descriptive_comparison"
            ] = "AUTHORIZED"
            json_path.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            CAPTURE.write_manifest(
                root,
                [
                    json_path,
                    root / CAPTURE.MATCHED_FAMILY_MEMBER_CSV,
                    root / CAPTURE.MATCHED_FAMILY_DENOMINATOR_CSV,
                ],
                root / CAPTURE.MATCHED_FAMILY_INTERNAL_MANIFEST,
            )
            with self.assertRaisesRegex(RuntimeError, "authorization boundary"):
                CAPTURE.validate_matched_family_outputs(root)

    def test_matched_family_internal_manifest_must_cover_all_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_valid_matched_family_fixture(root)
            CAPTURE.write_manifest(
                root,
                [
                    root / CAPTURE.MATCHED_FAMILY_JSON,
                    root / CAPTURE.MATCHED_FAMILY_MEMBER_CSV,
                ],
                root / CAPTURE.MATCHED_FAMILY_INTERNAL_MANIFEST,
            )
            with self.assertRaisesRegex(RuntimeError, "manifest coverage drifted"):
                CAPTURE.validate_matched_family_outputs(root)


if __name__ == "__main__":
    unittest.main()
