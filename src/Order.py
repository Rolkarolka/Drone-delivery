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
