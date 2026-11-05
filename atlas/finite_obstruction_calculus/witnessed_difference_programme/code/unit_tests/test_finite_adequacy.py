from fractions import Fraction
from itertools import product

import pytest
from witnessed_difference.finite_adequacy import AtomicValuation, ChainClock


def test_clock_adequacy_and_all_partition_refinements() -> None:
    clock = ChainClock((1, 2, 3, 4), (0, 2, 5, 7, 12), 1, (1, 1, 1, 1))
    for start in range(5):
        for stop in range(start, 5):
            discrepancy, budget = clock.interval_bound(start, stop)
            assert discrepancy <= budget
    for selected in product((False, True), repeat=3):
        cuts = (0,) + tuple(i + 1 for i, keep in enumerate(selected) if keep) + (4,)
        coarse = clock.coarsen(cuts)
        for start in range(len(cuts)):
            for stop in range(start, len(cuts)):
                assert coarse.interval_bound(start, stop) == clock.interval_bound(cuts[start], cuts[stop])


def test_clock_bound_is_sharp_and_survives_nonunit_calibration() -> None:
    clock = ChainClock((Fraction(1, 3), Fraction(2, 3)), (0, Fraction(1, 3), 1), 2, (Fraction(1, 3), Fraction(2, 3)))
    assert clock.interval_bound(0, 2) == (1, 1)
    assert clock.coarsen((0, 2)).interval_bound(0, 1) == (1, 1)
    empty = ChainClock((), (0,), 1, ())
    assert empty.coarsen((0,)).interval_bound(0, 0) == (0, 0)


@pytest.mark.parametrize("args", [
    ((1,), (0,), 1, (0,)),
    ((0,), (0, 0), 1, (0,)),
    ((1,), (0, 1), 0, (0,)),
    ((1,), (0, 1), 1, (-1,)),
    ((1,), (0, 2), 1, (0,)),
    ((1.0,), (0, 1), 1, (0,)),
    ((True,), (0, 1), 1, (0,)),
])
def test_clock_rejects_missing_hypotheses(args: tuple) -> None:
    with pytest.raises((TypeError, ValueError)):
        ChainClock(*args)


def test_clock_rejects_invalid_partitions_and_intervals() -> None:
    clock = ChainClock((1, 1), (0, 1, 2), 1, (0, 0))
    for cuts in ((), (1, 2), (0, 1), (0, 2, 2), (0, True, 2), (0, 3, 2)):
        with pytest.raises(ValueError):
            clock.coarsen(cuts)
    for start, stop in ((-1, 0), (0, 3), (2, 1), (True, 2)):
        with pytest.raises(ValueError):
            clock.interval_bound(start, stop)


def test_full_boolean_valuation_representation_and_uniqueness() -> None:
    for masses in product((0, Fraction(1, 3), Fraction(2, 3)), repeat=3):
        valuation = AtomicValuation(masses)
        table = tuple(valuation.event_mass(mask) for mask in range(8))
        reconstructed = AtomicValuation.from_event_table(table)
        assert reconstructed == valuation
        for left in range(8):
            for right in range(8):
                if left & right == 0:
                    assert table[left | right] == table[left] + table[right]
    assert AtomicValuation.from_event_table((0,)).masses == ()


@pytest.mark.parametrize("table", [(), (0, 1, 2), (1,), (0, -1), (0, 1, 1, 3), (0, 0.5)])
def test_full_event_table_rejects_countermodels(table: tuple) -> None:
    with pytest.raises((TypeError, ValueError)):
        AtomicValuation.from_event_table(table)


def test_atomic_distance_and_refinement_contractivity() -> None:
    fine = AtomicValuation((Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)))
    other = AtomicValuation((Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)))
    exact_distance = max(abs(fine.event_mass(mask) - other.event_mass(mask)) for mask in range(8))
    assert fine.event_distance(other) == exact_distance == Fraction(1, 4)
    assert fine.event_distance(other) == sum((abs(a - b) for a, b in zip(fine.masses, other.masses)), Fraction(0)) / 2
    for mapping in product(range(3), repeat=3):
        coarse = fine.pushforward(mapping, 3)
        other_coarse = other.pushforward(mapping, 3)
        assert coarse.event_distance(other_coarse) <= exact_distance
        for mask in range(8):
            pullback = sum(1 << i for i, target in enumerate(mapping) if mask & (1 << target))
            assert coarse.event_mass(mask) == fine.event_mass(pullback)
    # Unequal totals require max(positive, negative), not half the l1 formula.
    assert AtomicValuation((2, 1)).event_distance(AtomicValuation((0, 0))) == 3


def test_atomic_validation_rejects_type_and_carrier_confusion() -> None:
    valuation = AtomicValuation((1, 2))
    for mask in (-1, 4, True, 0.0):
        with pytest.raises(ValueError):
            valuation.event_mass(mask)
    for mapping, size in (((0,), 1), ((0, True), 2), ((0, 2), 2), ((0, 0), True), ((0, 0), -1)):
        with pytest.raises(ValueError):
            valuation.pushforward(mapping, size)
    with pytest.raises(ValueError):
        valuation.event_distance(AtomicValuation((1,)))
    with pytest.raises(ValueError):
        AtomicValuation((-1,))
    assert AtomicValuation(()).pushforward((), 0).masses == ()
