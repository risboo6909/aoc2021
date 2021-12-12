import builtins
import os
from collections import defaultdict
from functools import partial

peq = partial(int.__eq__, 2)


def dfs(nodes, cur_node, freq, twice):
    if cur_node == "end":
        return 1

    if cur_node.islower():

        if freq[cur_node] > 0:
            if not twice:
                # can't visit small caves more than once
                return 0
            elif cur_node == "start" or any(map(peq, freq.values())):
                return 0

        freq[cur_node] += 1

    total_paths = 0

    for dest_node in nodes[cur_node]:
        total_paths += dfs(nodes, dest_node, freq, twice)

    if cur_node.islower() and freq[cur_node] > 0:
        freq[cur_node] -= 1

    return total_paths


def silver(nodes):
    return dfs(nodes, "start", defaultdict(int), twice=False)


def gold(nodes):
    return dfs(nodes, "start", defaultdict(int), twice=True)


def parse(lines):
    nodes = defaultdict(list)

    for line in lines:
        from_node, to_node = line.strip().split("-")
        nodes[from_node].append(to_node)
        nodes[to_node].append(from_node)

    return nodes


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    nodes = parse(lines)

    return "DAY 12", silver(nodes), gold(nodes)
