import os
from posixpath import split
import random
from collections import defaultdict
from pyeasyga import pyeasyga
from .alu import ALU

#INF = 99999999999999

numbers = [k for k in range(1, 10) for x in range(1)]

def choose_number():
    return random.randint(1, 9)

def silver_ga(alu, best):

    def create_individual(data):
        individual = data[:]
        random.shuffle(individual)
        return individual

    def fitness(individual, _):
        alu.reset()
        alu.set_input_stream(*individual)
        alu.run_program()

        penalty = 0 #10.0 / int(''.join(map(str, individual)))
        for i in individual:
            penalty += 9 - i
        # if individual[0] < 9:
        #     penalty += (9 - individual[0])
        # if individual[1] < 9:
        #     penalty += (9 - individual[1])

        if alu.reg_data['z'] == 0:
            return 0
        
        return alu.reg_data['z'] + 0.6*penalty

    def mutate(individual):
        mutate_index1 = random.randrange(len(individual))
        individual[mutate_index1] = choose_number()
        
    def selection(population):
        return random.choice(population)

    ga = pyeasyga.GeneticAlgorithm(best, 
    generations=3000, 
    population_size=30, 
    crossover_probability=0.9, 
    mutation_probability=0.4,
    elitism=True,
    maximise_fitness=False)

    ga.create_individual = create_individual
    ga.fitness_function = fitness
    ga.mutate_function = mutate
    ga.selection_function = selection
    ga.run()
    
    return ga.best_individual()[1]

def compute_uniq(alu, split_at_pos):
    uniq_res = set()

    for n in range(int('1'*split_at_pos), 10**split_at_pos):
        alu.reset()
        alu.set_input_stream(*list(map(int, str(n))))
        alu.run_program()
        uniq_res.add(alu.reg_data['z'])

    return uniq_res

def silver(alu):
    # best = [choose_number() for _ in range(14)]
    # #best = [9, 6, 9, 7, 9, 6, 5, 9, 6, 9, 2, 4, 9, 5]
    # while True:
    #     best = silver_ga(alu, best)

    #     alu.reset()
    #     alu.set_input_stream(*list(map(int, best)))
    #     alu.run_program()
        
    #     print(best, alu.reg_data['z'])
    #     if alu.reg_data['z'] == 0:
    #         break

    # for n in range (96979659692496, 99999999999999):
    #     alu.reset()

    #     alu.set_input_stream(*list(map(int, str(n))))
    #     alu.run_program()

    #     res = alu.reg_data['z']

    #     #print(n, res)
    #     if res == 0:
    #         return n

    # return False

    start_split = 1
    head_alu, _ = alu.split_program(start_split)
    uniq_results = compute_uniq(head_alu, start_split)

    for split_pos in range(start_split+1, 15):
        head_alu, _ = alu.split_program(split_pos)
        _, tail_alu = head_alu.split_program(split_pos-1)
        new_results = set()

        print(len(uniq_results), split_pos-1)

        for n in range(1, 10):
            for prev_res in uniq_results:
                tail_alu.reset()
                tail_alu.set_input_stream(n)
                tail_alu.reg_data['z'] = prev_res
                tail_alu.run_program()
                new_results.add(tail_alu.reg_data['z'])

        uniq_results = new_results

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
