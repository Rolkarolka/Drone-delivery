from objects import ItemList


class Order:
    def __init__(self, index, coordinates, amount, products):
        self.index = index
        self.coordinates = coordinates
        self.amount = amount
        self.score = 0
        self.items = ItemList(index_list=products)

    def __repr__(self):
        return f"Order {self.index}: {self.coordinates}"
