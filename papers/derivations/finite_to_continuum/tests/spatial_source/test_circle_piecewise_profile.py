from fractions import Fraction as Q
import pytest
from omega_engine_projects.finite_to_continuum.code.circle_piecewise_linear import CirclePiecewiseLinear as P


def test_one_immutable_periodic_profile_has_exact_all_grid_targets():
    source = [[0, 0], [Q(1, 2), 1], [1, 0]]
    p = P(source)
    source[1][1] = 200  # Constructor retained an immutable value, not caller storage.
    assert p.norm == 1 and p.lipschitz == 2 and p.square_integral == Q(1, 3)
    assert p.uniform_samples(4) == (0, Q(1, 2), 1, Q(1, 2))
    assert p.evaluate(Q(-1, 4)) == Q(1, 2) and p.evaluate(Q(3, 2)) == 1
    for l in (4, 8, 16):
        assert sum(v*v for v in p.uniform_samples(l))/l-p.square_integral == Q(2, 3*l*l)


def test_constant_and_signed_profiles_do_not_require_positive_weights():
    constant = P(((0, -2), (1, -2)))
    assert constant.norm == 2 and constant.lipschitz == 0 and constant.square_integral == 4
    signed = P(((0, -1), (Q(1, 2), 1), (1, -1)))
    assert signed.square_integral == Q(1, 3) and signed.lipschitz == 4


@pytest.mark.parametrize("knots", (
    (), ((0, 0),), ((0, 0), (1, 1)), ((0, 0), (0, 0), (1, 0)),
    ((Q(1, 2), 0), (1, 0)), ((0, 0.0), (1, 0)), ((0, True), (1, True)),
))
def test_nonperiodic_ambiguous_and_inexact_profiles_refuse(knots):
    with pytest.raises((TypeError, ValueError)):
        P(knots)


@pytest.mark.parametrize("nodes", (0, 257, True, 4.0))
def test_grid_resource_or_inexact_counts_refuse(nodes):
    with pytest.raises((TypeError, ValueError)):
        P(((0, 0), (1, 0))).uniform_samples(nodes)
