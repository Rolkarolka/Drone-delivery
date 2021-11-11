import math


def calc_distance(coordA, coordB):
    return math.sqrt((coordA[0] - coordB[0]) ** 2 + (coordA[1] - coordB[1]) ** 2)


class Drone:
    def __init__(self, index, coords):
        self.index = index
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
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


class Simulation:
    def __init__(self, filename, draws_map=False):
        self.load_file(filename)
        if draws_map:
            self.draw_map()
        self.turn = 0

        first_warehouse = self.warehouses[0]
        for i in range(self.no_drones):
            self.drones.append(Drone(i, first_warehouse.coords))

        self.make_turn()

    def make_turn(self):
        print(f"Turn {self.turn}")
        order = self.orders.pop(0)
        warehouse = min(self.warehouses, key=lambda w: w.calc_heuristic(order))
        drone = min(self.drones, key=lambda d: calc_distance(d.coords, warehouse.coords))
        print(
            f"Order {order.index}: Drone {drone.index} {drone.coords} will fly to Warehouse {warehouse.index} {warehouse.coords}")

    def load_file(self, filename):
        with open(filename) as file:
            lines = file.readlines()
            params = lines[0].strip().split(" ")
            self.rows = int(params[0])
            self.columns = int(params[1])
            self.drones = []
            self.no_drones = int(params[2])
            self.deadline = int(params[3])
            self.max_load = int(params[4])

            self.no_types = int(lines[1].strip())

            self.types = [int(product_type) for product_type in lines[2].strip().split(" ")]

            self.no_warehouses = int(lines[3].strip())
            self.warehouses = []
            index = 0
            for i in range(4, 4 + self.no_warehouses * 2, 2):
                coords = [int(coord) for coord in lines[i].strip().split(" ")]
                products = [int(product_type) for product_type in lines[i + 1].strip().split(" ")]
                self.warehouses.append(Warehouse(index, coords, products))
                index += 1
            i += 2

            self.no_orders = int(lines[i].strip())
            self.orders = []
            index = 0
            for i in range(i + 1, i + 2 + self.no_warehouses * 3, 3):
                coords = [int(coord) for coord in lines[i].strip().split(" ")]
                amount = int(lines[i + 1].strip())
                products = [int(product_type) for product_type in lines[i + 2].strip().split(" ")]
                self.orders.append(Order(index, coords, amount, products))
                index += 1

    def draw_map(self):
        for row in range(self.rows):
            for column in range(self.columns):
                no_object = True
                for coords, products in self.warehouses:
                    if [row, column] == coords:
                        print("W", end="")
                        no_object = False
                for coords, amount, types in self.orders:
                    if [row, column] == coords:
                        print("O", end="")
                        no_object = False
                if no_object:
                    print("-", end="")
            print()
        print()

    def find_best_warehouse(self, coords, product_type):
        pass


if __name__ == '__main__':
    sim = Simulation('busy_day_mini.in', False)
