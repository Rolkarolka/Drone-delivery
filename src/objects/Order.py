from objects import ItemList


class Order:
    def __init__(self, index, coordinates, amount, products):
        self.index = index
        self.coordinates = coordinates
        self.amount = amount
        self.score = 0
        self._items = ItemList(index_list=products)

    def has_all_items(self) -> bool:
        return self._items.has_all()

    def reserve_items(self, item_list):
        return self._items.reserve(item_list)

    def move_from_reserve(self) -> int:
        return self._items.move_from_reserve()

    def __repr__(self):
        return f"Order {self.index}: {self.coordinates}"
