import os
from typing import List


def bin_to_int(bits: List[int]) -> int:
    res, pow = 0, 1
    for bit in reversed(bits):
        res += pow * bit
        pow <<= 1

    return res


def silver(lines: List[str]) -> int:
    zeros_freq = [0] * (len(lines[0])-1)
    ones_freq = [0] * (len(lines[0])-1)

    for line in lines:
        for (i, bit) in enumerate(line.strip()):
            if bit == '0':
                zeros_freq[i] += 1
            else:
                ones_freq[i] += 1

    gamma_bin = []
    epsilon_bin = []

    for i in range(len(zeros_freq)):
        if zeros_freq[i] >= ones_freq[i]:
            gamma_bin.append(0)
            epsilon_bin.append(1)
        else:
            gamma_bin.append(1)
            epsilon_bin.append(0)

    gamma = bin_to_int(gamma_bin)
    epsilon = bin_to_int(epsilon_bin)

    return gamma * epsilon


def gold(lines: List[str]) -> int:
    return 0


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), 'input'), 'rt').readlines()

    return "DAY 3", silver(lines), gold(lines)
