import random
from collections import deque
from typing import Protocol
import pygame
from vector import Vector
from game_controller import HumanController
from typing import List


class SnakeGame:
    def __init__(self, xsize: int=30, ysize: int=30, scale: int=15):
        self.grid = Vector(xsize, ysize)
        self.scale = scale
        self.snake = Snake(game=self)
        self.food = Food(game=self)


    def run(self):
        running = True
        self.snake.debug()
        valid_moves = self.snake.calculate_valid_moves()
        while running:
            valid_moves = self.snake.calculate_valid_moves()  # Calculate valid moves
            next_move = random.choice(valid_moves) if valid_moves else None
            next_move = self.controller.update()
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
        print(f'{message} ... Score: {self.snake.score}')


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

    def move(self):
        self.p = self.p + self.v

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
        print("Snake's body positions:", self.body)
        # Print current position
        print("Current position:", self.p)


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
