from random import seed
import numpy as np
import pytest
import sys

sys.path.append('.')
sys.path.append('./src')

from src.algorythm import Succession, SuccessionType, GeneticAlgorythm


def prepare_arguments_before_test(selection_type):
    seed(2137)
    np.random.seed(2137)
    algorythm = GeneticAlgorythm('resources/busy_day_mini.in', 4, 3, selection_type=selection_type)
    init_population = algorythm.initialize_population()
    rating = algorythm.evaluation(init_population)
    population = algorythm.mutation(init_population)

    succession = Succession()
    return succession, rating, population


def test_elite_succession():
    # given:
    succession, rating, population = prepare_arguments_before_test(SuccessionType.ELITE_SUCCESSION)
    succession_func = succession.return_succession_type(SuccessionType.ELITE_SUCCESSION)
    # when:
    s_population = succession_func(rating, population)
    # then:
    assert len(s_population) == len(population)
    assert len(s_population) == len(rating)
    assert s_population[0].weights == rating[0].weights
    assert id(s_population[0]) != id(rating[0])


def test_steady_state_succession():
    # given:
    succession, rating, population = prepare_arguments_before_test(SuccessionType.STEADY_STATE_SUCCESSION)
    succession_func = succession.return_succession_type(SuccessionType.STEADY_STATE_SUCCESSION)
    # when:
    s_population = succession_func(rating, population)
    # then:
    assert len(s_population) == len(population)
    assert len(s_population) == len(rating)


@pytest.mark.parametrize("succession_type",
                         [SuccessionType.NONE,
                          SuccessionType.GENERATIONAL_SUCCESSION])
def test_no_succession(succession_type):
    # given:
    succession, rating, population = prepare_arguments_before_test(succession_type)
    succession_func = succession.return_succession_type(succession_type)
    # when:
    co_population = succession_func(rating, population)
    # then:
    assert len(co_population) == len(population)
    assert id(co_population[0]) != id(population[0])


@pytest.mark.parametrize("succession_type, func_name",
                         [(SuccessionType.ELITE_SUCCESSION, "elite_succession"),
                          (SuccessionType.GENERATIONAL_SUCCESSION, "generational_succession"),
                          (SuccessionType.STEADY_STATE_SUCCESSION, "steady_state_succession")])
def test_return_succession_type(succession_type, func_name):
    cross_over = Succession()
    func = cross_over.return_succession_type(succession_type)
    assert func.__name__ == func_name
