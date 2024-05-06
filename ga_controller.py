from typing import Protocol
from vector import Vector
import pygame
from game_controller import GameController
from ga_models.ga_simple import SimpleModel
import numpy

class GAController(GameController):
    def __init__(self, game, display=True):
        self.display = display
        self.game = game
        self.model =  SimpleModel(dims=(7,4,4,7), game=self.game )
        #set refrence inside the game object to the controller
        self.game.controller = self
        # print(self.game.debug())
        # self.action_space = (Vector(0, -1), Vector(0, 1), Vector(1, 0), Vector(-1, 0))
        self.action_space = (Vector(0, -1), Vector(0, 1), Vector(1, 0), Vector(-1, 0))
        print(self.game.controller)
        if self.display:
            pygame.init()
            self.screen = pygame.display.set_mode((game.grid.x * game.scale, game.grid.y * game.scale))
            self.clock = pygame.time.Clock()
            self.color_snake_head = (0, 255, 0)
            self.color_food = (255, 0, 0)
            #Possible directions to move
    def observe_environment(self):
        # Observation space: relative position of the snake's head to the walls and the food
        # Position of the snake's head
        head_x, head_y = self.game.snake.p.x, self.game.snake.p.y

        # Distances to the walls
        distance_to_top_wall = head_y
        distance_to_bottom_wall = self.game.grid.y - head_y
        distance_to_left_wall = head_x
        distance_to_right_wall = self.game.grid.x - head_x

        # Relative position to the food
        food_x, food_y = self.game.food.p.x, self.game.food.p.y
        food_distance_x = food_x - head_x
        food_distance_y = food_y - head_y

        # Concatenate all observations into a tuple or list
        return np.array([distance_to_top_wall, distance_to_bottom_wall, distance_to_left_wall, distance_to_right_wall, food_distance_x, food_distance_y])
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
        print("obs:::::",obs)

        # action space

        next_move = self.action_space[self.model.action(obs)]
        print("##############################################################")
        print("##############################################################")
        print("next move!!!!!!!!!!!!!!!!!!!!!!",next_move)
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

    def action_space(self, obj):
        print(obj,"ACTION SPACE")
        return

    def __str__(self):
        return f"GAController(food={self.game.food},food={self.game.snake}, display={self.display})"