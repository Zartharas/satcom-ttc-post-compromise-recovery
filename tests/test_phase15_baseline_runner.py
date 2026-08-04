from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT / "experiments" / "scripts" / "run_phase15_baseline_parity.py"
)
SPEC = importlib.util.spec_from_file_location("phase15_baseline_runner", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class Phase15BaselineRunnerTests(unittest.TestCase):
    def test_retained_catalog_is_preferred_beside_config(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config_path = root / "phase-15-baseline-parity.json"
            retained_catalog = root / "baseline-test-catalog.json"
            config_path.write_text("{}\n", encoding="utf-8")
            retained_catalog.write_text('{"tests": []}\n', encoding="utf-8")

            resolved = RUNNER.resolve_catalog_path(
                config_path,
                {"catalog": "tests/scenarios/baseline-test-catalog.json"},
                None,
            )
            self.assertEqual(resolved, retained_catalog.resolve())

    def test_explicit_catalog_has_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config_path = root / "phase-15-baseline-parity.json"
            retained_catalog = root / "baseline-test-catalog.json"
            explicit_catalog = root / "explicit-catalog.json"
            config_path.write_text("{}\n", encoding="utf-8")
            retained_catalog.write_text('{"tests": []}\n', encoding="utf-8")
            explicit_catalog.write_text('{"tests": []}\n', encoding="utf-8")

            resolved = RUNNER.resolve_catalog_path(
                config_path,
                {"catalog": "tests/scenarios/baseline-test-catalog.json"},
                explicit_catalog,
            )
            self.assertEqual(resolved, explicit_catalog.resolve())


if __name__ == "__main__":
    unittest.main()
