# #!/usr/bin/env python

import random
from snake import SnakeGame
from ga_controller import GAController



def print_max(population):
        max_fitness = max(controller.game.fitness for controller in population)
        print(f"Maximum fitness value of the current population: {max_fitness}")

# def mate_in_pairs(population):     # Extracting the list of keys to access the creatures in order    keys = list(creatures_dict.keys())          # Iterate over the keys in steps of 2 to get pairsfor i in range(0, len(keys) - 1, 2):         creature1 = creatures_dict[keys[i]]         creature2 = creatures_dict[keys[i+1]]         creature1.mate(creature2)
#     babies = []

#     for i in range(0, len(population) - 1, 2):
#         game = SnakeGame()
#         game2 = SnakeGame()
#         controller = GAController(game)
#         controller2 = GAController(game)
#         dad = population[i]
#         mom = population[i+1]
#         baby = dad.model + mom.model
#         baby2 = dad.model + mom.model
#         baby.mutate(0.3)
#         baby2.mutate(0.3)
#         babies.append(controller)
#         babies.append(controller2)
#     # print(babies)
#     return babies


class GeneticAlgorithm:
    def __init__(self, population_size=60, generations=5, keep_ratio=0.35, elite=2):
        self.population_size = population_size
        self.generations = generations
        self.population = []
        self.keep_ratio = keep_ratio
        self.elite = elite
        self.pop = []

    def initialize_population(self):
        for _ in range(self.population_size):
            game = SnakeGame()
            controller = GAController(game)
            game.run()
            print(controller)
            self.population.append(controller)
        print(self.population)

        # self.print_fitness_values()


    def create_population(self):
        for gen in range(self.generations):

            for controller in self.population:
                for i in range(self.population_size):
                    # print(self.population)
                    controller.game.run()
            self.pop.append(controller)
                    # Now you can access the index (idx) and the controller object in thi

                # Sort self.population by fitness
        self.pop = sorted(self.pop, key=lambda x: x.game.fitness, reverse=True)

                # Determine how many top performers to keep based on the ratio
        best = int(len(self.pop) * self.keep_ratio)
        elite = self.pop[:3]
        self.pop = self.pop[:best]
                # Retain top performers
        self.pop = self.pop[:best]

        babies = self.mate_in_pairs()
        self.pop.extend(babies)
        self.pop.extend(elite)


    def mate_in_pairs(self):     # Extracting the list of keys to access the creatures in order    keys = list(creatures_dict.keys())          # Iterate over the keys in steps of 2 to get pairsfor i in range(0, len(keys) - 1, 2):         creature1 = creatures_dict[keys[i]]         creature2 = creatures_dict[keys[i+1]]         creature1.mate(creature2)
        babies = []


    def mate_in_pairs(self):
        babies = []
        while len(babies) < (self.population_size-self.elite):
            game = SnakeGame()
            game2 = SnakeGame()
            controller = GAController(game)
            controller2 = GAController(game2)
            dad = random.choice(self.population)
            mom = random.choice(self.population)
            baby = dad.model + mom.model
            baby2 = dad.model + mom.model
            baby.mutate(0.08)
            baby2.mutate(0.08)
            babies.append(controller)
            babies.append(controller2)
        return babies
    def find_best_controller(self):
        print(self.population)
        sorted_population = sorted(self.population, key=lambda x: x.game.fitness, reverse=True)
        best_controllers = sorted_population[:30]
        for controller in best_controllers:
            print(f"Controller fitness: {controller.game.fitness}points:{controller.game.snake.score}")
        return best_controllers

if __name__ == '__main__':
    ga = GeneticAlgorithm(population_size=40, generations=20, elite=3)
    ga.initialize_population()
    # ga.print_fitness_values()
    ga.create_population()
    ga.find_best_controller()
    # def evolve_generations_tournament(self):
    #     for _ in range(self.generations):
    #         self.print_fitness_values()
    #         self.generations = self.generations - 1
    #         print(self.generations)
    #         new_pop = []
    #         # Tournament selection
    #         tournament_size = 50  # Define the tournament size
    #         while len(new_pop) < self.population_size:
    #             # Randomly select individuals for the tournament
    #             tournament_participants = random.sample(self.population, tournament_size)
    #             # Choose the best individual from the tournament
    #             winner = max(tournament_participants, key=lambda x: x.game.fitness)
    #             print(winner.game.fitness)
    #             new_pop.append(winner)
    #         print("LENG", len(new_pop))

    #         # Mating to fill remaining slots
    #         while len(new_pop) < self.population_size:
    #             dad = random.choice(new_pop)
    #             mom = random.choice(new_pop)
    #             baby = dad.model + mom.model
    #             baby.mutate(0.08)
    #             new_controller = GAController(SnakeGame(), model=baby)
    #             new_pop.append(new_controller)
    #         self.population = new_pop
    # # ga.evolve_generations_tournament()
    # # print("Best Controller Fitness:", best_controller.game.fitness)