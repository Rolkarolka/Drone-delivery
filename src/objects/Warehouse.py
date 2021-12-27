class Warehouse:
    def __init__(self, index, coordinates, products):
        self.index = index
        self.coordinates = coordinates
        self.products = products
        self.score = 0

    def __str__(self):
        return f"Warehouse {self.index}: {self.coordinates}"

    def __repr__(self):
        return f"{self.__str__()} -> {self.score}"
