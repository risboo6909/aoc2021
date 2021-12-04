import os
from collections import defaultdict
from typing import List

MATCH_LEN = 5


class Board(object):
    def __init__(self):
        self.__cols_counter = defaultdict(int)
        self.__rows_counter = defaultdict(int)

        self.__cur_row = 0
        self.__numbers_to_coords = {}
        self.__coords_to_numbers = {}

        self.__marked_pos = set()

    def add_row(self, row):
        for col, num in enumerate(row):
            self.__numbers_to_coords[num] = (self.__cur_row, col)
            self.__coords_to_numbers[(self.__cur_row, col)] = num
        self.__cur_row += 1

    def has_number(self, n):
        return n in self.__numbers_to_coords

    def get_number_pos(self, n):
        return self.__numbers_to_coords[n]

    def get_unmarked(self):
        unmarked = set()
        for pos in self.__coords_to_numbers:
            if pos not in self.__marked_pos:
                unmarked.add(self.__coords_to_numbers[pos])
        return unmarked

    def inc_counters(self, n: int) -> bool:
        row, col = self.get_number_pos(n)
        self.__marked_pos.add((row, col))

        self.__rows_counter[row] += 1
        if self.__rows_counter[row] == MATCH_LEN:
            return True

        self.__cols_counter[col] += 1
        if self.__cols_counter[col] == MATCH_LEN:
            return True

        return False

    def __str__(self):
        board = []
        for row in range(MATCH_LEN):
            line = []
            for col in range(MATCH_LEN):
                n = self.__coords_to_numbers.get((row, col), None)
                if n is not None:
                    line.append(str(n))
            board.append(" ".join(line))

        return "\n".join(board)


def silver(seq, boards):
    for n in seq:
        for board in boards:
            if not board.has_number(n):
                continue
            if board.inc_counters(n):
                # we've found the winner
                return sum(board.get_unmarked()) * n


def gold(seq, boards):
    winning_boards = []
    last_n = 0

    for n in seq:
        for board in boards:
            if board in winning_boards:
                continue

            if not board.has_number(n):
                continue

            if board.inc_counters(n):
                winning_boards.append(board)
                last_n = n

    last_winner = winning_boards[-1]
    return sum(last_winner.get_unmarked()) * last_n


def parse(lines: List[str]):
    cur_board = None
    boards = []
    sequence = []

    for line in lines:
        line = line.strip()
        if line == "":
            cur_board = Board()
            boards.append(cur_board)
        elif "," in line:
            # parse sequence
            sequence.extend(map(int, line.split(",")))
        else:
            # parse board
            cur_board.add_row(map(int, line.split()))

    return sequence, boards


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    return "DAY 4", silver(*parse(lines)), gold(*parse(lines))
