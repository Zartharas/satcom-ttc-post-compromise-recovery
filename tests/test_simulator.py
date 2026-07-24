import unittest
from ttc_recovery.simulator import Simulation, Outcome, b0_otar, b1_triple_kem, b2_strict_rke


class BaselineSkeletonTests(unittest.TestCase):
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

    def test_b1_normal(self):
        sim = self.run_case("b1-normal", lambda s: b1_triple_kem(s))
        self.assertEqual(sim.joint_state(), "SYNC(1)")

    def test_b1_confirm_loss(self):
        sim = self.run_case("b1-confirm-loss", lambda s: b1_triple_kem(s, drop_confirm=True))
        self.assertEqual(sim.joint_state(), "G_AHEAD")
        self.assertEqual(sim.evaluate(), Outcome.DIVERGED)

    def test_b1_reorder(self):
        sim = self.run_case("b1-reorder", lambda s: b1_triple_kem(s, out_of_order=True))
        self.assertEqual(sim.ground.epoch, 0)
        self.assertEqual(sim.spacecraft.epoch, 0)

    def test_b2_normal(self):
        sim = self.run_case("b2-normal", lambda s: b2_strict_rke(s))
        self.assertEqual(sim.joint_state(), "SYNC(1)")

    def test_b2_ack_loss(self):
        sim = self.run_case("b2-ack-loss", lambda s: b2_strict_rke(s, drop_ack=True))
        self.assertEqual(sim.evaluate(), Outcome.LOCKED)


if __name__ == "__main__":
    unittest.main()
