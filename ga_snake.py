#!/usr/bin/env python


from numpy import number
from snake import SnakeGame
from ga_controller import GAController

def remove_lowest_values(sorted_list):
    # Calculate the index to start slicing from
    index_to_remove = len(sorted_list) // 2
    # Slice the list to remove the lowest values
    result = sorted_list[index_to_remove:]
    return result

def init_population(pop_size):
    population = []
    for _ in range(pop_size):
        game = SnakeGame()
        controller = GAController(game)
        population.append((game, controller))
    return population

class Population:
    def __init__(self, population_size: int, generations: number):
        self.generations = generations
        self.population_size = population_size
        self.population = init_population(population_size)

    # def mutate_pop(self):
    #     for pop in self.population:
    #         print(pop)
    #         pop.snake.game.mutate(0.05)
    def selection(self):
        self.population
        selected = []
        results = []
        for population_tuple in self.population:
            game = population_tuple[0]
            obj_controller = population_tuple[1]
            game.run()
            results.append(obj_controller)

        results = remove_lowest_values(results)
        return results
    def mate_in_pairs(self):     # Extracting the list of keys to access the creatures in order    keys = list(creatures_dict.keys())          # Iterate over the keys in steps of 2 to get pairsfor i in range(0, len(keys) - 1, 2):         creature1 = creatures_dict[keys[i]]         creature2 = creatures_dict[keys[i+1]]         creature1.mate(creature2)
        babies = []
        for i in range(0, len(self.population) - 1, 2):
            dad = self.population[i]
            mom = self.population[i+1]
            baby = dad + mom
            baby2 = dad + mom
            # baby.mutate(0.05)
            # baby2.mutate(0.05)
            babies.append(baby)
            babies.append(baby2)
        return babies

    #         population.append(controller)

pop = Population(2, 100)
print(pop.generations)
i = 0
while i < 3:
    print("ddd")
    # pop.mutate_pop()
    pop.selection()
    pop.mate_in_pairs()
    i =+ 1





def get_fitness(game):
    return game.fitness

# Create 100 instances of the Snake game and add them to the population



# Run each game in the population

# def mate_in_pairs(population):     # Extracting the list of keys to access the creatures in order    keys = list(creatures_dict.keys())          # Iterate over the keys in steps of 2 to get pairsfor i in range(0, len(keys) - 1, 2):         creature1 = creatures_dict[keys[i]]         creature2 = creatures_dict[keys[i+1]]         creature1.mate(creature2)
#     babies = []
#     for i in range(0, len(population) - 1, 2):
#         dad = population[i]
#         mom = population[i+1]
#         baby = dad + mom
#         baby2 = dad + mom
#         baby.mutate(0.05)
#         baby2.mutate(0.05)
#         babies.append(baby,baby2)
#     return babies




# def generations(generations, pop_size):
#     gens = []
#     init_population(pop_size)



    # for generation in range(generations):
    #     for game in generation:
    #         controller = GAController(game)
    #         game.run()
    #         population.append(controller)
    #     parents = kill_half(population)
    #     offspring = mate_in_pairs(parents)
    #     population = parents.append(offspring)
