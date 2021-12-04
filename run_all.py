import day1.day1 as d1
import day2.day2 as d2
import day3.day3 as d3
import day4.day4 as d4


def show_solution(solution_tuple):
    name, silver, gold = solution_tuple
    print(f"{name}: silver: {silver}, gold: {gold}")


if __name__ == "__main__":
    problems = [d1, d2, d3, d4]
    for problem in problems:
        show_solution(problem.solve())
