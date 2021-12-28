from copy import deepcopy

from algorythm import Simulation, SimulationParameters
import numpy as np
import random


class GeneticAlgorythm:
    def __init__(self, filename, population_size, max_generations, elite_size=5, tournament_size=2):
        self.sim_consts = self.get_simulation_from_filename(filename)
        self.max_generations = max_generations
        self.population_size = population_size
        self.elite_size = elite_size
        self.tournament_size = tournament_size
        self.algorithm()

    @staticmethod
    def get_simulation_from_filename(filename):
        simulation_parameters = SimulationParameters()
        simulation_parameters.load_file(filename)
        return simulation_parameters

    def algorithm(self):
        t = 0
        population = self.initialize_population()
        rating = self.evaluation(population)
        while t < self.max_generations:
            t_population = self.tournament_selection(population)
            m_population = self.mutation(t_population)
            population = self.elite_succession(rating, m_population)
            rating = self.evaluation(population)
            t += 1

    def initialize_population(self):
        population = []
        for i in range(self.population_size):
            population.append(Simulation(self.sim_consts, self.initialize_weights()))
        return population

    @staticmethod
    def initialize_weights():
        """
        "wzl": weight of the number of products in the order Z_L
        "wzr": weight of order variety Z_R - quantity of product types in the order under consideration
        "wzp": weight of the popularity of Z_P products - availability in warehouses included in the order under consideration
        "wzo": weight of the distance between the current position of the aircraft and the target Z_O
        "wml": weight of the quantity of the product available in the warehouse M_L
        "wmz": weight of the distance between the warehouse location and the M_OZ destination point
        "wmd": weight of the distance between the current position of the drone and the M_OD magazine
        """
        return {
            "wzl": np.random.normal(0, 1),
            "wzr": np.random.normal(0, 1),
            "wzp": np.random.normal(0, 1),
            "wzo": np.random.normal(0, 1),
            "wml": np.random.normal(0, 1),
            "wmz": np.random.normal(0, 1),
            "wmd": np.random.normal(0, 1)
        }

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
