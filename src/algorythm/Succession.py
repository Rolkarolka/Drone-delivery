from copy import deepcopy
from enum import Enum
import numpy as np


class SuccessionType(Enum):
    ELITE_SUCCESSION = 1
    GENERATIONAL_SUCCESSION = 2
    STEADY_STATE_SUCCESSION = 3


class Succession:
    def __init__(self, elite_size=2, stayed_population_percent=0.5):
        self.elite_size = elite_size
        self.stayed_population_percent = stayed_population_percent
        self.tournament_size = 2

    def elite_succession(self, last_population, current_population):
        return last_population[0:self.elite_size] + current_population[0:-self.elite_size]

    def generational_succession(self, last_population, current_population):
        return current_population

    def steady_state_succession(self, last_population, current_population):
        new_population = []
        amount_stayed_population = int(len(last_population) * self.stayed_population_percent)
        for _ in range(amount_stayed_population):
            opponents = [np.random.choice(last_population, 1), np.random.choice(current_population, 1)]
            new_population.append(deepcopy(max(opponents, key=lambda single_simulation: single_simulation.score)))
        return new_population

    def return_succession_type(self, succession_type):
        if succession_type == SuccessionType.ELITE_SUCCESSION:
            return self.elite_succession
        elif succession_type == SuccessionType.GENERATIONAL_SUCCESSION:
            return self.generational_succession
        elif succession_type == SuccessionType.STEADY_STATE_SUCCESSION:
            return self.steady_state_succession
