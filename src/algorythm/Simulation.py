import math
from copy import deepcopy
from typing import Dict

from algorythm.SimulationWeights import SimulationWeights
from objects import Drone, Order, DroneStatus
from algorythm import SimulationParameters
from utilities import Utilities
import logging


class Simulation:
    def __init__(self,
                 parameters: SimulationParameters,
                 weights: Dict[str, int] = None):
        self.parameters = deepcopy(parameters)
        if weights is not None:
            self.weights = weights
        else:
            self.weights = SimulationWeights.initialize_weights()
        self.score = 0

    def are_drones_working(self) -> bool:
        status = False
        for drone in self.parameters.drones:
            if drone.status != DroneStatus.NO_ORDER:
                status = True
        return status

    def run(self):
        for turn in range(self.parameters.max_turns):
            for drone in self.parameters.drones:
                if drone.is_ready():
                    if drone.status == DroneStatus.NO_ORDER and len(self.parameters.orders) > 0:
                        self.evaluate_orders(drone)
                        drone.set_order(self.parameters.orders.pop(0))

                    if drone.status == DroneStatus.NO_TARGET:
                        if not drone.has_all_items():
                            if drone.get_remaining_load() > 0:
                                self.evaluate_warehouses(drone, drone.order)
                                drone.fly_to_load(self.parameters.warehouses[0])
                            else:
                                drone.fly_to_order()
                        else:
                            drone.fly_to_order()
                if drone.is_ready() and drone.status == DroneStatus.READY_TO_SCORE:
                    self.score += drone.calc_score(self.parameters.max_turns, turn)
                drone.update_time()
            if len(self.parameters.orders) == 0 and not self.are_drones_working():
                break
        logging.info(f"Total simulation score = {self.score}")

    def evaluate_orders(self, drone: Drone):
        for order in self.parameters.orders:
            order.score = self.weights["wzl"] * order.amount + \
                          self.weights["wzr"] * len(order._items.keys()) + \
                          self.weights["wzo"] * Utilities.calc_distance(drone.coordinates, order.coordinates)
            # TODO: Add more parameters
        self.parameters.orders.sort(reverse=True, key=lambda o: o.score)

    def evaluate_warehouses(self, drone: Drone, order: Order):
        for warehouse in self.parameters.warehouses:
            items_to_pick = 0
            for item_type in order._items.keys():
                if item_type in warehouse.items.keys():
                    items_to_pick += min(order._items[item_type].get_remains(), warehouse.items[item_type].current)

            if items_to_pick != 0:
                warehouse.score = self.weights["wmz"] * Utilities.calc_distance(order.coordinates, warehouse.coordinates) + \
                                  self.weights["wmd"] * Utilities.calc_distance(drone.coordinates, warehouse.coordinates) + \
                                  self.weights["wml"] * items_to_pick
            else:
                # There is nothing important in it
                warehouse.score = -math.inf

        self.parameters.warehouses.sort(reverse=True, key=lambda w: w.score)
