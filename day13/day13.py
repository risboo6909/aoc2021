import os
from collections import namedtuple

Fold = namedtuple("Fold", "axis pos")

OCCUPIED = 1


class Board(object):
    def __init__(self):
        self.__board = {}
        self.__max_row = 0
        self.__max_col = 0

    def __str__(self):
        res = []

        for row_idx in range(self.__max_row + 1):
            col = []
            for col_idx in range(self.__max_col + 1):
                if (row_idx, col_idx) in self.__board:
                    col.append("#")
                else:
                    col.append(".")
            res.append(col)

        return "\n".join(["".join([cell for cell in row]) for row in res])

    def clone_empty(self):
        tmp = Board()
        tmp.set_max_col(self.get_max_col())
        tmp.set_max_row(self.get_max_row())
        return tmp

    def add_point(self, row, col):
        self.__board[(row, col)] = OCCUPIED

        self.__max_row = max(row, self.__max_row)
        self.__max_col = max(col, self.__max_col)

    def get_cells_gt(self, margin, axis):
        for (row, col) in self.__board.keys():
            if axis == "x":
                if col > margin and self.__board[(row, col)] == OCCUPIED:
                    yield (row, col)
            else:
                if row > margin and self.__board[(row, col)] == OCCUPIED:
                    yield (row, col)

    def get_cells_lt(self, margin, axis):
        for (row, col) in self.__board.keys():
            if axis == "x":
                if col <= margin and self.__board[(row, col)] == OCCUPIED:
                    yield (row, col)
            else:
                if row <= margin and self.__board[(row, col)] == OCCUPIED:
                    yield (row, col)

    def num_visible(self):
        return sum(self.__board.values())

    def get_max_row(self):
        return self.__max_row

    def get_max_col(self):
        return self.__max_col

    def set_max_col(self, max_col):
        self.__max_col = max_col

    def set_max_row(self, max_row):
        self.__max_row = max_row


def apply_fold(board, fold):
    new_board = board.clone_empty()

    for cell in board.get_cells_gt(fold.pos, fold.axis):
        if fold.axis == "x":
            new_board.add_point(cell[0], board.get_max_col() - cell[1])
        else:
            new_board.add_point(board.get_max_row() - cell[0], cell[1])

    for cell in board.get_cells_lt(fold.pos, fold.axis):
        new_board.add_point(*cell)

    # shrink down the board
    if fold.axis == "y":
        new_board.set_max_row(fold.pos - 1)
    else:
        new_board.set_max_col(fold.pos - 1)

    return new_board


def silver(board, folds):
    board = apply_fold(board, folds[0])
    return board.num_visible()


def gold(board, folds):
    for fold in folds:
        board = apply_fold(board, fold)
    return "\n{}".format(board)


def parse(lines):
    board = Board()
    folds = []

    for line in lines:
        line = line.strip()

        if line == "":
            continue
        elif line.startswith("fold"):
            axis, pos = line.rsplit(None, 1)[1].split("=")
            folds.append(Fold(axis=axis, pos=int(pos)))
        else:
            col, row = line.split(",")
            board.add_point(int(row), int(col))

    return board, folds


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    board, folds = parse(lines)

    return "DAY 13", silver(board, folds), gold(board, folds)
