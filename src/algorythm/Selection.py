from enum import Enum
import numpy as np
from copy import deepcopy


class SelectionType(Enum):
    TOURNAMENT_SELECTION = 1
    ROULETTE_WHEEL_SELECTION = 2
    RANK_SELECTION = 3


class Selection:
    def __init__(self, tournament_size=2, stayed_ranked_population_percent=0.5):
        self.tournament_size = tournament_size
        self.stayed_ranked_population_percent = stayed_ranked_population_percent

    def tournament_selection(self, population):
        new_population = []
        for _ in population:
            opponents = [population[np.random.randint(len(population))] for _ in range(self.tournament_size)]
            new_population.append(deepcopy(max(opponents, key=lambda single_simulation: single_simulation.score)))
        return new_population

    def roulette_wheel_selection(self, population):
        score_sum = sum([simulation.score for simulation in population])
        simulation_probabilities = [simulation.score / score_sum for simulation in population]
        return np.random.choice(population, p=simulation_probabilities)

    def rank_selection(self, population):
        best_simulations = population[:int(self.stayed_ranked_population_percent * len(population))]
        return np.random.choice(best_simulations)

    def no_selection(self, population):
        return population

    def return_selection_type(self, selection_type):
        if selection_type == SelectionType.TOURNAMENT_SELECTION:
            return self.tournament_selection
        elif selection_type == SelectionType.RANK_SELECTION:
            return self.rank_selection
        elif selection_type == SelectionType.ROULETTE_WHEEL_SELECTION:
            return self.roulette_wheel_selection
        else:
            return self.no_selection
