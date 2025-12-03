import unittest
from simulation import SimulationConfig, BilboGollumSimulation

class TestBilboGollumSimulation(unittest.TestCase):
    def setUp(self):
        self.config = SimulationConfig()
        self.sim = BilboGollumSimulation(self.config)

    def test_config_defaults(self):
        self.assertEqual(self.config.theta, 0.6)
        self.assertEqual(self.config.p_solve_fair_riddle, 0.7)

    def test_simulate_once_keys(self):
        result = self.sim.simulate_once("A")
        self.assertIn("survive", result)
        self.assertIn("collapse", result)
        self.assertIsInstance(result["survive"], bool)
        self.assertIsInstance(result["collapse"], bool)

    def test_run_monte_carlo_range(self):
        survival, collapse = self.sim.run_monte_carlo("F", n_runs=100)
        self.assertTrue(0 <= survival <= 1)
        self.assertTrue(0 <= collapse <= 1)

    def test_bilbo_decision_fair(self):
        decision = self.sim.bilbo_decision("Treacherous", "F")
        self.assertEqual(decision, "C")

    def test_bilbo_decision_defect(self):
        decision = self.sim.bilbo_decision("Fair", "D")
        self.assertEqual(decision, "D")

    def test_adaptive_logic(self):
        # Force parameters where Defect is clearly better
        self.config.p_solve_fair_riddle = 0.0 # Fail riddle always
        self.config.p_gollum_snap = 1.0       # Gollum snaps always if fair
        # Cooperate survival = 0
        
        self.config.survival_if_defect = 1.0
        self.config.survival_if_no_defect = 1.0
        # Defect survival = 1.0
        
        decision = self.sim.bilbo_decision("Fair", "A")
        self.assertEqual(decision, "D")

if __name__ == '__main__':
    unittest.main()
