import numpy as np
from algorythm import *
from random import seed
import logging
import sys
from argparse import ArgumentParser


def parse_args(argv):
    parser = ArgumentParser(description=f'Genetic algorithm for POP course')
    parser.add_argument('-m', '--mutation', type=int,
                        help='[number] type of mutation, where: 1 -> uniform; 2 -> gaussian; 3 -> cauchy. '
                             '[Default value]: 3')
    parser.add_argument('-sl', '--selection', type=int,
                        help='[number] type of selection, where: 1-> tournament; 2 -> roulette wheel, 3 -> rank. '
                             '[Default value]: 1')
    parser.add_argument('-sc', '--succession', type=int,
                        help='[number] type of succession, where: 1 -> elite; 2 -> generational; 3 -> steady-state.'
                             '[Default value]: 1')
    parser.add_argument('-co', '--crossover', type=int,
                        help='[number], type of cross-over, where: 1 -> single point; 2 -> linear; 3 -> single '
                             'arithmetic; 4 -> None. [Default value]: 2')
    parser.add_argument('-p', '--population', type=int, help='[number] amount of population. [Default value]: 10')
    parser.add_argument('-g', '--generation', type=int, help='[number] max amount of generation [Default value]: 50')
    parser.add_argument('-f', '--input_filename', type=str, help='[string] file to path with input data for simulations'
                                                                 '[Default value]: \'resources/busy_day.in\'')
    args = parser.parse_args(argv[1:])
    return args.mutation, args.selection, args.succession, args.crossover, args.population, args.generation, args.input_filename


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
    mutation, selection, succession, crossover, population, generation, filename = parse_args(sys.argv)

    mutation_type = MutationType(int(mutation)) if mutation is not None else MutationType.CAUCHY_MUTATION
    selection_type = SelectionType(int(selection)) if selection is not None else SelectionType.TOURNAMENT_SELECTION
    succession_type = SuccessionType(int(succession)) if succession is not None else SuccessionType.ELITE_SUCCESSION
    crossover_type = CrossOverType(int(crossover)) if crossover is not None else CrossOverType.LINEAR_CROSSOVER
    population_size = int(population) if population is not None else 10
    generation_size = int(generation) if generation is not None else 50
    input_filename = filename if filename is not None else 'resources/busy_day.in'

    algorythm = GeneticAlgorythm(filename=input_filename,
                                 population_size=population_size,
                                 max_generations=generation_size,
                                 mutation_type=mutation_type,
                                 selection_type=selection_type,
                                 succession_type=succession_type,
                                 crossover_type=crossover_type)
    algorythm.start()
