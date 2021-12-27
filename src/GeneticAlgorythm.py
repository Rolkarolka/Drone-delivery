from src.Drone import Drone
from src.Order import Order
from src.Warehouse import Warehouse
from src.Simulation import SimulationParameters, Simulation


class GeneticAlgorythm:
    def __init__(self, filename, population_size, max_generations):
        self.sim_consts = self.load_file(filename)
        self.max_generations = max_generations
        self.population_size = population_size

        self.population = self.generate_population()
        for generation in range(0, self.max_generations):
            self.evaluate(self.population)
            mutated_population = self.mutate(self.population)
            self.population = self.join(self.population, mutated_population)

    @staticmethod
    def load_file(filename):
        with open(filename) as file:
            lines = file.readlines()
        params = lines[0].strip().split(" ")
        rows = int(params[0])
        columns = int(params[1])

        no_drones = int(params[2])
        deadline = int(params[3])
        max_load = int(params[4])

        no_types = int(lines[1].strip())
        types = [int(product_type) for product_type in lines[2].strip().split(" ")]
        assert len(types) == no_types

        no_warehouses = int(lines[3].strip())
        warehouses = []
        line_idx = 4
        for index in range(no_warehouses):
            coords = [int(coord) for coord in lines[line_idx].strip().split(" ")]
            products = [int(product_type) for product_type in lines[line_idx + 1].strip().split(" ")]
            warehouses.append(Warehouse(index, coords, products))
            line_idx += 2
        assert len(warehouses) == no_warehouses

        drones = []
        for i in range(0, no_drones):
            drones.append(Drone(i, warehouses[0].coords, max_load))
        assert len(drones) == no_drones

        no_orders = int(lines[line_idx].strip())
        orders = []
        line_idx += 1
        for index in range(no_orders):
            coords = [int(coord) for coord in lines[line_idx].strip().split(" ")]
            amount = int(lines[line_idx + 1].strip())
            products = [int(product_type) for product_type in lines[line_idx + 2].strip().split(" ")]
            orders.append(Order(index, coords, amount, products))
            line_idx += 3
        assert len(orders) == no_orders

        return SimulationParameters(columns, rows, deadline, drones, types, warehouses, orders)

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
