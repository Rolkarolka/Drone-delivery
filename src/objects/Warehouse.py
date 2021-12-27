import math


class Warehouse:
    def __init__(self, index, coordinates, products):
        self.index = index
        self.coordinates = coordinates
        self.products = products
        self.score = 0

    def calc_heuristic(self, order: 'Order') -> float:
        total_amount = 0
        for product_type, amount in order.contents.items():
            total_amount += max(amount, self.products[product_type])
        heuristic_value = math.sqrt((self.coordinates[0] - order.coordinates[0]) ** 2 + (self.coordinates[1] - order.coordinates[1]) ** 2) / total_amount
        return heuristic_value

    def __repr__(self):
        return f"Warehouse {self.index}: {self.coordinates} -> {self.score}"
