from collections import defaultdict

import heapq
import os


def generate_nodes_and_weights(table):
    nodes = defaultdict(set)
    weights = dict()

    for row_idx, row in enumerate(table):
        for col_idx, weight in enumerate(row):
            weights[(row_idx, col_idx)] = weight
            if col_idx > 0:
                nodes[(row_idx, col_idx)].add((row_idx, col_idx - 1))
            if col_idx < len(row) - 1:
                nodes[(row_idx, col_idx)].add((row_idx, col_idx + 1))
            if row_idx > 0:
                nodes[(row_idx, col_idx)].add((row_idx - 1, col_idx))
            if row_idx < len(table) - 1:
                nodes[(row_idx, col_idx)].add((row_idx + 1, col_idx))

    return nodes, weights


def dijkstra(nodes, weights):

    start_point = (0, 0)

    to_visit = []

    visited = set([start_point])
    path_weights = {start_point: 0}

    cur_node = start_point

    heapq.heappush(to_visit, (weights[start_point], *start_point))

    while to_visit:

        for dst_node in nodes[cur_node]:

            if dst_node not in visited:
                path_weight = weights[dst_node] + path_weights[cur_node]

                if dst_node not in path_weights:
                    path_weights[dst_node] = path_weight
                elif path_weight < path_weights[dst_node]:
                    path_weights[dst_node] = path_weight

                heapq.heappush(to_visit, (path_weights[dst_node], *dst_node))

        while to_visit and cur_node in visited:
            _, row, col = heapq.heappop(to_visit)
            cur_node = (row, col)

        visited.add(cur_node)

    return path_weights


def silver_and_gold(table):
    path_weights = dijkstra(*generate_nodes_and_weights(table))
    (_, _), weight = sorted(path_weights.items())[-1]
    return weight


def inc(n):
    return 1 + n % 9


def parse(lines):

    table = []

    for row_idx, line in enumerate(lines):
        row = []
        for col_idx, weight in enumerate(list(line.strip())):
            row.append(int(weight))
        table.append(row)

    # extend map assuming our current map is just one tile of 5x5 grid
    table_big = [[0 for _ in range(len(table[0]) * 5)] for _ in range(len(table) * 5)]

    src_table_rows = len(table)
    src_table_cols = len(table[0])

    for row_idx, row in enumerate(table_big):
        for col_idx, _ in enumerate(row):

            if row_idx < src_table_rows and col_idx < src_table_cols:
                new_weight = table[row_idx][col_idx]
            else:
                if row_idx >= src_table_rows and col_idx >= src_table_cols:
                    new_weight = max(
                        inc(table_big[row_idx - src_table_rows][col_idx]),
                        inc(table_big[row_idx][col_idx - src_table_cols]),
                    )
                elif row_idx >= src_table_rows:
                    new_weight = inc(table_big[row_idx - src_table_rows][col_idx])
                else:
                    new_weight = inc(table_big[row_idx][col_idx - src_table_cols])

            table_big[row_idx][col_idx] = new_weight

    return table, table_big


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()
    table, table_big = parse(lines)

    return "DAY15", silver_and_gold(table), silver_and_gold(table_big)
