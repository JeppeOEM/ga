import random
from typing import Protocol, Tuple, List, Sequence #Sequence is a type for deque
import numpy
import numpy as np
from ga_models.ga_protocol import GAModel
from ga_models.activation import sigmoid, tanh, softmax
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.utils import to_categorical
from sklearn.neural_network import MLPClassifier
class SimpleModel(GAModel):
    #  *, the * means that you must pass the parameter with a keyword, in this case dims="value"
    def __init__(self, *, dims: Tuple[int, ...], game):
        assert len(dims) >= 2, 'Error: dims must be two or higher.'
        self.dims = dims
        self.DNA = []
        self.game = game
        self.neural_network = self.create_neural_network()
        #populate with random numbers
        for i, dim in enumerate(dims):
            if i < len(dims) - 1:
                number = np.random.rand(dim, dims[i+1])
                print(number)
                self.DNA.append(number)



    #the @ symbol is used for matrix multiplication when used between two arrays or matrices.
    #supported by libraries like NumPy.
    def update(self, obs: Sequence) -> Tuple[int, ...]:
        x = obs
        self.game.food
        self.game.snake
        self.game.grid
        for i, layer in enumerate(self.DNA):
            print("DNA!!!!!!!!!!!",self.DNA)
            print("DNA LAYER $$$$$$$$$$$$$$$$$$",layer)
            if not i == 0:
                #tanh = hyperbolic tangent function
                #often used as a activation fucntion ranges from -1 to 1
                x = tanh(x)
                print("TANH",x)
            #multiplicating
            # x = x @ layer
            x = self.neural_network.predict(x.reshape(1, -1))
            x = x.flatten()
            print("#######################    x:", x)
            #softmax converts a vector of numbers into a probability distribution
        return softmax(x)

    def action(self, obs: Sequence):
        return self.update(obs).argmax()

    def mutate(self, mutation_rate) -> None:
        if random.random() < mutation_rate:
            random_layer = random.randint(0, len(self.DNA) - 1)
            row = random.randint(0, self.DNA[random_layer].shape[0] - 1)
            col = random.randint(0, self.DNA[random_layer].shape[1] - 1)
            self.DNA[random_layer][row][col] = random.uniform(-1, 1)

    def __add__(self, other):
        baby_DNA = []
        for mom, dad in zip(self.DNA, other.DNA):
            if random.random() > 0.5:
                baby_DNA.append(mom)
            else:
                baby_DNA.append(dad)
        baby = type(self)(dims=self.dims)
        baby.DNA = baby_DNA
        return baby

    def DNA(self):
        return self.DNA

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


    def create_neural_network(self):
        model = MLPClassifier(hidden_layer_sizes=(64, 32),
                              activation='relu',
                              random_state=42)
        return model