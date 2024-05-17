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
        self.moves_without_food = 0
        self.max_moves_without_food = 60


    @property
    def fitness(self):
        if self.snake.score == 0:
            return 0  # or handle this case according to your logic
        fit = (self.step / (self.snake.score * 20)) + (self.snake.direction_changes * 0.1)
        return fit

    def run(self):
        running = True
        # self.snake.debug()

        while running:
            # valid_moves = self.snake.calculate_valid_moves()
            next_move = self.controller.update()
            print(next_move)
            self.step += 1
            self.moves_without_food += 1
            # next_move = random.choice(valid_moves) if valid_moves else None
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
                self.moves_without_food = 0
            if self.moves_without_food > self.max_moves_without_food:
                self.snake.score = 0
                running = False
                message = 'Game over! Took too many moves without eating!'
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
        self.last_move = None
        self.repetion_count = 0
        self.opposite_move_count = 0
        self.direction_changes = 0

    def direction(self, vector):
        if vector == Vector(0, 1):
            return 'NORTH'
        elif vector == Vector(1, 0):
            return 'EAST'
        elif vector == Vector(0, -1):
            return 'SOUTH'
        elif vector == Vector(-1, 0):
            return 'WEST'
        else:
            raise ValueError(f"Unknown direction for vector {vector}")

    def same_direction_count(self):
        if self.last_move is not None and self.direction(self.v) == self.direction(self.last_move):
            self.repetition_count += 1
        else:
            self.repetition_count = 0  # Reset if direction changes

    def opposite_direction_count(self):
        opposite_direction = {
            'NORTH': 'SOUTH',
            'EAST': 'WEST',
            'SOUTH': 'NORTH',
            'WEST': 'EAST'
        }

        if self.last_move is not None:
            current_direction = self.direction(self.v)
            last_direction = self.direction(self.last_move)
            if current_direction == opposite_direction.get(last_direction):
                self.opposite_move_count += 1



    def move(self):
        self.same_direction_count()
        self.opposite_direction_count()
        if self.last_move is not None and self.v != self.last_move:
            self.direction_changes += 1
        if self.opposite_move_count > 5:
            valid_moves = self.calculate_valid_moves()
            current_direction = self.direction(self.v)
            self.v = self.choose_valid_move(valid_moves, current_direction)
        self.p = self.p + self.v
        self.last_move = self.v

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

        # Check if moving up is valid
        if self.v != Vector(0, -1):  # Ensure it's not moving downwards
            move_up = Vector(0, 1)
            valid_moves.append(move_up)

        # Check if moving down is valid
        if self.v != Vector(0, 1):  # Ensure it's not moving upwards
            move_down = Vector(0, -1)
            valid_moves.append(move_down)

        # Check if moving left is valid
        if self.v != Vector(1, 0):  # Ensure it's not moving right
            move_left = Vector(-1, 0)
            valid_moves.append(move_left)

        # Check if moving right is valid
        if self.v != Vector(-1, 0):  # Ensure it's not moving left
            move_right = Vector(1, 0)
            valid_moves.append(move_right)

        return valid_moves

    def choose_valid_move(self, valid_moves: List[Vector], current_direction: str) -> Vector:
        """
        Choose a valid move that is not opposite to the current direction.
        """
        opposite_direction = {
            'NORTH': Vector(0, -1),
            'EAST': Vector(-1, 0),
            'SOUTH': Vector(0, 1),
            'WEST': Vector(1, 0)
        }

        # Include the current direction but exclude the opposite direction
        valid_moves = [move for move in valid_moves if move != opposite_direction[current_direction] or move == self.v]

        # If no valid moves remain, just return the current direction (safe fallback)
        if not valid_moves:
            return self.v

        return random.choice(valid_moves)
