import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Optional

def plot_sensitivity_heatmap(
    data: np.ndarray, 
    x_labels: np.ndarray, 
    y_labels: np.ndarray,
    x_label_name: str = "Bilbo's Riddle Skill (p_solve)",
    y_label_name: str = "Belief Gollum is Treacherous (theta)",
    title: str = "Adaptive Strategy Survival Heatmap"
):
    """
    Generates and displays a heatmap of survival probabilities.
    """
    plt.figure(figsize=(9, 6))
    sns.heatmap(
        data,
        xticklabels=np.round(x_labels, 2),
        yticklabels=np.round(y_labels, 2),
        cmap="YlGnBu",
        cbar_kws={'label': 'Survival Probability'}
    )
    plt.xlabel(x_label_name)
    plt.ylabel(y_label_name)
    plt.title(title)
    plt.tight_layout()
    plt.show()

def plot_outcome_distribution(outcomes: List[int], strategy: str):
    """
    Generates and displays a histogram of collapse outcomes.
    0 = No Collapse, 1 = Collapse
    """
    plt.figure(figsize=(6, 4))
    plt.hist(outcomes, bins=[-0.5, 0.5, 1.5], edgecolor='black', rwidth=0.8)
    plt.xticks([0, 1], ["No Collapse", "Collapse"])
    plt.title(f"Outcome Distribution for Strategy '{strategy}'")
    plt.xlabel("Game Collapse")
    plt.ylabel("Count")
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()
