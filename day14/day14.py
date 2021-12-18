from collections import Counter, defaultdict

import os


def accumulate(cache, acc, st, end, depth):
    cache.update(acc)
    for (_, _, d), counters in acc.items():
        if d + 1 == depth:
            cache[(st, end, depth)].update(counters)


def solve_rec(st, end, table, global_cache, scores, depth):
    key = (st, end, depth)

    if depth == 0:
        return defaultdict(Counter)

    counter = global_cache.get(key)
    if counter:
        scores.update(counter)
        return {key: counter}

    cache = defaultdict(Counter)

    # consider an example: 'NN', if we insert 'B' between two 'N' we get 'NBN'

    # this will be equal to 'B' (the thing we are inserting between 'N.N')
    to_insert = table[(st, end)]

    # first traverse left 'NB'
    acc_left = solve_rec(st, to_insert, table, global_cache, scores, depth - 1)
    accumulate(cache, acc_left, st, end, depth)

    # second traverse right 'BN'
    acc_right = solve_rec(to_insert, end, table, global_cache, scores, depth - 1)
    accumulate(cache, acc_right, st, end, depth)

    # partial caches for nodes
    cache[key][to_insert] += 1

    # plain dict for convenient quantities computation
    scores[to_insert] += 1

    for key, counters in cache.items():
        for inserted, count in counters.items():
            global_cache[key].setdefault(inserted, count)

    return cache


def find_maxmin_delta(sequence, table, iterations):
    scores = Counter()
    global_cache = defaultdict(Counter)

    for st, end in zip(sequence, sequence[1:]):
        solve_rec(st, end, table, global_cache, scores, iterations)

    for s in sequence:
        scores[s] += 1

    return max(scores.values()) - min(scores.values())


def silver(init, table):
    return find_maxmin_delta(init, table, 10)


def gold(init, table):
    return find_maxmin_delta(init, table, 40)


def parse(lines):
    table = {}
    initial = list(lines[0].strip())

    # read transformation rules
    for line in lines[2:]:
        left, right = line.strip().split(" -> ")
        table[(left[0], left[1])] = right

    return initial, table


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()
    initial, table = parse(lines)

    return "DAY14", silver(initial, table), gold(initial, table)
