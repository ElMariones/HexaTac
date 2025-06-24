# game_logic.py
# Core game engine – independent of GUI & AI.

import config

# Axial directions for a hex grid
DIRECTIONS = [
    (1, 0),  (0, 1),  (-1, 1),
    (-1, 0), (0, -1), (1, -1)
]


class HexaTacGame:
    """Manages the game logic and state."""
    def __init__(self):
        self.radius = config.HEX_RADIUS
        self.board = self._create_board()
        self.current_player = config.HUMAN_PLAYER
        self.is_game_over = False
        self.winner = None
        self.winning_line = []

    # ------------------------------------------------------------------ #
    #                          BOARD CREATION                            #
    # ------------------------------------------------------------------ #
    def _create_board(self):
        """
        Creates a radius-N hexagon in axial coordinates.

        A tile (q, r) is inside the board iff
            |q| ≤ radius, |r| ≤ radius, |s| ≤ radius
        where s = -q - r
        """
        board = {}
        for q in range(-self.radius, self.radius + 1):
            for r in range(-self.radius, self.radius + 1):
                s = -q - r
                if abs(s) <= self.radius:
                    board[(q, r)] = None
        return board

    # ------------------------------------------------------------------ #
    #                         MOVE HANDLING                              #
    # ------------------------------------------------------------------ #
    def make_move(self, q, r):
        """
        Places the current player’s mark on (q, r) **only if** the
        coordinate is on the board and the tile is empty.
        """
        if (
            (q, r) in self.board           
            and self.board[(q, r)] is None
            and not self.is_game_over
        ):
            self.board[(q, r)] = self.current_player

            if self._check_win(q, r):
                self.is_game_over = True
                self.winner = self.current_player
            elif self._is_draw():
                self.is_game_over = True
                self.winner = "Draw"
            else:
                # switch turns
                self.current_player = (
                    config.AI_PLAYER
                    if self.current_player == config.HUMAN_PLAYER
                    else config.HUMAN_PLAYER
                )
            return True
        return False

    # ------------------------------------------------------------------ #
    #                       WIN / DRAW DETECTION                         #
    # ------------------------------------------------------------------ #
    def _check_win(self, q, r):
        """Returns True if the last move completed a 4-in-a-row line."""
        player = self.board.get((q, r))
        if not player:
            return False

        for dq, dr in DIRECTIONS:
            line = [(q, r)]

            # forward direction
            for i in range(1, config.WINNING_LENGTH):
                qq, rr = q + dq * i, r + dr * i
                if self.board.get((qq, rr)) == player:
                    line.append((qq, rr))
                else:
                    break

            # backward direction
            for i in range(1, config.WINNING_LENGTH):
                qq, rr = q - dq * i, r - dr * i
                if self.board.get((qq, rr)) == player:
                    line.append((qq, rr))
                else:
                    break

            if len(line) >= config.WINNING_LENGTH:
                self.winning_line = line[:config.WINNING_LENGTH]
                return True
        return False

    def _is_draw(self):
        return all(v is not None for v in self.board.values())

    # ------------------------------------------------------------------ #
    #                         PUBLIC HELPERS                             #
    # ------------------------------------------------------------------ #
    def get_valid_moves(self):
        """List of empty tiles on the board."""
        return [pos for pos, owner in self.board.items() if owner is None]

    def reset(self):
        self.__init__()
