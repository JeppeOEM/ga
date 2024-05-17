#!/usr/bin/env python

from snake import SnakeGame
from ga_controller import GAController

def kill_half(sorted_list):
    # Calculate the index to start slicing from
    sorted()
    index_to_remove = len(sorted_list) // 2
    # Slice the list to remove the lowest values
    result = sorted_list[index_to_remove:]
    return result

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

# for _ in range(1000):
#     game = SnakeGame()
#     controller = GAController(game)
#     population.append(controller)
#     game.run()


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

if __name__ == '__main__':
     for _ in range(2):
        population = []
        for _ in range(100):
            game = SnakeGame()
            controller = GAController(game)
            game.run()
            population.append(controller)

        # Sort the population by game.fitness in descending order
        population = sorted(population, key=lambda x: x.game.fitness, reverse=True)

        # Access the sorted population
        for controller in population:
            print(f"Fitness: {controller.game.fitness}")

