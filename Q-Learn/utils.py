import numpy as np
import copy

def get_metrics(board):
    # Assuming Board class has methods to retrieve necessary information
    capped = board.black_kings + board.white_kings  # Number of kings on the board
    potential = len(board.get_all_moves(board.turn))  # Number of possible moves for the current player
    men = len(board.get_all_pieces(board.turn))  # Number of men for the current player
    kings = board.black_kings - board.white_kings  # Difference in the number of kings
    caps = len(board.capturables(board.turn))  # Number of capturable pieces for the current player
    semicaps = len(board.semicapturables(board.turn))  # Number of semicapturable pieces for the current player
    uncaps = len(board.uncapturables(board.turn))  # Number of uncapturable pieces for the current player
    mid = len(board.at_middle(board.turn))  # Number of pieces at the middle of the board for the current player
    far = len(board.at_enemy(board.turn))  # Number of pieces at the enemy's side of the board for the current player
    won = 1 if board.winner(None) == board.turn else 0  # Check if the current player has won

    score = 4 * capped + potential + men + 3 * kings + caps + 2 * semicaps + 3 * uncaps + 2 * mid + 3 * far + 100 * won

    if score < 0:
        return np.array([-1, capped, potential, men, kings, caps, semicaps, uncaps, mid, far, won])
    else:
        return np.array([1, capped, potential, men, kings, caps, semicaps, uncaps, mid, far, won])

# function to get all possible moves for a given player
def get_all_moves(board,color,game):
    
    moves=[]
    # loop through all pieces of the given color
    for piece in board.get_all_pieces(color):
        # get all valid moves for the current piece
        valid_moves=board.get_valid_moves(piece)
        
        for move, skip in valid_moves.items(): 
            # simulate the move and add the resulting board to the list of moves
            temp_board = copy.deepcopy(board)   
            temp_piece = temp_board.get_piece(piece.row, piece.col)  
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board) 

    return moves  

def simulate_move(piece, move, board, game, skip):
    # Assume piece is an instance of the Pieces class representing a checkers piece

    # Extract destination coordinates from the move
    dest_row, dest_col = move

    # Update the piece's position on the simulated board
    board.move(piece, dest_row, dest_col)

    # Check if any opponent's pieces are skipped and remove them
    if skip:
        for skipped_piece in skip:
            board.remove(skipped_piece)

    # Perform any additional checks or updates based on the game rules

    # For example, if a piece reaches the opposite end of the board, make it a king
    if dest_row == 0 or dest_row == board.ROWS - 1:
        piece.make_king()

    # Perform any other checks or updates based on the specific rules of the game

    # Return the updated board
    return board


def expand(board_state):
    flattened_state = board_state.flatten()
    return flattened_state


def compress(flattened_state):
    board_state = np.reshape(flattened_state, (8, 8))  
    return board_state
