import numpy as np
from algorythm import Simulation, SimulationParameters, SimulationWeights
from random import seed
import logging


class TestSimulation:
    @staticmethod
    def prepare():
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO
        )
        seed(2137)
        np.random.seed(2137)

    def test_main_simulation(self):
        self.prepare()

        simulation_parameters = SimulationParameters().from_file("resources/busy_day.in")
        simulation = Simulation(simulation_parameters)
        simulation.run()
        assert simulation.score == 90203

    def test_mini_simulation(self):
        self.prepare()

        simulation_parameters = SimulationParameters().from_file("resources/busy_day_mini.in")
        simulation = Simulation(simulation_parameters)
        simulation.run()
        assert simulation.score == 217
