import math


class Utilities:
    @staticmethod
    def calc_distance(coord_a, coord_b):
        return math.sqrt((coord_a[0] - coord_b[0]) ** 2 + (coord_a[1] - coord_b[1]) ** 2)
