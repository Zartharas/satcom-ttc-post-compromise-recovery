import csv
import json
import tempfile
import unittest
from pathlib import Path

from ttc_recovery.fault_metrics import (
    ExperimentPhase,
    FaultAction,
    FaultKind,
    SeededExperimentConfig,
    generate_fault_schedule,
    run_seeded_experiment,
    schedule_from_dicts,
    schedule_sha256,
    serialize_schedule,
    write_results,
)


class SeededFaultMetricTests(unittest.TestCase):
    def config(self, **changes):
        values = {
            "seed": 7001,
            "ground_epoch": 2,
            "spacecraft_epoch": 1,
            "max_transmissions": 3,
            "candidate_lifetime_contacts": 3,
            "max_faults": 3,
            "compromise_active_keys": True,
        }
        values.update(changes)
        return SeededExperimentConfig(**values)

    def test_same_seed_generates_identical_serialized_schedule(self):
        first = generate_fault_schedule(self.config(seed=8119))
        second = generate_fault_schedule(self.config(seed=8119))
        self.assertEqual(serialize_schedule(first), serialize_schedule(second))
        self.assertEqual(schedule_sha256(first), schedule_sha256(second))

    def test_serialized_schedule_round_trip_preserves_digest(self):
        schedule = generate_fault_schedule(self.config(seed=8123, max_faults=5))
        rows = json.loads(serialize_schedule(schedule))
        restored = schedule_from_dicts(rows)
        self.assertEqual(serialize_schedule(schedule), serialize_schedule(restored))
        self.assertEqual(schedule_sha256(schedule), schedule_sha256(restored))

    def test_no_fault_recovery_reports_separate_security_and_availability(self):
        result = run_seeded_experiment(self.config(), schedule=[])
        metrics = result.metrics
        self.assertEqual(metrics.outcome, "SUCCESS")
        self.assertEqual(metrics.security_state, "SECURE_PROVISIONAL")
        self.assertEqual(metrics.availability_state, "AVAILABLE")
        self.assertTrue(metrics.command_accepted)
        self.assertTrue(metrics.telemetry_complete)
        self.assertFalse(metrics.active_key_compromised)
        self.assertEqual(metrics.total_transmissions, 6)

    def test_prepare_drop_budget_exhaustion_is_expired(self):
        schedule = [
            FaultAction(ExperimentPhase.PREPARE, attempt, FaultKind.DROP)
            for attempt in range(1, 4)
        ]
        result = run_seeded_experiment(self.config(), schedule=schedule)
        self.assertEqual(result.metrics.outcome, "EXPIRED")
        self.assertEqual(result.metrics.availability_state, "UNAVAILABLE")
        self.assertEqual(result.metrics.drop_count, 3)
        self.assertFalse(result.metrics.command_accepted)

    def test_contact_close_increases_duration_and_retry_overhead(self):
        schedule = [
            FaultAction(
                ExperimentPhase.PREPARE,
                1,
                FaultKind.CONTACT_CLOSE,
                contacts=1,
            )
        ]
        result = run_seeded_experiment(self.config(), schedule=schedule)
        self.assertEqual(result.metrics.outcome, "SUCCESS")
        self.assertEqual(result.metrics.recovery_duration_contacts, 2)
        self.assertEqual(result.metrics.divergent_contact_windows, 1)
        self.assertEqual(result.metrics.retry_overhead, 1)

    def test_delay_is_measured_in_contact_windows(self):
        schedule = [
            FaultAction(
                ExperimentPhase.COMMIT,
                1,
                FaultKind.DELAY,
                contacts=2,
            )
        ]
        result = run_seeded_experiment(self.config(), schedule=schedule)
        self.assertEqual(result.metrics.outcome, "SUCCESS")
        self.assertEqual(result.metrics.delay_count, 1)
        self.assertEqual(result.metrics.recovery_duration_contacts, 3)
        self.assertGreaterEqual(result.metrics.divergent_contact_windows, 2)

    def test_duplicate_commit_is_rejected_without_blocking_recovery(self):
        schedule = [
            FaultAction(ExperimentPhase.COMMIT, 1, FaultKind.DUPLICATE)
        ]
        result = run_seeded_experiment(self.config(), schedule=schedule)
        self.assertEqual(result.metrics.outcome, "SUCCESS")
        self.assertEqual(result.metrics.duplicate_count, 1)
        self.assertGreaterEqual(result.metrics.replay_rejection_count, 1)

    def test_reordered_response_is_rejected_then_normal_response_succeeds(self):
        schedule = [
            FaultAction(ExperimentPhase.RESPONSE, 1, FaultKind.REORDER)
        ]
        result = run_seeded_experiment(self.config(), schedule=schedule)
        self.assertEqual(result.metrics.outcome, "SUCCESS")
        self.assertEqual(result.metrics.reorder_count, 1)
        self.assertGreaterEqual(result.metrics.rejection_count, 1)

    def test_stale_counter_is_rejected_and_counted(self):
        schedule = [
            FaultAction(ExperimentPhase.PREPARE, 1, FaultKind.STALE_COUNTER)
        ]
        result = run_seeded_experiment(self.config(), schedule=schedule)
        self.assertEqual(result.metrics.outcome, "SUCCESS")
        self.assertGreaterEqual(result.metrics.stale_state_rejection_count, 1)

    def test_stale_commit_replay_is_rejected_and_counted(self):
        schedule = [
            FaultAction(ExperimentPhase.COMMIT, 1, FaultKind.STALE_REPLAY)
        ]
        result = run_seeded_experiment(self.config(), schedule=schedule)
        self.assertEqual(result.metrics.outcome, "SUCCESS")
        self.assertEqual(result.metrics.replay_count, 1)
        self.assertGreaterEqual(result.metrics.stale_state_rejection_count, 1)

    def test_spacecraft_restart_before_commit_prevents_activation(self):
        schedule = [
            FaultAction(
                ExperimentPhase.COMMIT,
                1,
                FaultKind.ENDPOINT_RESTART,
                target="spacecraft",
            )
        ]
        result = run_seeded_experiment(self.config(), schedule=schedule)
        self.assertEqual(result.metrics.outcome, "EXPIRED")
        self.assertEqual(result.metrics.restart_count, 1)
        self.assertEqual(result.metrics.availability_state, "UNAVAILABLE")

    def test_confirm_contact_closure_exhaustion_is_secure_degraded(self):
        schedule = [
            FaultAction(
                ExperimentPhase.CONFIRM,
                attempt,
                FaultKind.CONTACT_CLOSE,
            )
            for attempt in range(1, 4)
        ]
        result = run_seeded_experiment(self.config(), schedule=schedule)
        self.assertEqual(result.metrics.outcome, "SECURE_DEGRADED")
        self.assertEqual(result.metrics.alignment, "S_AHEAD")
        self.assertEqual(result.metrics.availability_state, "DEGRADED")

    def test_status_loss_is_indeterminate_not_diverged(self):
        schedule = [
            FaultAction(ExperimentPhase.STATUS_TELEMETRY, 1, FaultKind.DROP)
        ]
        result = run_seeded_experiment(self.config(), schedule=schedule)
        self.assertEqual(result.metrics.outcome, "INDETERMINATE")
        self.assertTrue(result.metrics.alignment.startswith("SYNC"))
        self.assertEqual(result.metrics.availability_state, "DEGRADED")
        self.assertFalse(result.metrics.telemetry_complete)

    def test_json_and_csv_outputs_are_analysis_ready(self):
        results = [
            run_seeded_experiment(self.config(seed=9001), schedule=[]),
            run_seeded_experiment(
                self.config(seed=9002),
                schedule=[
                    FaultAction(
                        ExperimentPhase.TEST_COMMAND,
                        1,
                        FaultKind.DROP,
                    )
                ],
            ),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "results.json"
            csv_path = root / "metrics.csv"
            write_results(results, json_path, csv_path)

            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["result_count"], 2)
            self.assertEqual(
                payload["status"], "PROVISIONAL_INTERNAL_REVIEW_ONLY"
            )

            with csv_path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 2)
            self.assertIn("security_state", rows[0])
            self.assertIn("availability_state", rows[0])
            self.assertIn("schedule_sha256", rows[0])


if __name__ == "__main__":
    unittest.main()
