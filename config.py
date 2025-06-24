# config.py
# This file contains all the configuration settings and constants for the game.

# --- Game Logic ---
HEX_RADIUS = 3
WINNING_LENGTH = 4
AI_PLAYER = 'O'
HUMAN_PLAYER = 'X'

# --- AI Behavior ---
# The new structure includes depth and mistake chance for each level.
DIFFICULTY_LEVELS = {
    "Easy":   {"depth": 2, "mistake": 0.30},
    "Medium": {"depth": 3, "mistake": 0.15},
    "Hard":   {"depth": 4, "mistake": 0.05},
}
AI_THINK_TIME = 0.05 

# --- UI / Visual Design ---
INITIAL_WIDTH = 600
INITIAL_HEIGHT = 700
MIN_WIDTH = 450
MIN_HEIGHT = 550

BG_COLOR = "#1a2a3a"
TEXT_COLOR = "#ffffff"
BUTTON_BG_COLOR = "#1f3641"
BUTTON_ACTIVE_BG_COLOR = "#2a475e"
ACCENT_COLOR = "#66fcf1"

EMPTY_COLOR = "#2a475e"
PLAYER_X_COLOR = "#66fcf1" # Default Player Color
PLAYER_O_COLOR = "#f7a072" # Default AI Color
BORDER_COLOR = "#1f3641"
WIN_LINE_COLOR = "#ffeb3b"

# New: Added color options for the selection menu
COLOR_OPTIONS = [
    "#66fcf1", # Neon Cyan (Default P1)
    "#f7a072", # Deep Orange (Default AI)
    "#a4de02", # Lime Green
    "#ff4b91", # Hot Pink
    "#b072f7", # Lavender
    "#ffffff", # White
]

TITLE_FONT = ("Consolas", 28, "bold")
BUTTON_FONT = ("Consolas", 16, "bold")
STATUS_FONT = ("Consolas", 14, "bold")
