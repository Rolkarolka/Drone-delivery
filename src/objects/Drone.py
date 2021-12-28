import math

from objects import Order, Warehouse
from utilities import Utilities


class Drone:
    def __init__(self, index, coordinates, max_load):
        self.index = index
        self.coordinates = coordinates
        self.max_load = max_load
        self.time_to_ready = 0

        self.status = "NO_ORDER"
        self.order = None
        self.warehouse = None

    def update_time(self):
        if self.time_to_ready > 0:
            self.time_to_ready -= 1
        else:
            if self.status == "FLYING_TO_LOAD":
                self.status = "READY_TO_LOAD"
            if self.status == "FLYING_TO_DELIVER":
                self.status = "READY_TO_DELIVER"
            if self.status == "LOADING":
                self.status = "NO_TARGET"
            if self.status == "DELIVERING":
                self.status = "READY_TO_SCORE"

    def is_ready(self):
        return self.time_to_ready == 0

    def has_all_items(self) -> bool:
        return self.order.items.has_all()

    def set_order(self, order: Order):
        self.order = order
        self.status = "NO_TARGET"
        print(f"{self} will be delivering {order}")

    def fly_to_warehouse(self):
        if self.coordinates != self.warehouse.coordinates:
            self.fly_to(self.warehouse)
            self.status = "FLYING_TO_LOAD"
        else:
            self.status = "READY_TO_LOAD"

    def fly_to_order(self):
        if self.coordinates != self.order.coordinates:
            self.fly_to(self.order)
            self.status = "FLYING_TO_DELIVER"
        else:
            self.status = "READY_TO_DELIVER"

    def fly_to(self, target):
        self.time_to_ready += math.ceil(Utilities.calc_distance(self.coordinates, target.coordinates))
        print(f"{self} will be flying to {target}, time: {self.time_to_ready}")
        self.coordinates = target.coordinates

    def reserve_goods(self, warehouse: Warehouse):
        self.warehouse = warehouse
        self.order.items.reserve(warehouse.items)

    def load(self):
        print(f"{self} is loading items from {self.warehouse}")
        self.time_to_ready += self.order.items.move_from_reserve()
        self.warehouse = None
        self.status = "LOADING"

    def deliver(self):
        self.time_to_ready += 1
        print(f"{self} is delivering items to {self.order}")
        self.status = "DELIVERING"

    def calc_score(self, max_turns, turn) -> int:
        score = math.ceil((max_turns - (turn + 1.0)) / max_turns * 100.0)
        print(f"{self} finished {self.order}, score = {score}")
        self.status = "NO_ORDER"
        self.order = None
        return score

    def __repr__(self):
        return f"Drone {self.index}: {self.coordinates}"
