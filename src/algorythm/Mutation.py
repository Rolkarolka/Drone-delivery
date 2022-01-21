from enum import Enum
import numpy as np


class MutationType(Enum):
    UNIFORM_MUTATION = 1
    GAUSSIAN_MUTATION = 2
    CAUCHY_MUTATION = 3
    NONE = 4


class Mutation:

    def mutation(self, mutation_type, population):

        for simulation in population:
            amount_of_muted_weights = np.random.randint(0, len(simulation.weights))
            # choose which and how many of weights will be muted
            weights_to_be_muted = np.random.choice(list(simulation.weights.keys()), size=amount_of_muted_weights, replace=False)
            # mute chosen
            for weight in weights_to_be_muted:
                simulation.weights[weight] = mutation_type
        return population

    def uniform_mutation(self, population):
        return self.mutation(np.random.uniform(0, 1), population)

    def gaussian_mutation(self, population):
        return self.mutation(np.absolute(np.random.normal(0, 1)), population)

    def cauchy_mutation(self, population):
        return self.mutation(np.random.standard_cauchy(len(population)), population)

    def no_mutation(self, population):
        return population

    def return_mutation_type(self, mutation_type):
        if mutation_type == MutationType.UNIFORM_MUTATION:
            return self.uniform_mutation
        elif mutation_type == MutationType.GAUSSIAN_MUTATION:
            return self.gaussian_mutation
        elif mutation_type == MutationType.CAUCHY_MUTATION:
            return self.cauchy_mutation
        else:
            return self.no_mutation
