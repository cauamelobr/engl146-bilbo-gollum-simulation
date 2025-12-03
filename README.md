# The Bilbo vs. Gollum Game: A Simple Explanation

Imagine you could play the famous "Riddle Game" from *The Hobbit* thousands of times in a row to see what strategy works best. That's exactly what this computer program does!

## What is this?
This is a **simulation**. Think of it like a very fast video game that plays itself. We tell the computer the rules of the encounter between Bilbo and Gollum, and then we ask it to play out the scene 100,000 times to see what happens.

## The Players

### 🧙‍♂️ Bilbo
Bilbo is in a tight spot. He can choose how to behave:
1.  **Be Fair**: Play by the rules and hope Gollum does too.
2.  **Cheating (Defect)**: Use the Ring to escape or trick Gollum.
3.  **Adaptive**: Look at Gollum and decide. If Gollum looks dangerous, cheat. If he looks calm, play fair.

### 👹 Gollum
Gollum is unpredictable.
- Sometimes he is **Fair** and will let Bilbo go if he wins.
- Sometimes he is **Treacherous** and will try to eat Bilbo no matter what.
- Even a "Fair" Gollum might snap and attack if he gets frustrated!

## The Experiment
We wanted to answer one question: **What is the best way for Bilbo to survive?**

We ran the simulation for three different strategies:

1.  **Always Be Nice**: Bilbo always plays fair.
    - *Risk*: If Gollum is treacherous, Bilbo gets eaten.
2.  **Always Cheat**: Bilbo always uses the Ring.
    - *Risk*: This might provoke a fight, but it's safer than trusting a monster.
3.  **Smart Strategy (Adaptive)**: Bilbo guesses what mood Gollum is in.
    - *Goal*: Get the best of both worlds.

## The Results
The computer showed us that:
- **Being Nice is Dangerous**: Trusting Gollum blindly is the riskiest option.
- **Cheating Works**: It's not polite, but it keeps Bilbo alive more often.
- **Being Smart is Best**: If Bilbo can correctly guess if Gollum is lying, he has the highest chance of survival.

---

# Technical Documentation

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the simulation:
```bash
python main.py
```

This will:
1.  Run a Monte Carlo simulation for 100,000 rounds.
2.  Print the survival probabilities for each strategy.
3.  Generate visualization plots (Heatmaps and Histograms).

## Project Structure

- `main.py`: Entry point.
- `simulation.py`: Core simulation logic and configuration.
- `visualization.py`: Plotting functions.
- `test_simulation.py`: Unit tests.
