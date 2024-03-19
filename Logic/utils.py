import numpy as np
import copy
from pieces import *
from constants import *
from board import *

def get_metrics(board):
    # Assuming Board class has methods to retrieve necessary information
    capped = 12 - board.black_left
    potential = possible_moves(board) - possible_moves(reverse(board))
    men =   board.white_left - board.black_left 
    kings = board.white_kings - board.black_kings 
    caps = capturables(board) - capturables(reverse(board))
    semicaps = semicapturables(board)
    uncaps = uncapturables(board) - uncapturables(reverse(board))
    mid = at_middle(board) - at_middle(reverse(board))
    far = at_enemy(board) - at_enemy(reverse(board))
    won = game_winner(board)
    

    score = 4 * capped + potential + men + 3 * kings + caps + 2 * semicaps + 3 * uncaps + 2 * mid + 3 * far + 100 * won

    if score < 0:
        return np.array([-1, capped, potential, men, kings, caps, semicaps, uncaps, mid, far, won])
    else:
        return np.array([1, capped, potential, men, kings, caps, semicaps, uncaps, mid, far, won])

# function to get all possible moves for a given player
def get_all_moves(board,color,game):
    
    board_list=[]
    # loop through all pieces of the given color
    for piece in board.get_all_pieces(color):
        # get all valid moves for the current piece
        valid_moves=board.get_valid_moves(piece)
        
        for move, skip in valid_moves.items(): 
            # simulate the move and add the resulting board to the list of moves
            temp_board = copy.deepcopy(board)   
            temp_piece = temp_board.get_piece(piece.row, piece.col)  
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            board_list.append(new_board) 

    return board_list

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

# def expand(flattened_state):
#     board_state = np.reshape(flattened_state, (8, 8))  
#     return board_state

def expand(board):
	b = Board()
	b.create_blank_board()
	for i in range(0, 8):
		if (i%2 == 0):
			for j in range(0, 4):
				if board[i*4+j] ==1:
					b.board[i].append(0)
					b.board[i].append(Pieces(i, j, WHITE, False))
				elif board[i*4+j] == 3:
					b.board[i].append(0)
					b.board[i].append(Pieces(i, j, WHITE, True))
				elif board[i*4+j] == -1:
					b.board[i].append(0)
					b.board[i].append(Pieces(i, j, BLACK, False))
				elif board[i*4+j] == -3:
					b.board[i].append(0)
					b.board[i].append(Pieces(i, j, BLACK, True))
				else:
					b.board[i].append(0)
					b.board[i].append(0)
			#b[i] = np.array([0, board[i*4], 0, board[i*4 + 1], 0, board[i*4 + 2], 0, board[i*4 + 3]])
		else:
			for j in range(0, 4):
				if board[i*4+j] == 1:
					b.board[i].append(Pieces(i, j, WHITE, False))
					b.board[i].append(0)
				elif board[i*4+j] == 3:
					b.board[i].append(Pieces(i, j, WHITE, True))
					b.board[i].append(0)
				elif board[i*4+j] == -1:
					b.board[i].append(Pieces(i, j, BLACK, False))
					b.board[i].append(0)
				elif board[i*4+j] == -3:
					b.board[i].append(Pieces(i, j, BLACK, True))
					b.board[i].append(0)
				else:
					b.board[i].append(0)
					b.board[i].append(0)
			#b[i] = np.array([board[i*4], 0, board[i*4 + 1], 0, board[i*4 + 2], 0, board[i*4 + 3], 0])
	return b


# def compress(board_state):
#	  flattened_state = board_state.flatten()
#     return flattened_state


