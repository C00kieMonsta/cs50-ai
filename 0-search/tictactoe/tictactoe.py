"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return winner(board)

    flat_board = [item for sublist in board for item in sublist]
    
    # check if all none values
    if all(v is EMPTY for v in flat_board):
        return X
    
    xs = [item for item in flat_board if item == X]
    os = [item for item in flat_board if item == O]

    # check based on length of lists
    if len(xs) > len(os):
        return O
    else:
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                actions.append((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception('Action is not valid')

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # check rows
    board_t = [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]

    # check diagonals
    diagonals = [
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]

    all_combinations = board + board_t + diagonals
    for row in all_combinations:    
        if all(item is row[0] for item in row):
            return row[0]
        
    return EMPTY


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    flat_board = [item for sublist in board for item in sublist]
    if winner(board) is not EMPTY or EMPTY not in flat_board:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    X is Max player
    O is Min player
    """

    if player(board) == X: # X must maximise
        v = -math.inf
        for action in actions(board):
            tmp = min_value(result(board, action))
            if tmp > v:
                v = tmp
                opt_action = action

    else: # O must minimize score
        v = math.inf
        for action in actions(board):
            tmp = max_value(result(board, action))
            if tmp < v:
                v = tmp
                opt_action = action
    
    return opt_action

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
    
