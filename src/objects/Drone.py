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
        self.warehouse = None

    def update_time(self):
        if self.time_to_ready > 0:
            self.time_to_ready -= 1

    def is_ready(self):
        return self.time_to_ready == 0

    def has_all_items(self) -> bool:
        return self.order.has_all_items()

    def set_order(self, order: Order):
        self.order = order
        self.status = "NO_TARGET"
        logging.info(f"{self} will be delivering {order}")

    def fly_to_load(self):
        fly_time = self.fly_to(self.warehouse)
        loading_time = self.order.move_from_reserve()
        logging.info(f"{self} will be flying to {self.warehouse} and loading items, "
                     f"time: {fly_time}+{loading_time}={fly_time+loading_time}")

        self.time_to_ready = fly_time + loading_time
        self.warehouse = None
        self.status = "NO_TARGET"

    def fly_to_order(self):
        fly_time = self.fly_to(self.order)
        unloading = 1  # Unloading take 1 turn
        logging.info(f"{self} will be flying to {self.order} and unloading items, "
                     f"time: {fly_time}+{unloading}={fly_time+unloading}")

        self.time_to_ready += fly_time + unloading
        self.status = "READY_TO_SCORE"

    def fly_to(self, target) -> int:
        time_to_ready = math.ceil(Utilities.calc_distance(self.coordinates, target.coordinates))
        self.coordinates = target.coordinates
        return time_to_ready

    def reserve_goods(self, warehouse: Warehouse):
        self.warehouse = warehouse
        self.order.reserve_items(warehouse.items)

    def calc_score(self, max_turns, turn) -> int:
        score = math.ceil((max_turns - (turn + 1.0)) / max_turns * 100.0)
        logging.info(f"{self} finished {self.order}, score = {score}")
        self.status = "NO_ORDER"
        self.order = None
        return score

    def __repr__(self):
        return f"Drone {self.index}: {self.coordinates}"
