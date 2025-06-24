# ai.py
# This file contains all the AI logic, including the Minimax algorithm and board evaluation.

import math
import random
import config

def _find_immediate_threats(game, valid_moves):
    """
    Checks for immediate win or loss scenarios to speed up decision-making.
    Returns the critical move if found, otherwise None.
    """
    # Check if the AI can win in one move
    for move in valid_moves:
        temp_board = game.board.copy()
        temp_board[move] = config.AI_PLAYER
        # A lightweight check for a win from this move
        if _is_winning_move(temp_board, move, config.AI_PLAYER):
            return move  # Take the winning move immediately

    # Check if the Player can win in one move, and block them
    for move in valid_moves:
        temp_board = game.board.copy()
        temp_board[move] = config.HUMAN_PLAYER
        if _is_winning_move(temp_board, move, config.HUMAN_PLAYER):
            return move # Block the player's winning move

    return None

def _is_winning_move(board, last_move, player):
    """
    A lightweight version of game_logic.check_win for internal AI use.
    Checks if 'last_move' by 'player' resulted in a win on the given 'board'.
    """
    q, r = last_move
    for dq, dr in [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]:
        line = [last_move]
        # Check one direction
        for i in range(1, config.WINNING_LENGTH):
            pos = (q + dq * i, r + dr * i)
            if board.get(pos) == player:
                line.append(pos)
            else:
                break
        if len(line) >= config.WINNING_LENGTH:
            return True
    return False

def evaluate_sequence(sequence, player):
    """
    Evaluates a single line of 4 tiles. This has been updated for more aggressive scoring.
    """
    score = 0
    opponent = config.HUMAN_PLAYER if player == config.AI_PLAYER else config.AI_PLAYER
    
    player_count = sequence.count(player)
    empty_count = sequence.count(None)
    opponent_count = sequence.count(opponent)

    if player_count == 4:
        score += 100000
    elif player_count == 3 and empty_count == 1:
        score += 1000
    elif player_count == 2 and empty_count == 2:
        score += 50

    if opponent_count == 3 and empty_count == 1:
        score -= 5000
    elif opponent_count == 2 and empty_count == 2:
        score -= 200
        
    return score

def evaluate_board(board):
    """
    Scores the entire board state from the perspective of the AI.
    This version is more efficient than the previous one.
    """
    score = 0
    # Iterate through every tile as a potential start of a line
    for (q, r) in board:
        # Check in the 3 primary directions to not double-count lines
        for (dq, dr) in [(1, 0), (0, 1), (-1, 1)]:
            sequence = []
            is_valid_line = True
            for i in range(config.WINNING_LENGTH):
                pos = (q + dq * i, r + dr * i)
                # Check if the tile is on the board
                if pos in board:
                    sequence.append(board[pos])
                else:
                    is_valid_line = False
                    break
            
            if is_valid_line:
                score += evaluate_sequence(sequence, config.AI_PLAYER)
    return score


def is_terminal_node(board):
    """Checks if the board is full (a draw)."""
    return not any(v is None for v in board.values())

def minimax(board, depth, maximizing_player, alpha, beta, last_move=None): # Add last_move parameter
    """Minimax algorithm with alpha-beta pruning."""
    
    # This check is now more robust
    if _is_winning_move(board, last_move, config.HUMAN_PLAYER) if last_move else False:
        return -100000, last_move
    if _is_winning_move(board, last_move, config.AI_PLAYER) if last_move else False:
        return 100000, last_move
    if is_terminal_node(board): # Draw
        return 0, last_move

    if depth == 0:
        return evaluate_board(board), last_move

    valid_moves = [pos for pos, owner in board.items() if owner is None]
    if not valid_moves:
        return evaluate_board(board), None # No moves left

    if maximizing_player:
        max_eval = -math.inf
        best_move = random.choice(valid_moves)
        for move in valid_moves:
            temp_board = board.copy()
            temp_board[move] = config.AI_PLAYER
            evaluation, _ = minimax(temp_board, depth - 1, False, alpha, beta, move) # Pass move
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move
    else: # Minimizing player
        min_eval = math.inf
        best_move = random.choice(valid_moves)
        for move in valid_moves:
            temp_board = board.copy()
            temp_board[move] = config.HUMAN_PLAYER
            evaluation, _ = minimax(temp_board, depth - 1, True, alpha, beta, move) # Pass move
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval, best_move

# You also need to update the initial call in find_best_move
def find_best_move(game, difficulty_settings):
    """
    Main entry point for the AI's decision-making process.
    Accepts a dictionary of difficulty settings.
    """
    valid_moves = game.get_valid_moves()
    if not valid_moves:
        return None

    # Heuristic: Check for immediate wins or required blocks first.
    critical_move = _find_immediate_threats(game, valid_moves)
    if critical_move:
        return critical_move

    # Use the mistake chance from the passed settings
    if random.random() < difficulty_settings["mistake"]:
        return random.choice(valid_moves)
    
    # Use the depth from the passed settings for the full search
    depth = difficulty_settings["depth"]
    # The initial call doesn't have a "last_move", so we can pass None
    _, best_move = minimax(game.board, depth, True, -math.inf, math.inf, None) 
    
    # Add a fallback just in case minimax returns None
    if best_move is None and valid_moves:
        return random.choice(valid_moves)
    
    return best_move