"""Integral triangle quotients for arbitrary signed attachment degrees."""
import itertools
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preservation import protocol, triangle_degree_class  # noqa: E402


def test_classes_exactly_modulo_the_attached_boundary():
    for m in range(-8, 9):
        for k, other in itertools.product(range(-20, 21), repeat=2):
            expected = k == other if m == 0 else (k-other) % abs(m) == 0
            assert (triangle_degree_class(m, [k]*3) == triangle_degree_class(m, [other]*3)) == expected
        for chain in itertools.product(range(-2, 3), repeat=3):
            if len(set(chain)) != 1:
                with pytest.raises(ValueError):
                    triangle_degree_class(m, chain)


def test_nonzero_generator_has_exact_finite_order():
    for m in range(-12, 13):
        if m:
            order = abs(m)
            assert triangle_degree_class(m, [order]*3) == 0
            assert all(triangle_degree_class(m, [k]*3) != 0 for k in range(1, order))
            assert len({triangle_degree_class(m, [k]*3) for k in range(order)}) == order
        else:
            assert all(triangle_degree_class(0, [k]*3) == k for k in range(-20, 21))


@pytest.mark.parametrize("field", ["2,1,1", "02,1,1,1", "2,1,1,0", "2,1000001,1000001,1000001"])
def test_degree_protocol_refusals(field):
    assert protocol("v1\ttriangle_degree\t"+field) == "REFUSE"
