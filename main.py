import math


def calc_distance(coordA, coordB):
    return math.sqrt((coordA[0] - coordB[0]) ** 2 + (coordA[1] - coordB[1]) ** 2)


class Drone:
    def __init__(self, index, max_load):
        self.index = index
        self.coords = [0, 0]
        self.max_load = max_load
        self.ready = True

    def __repr__(self):
        return f"Drone {self.index} {self.coords}"


class Warehouse:
    def __init__(self, index, coords, products):
        self.index = index
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        self.products = products

    def calc_heuristic(self, order: 'Order') -> float:
        total_amount = 0
        for product_type, amount in order.contents.items():
            total_amount += max(amount, self.products[product_type])
        heuristic_value = calc_distance(self.coords, order.coords) / total_amount
        return heuristic_value

    def __repr__(self):
        return f"Warehouse {self.index} {self.coords}"


class Order:
    def __init__(self, index, coords, amount, products):
        self.index = index
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        self.amount = amount
        self.contents = {}
        for product in products:
            self.contents[product] = self.contents.setdefault(product, 0) + 1

    def __repr__(self):
        return f"Order {self.index} {self.coords}"


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

        drones = []
        for i in range(0, no_drones):
            drones.append(Drone(i, max_load))
        assert len(drones) == no_drones

        no_types = int(lines[1].strip())
        types = [int(product_type) for product_type in lines[2].strip().split(" ")]
        assert len(types) == no_types

        no_warehouses = int(lines[3].strip())
        warehouses = []
        index = 0
        for line_idx in range(4, 4 + no_warehouses * 2, 2):
            coords = [int(coord) for coord in lines[line_idx].strip().split(" ")]
            products = [int(product_type) for product_type in lines[line_idx + 1].strip().split(" ")]
            warehouses.append(Warehouse(index, coords, products))
            index += 1
        assert len(warehouses) == no_warehouses
        line_idx += 2

        no_orders = int(lines[line_idx].strip())
        orders = []
        index = 0
        for line_idx in range(line_idx + 1, line_idx + 1 + no_orders * 3, 3):
            coords = [int(coord) for coord in lines[line_idx].strip().split(" ")]
            amount = int(lines[line_idx + 1].strip())
            products = [int(product_type) for product_type in lines[line_idx + 2].strip().split(" ")]
            orders.append(Order(index, coords, amount, products))
            index += 1
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
        return population.copy()

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
        self.parameters = parameters
        self.turn = 0

        self.result = None

        first_warehouse = self.parameters.warehouses[0]
        for i in range(len(self.parameters.drones)):
            self.parameters.drones.append(Drone(i, first_warehouse.coords))

        # self.make_turn()

    def make_turn(self):
        pass
        # print(f"Turn {self.turn}")
        # order = self.orders.pop(0)
        # warehouse = min(self.warehouses, key=lambda w: w.calc_heuristic(order))
        # drone = min(self.drones, key=lambda d: calc_distance(d.coords, warehouse.coords))
        # print(
        #     f"Order {order.index}: Drone {drone.index} {drone.coords} will fly to Warehouse {warehouse.index} {warehouse.coords}")

    def draw_map(self):
        pass
        # for row in range(self.rows):
        #     for column in range(self.columns):
        #         no_object = True
        #         for coords, products in self.warehouses:
        #             if [row, column] == coords:
        #                 print("W", end="")
        #                 no_object = False
        #         for coords, amount, types in self.orders:
        #             if [row, column] == coords:
        #                 print("O", end="")
        #                 no_object = False
        #         if no_object:
        #             print("-", end="")
        #     print()
        # print()

    def find_best_warehouse(self, coords, product_type):
        pass


if __name__ == '__main__':
    algorythm = GeneticAlgorythm('busy_day.in', 1, 10)
