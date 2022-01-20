from algorythm import Selection, SelectionType, SimulationParameters, Simulation, SimulationWeights
import threading
import numpy as np
import random
import logging
from utilities import Utilities


class GeneticAlgorythm:
    def __init__(self, filename, population_size, max_generations, elite_size=5, selection_type=SelectionType.TOURNAMENT_SELECTION):
        self.sim_consts = SimulationParameters.from_file(filename)
        self.max_generations = max_generations
        self.population_size = population_size
        self.selection_type = selection_type
        self.selection = Selection().return_selection_type(selection_type)
        self.elite_size = elite_size
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
                                                                           f"elite={self.elite_size}/"
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

    @staticmethod
    def mutation(population):
        for simulation in population:
            # choose which and how many of weights will be muted
            weights_to_be_muted = random.sample(list(simulation.weights),
                                                random.randint(0, len(simulation.weights.keys())))
            # mute chosen
            for weight in weights_to_be_muted:
                simulation.weights[weight] = np.random.normal(0, 1)
        return population

    def elite_succession(self, last_population, current_population):
        return last_population[0:self.elite_size] + current_population[0:-self.elite_size]

    def reset_simulations(self, population):
        return [Simulation(self.sim_consts, simulation.weights) for simulation in population]
