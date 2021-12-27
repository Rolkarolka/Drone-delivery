import math

from src.objects import Order
from utils import calc_distance


class Drone:
    def __init__(self, index, coordinates, max_load):
        self.index = index
        self.coordinates = coordinates
        self.max_load = max_load
        self.time_to_ready = 0
        self.items = {}
        self.order = None
        self.target = None

    def update_time(self):
        self.time_to_ready -= 1

    def is_ready(self):
        return self.time_to_ready == 0

    def set_order(self, order: Order):
        self.order = order
        print(f"{self} will be delivering {order}")

    def has_all_items(self) -> bool:
        for item_types in self.order.contents.keys():
            if self.order.contents[item_types] > self.items.get(item_types, 0):
                return False
        return True

    def set_target(self, target):
        self.target = target

    def fly_to(self, coordinates):
        if self.coordinates != coordinates:
            self.time_to_ready = math.ceil(calc_distance(self.coordinates, coordinates))
            print(f"{self} will be flying to {coordinates}. ETA: {self.time_to_ready}")
            self.coordinates = coordinates

    def load(self):
        # TODO: Loading
        self.items = self.order.contents
        self.time_to_ready += 1
        print(f"{self} is loading items from {self.target}")

    def unload(self):
        # TODO: Unloading
        print(f"{self} is unloading items to {self.target}")

    def __repr__(self):
        return f"Drone {self.index}: {self.coordinates}"
