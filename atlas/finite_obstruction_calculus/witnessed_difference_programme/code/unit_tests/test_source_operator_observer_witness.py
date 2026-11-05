from fractions import Fraction

from witnessed_difference.source_operator_observer_witness import (
    incompatible_reference_fixture,
    missing_hypothesis_countermodels,
)


def test_actual_incompatible_reference_fixture():
    defects, dual, value = incompatible_reference_fixture()
    assert defects == ((Fraction(0), Fraction(0)), (Fraction(-1), Fraction(1)))
    assert value == Fraction(1)
    assert dual[0] == (Fraction(1, 2), Fraction(-1, 2))


def test_transport_and_control_hypotheses_are_independent():
    source, target, before, after = missing_hypothesis_countermodels()
    assert source < target
    assert sum(after) < sum(before)
    assert after[1] > before[1]
