#!/usr/bin/env python


from snake import SnakeGame
from ga_controller import GAController

def kill_half(sorted_list):
    # Calculate the index to start slicing from
    index_to_remove = len(sorted_list) // 2
    # Slice the list to remove the lowest values
    result = sorted_list[index_to_remove:]
    return result



def get_fitness(game):
    return game.fitness

# Create 100 instances of the Snake game and add them to the population



# Run each game in the population

def mate_in_pairs(population):     # Extracting the list of keys to access the creatures in order    keys = list(creatures_dict.keys())          # Iterate over the keys in steps of 2 to get pairsfor i in range(0, len(keys) - 1, 2):         creature1 = creatures_dict[keys[i]]         creature2 = creatures_dict[keys[i+1]]         creature1.mate(creature2)
    babies = []
    for i in range(0, len(population) - 1, 2):
        dad = population[i]
        mom = population[i+1]
        baby = dad + mom
        baby2 = dad + mom
        baby.mutate(0.05)
        baby2.mutate(0.05)
        babies.append(baby,baby2)
    return babies


def init_population(pop_size):
    population = []
    for _ in range(pop_size):
        game = SnakeGame()
        population.append(game)
    return population

def generations(generations, pop_size):
    gens = []
    init_population(pop_size)



    for generation in range(generations):
        for game in generation:
            controller = GAController(game)
            game.run()
            population.append(controller)
        parents = kill_half(population)
        offspring = mate_in_pairs(parents)
        population = parents.append(offspring)


generations(100, 100)