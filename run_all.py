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


def show_solution(solution_tuple):
    name, silver, gold = solution_tuple
    print(f"{name}: silver: {silver}, gold: {gold}")


if __name__ == "__main__":
    problems = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14]
    for problem in problems:
        show_solution(problem.solve())
