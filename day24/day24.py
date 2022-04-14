import os


def silver(parsed):
    pass


def gold(parsed):
    pass


def parse(lines):
    parsed = lines
    return parsed


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), "input"), "rt").readlines()

    parsed = parse(lines)

    return "DAY24", silver(parsed), gold(parsed)
