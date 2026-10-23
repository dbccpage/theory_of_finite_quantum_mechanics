"""Finite scalar simplicial cochains with constant coefficients."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from ._validation import integer, nonnegative


class SimplicialComplex:
    """Finite abstract complex; increasing tuples declare orientations."""

    def __init__(self, simplices: Sequence[tuple[int, ...]]) -> None:
        closure: set[tuple[int, ...]] = set()

        def add_faces(simplex: tuple[int, ...]) -> None:
            if simplex in closure:
                return
            closure.add(simplex)
            if len(simplex) > 1:
                for i in range(len(simplex)):
                    add_faces(simplex[:i] + simplex[i + 1 :])

        for raw in simplices:
            if not raw:
                raise ValueError("empty simplices are not supported; use [] for the empty complex")
            vertices = tuple(integer(v, "vertex") for v in raw)
            if len(set(vertices)) != len(vertices):
                raise ValueError("simplex vertices must be distinct")
            add_faces(tuple(sorted(vertices)))
        self.simplices_by_dim: dict[int, list[tuple[int, ...]]] = {}
        max_dim = max((len(s) - 1 for s in closure), default=-1)
        for degree in range(max_dim + 1):
            self.simplices_by_dim[degree] = sorted(s for s in closure if len(s) == degree + 1)

    @property
    def max_dimension(self) -> int:
        return max(self.simplices_by_dim, default=-1)

    def get_simplices(self, dim: int) -> list[tuple[int, ...]]:
        return list(self.simplices_by_dim.get(integer(dim, "dim"), []))

    def num_simplices(self, dim: int) -> int:
        return len(self.get_simplices(dim))


def simplicial_boundary_matrix(complex_: SimplicialComplex, dim: int) -> np.ndarray:
    """Integer oriented incidence: partial_p: C_p -> C_(p-1)."""
    degree = integer(dim, "dim")
    if degree == 0:
        return np.zeros((0, complex_.num_simplices(0)), dtype=int)
    columns = complex_.get_simplices(degree)
    rows = complex_.get_simplices(degree - 1)
    index = {s: i for i, s in enumerate(rows)}
    result = np.zeros((len(rows), len(columns)), dtype=int)
    for col, simplex in enumerate(columns):
        for i in range(len(simplex)):
            result[index[simplex[:i] + simplex[i + 1 :]], col] = (-1) ** i
    return result


def simplicial_coboundary_matrix(complex_: SimplicialComplex, dim: int) -> np.ndarray:
    """d_p = partial_(p+1)^T for Euclidean scalar coefficients."""
    return simplicial_boundary_matrix(complex_, integer(dim, "dim") + 1).T


def simplicial_laplacian(complex_: SimplicialComplex, dim: int) -> np.ndarray:
    """Delta_p = partial_p^T partial_p + partial_(p+1) partial_(p+1)^T."""
    degree = integer(dim, "dim")
    down = simplicial_boundary_matrix(complex_, degree)
    up = simplicial_boundary_matrix(complex_, degree + 1)
    return down.T @ down + up @ up.T


def hodge_decomposition(
    cochain: np.ndarray,
    complex_: SimplicialComplex,
    dim: int,
    tol: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Numerical orthogonal components (exact, coexact, harmonic).

    Components are unique; potentials need not be. tol is the relative SVD
    cutoff for the image projections, not a physical entanglement threshold.
    Complex scalar coefficients are supported.
    """
    degree = integer(dim, "dim")
    tol = nonnegative(tol, "tol")
    if not 0 < tol < 1:
        raise ValueError("tol must lie strictly between 0 and 1")
    omega = np.asarray(cochain, dtype=complex)
    count = complex_.num_simplices(degree)
    if omega.shape != (count,) or not np.isfinite(omega).all():
        raise ValueError("cochain must be a finite vector matching the declared degree")

    def image_projection(a: np.ndarray) -> np.ndarray:
        if not a.shape[0] or not a.shape[1]:
            return np.zeros_like(omega)
        potential = np.linalg.lstsq(a, omega, rcond=tol)[0]
        return a @ potential

    exact = image_projection(simplicial_boundary_matrix(complex_, degree).T)
    coexact = image_projection(simplicial_boundary_matrix(complex_, degree + 1))
    return exact, coexact, omega - exact - coexact
