from collections import defaultdict
from itertools import product, chain
import os


MAX_SCORE = 21


def new_pos(cur_pos, dice):
    return ((cur_pos + dice - 1) % 10) + 1


def next_player(cur_player):
    return (cur_player + 1) % 2


def silver(pos):
    scores = defaultdict(int)
    dice_rolls = 1

    while True:
        for player_no in pos.keys():
            for _ in range(3):
                pos[player_no] = new_pos(pos[player_no], dice_rolls)
                dice_rolls += 1

            scores[player_no] += pos[player_no]
            if scores[player_no] >= 1000:
                return (dice_rolls - 1) * scores[(player_no + 1) % 2]


def make_pos(pos, dice_sum, cur_player):
    another_player = next_player(cur_player)
    return {
        cur_player: new_pos(pos[cur_player], dice_sum),
        another_player: pos[another_player],
    }


def make_sum(pos, sums, cur_player):
    another_player = next_player(cur_player)
    return {
        cur_player: sums[cur_player] + pos[cur_player],
        another_player: sums[another_player],
    }


dices = [1, 2, 3]
dices_sums = list(map(sum, product(map(sum, product(dices, dices)), dices)))


def rec(pos, sums, mem, cur_player):

    player1_sum, player2_sum = sums[0], sums[1]

    if player1_sum >= MAX_SCORE:
        return {0: 1}
    if player2_sum >= MAX_SCORE:
        return {1: 1}

    key = tuple(chain(pos.items(), sums.items()))

    if key in mem:
        return mem[key]

    mem[key] = defaultdict(int)

    for dice_sum in dices_sums:
        new_pos = make_pos(pos, dice_sum, cur_player)
        new_sum = make_sum(new_pos, sums, cur_player)
        res = rec(new_pos, new_sum, mem, next_player(cur_player))

        for player, score in res.items():
            mem[key][player] += score

    return mem[key]


def gold(pos):
    mem = {}
    initial_sums = {0: 0, 1: 0}

    rec(pos, initial_sums, mem, 0)
    return max(mem[tuple(chain(pos.items(), initial_sums.items()))].values())


def parse_player(line):
    _, player, _, _, start_pos = line.split()
    return int(player) - 1, int(start_pos)


def parse(lines):
    pos = {}
    for line in lines:
        player, start_pos = parse_player(line.strip())
        pos[player] = start_pos

    return pos


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    pos = parse(lines)

    return "DAY21", silver(pos.copy()), gold(pos.copy())
