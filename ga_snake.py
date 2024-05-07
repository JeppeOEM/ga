#!/usr/bin/env python


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

for _ in range(10):
    game = SnakeGame()
    game.fitness
    population.append(game)

# Run each game in the population
for game in population:
    controller = GAController(game)
    game.run()



population.sort(key=get_fitness, reverse=True)
population = remove_lowest_values(population)


print(population)

def generations(generations, pop_size):
    gens = []
    pop = [TSM(cities_map) for _ in range(pop_size)]

    for generation in range(generations):
        reduced_pop = kill_half(pop)
        offspring = create_offsprings(reduced_pop)
        # print(offspring)
        # print(reduced_pop)
        new_gen = reduced_pop.append(offspring)
        gens.append(new_gen)
        print(len(gens))

generations(10, 100)