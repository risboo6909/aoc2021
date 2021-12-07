from typing import List
import os


def compute_sum(n: int) -> int:
    return int(0.5 * n * (n + 1))


def compute_total_dist(x, coords: List[int], weighted: bool) -> int:
    dist = 0
    for c in coords:
        if weighted:
            n = abs(x - c)
            dist += compute_sum(n)
        else:
            dist += abs(x - c)
    return dist


def compute_fuel(coords: List[int], weighted: bool) -> int:
    coords = sorted(coords)
    prev_fuel = cur_fuel = None
    for idx in range(coords[0], coords[-1]):
        cur_fuel = compute_total_dist(idx, coords, weighted)
        if prev_fuel and cur_fuel >= prev_fuel:
            return prev_fuel
        prev_fuel = cur_fuel


def silver(coords: List[int]) -> int:
    return compute_fuel(coords, weighted=False)


def gold(coords: List[int]) -> int:
    return compute_fuel(coords, weighted=True)


def parse(lines: List[str]) -> List[int]:
    res = []
    for line in lines:
        res.extend(map(int, line.strip().split(",")))
    return res


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    coords = parse(lines)

    return "DAY 7", silver(coords), gold(coords)
