import hashlib
import json
import unittest
from pathlib import Path

from ttc_recovery import fault_metrics as fm


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "experiments" / "configs" / "paper-final-experiment.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PaperFinalExperimentPreRunTests(unittest.TestCase):
    def test_predeclared_final_experiment_contract(self):
        payload = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], "PREDECLARED_PRE_RUN_NOT_EXECUTED")
        self.assertFalse(payload["outcomes_read_during_plan_generation"])

        for rel, expected in payload["protected_inputs_sha256"].items():
            self.assertEqual(sha256_file(ROOT / rel), expected, rel)

        expected_cells = {
            (kind.value, phase.value)
            for kind, valid_phases in fm._VALID_PHASES.items()
            for phase in valid_phases
        }
        declared_cells = {
            (row["fault_kind"], row["phase"])
            for row in payload["fault_phase_applicability"]
        }
        self.assertEqual(declared_cells, expected_cells)
        self.assertEqual(len(expected_cells), 31)
        self.assertNotIn(("DUPLICATE", "TEST_COMMAND"), expected_cells)
        self.assertNotIn(("DUPLICATE", "STATUS_TELEMETRY"), expected_cells)

        study_b = payload["studies"]["study_b_deterministic_t1"]
        self.assertEqual(study_b["schedule_count"], 40)
        self.assertEqual(len(study_b["schedules"]), 40)
        for row in study_b["schedules"]:
            schedule = fm.schedule_from_dicts(row["actions"])
            self.assertEqual(fm.schedule_sha256(schedule), row["schedule_sha256"])

        study_c = payload["studies"]["study_c_mixed_fault_t1"]
        self.assertEqual(study_c["seeds"], list(range(10001, 10101)))
        self.assertEqual(study_c["schedule_count"], 100)
        self.assertEqual(len(study_c["schedules"]), 100)
        self.assertEqual(study_c["total_injected_actions"], 191)

        covered = set()
        total_actions = 0
        for row in study_c["schedules"]:
            schedule = fm.schedule_from_dicts(row["actions"])
            self.assertEqual(fm.schedule_sha256(schedule), row["schedule_sha256"])
            total_actions += len(schedule)
            covered.update((action.kind.value, action.phase.value) for action in schedule)
        self.assertEqual(total_actions, 191)
        self.assertEqual(covered, expected_cells)

        study_d = payload["studies"]["study_d_sensitivity_t1"]
        self.assertEqual(study_d["schedule_count"], 12)
        self.assertEqual(len(study_d["schedules"]), 12)
        self.assertEqual(study_d["max_transmissions_grid"], [2, 3, 4])
        self.assertEqual(study_d["candidate_lifetime_contacts_grid"], [2, 3, 4])
        self.assertEqual(study_d["execution_count"], 108)
        for row in study_d["schedules"]:
            schedule = fm.schedule_from_dicts(row["actions"])
            self.assertEqual(fm.schedule_sha256(schedule), row["schedule_sha256"])


if __name__ == "__main__":
    unittest.main()
