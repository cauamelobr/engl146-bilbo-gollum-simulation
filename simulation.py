import random
from dataclasses import dataclass
from typing import Dict, Tuple, Literal

@dataclass
class SimulationConfig:
    """Configuration parameters for the Bilbo-Gollum simulation."""
    theta: float = 0.6          # Bilbo's prior belief Gollum is treacherous
    phi: float = 0.5            # Probability Bilbo is desperate/adaptive
    p_solve_fair_riddle: float = 0.7  # Bilbo's fair-riddle skill
    p_gollum_snap: float = 0.3        # Chance a "fair" Gollum snaps under stress
    p_honor_if_fair: float = 0.9      # Gollum honors bargain if calm + fair
    survival_if_defect: float = 0.85      # Bilbo survival chance if he defects + Gollum attacks
    survival_if_no_defect: float = 0.90   # Bilbo survival if he defects but Gollum does not attack
    base_defect_prob_treacherous: float = 0.8
    base_defect_prob_fair: float = 0.6


class BilboGollumSimulation:
    """
    Engine for simulating the Bilbo-Gollum riddle game interactions.
    Encapsulates all game logic and probability calculations.
    """
    def __init__(self, config: SimulationConfig):
        self.config = config

    def sample_gollum_type(self) -> str:
        return "Treacherous" if random.random() < self.config.theta else "Fair"

    def sample_bilbo_type(self) -> str:
        return "Desperate" if random.random() < self.config.phi else "RuleBound"

    def expected_survival_if_cooperate(self, t_gollum: str) -> float:
        """Calculate expected survival utility for Cooperate action."""
        # If Bilbo solves the riddle → survives
        survival_if_solve = 1.0

        # If Bilbo fails
        if t_gollum == "Treacherous":
            survival_if_fail = 0.0
        else:
            # Gollum may still snap
            survival_if_fail = (1 - self.config.p_gollum_snap) * 1.0 + self.config.p_gollum_snap * 0.0

        return (
            self.config.p_solve_fair_riddle * survival_if_solve +
            (1 - self.config.p_solve_fair_riddle) * survival_if_fail
        )

    def expected_survival_if_defect(self, t_gollum: str) -> float:
        """Calculate expected survival utility for Defect action."""
        # Determine Gollum’s likelihood to defect
        if t_gollum == "Treacherous":
            base_defect = self.config.base_defect_prob_treacherous
        else:
            base_defect = self.config.base_defect_prob_fair

        return (
            base_defect * self.config.survival_if_defect +
            (1 - base_defect) * self.config.survival_if_no_defect
        )

    def bilbo_decision(self, t_gollum: str, strategy: str) -> str:
        """
        Determine Bilbo's action based on strategy and Gollum's type.
        Strategies:
        F = always fair (Cooperate)
        D = always defect (Defect)
        A = adaptive (choose higher expected survival)
        """
        if strategy == "F":
            return "C"
        if strategy == "D":
            return "D"

        # Adaptive strategy
        eu_c = self.expected_survival_if_cooperate(t_gollum)
        eu_d = self.expected_survival_if_defect(t_gollum)
        return "D" if eu_d > eu_c else "C"

    def simulate_once(self, strategy: str) -> Dict[str, bool]:
        """Run a single simulation round."""
        t_g = self.sample_gollum_type()
        # t_b is sampled but not strictly used in decision logic in original code, 
        # but kept for completeness if needed for future extensions.
        _ = self.sample_bilbo_type() 
        
        action_b = self.bilbo_decision(t_g, strategy)

        # --- Bilbo cooperates (fair riddle) ---
        if action_b == "C":
            if random.random() < self.config.p_solve_fair_riddle:
                return {"survive": True, "collapse": False}

            # Bilbo fails
            if t_g == "Treacherous":
                return {"survive": False, "collapse": True}
            else:
                if random.random() < self.config.p_gollum_snap:
                    return {"survive": False, "collapse": True}
                else: 
                    return {"survive": True, "collapse": False}

        # --- Bilbo defects ("pocket") ---
        else:
            if t_g == "Treacherous":
                base_defect = self.config.base_defect_prob_treacherous
            else:
                base_defect = self.config.base_defect_prob_fair

            gollum_defects_now = random.random() < base_defect

            if gollum_defects_now:
                survives = random.random() < self.config.survival_if_defect
                return {"survive": survives, "collapse": True}
            else:
                survives = random.random() < self.config.survival_if_no_defect
                return {"survive": survives, "collapse": False}

    def run_monte_carlo(self, strategy: str, n_runs: int) -> Tuple[float, float]:
        """
        Run Monte Carlo simulation for a given strategy.
        Returns (survival_rate, collapse_rate).
        """
        survived_count = 0
        collapsed_count = 0
        
        for _ in range(n_runs):
            out = self.simulate_once(strategy)
            if out["survive"]:
                survived_count += 1
            if out["collapse"]:
                collapsed_count += 1
                
        return survived_count / n_runs, collapsed_count / n_runs
