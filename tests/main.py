import logging

from tests.main_test import TestSimulation

if __name__ == '__main__':
    sim = TestSimulation()
    sim.test_main_simulation(logging_level=logging.INFO)