def compress(board):
	b = np.zeros((1,32), dtype='b')
	for i in range(0, 8):
		if (i%2 == 0):
			for j in np.arange(1, 8, 2):
				piece = board.board[i][j]
				if piece != 0:
					if (piece.color) == WHITE:
						if (piece.king):
							b[0, i*4 + j//2] = 3
						else:
							b[0, i*4 + j//2] = 1
					elif (piece.color) == BLACK:
						if (piece.king):
							b[0, i*4 + j//2] = -3
						else:
							b[0, i*4 + j//2] = -1
				else:
					b[0, i*4 + j//2] = 0
       		#b[0, i*4 : i*4+4] = np.array([board[i][1], board[i][3], board[i][5], board[i][7]])
		else:
			for j in np.arange(0, 8, 2):
				piece = board.board[i][j]
				if piece != 0:
					if (piece.color) == WHITE:
						if (piece.king):
							b[0, i*4 + j//2] = 3
						else:
							b[0, i*4 + j//2] = 1
					elif (piece.color) == BLACK:
						if (piece.king):
							b[0, i*4 + j//2] = -3
						else:
							b[0, i*4 + j//2] = -1
				else:
					b[0, i*4 + j//2] = 0
			#b[0, i*4 : i*4+4] = np.array([board[i, 0], board[i, 2], board[i, 4], board[i, 6]])
	return b

def reverse(board):
    # Iterate over each row in the board
    for row in range(ROWS):
        # Reverse the order of the pieces in the row
        board.board[row].reverse()
    # Reverse the order of the rows in the board
    board.board.reverse()

    return board


def generate_branches(board, x, y):
	tmp_board = compress(board)
	piece = board.board[x][y]
	if (piece != 0):
		if (piece.color == WHITE and x < 5):
			tmp_piece = piece
			if (y < 5):
				tmp_piece_1 = board.board[x+1][y+1]
				tmp_piece_2 = board.board[x+2][y+2]
				if (tmp_piece_1 != 0 and tmp_piece_1.color == BLACK and tmp_piece_2 == 0):
					board.board[x+2][y+2] = tmp_piece
					if (x+2 == 7):
						board.board[x+2][y+2].make_king()
					#temp = board[x+1, y+1]
					board.board[x+1][y+1] = 0
					if (board.board[x][y] != board.board[x+2][y+2]):
						board.board[x][y] = 0
						tmp_board = np.vstack((tmp_board, compress(board)))
					else:
						board.board[x][y] = 0
						tmp_board = np.vstack((tmp_board, generate_branches(board, x+2, y+2)))
					board.board[x+1][y+1] = tmp_piece_1
					board.board[x][y] = tmp_piece
					board.board[x+2][y+2] = 0
			if (y > 1):
				tmp_piece_1 = board.board[x+1][y-1]
				tmp_piece_2 = board.board[x+2][y-2]
				if (tmp_piece_1 != 0 and tmp_piece_1.color==BLACK and tmp_piece_2 == 0):
					board.board[x+2, y-2] = tmp_piece
					if (x+2 == 7):
						board.board[x+2][y-2].make_king()
					#temp = board[x+1, y-1]
					board.board[x+1][y-1] = 0
					if (board.board[x][y] != board.board[x+2][y-2]):
						board.board[x][y] = 0
						tmp_board = np.vstack((tmp_board, compress(board)))
					else:
						board.board[x][y] = 0
					tmp_board = np.vstack((tmp_board, generate_branches(board, x+2, y-2)))
					board.board[x+1][y-1] = tmp_piece_1
					board.board[x][y] = tmp_piece
					board.board[x+2][y-2] = 0
		if (piece.color == WHITE and piece.king == True and piece.row > 0):
			if (y < 5):
				tmp_piece_1 = board.board[x-1][y+1]
				tmp_piece_2 = board.board[x-2][y+2]
				if (tmp_piece_1.color == BLACK and tmp_piece_2 == 0):
					board.board[x-2][y+2] = piece
					board.board[x][y] = 0
					#temp = board[x-1, y+1]
					board.board[x-1][y+1] = 0
					tmp_board = np.vstack((tmp_board, generate_branches(board, x-2, y+2)))
					board.board[x-1][y+1] = tmp_piece_1
					board.board[x][y] = board.board[x-2][y+2]
					board.board[x-2][y+2] = 0
			if (y > 1):
				tmp_piece_1 = board.board[x-1][y-1]
				tmp_piece_2 = board.board[x-2][y-2]
				if (tmp_piece_1.color == BLACK and tmp_piece_2 == 0):
					board.board[x-2][y-2] = piece
					board.board[x][y] = 0
					#temp = board[x-1, y-1]
					board.board[x-1][y-1] = 0
					tmp_board = np.vstack((tmp_board, generate_branches(board, x-2, y-2)))
					board.board[x-1][y-1] = tmp_piece_1
					board.board[x][y] = board.board[x-2][y-2]
					board.board[x-2][y-2] = 0
	return tmp_board


def generate_next(board):
	tmp_board = compress(board)
	for i in range(0, 8):
		for j in range(0, 8):
			if (board.board[i][j] !=0):
				if (board.board[i][j].color == WHITE):
					tmp_board = np.vstack((tmp_board, generate_branches(board, i, j)[1:]))
	if (len(tmp_board) > 1):
		return tmp_board[1:]
	for i in range(0, 8):
		for j in range(0, 8):
			tmp_piece = board.board[i][j]
			if (tmp_piece != 0):
				if (tmp_piece.color == WHITE and i < 7):
					if (j < 7):
						if (board.board[i+1][j+1] == 0):
							board.board[i+1][j+1] = tmp_piece
							if (i+1 == 7):
								board.board[i+1][j+1].make_king()
							board.board[i][j] = 0
							tmp_board = np.vstack((tmp_board, compress(board)))
							board.board[i][j] = tmp_piece
							board.board[i+1][j+1] = 0
					if (j > 0):
						if (board.board[i+1][j-1] == 0):
							board.board[i+1][j-1] = tmp_piece
							if (i+1 == 7):
								board.board[i+1][j-1].make_king()
							board.board[i][j] = 0
							tmp_board = np.vstack((tmp_board, compress(board)))
							board.board[i][j] = tmp_piece
							board.board[i+1][j-1] = 0
				if (tmp_piece.king == True and tmp_piece.color == WHITE and i > 0):
					if (j < 7):
						if (board.board[i-1][j+1] == 0):
							board.board[i-1][j+1] = tmp_piece
							board.board[i][j] = 0
							tmp_board = np.vstack((tmp_board, compress(board)))
							board.board[i][j] = board.board[i-1][j+1]
							board.board[i-1][j+1] = 0
					elif (j > 0):
						if (board.board[i-1][j-1] == 0):
							board.board[i-1][j-1] = tmp_piece
							board.board[i][j] = 0
							tmp_board = np.vstack((tmp_board, compress(board)))
							board.board[i][j] = board.board[i-1][j-1]
							board.board[i-1][j-1] = 0
	return tmp_board[1:]

# TODO empty intermediate rows
def possible_moves(board):
	count = 0
	for i in range(0, 8):
		for j in range(0, 8):
			if (board.board[i][j] != 0):
				if (board.board[i][j].color == WHITE):
					count += num_branches(board, i, j)
	if (count > 0):
		return count
	for i in range(0, 8):
		for j in range(0, 8):
			if (board.board[i][j] != 0):
				if (board.board[i][j].color == WHITE and i < 7):
					if (j < 7):
						count += (board.board[i+1][j+1] == 0)
					if (j > 0):
						count += (board.board[i+1][j-1] == 0)
				if (board.board[i][j].king and i > 0):
					if (j < 7):
						count += (board.board[i-1][j+1] == 0)
					elif (j > 0):
						count += (board.board[i-1][j-1] == 0)
     
	return count


def num_branches(board, x, y):
	count = 0
	piece = board.board[x][y]
	if (piece != 0):
		if (piece.color == WHITE and x < 6):
			if (y < 6):
				if (board.board[x+1][y+1] != 0 and board.board[x+1][y+1].color == BLACK and board.board[x+2][y+2] == 0):
					board.board[x+2][y+2] = piece
					board.board[x][y] = 0
					tmp_piece = board.board[x+1][y+1]
					board.board[x+1][y+1] = 0
					count += num_branches(board, x+2, y+2) + 1
					board.board[x+1][y+1] = tmp_piece
					board.board[x][y] = board.board[x+2][y+2]
					board.board[x+2][y+2] = 0
			if (y > 1):
				if (board.board[x+1][y-1] != 0 and board.board[x+1][y-1].color == BLACK and board.board[x+2][y-2] == 0):
					board.board[x+2][y-2] = piece
					board.board[x][y] = 0
					tmp_piece = board.board[x+1][y-1]
					board.board[x+1][y-1] = 0
					count += num_branches(board, x+2, y-2) + 1
					board.board[x+1][y-1] = tmp_piece
					board.board[x][y] = board.board[x+2][y-2]
					board.board[x+2][y-2] = 0
		if (piece.king and piece.color == WHITE and x > 0):
			if (y < 6):
				if (board.board[x-1][y+1] != 0 and board.board[x-1][y+1].color == BLACK and board.board[x-2][y+2] == 0):
					board.board[x-2][y+2] = piece
					board.board[x][y] = 0
					tmp_piece = board.board[x-1][y+1]
					board.board[x-1][y+1] = 0
					count += num_branches(board, x-2, y+2) + 1
					board.board[x-1][y+1] = tmp_piece
					board.board[x][y] = board.board[x-2][y+2]
					board.board[x-2][y+2] = 0
			if (y > 1):
				if (board.board[x-1][y-1] != 0 and board.board[x-1][y-1].color == BLACK and board.board[x-2][y-2] == 0):
					board.board[x-2][y-2] = piece
					board.board[x][y] = 0
					tmp_piece = board.board[x-1][y-1]
					board.board[x-1][y-1] = 0
					count += num_branches(board, x-2, y-2) + 1
					board.board[x-1][y-1] = tmp_piece
					board.board[x][y] = board.board[x-2][y-2]
					board.board[x-2][y-2] = 0
	return count

def capturables(board): # possible number of unsupported enemies
	count = 0
	for i in range(1, 7):
		for j in range(1, 7):
			if (board.board[i][j] != 0 and board.board[i][j].color == BLACK):
				piece = board.board[i+1][j+1]
				tmp_piece1 = board.board[i+1][j-1]
				tmp_piece2 = board.board[i-1][j+1]
				tmp_piece3 = board.board[i-1][j-1]
				count += ((piece != 0 and piece.color == WHITE) and (tmp_piece1 != 0 and tmp_piece1.color == WHITE) and (tmp_piece2 != 0 and tmp_piece2.color == WHITE) and (tmp_piece3 != 0 and tmp_piece3.color == WHITE))
	return count


def semicapturables(board): # number of own units with at least one support
	return (12 - uncapturables(board) - capturables(reverse(board)))


def uncapturables(board): # number of own units that can't be captured
	count = 0
	for i in range(1, 7):
		for j in range(1, 7):
			if (board.board[i][j] != 0 and board.board[i][j].color == WHITE):
				tmp_piece = board.board[i+1][j+1]
				tmp_piece1 = board.board[i+1][j-1]
				tmp_piece2 = board.board[i-1][j+1]
				tmp_piece3 = board.board[i-1][j-1]
				count += ((tmp_piece != 0 and tmp_piece.color == WHITE and tmp_piece1 != 0 and tmp_piece1.color == WHITE) or
              			(tmp_piece2 != 0 and tmp_piece2.color == WHITE and tmp_piece3 != 0 and tmp_piece3.color == WHITE) or
                 		(tmp_piece != 0 and tmp_piece.color == WHITE and tmp_piece2 != 0 and tmp_piece2.color == WHITE) or 
                   		(tmp_piece1 != 0 and tmp_piece1.color == WHITE and  tmp_piece3 != 0 and tmp_piece3.color == WHITE))
	for col in range(0, 8):
		if (board.board[0][col] != 0 and board.board[0][col].color == WHITE):
			count += 1
		if (board.board[0][col] != 0 and board.board[0][col].king and board.board[0][col].color == WHITE):
			count += 1
		if (board.board[7][col] != 0 and board.board[7][col].color == WHITE):
			count += 1
		if (board.board[7][col] != 0 and board.board[7][col].king and board.board[7][col].color == WHITE):
			count += 1
	for row in range(1, 7):
		if (board.board[row][0] != 0 and board.board[row][0].color == WHITE):
			count += 1
		if (board.board[row][0] != 0 and board.board[row][0].king and board.board[row][0].color == WHITE):
			count += 1
		if (board.board[row][7] != 0 and board.board[row][7].color == WHITE):
			count += 1
		if (board.board[row][7] != 0 and board.board[row][7].king and board.board[row][7].color == WHITE):
			count += 1
	return count


def game_winner(board):
	if (board.black_left == 0):
		return 1
	elif (board.white_left == 0):
		return -1
	if (possible_moves(board) == 0):
		return -1
	elif (possible_moves(reverse(board)) == 0):
		return 1
	else:
		return 0


def at_enemy(board):
	count = 0
	for i in range(5, 8):
		for col in range(0, 8):
			if (board.board[i][col] != 0 and board.board[i][col].color == WHITE):
				count += 1
			if (board.board[i][col] != 0 and board.board[i][col].king and board.board[i][col].color == WHITE):
				count += 1
	return count


def at_middle(board):
	count = 0
	for i in range(3, 5):
		for col in range(0, 8):
			if (board.board[i][col] != 0 and board.board[i][col].color == WHITE):
				count += 1
			if (board.board[i][col] != 0 and board.board[i][col].king and board.board[i][col].color == WHITE):
				count += 1
	return count