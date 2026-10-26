"""Galois lattice of transformation monoids and invariant convex bodies for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

from enum import Enum
from typing import Callable, List
import numpy as np

Gauge = Callable[[np.ndarray], float]


class MonoidClass(str, Enum):
    """Hierarchy of transformation submonoids of End_b(V)."""

    TRIVIAL = "trivial"  # {I}
    PERMUTATION = "permutation"  # S_n
    SIGNED_PERMUTATION = "signed_permutation"  # Z_2^n rtimes S_n (hyperoctahedral)
    POSITIVE_DIAGONAL = "positive_diagonal"  # Diag(a_i), 0 <= a_i <= 1
    DIAGONAL_CONTRACTION = "diagonal_contraction"  # Diag(a_i), |a_i| <= 1
    ORTHOGONAL = "orthogonal"  # SO(n) or O(n)
    FULL_LINEAR = "full_linear"  # End_b(V) (Maximal symmetry)


def sample_monoid_generators(monoid: MonoidClass, dimension: int) -> List[np.ndarray]:
    """Sample representative generators/operators for a declared monoid class."""
    if dimension < 2:
        raise ValueError("Dimension must be at least 2")

    generators: List[np.ndarray] = [np.eye(dimension)]

    if monoid == MonoidClass.TRIVIAL:
        return generators

    if monoid in (MonoidClass.PERMUTATION, MonoidClass.SIGNED_PERMUTATION):
        # Transposition (0, 1)
        p = np.eye(dimension)
        p[[0, 1]] = p[[1, 0]]
        generators.append(p)
        # Cyclic shift (0, 1, ..., n-1)
        shift = np.roll(np.eye(dimension), 1, axis=1)
        generators.append(shift)

    if monoid == MonoidClass.SIGNED_PERMUTATION:
        # Sign flip on coordinate 0
        s0 = np.eye(dimension)
        s0[0, 0] = -1.0
        generators.append(s0)

    if monoid in (MonoidClass.POSITIVE_DIAGONAL, MonoidClass.DIAGONAL_CONTRACTION):
        generators.append(np.diag([0.5] + [1.0] * (dimension - 1)))
        generators.append(np.diag([0.0] + [1.0] * (dimension - 1)))

    if monoid == MonoidClass.DIAGONAL_CONTRACTION:
        generators.append(np.diag([-0.5] + [1.0] * (dimension - 1)))
        generators.append(np.diag([-1.0] + [1.0] * (dimension - 1)))

    if monoid in (MonoidClass.ORTHOGONAL, MonoidClass.FULL_LINEAR):
        # 2D Givens rotation in plane (0, 1)
        theta = np.pi / 4.0
        rot = np.eye(dimension)
        rot[0, 0] = np.cos(theta)
        rot[0, 1] = -np.sin(theta)
        rot[1, 0] = np.sin(theta)
        rot[1, 1] = np.cos(theta)
        generators.append(rot)

    if monoid == MonoidClass.FULL_LINEAR:
        # Rank-one projection onto e_0
        p0 = np.zeros((dimension, dimension))
        p0[0, 0] = 1.0
        generators.append(p0)
        # Shear matrix
        shear = np.eye(dimension)
        shear[0, 1] = 0.5
        generators.append(shear)

    return generators


def check_bidirectional_reachability(
    u: np.ndarray, v: np.ndarray, monoid: MonoidClass, ambient_norm: str = "l2"
) -> bool:
    """Check whether monoid contains contractions T, S with T u = v and S v = u.

    For FULL_LINEAR: always true for any equal-norm vectors via Hahn-Banach rank-one operators.
    For ORTHOGONAL: true if and only if ||u||_2 == ||v||_2.
    For SIGNED_PERMUTATION: true if and only if |u| is a permutation of |v|.
    For TRIVIAL: true if and only if u == v.
    """
    u_arr = np.asarray(u, dtype=float).ravel()
    v_arr = np.asarray(v, dtype=float).ravel()

    if u_arr.shape != v_arr.shape:
        return False

    if monoid == MonoidClass.FULL_LINEAR:
        # End_b(V) has rank-one operators connecting any pair of equal-norm vectors
        from norms import l1, l2, linf

        norm_map = {"l1": l1, "l2": l2, "linf": linf}
        fn = norm_map.get(ambient_norm.lower(), l2)
        return bool(abs(fn(u_arr) - fn(v_arr)) < 1e-7)

    elif monoid == MonoidClass.ORTHOGONAL:
        return bool(abs(np.linalg.norm(u_arr, 2) - np.linalg.norm(v_arr, 2)) < 1e-7)

    elif monoid == MonoidClass.SIGNED_PERMUTATION:
        u_sorted = np.sort(np.abs(u_arr))
        v_sorted = np.sort(np.abs(v_arr))
        return bool(np.allclose(u_sorted, v_sorted, atol=1e-7))

    elif monoid == MonoidClass.PERMUTATION:
        u_sorted = np.sort(u_arr)
        v_sorted = np.sort(v_arr)
        return bool(np.allclose(u_sorted, v_sorted, atol=1e-7))

    elif monoid == MonoidClass.TRIVIAL:
        return bool(np.allclose(u_arr, v_arr, atol=1e-7))

    return False


def monoid_containment_lattice() -> dict[MonoidClass, list[MonoidClass]]:
    """Return the immediate cover relations in the submonoid lattice.

    Parent -> List[immediate submonoids].
    """
    return {
        MonoidClass.FULL_LINEAR: [
            MonoidClass.ORTHOGONAL,
            MonoidClass.DIAGONAL_CONTRACTION,
        ],
        MonoidClass.ORTHOGONAL: [MonoidClass.SIGNED_PERMUTATION],
        MonoidClass.DIAGONAL_CONTRACTION: [
            MonoidClass.POSITIVE_DIAGONAL,
            MonoidClass.SIGNED_PERMUTATION,
        ],
        MonoidClass.POSITIVE_DIAGONAL: [MonoidClass.TRIVIAL],
        MonoidClass.SIGNED_PERMUTATION: [MonoidClass.PERMUTATION],
        MonoidClass.PERMUTATION: [MonoidClass.TRIVIAL],
        MonoidClass.TRIVIAL: [],
    }
