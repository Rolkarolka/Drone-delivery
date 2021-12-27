from random import random
from copy import deepcopy
import math

from typing import Dict

from src.objects import Drone, Order
from src import SimulationParameters
from utils import calc_distance


class Simulation:
    def __init__(self, parameters: SimulationParameters, weights: Dict[str, int]):
        self.parameters = deepcopy(parameters)
        self.weights = weights

        self.score = 0

    def run(self, log=False):
        if log:
            self.draw_map()

        for turn in range(self.parameters.max_turns):
            print(f"Turn {turn}")
            for drone in self.parameters.drones:
                if drone.is_ready():
                    if not drone.order:
                        order = self.evaluate_orders()
                        drone.set_order(order)

                    if not drone.has_all_items():
                        if drone.target is None:
                            warehouse = self.evaluate_warehouses(drone, drone.order)
                            # warehouse.reserve_goods(drone.order)
                            drone.set_target(warehouse)
                            drone.fly_to(warehouse.coordinates)
                        else:
                            drone.load()
                            drone.set_target(None)
                    else:
                        if drone.target is None:
                            drone.set_target(drone.order)
                            drone.fly_to(drone.order.coordinates)
                        else:
                            drone.unload()

                drone.update_time()
            # drone.set_order(order)
        # warehouse = min(self.warehouses, key=lambda w: w.calc_heuristic(order))
        # drone = min(self.drones, key=lambda d: calc_distance(d.coordinates, warehouse.coordinates))
        # print( f"Order {order.index}: Drone {drone.index} {drone.coordinates}
        # will fly to Warehouse {warehouse.index} {warehouse.coordinates}")

    def evaluate_orders(self):
        for order in self.parameters.orders:
            order.score = self.weights["wzl"] * order.amount + \
                          self.weights["wzr"] * len(order.contents.keys())
            # TODO: Add more parameters
        self.parameters.orders.sort(reverse=True, key=lambda o: o.score)
        if self.parameters.orders:
            return self.parameters.orders.pop(0)
        else:
            return None

    def evaluate_warehouses(self, drone: Drone, order: Order):
        for warehouse in self.parameters.warehouses:
            warehouse.score = self.weights["wmz"] * calc_distance(order.coordinates, warehouse.coordinates) + \
                              self.weights["wmd"] * calc_distance(drone.coordinates, warehouse.coordinates)
            # TODO: Add more parameters
        self.parameters.warehouses.sort(reverse=True, key=lambda w: w.score)
        if self.parameters.warehouses:
            return self.parameters.warehouses[0]
        else:
            return None

    def draw_map(self):
        for row in range(self.parameters.rows):
            for column in range(self.parameters.columns):
                no_object = True
                for warehouse in self.parameters.warehouses:
                    if [row, column] == warehouse.coordinates:
                        print("W", end="")
                        no_object = False
                for order in self.parameters.orders:
                    if [row, column] == order.coordinates:
                        print("O", end="")
                        no_object = False
                if no_object:
                    print("-", end="")
            print()
        print()
