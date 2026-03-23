"""
Tic Tac Toe Player
"""


import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x = sum(row.count(X) for row in board)
    o = sum(row.count(O) for row in board)
    return X if x == o else O


def actions(board):
    return {(i, j)
            for i in range(3)
            for j in range(3)
            if board[i][j] == EMPTY}


def result(board, action):
    i, j = action
    if board[i][j] is not EMPTY:
        raise Exception("Invalid move")

    new = deepcopy(board)
    new[i][j] = player(board)
    return new


def winner(board):
    lines = []

    # Rows and columns
    for i in range(3):
        lines.append(board[i])
        lines.append([board[0][i], board[1][i], board[2][i]])

    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line == [X, X, X]:
            return X
        if line == [O, O, O]:
            return O

    return None


def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    if terminal(board):
        return None

    turn = player(board)

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

    best_action = None

    if turn == X:
        best = -math.inf
        for action in actions(board):
            val = min_value(result(board, action))
            if val > best:
                best = val
                best_action = action
    else:
        best = math.inf
        for action in actions(board):
            val = max_value(result(board, action))
            if val < best:
                best = val
                best_action = action

    return best_action

