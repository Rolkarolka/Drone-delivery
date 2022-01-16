from objects import ItemList


class Warehouse:
    def __init__(self, index: int, coordinates, products: list):
        self.index = index
        self.coordinates = coordinates
        self.score = 0
        self.items = ItemList(item_list=products)

    def __str__(self):
        return f"Warehouse {self.index}: {self.coordinates}"

    def __repr__(self):
        return f"{self.__str__()} -> {self.score}"
