import random
from typing import List, Protocol
from vector import Vector
import pygame
from game_controller import GameController
from ga_models.ga_simple import SimpleModel

class GAController(GameController):
    def __init__(self, game, display=False):
        self.display = display
        self.game = game
        self.model =  SimpleModel(dims=(7,4,4,4))
        #set refrence inside the game object to the controller
        self.game.controller = self
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

        # score
        s = self.game.snake.score

        obs = (dn, de, ds, dw, dfx, dfy, s)

        current_direction = self.game.snake.direction()
        # print(current_direction)
        next_move_index = self.model.action(obs)
        next_move = self.action_space[next_move_index]
        valid_moves = []
        if current_direction == 'NORTH':
            valid_moves = ['NORTH', 'EAST', 'WEST']
        elif current_direction == 'EAST':
            valid_moves = ['NORTH', 'EAST', 'SOUTH']
        elif current_direction == 'SOUTH':
            valid_moves = ['EAST', 'SOUTH', 'WEST']
        elif current_direction == 'WEST':
            valid_moves = ['NORTH', 'SOUTH', 'WEST']

        # If the next move is not valid, choose a random valid move
        # if next_move not in valid_moves:
        #     next_move = random.choice(valid_moves)
        # action space

        # print(next_move)
        # test=self.model.action(obs)
        # print("next",test)
        # next_move = self.action_space[test]

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

    # def action_space(self, obj):
    #     return

    def __str__(self):
        return f"GAController(food={self.game.food},food={self.game.snake}, display={self.display})"
