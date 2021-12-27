import os
from collections import namedtuple

Range = namedtuple("Range", "start end")


def simulate(v_x, v_y, x_range, y_range):
    cur_x = cur_y = 0
    highest_y = 0

    while cur_y >= y_range.start and cur_x <= x_range.end:

        if cur_x >= x_range.start and cur_x <= x_range.end:
            if cur_y >= y_range.start and cur_y <= y_range.end:
                return highest_y

        cur_x += v_x
        cur_y += v_y

        if v_x > 0:
            v_x -= 1

        v_y -= 1
        if v_y < 0 and highest_y == 0:
            highest_y = cur_y

    return None


def find_initials(x_range, y_range):
    for vx in range(x_range.end):
        if 0.5 * vx * (vx + 1) < x_range.start:
            continue
        min_vx = vx
        break

    for vy in range(abs(y_range.start)):
        if 0.5 * vy * (vy + 1) < abs(y_range.end):
            continue
        min_vy = vy
        break

    return min_vx, min_vy


def silver(x_range, y_range):
    min_vx, min_vy = find_initials(x_range, y_range)

    highest_y = None

    for v_x in range(min_vx, x_range.end + 1):
        for v_y in range(min_vy, abs(y_range.start)):
            tmp = simulate(v_x, v_y, x_range, y_range)
            if tmp is not None:
                highest_y = tmp

    return highest_y


def gold(x_range, y_range):
    min_vx, _ = find_initials(x_range, y_range)

    cnt = 0

    for v_x in range(min_vx, x_range.end + 1):
        for v_y in range(y_range.start, abs(y_range.start)):
            tmp = simulate(v_x, v_y, x_range, y_range)
            if tmp is not None:
                cnt += 1

    return cnt


def parse_range(range_raw):
    # parses raw range, for example: x=20..30
    _, range = range_raw.split("=")
    start, end = range.split("..")
    return Range(start=int(start), end=int(end))


def parse(lines):
    line = lines[0]
    _, _, x_range_raw, y_range_raw = line.strip().replace(",", "").split()
    x_range = parse_range(x_range_raw)
    y_range = parse_range(y_range_raw)
    return x_range, y_range


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()
    x_range, y_range = parse(lines)
    return "DAY17", silver(x_range, y_range), gold(x_range, y_range)
