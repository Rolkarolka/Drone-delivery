from random import seed
import numpy as np
import pytest
import sys

sys.path.append('.')
sys.path.append('./src')

from src.algorythm import CrossOver, CrossOverType, GeneticAlgorythm


def prepare_arguments_before_test(selection_type):
    seed(2137)
    np.random.seed(2137)
    algorythm = GeneticAlgorythm('resources/busy_day_mini.in', 4, 3, selection_type=selection_type)
    population = algorythm.initialize_population()

    for simulation in population:
        simulation.score = np.random.randint(0, 100)
    cross_over = CrossOver()
    return cross_over, population


@pytest.mark.parametrize("selection_type",
                         [CrossOverType.SINGLE_POINT_CROSSOVER,
                          CrossOverType.LINEAR_CROSSOVER,
                          CrossOverType.SINGLE_ARITHMETIC_CROSSOVER])
def test_cross_over(selection_type):
    # given:
    cross_over, population = prepare_arguments_before_test(selection_type)
    cross_over_func = cross_over.return_cross_over_type(selection_type)
    # when:
    co_population = cross_over_func([population[0]])
    # then:
    assert len(co_population) == 1
    assert co_population[0].weights == population[0].weights
    assert id(co_population[0]) != id(population[0])


def test_no_cross_over():
    # given:
    cross_over, population = prepare_arguments_before_test(CrossOverType.NONE)
    cross_over_func = cross_over.return_cross_over_type(CrossOverType.NONE)
    # when:
    co_population = cross_over_func(population)
    # then:
    assert len(co_population) == len(population)
    assert id(co_population[0]) != id(population[0])
    assert co_population[0].weights == {'wzl': 0.04629639546248449, 'wzr': -0.9226039536760489,
                                        'wzp': 0.46958468600224995, 'wzo': -1.5675182646238819,
                                        'wml': 0.5025648293370546, 'wmz': 1.0554395114897537, 'wmd': 1.2415631138712244}


@pytest.mark.parametrize("cross_over_type, func_name",
                         [(CrossOverType.SINGLE_POINT_CROSSOVER, "single_point_crossover"),
                          (CrossOverType.SINGLE_ARITHMETIC_CROSSOVER, "single_arithmetic_crossover"),
                          (CrossOverType.LINEAR_CROSSOVER, "linear_crossover")])
def test_return_cross_over_type(cross_over_type, func_name):
    cross_over = CrossOver()
    func = cross_over.return_cross_over_type(cross_over_type)
    assert func.__name__ == func_name
