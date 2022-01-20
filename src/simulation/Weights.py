import numpy as np


class SimulationWeights:
    @staticmethod
    def initialize_weights():
        """
        "wzl": weight of the number of products in the order Z_L
        "wzr": weight of order variety Z_R - quantity of product types in the order under consideration
        "wzp": weight of the popularity of Z_P products - availability in warehouses included in the order under consideration
        "wzo": weight of the distance between the current position of the aircraft and the target Z_O
        "wml": weight of the quantity of the product available in the warehouse M_L
        "wmz": weight of the distance between the warehouse location and the M_OZ destination point
        "wmd": weight of the distance between the current position of the drone and the M_OD magazine
        """
        return {
            "wzl": np.random.normal(0, 1),
            "wzr": np.random.normal(0, 1),
            "wzp": np.random.normal(0, 1),
            "wzo": np.random.normal(0, 1),
            "wml": np.random.normal(0, 1),
            "wmz": np.random.normal(0, 1),
            "wmd": np.random.normal(0, 1)
        }
