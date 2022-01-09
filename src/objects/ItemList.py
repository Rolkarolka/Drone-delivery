class ItemList:
    def __init__(self, item_list: list = None, index_list: list = None):
        self.items = {}
        if item_list is not None:
            self.from_list(item_list)
        if index_list is not None:
            self.from_index_list(index_list)

    def count(self) -> int:
        num = 0
        for item_type in self.items.keys():
            num += self.items[item_type].current
        return num

    def from_list(self, item_list):
        for i in range(len(item_list)):
            self.items[i] = Item(item_list[i], 0)

    def from_index_list(self, item_list):
        for index in item_list:
            if index in self.items.keys():
                self.items[index].total += 1
            else:
                self.items[index] = Item(1, 0)

    def has_all(self) -> bool:
        for item_type in self.items.keys():
            if not self.items[item_type].has_all():
                return False
        return True

    def load(self, item_list, max_load) -> int:
        types = 0
        for item_type in self.items.keys():
            amount = self.items[item_type].get_remains()
            if item_type in item_list.keys():
                amount = min(item_list[item_type].current, amount, max_load)
                max_load -= amount
                if amount != 0:
                    types += 1
                    item_list[item_type].current -= amount
                    self.items[item_type].current += amount
        return types

    def unload(self):
        for item_type in self.items.keys():
            self.items[item_type].unload()
        return 1

    def fill(self):
        for item_type in self.items.keys():
            self.items[item_type].fill()

    def keys(self):
        return self.items.keys()

    def __getitem__(self, key):
        return self.items[key]

    def __str__(self):
        return str(self.items)


class Item:
    def __init__(self, total, current):
        self.total = total
        self.current = current

    def has_all(self) -> bool:
        return self.current >= self.total

    def get_remains(self):
        return self.total - self.current

    def unload(self):
        if self.current > 0:
            self.total -= self.current
            self.current -= self.current
            return True
        else:
            return False

    def fill(self):
        self.current = self.total

    def __repr__(self):
        return f"{self.total}/{self.current}"
