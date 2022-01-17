from objects import *


class SimulationParameters:
    def __init__(self,
                 columns=None,
                 rows=None,
                 max_turns=None,
                 max_payload=None,
                 drones=None,
                 types=None,
                 warehouses=None,
                 orders=None):
        self.columns = columns
        self.rows = rows
        self.max_turns = max_turns
        self.max_payload = max_payload
        self.drones = drones
        self.types = types
        self.warehouses = warehouses
        self.orders = orders
        self.all_items = ItemList()

    @staticmethod
    def from_file(filename: str):
        simulation_parameters = SimulationParameters()
        simulation_parameters._load_file(filename)
        return simulation_parameters

    def _load_file(self, filename: str):
        with open(filename) as file:
            lines = file.readlines()
        basic_info_lines_amount = 3
        self.rows, self.columns, no_drones, self.max_turns, self.max_payload = map(int, lines[0].strip().split(" "))
        no_product_type = int(lines[1].strip())
        self.types = [int(product_type) for product_type in lines[2].strip().split(" ")]
        assert len(self.types) == no_product_type

        self.warehouses = self._create_warehouse_list(lines[basic_info_lines_amount:])
        self.drones = self._create_drone_list(no_drones, self.warehouses[0], self.max_payload)
        self.orders = self._create_order_list(lines[basic_info_lines_amount + 2 * len(self.warehouses) + 1:])

    def _create_warehouse_list(self, lines: [str]) -> [Warehouse]:
        no_warehouses = int(lines[0].strip())
        warehouses = []
        for index, line_idx in zip(range(no_warehouses), range(1, 1 + no_warehouses * 2, 2)):
            warehouse_coordinates = list(map(int, lines[line_idx].strip().split(" ")))
            item_list = ItemList(item_list=[int(product_type) for product_type in lines[line_idx + 1].strip().split(" ")])
            warehouses.append(Warehouse(index, warehouse_coordinates, item_list))
            self.all_items.update(item_list)
        assert len(warehouses) == no_warehouses
        return warehouses

    @staticmethod
    def _create_drone_list(no_drones: int, home_warehouse: Warehouse, max_payload: int) -> [Drone]:
        drones = []
        for i in range(0, no_drones):
            drones.append(Drone(i, home_warehouse.coordinates, max_payload))
        assert len(drones) == no_drones
        return drones

    @staticmethod
    def _create_order_list(lines) -> [Order]:
        no_orders = int(lines[0].strip())
        orders = []
        for index, line_idx in zip(range(no_orders), range(1, 1 + no_orders * 3, 3)):
            order_coordinates = [int(coord) for coord in lines[line_idx].strip().split(" ")]
            amount = int(lines[line_idx + 1].strip())
            stock_level = [int(product_type) for product_type in lines[line_idx + 2].strip().split(" ")]
            order = Order(index, order_coordinates, amount, stock_level)
            orders.append(order)
        assert len(orders) == no_orders
        return orders
