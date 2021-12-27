from src import Simulation, SimulationParameters


class GeneticAlgorythm:
    def __init__(self, filename, population_size, max_generations):
        self.sim_consts = self.get_simulation_from_filename(filename)
        self.max_generations = max_generations
        self.population_size = population_size

        self.population = self.generate_population()
        for generation in range(0, self.max_generations):
            self.evaluate(self.population)
            mutated_population = self.mutate(self.population)
            self.population = self.join(self.population, mutated_population)

    def get_simulation_from_filename(self, filename):
        simulation_parameters = SimulationParameters()
        simulation_parameters.load_file(filename)
        return simulation_parameters

    def generate_population(self):
        population = []
        for i in range(self.population_size):
            population.append(Simulation(self.sim_consts))
        return population

    @staticmethod
    def evaluate(population):
        for simulation in population:
            simulation.run()

    @staticmethod
    def mutate(population):
        # TODO: mutation
        return population

    @staticmethod
    def join(last_population, current_population):
        return last_population[:3] + current_population
