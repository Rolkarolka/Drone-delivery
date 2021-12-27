from src import Simulation, SimulationParameters
import numpy as np


class GeneticAlgorythm:
    def __init__(self, filename, population_size, max_generations):
        self.sim_consts = self.get_simulation_from_filename(filename)
        self.max_generations = max_generations
        self.population_size = population_size

        self.algorithm()

    @staticmethod
    def get_simulation_from_filename(filename):
        simulation_parameters = SimulationParameters()
        simulation_parameters.load_file(filename)
        return simulation_parameters

    def algorithm(self):
        t = 0
        population = self.initialize_population()
        # evaluate starting population
        rating = self.evaluate(population)
        while t < self.max_generations:
            t_population = self.tournament_selection(population)
            m_population = self.mutation(t_population)
            population = self.elite_succession(rating, m_population)
            rating = self.evaluate(population)
            t += 1


    def initialize_population(self):
        population = []
        # TODO: generation
        for i in range(self.population_size):
            population.append(Simulation(self.sim_consts, self.initialize_weights()))
        return population

    def initialize_weights(self):
        return {
            "wzl": np.random.normal(0, 1),  # weight of the number of products in the order Z_L
            "wzr": np.random.normal(0, 1),  # weight of order variety Z_R - quantity of product types in the order under consideration
            "wzp": np.random.normal(0, 1),  # weight of the popularity of Z_P products - availability in warehouses included in the order under consideration
            "wzo": np.random.normal(0, 1),  # weight of the distance between the current position of the aircraft and the target Z_O
            "wml": np.random.normal(0, 1),  # weight of the quantity of the product available in the warehouse M_L
            "wmz": np.random.normal(0, 1),  # weight of the distance between the warehouse location and the M_OZ destination point
            "wmd": np.random.normal(0, 1)   # weight of the distance between the current position of the drone and the M_OD magazine
        }

    def tournament_selection(self, population):
        # TODO make reproduction
        return population

    @staticmethod
    def evaluate(population):
        for simulation in population:
            # TODO: evaluation
            simulation.run()
        return population  # return grade of

    @staticmethod
    def mutation(population):
        # TODO: mutation
        return population

    @staticmethod
    def elite_succession(last_population, current_population):
        return last_population[:3] + current_population
