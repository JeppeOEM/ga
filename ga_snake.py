# #!/usr/bin/env python

import random
from snake import SnakeGame
from ga_controller import GAController



def print_max(population):
        max_fitness = max(controller.game.fitness for controller in population)
        print(f"Maximum fitness value of the current population: {max_fitness}")


class GeneticAlgorithm:
    #Take care Elite is broken will add them to array end the end so the array will get bigger

    def __init__(self, population_size=60, generations=5, keep_ratio=0.3, elite=12):
        self.population_size = population_size
        self.generations = generations
        self.population = []
        self.keep_ratio = keep_ratio
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
                    game = SnakeGame()
                    controller = GAController(game)
                    controller.model = old_controller.model
                    controller.game = game  #
                    new_pop.append(controller)
            #create new population
            self.population = []
            for new_controller in new_pop:

                for _ in range(self.population_size):
                    new_controller.game.run()
                self.population.append(new_controller)



            # Sort in best results self.populationulation by fitness
            self.population = sorted(self.population, key=lambda x: x.game.fitness, reverse=True)
            self.print_best_snakes(self.population)

            elite = self.population[:self.elite]
            del self.population[:self.elite]  # Extract elite elements
            self.population = self.population[self.elite:]# removes from list
            best = int(len(self.population) * self.keep_ratio)
            del self.population[best:] # remove worst

            babies = self.mate_in_pairs()
            self.population.extend(babies)
            self.population.extend(elite)
            # print("new born babies")
            # self.print_best_snakes(self.population)
            # print("new born babies")






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

    def print_best_snakes(self, population, iterator=0):
        for i, pop in enumerate(population[:10], start=1):
            print(f"{i}# fitness: {pop.game.fitness} score: {pop.game.snake.score} steps: {pop.game.step}")


if __name__ == '__main__':
    ga = GeneticAlgorithm(population_size=50, generations=10, elite=0)
    ga.initialize_population()
    ga.create_population()
    ga.print_best_snakes(ga.population)
