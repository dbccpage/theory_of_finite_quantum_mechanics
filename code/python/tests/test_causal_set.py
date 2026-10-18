"""Tests for exact finite causal sets and Benincasa-Dowker interval action."""

from fractions import Fraction
import pytest
from src.general_relativity.causal_set import CausalSet, PosetError, AUTHORITY_FENCE


def test_discrete_causal_set():
    cs = CausalSet.discrete(4, label="discrete_4")
    assert cs.degree == 4
    assert cs.ordering_fraction() == Fraction(0)
    assert cs.spacelike(0, 1) is True
    assert cs.two_dimensional_interval_action() == 4
    assert cs.authority_fence() == AUTHORITY_FENCE


def test_chain_causal_set():
    # Linear chain 0 -> 1 -> 2 -> 3
    relations = [(0, 1), (1, 2), (2, 3)]
    cs = CausalSet.from_relations(4, relations, label="chain_4")

    assert cs.degree == 4
    # All pairs are comparable, total 6 pairs
    assert cs.order.relation_count() == 6
    assert cs.ordering_fraction() == Fraction(1)
    assert cs.spacelike(0, 3) is False

    # Alexandrov intervals
    assert cs.alexandrov_interval(0, 2) == [0, 1, 2]
    assert cs.past(2) == [0, 1]
    assert cs.future(1) == [2, 3]

    # Interval abundances:
    # Open intervals:
    # len 0: (0,1), (1,2), (2,3) -> 3 pairs
    # len 1: (0,2) has {1}, (1,3) has {2} -> 2 pairs
    # len 2: (0,3) has {1, 2} -> 1 pair
    abundances = cs.interval_abundances()
    assert abundances == [3, 2, 1]

    # Action: N - 2*N_0 + 4*N_1 - 2*N_2 = 4 - 2(3) + 4(2) - 2(1) = 4 - 6 + 8 - 2 = 4
    assert cs.two_dimensional_interval_action() == 4


def test_causal_set_cycle_detection():
    # Cycle 0 -> 1 -> 0 should raise PosetError
    with pytest.raises(PosetError):
        CausalSet.from_relations(2, [(0, 1), (1, 0)])
