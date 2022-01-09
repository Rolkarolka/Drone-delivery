import numpy as np
from algorythm import Simulation, SimulationParameters, SimulationWeights
from random import seed
import logging


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )
    seed(2137)
    np.random.seed(2137)

    simulation_parameters = SimulationParameters().from_file("resources/busy_day.in")
    simulation = Simulation(simulation_parameters)
    simulation.run()
