import os
from typing import List, Tuple, Callable


def bin_to_dec(bits: List[int]) -> int:
    res, base = 0, 1
    for bit in reversed(bits):
        res += base * bit
        base <<= 1

    return res


def compute_freq(items: List[str]) -> Tuple[List[int], List[int]]:
    zeros_freq = [0] * (len(items[0]) - 1)
    ones_freq = [0] * (len(items[0]) - 1)

    for item in items:
        for (i, bit) in enumerate(item.strip()):
            if bit == "0":
                zeros_freq[i] += 1
            else:
                ones_freq[i] += 1
    return zeros_freq, ones_freq


def silver(lines: List[str]) -> int:

    zeros_freq, ones_freq = compute_freq(lines)

    gamma_bin = []
    epsilon_bin = []

    for i in range(len(zeros_freq)):
        if zeros_freq[i] >= ones_freq[i]:
            gamma_bin.append(0)
            epsilon_bin.append(1)
        else:
            gamma_bin.append(1)
            epsilon_bin.append(0)

    gamma = bin_to_dec(gamma_bin)
    epsilon = bin_to_dec(epsilon_bin)

    return gamma * epsilon


def rec(
    lines: List[str],
    pred: Callable[[List[str], List[int], List[int], int], List[str]],
    pos: int,
) -> List[int]:
    if len(lines) == 1:
        return list(map(int, lines[0].strip()))

    zeros_freq, ones_freq = compute_freq(lines)
    filtered = pred(lines, zeros_freq[pos], ones_freq[pos], pos)

    return rec(filtered, pred, pos + 1)


def oxygen(lines: List[str], zeros: List[int], ones: List[int], pos: int) -> List[str]:
    if ones >= zeros:
        return list(filter(lambda item: item[pos] == "1", lines))

    return list(filter(lambda item: item[pos] == "0", lines))


def co2(lines: List[str], zeros: List[int], ones: List[int], pos: int) -> List[str]:
    if zeros > ones:
        return list(filter(lambda item: item[pos] == "1", lines))

    return list(filter(lambda item: item[pos] == "0", lines))


def gold(lines: List[str]):
    return bin_to_dec(rec(lines, oxygen, 0)) * bin_to_dec(rec(lines, co2, 0))


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    return "DAY 3", silver(lines), gold(lines)
