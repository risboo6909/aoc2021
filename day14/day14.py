from copy import deepcopy
from collections import Counter, defaultdict
from typing import DefaultDict, Optional, List, Tuple, Dict
import os


class Elem(object):

    def __init__(self, label):
        self.next = None
        self.label = label

    def insert_next(self, elem):
        tmp = self.next
        self.next = elem
        elem.next = tmp
        return elem


def polymer_str(cur: Elem) -> str:
    res = []
    while cur is not None:
        res.append(cur.label)
        cur = cur.next
    return ''.join(res)


def silver(cur: Elem, table: Dict[str, str]):
    cloned = deepcopy(cur)
    for to in range(10):

        cur = deepcopy(cloned)

        for _ in range(to):

            new_cur = new_head = Elem(cur.label)

            while cur.next is not None:
                pair = '{}{}'.format(cur.label, cur.next.label)
                label_new = table[pair]

                new_cur = new_cur.insert_next(Elem(label_new))
                cur = cur.next
                new_cur = new_cur.insert_next(Elem(cur.label))

            cur = new_head

        head = cur
        freq = defaultdict(int)
        while cur is not None:
            freq[cur.label] += 1
            cur = cur.next

        print('iters: {}, max: {}, min: {}'.format(
            to, max(freq.values()), min(freq.values())))

    print(polymer_str(head))

    return max(freq.values()) - min(freq.values())


scores = defaultdict(int)
cache = defaultdict(Counter)

max_depth = 10
global_cache = defaultdict(Counter)


def accumulate(cache, acc, st, end, depth):
    global global_cache
    # cache[(st, end, depth)]
    # for d in range(depth, -1, -1):
    # for k, v in acc[(st, end, d)].items():
    # cache[(st, end, depth)][k] += v
    for (st2, end2, d), counters in acc.items():
        for k, v in counters.items():
            cache[(st2, end2, d)][k] += v
            if d + 1 == depth:
                cache[(st, end, depth)][k] += v


def accumulate2(st, end, depth):
    global cache
    for (st2, end2, d), counters in deepcopy(cache).items():
        for k, v in counters.items():
            cache[(st2, end2, d)][k] += v
            if d + 1 == depth:
                cache[(st, end, depth)][k] += v


def update_scores(scores, cache, st, end, depth):
    for k, v in cache[(st, end, depth)].items():
        #print('hit: st:{}, end: {}, depth: {}, {} {}'.format(st, end, depth, k, v))
        scores[k] += v


def copy_depth(cache, st, end, depth):
    res = defaultdict(Counter)
    for (st2, end2, d), counters in cache.items():
        if st2 == st and end2 == end and d == depth:
            res[(st, end, d)] = counters

    return res


def solve_rec(st, end, table, depth):
    global global_cache, scores

    key = (st, end)
    to_insert = table[key]

    if depth == 0:
        # print(key)
        # print('st, ins, et: ', st,  to_insert, end)
        return defaultdict(Counter), False

    if (st, end, depth) in global_cache:
        #     cache = defaultdict(Counter)
        #     for (k, v, d), counter in global_cache.items():
        #         if d > depth:
        #             continue
        #         for l, n in counter.items():
        #             cache[(k, v, d)][l] += n

        counter = global_cache[(st, end, depth)]
        for e, v in counter.items():
            scores[e] += v

        scores[to_insert[0]] += 1

        res = {(st, end, depth): counter}
        return res, True

        # if (st, end, depth) in cache:
        #     counter = cache[(st, end, depth)]
        #     # for e, v in counter.items():
        #     #     scores[e] += v
        #     return scores

    cache_left = defaultdict(Counter)
    cache_right = defaultdict(Counter)
    cache = defaultdict(Counter)

    acc_left, from_cache_left = solve_rec(st, to_insert[0], table, depth-1)
    if not from_cache_left:
        accumulate(cache_left, acc_left, st, end, depth)
    else:
        cache_left = acc_left
    acc_right, from_cache_right = solve_rec(to_insert[0], end, table, depth-1)
    if not from_cache_right:
        accumulate(cache_right, acc_right, st, end, depth)
    else:
        cache_right = acc_right

    if not from_cache_left:
        for (k, v, d), counter in cache_left.items():
            for l, n in counter.items():
                global_cache[(k, v, d)][l] = n

    if not from_cache_right:
        for (k, v, d), counter in cache_right.items():
            for l, n in counter.items():
                global_cache[(k, v, d)][l] = n

    for (k, v, d), counter in cache_left.items():
        cache[(k, v, d)] += counter

    for (k, v, d), counter in cache_right.items():
        cache[(k, v, d)] += counter

    cache[(st, end, depth)][to_insert[0]] += 1

    scores[to_insert[0]] += 1

    return cache, False

    # print('depth: {}, left: {},  right: {}'.format(depth, acc_left, acc_right))
    # if acc_left is not None:
    #     accumulate(cache, acc_left, st, end, depth)

    # if acc_right is not None:
    #     accumulate(cache, acc_right, st, end, depth)

    # print(global_cache)


def gold(init, table):
    global global_cache
    for st, end in zip(init, init[1:]):
        #print(st, end)
        solve_rec(st, end, table, max_depth)
        # print(cache[('N', 'N', 10)], cache[(
        #     'N', 'C', 10)], cache[('C', 'B', 10)])
    print(global_cache)
    print(scores)


def parse(lines: List[str]) -> Tuple[Optional[Elem], Dict[str, str]]:
    line = lines[0]
    prev = head = None

    # create initial polymer
    for e in line.strip():
        cur = Elem(e)

        if head is None:
            head = cur

        if prev is not None:
            prev.insert_next(cur)

        prev = cur

    table = {}

    # read transformation rules
    for line in lines[2:]:
        left, right = line.strip().split(' -> ')
        table[(left[0], left[1])] = [right]

    # for line in lines[2:]:
    #     left, right = line.strip().split(' -> ')
    #     table[left] = right

    return head, table


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), "input"), "rt").readlines()

    head, table = parse(lines)

    # return "DAY 14", silver(head, table), 0
    gold(['N', 'N', 'C', 'B'], table)
    return "DAY14", 0, 0
