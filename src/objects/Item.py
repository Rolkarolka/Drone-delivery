class Item:
    def __init__(self, item_type, quantity):
        self.type = item_type
        self.quantity = quantity

    def is_empty(self):
        return self.quantity == 0

    def __repr__(self):
        return f"Item {self.type} [{self.quantity}]"
