import numpy as np
from src.algorythm import GeneticAlgorythm
from random import seed
import logging
from subprocess import check_output


def get_project_root() -> str:
    return check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("log/info.log"),
            logging.StreamHandler()
        ]
    )
    seed(2137)
    np.random.seed(2137)
    algorythm = GeneticAlgorythm('resources/busy_day.in', population_size=20, max_generations=50)
    algorythm.start()
