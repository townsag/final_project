import numpy as np
from numpy import ndarray

def has_open_space(board: ndarray[int, ...]) -> bool:
    return np.any(board == 0)


def is_valid_move(board: ndarray[int, ...], direction: int) -> bool:
    new_matrix, _ = make_move(board, 0, direction)
    return not np.array_equal(new_matrix, board)


def has_valid_move(board: ndarray[int, ...]) -> bool:
    return any(is_valid_move(board, direction) for direction in range(4))


def add_value(board: ndarray[int, ...]) -> ndarray[int, ...]:
    # make a list of all the empty spaces in the
    empty_spaces = list(zip(np.where(board == 0)[0], np.where(board == 0)[1]))
    # empty_spaces = np.argwhere(board == 0)
    random_index = np.random.choice(len(empty_spaces))
    new_board = board.copy()
    new_board[empty_spaces[random_index]] = np.random.choice([2, 4], p=[2 / 3, 1 / 3])
    return new_board


def make_move(board: ndarray[int, ...], current_score: int, direction: int) ->\
        tuple[ndarray[int, ...], int]:
    # 0: up, 1: right, 2: down, 3: left
    new_board = np.copy(board)
    new_board = np.rot90(new_board, k=direction)
    shifted_board = shift(new_board)
    joined_board, score_change = join(shifted_board)
    return_board = np.rot90(joined_board, k=(4 - direction))
    return return_board, current_score + score_change


def shift(board: ndarray[int, ...]) -> ndarray[int, ...]:
    new_board = np.copy(board)
    for column in range(board.shape[1]):
        top_row = 0  # stores the row of the highest zero element
        for row in range(board.shape[0]):
            if new_board[row, column] != 0:
                new_board[(top_row, row), (column, column)] = \
                    new_board[(row, top_row), (column, column)]
                top_row += 1
    return new_board


def join(board: ndarray[int, ...]) -> tuple[ndarray[int, ...], int]:
    new_board = np.copy(board)
    score_change = 0
    for column in range(board.shape[1]):
        for row in range(board.shape[0] - 1):
            if new_board[row, column] == new_board[row + 1, column] and \
                    new_board[row, column] != 0:
                new_board[row, column] += new_board[row + 1, column]
                score_change += new_board[row, column]
                new_board[row + 1, column] = 0
                new_board[(row + 1):, column] = \
                    np.roll(new_board[(row + 1):, column], -1)
    return new_board, score_change
