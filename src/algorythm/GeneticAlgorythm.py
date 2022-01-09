from copy import deepcopy

from algorythm import Simulation, SimulationParameters
import numpy as np
import random
import logging

from algorythm.SimulationWeights import SimulationWeights


class GeneticAlgorythm:
    def __init__(self, filename, population_size, max_generations, elite_size=5, tournament_size=2):
        self.sim_consts = SimulationParameters.from_file(filename)
        self.max_generations = max_generations
        self.population_size = population_size
        self.elite_size = elite_size
        self.tournament_size = tournament_size
        self.algorithm()

    def algorithm(self):
        t = 0
        population = self.initialize_population()
        rating = self.evaluation(population)
        while t < self.max_generations:
            logging.debug(f"Max score in current generation {t}: {max([simulation.score for simulation in population])}")
            t_population = self.tournament_selection(population)
            m_population = self.mutation(t_population)
            population = self.elite_succession(rating, m_population)
            population = self.reset_simulations(population)
            rating = self.evaluation(population)
            t += 1
        best_simulation = max(population, key=lambda simulation: simulation.score)
        logging.debug(f"______ OUTPUT _____"
                      f"\nMax score in last generation {t}: {best_simulation.score}"
                      f"\nWeights "
                      f"values: {best_simulation.weights}\n_____________________________")

    def initialize_population(self):
        population = []
        for i in range(self.population_size):
            population.append(Simulation(self.sim_consts, SimulationWeights.initialize_weights()))
        return population

    def tournament_selection(self, population):
        new_population = []
        for _ in population:
            opponents = [population[np.random.randint(len(population))] for _ in range(self.tournament_size)]
            new_population.append(deepcopy(max(opponents, key=lambda single_simulation: single_simulation.score)))
        return new_population

    @staticmethod
    def evaluation(population):
        for simulation in population:
            simulation.run()
        rated = sorted(population, key=lambda single_simulation: single_simulation.score)
        rated.reverse()
        return rated

    @staticmethod
    def mutation(population):
        for simulation in population:
            # choose which and how many of weights will be muted
            weights_to_be_muted = random.sample(list(simulation.weights), random.randint(0, len(simulation.weights.keys())))
            # mute chosen
            for weight in weights_to_be_muted:
                simulation.weights[weight] = np.random.normal(0, 1)
        return population

    def elite_succession(self, last_population, current_population):
        return last_population[0:self.elite_size] + current_population[0:-self.elite_size]

    def reset_simulations(self, population):
        return [Simulation(self.sim_consts, simulation.weights) for simulation in population]
