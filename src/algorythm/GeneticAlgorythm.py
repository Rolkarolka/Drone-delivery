from simulation import SimulationParameters, Simulation, SimulationWeights
from algorythm import Selection, SelectionType, MutationType, Mutation
from utilities import Utilities
import threading
import numpy as np
from copy import deepcopy
import logging


class GeneticAlgorythm:
    def __init__(self, filename, population_size, max_generations, elite_size=5,
                 selection_type=SelectionType.TOURNAMENT_SELECTION,
                 mutation_type=MutationType.GAUSSIAN_MUTATION):
        self.sim_consts = SimulationParameters.from_file(filename)
        self.max_generations = max_generations
        self.population_size = population_size
        self.selection_type = selection_type
        self.mutation_type = mutation_type
        self.succession_type = succession_type
        self.mutation = Mutation().return_mutation_type(mutation_type)
        self.selection = Selection().return_selection_type(selection_type)
        self.algorithm()

    def algorithm(self):
        t = 0
        population = self.initialize_population()
        rating = self.evaluation(population)
        score_history = []
        while t < self.max_generations:
            aggregated_results = self.aggregate_results(population)
            logging.info(f"Generation {t} [min/avr/max]: {aggregated_results}")
            score_history.append(aggregated_results)

            t_population = self.selection(population)
            m_population = self.mutation(t_population)
            population = self.elite_succession(rating, m_population)
            population = self.reset_simulations(population)
            rating = self.evaluation(population)
            t += 1
        aggregated_results = self.aggregate_results(population)
        best_simulation = max(population, key=lambda simulation: simulation.score)
        logging.info(f"Generation {t} [min/avr/max]: {aggregated_results}\n"
                     f"Weights:\n"
                     f"{best_simulation.weights}")
        Utilities.draw_plot(score_history, filename="algorithm.jpg", title=f"Generic algorythm "
                                                                           f"(pop={self.population_size}/"
                                                                           f"mutation={self.mutation_type}/"
                                                                           f"selection={self.selection_type})", )

    @staticmethod
    def aggregate_results(population):
        simulation_results = [simulation.score for simulation in population]
        aggregated_results = (
            min(simulation_results),
            int(np.mean(simulation_results).round()),
            max(simulation_results)
        )
        return aggregated_results

    def initialize_population(self):
        population = []
        for i in range(self.population_size):
            population.append(Simulation(self.sim_consts, SimulationWeights.initialize_weights()))
        return population

    def reset_simulations(self, population):
        return [Simulation(self.sim_consts, simulation.weights) for simulation in population]

    @staticmethod
    def evaluation(population):
        threads = []
        for simulation in population:
            thread = threading.Thread(target=simulation.run())
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        rated = sorted(population, key=lambda single_simulation: single_simulation.score)
        rated.reverse()
        return rated
