from random import seed
import numpy as np
import pytest
import sys

sys.path.append('.')
sys.path.append('./src')

from src.algorythm import Selection, SelectionType, GeneticAlgorythm


def prepare_arguments_before_test(selection_type):
    seed(2137)
    np.random.seed(2137)
    algorythm = GeneticAlgorythm('resources/busy_day.in', 4, 3, selection_type=selection_type)
    population = algorythm.initialize_population()

    for simulation in population:
        simulation.score = np.random.randint(0, 100)
    selection = Selection()
    return selection, population


@pytest.mark.parametrize("selection_type, expected_score",
                         [(SelectionType.TOURNAMENT_SELECTION, [62, 64, 64, 62]),
                          (SelectionType.RANK_SELECTION, [62, 62, 64, 64]),
                          (SelectionType.ROULETTE_WHEEL_SELECTION, [62, 62, 64, 62])])
def test_selection(selection_type, expected_score):
    # given:
    selection, population = prepare_arguments_before_test(selection_type)
    selection_func = selection.return_selection_type(selection_type)
    # when:
    s_population = selection_func(population)
    # then:
    sp_score = [simulation.score for simulation in s_population]
    assert sp_score == expected_score
    assert len(s_population) == len(population)


def test_no_selection():
    # given:
    selection, population = prepare_arguments_before_test(SelectionType.NONE_SELECTION)
    selection_func = selection.return_selection_type(SelectionType.NONE_SELECTION)
    # when:
    s_population = selection_func(population)
    # then:
    assert [simulation.score for simulation in s_population] == [simulation.score for simulation in population]
    assert len(s_population) == len(population)


@pytest.mark.parametrize("selection_type, func_name",
                         [(SelectionType.TOURNAMENT_SELECTION, "tournament_selection"),
                          (SelectionType.RANK_SELECTION, "rank_selection"),
                          (SelectionType.ROULETTE_WHEEL_SELECTION, "roulette_wheel_selection")])
def test_return_selection_type(selection_type, func_name):
    selection = Selection()
    func = selection.return_selection_type(selection_type)
    assert func.__name__ == func_name
