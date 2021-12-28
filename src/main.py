import numpy as np
from GeneticAlgorythm import GeneticAlgorythm
from random import seed

if __name__ == '__main__':
    seed(2137)
    np.random.seed(2137)
    algorythm = GeneticAlgorythm('../resources/busy_day.in', 1, 1)
    pass
