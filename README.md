# 🧠 Reinforcement Learning Agent with SARSA and More

This project implements intelligent agents using reinforcement learning algorithms such as **SARSA**, **Q-Learning**, and **ε-greedy exploration**. The agent learns to navigate an environment (e.g., a GridWorld or Pac-Man maze) by interacting with it and maximizing long-term reward.

> This project was part of an academic exploration into applied machine learning and autonomous agent design.

---

## 📌 Features

- ✅ Implemented **SARSA (State-Action-Reward-State-Action)** algorithm from scratch
- ✅ Integrated **Q-learning** with epsilon-greedy policies
- ✅ Custom reward shaping to improve learning performance
- ✅ Designed exploration-vs-exploitation trade-offs using decaying epsilon strategies
- ✅ Visual environment simulations (e.g., Pac-Man, GridWorld)
- ✅ Logging and debugging tools to monitor agent behavior over episodes

---

## 🧠 Algorithms Implemented

| Algorithm | Description |
|----------|-------------|
| **SARSA** | On-policy method for learning state-action values. The agent updates its Q-values using the action actually taken in the next state. |
| **Q-Learning** | Off-policy method that uses the max action-value from the next state, regardless of the policy being followed. |
| **ε-greedy** | A strategy where the agent explores randomly with probability ε and exploits the best-known action otherwise. |

---

## 🎯 Goal of the Project

The goal was to develop an intelligent agent capable of learning optimal strategies through interaction with its environment, without prior knowledge of the environment’s dynamics.

This included:
- Understanding the convergence properties of SARSA vs Q-Learning
- Testing robustness of the learned policy in stochastic environments
- Exploring feature engineering and state abstraction

---

## 🛠️ Installation & Setup

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
pip install -r requirements.txt
python run_agent.py
