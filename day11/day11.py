from typing import List
import os

EMPTY_OCTO = 0
FULL_OCTO = 10


class Board(object):
    def __init__(self):
        self.__board = []
        self.total_flashes = 0

    def __str__(self):
        return "\n".join(
            [" ".join([str(cell) for cell in row]) for row in self.__board]
        )

    def add_row(self, row: List[int]):
        self.__board.append(row)

    def is_all_zeros(self):
        return all(all(cell == 0 for cell in row) for row in self.__board)

    def inc_energy(self, row_idx, col_idx, count_zeros):
        if row_idx < 0 or row_idx >= len(self.__board):
            return

        if col_idx < 0 or col_idx >= len(self.__board[0]):
            return

        if not count_zeros and self.__board[row_idx][col_idx] == EMPTY_OCTO:
            return

        self.__board[row_idx][col_idx] = min(
            self.__board[row_idx][col_idx] + 1, FULL_OCTO
        )

    def charge_vicinity(self, row_idx, col_idx):
        # charge neighbours
        for dy in [-1, 0, +1]:
            for dx in [-1, 0, +1]:
                if dy == dx == 0:
                    continue
                self.inc_energy(row_idx + dy, col_idx + dx, count_zeros=False)

    def step(self):
        # 1. Inc energy for each octopus by 1
        for row_idx in range(len(self.__board)):
            for col_idx in range(len(self.__board[row_idx])):
                self.inc_energy(row_idx, col_idx, count_zeros=True)

        # 2. Flash octopuses
        while True:

            must_flash = set()

            for row_idx in range(len(self.__board)):
                for col_idx in range(len(self.__board[row_idx])):

                    if self.__board[row_idx][col_idx] != FULL_OCTO:
                        continue

                    must_flash.add((row_idx, col_idx))
                    self.__board[row_idx][col_idx] = EMPTY_OCTO

            if not must_flash:
                break

            self.total_flashes += len(must_flash)

            for coords in must_flash:
                self.charge_vicinity(*coords)


def silver(board: Board):
    for _ in range(100):
        board.step()
    return board.total_flashes


def gold(board: Board):
    step = 1

    while True:
        board.step()
        if board.is_all_zeros():
            break
        step += 1

    return step


def parse(lines: List[str]):
    board = Board()
    for line in lines:
        board.add_row(list(map(int, line.strip())))

    return board


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    return "DAY 11", silver(parse(lines)), gold(parse(lines))
