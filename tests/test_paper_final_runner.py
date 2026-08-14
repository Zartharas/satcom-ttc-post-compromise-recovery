import hashlib
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "experiments" / "scripts" / "run_paper_final_experiment.py"
PLAN = ROOT / "experiments" / "configs" / "paper-final-experiment.json"


def load_runner():
    spec = importlib.util.spec_from_file_location("paper_final_runner", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PaperFinalRunnerContractTests(unittest.TestCase):
    def test_runner_is_bound_to_committed_outcome_blind_plan(self):
        module = load_runner()
        actual = hashlib.sha256(PLAN.read_bytes()).hexdigest()
        self.assertEqual(module.EXPECTED_PLAN_SHA256, actual)

        payload = module.validate_plan(PLAN)
        self.assertEqual(
            payload["status"],
            "PREDECLARED_PRE_RUN_NOT_EXECUTED",
        )
        self.assertFalse(payload["outcomes_read_during_plan_generation"])
        self.assertEqual(
            payload["studies"]["study_b_deterministic_t1"]["schedule_count"],
            40,
        )
        self.assertEqual(
            payload["studies"]["study_c_mixed_fault_t1"]["schedule_count"],
            100,
        )
        self.assertEqual(
            payload["studies"]["study_d_sensitivity_t1"]["execution_count"],
            108,
        )


if __name__ == "__main__":
    unittest.main()
