"""Finite certificates and independent matrix checks for §7.8."""

from fractions import Fraction as F
from itertools import combinations, product

import pytest
from physical_obstruction import (
    cycle_gradient,
    cycle_minimizer,
    cycle_quotient,
    product_distance_lower_bound,
    product_moment_defect,
    verify_cycle_certificate,
)


@pytest.mark.parametrize("values", [(1, -2, 4), (F(2, 7), 0, -1, 3, F(1, 3))])
def test_cycle_primal_dual_certificate_and_gauge_invariance(values):
    potential = cycle_minimizer(values)
    mass = cycle_quotient(values)
    assert verify_cycle_certificate(values, potential, mass)
    shifted = tuple(x + y for x, y in zip(values, cycle_gradient(range(len(values)))))
    assert cycle_quotient(shifted) == mass
    assert not verify_cycle_certificate(values, potential, mass + 1)
    corrupted = (potential[0] + 100,) + potential[1:]
    assert not verify_cycle_certificate(values, corrupted, mass)


def test_cycle_zero_class_is_exact_not_just_closed():
    values = (3, -2, -1, 0, 0)
    assert cycle_quotient(values) == 0
    assert cycle_gradient(cycle_minimizer(values)) == values
    assert cycle_quotient((-1,) * 5) == 1


@pytest.mark.parametrize("value", [0.0, True, "1/2"])
def test_inexact_or_coerced_certificate_data_is_refused(value):
    with pytest.raises(TypeError):
        cycle_quotient((value, 0, 0))
    with pytest.raises(TypeError):
        verify_cycle_certificate((0, 0, 0), (0, 0, 0), value)


def test_malformed_shapes_and_measurement_budgets_are_refused():
    with pytest.raises(ValueError):
        cycle_minimizer((1, 2))
    with pytest.raises(ValueError):
        verify_cycle_certificate((0, 0, 0), (0, 0, 0, 0), 0)
    with pytest.raises(ValueError):
        product_moment_defect(2, (0, 0))
    with pytest.raises(ValueError):
        product_distance_lower_bound((1, 1, 1), True)
    with pytest.raises(ValueError):
        product_distance_lower_bound((1, 1, 1), 3, F(-1, 10))
    with pytest.raises(ValueError):
        product_distance_lower_bound((3, 0, 0), 3)


def test_product_reports_and_noise_floor():
    factors = (F(1, 2), F(-1, 3), F(2, 5))
    assert product_moment_defect(F(-1, 15), factors) == 0
    assert product_moment_defect(-1, (0, 0, 0)) == -1
    assert product_distance_lower_bound((-1,) * 5, 3) == F(1, 4)
    assert product_distance_lower_bound((-1,) * 5, 3, F(1, 20)) == F(1, 5)
    assert product_distance_lower_bound((-1,) * 5, 3, F(1, 2)) == 0


def test_product_telescoping_constant_for_exact_moment_endpoints():
    values = (F(-1), F(-1, 2), F(0), F(1, 2), F(1))
    for left in product(values, repeat=3):
        for right in ((F(0),) * 3, (F(1),) * 3, (F(-1),) * 3):
            bound = sum(abs(x - y) for x, y in zip(left, right))
            assert abs(product_moment_defect(0, left)
                       - product_moment_defect(0, right)) <= bound


def test_cycle_incidence_kernel_and_rotation_covariance():
    sp = pytest.importorskip("sympy")
    for size in (5, 6, 11):
        d0 = sp.zeros(size)
        shift = sp.zeros(size)
        for j in range(size):
            d0[j, j], d0[j, (j + 1) % size] = -1, 1
            shift[j, (j + 1) % size] = 1
        ell = sp.ones(1, size) / size
        assert ell * d0 == sp.zeros(1, size)
        assert d0.rank() == size - 1
        assert d0 * shift == shift * d0
        assert sp.zeros(0, size) * d0 == sp.zeros(0, size)


@pytest.mark.parametrize("size", [5, 6])
def test_cycle_graph_state_pair_blindness_and_nonzero_measured_class(size):
    sp = pytest.importorskip("sympy")
    from short_time_jets import I2, X, Z, partial_trace, tensor

    signs = [(-1) ** (sum(bits) + sum(bits[j] * bits[(j + 1) % size]
                                    for j in range(size)))
             for bits in product((0, 1), repeat=size)]
    vector = sp.Matrix(signs)
    rho = vector * vector.T / 2**size
    assert rho * rho == rho
    for pair in combinations(range(size), 2):
        assert partial_trace(rho, (2,) * size, pair) == sp.eye(4) / 4
    for j in range(size):
        factors = [I2] * size
        factors[j], factors[(j - 1) % size], factors[(j + 1) % size] = X, Z, Z
        assert sp.trace(tensor(*factors) * rho) == -1
    assert product_distance_lower_bound((-1,) * size, 3) == F(1, 4)


def test_ising_ring_moment_is_derived_from_heisenberg_conjugation():
    sp = pytest.importorskip("sympy")
    from short_time_jets import I2, PLUS, X, Z, state_jets, tensor

    left, right, t = sp.symbols("left right t", real=True)
    p, q = tensor(Z, Z, I2), tensor(I2, Z, Z)
    unitary = ((sp.cos(left * t) * sp.eye(8) - sp.I * sp.sin(left * t) * p)
               * (sp.cos(right * t) * sp.eye(8) - sp.I * sp.sin(right * t) * q))
    rho, observable = tensor(PLUS, PLUS, PLUS), tensor(Z, X, Z)
    mean = sp.trace(unitary.H * observable * unitary * rho)
    assert sp.trigsimp(mean + sp.sin(2 * left * t) * sp.sin(2 * right * t)) == 0
    jets = state_jets(left * p + right * q, rho, 4)
    measured = [sp.simplify(sp.trace(observable * jet)) for jet in jets]
    assert measured[:4] == [0, 0, -8 * left * right, 0]
    assert sp.expand(measured[4] - 64 * left * right * (left**2 + right**2)) == 0


def test_actual_linear_observer_has_unretained_directions():
    sp = pytest.importorskip("sympy")
    from short_time_jets import I2, X, Z, tensor

    hidden = tensor(X, X, I2, I2, I2)
    for j in range(5):
        for pauli in (X, Z):
            factors = [I2] * 5
            factors[j] = pauli
            assert sp.trace(tensor(*factors) * hidden) == 0
        factors = [I2] * 5
        factors[j], factors[(j - 1) % 5], factors[(j + 1) % 5] = X, Z, Z
        assert sp.trace(tensor(*factors) * hidden) == 0


def test_positive_quotient_does_not_exclude_separable_classical_mixtures():
    sp = pytest.importorskip("sympy")
    from short_time_jets import I2, PLUS, ZERO, X, Z, partial_trace, tensor

    one = I2 - ZERO
    rho = (tensor(ZERO, PLUS, ZERO, ZERO, ZERO)
           + tensor(one, PLUS, one, one, one)) / 2
    product_state = tensor(*(partial_trace(rho, (2,) * 5, (j,)) for j in range(5)))
    cochain = []
    for j in range(5):
        factors = [I2] * 5
        factors[j], factors[(j - 1) % 5], factors[(j + 1) % 5] = X, Z, Z
        value = sp.trace(tensor(*factors) * (rho - product_state))
        cochain.append(F(int(value.p), int(value.q)))
    assert cochain == [0, 1, 0, 0, 0]
    assert cycle_quotient(cochain) == F(1, 5)
