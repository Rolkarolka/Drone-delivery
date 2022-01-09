import math

from objects import Order, Warehouse
from utilities import Utilities
import logging


class Drone:
    def __init__(self, index, coordinates, max_load):
        self.index = index
        self.coordinates = coordinates
        self.max_load = max_load
        self.time_to_ready = 0

        self.status = "NO_ORDER"
        self.order = None

    def update_time(self):
        if self.time_to_ready > 0:
            self.time_to_ready -= 1

    def is_ready(self):
        return self.time_to_ready == 0

    def get_remaining_load(self):
        return self.max_load - self.order.get_load()

    def has_all_items(self) -> bool:
        return self.order.has_all_items()

    def set_order(self, order: Order):
        self.order = order
        self.status = "NO_TARGET"
        logging.info(f"{self} will be delivering {order}")

    def fly_to_load(self, warehouse: Warehouse):
        logging.info(f"{self} will be flying to {warehouse} and loading items")
        fly_time = self.fly_to(warehouse)
        loading_time = self.order.load(warehouse.items, self.get_remaining_load())
        logging.info(f"It will take {fly_time}+{loading_time}={fly_time+loading_time} turns")

        self.time_to_ready = fly_time + loading_time
        self.status = "NO_TARGET"

    def fly_to_order(self):
        logging.info(f"{self} will be flying to {self.order} and unloading items")
        fly_time = self.fly_to(self.order)
        unloading = self.order.unload()
        logging.info(f"It will take {fly_time}+{unloading}={fly_time+unloading} turns")

        self.time_to_ready += fly_time + unloading
        if self.order.has_all_items():
            self.status = "READY_TO_SCORE"
        else:
            self.status = "NO_TARGET"

    def fly_to(self, target) -> int:
        time_to_ready = math.ceil(Utilities.calc_distance(self.coordinates, target.coordinates))
        self.coordinates = target.coordinates
        return time_to_ready

    def calc_score(self, max_turns, turn) -> int:
        score = math.ceil((max_turns - (turn + 1.0)) / max_turns * 100.0)
        logging.info(f"{self} finished {self.order}, score = {score}")
        self.status = "NO_ORDER"
        self.order = None
        return score

    def __repr__(self):
        return f"Drone {self.index}: {self.coordinates}"