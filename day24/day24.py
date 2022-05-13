import os
from collections import defaultdict
from .alu import ALU

INP_LEN = 14


def get_subroutine(alu, idx):
    head_alu, _ = alu.split_program(idx)
    _, tail_alu = head_alu.split_program(idx - 1)
    return tail_alu


def compute(alu):

    to_check = range(1, 10)

    good_zs = defaultdict(set)
    collected_numbers = {}

    for current_pos in range(0, 15):

        cur_set = {0: None}

        for split_pos in range(1, 15):

            # get just one block at split_pos
            subroutine = get_subroutine(alu, split_pos)

            new_set = defaultdict(set)

            if len(collected_numbers) > 0:
                l = len(str(list(collected_numbers)[0]))
                pos = l - 1 - INP_LEN + split_pos
                if pos >= 0:
                    to_check = set(
                        int(item[pos]) for item in map(str, collected_numbers)
                    )

            print("values to check: {}".format(to_check))

            for prev_z, input_digits in cur_set.items():

                for n in to_check:

                    subroutine.reset()
                    subroutine.set_input_stream(n)
                    subroutine.reg_data["z"] = prev_z
                    subroutine.run_program()

                    z = subroutine.reg_data["z"]
                    if split_pos in good_zs:
                        if z not in good_zs[split_pos]:
                            continue
                        good_zs[split_pos - 1].add(prev_z)

                    if split_pos < INP_LEN - current_pos:
                        new_set[z] = None
                        continue

                    if split_pos == INP_LEN:
                        if z != 0:
                            continue
                        good_zs[split_pos - 1].add(prev_z)

                    if input_digits:
                        new_set[z].update({10 * k + n for k in input_digits})
                    else:
                        new_set[z].add(n)

            cur_set = new_set
            print(
                "{} possible outcomes for {} digits\n".format(len(cur_set), split_pos)
            )

        collected_numbers = cur_set[0]
        # print("\n\n", cur_set[0], "\n\n")

    return collected_numbers


def parse(lines):
    alu = ALU()
    alu.parse_program(lines)
    return alu


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()
    all_solutions = compute(parse(lines))
    return "DAY24", max(all_solutions), min(all_solutions)
