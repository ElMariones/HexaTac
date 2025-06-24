# gui.py
# This file handles the entire graphical user interface using Tkinter.
# It now manages multiple frames (Menu, Game) for a better user experience.

import tkinter as tk
import math
import random
import config
from game_logic import HexaTacGame
import ai

class HexaTacApp(tk.Tk):
    """The main application window that manages different frames."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("HexaTac: by Mario Landaburu")
        self.geometry(f"{config.INITIAL_WIDTH}x{config.INITIAL_HEIGHT}")
        self.minsize(config.MIN_WIDTH, config.MIN_HEIGHT)
        self.configure(bg=config.BG_COLOR)

        self.current_difficulty_name = "Medium"

        # --- Store custom colors at the app level ---
        self.player_color = tk.StringVar(value=config.PLAYER_X_COLOR)
        self.ai_color = tk.StringVar(value=config.PLAYER_O_COLOR)

        # --- Store streaks ---
        self.current_streak = 0
        self.best_streak = 0

        # Container for all frames
        container = tk.Frame(self, bg=config.BG_COLOR)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # --- NEW: Added ColorSelectorMenu to the frame list ---
        for F in (MainMenu, GameScreen, ColorSelectorMenu):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.bind("<Configure>", self.on_app_resize)

        self.show_frame("MainMenu")

    def on_app_resize(self, event=None):
        """When the main window resizes, tell the active GameScreen to update itself."""
        game_frame = self.frames["GameScreen"]
        if game_frame.winfo_viewable():
            game_frame.on_resize()

    def show_frame(self, page_name):
        """Raises the selected frame to the top."""
        if page_name == "GameScreen":
            game_frame = self.frames["GameScreen"]
            game_frame.start_new_game(self.current_difficulty_name)
        
        frame = self.frames[page_name]
        frame.tkraise()

class MainMenu(tk.Frame):
    """The main menu screen."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=config.BG_COLOR)
        self.controller = controller
        
        self.difficulty_var = tk.StringVar(value="Medium")

        title_label = tk.Label(self, text="HexaTac", font=config.TITLE_FONT, bg=config.BG_COLOR, fg=config.TEXT_COLOR)
        title_label.pack(side="top", pady=(80, 20))
        
        subtitle_label = tk.Label(self, text="by Mario Landaburu", font=config.BUTTON_FONT, bg=config.BG_COLOR, fg=config.ACCENT_COLOR)
        subtitle_label.pack(side="top", pady=(0, 60))

        difficulty_frame = tk.Frame(self, bg=config.BG_COLOR)
        difficulty_frame.pack(pady=20)

        tk.Label(difficulty_frame, text="Select Difficulty:", font=config.STATUS_FONT, bg=config.BG_COLOR, fg=config.TEXT_COLOR).pack()

        for level in config.DIFFICULTY_LEVELS.keys():
            rb = tk.Radiobutton(difficulty_frame, text=level, variable=self.difficulty_var, value=level,
                                font=config.STATUS_FONT, bg=config.BG_COLOR, fg=config.TEXT_COLOR, 
                                selectcolor=config.BUTTON_BG_COLOR, activebackground=config.BG_COLOR, 
                                activeforeground=config.TEXT_COLOR, indicatoron=False,
                                borderwidth=2, relief=tk.RAISED, padx=20, pady=10)
            rb.pack(fill="x", pady=5)

        button_frame = tk.Frame(self, bg=config.BG_COLOR)
        button_frame.pack(pady=40)

        play_button = tk.Button(button_frame, text="Play Game", font=config.BUTTON_FONT,
                                command=self.play_game,
                                bg=config.BUTTON_BG_COLOR, fg=config.TEXT_COLOR, 
                                activebackground=config.BUTTON_ACTIVE_BG_COLOR, relief=tk.FLAT, padx=20, pady=10)
        play_button.pack(pady=10)
        
        # --- NEW: Color Selector Button ---
        color_button = tk.Button(button_frame, text="Color Selector", font=config.BUTTON_FONT,
                                command=lambda: controller.show_frame("ColorSelectorMenu"),
                                bg=config.BUTTON_BG_COLOR, fg=config.TEXT_COLOR, 
                                activebackground=config.BUTTON_ACTIVE_BG_COLOR, relief=tk.FLAT, padx=20, pady=10)
        color_button.pack(pady=10)

    def play_game(self):
        """Stores the selected difficulty and switches to the game screen."""
        self.controller.current_difficulty_name = self.difficulty_var.get()
        self.controller.show_frame("GameScreen")

