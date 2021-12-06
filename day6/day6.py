import os

DAYS_TO_BORN = 6
DAYS_TO_BORN_NEW = 8


def solve_both(species, num_days):
    gen = [0] * (DAYS_TO_BORN_NEW+1)

    for age in species:
        gen[age] += 1

    while num_days > 0:
        next_gen = [0] * (DAYS_TO_BORN_NEW+1)
        for age, cnt in enumerate(gen):
            if age > 0:
                next_gen[age - 1] += cnt
            else:
                next_gen[DAYS_TO_BORN] += cnt
                next_gen[DAYS_TO_BORN_NEW] += cnt

        gen = next_gen
        num_days -= 1

    return sum(gen)


def parse(lines):
    res = []
    for line in lines:
        res.extend(map(int, line.strip().split(",")))
    return res


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), "input"), "rt").readlines()

    numbers = parse(lines)

    return "DAY 6", solve_both(numbers, 80), solve_both(numbers, 256)
