from dataclasses import replace
from fractions import Fraction as Q
from itertools import product

import pytest
from witnessed_difference.empirical_repair import (
    Scenario,
    iid_l1_failure,
    repair,
    sampling_tolerance,
    verify_repair,
)
from witnessed_difference.outcomes import Accepted, Refused


def test_three_context_radius_and_actual_input_bound_replay():
    site = Scenario(1, 3, ((0,),) * 3)
    source = tuple(tuple(Q(int(i == j)) for j in range(3)) for i in range(3))
    result = repair(site, source)
    assert isinstance(result, Accepted)
    receipt = result.value
    assert receipt.radius == Q(4, 3) > Q(1)
    assert receipt.repaired == ((Q(1, 3),) * 3,) * 3
    assert verify_repair(site, source, receipt)
    assert not verify_repair(site, source, replace(receipt, radius=Q(1)))
    assert not verify_repair(site, source, replace(receipt, repaired=tuple(tuple(float(v) for v in p)
                                                                         for p in receipt.repaired)))
    assert not verify_repair(site, source, replace(receipt, source=tuple(tuple(float(v) for v in p)
                                                                       for p in source)))
    assert not verify_repair(site, source, replace(receipt, source=tuple(tuple(bool(v) for v in p)
                                                                       for p in source)))
    assert not verify_repair(site, source, replace(receipt, optimum=replace(receipt.optimum,
                                                                         dual=(Q(0),) * len(receipt.optimum.dual))))
    replacement = ((Q(1), Q(0), Q(0)),) * 3
    assert not verify_repair(site, source, repair(site, replacement).value)
    assert isinstance(repair(site, source, max_pivots=0), Refused)


def test_two_contexts_and_compatible_pr_do_not_force_a_joint_model():
    site = Scenario(1, 2, ((0,),) * 2)
    assert repair(site, ((Q(1), Q(0)), (Q(0), Q(1)))).value.radius == Q(1)
    pr = Scenario(4, 2, ((0, 2), (0, 3), (1, 2), (1, 3)))
    equal, opposite = (Q(1, 2), Q(0), Q(0), Q(1, 2)), (Q(0), Q(1, 2), Q(1, 2), Q(0))
    source = (equal, equal, equal, opposite)
    assert pr.compatible(source)
    assert repair(pr, source).value.radius == 0
    # Every deterministic global assignment violates at least one PR equation.
    assert all(not (a0 == b0 and a0 == b1 and a1 == b0 and a1 != b1)
               for a0, a1, b0, b1 in product(range(2), repeat=4))


def test_iid_bound_against_exact_trial_enumeration_and_protocol():
    n, p, r = 4, Q(1, 3), Q(1, 2)
    failure, mean_square = Q(0), Q(0)
    for trial in product(range(2), repeat=n):
        count = sum(trial)
        probability = p ** count * (1 - p) ** (n - count)
        distance = 2 * abs(Q(count, n) - p)
        failure += probability * int(distance > r)
        mean_square += probability * distance ** 2
    assert mean_square == 4 * p * (1 - p) / n <= Q(1, n)
    assert failure <= iid_l1_failure(n, 2, r)
    site = Scenario(1, 2, ((0,),) * 2)
    pairs, failure = sampling_tolerance(site, (((0,),) * 400,) * 2, (Q(1, 10),) * 2)
    assert pairs == ((0, 1, Q(1, 5)),) and failure == Q(1, 2)
    assert iid_l1_failure(1, 100, Q(2)) == 0
    with pytest.raises(ValueError):
        Scenario(2, 2, ((0, 1),), max_sections=3)
    with pytest.raises(ValueError):
        sampling_tolerance(site, (((0,),), ()), (Q(1),) * 2)


def test_max_cells_dense_matrix_budget_exhausted():
    site = Scenario(1, 2, ((0,),) * 2, max_cells=10)
    source = ((Q(1), Q(0)), (Q(0), Q(1)))
    with pytest.raises(ValueError, match="declared dense matrix cell budget exhausted"):
        site.repair_program(source)
