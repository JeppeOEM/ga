import math
import random
from collections import deque
from typing import List, Protocol
import pygame
from vector import Vector
from game_controller import HumanController


class SnakeGame:
    def __init__(self, xsize: int=30, ysize: int=30, scale: int=15):
        self.grid = Vector(xsize, ysize)
        self.scale = scale
        self.snake = Snake(game=self)
        self.food = Food(game=self)
        self.step = 0

    @property
    def fitness(self):
        if self.snake.score == 0:
            return 0  # or handle this case according to your logic
        fit = self.step / (self.snake.score * 10)
        return fit

    def run(self):
        running = True
        self.snake.debug()

        while running:
            valid_moves = self.snake.calculate_valid_moves()
            next_move = self.controller.update()
            self.step += 1
            next_move = random.choice(valid_moves) if valid_moves else None
            if next_move:
                self.snake.v = next_move
            else:
                running = False
            if next_move: self.snake.v = next_move
            self.snake.move()
            if not self.snake.p.within(self.grid):
                running = False
                message = 'Game over! You crashed into the wall!'
            if self.snake.cross_own_tail:
                running = False
                message = 'Game over! You hit your own tail!'
            if self.snake.p == self.food.p:
                self.snake.add_score()
                self.food = Food(game=self)
        print(f'{message} ... Score: {self.snake.score}....')


class Food:
    def __init__(self, game: SnakeGame):
        self.game = game
        self.p = Vector.random_within(self.game.grid)


class Snake:
    def __init__(self, *, game: SnakeGame):
        self.game = game
        self.score = 0
        self.v = Vector(0, 0)
        self.body = deque()
        self.body.append(Vector.random_within(self.game.grid))

    def direction(self):
        if self.v == Vector(0, 1):
            return 'NORTH'
        elif self.v == Vector(1, 0):
            return 'EAST'
        elif self.v == Vector(0, -1):
            return 'SOUTH'
        elif self.v == Vector(-1, 0):
            return 'WEST'
        else:
            return None  # Handle undefined direction
    def move(self):
        self.p = self.p + self.v
    @property
    def get_score(self):
        return self.score


    @property
    def cross_own_tail(self):
        try:
            self.body.index(self.p, 1)
            return True
        except ValueError:
            return False

    @property
    def p(self):
        return self.body[0]

    @p.setter
    def p(self, value):
        self.body.appendleft(value)
        self.body.pop()

    def add_score(self):
        self.score += 1
        tail = self.body.pop()
        self.body.append(tail)
        self.body.append(tail)

    def debug(self):
        print('===')
        for i in self.body:
            print(str(i))
    def calculate_valid_moves(self) -> List[Vector]:
        """
        Calculate valid moves based on the current state of the snake.
        """
        valid_moves = []

        # Print snake's body positions
        # print("Snake's body positions:", self.body)
        # Print current position
        # print("Current position:", self.p)


        # Check if moving up is valid
        if self.v != Vector(0, -1):  # Ensure it's not moving downwards
            valid_moves.append(Vector(0, 1))

        # Check if moving down is valid
        if self.v != Vector(0, 1):  # Ensure it's not moving upwards
            valid_moves.append(Vector(0, -1))

        # Check if moving left is valid
        if self.v != Vector(1, 0):  # Ensure it's not moving right
            valid_moves.append(Vector(-1, 0))

        # Check if moving right is valid
        if self.v != Vector(-1, 0):  # Ensure it's not moving left
            valid_moves.append(Vector(1, 0))

        return valid_moves