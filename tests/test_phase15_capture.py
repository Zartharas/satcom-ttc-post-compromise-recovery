from __future__ import annotations

import importlib.util
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


if __name__ == "__main__":
    unittest.main()
