"""Adversarial scalar fixtures; binary floats here are rejection probes only."""
from fractions import Fraction

import pytest

from src.finite_probability.simplex import ProbabilitySimplex, SimplexError, StochasticMap
from src.bin import BinWitnessError, ray_power_two
from src.bin.entropy_cli import ParityError, collision_probability


class LeakingFraction(Fraction):
    def __mul__(self, other):
        return 0.5


class AdditionLeak(Fraction):
    def __radd__(self, other):
        return 1.0


@pytest.mark.parametrize("scalar", [LeakingFraction(1), AdditionLeak(1)])
def test_distribution_admission_refuses_overridden_fraction_arithmetic(scalar):
    with pytest.raises(SimplexError, match="not an exact rational"):
        ProbabilitySimplex([scalar])
    with pytest.raises(SimplexError, match="not an exact rational"):
        StochasticMap([[scalar]])


@pytest.mark.parametrize("scalar", [LeakingFraction(1), AdditionLeak(1)])
def test_simplex_operations_refuse_subclass_coefficients(scalar):
    state = ProbabilitySimplex([1])
    with pytest.raises(SimplexError, match="not an exact rational"):
        state.expectation([scalar])
    with pytest.raises(SimplexError, match="not an exact rational"):
        state.mixture(state, scalar)


@pytest.mark.parametrize("scalar", [LeakingFraction(1), AdditionLeak(1)])
def test_ray_and_collision_refuse_subclasses(scalar):
    with pytest.raises(BinWitnessError, match="not an exact rational"):
        ray_power_two((scalar, 0, 0))
    with pytest.raises(ParityError, match="not an exact rational"):
        collision_probability((scalar,))


def test_exact_controls_have_an_independent_arithmetic_basis():
    # E[X] = 1/3 * 2 + 2/3 * (-1) = 0; purity = 1/9 + 4/9.
    state = ProbabilitySimplex([Fraction(1, 3), Fraction(2, 3)])
    assert state.expectation([2, -1]) == Fraction(0)
    assert type(state.expectation([2, -1])) is Fraction
    assert collision_probability((Fraction(1, 3), Fraction(2, 3))) == Fraction(5, 9)
    assert ray_power_two((Fraction(3, 5), Fraction(4, 5), 0)) == Fraction(1)
    assert StochasticMap([[0, 1], [1, 0]]).apply(state).probs == [Fraction(2, 3), Fraction(1, 3)]
