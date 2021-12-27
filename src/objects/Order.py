class Order:
    def __init__(self, index, coordinates, amount, products):
        self.index = index
        self.coordinates = coordinates
        self.amount = amount
        self.score = 0
        self.contents = {}
        for product in products:
            self.contents[product] = self.contents.setdefault(product, 0) + 1

    def __str__(self):
        return f"Order {self.index}: {self.coordinates}"

    def __repr__(self):
        return f"{self.__str__} -> {self.score}"
