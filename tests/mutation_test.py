from algorythm import Mutation, GeneticAlgorythm, MutationType

from random import seed
import numpy as np
import pytest
import sys

sys.path.append('.')
sys.path.append('./src')


def prepare_arguments_before_test(mutation_type):
    seed(2137)
    np.random.seed(2137)
    algorythm = GeneticAlgorythm('resources/busy_day_mini.in', 20, 100, mutation_type=mutation_type)
    population = algorythm.initialize_population()
    mutation = Mutation()
    return mutation, population


@pytest.mark.parametrize("mutation_type, amount_expected_changes",
                         [(MutationType.UNIFORM_MUTATION, 3),
                          (MutationType.GAUSSIAN_MUTATION, 3),
                          (MutationType.CAUCHY_MUTATION, 3),
                          (MutationType.NONE, 7)])
def test_mutation(mutation_type, amount_expected_changes):
    # given:
    mutation, population = prepare_arguments_before_test(mutation_type)
    ex_population = [population[0]]
    mutation_func = mutation.return_mutation_type(mutation_type)
    # when:
    m_population = mutation_func(ex_population)
    # then:
    ex_weights = ex_population[0].weights
    m_weights = m_population[0].weights
    shared_items = {key: m_weights[key] for key in m_weights if m_weights[key] == ex_weights[key]}
    assert len(shared_items) == amount_expected_changes


@pytest.mark.parametrize("mutation_type, func_name",
                         [(MutationType.UNIFORM_MUTATION, "uniform_mutation"),
                          (MutationType.GAUSSIAN_MUTATION, "gaussian_mutation"),
                          (MutationType.CAUCHY_MUTATION, "cauchy_mutation"),
                          (MutationType.NONE, "no_mutation")])
def test_return_mutation_type(mutation_type, func_name):
    mutation = Mutation()
    func = mutation.return_mutation_type(mutation_type)
    assert func.__name__ == func_name
