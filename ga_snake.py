# #!/usr/bin/env python

import random
from snake import SnakeGame
from ga_controller import GAController



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
        baby.mutate(0.08)
        baby2.mutate(0.08)
        babies.append(baby)
        babies.append(baby2)
    # print(babies)
    return babies


class GeneticAlgorithm:
    def __init__(self, population_size=60, generations=5):
        self.population_size = population_size
        self.generations = generations
        self.population = []

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            game = SnakeGame()
            controller = GAController(game)
            game.run()
            population.append(controller)
        print(len(population))


        self.print_fitness_values()
        self.population = population

    def evolve_generations_tournament(self):
        for _ in range(self.generations):
            self.print_fitness_values()
            self.generations = self.generations - 1
            print(self.generations)
            new_pop = []
            # Tournament selection
            tournament_size = 50  # Define the tournament size
            while len(new_pop) < self.population_size:
                # Randomly select individuals for the tournament
                tournament_participants = random.sample(self.population, tournament_size)
                # Choose the best individual from the tournament
                winner = max(tournament_participants, key=lambda x: x.game.fitness)
                print(winner.game.fitness)
                new_pop.append(winner)
            print("LENG", len(new_pop))

            # Mating to fill remaining slots
            while len(new_pop) < self.population_size:
                dad = random.choice(new_pop)
                mom = random.choice(new_pop)
                baby = dad.model + mom.model
                baby.mutate(0.08)
                new_controller = GAController(SnakeGame(), model=baby)
                new_pop.append(new_controller)
            self.population = new_pop

    def evolve_generations(self):
        for _ in range(self.generations):
            self.print_fitness_values()
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
            new_pop = sorted(new_pop, key=lambda x: x.game.fitness, reverse=True)
            print("LENG",len(new_pop))
            new_pop = new_pop[:len(new_pop) // 2]

            new_controllers = []
            new_models = mate_in_pairs(new_pop)
            for model in new_models:
                game = SnakeGame()
                controller = GAController(game, model=model)
                new_controllers.append(controller)
            print("new models",len(new_models))
            print("new controllers",len(new_controllers))
            #.append when make them contain the same objects


            new_controllers.extend(new_pop)
            print()
            self.population = new_controllers

    def find_best_controller(self):
        sorted_population = sorted(self.population, key=lambda x: x.game.fitness, reverse=True)
        best_controllers = sorted_population[:30]
        return best_controllers
    def print_fitness_values(self):
        population = sorted(self.population, key=lambda x: x.game.fitness, reverse=True)
        population = population[:10]
        print("Fitness values of the current population:")
        for i, controller in enumerate(population):
            print(f"Controller {i+1}: Fitness = {controller.game.fitness}")
    def print_max_fitness_value(self, population):
        max_fitness = max(controller.game.fitness for controller in population)
        print(f"Maximum fitness value of the current population: {max_fitness}")


if __name__ == '__main__':
    ga = GeneticAlgorithm(population_size=100, generations=500)
    ga.initialize_population()
    ga.print_fitness_values()
    ga.evolve_generations()
    ga.print_fitness_values()
    # ga.evolve_generations_tournament()
    # print("Best Controller Fitness:", best_controller.game.fitness)