import random
from typing import List, Protocol, Tuple
from vector import Vector
import pygame
from game_controller import GameController
from ga_models.ga_simple import SimpleModel

class GAController(GameController):
    def __init__(self, game, model=None, display=False):
        self.display = display
        self.game = game
        if model:
            self.model = model  # Use the provided model
        else:
            self.model = SimpleModel(dims=(11, 9, 15, 3))
        #set refrence inside the game object to the controller
        self.game.controller = self
        # self.game.snake.controller = self
        # print(self.game.debug())
        # self.action_space = (Vector(0, -1), Vector(0, 1), Vector(1, 0), Vector(-1, 0))
        self.action_space = (Vector(0, -1), Vector(0, 1), Vector(1, 0), Vector(-1, 0))


        if self.display:
            pygame.init()
            self.screen = pygame.display.set_mode((game.grid.x * game.scale, game.grid.y * game.scale))
            self.clock = pygame.time.Clock()
            self.color_snake_head = (0, 255, 0)
            self.color_food = (255, 0, 0)
            #Possible directions to move
            self.step_count = 0

    def __del__(self):
        if self.display:
            pygame.quit()
    def play_again(self):
        self.game.run()

    def update(self) -> Vector:
        # observation space

        # delta north, east, south, west
        dn = self.game.snake.p.y
        de = self.game.grid.x - self.game.snake.p.x
        ds = self.game.grid.y - self.game.snake.p.y
        dw = self.game.snake.p.x

        # delta food x and y
        dfx = self.game.snake.p.x - self.game.food.p.x
        dfy = self.game.snake.p.y - self.game.food.p.y
        #made with @property so last_move is = last_move()
        last_move = self.game.snake.last_move
        # print(last_move)
        # score
        s = self.game.snake.score

        if last_move is not None:
            if last_move == Vector(0, -1):  # Last move was up
                self.action_space = (Vector(-1, 0), Vector(1, 0), Vector(0, -1))  # Left, right, straight
            elif last_move == Vector(0, 1):  # Last move was down
                self.action_space = (Vector(1, 0), Vector(-1, 0), Vector(0, 1))  # Right, left, straight
            elif last_move == Vector(-1, 0):  # Last move was left
                self.action_space = (Vector(0, -1), Vector(0, 1), Vector(-1, 0))  # Straight, up, down
            elif last_move == Vector(1, 0):  # Last move was right
                self.action_space = (Vector(0, 1), Vector(0, -1), Vector(1, 0))  # Straight, down, up

    # Threats from borders: 1 if next to border, 0 otherwise
        tn = 1 if self.game.snake.p.y == 0 else 0  # Top border
        te = 1 if self.game.snake.p.x == self.game.grid.x - 1 else 0  # Right border
        ts = 1 if self.game.snake.p.y == self.game.grid.y - 1 else 0  # Bottom border
        tw = 1 if self.game.snake.p.x == 0 else 0  # Left border
        obs = (dn, de, ds, dw, dfx, dfy,tn,te,ts,tw, s)
        # print("north:",dn,"east:", de, "sourth",ds,"west", dw, dfx, dfy, s)

        # self.action_space = self.calculate_valid_moves()

        next_move = self.action_space[self.model.action(obs)]



        # display
        if self.display:
            self.screen.fill('black')
            for i, p in enumerate(self.game.snake.body):
                pygame.draw.rect(self.screen, (0, max(128, 255 - i * 12), 0), self.block(p))
            pygame.draw.rect(self.screen, self.color_food, self.block(self.game.food.p))
            pygame.display.flip()
            self.clock.tick(10)
        return next_move

    def block(self, obj):
        return (obj.x * self.game.scale,
                obj.y * self.game.scale,
                self.game.scale,
                self.game.scale)


    def calculate_valid_moves(self) -> Tuple[Vector, ...]:

        # Calculate valid moves based on the current state of the snake.

        if self.game.snake.last_move is None:
            return ()  # Return an empty tuple if last move is None
        else:
            last_move = self.game.snake.last_move

        # Define valid moves based on the last move
        valid_moves = ()

        # Check if moving up is valid
        if last_move != Vector(0, -1):
            move_up = Vector(0, 1)
            valid_moves += (move_up,)

        # Check if moving down is valid
        if last_move != Vector(0, 1):
            move_down = Vector(0, -1)
            valid_moves += (move_down,)

        # Check if moving left is valid
        if last_move != Vector(1, 0):
            move_left = Vector(-1, 0)
            valid_moves += (move_left,)

        # Check if moving right is valid
        if last_move != Vector(-1, 0):
            move_right = Vector(1, 0)
            valid_moves += (move_right,)

        return valid_moves

    def __str__(self):
        return f"__STR__:GAController(food={self.game.food},food={self.game.snake}, display={self.display})"
