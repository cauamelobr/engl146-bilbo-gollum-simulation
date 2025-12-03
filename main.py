import numpy as np
import pandas as pd
from simulation import SimulationConfig, BilboGollumSimulation
from visualization import plot_sensitivity_heatmap, plot_outcome_distribution

def run_sensitivity_analysis():
    """
    Runs sensitivity analysis for the Adaptive strategy over a grid of 
    theta (belief Gollum is treacherous) and p_solve (riddle skill).
    """
    theta_values = np.linspace(0.1, 0.9, 9)
    solve_values = np.linspace(0.4, 0.9, 10)
    
    heat_data = np.zeros((len(theta_values), len(solve_values)))
    
    # Base configuration
    config = SimulationConfig()
    
    print("Running sensitivity analysis...")
    for i, th in enumerate(theta_values):
        for j, sol in enumerate(solve_values):
            # Update config for this grid point
            config.theta = th
            config.p_solve_fair_riddle = sol
            
            sim = BilboGollumSimulation(config)
            survival, _ = sim.run_monte_carlo("A", n_runs=6000)
            heat_data[i][j] = survival
            
    plot_sensitivity_heatmap(heat_data, solve_values, theta_values)

def run_outcome_distributions():
    """
    Generates outcome distribution plots for all strategies.
    """
    config = SimulationConfig()
    sim = BilboGollumSimulation(config)
    
    strategies = ["A", "F", "D"]
    for strat in strategies:
        print(f"Simulating outcome distribution for strategy: {strat}")
        outcomes = []
        for _ in range(5000):
            out = sim.simulate_once(strat)
            outcomes.append(1 if out["collapse"] else 0)
        plot_outcome_distribution(outcomes, strat)

def main():
    # 1. Standard Monte Carlo Run
    print("Running standard Monte Carlo simulation...")
    config = SimulationConfig()
    sim = BilboGollumSimulation(config)
    
    strategies = ["F", "D", "A"]
    summary = []
    
    for strat in strategies:
        s, c = sim.run_monte_carlo(strat, n_runs=100_000)
        summary.append({
            "Strategy": strat,
            "Survival Probability": round(s, 4),
            "Collapse Probability": round(c, 4)
        })

    df = pd.DataFrame(summary)
    print("\nSimulation Results:")
    print(df)
    print("\n" + "-"*30 + "\n")

    # 2. Visualizations
    run_sensitivity_analysis()
    run_outcome_distributions()

if __name__ == "__main__":
    main()
