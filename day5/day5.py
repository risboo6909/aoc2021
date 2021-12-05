import os
from typing import List
from collections import namedtuple, defaultdict

Point = namedtuple("Point", "x, y")
Line = namedtuple("Line", "x1, y1, x2, y2")


def gen_points(line: Line):

    mov_x = line.x2 - line.x1
    mov_y = line.y2 - line.y1

    mag_x = max(abs(mov_x), 1)
    mag_y = max(abs(mov_y), 1)

    direction = (int(mov_x / mag_x), int(mov_y / mag_y))

    x, y = line.x1, line.y1

    while x != line.x2 or y != line.y2:
        yield Point(x=x, y=y)
        x += direction[0]
        y += direction[1]

    yield Point(x=x, y=y)


def is_diag(line: Line) -> bool:
    return line.x1 != line.x2 and line.y1 != line.y2


def silver(lines: List[Line]) -> int:
    field = defaultdict(int)
    for line in lines:

        if is_diag(line):
            continue

        for point in gen_points(line):
            field[point] += 1

    return sum(map(lambda cnt: 1 if cnt > 1 else 0, field.values()))


def gold(lines: List[Line]) -> int:
    field = defaultdict(int)
    for line in lines:
        for point in gen_points(line):
            field[point] += 1

    return sum(map(lambda cnt: 1 if cnt > 1 else 0, field.values()))


def parse_point(point_str: str) -> Point:
    x, y = point_str.strip().split(",")
    return Point(x=int(x), y=int(y))


def parse(lines: List[str]) -> List[Line]:
    res = []
    for line in lines:

        line.replace(" ", "")
        from_point, to_point = line.strip().split("->")

        from_parsed = parse_point(from_point)
        to_parsed = parse_point(to_point)

        res.append(
            Line(x1=from_parsed.x, y1=from_parsed.y, x2=to_parsed.x, y2=to_parsed.y)
        )
    return res


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    parsed = parse(lines)

    return "DAY 5", silver(parsed), gold(parsed)
