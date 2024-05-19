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
        self.step = 1
        self.death = 0
        self.total_score = 0
        self.quick_food = 0



    @property
    def fitness(self):
        score_weight = 200
        steps_weight = 0.1
        death_penalty = 0.1
        exploration = 0
        quick_food_weight = 200
        rep_weight = 10
        same_move = -(self.snake.wriggle_score + self.snake.repetition_score) / 2
        rep_bonus = 0
        wrig_bonus = 0
        if self.snake.wriggle_score == 0:
            wrig_bonus = 10
        if self.snake.repetition_score == 0:
            rep_bonus = 10
        # quick_food = self.quick_food * quick_food_weight
        # rep = (-self.snake.repetition_score / rep_weight)
        # death = -(self.death)
        score = (self.snake.score * score_weight)
        fitness = (score+same_move+wrig_bonus+rep_bonus)
        if fitness < 0:
            fitness = 0
        return fitness

    def run(self):
        running = True
        # self.snake.debug()

        while running:
            message=""
            # valid_moves = self.snake.calculate_valid_moves()
            next_move = self.controller.update()
            # print(next_move)
            self.step += 1
            self.snake.moves_without_food += 1
            # next_move = random.choice(valid_moves) if valid_moves else None
            if next_move:
                self.snake.v = next_move
            else:
                running = False
            if next_move: self.snake.v = next_move
            self.snake.move()
            #+=
            self.snake.moves_without_food += 1
            self.snake.step_game += 1
            if not self.snake.p.within(self.grid):
                running = False
                message = 'Game over! You crashed into the wall!'
                self.death += 1
                self.snake.step_game = 0
                # self.snake.moves_without_food = 0
            if self.snake.cross_own_tail:
                running = False
                message = 'Game over! You hit your own tail!'
                self.snake.step_game = 0
                self.snake.moves_without_food = 0
            if self.snake.p == self.food.p:
                self.snake.add_score()
                self.food = Food(game=self)
                self.snake.moves_without_food - 5
                if self.snake.step_game > 20:
                    self.quick_food += 1
                # self.snake.moves_without_food = 0
                message = 'Yum 1 food eaten'
            if self.snake.moves_without_food > self.snake.max_moves_without_food:
                self.snake.score = 0
                running = False
                self.death += 1
                # self.snake.moves_without_food = 0
                self.snake.step_game = 0
                message = 'Game over! Took too many moves without eating!'
        # if self.snake.score > 0:
        # print(f'{message} ... Score: {self.snake.score}....')


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
        self.moves_without_food = 1
        #Starting point is last move to begin with
        self.last_move = Vector(0, 0)
        self.opposite_move_count = 0
        self.direction_changes = 0
        self.max_moves_without_food = 200
        self.step_game = 0
        self.repetition_count = 0
        self.repetition_score = 0
        self.wriggle = 0
        self.wriggle_score = 0
    def direction(self, vector):
        if vector == Vector(0, 1):
            return 'NORTH'
        elif vector == Vector(1, 0):
            return 'EAST'
        elif vector == Vector(0, -1):
            return 'SOUTH'
        elif vector == Vector(-1, 0):
            return 'WEST'
        elif vector == Vector(0,0): #start
            pass
        else:
            raise ValueError(f"Unknown direction for vector {vector}")

    def same_direction_count(self):
        # print("Move this way",self.v,"last move",self.last_move)
        if self.last_move is not None and self.direction(self.v) == self.direction(self.last_move):
            self.repetition_count += 1
            # print(self.repetition_count)
            if self.repetition_count > 11:
                self.repetition_score +=1
                self.repetition_count = 0
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
            print(self.v)
            print(self.last_move)
            if current_direction == opposite_direction.get(last_direction):
                self.opposite_move_count += 1
                print(self.opposite_direction_count)



    def move(self):
        self.same_direction_count()
        self.wriggle_walk()

        # print("rep current",self.repetition_count)
        # print("rep score",self.repetition_score)
        # print("wriggle score", self.wriggle_score)
        # self.opposite_direction_count()
        # if self.last_move is not None and self.v != self.last_move:
        #     self.direction_changes += 1
        # if self.opposite_move_count > 5:
        #     valid_moves = self.calculate_valid_moves()
        #     current_direction = self.direction(self.v)
        #     self.v = self.choose_valid_move(valid_moves, current_direction)
        self.p = self.p + self.v
        # print("MOVE",self.last_move,self.v)
        self.last_move = self.v
        # print("current",self.v, "last",self.last_move)

    @property
    def get_score(self):
        return self.score

    def get_last_move(self):
        return self.last_move


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

    def wriggle_walk(self):
        specific_from_vector = Vector(0, -1)
        specific_to_vector = Vector(-1, 0)

        if self.last_move == specific_from_vector and self.v == specific_to_vector:
            self.wriggle += 1

        if self.wriggle > 4:
            self.wriggle_score += 1
            self.wriggle = 0
            print("Specific transition occurred more than 5 times")



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
