import unittest

from ttc_recovery.simulator import (
    B1ActivationPolicy,
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

    def test_b1_normal_bilateral_completion(self):
        sim = self.run_case("b1-normal", lambda s: b1_triple_kem(s))
        self.assertEqual(sim.joint_state(), "SYNC(1)")
        self.assertEqual(sim.ground.crypto_complete_epoch, 1)
        self.assertEqual(sim.spacecraft.crypto_complete_epoch, 1)
        self.assertEqual(sim.evaluate(), Outcome.SUCCESS)

    def test_b1_confirm_loss_expires_without_operational_divergence(self):
        sim = self.run_case("b1-confirm-loss", lambda s: b1_triple_kem(s, drop_confirm=True))
        self.assertEqual(sim.alignment_state(), "SYNC(0)")
        self.assertEqual(sim.ground.crypto_complete_epoch, 1)
        self.assertIsNone(sim.spacecraft.crypto_complete_epoch)
        self.assertTrue(sim.completion_ambiguous)
        self.assertEqual(sim.evaluate(), Outcome.EXPIRED)

    def test_b1_local_activation_policy_can_diverge(self):
        sim = self.run_case(
            "b1-local-activation",
            lambda s: b1_triple_kem(
                s,
                drop_confirm=True,
                activation_policy=B1ActivationPolicy.ACTIVATE_ON_LOCAL_COMPLETION,
            ),
        )
        self.assertEqual(sim.alignment_state(), "G_AHEAD")
        self.assertEqual(sim.evaluate(), Outcome.DIVERGED)

    def test_b1_reorder_aborts(self):
        sim = self.run_case("b1-reorder", lambda s: b1_triple_kem(s, out_of_order=True))
        self.assertEqual(sim.alignment_state(), "SYNC(0)")
        self.assertEqual(sim.evaluate(), Outcome.EXPIRED)

    def test_b2_normal(self):
        sim = self.run_case("b2-normal", lambda s: b2_urke_strict(s))
        self.assertEqual(sim.joint_state(), "SYNC(1)")
        self.assertEqual(sim.evaluate(), Outcome.SUCCESS)

    def test_b2_fresh_update_heals_current_key_exposure(self):
        sim = self.run_case(
            "b2-heal-current-exposure",
            lambda s: b2_urke_strict(s, compromise_current=True),
        )
        self.assertIn("K0", sim.ground.attacker_known_keys)
        self.assertNotIn("R1", sim.ground.attacker_known_keys)
        self.assertEqual(sim.evaluate(), Outcome.SUCCESS)

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
