import os
import random
from collections import defaultdict
from pyeasyga import pyeasyga
from .alu import ALU

#INF = 99999999999999

numbers = [k for k in range(1, 10) for x in range(k)]

def choose_number():
    return random.choice(numbers)

def silver_ga(alu, best):

    def create_individual(data):
        #return [choose_number() for _ in range(14)]
        individual = data[:]
        random.shuffle(individual)
        return individual

    def fitness(individual, _):
        alu.reset()
        alu.set_input_stream(*individual)
        alu.run_program()

        penalty = 0 #10.0 / int(''.join(map(str, individual)))
        # if individual[0] < 9:
        #     penalty += (9 - individual[0])
        # if individual[1] < 9:
        #     penalty += (9 - individual[1])

        if alu.reg_data['z'] == 0:
            return 0
        
        return alu.reg_data['z'] + penalty

    def mutate(individual):
        mutate_index1 = random.randrange(len(individual))
        individual[mutate_index1] = choose_number()
        
    def selection(population):
        return random.choice(population)

    ga = pyeasyga.GeneticAlgorithm(best, 
    generations=1000, 
    population_size=50, 
    crossover_probability=0.3, 
    mutation_probability=0.4,
    elitism=True,
    maximise_fitness=False)

    ga.create_individual = create_individual
    ga.fitness_function = fitness
    ga.mutate_function = mutate
    ga.selection_function = selection
    ga.run()
    
    return ga.best_individual()[1]

def silver(alu):
    best = [choose_number() for _ in range(14)]
    best = [9, 6, 9, 7, 9, 6, 5, 9, 6, 9, 2, 4, 9, 5]
    best = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    while True:
        best = silver_ga(alu, best)

        alu.reset()
        alu.set_input_stream(*list(map(int, best)))
        alu.run_program()
        
        print(best, alu.reg_data['z'])
        if alu.reg_data['z'] == 0:
            break

    # periods = defaultdict(int)
    # last_seen = {}

    # for n in range (99999999999999, 11111111111110, -1):
    #     alu.reset()

    #     alu.set_input_stream(*list(map(int, str(n))))
    #     alu.run_program()

    #     res = alu.reg_data['z']
    #     res_str = str(res)
    #     res_len = len(res_str)

    #     if res_len in last_seen:
    #         periods[res_len] = last_seen[res_len] - n

    #     last_seen[res_len] = n

    #     print(periods, n, res)

    #     #print(n, res)
    #     if res == 0:
    #         return n

    # return False

def gold(alu):
    pass

def parse(lines):
    alu = ALU()
    alu.parse_program(lines)
    return alu


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), "input"), "rt").readlines()

    return "DAY24", silver(parse(lines)), 1 #gold(parse(lines))
