from copy import deepcopy
from enum import Enum
import numpy as np


class CrossOverType(Enum):
    SINGLE_POINT_CROSSOVER = 1
    LINEAR_CROSSOVER = 2
    SINGLE_ARITHMETIC_CROSSOVER = 3
    NONE = 4


class CrossOver:
    def __init__(self):
        self.linear_parameters = [(0.5, 0.5), (1.5, -0.5), (-0.5, 1.5)]
        self.single_arithmetic_parameter = 0.5

    def single_point_crossover(self, population):
        new_population = deepcopy(population)
        for simulation in new_population:
            parent_change_index = np.random.choice(len(list(simulation.weights.keys())))
            parents = [new_population[np.random.randint(len(new_population))], new_population[np.random.randint(len(new_population))]]
            for index, weight in enumerate(simulation.weights.keys()):
                if index > parent_change_index:
                    simulation.weights[weight] = parents[0].weights[weight]
                else:
                    simulation.weights[weight] = parents[1].weights[weight]
        return new_population

    def linear_crossover(self, population):
        new_population = deepcopy(population)
        parent = lambda x: new_population[np.random.randint(len(new_population))].weights[x]
        for simulation in new_population:
            weight_key = np.random.choice(list(simulation.weights.keys()))
            parents = [parent(weight_key), parent(weight_key)]
            weight_val_proposal = [(params[0]*parents[0]+params[1]*parents[1]) for params in self.linear_parameters]
            simulation.weights[weight_key] = np.random.choice(weight_val_proposal)
        return new_population

    def single_arithmetic_crossover(self, population):
        new_population = deepcopy(population)
        for simulation in new_population:
            weight_key = np.random.choice(list(simulation.weights.keys()))
            parents = [new_population[np.random.randint(len(new_population))].weights[weight_key], new_population[np.random.randint(len(new_population))].weights[weight_key]]
            weight_val_proposal = [self.single_arithmetic_parameter*parents[f_parent]+(1-self.single_arithmetic_parameter)*parents[s_parent] for f_parent, s_parent in [(0, 1), (1, 0)]]
            simulation.weights[weight_key] = np.random.choice(weight_val_proposal)
        return new_population

    def no_crossover(self, population):
        new_population = deepcopy(population)
        return new_population

    def return_cross_over_type(self, cross_over_type):
        if cross_over_type == CrossOverType.SINGLE_POINT_CROSSOVER:
            return self.single_point_crossover
        elif cross_over_type == CrossOverType.SINGLE_ARITHMETIC_CROSSOVER:
            return self.single_arithmetic_crossover
        elif cross_over_type == CrossOverType.LINEAR_CROSSOVER:
            return self.linear_crossover
        else:
            return self.no_crossover
