"""Pairwise minimality and negative controls for the paper repair reference."""

from itertools import combinations, product

import pytest

from ..report_repair import least_repair, replay_repair, split_class


def test_all_4681_small_tables_reach_the_least_repair_within_class_bound():
    checked = 0
    for n in range(5):
        for values in product(range(2), repeat=2 * n):
            answers = [values[2 * i:2 * i + 2] for i in range(n)]
            for report in product(range(2), repeat=n):
                current = least_repair(report, [() for _ in report])
                steps = []
                while True:
                    witness = next(((i, j, q) for i, j in combinations(range(n), 2)
                                    if current[i] == current[j]
                                    for q in range(2) if answers[i][q] != answers[j][q]), None)
                    if witness is None:
                        break
                    before = len(set(current))
                    current = split_class(current, answers, *witness)
                    assert len(set(current)) > before
                    steps.append(witness)
                target = least_repair(report, answers)
                assert len(steps) <= len(set(target)) - len(set(report))
                assert replay_repair(report, answers, steps, current)
                for i, j in combinations(range(n), 2):
                    assert (current[i] == current[j]) == (
                        report[i] == report[j] and answers[i] == answers[j])
                checked += 1
    assert checked == 4681


def test_other_classes_and_unasked_distinctions_are_preserved():
    report = (0, 0, 1, 1)
    answers = ((0,), (1,), (0,), (1,))
    assert split_class(report, answers, 0, 1, 0) == (0, 1, 2, 2)
    assert least_repair((0, 1, 0), ((7,), (7,), (7,))) == (0, 1, 0)


def test_sharp_bound_and_alternative_witness_order():
    answers = ((0, 0), (1, 0), (0, 1))
    assert replay_repair((0, 0, 0), answers, [(0, 2, 1), (0, 1, 0)], (0, 1, 2))
    assert not replay_repair((0, 0, 0), answers, [], (0, 0, 0))
    assert not replay_repair((0, 0, 0), answers, [(0, 2, 1)], (0, 1, 2))
    assert split_class((0, 0, 0), ((0,), (1,), (2,)), 0, 1, 0) == (0, 1, 2)


@pytest.mark.parametrize("witness", [(-1, 1, 0), (0, 9, 0), (0, 1, 9), (0, 0, 0),
                                         (True, 1, 0), (0, 1, False), (0, 1, 0.0)])
def test_malformed_witnesses_refuse(witness):
    with pytest.raises(ValueError):
        split_class((0, 0), ((0,), (1,)), *witness)


@pytest.mark.parametrize("report,answers", [((0,), ()), ((False,), ((0,),)),
                                             ((0,), ((True,),)), ((0, 0), ((0,), ()))])
def test_malformed_tables_refuse(report, answers):
    with pytest.raises(ValueError):
        least_repair(report, answers)


def test_candidate_replay_refuses_booleans_and_oversplitting():
    with pytest.raises(ValueError):
        replay_repair((0,), ((0,),), [], (False,))
    assert not replay_repair((0, 0), ((0,), (0,)), [], (0, 1))
    assert least_repair((), ()) == ()
    assert least_repair((0, 1, 0), ((), (), ())) == (0, 1, 0)
