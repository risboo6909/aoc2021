import os


pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def process(line):
    q = []

    for s in line:
        if s in pairs.values():
            if q and pairs[q[-1]] != s:
                # error found
                return s, "error"
            q.pop()
        else:
            q.append(s)

    return q, None


def silver(lines):

    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    points = 0

    for line in lines:
        s, err = process(line.strip())
        if err == "error":
            points += scores[s]

    return points


def gold(lines):

    scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    all_points = []

    for line in lines:

        points = 0
        q, err = process(line.strip())

        if err is None:
            # restore missing symbols
            while q:
                points = points * 5 + scores[pairs[q.pop()]]

            all_points.append(points)

    middle_point_idx = int(0.5 * len(all_points))
    return sorted(all_points)[middle_point_idx]


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    return "DAY 10", silver(lines), gold(lines)
