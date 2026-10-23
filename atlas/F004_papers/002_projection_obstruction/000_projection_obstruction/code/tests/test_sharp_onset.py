"""Exact instances and negative controls for §§5.17 and 7.8."""

from math import factorial

import pytest

sp = pytest.importorskip("sympy")

from derivation_replays import cumulant_jets  # noqa: E402
from short_time_jets import I2, ZERO, X, Y, Z, defect_jets, state_jets, tensor  # noqa: E402


def test_delayed_pair_onset_and_exact_exceptional_set():
    a, b = sp.symbols("a b", real=True)
    h = a * tensor(X, I2) + b * tensor(Z, X)
    jets = defect_jets(h, tensor(ZERO, ZERO), (2, 2), (0, 1), 2)
    assert jets[:2] == [sp.zeros(4)] * 2
    assert jets[2] == a * b * (tensor(X, X) - tensor(Y, Y))
    assert sp.trace(tensor(X, X) * jets[2]) == 4 * a * b
    # These higher jets are finite controls, not the all-time zero argument.
    for zero in ({a: 0}, {b: 0}):
        assert defect_jets(h.subs(zero), tensor(ZERO, ZERO), (2, 2), (0, 1), 4) == [sp.zeros(4)] * 5


def test_distinct_coupling_monomials_can_cancel():
    a, b = sp.symbols("a b", real=True)
    h = a * tensor(X, X) + b * tensor(Y, Y)
    jet = defect_jets(h, tensor(ZERO, ZERO), (2, 2), (0, 1), 1)[1]
    assert sp.trace(tensor(Y, X) * jet) == -2 * (a - b)
    assert jet.subs(b, a) == sp.zeros(4)
    assert h.subs(b, a) * tensor(ZERO, ZERO) == sp.zeros(4)


def test_tree_construction_three_vertices_includes_all_partition_subtractions():
    a, b = sp.symbols("a b", real=True)
    # Group incidence qubits by vertex: (0), (1,2), (3).
    h = a * tensor(X, X, I2, I2) + b * tensor(I2, I2, X, X)
    jets = cumulant_jets(state_jets(h, tensor(ZERO, ZERO, ZERO, ZERO), 2),
                         (2, 4, 2), (0, 1, 2))
    witness = tensor(Y, X, Y, X)
    assert jets[:2] == [sp.zeros(16)] * 2
    assert sp.trace(witness * jets[2]) == 8 * a * b


@pytest.mark.parametrize("edges", [((0, 1),), ((0, 1), (1, 2), (2, 3)),
                                   ((0, 1), (0, 2), (0, 3))])
def test_incidence_tree_moments_have_no_proper_subset_term(edges):
    t = sp.symbols("t", real=True)
    couplings = tuple(sp.Integer(i + 1) for i in range(len(edges)))
    vertices = sorted({v for edge in edges for v in edge})
    # Derive the edge moments from their two-qubit state independently.
    edge_means = []
    for coupling in couplings:
        vector = sp.Matrix([sp.cos(coupling * t), 0, 0, -sp.I * sp.sin(coupling * t)])
        rho = vector * vector.H
        for pauli in (X, Y):
            assert sp.trace(tensor(pauli, I2) * rho) == 0
            assert sp.trace(tensor(I2, pauli) * rho) == 0
        edge_means.append(sp.trigsimp(sp.trace(tensor(Y, X) * rho)))
    for mask in range(1, 2**len(vertices) - 1):
        retained = {v for v in vertices if mask & (1 << v)}
        assert any((u in retained) != (v in retained) for u, v in edges)
    moment = sp.prod(edge_means)
    order = len(edges)
    assert all(sp.diff(moment, t, j).subs(t, 0) == 0 for j in range(order))
    assert sp.diff(moment, t, order).subs(t, 0) == factorial(order) * (-2)**order * sp.prod(couplings)


def test_symmetry_odd_scalar_is_not_an_operator_zero_certificate():
    h, initial = tensor(X, X), tensor(ZERO, ZERO)
    symmetry, odd = tensor(Z, Z), tensor(X, Z)
    assert symmetry * h == h * symmetry
    assert symmetry * initial == initial * symmetry
    assert symmetry * odd * symmetry == -odd
    jets = defect_jets(h, initial, (2, 2), (0, 1), 2)
    assert jets[1] != sp.zeros(4)
    assert all(sp.trace(odd * jet) == 0 for jet in jets)


def test_local_closure_requires_the_boundary_commutator_check():
    boundary_ok, boundary_bad = tensor(Z, X), tensor(X, X)
    local_observable = tensor(Z, I2)
    assert boundary_ok * local_observable == local_observable * boundary_ok
    assert boundary_bad * local_observable != local_observable * boundary_bad
    # A vanishing first derivative alone cannot discard the bad boundary.
    initial = tensor(ZERO, ZERO)
    jets = state_jets(boundary_bad, initial, 2)
    assert sp.trace(local_observable * jets[1]) == 0
    assert sp.trace(local_observable * jets[2]) == -4
