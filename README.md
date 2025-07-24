# 👾 Pac-Man AI – Classical Search & Adversarial Agents

This project implements intelligent Pac-Man agents using classical artificial intelligence algorithms such as **Minimax**, **Alpha-Beta Pruning**, **Expectimax**, and **A\***. The agents are designed to make optimal decisions in a dynamic environment involving ghosts, food pellets, and power capsules.

> Developed as part of an AI coursework (e.g., UC Berkeley CS188), this assignment focuses on building adversarial agents and pathfinding strategies without relying on machine learning.

---

## 🧩 Features

- ✅ **Reflex Agent** using evaluation functions
- ✅ **Minimax Agent** (perfect-play adversarial search)
- ✅ **Alpha-Beta Pruning Agent** (optimized minimax)
- ✅ **Expectimax Agent** (probabilistic ghost behavior)
- ✅ **Custom Evaluation Function** to guide decisions
- ✅ **A\* Search** for efficient pathfinding (optional/extra)

---

## 📷 Demo

> (Include a screenshot or GIF of your Pac-Man AI dodging ghosts and grabbing pellets if available.)

---

## 🧠 Algorithms Implemented

### Minimax Agent
- Treats ghosts as adversaries
- Recursively evaluates game trees to a fixed depth
- Picks the move that maximizes Pac-Man’s guaranteed outcome

### Alpha-Beta Agent
- Pruned version of minimax to reduce computation
- Cuts off branches that cannot affect the final decision
- Greatly improves efficiency for deeper trees

### Expectimax Agent
- Models ghosts as stochastic agents
- Uses expected values rather than worst-case assumptions
- More realistic for uncertain environments

### Reflex Agent
- Evaluates actions based on a hand-crafted function considering:
  - Distance to nearest food
  - Ghost proximity
  - Power capsule availability

---

## 🔍 Evaluation Function Design

Custom evaluation function takes into account:
- Manhattan distance to closest food
- Distance to active/scared ghosts
- Number of remaining food pellets
- Current score and penalty for stopping

> This function was critical for reflex and depth-limited agents to behave effectively.

---

## 🗂️ File Structure

```bash
.
├── multiAgents.py          # Main AI logic for agents
├── search.py               # A* and other search utilities
├── pacman.py               # Game engine
├── util.py                 # Helper functions
├── README.md
