"""Tests for ProbabilitySimplex and StochasticMap under exact rational arithmetic."""

import pytest
from fractions import Fraction
from src.finite_probability.simplex import (
    ProbabilitySimplex,
    StochasticMap,
)


def test_simplex_construction_and_normalization():
    # Valid distribution
    p = ProbabilitySimplex([Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)])
    assert p.dim == 3
    assert p[0] == Fraction(1, 2)
    assert p[1] == Fraction(1, 3)
    assert p[2] == Fraction(1, 6)

    # Uniform distribution
    u = ProbabilitySimplex.uniform(4)
    assert u.dim == 4
    for i in range(4):
        assert u[i] == Fraction(1, 4)

    # Dirac distribution
    d = ProbabilitySimplex.dirac(3, 1)
    assert d.probs == [Fraction(0), Fraction(1), Fraction(0)]

    # Non-normalizing errors
    with pytest.raises(ValueError):
        ProbabilitySimplex([Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)])
    with pytest.raises(ValueError):
        ProbabilitySimplex([-Fraction(1, 2), Fraction(3, 2)])


def test_total_variation_distance():
    p = ProbabilitySimplex.dirac(2, 0)
    q = ProbabilitySimplex.dirac(2, 1)
    assert p.total_variation_distance(q) == Fraction(1)
    assert p.total_variation_distance(p) == Fraction(0)

    u = ProbabilitySimplex.uniform(2)
    # TV(dirac(0), uniform) = 1/2 (|1 - 1/2| + |0 - 1/2|) = 1/2 (1/2 + 1/2) = 1/2
    assert p.total_variation_distance(u) == Fraction(1, 2)


def test_mixture_and_expectation():
    p = ProbabilitySimplex.dirac(2, 0)
    q = ProbabilitySimplex.dirac(2, 1)
    # 50/50 mixture gives uniform
    mix = p.mixture(q, Fraction(1, 2))
    assert mix.equals(ProbabilitySimplex.uniform(2)) if hasattr(mix, 'equals') else mix == ProbabilitySimplex.uniform(2)

    # Expectation of [10, 20] under uniform
    u = ProbabilitySimplex.uniform(2)
    assert u.expectation([10, 20]) == Fraction(15)


def test_stochastic_map_pushforward():
    # 2x2 transition matrix
    # [1/2, 1/2]
    # [0,   1  ]
    t = StochasticMap([
        [Fraction(1, 2), Fraction(1, 2)],
        [Fraction(0), Fraction(1)],
    ])
    p = ProbabilitySimplex([Fraction(1), Fraction(0)])
    p_next = t.apply(p)
    assert p_next.probs == [Fraction(1, 2), Fraction(1, 2)]

    # Steady state is absorbing at state 1
    p2 = ProbabilitySimplex([Fraction(0), Fraction(1)])
    assert t.apply(p2) == p2
