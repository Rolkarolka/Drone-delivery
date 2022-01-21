from enum import Enum
import numpy as np


class CrossOverType(Enum):
    SINGLE_POINT_CROSSOVER = 1
    LINEAR_CROSSOVER = 2
    BLENDED_CROSSOVER = 3
    NONE = 4


class CrossOver:
    def __init__(self):
        self.linear_parameters = [(0.5, 0.5), (1.5, -0.5), (-0.5, 1.5)]
        self.single_arithmetic_parameter = 0.5

    def single_point_crossover(self, population):
        for simulation in population:
            parent_change_index = np.random.choice(len(list(simulation.weights.keys())))
            parents = [population[np.random.randint(len(population))], population[np.random.randint(len(population))]]
            for index, weight in enumerate(simulation.weights.keys()):
                if index > parent_change_index:
                    simulation.weights[weight] = parents[0].weights[weight]
                else:
                    simulation.weights[weight] = parents[1].weights[weight]

    def linear_crossover(self, population):
        for simulation in population:
            weight_key = np.random.choice(list(simulation.weights.keys()))
            parents = [population[np.random.randint(len(population))].weights[weight_key], population[np.random.randint(len(population))].weights[weight_key]]
            weight_val_proposal = [params[0]*parents[0]+params[1]*parents[1] for params in self.linear_parameters]
            simulation.weights[weight_key] = np.random.choice(weight_val_proposal)
        return population

    def single_arithmetic_crossover(self, population):
        for simulation in population:
            weight_key = np.random.choice(list(simulation.weights.keys()))
            parents = [population[np.random.randint(len(population))].weights[weight_key], population[np.random.randint(len(population))].weights[weight_key]]
            weight_val_proposal = [self.single_arithmetic_parameter*parents[f_parent]+(1-self.single_arithmetic_parameter)*parents[s_parent] for f_parent, s_parent in [(0, 1), (1, 0)]]
            simulation.weights[weight_key] = np.random.choice(weight_val_proposal)
        return population

    def no_crossover(self, population):
        return population

    def return_cross_over_type(self, cross_over_type):
        if cross_over_type == CrossOverType.SINGLE_POINT_CROSSOVER:
            return self.single_point_crossover
        elif cross_over_type == CrossOverType.BLENDED_CROSSOVER:
            return self.single_arithmetic_crossover
        elif cross_over_type == CrossOverType.LINEAR_CROSSOVER:
            return self.linear_crossover
        else:
            return self.no_crossover
