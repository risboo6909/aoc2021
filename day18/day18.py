from copy import deepcopy

import os
import math

VAL_IDX = 0
POS_IDX = 1

LEFT_IDX = 0
RIGHT_IDX = 1


# enumerate each element with index from left to right
# where left index is the smallest and right index is the largest
# so [[5, 7], 9] => [[(5, 1), (7, 2)], (9, 3)]
def index(input, abs_pos):
    for idx, v in enumerate(input):
        if isinstance(v, list):
            abs_pos = index(v, abs_pos)
        elif isinstance(v, int):
            abs_pos += 1
            input[idx] = (v, abs_pos)
        else:
            abs_pos += 1
            input[idx] = (v[VAL_IDX], abs_pos)

    return abs_pos


def explode(input):

    found = [False]
    replaced = [False]

    def replace(input, target, plain_pos):
        for idx, v in enumerate(input):
            if isinstance(v, list):
                replace(v, target, plain_pos)
            elif v[POS_IDX] == plain_pos:
                input[idx] = (v[VAL_IDX] + target, plain_pos)

    def find(input, left, right, depth):
        if depth == 5 and not found[0]:
            found[0] = True
            # pair is nested inside four pairs, explode!
            return input

        for idx, v in enumerate(input):
            if not isinstance(v, list):
                continue

            left, right = find(v, left, right, depth + 1)
            if left and right and not replaced[0]:
                input[idx], replaced[0] = (0, left[POS_IDX]), True

        return left, right

    index(input, 0)

    left, right = find(input, None, None, 1)
    if left:
        replace(input, left[VAL_IDX], left[POS_IDX] - 1)
    if right:
        replace(input, right[VAL_IDX], right[POS_IDX] + 1)

    return found[0]


def split(input):

    found = [False]

    def rec(input):
        if found[0]:
            return True

        for idx, v in enumerate(input):
            if isinstance(v, list):
                rec(v)
            elif v[VAL_IDX] >= 10 and not found[0]:
                val, pos = v[VAL_IDX], v[POS_IDX]
                input[idx] = [(val // 2, pos), (int(math.ceil((val / 2))), pos)]
                found[0] = True

    rec(input)

    return found[0]


def magnitude(input):
    if isinstance(input[LEFT_IDX], list):
        res1 = magnitude(input[LEFT_IDX])
    else:
        res1 = input[LEFT_IDX][VAL_IDX]

    if isinstance(input[RIGHT_IDX], list):
        res2 = magnitude(input[RIGHT_IDX])
    else:
        res2 = input[RIGHT_IDX][VAL_IDX]

    return 3 * res1 + 2 * res2


def add(left, right):
    tmp = [deepcopy(left)]
    tmp.append(deepcopy(right))
    return tmp


def reduce(expr):
    while True:
        if explode(expr):
            continue
        if not split(expr):
            break

    return expr


def silver(parsed):

    expr = parsed[0]

    for to_add in parsed[1:]:
        expr = add(expr, to_add)
        reduce(expr)

    return magnitude(expr)


def gold(parsed):

    best = 0

    for idx1, first in enumerate(parsed):
        for idx2, second in enumerate(parsed):

            if idx1 == idx2:
                continue

            res = add(first, second)
            reduce(res)

            m = magnitude(res)
            if m > best:
                best = m

    return best


def parse(lines):
    parsed = []
    for line in lines:
        line = line.strip()
        parsed.append(eval(line))

    return parsed


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()
    parsed = parse(lines)

    return "DAY18", silver(parsed), gold(parsed)
