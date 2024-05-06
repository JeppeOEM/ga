#!/usr/bin/env python


from snake import SnakeGame
from ga_controller import GAController


population = []

# Create 100 instances of the Snake game and add them to the population
for _ in range(100):
    game = SnakeGame()
    population.append(game)

# Run each game in the population
for game in population:
    controller = GAController(game)
    game.run()