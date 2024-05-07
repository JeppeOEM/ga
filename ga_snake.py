#!/usr/bin/env python
def kill_half(sorted_list):
    # Calculate the index to start slicing from
    index_to_remove = len(sorted_list) // 2
    # Slice the list to remove the lowest values
    result = sorted_list[index_to_remove:]
    return result

from snake import SnakeGame
from ga_controller import GAController

def remove_lowest_values(sorted_list):
    # Calculate the index to start slicing from
    index_to_remove = len(sorted_list) // 2
    # Slice the list to remove the lowest values
    result = sorted_list[index_to_remove:]
    return result

population = []

def get_fitness(game):
    return game.fitness

# Create 100 instances of the Snake game and add them to the population

for _ in range(1000):
    game = SnakeGame()
    controller = GAController(game)
    population.append(controller)
    game.run()


def mate_in_pairs(population):     # Extracting the list of keys to access the creatures in order    keys = list(creatures_dict.keys())          # Iterate over the keys in steps of 2 to get pairsfor i in range(0, len(keys) - 1, 2):         creature1 = creatures_dict[keys[i]]         creature2 = creatures_dict[keys[i+1]]         creature1.mate(creature2)
    babies = []
    for i in range(0, len(population) - 1, 2):
        dad = population[i]
        mom = population[i+1]
        print(dad,mom)
        baby = dad.model + mom.model
        baby2 = dad.model + mom.model
        baby.mutate(0.05)
        baby2.mutate(0.05)
        babies.append(baby)
        babies.append(baby2)
    return babies

# population.sort(key=get_fitness, reverse=True)
# population = remove_lowest_values(population)





reduced_pop = kill_half(population)
offspring = mate_in_pairs(reduced_pop)
        # print(offspring)
        # print(reduced_pop)
new_gen = reduced_pop.append(offspring)
