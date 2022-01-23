from simulation import SimulationParameters, Simulation, SimulationWeights
from algorythm import Selection, Mutation, Succession, CrossOver
from utilities import Utilities
import threading
import numpy as np
import logging


class GeneticAlgorythm:
    def __init__(self, filename, population_size, max_generations, selection_type,
                 mutation_type, succession_type, crossover_type):
        self.sim_consts = SimulationParameters.from_file(filename)
        self.max_generations = max_generations
        self.population_size = population_size
        self.selection_type = selection_type
        self.mutation_type = mutation_type
        self.succession_type = succession_type
        self.cross_over_type = crossover_type
        self.mutation = Mutation().return_mutation_type(mutation_type)
        self.selection = Selection().return_selection_type(selection_type)
        self.succession = Succession().return_succession_type(succession_type)
        self.cross_over = CrossOver().return_cross_over_type(crossover_type)
        self.score_history = []
        self.algorithm_name = f"alg_" \
                              f"{self.population_size}_" \
                              f"{self.succession_type.value}_" \
                              f"{self.mutation_type.value}_" \
                              f"{self.cross_over_type.value}_" \
                              f"{self.selection_type.value}_"

    def start(self):
        t = 0
        population = self.initialize_population()
        rating = self.evaluation(population)
        while t < self.max_generations:
            self.aggregate_results(population, t)
            t_population = self.selection(population)
            m_population = self.mutation(t_population)
            c_population = self.cross_over(m_population)
            population = self.succession(rating, c_population)
            population = self.reset_simulations(population)
            rating = self.evaluation(population)
            t += 1
        self.aggregate_results(population, t)
        best_simulation = max(population, key=lambda simulation: simulation.score)
        self.present_algorithm_results(best_simulation)

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
        return sorted(population, key=lambda single_simulation: single_simulation.score, reverse=True)

    def aggregate_results(self, population, t):
        simulation_results = [simulation.score for simulation in population]
        aggregated_results = (
            min(simulation_results),
            int(np.mean(simulation_results).round()),
            max(simulation_results)
        )
        logging.info(f"Generation {t} [min/avr/max]: {aggregated_results}")
        self.save_raw_data(aggregated_results)
        self.score_history.append(aggregated_results)
        return aggregated_results

    def present_algorithm_results(self, best_simulation):
        logging.info(f"Weights:\n"
                     f"{best_simulation.weights}")
        Utilities.draw_plot(self.score_history,
                            filename=f"log/plots/{self.algorithm_name}.jpg",
                            title=f"Generic algorythm "
                                  f"(pop={self.population_size}/"
                                  f"suc={self.succession_type.value}/"
                                  f"mut={self.mutation_type.value}/"
                                  f"cro={self.cross_over_type.value}/"
                                  f"sel={self.selection_type.value})")

    def save_raw_data(self, aggregated_results):
        with open(f"log/raw_data/{self.algorithm_name}.txt", "a+") as file:
            file.write(f"{aggregated_results[0]};{aggregated_results[1]};{aggregated_results[2]}\n")