# #!/usr/bin/env python

import random
from snake import SnakeGame
from ga_controller import GAController

# def kill_half(sorted_list):
#     # Calculate the index to start slicing from
#     sorted()
#     index_to_remove = len(sorted_list) // 2
#     # Slice the list to remove the lowest values
#     result = sorted_list[index_to_remove:]
#     return result

# def remove_lowest_values(sorted_list):
#     # Calculate the index to start slicing from
#     index_to_remove = len(sorted_list) // 2
#     # Slice the list to remove the lowest values
#     result = sorted_list[index_to_remove:]
#     return result

# population = []

# def get_fitness(game):
#     return game.fitness

# # Create 100 instances of the Snake game and add them to the population

# # for _ in range(1000):
# #     game = SnakeGame()
# #     controller = GAController(game)
# #     population.append(controller)
# #     game.run()


def print_max(population):
        max_fitness = max(controller.game.fitness for controller in population)
        print(f"Maximum fitness value of the current population: {max_fitness}")

def mate_in_pairs(population):     # Extracting the list of keys to access the creatures in order    keys = list(creatures_dict.keys())          # Iterate over the keys in steps of 2 to get pairsfor i in range(0, len(keys) - 1, 2):         creature1 = creatures_dict[keys[i]]         creature2 = creatures_dict[keys[i+1]]         creature1.mate(creature2)
    babies = []
    for i in range(0, len(population) - 1, 2):
        dad = population[i]
        mom = population[i+1]
        baby = dad.model + mom.model
        baby2 = dad.model + mom.model
        baby.mutate(0.05)
        baby2.mutate(0.05)
        babies.append(baby)
        babies.append(baby2)
    # print(babies)
    return babies




class GeneticAlgorithm:
    def __init__(self, population_size=10, generations=2):
        self.population_size = population_size
        self.generations = generations
        self.population = []
        self.elite = 0
        self.keep_ratio=0.3


    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            game = SnakeGame()
            controller = GAController(game)
            game.run()
            population.append(controller)
        print(len(population))


        self.population = population

    def evolve_generations(self):
        for _ in range(self.generations):
            self.generations = self.generations-1
            print(self.generations)
            new_pop=[]
            for controller in self.population:
                game = SnakeGame()
                game.controller = controller
                print(type(controller))
                controller.game = game
                game.run()

                print(controller.game.fitness)
                # if len(new_pop) > 0:
                #     self.print_max_fitness_value(new_pop)
                new_pop.append(controller)







            #######################
            new_pop = sorted(new_pop, key=lambda x: x.game.fitness, reverse=True)

            elite = self.population[:self.elite]
            del self.population[:self.elite]  # Extract elite elements
            self.population = self.population[self.elite:]# removes from list
            best = int(len(self.population) * self.keep_ratio)
            del self.population[best:] # remove worst



            # print("LENG",len(new_pop))
            # new_pop = new_pop[:len(new_pop) // 2]
            # self.print_fitness_values(new_pop)
            new_controllers = []
            new_models = mate_in_pairs(new_pop)
            for model in new_models:
                game = SnakeGame()
                controller = GAController(game, model=model)
                new_controllers.append(controller)
            print("new models",len(new_models))
            print("new controllers",len(new_controllers))
            #.append when make them contain the same objects

            new_controllers.extend(elite)
            new_controllers.extend(new_pop)
            self.population = new_controllers
    def mate_in_pairs(self):
        babies = []
        size = self.population_size - len(self.population)
        size = size - self.elite
        while len(babies) < size:
            dad, mom = random.sample(self.population, 2)
            baby = dad.model + mom.model
            baby2 = dad.model + mom.model
            baby.mutate(0.08)
            baby2.mutate(0.08)
            babies.append(baby)
            babies.append(baby)
        return babies
    def find_best_controller(self):
        sorted_population = sorted(self.population, key=lambda x: x.game.fitness, reverse=True)
        best_controllers = sorted_population[:30]
        return best_controllers
    def print_fitness_values(self, population):
        print("Fitness values of the current population:")
        for i, controller in enumerate(population):
            print(f"Controller {i+1}: Fitness = {controller.game.fitness}")
    def print_max_fitness_value(self, population):
        max_fitness = max(controller.game.fitness for controller in population)
        print(f"Maximum fitness value of the current population: {max_fitness}")


if __name__ == '__main__':
    ga = GeneticAlgorithm(population_size=100, generations=3)
    ga.initialize_population()
    ga.evolve_generations()
    best_controllers = ga.find_best_controller()
    for i, controller in enumerate(best_controllers, start=1):
        print(f"Rank {i}: Fitness = {controller.game.fitness}")
    # print("Best Controller Fitness:", best_controller.game.fitness)