# 🎮 HexaTac:

*A modern, challenging re-imagining of Tic-Tac-Toe, built with Python & Tkinter.*

Face off against a configurable AI opponent on a **hexagonal** grid where the goal is to align **four** tiles.  With a responsive UI, customizable colours, and three difficulty settings.

---

## ✨ Features

|                           |                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------- |
| **Hexagonal Grid**        | A fresh twist that demands new strategies and spatial thinking.                                   |
| **Challenging AI**        | Minimax + alpha–beta pruning, with tunable “blunder” chance to keep it beatable.                  |
| **Adjustable Difficulty** | *Easy*, *Medium*, *Hard* → different search depths & mistake rates.                               |
| **Customisable Colours**  | In-game palette (6 vibrant hues) for both players.                                                |
| **Responsive Interface**  | Grid smoothly scales to any window size, including full-screen.                                  |
| **Win-Streak Tracking**   | Tracks current & best streaks for extra bragging rights.                                          |
| **Clean Architecture**    | UI, game logic, AI, and config live in separate modules; easy to extend or embed.                |

---

## 📸 Screenshots

<p align="center">
  <img src="https://i.imgur.com/gjEKakl.png" width="400" alt="Main menu">
  <img src="https://i.imgur.com/4qWj5Be.png"  width="400" alt="Gameplay">
</p>

---

## 🛠️ Technologies & Project Layout

* **Python 3 only** – no external deps  
* GUI: built-in **Tkinter**

```text
/hexatac/
├── main.py        # application entry-point
├── gui.py         # Tkinter UI & event loop
├── game_logic.py  # board representation, rules, win/draw detection
├── ai.py          # Minimax opponent + heuristics
└── config.py      # colours, fonts, gameplay constants
```
## 🚀 Getting Started

* **Python 3.6+**
  
  ```text
  git clone https://github.com/<your-username>/HexaTac.git
  cd HexaTac
  python main.py
* The game window pops up – start playing immediately!

## 🎲 How to Play

### Main Menu
1. **Pick a difficulty**&nbsp;— *Easy*, *Medium*, or *Hard*.  
2. *(Optional)* click **Colour Selector** to customise tile colours.  
3. Press **Play Game** to begin.

### Gameplay
- You are **`X`** and always move first.  
- **Click** any empty hex tile to place your mark.  
- The **first player to align four** tiles in a straight hex-direction wins.

### Game Over
- A pop-up shows the result plus your current / best win-streaks.  
- Choose **Play Again** (same settings) or **Main Menu** to return.
