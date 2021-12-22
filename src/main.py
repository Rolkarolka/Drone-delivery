import math
from copy import deepcopy
from random import random, seed


def calc_distance(coordA, coordB):
    return math.sqrt((coordA[0] - coordB[0]) ** 2 + (coordA[1] - coordB[1]) ** 2)


class Drone:
    def __init__(self, index, coords, max_load):
        self.index = index
        self.coords = coords
        self.max_load = max_load
        self.ready = True

    def __repr__(self):
        return f"Drone {self.index}: {self.coords}"


class Warehouse:
    def __init__(self, index, coords, products):
        self.index = index
        self.coords = coords
        self.products = products
        self.score = 0

    def calc_heuristic(self, order: 'Order') -> float:
        total_amount = 0
        for product_type, amount in order.contents.items():
            total_amount += max(amount, self.products[product_type])
        heuristic_value = calc_distance(self.coords, order.coords) / total_amount
        return heuristic_value

    def __repr__(self):
        return f"Warehouse {self.index}: {self.coords} -> {self.score}"


class Order:
    def __init__(self, index, coords, amount, products):
        self.index = index
        self.coords = coords
        self.amount = amount
        self.score = 0
        self.contents = {}
        for product in products:
            self.contents[product] = self.contents.setdefault(product, 0) + 1

    def __repr__(self):
        return f"Order {self.index}: {self.coords} -> {self.score}"


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


class SimulationParameters:
    def __init__(self, columns, rows, deadline, drones, types, warehouses, orders):
        self.columns = columns
        self.rows = rows
        self.deadline = deadline
        self.drones = drones
        self.types = types
        self.warehouses = warehouses
        self.orders = orders


class Simulation:
    def __init__(self, parameters: SimulationParameters):
        self.parameters = deepcopy(parameters)
        self.wzl = random()
        self.wzr = random()
        self.wzp = random()
        self.wzo = random()

        self.wmz = random()
        self.wmd = random()

        self.result = None

    def run(self, log=True):
        if log:
            self.draw_map()

        for turn in range(self.parameters.deadline):
            print(f"Turn {turn}")
            drone = self.parameters.drones[0]
            order = self.evaluate_orders()
            warehouse = self.evaluate_warehouses(drone, order)
        # warehouse = min(self.warehouses, key=lambda w: w.calc_heuristic(order))
        # drone = min(self.drones, key=lambda d: calc_distance(d.coords, warehouse.coords))
        # print(
        #     f"Order {order.index}: Drone {drone.index} {drone.coords} will fly to Warehouse {warehouse.index} {warehouse.coords}")

    def evaluate_orders(self):
        for order in self.parameters.orders:
            order.score = self.wzl * order.amount +\
                          self.wzr * len(order.contents.keys())
            # TODO: Add more parameters
        self.parameters.orders.sort(reverse=True, key=lambda o: o.score)
        return self.parameters.orders.pop(0)

    def evaluate_warehouses(self, drone: Drone, order: Order):
        for warehouse in self.parameters.warehouses:
            warehouse.score = self.wmz * calc_distance(order.coords, warehouse.coords) +\
                              self.wmd * calc_distance(drone.coords, warehouse.coords)
            # TODO: Add more parameters
        self.parameters.warehouses.sort(reverse=True, key=lambda w: w.score)
        return self.parameters.warehouses.pop(0)

    def draw_map(self):
        for row in range(self.parameters.rows):
            for column in range(self.parameters.columns):
                no_object = True
                for warehouse in self.parameters.warehouses:
                    if [row, column] == warehouse.coords:
                        print("W", end="")
                        no_object = False
                for order in self.parameters.orders:
                    if [row, column] == order.coords:
                        print("O", end="")
                        no_object = False
                if no_object:
                    print("-", end="")
            print()
        print()


if __name__ == '__main__':
    seed(2137)
    algorythm = GeneticAlgorythm('resources/busy_day_mini.in', 1, 1)
    pass
