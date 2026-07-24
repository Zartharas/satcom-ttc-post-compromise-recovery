import unittest

from ttc_recovery.simulator import (
    B1ActivationPolicy,
    B2CompromiseScope,
    Outcome,
    Simulation,
    b0_otar,
    b1_triple_kem,
    b2_urke_strict,
    replay_b2_update,
    restore_ground_snapshot,
)


class BaselineSemanticTests(unittest.TestCase):
    def run_case(self, label, action):
        sim = Simulation(label)
        sim.schedule(0, label, lambda: action(sim))
        sim.run()
        return sim

    def test_b0_normal(self):
        sim = self.run_case("b0-normal", lambda s: b0_otar(s))
        self.assertEqual(sim.joint_state(), "SYNC(1)")
        self.assertEqual(sim.evaluate(), Outcome.SUCCESS)

    def test_b0_master_compromise(self):
        sim = self.run_case("b0-compromised", lambda s: b0_otar(s, master_compromised=True))
        self.assertEqual(sim.evaluate(), Outcome.AVAILABLE_UNSAFE)

    def test_b0_drop(self):
        sim = self.run_case("b0-drop", lambda s: b0_otar(s, drop_upload=True))
        self.assertEqual(sim.joint_state(), "SYNC(0)")

    def test_b1_normal_local_completion_activation(self):
        sim = self.run_case("b1-normal", lambda s: b1_triple_kem(s))
        self.assertEqual(sim.joint_state(), "SYNC(1)")
        self.assertEqual(sim.ground.crypto_complete_epoch, 1)
        self.assertEqual(sim.spacecraft.crypto_complete_epoch, 1)
        self.assertEqual(sim.evaluate(), Outcome.SUCCESS)

    def test_b1_confirm_loss_local_completion_diverges(self):
        sim = self.run_case("b1-confirm-loss", lambda s: b1_triple_kem(s, drop_confirm=True))
        self.assertEqual(sim.alignment_state(), "G_AHEAD")
        self.assertEqual(sim.ground.crypto_complete_epoch, 1)
        self.assertIsNone(sim.spacecraft.crypto_complete_epoch)
        self.assertTrue(sim.completion_ambiguous)
        self.assertEqual(sim.evaluate(), Outcome.DIVERGED)

    def test_b1_status_gated_activation_normal(self):
        sim = self.run_case(
            "b1-status-normal",
            lambda s: b1_triple_kem(
                s,
                activation_policy=B1ActivationPolicy.DEFER_UNTIL_AUTHENTICATED_STATUS,
            ),
        )
        self.assertEqual(sim.alignment_state(), "SYNC(1)")
        self.assertEqual(sim.evaluate(), Outcome.SUCCESS)

    def test_b1_status_gated_confirm_loss_expires_without_activation(self):
        sim = self.run_case(
            "b1-status-confirm-loss",
            lambda s: b1_triple_kem(
                s,
                drop_confirm=True,
                activation_policy=B1ActivationPolicy.DEFER_UNTIL_AUTHENTICATED_STATUS,
            ),
        )
        self.assertEqual(sim.alignment_state(), "SYNC(0)")
        self.assertEqual(sim.evaluate(), Outcome.EXPIRED)

    def test_b1_status_gated_status_loss_diverges(self):
        sim = self.run_case(
            "b1-status-loss",
            lambda s: b1_triple_kem(
                s,
                activation_policy=B1ActivationPolicy.DEFER_UNTIL_AUTHENTICATED_STATUS,
                drop_status=True,
            ),
        )
        self.assertEqual(sim.alignment_state(), "S_AHEAD")
        self.assertEqual(sim.evaluate(), Outcome.DIVERGED)

    def test_b1_reorder_aborts(self):
        sim = self.run_case("b1-reorder", lambda s: b1_triple_kem(s, out_of_order=True))
        self.assertEqual(sim.alignment_state(), "SYNC(0)")
        self.assertEqual(sim.evaluate(), Outcome.EXPIRED)

    def test_b2_normal(self):
        sim = self.run_case("b2-normal", lambda s: b2_urke_strict(s))
        self.assertEqual(sim.joint_state(), "SYNC(1)")
        self.assertEqual(sim.evaluate(), Outcome.SUCCESS)

    def test_b2_fresh_update_replaces_exposed_traffic_key(self):
        sim = self.run_case(
            "b2-traffic-key-exposure",
            lambda s: b2_urke_strict(s, compromise_scope=B2CompromiseScope.TRAFFIC_KEY),
        )
        self.assertIn("K0", sim.ground.attacker_known_keys)
        self.assertNotIn("R1", sim.ground.attacker_known_keys)
        self.assertEqual(sim.evaluate(), Outcome.SUCCESS)

    def test_b2_sender_state_exposure_passive_interval_recovers(self):
        sim = self.run_case(
            "b2-sender-state-passive",
            lambda s: b2_urke_strict(s, compromise_scope=B2CompromiseScope.SENDER_STATE),
        )
        self.assertTrue(sim.ground.state_exposed)
        self.assertNotIn("R1", sim.ground.attacker_known_keys)
        self.assertEqual(sim.evaluate(), Outcome.SUCCESS)

    def test_b2_receiver_state_exposure_traces_future_key(self):
        sim = self.run_case(
            "b2-receiver-state",
            lambda s: b2_urke_strict(s, compromise_scope=B2CompromiseScope.RECEIVER_STATE),
        )
        self.assertTrue(sim.spacecraft.state_exposed)
        self.assertIn("R1", sim.ground.attacker_known_keys)
        self.assertIn("R1", sim.spacecraft.attacker_known_keys)
        self.assertEqual(sim.evaluate(), Outcome.AVAILABLE_UNSAFE)

    def test_b2_both_endpoint_states_exposed_remains_unsafe(self):
        sim = self.run_case(
            "b2-both-states",
            lambda s: b2_urke_strict(s, compromise_scope=B2CompromiseScope.BOTH_ENDPOINT_STATES),
        )
        self.assertTrue(sim.ground.state_exposed)
        self.assertTrue(sim.spacecraft.state_exposed)
        self.assertIn("R1", sim.spacecraft.attacker_known_keys)
        self.assertEqual(sim.evaluate(), Outcome.AVAILABLE_UNSAFE)

    def test_b2_sender_state_active_impersonation_locks(self):
        sim = self.run_case(
            "b2-sender-impersonation",
            lambda s: b2_urke_strict(
                s,
                compromise_scope=B2CompromiseScope.SENDER_STATE,
                active_sender_impersonation=True,
            ),
        )
        self.assertTrue(sim.attacker_impersonated_sender)
        self.assertEqual(sim.alignment_state(), "S_AHEAD")
        self.assertIn("A1", sim.spacecraft.attacker_known_keys)
        self.assertEqual(sim.evaluate(), Outcome.LOCKED)

    def test_b2_dropped_update_locks_after_sender_evolution(self):
        sim = self.run_case("b2-update-loss", lambda s: b2_urke_strict(s, drop_update=True))
        self.assertEqual(sim.alignment_state(), "G_AHEAD")
        self.assertEqual(sim.joint_state(), "LOCKED")
        self.assertEqual(sim.evaluate(), Outcome.LOCKED)

    def test_b2_lost_status_is_not_cryptographic_divergence(self):
        sim = self.run_case("b2-status-loss", lambda s: b2_urke_strict(s, lose_status=True))
        self.assertEqual(sim.alignment_state(), "SYNC(1)")
        self.assertEqual(sim.evaluate(), Outcome.INDETERMINATE)

    def test_b2_stale_ground_restore_locks(self):
        sim = self.run_case("b2-stale-restore", lambda s: b2_urke_strict(s))
        restore_ground_snapshot(sim, 0, "K0")
        sim.check_invariants()
        self.assertEqual(sim.alignment_state(), "S_AHEAD")
        self.assertEqual(sim.joint_state(), "LOCKED")
        self.assertEqual(sim.evaluate(), Outcome.LOCKED)

    def test_b2_replay_is_rejected_without_state_change(self):
        sim = self.run_case("b2-replay", lambda s: b2_urke_strict(s))
        accepted = replay_b2_update(sim, target_epoch=1, message_id="update-1")
        self.assertFalse(accepted)
        self.assertEqual(sim.alignment_state(), "SYNC(1)")
        self.assertEqual(sim.evaluate(), Outcome.SUCCESS)


if __name__ == "__main__":
    unittest.main()
