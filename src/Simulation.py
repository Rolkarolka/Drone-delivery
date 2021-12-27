from random import random
from copy import deepcopy
import math

from typing import Dict

from src.objects import Drone, Order
from src import SimulationParameters


class Simulation:
    def __init__(self, parameters: SimulationParameters, weights: Dict[str, int]):
        self.parameters = deepcopy(parameters)
        self.weights = weights

        self.score = 0

    def run(self, log=True):
        if log:
            self.draw_map()

        for turn in range(self.parameters.max_payload):
            print(f"Turn {turn}")
            drone = self.parameters.drones[0]
            order = self.evaluate_orders()
            warehouse = self.evaluate_warehouses(drone, order)
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
            warehouse.score = self.weights["wmz"] * self.calc_distance(order.coordinates, warehouse.coordinates) + \
                              self.weights["wmd"] * self.calc_distance(drone.coordinates, warehouse.coordinates)
            # TODO: Add more parameters
        self.parameters.warehouses.sort(reverse=True, key=lambda w: w.score)
        if self.parameters.warehouses:
            return self.parameters.warehouses.pop(0)
        else:
            return None

    @staticmethod
    def calc_distance(coordA, coordB):
        return math.sqrt((coordA[0] - coordB[0]) ** 2 + (coordA[1] - coordB[1]) ** 2)

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
