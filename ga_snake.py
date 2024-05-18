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
    #Take care Elite is broken will add them to array end the end so the array will get bigger
    def __init__(self, population_size=60, generations=5, remove_ratio=0.5, elite=12):
        self.population_size = population_size
        self.generations = generations
        self.population = []
        self.remove_ratio = remove_ratio
        self.elite = elite
        self.pop = []
        self.generations_info = []
        #iterator
        self.i = 0
        self.display = False

    def initialize_population(self):
        for _ in range(self.population_size):
            game = SnakeGame()
            controller = GAController(game)
            game.run()
            self.population.append(controller)
        print(self.population)

        # self.print_fitness_values()


    def create_population(self):
        for gen in range(self.generations):
            print("LEN:", len(self.population))
            print("GENERATION: ",gen)
            if gen == self.generations:
                print(gen,"s")
                self.display = True


            i = 0
            new_pop = []
            for old_controller in self.population:
                    game = SnakeGame()  # Create a new instance of SnakeGame
                    controller = GAController(game)  # Create a new instance of GAController
                    controller.model = old_controller.model  # Set the model from the old controller to the new one
                    controller.game = game  # Add the snake game to the controller
                    new_pop.append(controller)
            #create new population
            self.population = []
            for new_controller in new_pop:
                for _ in range(self.population_size):
                            # print(self.population)
                            # if self.display:
                            #     controller.display = self.display
                    new_controller.game.run()
                self.population.append(new_controller)
            # gets saved to the ppulation
                # self.population.append(controller)
            print(f"*******Population number:{i}******")

            # Sort in best results self.populationulation by fitness
            self.population = sorted(self.population, key=lambda x: x.game.fitness, reverse=True)
            self.print_best_snakes(self.population)

            elite = self.population[:self.elite]
            del self.population[:self.elite]  # Extract elite elements
            self.population = self.population[self.elite:]# removes from list
            best = int(len(self.population) * self.remove_ratio)
            del self.population[best:] # remove worst

            babies = self.mate_in_pairs()
            self.population.extend(babies)
            self.population.extend(elite)
            # self.print_best_snakes(self.population)




    def mate_in_pairs(self):     # Extracting the list of keys to access the creatures in order    keys = list(creatures_dict.keys())          # Iterate over the keys in steps of 2 to get pairsfor i in range(0, len(keys) - 1, 2):         creature1 = creatures_dict[keys[i]]         creature2 = creatures_dict[keys[i+1]]         creature1.mate(creature2)
        babies = []
    # mixes randomly but not the same one twice
    def mate_in_pairs(self):
        babies = []
        size = self.population_size - len(self.population)
        size = size - self.elite
        while len(babies) < size:
            game = SnakeGame()
            game2 = SnakeGame()
            dad, mom = random.sample(self.population, 2)
            controller = GAController(game)
            controller2 = GAController(game2)
            baby = dad.model + mom.model
            baby2 = dad.model + mom.model
            baby.mutate(0.08)
            baby2.mutate(0.08)
            babies.append(controller)
            babies.append(controller2)
        return babies
    ## pairs next one
    # def mate_in_pairs(self):
    #     babies = []
    #     while len(babies) < (self.population_size-self.elite):
    #         game = SnakeGame()
    #         game2 = SnakeGame()
    #         controller = GAController(game)
    #         controller2 = GAController(game2)
    #         dad = random.choice(self.population)
    #         mom = random.choice(self.population)
    #         baby = dad.model + mom.model
    #         baby2 = dad.model + mom.model
    #         baby.mutate(0.08)
    #         baby2.mutate(0.08)
    #         babies.append(controller)
    #         babies.append(controller2)
    #     return babies
    def print_best_snakes(self, population, iterator=0):
        i=0
        for pop in population:
            i+=1
            print(f"{i}# fitness: {pop.game.fitness} score: {pop.game.snake.score} steps: {pop.game.step}")
        print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDONNNNNNNNNNNNNNEEEEEEEEEE")
        # sorted_population = sorted(self.population, key=lambda x: x.game.fitness, reverse=True)
        # best_controllers = sorted_population[:30]

        # for controller in best_controllers:
        #     info = f" Gen {iterator}Controller fitness: {controller.game.fitness}points:{controller.game.snake.score}"
        #     self.generations_info.append(info)
        #     print(f"Controller fitness: {controller.game.fitness}points:{controller.game.snake.score}")


if __name__ == '__main__':
    ga = GeneticAlgorithm(population_size=50, generations=300, elite=2)
    ga.initialize_population()
    # ga.print_fitness_values()
    ga.create_population()
    # for info in ga.generations_info:
    #     print(info)
    ga.print_best_snakes(ga.population)
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