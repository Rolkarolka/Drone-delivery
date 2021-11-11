class Simulation:
    def __init__(self, namefile):
        with open(namefile) as file:
            lines = file.readlines()
            params = lines[0].strip().split(" ")
            self.rows = int(params[0])
            self.columns = int(params[1])
            self.no_drones = int(params[2])
            self.deadline = int(params[3])
            self.max_load = int(params[4])

            self.no_types = int(lines[1].strip())

            self.types = [int(product_type) for product_type in lines[2].strip().split(" ")]

            self.no_warehouses = int(lines[3].strip())
            self.warehouses = []
            for i in range(4, 4 + self.no_warehouses * 2, 2):
                warehouse = []
                coords = [int(coord) for coord in lines[i].strip().split(" ")]
                warehouse.append(coords)
                products = [int(product_type) for product_type in lines[i + 1].strip().split(" ")]
                warehouse.append(products)
                self.warehouses.append(warehouse)
            i += 2

            self.no_orders = int(lines[i].strip())
            self.orders = []
            for i in range(i + 1, i + 1 + self.no_warehouses * 3, 3):
                order = []
                coords = [int(coord) for coord in lines[i].strip().split(" ")]
                order.append(coords)
                amount = int(lines[i + 1].strip())
                order.append(amount)
                products = [int(product_type) for product_type in lines[i + 2].strip().split(" ")]
                order.append(products)
                self.orders.append(order)
            pass


if __name__ == '__main__':
    sim = Simulation('busy_day.in')
