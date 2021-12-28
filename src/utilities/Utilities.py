import math


class Utilities:
    @staticmethod
    def calc_distance(coordA, coordB):
        return math.sqrt((coordA[0] - coordB[0]) ** 2 + (coordA[1] - coordB[1]) ** 2)