class ColorSelectorMenu(tk.Frame):
    """A screen for selecting player and AI colors."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=config.BG_COLOR)
        self.controller = controller
        self.player_btns = {}
        self.ai_btns = {}

        tk.Label(self, text="Color Selector", font=config.TITLE_FONT, bg=config.BG_COLOR, fg=config.TEXT_COLOR).pack(pady=(40, 20))

        # Player Color Section
        tk.Label(self, text="Player Color", font=config.BUTTON_FONT, bg=config.BG_COLOR, fg=self.controller.player_color.get()).pack(pady=(20, 10))
        player_frame = tk.Frame(self, bg=config.BG_COLOR)
        player_frame.pack()
        self._create_color_buttons(player_frame, "player")

        # AI Color Section
        tk.Label(self, text="AI Color", font=config.BUTTON_FONT, bg=config.BG_COLOR, fg=self.controller.ai_color.get()).pack(pady=(40, 10))
        ai_frame = tk.Frame(self, bg=config.BG_COLOR)
        ai_frame.pack()
        self._create_color_buttons(ai_frame, "ai")
        
        # Back Button
        back_button = tk.Button(self, text="Back to Menu", font=config.BUTTON_FONT,
                                command=lambda: controller.show_frame("MainMenu"),
                                bg=config.BUTTON_BG_COLOR, fg=config.TEXT_COLOR,
                                activebackground=config.BUTTON_ACTIVE_BG_COLOR, relief=tk.FLAT, padx=20, pady=10)
        back_button.pack(pady=60)

    def _create_color_buttons(self, parent_frame, target):
        """Helper to create a grid of color swatch buttons."""
        btn_dict = self.player_btns if target == "player" else self.ai_btns
        for i, color_hex in enumerate(config.COLOR_OPTIONS):
            btn = tk.Button(parent_frame, bg=color_hex, width=6, height=3,
                            command=lambda c=color_hex: self._select_color(target, c))
            btn.grid(row=0, column=i, padx=5, pady=5)
            btn_dict[color_hex] = btn
    
    def _select_color(self, target, color_hex):
        """Handles the logic of selecting a color."""
        if target == "player":
            if color_hex != self.controller.ai_color.get():
                self.controller.player_color.set(color_hex)
        elif target == "ai":
            if color_hex != self.controller.player_color.get():
                self.controller.ai_color.set(color_hex)
        
        # Update UI to reflect the new selection
        self.update_selections()

    def update_selections(self):
        """Updates the button states to show selections and disabled options."""
        player_color = self.controller.player_color.get()
        ai_color = self.controller.ai_color.get()
        
        # Update player buttons
        for color, btn in self.player_btns.items():
            btn.config(state=tk.NORMAL, relief=tk.RAISED)
            if color == ai_color:
                btn.config(state=tk.DISABLED, relief=tk.FLAT)
            if color == player_color:
                btn.config(relief=tk.SUNKEN)

        # Update AI buttons
        for color, btn in self.ai_btns.items():
            btn.config(state=tk.NORMAL, relief=tk.RAISED)
            if color == player_color:
                btn.config(state=tk.DISABLED, relief=tk.FLAT)
            if color == ai_color:
                btn.config(relief=tk.SUNKEN)

class GameScreen(tk.Frame):
    """The screen where the actual game is played."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=config.BG_COLOR)
        self.controller = controller
        self.game = None
        self.difficulty_settings = None # This will hold the dict e.g. {"depth": 3, "mistake": 0.15}
        self.difficulty_name = None
        self.tile_size = 0 
        self.end_game_overlay = None
        self.after_id = None # To manage the scheduled AI turn

        self.status_label = tk.Label(self, text="", fg=config.TEXT_COLOR, bg=config.BG_COLOR, font=config.STATUS_FONT)
        self.status_label.pack(pady=10)

        self.canvas = tk.Canvas(self, bg=config.BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def start_new_game(self, difficulty_name="Medium"):
        """Initializes or resets the game state for a new round."""
        self.game = HexaTacGame()
        self.difficulty_name = difficulty_name
        self.difficulty_settings = config.DIFFICULTY_LEVELS[difficulty_name]
        self.status_label.config(text=f"Your Turn (X) | Difficulty: {difficulty_name}")
        
        if self.end_game_overlay:
            self.end_game_overlay.destroy()
            self.end_game_overlay = None

        # Cancel any lingering AI turn from a previous game
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.after(10, self.on_resize)

    def on_resize(self, event=None):
        """Handles window resizing by scaling the hex grid."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return 

        grid_width_in_tiles = (config.HEX_RADIUS * 2 + 1) * 1.5
        grid_height_in_tiles = (config.HEX_RADIUS * 2 + 1) * math.sqrt(3)

        size_from_width = canvas_width / grid_width_in_tiles
        size_from_height = canvas_height / grid_height_in_tiles
        
        self.tile_size = min(size_from_width, size_from_height) * 0.9 
        
        self.draw_board()
        if self.game and self.game.is_game_over and self.end_game_overlay is None:
            self.show_end_game_options()


    def hex_to_pixel(self, q, r, center_x, center_y):
        """Converts axial hex coordinates to canvas pixel coordinates."""
        x = self.tile_size * (3/2 * q) + center_x
        y = self.tile_size * (math.sqrt(3)/2 * q + math.sqrt(3) * r) + center_y
        return x, y

    def pixel_to_hex(self, x_pix, y_pix):
        """Converts canvas pixel coordinates to the nearest axial hex coordinates."""
        if self.tile_size == 0: return 0, 0
        center_x, center_y = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2
        x_centered, y_centered = x_pix - center_x, y_pix - center_y
        q_frac = (2/3 * x_centered) / self.tile_size
        r_frac = (-1/3 * x_centered + math.sqrt(3)/3 * y_centered) / self.tile_size
        s_frac = -q_frac - r_frac
        q, r, s = round(q_frac), round(r_frac), round(s_frac)
        q_diff, r_diff, s_diff = abs(q - q_frac), abs(r - r_frac), abs(s - s_frac)
        if q_diff > r_diff and q_diff > s_diff: q = -r - s
        elif r_diff > s_diff: r = -q - s
        return int(q), int(r)

    def draw_board(self):
        if not self.game:
            return
        # wipe previous hexes / winning outline
        self.canvas.delete("hex")
        self.canvas.delete("win")

        cx, cy = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2

        # draw every tile
        for (q, r), owner in self.game.board.items():
            self.draw_hex(q, r, owner, cx, cy)          # draw_hex now tags="hex"

        # overlay a glowing outline if someone has won
        if self.game.is_game_over and self.game.winner != "Draw":
            self.draw_winning_line(cx, cy)              # draw_winning_line tags="win"


    def draw_hex(self, q, r, owner, center_x, center_y):
        """Draws a single hexagon tile on the canvas."""
        hex_center_x, hex_center_y = self.hex_to_pixel(q, r, center_x, center_y)
        points = []
        for i in range(6):
            angle_rad = math.pi / 180 * (60 * i)
            points.append((hex_center_x + self.tile_size * math.cos(angle_rad), hex_center_y + self.tile_size * math.sin(angle_rad)))
        fill_color = {
            config.HUMAN_PLAYER: self.controller.player_color.get(),
            config.AI_PLAYER: self.controller.ai_color.get()
        }.get(owner, config.EMPTY_COLOR)
        self.canvas.create_polygon(points, fill=fill_color, outline=config.BORDER_COLOR, width=2, tags="hex")

    def draw_winning_line(self, center_x, center_y):
        """Highlights the winning four-in-a-row."""
        if not self.game or not self.game.winning_line or not isinstance(self.game.winning_line, list):
            return

        for (q, r) in self.game.winning_line:
            hex_center_x, hex_center_y = self.hex_to_pixel(q, r, center_x, center_y)
            points = []
            for i in range(6):
                angle_rad = math.pi / 180 * (60 * i)
                points.append((hex_center_x + self.tile_size * math.cos(angle_rad), hex_center_y + self.tile_size * math.sin(angle_rad)))
            self.canvas.create_polygon(points, fill="", outline=config.WIN_LINE_COLOR, width=4, tags="win")

    def on_canvas_click(self, event):
        """Handles player clicks on the board."""
        if self.game and self.game.current_player == config.HUMAN_PLAYER and not self.game.is_game_over:
            q, r = self.pixel_to_hex(event.x, event.y)
            if self.game.make_move(q, r):
                self.draw_board()
                self.update_status()
                if not self.game.is_game_over:
                    self.after_id = self.after(int(config.AI_THINK_TIME * 1000), self.ai_turn)

    def ai_turn(self):
        """Initiates the AI's move and updates the board."""
        self.after_id = None # Clear the ID as the turn is now running
        if self.game and self.game.current_player == config.AI_PLAYER and not self.game.is_game_over:
            self.status_label.config(text="AI is thinking...")
            self.update_idletasks()
            
            # **FIX:** Pass the entire difficulty_settings dictionary to the AI module.
            # The AI module will handle the logic for mistakes and depth.
            best_move = ai.find_best_move(self.game, self.difficulty_settings)
            
            # The rest of the function remains the same, but the call above is now correct.
            if best_move and self.game.make_move(best_move[0], best_move[1]):
                self.draw_board()
                self.update_status()

    def update_status(self):
        """Updates the status label, tracks win streaks, and shows end-game options."""
        if not self.game: return
        
        if self.game.is_game_over:
            if self.game.winner == config.HUMAN_PLAYER:
                self.controller.current_streak += 1
                if self.controller.current_streak > self.controller.best_streak:
                    self.controller.best_streak = self.controller.current_streak
            elif self.game.winner == config.AI_PLAYER or self.game.winner == "Draw":
                self.controller.current_streak = 0
            
            if self.game.winner == "Draw":
                self.status_label.config(text="It's a Draw!")
            else:
                winner_name = "You" if self.game.winner == config.HUMAN_PLAYER else "The AI"
                self.status_label.config(text=f"Game Over: {winner_name} Wins!")
            self.show_end_game_options()
        else:
            self.status_label.config(text=f"Your Turn (X) | Difficulty: {self.difficulty_name}")

    def show_end_game_options(self):
        """Displays 'Play Again' and 'Main Menu' buttons over the canvas."""
        if self.end_game_overlay: self.end_game_overlay.destroy()

        self.end_game_overlay = tk.Frame(self.canvas, bg=config.BG_COLOR, relief=tk.RAISED, borderwidth=2)
        
        streak_font = ("Consolas", 12)
        streak_text = f"Current Streak: {self.controller.current_streak}"
        best_streak_text = f"Best Streak: {self.controller.best_streak}"

        tk.Label(self.end_game_overlay, text=streak_text, font=streak_font, bg=config.BG_COLOR, fg=config.TEXT_COLOR).pack(side="top", pady=(10, 5), padx=20)
        tk.Label(self.end_game_overlay, text=best_streak_text, font=streak_font, bg=config.BG_COLOR, fg=config.TEXT_COLOR).pack(side="top", pady=(5, 10), padx=20)

        play_again_cmd = lambda: self.controller.show_frame("GameScreen")
        
        play_again_btn = tk.Button(self.end_game_overlay, text="Play Again", font=config.BUTTON_FONT, command=play_again_cmd,
                                   bg=config.BUTTON_BG_COLOR, fg=config.TEXT_COLOR, activebackground=config.BUTTON_ACTIVE_BG_COLOR, relief=tk.FLAT, padx=10, pady=5)
        play_again_btn.pack(side="top", pady=10, padx=20)
        
        main_menu_btn = tk.Button(self.end_game_overlay, text="Main Menu", font=config.BUTTON_FONT, command=lambda: self.controller.show_frame("MainMenu"),
                                  bg=config.BUTTON_BG_COLOR, fg=config.TEXT_COLOR, activebackground=config.BUTTON_ACTIVE_BG_COLOR, relief=tk.FLAT, padx=10, pady=5)
        main_menu_btn.pack(side="top", pady=(0,10), padx=20)

        self.canvas.create_window(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, window=self.end_game_overlay, anchor="center")
