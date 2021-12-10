import os
from result import Ok, Err, Result
from typing import List, Tuple


pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def process(line: str) -> Result[List[str], str]:
    q: List[str] = []

    for s in line:
        if s in pairs.values():
            if q and pairs[q[-1]] != s:
                # error found
                return Err(s)
            q.pop()
        else:
            q.append(s)

    return Ok(q)


def silver(lines: List[str]) -> int:

    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    points = 0

    for line in lines:
        s = process(line.strip())
        if isinstance(s, Err):
            points += scores[s.value]

    return points


def gold(lines: List[str]) -> int:

    scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    all_points = []

    for line in lines:

        points = 0
        q = process(line.strip())

        if isinstance(q, Ok):
            # restore missing symbols
            while q.value:
                points = points * 5 + scores[pairs[q.value.pop()]]

            all_points.append(points)

    middle_point_idx = int(0.5 * len(all_points))
    return sorted(all_points)[middle_point_idx]


def solve() -> Tuple[str, int, int]:
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    return "DAY 10", silver(lines), gold(lines)
