from objects import ItemList


class Order:
    def __init__(self, index, coordinates, amount, products):
        self.index = index
        self.coordinates = coordinates
        self.amount = amount
        self.score = 0
        self._items = ItemList(index_list=products)

    def get_load(self) -> int:
        return self._items.count()

    def has_all_items(self) -> bool:
        return self._items.has_all()

    def unload(self):
        return self._items.unload()

    def load(self, item_list, max_load) -> int:
        return self._items.load(item_list, max_load)

    def __repr__(self):
        return f"Order {self.index}: {self.coordinates}"
