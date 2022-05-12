import os
from posixpath import split
import random
from collections import defaultdict
from pyeasyga import pyeasyga
from .alu import ALU

#INF = 99999999999999

INP_LEN = 14

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
    uniq_results = defaultdict(list)

    for n in range(int('1'*split_at_pos), 10**split_at_pos):
        alu.reset()
        alu.set_input_stream(*list(map(int, str(n))))
        alu.run_program()
        uniq_results[alu.reg_data['z']].append(str(n))

    return uniq_results

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

    # start_split = 1

    # head_alu, _ = alu.split_program(start_split)
    # uniq_results = compute_uniq(head_alu, start_split)

    print('phase 1...')

    cur_set = {0: []}
    compute_until = 15

    num_range = [list(map(int, str(n))) for n in range(11, 100) 
                        if 0 not in str(n)]

    for split_pos in range(1, compute_until, 1):

        # get just one block at split_pos
        head_alu, _ = alu.split_program(split_pos)
        _, tail_alu = head_alu.split_program(split_pos-1)

        new_set = defaultdict(list)

        for prev_res, input_digits in cur_set.items():

            for n in num_range:
                tail_alu.reset()
                tail_alu.set_input_stream(*n)
                tail_alu.reg_data['z'] = prev_res
                tail_alu.run_program()

                res = tail_alu.reg_data['z']

                if split_pos < 11:
                    new_set[res] = []
                    continue

                if split_pos == 14 and res != 0:
                    continue

                if input_digits:
                    new_set[res].extend([10*k+n for k in input_digits])
                else:
                    new_set[res].append(n)

        cur_set.clear()
        for k, v in new_set.items():
            cur_set[k] = list(set(v))
        
        print("{} possible outcomes for {} blocks".format(len(cur_set), split_pos))

    print(cur_set[0])

    print('\nphase 2...')

    # get rest blocks
    # _, tail_alu = alu.split_program(compute_until)
    # upper_range = int(''.join(['9'] * (INP_LEN - compute_until)))
    # lower_range = int(''.join(['1'] * (INP_LEN - compute_until)))

    # num_range = [list(map(int, str(n))) for n in range(upper_range, lower_range-1, -1) 
    #                         if 0 not in list(map(int, str(n)))]

    # print(len(cur_set.keys()))

    # for z, prefixes in cur_set.items():
    #     print(z)
    #     for n in num_range:
    #         tail_alu.reset()
    #         tail_alu.set_input_stream(*n)
    #         tail_alu.reg_data['z'] = z
    #         tail_alu.run_program()
    #         if tail_alu.reg_data['z'] == 0:
    #             return "yeess"

    #return max(cur_set[0], key=lambda v: int(v))

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
