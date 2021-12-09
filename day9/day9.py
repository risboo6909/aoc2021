import os
import numpy as np
from functools import reduce
from typing import List

BASIN_BORDER = 9


def directions(board, row_idx, col_idx):
    if row_idx > 0:
        yield (-1, 0)
    if col_idx > 0:
        yield (0, -1)
    if row_idx < board.shape[0] - 1:
        yield (1, 0)
    if col_idx < board.shape[1] - 1:
        yield (0, 1)


def min_neighbour(board, row_idx, col_idx):
    res = []

    for dir in directions(board, row_idx, col_idx):
        res.append(board[row_idx + dir[0], col_idx + dir[1]])

    return min(res)


def find_mins(board):
    min_points = {}

    for row_idx in range(board.shape[0]):
        for col_idx in range(board.shape[1]):
            cur_val = board[row_idx, col_idx]
            vicinity_min = min_neighbour(board, row_idx, col_idx)

            if vicinity_min > cur_val:
                min_points[(row_idx, col_idx)] = cur_val

    return min_points


def silver(min_points):
    return 1 + reduce(lambda x, y: x + y + 1, min_points)


def rec(board, visited, row_idx, col_idx):
    if board[row_idx, col_idx] == BASIN_BORDER:
        return 0

    if (row_idx, col_idx) in visited:
        return 0

    visited.add((row_idx, col_idx))

    res = 1
    for vec in directions(board, row_idx, col_idx):
        res += rec(board, visited, row_idx + vec[0], col_idx + vec[1])

    return res


def gold(board, min_points):
    # find largest basin
    basins = []
    for row_idx, col_idx in min_points.keys():
        basins.append(rec(board, set(), row_idx, col_idx))
    return np.prod(sorted(basins, reverse=True)[:3])


def parse(lines: List[str]):
    rows = []
    for line in lines:
        row = []
        for digit in line.strip():
            row.append(int(digit))
        rows.append(row)

    return np.array(rows, np.int)


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    board = parse(lines)
    min_points = find_mins(board)

    return "DAY 9", silver(min_points.values()), gold(board, min_points)
