import os


def silver(lines):
    return 0


def gold(lines):
    return 0


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), 'input'), 'rt').readlines()

    return "DAY 3", silver(lines), gold(lines)
