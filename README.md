# Connect 4 AI Game

A Python-based **Connect 4** game featuring multiple player types:
- Human Player
- Random Player
- AI Player using **Alpha-Beta Pruning**
- AI Player using **Expectimax*

Includes a simple **Tkinter GUI** to play against AI or another human/random player.

---

## Features

- Play between Human vs AI, AI vs AI, Human vs Random, etc.
- AI Agents:
  - **Alpha-Beta Pruning** (optimal play against strategic opponent)
  - **Expectimax** (optimal play against random opponent)
- Evaluation function that considers 2-in-a-rows, 3-in-a-rows, and winning lines.
- GUI built with **Tkinter** to visualize moves in real-time.
- Time-limited AI moves using multiprocessing.

---

## 🎮 Game Rules

- 6 rows × 7 columns grid.
- Players alternate turns dropping tokens in columns.
- First player to connect 4 tokens horizontally, vertically, or diagonally wins.

---

## Getting Started

### Requirements

- Python 3.6+
- `numpy`

### Installation

```bash
git clone https://github.com/AkshayJadhav96/ConnectFour.git
cd ConnectFour
pip install numpy
```
### How to play
```bash
python ConnectFour.py <player1_type> <player2_type> --time <seconds>
```
