"""Exact incidence identities and numerical scalar Hodge decompositions."""

import numpy as np
import pytest
from coda_higher_cell.simplicial_complex import (
    SimplicialComplex,
    hodge_decomposition,
    simplicial_boundary_matrix,
    simplicial_coboundary_matrix,
    simplicial_laplacian,
)


@pytest.mark.parametrize("simplices", [[(0, 1, 2)], [(0, 1, 2, 3)]])
def test_incidence_nilpotence(simplices):
    k = SimplicialComplex(simplices)
    for p in range(1, k.max_dimension):
        b0, b1 = simplicial_boundary_matrix(k, p), simplicial_boundary_matrix(k, p + 1)
        assert np.array_equal(b0 @ b1, np.zeros((b0.shape[0], b1.shape[1]), dtype=int))
        assert np.array_equal(
            simplicial_coboundary_matrix(k, p) @ simplicial_coboundary_matrix(k, p - 1), (b0 @ b1).T
        )


def test_hollow_filled_triangle_and_complex_hodge():
    hollow = SimplicialComplex([(0, 1), (0, 2), (1, 2)])
    filled = SimplicialComplex([(0, 1, 2)])
    cycle = np.array([1, -1, 1], dtype=complex)
    lap = simplicial_laplacian(hollow, 1)
    assert np.array_equal(lap @ cycle, np.zeros(3))
    assert np.array_equal(simplicial_laplacian(filled, 1), 3 * np.eye(3))
    omega = cycle * (1 + 2j) + np.array([1, 2, 1])
    exact, coexact, harmonic = hodge_decomposition(omega, hollow, 1)
    assert np.allclose(harmonic, (1 + 2j) * cycle)
    assert np.allclose(exact + coexact + harmonic, omega)
    for a, b in [(exact, coexact), (exact, harmonic), (coexact, harmonic)]:
        assert abs(np.vdot(a, b)) < 1e-10
    assert np.allclose(lap @ harmonic, 0)
    _, coexact_f, harmonic_f = hodge_decomposition(cycle, filled, 1)
    assert np.allclose(coexact_f, cycle)
    assert np.allclose(harmonic_f, 0)


def test_degree_zero_empty_and_missing_degree():
    k = SimplicialComplex([(0,), (1,)])
    exact, coexact, harmonic = hodge_decomposition(np.array([1, 2]), k, 0)
    assert np.array_equal(exact, [0, 0]) and np.array_equal(coexact, [0, 0])
    assert np.array_equal(harmonic, [1, 2])
    empty = SimplicialComplex([])
    assert empty.max_dimension == -1
    assert simplicial_laplacian(empty, 0).shape == (0, 0)
    assert all(x.shape == (0,) for x in hodge_decomposition(np.array([]), empty, 0))
    assert simplicial_laplacian(k, 4).shape == (0, 0)


@pytest.mark.parametrize("simplices", [[()], [(1, 1)], [(-1, 2)], [(True, 2)]])
def test_invalid_complex(simplices):
    with pytest.raises(ValueError):
        SimplicialComplex(simplices)


@pytest.mark.parametrize(
    "cochain,tol",
    [
        (np.array([1, 2]), 1e-10),
        (np.ones((3, 1)), 1e-10),
        (np.array([1, np.nan, 3]), 1e-10),
        (np.ones(3), 0),
        (np.ones(3), np.nan),
        (np.ones(3), 1),
    ],
)
def test_invalid_hodge_inputs(cochain, tol):
    with pytest.raises(ValueError):
        hodge_decomposition(cochain, SimplicialComplex([(0, 1, 2)]), 1, tol)


def test_negative_degree_and_orientation_canonicalization():
    k = SimplicialComplex([(2, 0, 1), (0, 1, 2)])
    assert k.get_simplices(2) == [(0, 1, 2)]
    with pytest.raises(ValueError):
        simplicial_boundary_matrix(k, -1)
