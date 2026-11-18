"""Fail-closed F1 lock tests only. No external runtime or experiment input."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_nos3_source_lock import validate_lock, extract_function


class SourceLockContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lock = json.loads(
            Path(__file__).with_name("NOS3_SOURCE_LOCK_AND_SECURITY_HOLD_2026-11-17.json")
            .read_text(encoding="utf-8")
        )

    def test_valid_prospective_lock(self):
        validate_lock(self.lock)

    def test_rejects_modified_gitlink(self):
        data = copy.deepcopy(self.lock)
        for x in data["upstream"]["nos3"]["gitlinks"]:
            if x["path"] == "components/cryptolib":
                x["sha"] = "0" * 40
                break
        with self.assertRaises(ValueError):
            validate_lock(data)

    def test_rejects_premature_runtime_pass(self):
        data = copy.deepcopy(self.lock)
        data["readiness"]["F2_real_integrated_restart"] = "PASS"
        with self.assertRaises(ValueError):
            validate_lock(data)

    def test_rejects_removed_security_hold(self):
        data = copy.deepcopy(self.lock)
        data["security_review"][0]["disposition"] = "PASS"
        with self.assertRaises(ValueError):
            validate_lock(data)

    def test_rejects_unfrozen_study_relabel(self):
        data = copy.deepcopy(self.lock)
        data["science_protocol_state"] = "FROZEN"
        with self.assertRaises(ValueError):
            validate_lock(data)

    def test_source_function_body_extraction(self):
        source = "static int32_t f(void);\nstatic int32_t f(void)\n{\nreturn 1;\n}\n"
        self.assertIn("return 1;", extract_function(source, "f"))


if __name__ == "__main__":
    unittest.main()
