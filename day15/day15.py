from collections import defaultdict
from copy import deepcopy

import heapq
import os

def dijkstra(nodes, weights):

    weights = deepcopy(weights)

    start_point = (0, 0)

    to_visit = []
    
    visited = {start_point: weights[start_point]}
    cur_node = start_point

    heapq.heappush(to_visit, start_point)

    while to_visit:
        cur_node = heapq.heappop(to_visit)

        for node in nodes[cur_node]:
            if node in visited:
                continue
            heapq.heappush(to_visit, node)

        if to_visit:
            print(to_visit)
            dst_node = heapq.heappop(to_visit)
            path_weight = weights[dst_node] + weights[cur_node]

            if dst_node not in visited:
                visited[dst_node] = path_weight
            elif path_weight < visited[dst_node]:
                visited[dst_node] = path_weight

    print(visited)

def silver(nodes, weights):
    dijkstra(nodes, weights)
    

def gold(nodes, weights):
    pass

def parse(lines):
    nodes = defaultdict(set)
    weights = dict()
    table = []
    
    for row_idx, line in enumerate(lines):
        row = []
        for col_idx, weight in enumerate(list(line.strip())):
            weights[(row_idx, col_idx)] = int(weight)
            row.append(int(weight))
        table.append(row)

    for row_idx, row in enumerate(table):
        for col_idx, _ in enumerate(row):
            if col_idx > 0:
                nodes[(row_idx, col_idx)].add((row_idx, col_idx-1))
            if col_idx < len(row)-1:
                nodes[(row_idx, col_idx)].add((row_idx, col_idx+1))
            if row_idx > 0:
                nodes[(row_idx, col_idx)].add((row_idx-1, col_idx))
            if row_idx < len(table)-1:
                nodes[(row_idx, col_idx)].add((row_idx+1, col_idx))

    return nodes, weights

def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()
    nodes, weights = parse(lines)
    return "DAY15", silver(nodes, weights), gold(nodes, weights)
