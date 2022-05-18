import os


class Board(object):
    def __init__(self):
        self.board = []

    def __convert_coords(self, row, col):
        rows = len(self.board)
        cols = len(self.board[0])

        if row < 0:
            row = rows - 1
        elif row > rows - 1:
            row = 0

        if col < 0:
            col = cols - 1
        elif col > cols - 1:
            col = 0

        return row, col

    def move_right(self, new_board, row_idx, col_idx):
        to_row, to_col = self.__convert_coords(row_idx, col_idx + 1)
        if self.board[to_row][to_col] == ".":
            new_board[to_row][to_col] = ">"
            return True

        new_board[row_idx][col_idx] = self.board[row_idx][col_idx]
        return False

    def move_down(self, new_board, row_idx, col_idx):
        to_row, to_col = self.__convert_coords(row_idx + 1, col_idx)
        if new_board[to_row][to_col] == "." and self.board[to_row][to_col] != "v":
            new_board[to_row][to_col] = "v"
            return True

        new_board[row_idx][col_idx] = self.board[row_idx][col_idx]
        return False

    def simulation_step(self):
        new_board = []
        for row in self.board:
            new_board.append(["." for _ in row])

        critter_moved = False

        for row_idx, row in enumerate(self.board):
            for col_idx, _ in enumerate(row):
                if self.board[row_idx][col_idx] == ">":
                    critter_moved |= self.move_right(new_board, row_idx, col_idx)

        for row_idx, row in enumerate(self.board):
            for col_idx, _ in enumerate(row):
                if self.board[row_idx][col_idx] == "v":
                    critter_moved |= self.move_down(new_board, row_idx, col_idx)

        self.board = new_board

        return critter_moved

    def add_row(self, row):
        self.board.append([p for p in row])

    def __str__(self):
        res = ""
        for row in self.board:
            res += "".join(row)
            res += "\n"
        return res


def silver(board):
    step = 1
    while True:
        if not board.simulation_step():
            return step
        step += 1


def gold(board):
    # not required!
    pass


def parse(lines):
    board = Board()
    for line in lines:
        board.add_row(line.strip())
    return board


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    board = parse(lines)

    return "DAY25", silver(board), gold(board)
