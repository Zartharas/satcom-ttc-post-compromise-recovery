import unittest
from dataclasses import replace

from ttc_recovery.simulator import Outcome
from ttc_recovery.t1_controller import (
    T1Endpoint,
    T1Session,
    run_bounded_recovery,
)


class ProvisionalT1Tests(unittest.TestCase):
    def test_normal_ground_ahead_recovery_succeeds(self):
        session = run_bounded_recovery(ground_epoch=2, spacecraft_epoch=1)
        self.assertEqual(session.alignment_state(), "SYNC(3)")
        self.assertEqual(session.outcome(), Outcome.SUCCESS)
        self.assertTrue(session.verification_complete)

    def test_spacecraft_ahead_selects_epoch_above_spacecraft_without_oracle(self):
        session = run_bounded_recovery(ground_epoch=0, spacecraft_epoch=3)
        self.assertEqual(session.alignment_state(), "SYNC(4)")
        self.assertEqual(session.outcome(), Outcome.SUCCESS)

    def test_prepare_loss_is_retried_within_bound(self):
        session = run_bounded_recovery(
            ground_epoch=1,
            spacecraft_epoch=0,
            drop_prepare_attempts=1,
        )
        self.assertEqual(session.outcome(), Outcome.SUCCESS)
        self.assertTrue(any(e["event"] == "t1_prepare_retried" for e in session.event_log))

    def test_response_loss_uses_idempotent_prepare_retry(self):
        session = run_bounded_recovery(
            ground_epoch=1,
            spacecraft_epoch=0,
            drop_response_attempts=1,
        )
        self.assertEqual(session.outcome(), Outcome.SUCCESS)
        self.assertTrue(
            any(e["event"] == "t1_prepare_retry_accepted" for e in session.event_log)
        )

    def test_commit_loss_is_retried_before_spacecraft_activation(self):
        session = run_bounded_recovery(
            ground_epoch=1,
            spacecraft_epoch=0,
            drop_commit_attempts=1,
        )
        self.assertEqual(session.outcome(), Outcome.SUCCESS)
        self.assertTrue(any(e["event"] == "t1_commit_retried" for e in session.event_log))

    def test_confirm_loss_uses_activation_receipt_for_idempotent_retry(self):
        session = run_bounded_recovery(
            ground_epoch=1,
            spacecraft_epoch=0,
            drop_confirm_attempts=1,
        )
        self.assertEqual(session.outcome(), Outcome.SUCCESS)
        self.assertTrue(
            any(e["event"] == "t1_commit_retry_confirmed" for e in session.event_log)
        )

    def test_confirmation_budget_exhaustion_is_secure_degraded_not_locked(self):
        session = run_bounded_recovery(
            ground_epoch=1,
            spacecraft_epoch=0,
            max_transmissions=2,
            drop_confirm_attempts=2,
        )
        self.assertEqual(session.alignment_state(), "S_AHEAD")
        self.assertEqual(session.outcome(), Outcome.SECURE_DEGRADED)
        self.assertIsNone(session.lockout_reason)

    def test_prepare_budget_exhaustion_expires_without_activation(self):
        session = run_bounded_recovery(
            ground_epoch=1,
            spacecraft_epoch=0,
            max_transmissions=2,
            drop_prepare_attempts=2,
        )
        self.assertEqual(session.ground.epoch, 1)
        self.assertEqual(session.spacecraft.epoch, 0)
        self.assertEqual(session.outcome(), Outcome.EXPIRED)

    def test_status_loss_is_indeterminate_after_convergence(self):
        session = run_bounded_recovery(
            ground_epoch=1,
            spacecraft_epoch=0,
            drop_status=True,
        )
        self.assertEqual(session.alignment_state(), "SYNC(2)")
        self.assertEqual(session.outcome(), Outcome.INDETERMINATE)

    def test_candidate_cannot_authorize_before_activation(self):
        session = T1Session(
            ground=T1Endpoint("ground", epoch=1, active_key="G1"),
            spacecraft=T1Endpoint("spacecraft", epoch=0, active_key="S0"),
        )
        prepare = session.start_recovery("r-candidate")
        response = session.spacecraft_accept_prepare(prepare)
        self.assertIsNotNone(response)
        commit = session.ground_accept_response(response)
        self.assertIsNotNone(commit)
        candidate = session.ground.pending.candidate_key_ref
        self.assertFalse(session.candidate_can_authorize(session.ground, candidate))
        self.assertTrue(
            session.candidate_can_authorize(session.ground, session.ground.active_key)
        )

    def test_unauthorized_prepare_is_rejected_without_spacecraft_state_change(self):
        session = T1Session(
            ground=T1Endpoint("ground", epoch=1, active_key="G1"),
            spacecraft=T1Endpoint("spacecraft", epoch=0, active_key="S0"),
        )
        prepare = session.start_recovery("r-unauthorized")
        forged = replace(
            prepare,
            message_id="forged-prepare",
            authorized_by="unauthorized-authority",
        )
        response = session.spacecraft_accept_prepare(forged)
        self.assertIsNone(response)
        self.assertEqual(session.spacecraft.epoch, 0)
        self.assertIsNone(session.spacecraft.pending)

    def test_pending_capacity_rejects_conflicting_recovery(self):
        session = T1Session(
            ground=T1Endpoint("ground", epoch=1, active_key="G1"),
            spacecraft=T1Endpoint("spacecraft", epoch=0, active_key="S0"),
        )
        prepare = session.start_recovery("r-one")
        response = session.spacecraft_accept_prepare(prepare)
        self.assertIsNotNone(response)
        conflicting = replace(
            prepare,
            message_id="prepare-r-two",
            recovery_id="r-two",
            counter=prepare.counter + 1,
            transcript_ref="transcript:r-two",
        )
        self.assertIsNone(session.spacecraft_accept_prepare(conflicting))
        self.assertEqual(session.spacecraft.pending.recovery_id, "r-one")

    def test_replayed_commit_after_success_is_rejected_without_state_change(self):
        session = run_bounded_recovery(ground_epoch=1, spacecraft_epoch=0)
        replay = session.last_commit
        before = (session.spacecraft.epoch, session.spacecraft.active_key)
        self.assertIsNone(session.spacecraft_accept_commit(replay))
        self.assertEqual(before, (session.spacecraft.epoch, session.spacecraft.active_key))
        self.assertEqual(session.outcome(), Outcome.SUCCESS)

    def test_conflicting_commit_is_rejected(self):
        session = T1Session(
            ground=T1Endpoint("ground", epoch=1, active_key="G1"),
            spacecraft=T1Endpoint("spacecraft", epoch=0, active_key="S0"),
        )
        prepare = session.start_recovery("r-conflict")
        response = session.spacecraft_accept_prepare(prepare)
        commit = session.ground_accept_response(response)
        conflicting = replace(
            commit,
            message_id="conflicting-commit",
            candidate_key_ref="T1:other:99",
        )
        self.assertIsNone(session.spacecraft_accept_commit(conflicting))
        self.assertEqual(session.spacecraft.epoch, 0)
        self.assertIsNotNone(session.spacecraft.pending)

    def test_compromised_operational_keys_are_replaced(self):
        session = run_bounded_recovery(
            ground_epoch=1,
            spacecraft_epoch=1,
            compromise_active_keys=True,
        )
        self.assertEqual(session.outcome(), Outcome.SUCCESS)
        self.assertNotIn(session.ground.active_key, session.ground.compromised_keys)
        self.assertNotIn(session.spacecraft.active_key, session.spacecraft.compromised_keys)


if __name__ == "__main__":
    unittest.main()
