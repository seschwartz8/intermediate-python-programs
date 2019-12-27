"""
Mini-max Tic-Tac-Toe Player using recursion and depth-first search
"""

# Provided GUI imports from Rice University
import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col). If game is over, the move (-1, -1) is returned.
    """
    # Establish base case (if game is over)
    score = 0
    if board.check_win() != None:
        move = (-1, -1)
        if board.check_win() == provided.PLAYERX:
            score = SCORES[provided.PLAYERX]
        elif board.check_win() == provided.PLAYERO:
            score = SCORES[provided.PLAYERO]
        elif board.check_win() == provided.DRAW:
            score = SCORES[provided.DRAW]
        return score, move
    else:
        # Initialize best_score and best_move at worst potential
        best_score = -1
        best_move = ()
        # For each empty square on the board
        for empty_square in list(board.get_empty_squares()):
            # Copy potential board child
            potential_board = board.clone()
            # Move into one of the empty squares as current player
            potential_board.move(empty_square[0], empty_square[1], player)
            # Use recursion to determine score and best move of potential board
            # given counter moves of opposing player
            score, move = mm_move(potential_board, provided.switch_player(player))
            # Return immediately if you've found best possible move
            if score * SCORES[player] == 1:
                return score, empty_square
            # Otherwise compare and store best scores/moves
            elif score * SCORES[player] > best_score:
                best_score = score
                best_move = empty_square
        return best_score, best_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]


#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
