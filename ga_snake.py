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



# def mate_in_pairs(population):     # Extracting the list of keys to access the creatures in order    keys = list(creatures_dict.keys())          # Iterate over the keys in steps of 2 to get pairsfor i in range(0, len(keys) - 1, 2):         creature1 = creatures_dict[keys[i]]         creature2 = creatures_dict[keys[i+1]]         creature1.mate(creature2)
#     babies = []
#     for i in range(0, len(population) - 1, 2):
#         dad = population[i]
#         mom = population[i+1]
#         baby = dad.model + mom.model
#         baby2 = dad.model + mom.model
#         baby.mutate(0.05)
#         baby2.mutate(0.05)
#         babies.append(baby)
#         babies.append(baby2)
#     # print(babies)
#     return babies

def have_same_object_id(list1, list2):
    # Create sets of object IDs for both lists
    ids_list1 = {id(obj): obj for obj in list1}
    ids_list2 = {id(obj): obj for obj in list2}

    # Check for intersection of the two sets
    common_ids = set(ids_list1.keys()).intersection(set(ids_list2.keys()))

    if common_ids:
        print("Common object IDs:")
        for obj_id in common_ids:
            obj1 = ids_list1[obj_id]
            obj2 = ids_list2[obj_id]
            print(f"Object ID: {obj_id}, Object in List1: {obj1}, Object in List2: {obj2}")
            # Access the method or attribute
            print(f"Fitness (List1): {obj1.game.fitness}")
            print(f"Fitness (List2): {obj2.game.fitness}")
        return True
    else:
        return False


class GeneticAlgorithm:
    def __init__(self, population_size=10, generations=2,keep_ratio=0.1, elite=2, mutation=0.08):
        self.population_size = population_size
        self.generations = generations
        self.population = []
        self.elite = elite
        self.keep_ratio=keep_ratio
        self.mutation = mutation


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
            # for controller in self.population:

            #         print("GEN")
            #         print(f"# step: {controller.game.step} fitness {controller.game.fitness} score: {controller.game.snake.score} ")
            #         print("GEN")
            self.generations = self.generations-1
            print("gen",self.generations)
            new_pop=[]
            for controller in self.population:
                game = SnakeGame()
                game.controller = controller
                controller.game = game
                game.run()
                # print(controller.game.fitness)
                # if len(new_pop) > 0:
                #     self.print_max_fitness_value(new_pop)
                new_pop.append(controller)

            #######################
            new_pop = sorted(new_pop, key=lambda x: x.game.fitness, reverse=True)
            # self.print_edge("first",new_pop)
            if self.elite > 0:
                elite = new_pop[:self.elite]
                del new_pop[-self.elite:]
                new_pop.extend(elite)
            # self.print_edge("first",new_pop)
            # self.print_controller(new_pop)
            # new_pop = new_pop[self.elite:]# removes from list
            best = int(len(new_pop) * self.keep_ratio)
            del new_pop[best:] # remove worst slices to the end of list
            self.print_controller(new_pop)
            # if self.elite > 0:
            #     have_same_object_id(elite, new_pop)
            # print("LENG",len(new_pop))
            # new_pop = new_pop[:len(new_pop) // 2]
            # self.print_fitness_values(new_pop)
            new_controllers = []

            new_models = self.mate_in_pairs(new_pop)
            for model in new_models:
                game = SnakeGame()
                controller = GAController(game, model=model)
                new_controllers.append(controller)
            # print("new models",len(new_models))
            #.append when make them contain the same objects

            new_controllers.extend(new_pop)
            self.population = new_controllers
            print("new controllers",len(new_controllers))
    def print_controller(self, pop):
        for i, controller in enumerate(pop, start=1):
            print(f"Controller {i+1}quick food:{controller.game.quick_food} :step:{controller.game.step} score {controller.game.snake.score} Fitness = {controller.game.fitness} repetion steps{controller.game.snake.repetition_count} wriggle:{controller.game.snake.wriggle_score}")
    def mate_in_pairs(self,population):
        babies = []
        size = self.population_size - len(population)
        size = size - self.elite
        while len(babies) < size:
            dad, mom = random.sample(self.population, 2)
            baby = dad.model + mom.model
            baby2 = dad.model + mom.model
            baby.mutate(self.mutation)
            baby2.mutate(self.mutation)
            babies.append(baby)
            babies.append(baby)
        return babies
    def find_best_controller(self):
        sorted_population = sorted(self.population, key=lambda x: x.game.fitness, reverse=True)
        best_controllers = sorted_population[:30]
        return best_controllers
    def print_fitness_values(self, population):
        print("Fitness values of the current population:")
        population = sorted(population, key=lambda x: x.game.fitness, reverse=False)
        for i, controller in enumerate(population):
            print(f"Controller {i+1} quick_food {controller.game.quick_food}:step:{controller.game.step} score {controller.game.snake.score} Fitness = {controller.game.fitness} repetion steps{controller.game.snake.repetition_count} wriggle:{controller.game.snake.wriggle_score}")
    def print_max_fitness_value(self, population):
        controller = max(controller.game.fitness for controller in population)

        print(f"Controller:step:{controller.game.step} score {controller.game.snake.score} Fitness = {controller.game.fitness} repetion steps{controller.game.snake.repetition_count} wriggle:{controller.game.snake.wriggle_score}")

    def print_edge(self, extreme_type, population):
        if extreme_type == "first":
            controller = population[0]
        elif extreme_type == "last":
            controller = population[-1]
        else:
            raise ValueError("Invalid extreme type. Use 'first' or 'last'.")


        print(f"FIRST OR LAST {controller.game.fitness} {controller} ")
        print(f"Controller:step:{controller.game.step} score {controller.game.snake.score} Fitness = {controller.game.fitness} repetion steps{controller.game.snake.repetition_count} wriggle:{controller.game.snake.wriggle_score}")


if __name__ == '__main__':
    ga = GeneticAlgorithm(population_size=50, generations=100, keep_ratio=0.1, elite=2)
    ga.initialize_population()
    ga.evolve_generations()
    ga.print_fitness_values(ga.population)
    # ga.print_max_fitness_value(ga.population)
    # best_controllers = ga.find_best_controller()
    # for i, controller in enumerate(best_controllers, start=1):
    #         print(f"{i}# fit {controller.game.fitness} score: {controller.game.snake.score} steps: {controller.game.step}wriggle score: {controller.game.snake.wriggle_score} repetition scores: {controller.game.snake.repetition_score}")



    # print("Best Controller Fitness:", best_controller.game.fitness)
