import os


def silver(lines):
    prev_depth = None
    result = 0

    for line in lines:
        depth = int(line)
        if prev_depth is not None:
            if depth > prev_depth:
                result += 1
        prev_depth = depth

    return result


def gold(lines):
    prev_sum_depth = None
    result = 0
    window = []

    for line in lines:
        depth = int(line)
        window.append(depth)

        if len(window) == 3:

            sum_depth = sum(window)
            if prev_sum_depth is not None and sum_depth > prev_sum_depth:
                result += 1

            prev_sum_depth = sum_depth
            window = window[1:]

    return result


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), 'input'), 'rt').readlines()

    print(silver(lines))
    print(gold(lines))
