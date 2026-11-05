"""Exact connected/disconnected and locality controls for §5.14."""

from math import factorial

import pytest

sp = pytest.importorskip("sympy")

from derivation_replays import (
    compositions,
    cumulant_constants,
    cumulant_jets,
    hermitian_trace_norm,
    partitions,
    placed_tensor,
    support_component,
)
from short_time_jets import I2, ZERO, X, Y, Z, defect_jets, state_jets, tensor


@pytest.mark.parametrize("factors", [(I2,), (I2, I2, I2)])
def test_placed_tensor_rejects_missing_or_extra_factors(factors):
    with pytest.raises(ValueError, match="one matrix per tensor block"):
        placed_tensor(((0,), (1,)), factors, (2, 2))


@pytest.mark.parametrize("factor", [sp.eye(3), sp.ones(2, 1)])
def test_placed_tensor_rejects_mismatched_block_shapes(factor):
    with pytest.raises(ValueError, match="matrix shape"):
        placed_tensor(((0,), (1,)), (factor, I2), (2, 2))


def test_placed_tensor_restores_heterogeneous_factors():
    first, second = sp.diag(2, 3), sp.diag(5, 7, 11)
    assert placed_tensor(((1,), (0,)), (second, first), (2, 3)) == tensor(first, second)


def test_connected_replays_reject_inexact_matrices_before_tracing():
    rho = sp.diag(sp.Float("0.5"), sp.Float("0.5"), 0, 0)
    for operation in (
        lambda: cumulant_jets([rho], (2, 2), (0, 1)),
        lambda: support_component(rho, (2, 2), (0, 1)),
        lambda: placed_tensor(((0, 1),), (rho,), (2, 2)),
    ):
        with pytest.raises(TypeError, match="exact scalar"):
            operation()


def test_two_independent_bell_pairs_have_no_connected_four_cumulant():
    vector = sp.Matrix([1, 0, 0, 1])
    bell = vector * vector.T / 2
    rho = tensor(bell, bell)
    highest = support_component(rho, (2,) * 4, (0, 1, 2, 3))
    assert highest == tensor(bell - sp.eye(4) / 4, bell - sp.eye(4) / 4)
    assert hermitian_trace_norm(highest) == sp.Rational(9, 4)
    assert cumulant_jets([rho], (2,) * 4, (0, 1, 2, 3))[0] == sp.zeros(16)


def test_pair_cumulant_agrees_with_independent_defect_implementation():
    h = tensor(X, X, I2) + tensor(I2, Y, X)
    rho = tensor(ZERO, ZERO, ZERO)
    derivatives = state_jets(h, rho, 3)
    assert cumulant_jets(derivatives, (2,) * 3, (0, 2)) == defect_jets(h, rho, (2,) * 3, (0, 2), 3)


def test_chain_steiner_onset_is_sharp_for_pair_and_triple():
    h = tensor(X, X, I2) + tensor(I2, Y, X)
    derivatives = state_jets(h, tensor(ZERO, ZERO, ZERO), 2)
    pair = cumulant_jets(derivatives, (2,) * 3, (0, 2))
    triple = cumulant_jets(derivatives, (2,) * 3, (0, 1, 2))
    assert pair[:2] == [sp.zeros(4)] * 2
    expected = sp.zeros(4)
    expected[1, 2], expected[2, 1] = 2 * sp.I, -2 * sp.I
    assert pair[2] == expected and hermitian_trace_norm(pair[2]) == 4
    assert triple[:2] == [sp.zeros(8)] * 2
    assert hermitian_trace_norm(triple[2]) == 8


def test_triple_second_jet_ignores_external_incident_edge():
    base = tensor(X, X, I2) + tensor(I2, Y, X)
    full = tensor(base, I2) + 7 * tensor(I2, I2, Z, X)
    small = cumulant_jets(state_jets(base, tensor(ZERO, ZERO, ZERO), 2), (2,) * 3, (0, 1, 2))
    large = cumulant_jets(state_jets(full, tensor(ZERO, ZERO, ZERO, ZERO), 2), (2,) * 4, (0, 1, 2))
    assert large == small  # j-k+1 = 0: the induced support alone suffices.


def test_disconnected_interactions_cancel_all_computed_connected_jets():
    h = tensor(X, X, I2, I2) + tensor(I2, I2, Y, Y)
    derivatives = state_jets(h, tensor(ZERO, ZERO, ZERO, ZERO), 2)
    assert cumulant_jets(derivatives, (2,) * 4, (0, 1, 2, 3)) == [sp.zeros(16)] * 3


def test_partition_constants_and_multinomial_derivative_identity():
    assert [cumulant_constants(k) for k in range(1, 7)] == [
        (1, 1), (2, 3), (6, 13), (26, 75), (150, 541), (1082, 4683)]
    for k in range(2, 5):
        for partition in partitions(tuple(range(k))):
            for j in range(5):
                lhs = 0
                for degrees in compositions(j, len(partition)):
                    term = sp.Integer(factorial(j))
                    for block, degree in zip(partition, degrees):
                        term *= sp.rf(len(block), degree) / factorial(degree)
                    lhs += term
                assert lhs == sp.rf(k, j)


def test_reference_components_sum_to_the_product_residual_without_singletons():
    # A rational density with correlations on overlapping supports.
    rho = (sp.eye(8) + tensor(X, X, I2) / 3 + tensor(I2, X, X) / 5) / 8
    components = []
    for mask in range(8):
        support = tuple(i for i in range(3) if mask & (1 << i))
        value = support_component(rho, (2,) * 3, support)
        if len(support) == 1:
            assert value == sp.zeros(8)
        components.append(value)
    assert sum(components, sp.zeros(8)) == rho
    assert components[0] == sp.eye(8) / 8


def test_augmented_cochain_observation_needs_cohomology_and_uniform_bounds():
    # Coordinates (repair, curvature, cohomology), B=span(e0).
    d0 = sp.Matrix([1, 0, 0])
    d1 = sp.Matrix([[0, 1, 0]])
    ell = sp.Matrix([[0, 0, 1]])
    assert d1 * d0 == ell * d0 == sp.zeros(1, 1)
    assert sp.Matrix.vstack(d1, ell).nullspace() == [d0]
    assert len(d1.nullspace()) == 2  # curvature alone misses retained H^1
    x = sp.Matrix([0, 1, 0])
    for size in (2, 7, 31):
        observed = (d1 * x)[0] / size + (ell * x)[0]
        assert observed == sp.Rational(1, size)  # quotient norm is 1; K >= size
