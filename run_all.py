import time

import day1.day1 as d1
import day2.day2 as d2
import day3.day3 as d3
import day4.day4 as d4
import day5.day5 as d5
import day6.day6 as d6
import day7.day7 as d7
import day8.day8 as d8
import day9.day9 as d9
import day10.day10 as d10
import day11.day11 as d11
import day12.day12 as d12
import day13.day13 as d13
import day14.day14 as d14
import day15.day15 as d15
import day16.day16 as d16
import day17.day17 as d17
import day18.day18 as d18
import day19.day19 as d19
import day20.day20 as d20
import day21.day21 as d21
import day22.day22 as d22
import day23.day23 as d23
import day24.day24 as d24


def show_solution(solution_tuple):
    name, silver, gold = solution_tuple
    print(f"{name}: silver: {silver}, gold: {gold}")


if __name__ == "__main__":
    problems = [
        # d1,
        # d2,
        # d3,
        # d4,
        # d5,
        # d6,
        # d7,
        # d8,
        # d9,
        # d10,
        # d11,
        # d12,
        # d13,
        # d14,
        # d15,
        # d16,
        # d17,
        # d18,
        # d19,
        # d20,
        # d21,
        # d22,
        # d23,
        d24,
    ]

    st = time.time()
    for problem in problems:
        show_solution(problem.solve())
    print("\ntime taken: {:.2f} sec.".format(time.time() - st))
