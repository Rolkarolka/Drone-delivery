from random import random
from copy import deepcopy
from src.Drone import Drone
from src.Order import Order
import math


class SimulationParameters:
    def __init__(self, columns, rows, deadline, drones, types, warehouses, orders):
        self.columns = columns
        self.rows = rows
        self.deadline = deadline
        self.drones = drones
        self.types = types
        self.warehouses = warehouses
        self.orders = orders


class Simulation:
    def __init__(self, parameters: SimulationParameters):
        self.parameters = deepcopy(parameters)
        self.wzl = random()
        self.wzr = random()
        self.wzp = random()
        self.wzo = random()

        self.wmz = random()
        self.wmd = random()

        self.result = None

    def run(self, log=True):
        if log:
            self.draw_map()

        for turn in range(self.parameters.deadline):
            print(f"Turn {turn}")
            drone = self.parameters.drones[0]
            order = self.evaluate_orders()
            warehouse = self.evaluate_warehouses(drone, order)
        # warehouse = min(self.warehouses, key=lambda w: w.calc_heuristic(order))
        # drone = min(self.drones, key=lambda d: calc_distance(d.coords, warehouse.coords))
        # print( f"Order {order.index}: Drone {drone.index} {drone.coords}
        # will fly to Warehouse {warehouse.index} {warehouse.coords}")

    def evaluate_orders(self):
        for order in self.parameters.orders:
            order.score = self.wzl * order.amount + \
                          self.wzr * len(order.contents.keys())
            # TODO: Add more parameters
        self.parameters.orders.sort(reverse=True, key=lambda o: o.score)
        if self.parameters.orders:
            return self.parameters.orders.pop(0)
        else:
            return None

    def evaluate_warehouses(self, drone: Drone, order: Order):
        for warehouse in self.parameters.warehouses:
            warehouse.score = self.wmz * self.calc_distance(order.coords, warehouse.coords) + \
                              self.wmd * self.calc_distance(drone.coords, warehouse.coords)
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
                    if [row, column] == warehouse.coords:
                        print("W", end="")
                        no_object = False
                for order in self.parameters.orders:
                    if [row, column] == order.coords:
                        print("O", end="")
                        no_object = False
                if no_object:
                    print("-", end="")
            print()
        print()
