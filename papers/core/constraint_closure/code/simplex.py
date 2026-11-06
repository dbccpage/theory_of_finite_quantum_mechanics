"""Simplex geometric primitives and Cayley-Menger calculations for Regge calculus.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Dict, List, Optional, Sequence, Tuple
import numpy as np


@dataclass(frozen=True)
class Simplex:
    """A k-simplex represented by an ordered tuple of vertex identifiers."""

    dimension: int
    vertices: Tuple[Any, ...]

    def __post_init__(self) -> None:
        if len(self.vertices) != self.dimension + 1:
            raise ValueError(
                f"Simplex of dimension {self.dimension} must have {self.dimension + 1} vertices, "
                f"got {len(self.vertices)}"
            )

    @property
    def faces(self) -> List[Simplex]:
        """Return all (k-1)-faces with alternating orientation."""
        if self.dimension == 0:
            return []
        sub_faces = []
        for i in range(len(self.vertices)):
            face_verts = self.vertices[:i] + self.vertices[i + 1 :]
            sub_faces.append(Simplex(dimension=self.dimension - 1, vertices=face_verts))
        return sub_faces


def cayley_menger_volume_sq(squared_distances: np.ndarray) -> float:
    """Compute squared volume of a d-simplex via the Cayley-Menger determinant.

    squared_distances is a (d+1) x (d+1) symmetric matrix where entry (i, j) is s_{ij} = d(v_i, v_j)^2.
    Formula:
        V^2 = (-1)^{d+1} / (2^d (d!)^2) * det(CM)
    where CM is the bordered matrix with top row / left column [0, 1, 1, ..., 1].
    """
    n = squared_distances.shape[0]
    dim = n - 1
    if dim < 1:
        return 0.0

    cm = np.zeros((n + 1, n + 1), dtype=float)
    cm[0, 1:] = 1.0
    cm[1:, 0] = 1.0
    cm[1:, 1:] = squared_distances

    det = np.linalg.det(cm)
    coeff = ((-1) ** (dim + 1)) / ((2.0 ** dim) * (math.factorial(dim) ** 2))
    val = coeff * det
    if val < -1e-12:
        raise ValueError(
            f"Invalid simplex geometry: Cayley-Menger squared volume is negative ({float(val):.6e}), "
            "violating metric embedding constraints."
        )
    return max(0.0, float(val))


def simplex_volume(squared_distances: np.ndarray) -> float:
    """Compute volume of a d-simplex from edge squared lengths."""
    return math.sqrt(cayley_menger_volume_sq(squared_distances))


def regular_simplex_dihedral_angle(dimension: int) -> float:
    """Dihedral angle of a regular d-simplex at a codimension-2 hinge.

    Formula: theta_d = arccos(1 / d)
    For d=2: angle at vertex = pi/3 (here cos = 1/2).
    For d=3: dihedral angle along edge = arccos(1/3) ~ 1.230959 rad.
    For d=4: dihedral angle along triangle = arccos(1/4) ~ 1.318116 rad.
    """
    if dimension < 1:
        raise ValueError("Dimension must be >= 1")
    return math.acos(1.0 / float(dimension))


def tetrahedron_dihedral_angle(
    s: Dict[Tuple[int, int], float],
    hinge_edge: Tuple[int, int],
) -> float:
    """Compute dihedral angle along hinge_edge in a tetrahedron using squared edge lengths.

    Let tetrahedron vertices be (0, 1, 2, 3) and hinge_edge be (0, 1).
    The two faces meeting at (0, 1) are (0, 1, 2) and (0, 1, 3).
    The dihedral angle theta_{01} satisfies:
        cos theta_{01} = (N_{012} . N_{013}) / (|N_{012}| |N_{013}|)
    computed via derivatives of Cayley-Menger or the triangle cross-products.
    """
    u, v = hinge_edge
    remaining = [i for i in range(4) if i not in (u, v)]
    if len(remaining) != 2:
        raise ValueError(f"Hinge edge {hinge_edge} must leave exactly 2 vertices in tetrahedron")
    w1, w2 = remaining

    def sq(i: int, j: int) -> float:
        key = (min(i, j), max(i, j))
        if key not in s:
            raise KeyError(f"Missing edge {key} in squared length dictionary")
        return s[key]

    def face_area_sq(a: int, b: int, c: int) -> float:
        d_mat = np.array([
            [0.0, sq(a, b), sq(a, c)],
            [sq(a, b), 0.0, sq(b, c)],
            [sq(a, c), sq(b, c), 0.0]
        ])
        return cayley_menger_volume_sq(d_mat)

    try:
        A1_sq = face_area_sq(u, v, w1)
        A2_sq = face_area_sq(u, v, w2)
    except ValueError as err:
        raise ValueError(
            f"Cannot compute tetrahedron dihedral angle: geometry is degenerate, unrealizable in R^3, "
            f"or violates metric embedding constraints ({err})."
        ) from err

    if A1_sq <= 1e-15 or A2_sq <= 1e-15:
        return 0.0

    full_mat = np.zeros((4, 4), dtype=float)
    for i in range(4):
        for j in range(4):
            if i != j:
                full_mat[i, j] = sq(i, j)
    try:
        vol_sq = cayley_menger_volume_sq(full_mat)
    except ValueError as err:
        raise ValueError(
            f"Cannot compute tetrahedron dihedral angle: geometry is degenerate, unrealizable in R^3, "
            f"or violates metric embedding constraints ({err})."
        ) from err

    coords = reconstruct_simplex_coordinates(full_mat, dim=3)
    if coords is not None:
        p0, p1 = coords[u], coords[v]
        pw1, pw2 = coords[w1], coords[w2]
        edge = p1 - p0
        edge_len = np.linalg.norm(edge)
        if edge_len < 1e-12:
            return 0.0
        e_hat = edge / edge_len

        n1 = np.cross(p1 - p0, pw1 - p0)
        n1_proj = n1 - np.dot(n1, e_hat) * e_hat
        n1_norm = np.linalg.norm(n1_proj)

        n2 = np.cross(p1 - p0, pw2 - p0)
        n2_proj = n2 - np.dot(n2, e_hat) * e_hat
        n2_norm = np.linalg.norm(n2_proj)

        if n1_norm < 1e-12 or n2_norm < 1e-12:
            return 0.0

        cos_theta = np.clip(np.dot(n1_proj, n2_proj) / (n1_norm * n2_norm), -1.0, 1.0)
        return float(math.acos(cos_theta))

    edge_vals = list(s.values())
    if len(edge_vals) == 6 and np.allclose(edge_vals, edge_vals[0], atol=1e-12) and edge_vals[0] > 0:
        return regular_simplex_dihedral_angle(3)

    raise ValueError(
        "Cannot compute tetrahedron dihedral angle: geometry is degenerate, unrealizable in R^3, "
        "or violates metric embedding constraints."
    )


def compute_simplex_dihedral_angles(
    vertices: Sequence[int],
    edge_lengths: Dict[Tuple[int, int], float],
    dim: int,
) -> Dict[Tuple[int, ...], float]:
    """Compute all dihedral angles at codimension-2 hinges in a d-simplex using Gram matrix inversion.

    vertices: tuple/list of d+1 vertex identifiers.
    edge_lengths: mapping (min(u, v), max(u, v)) -> length > 0.
    dim: simplex dimension d (e.g. 3 for tetrahedron, 4 for 4-simplex).
    Returns dict mapping canonical hinge tuple (of length d-1) to dihedral angle theta in radians.
    """
    n = dim + 1
    if len(vertices) != n:
        raise ValueError(f"Simplex of dimension {dim} must have {n} vertices, got {len(vertices)}")

    for k, length in edge_lengths.items():
        if not (isinstance(length, (int, float)) and math.isfinite(length) and length > 0):
            raise ValueError(f"Edge length for {k} must be positive and finite, got {length}")

    max_len = max(float(l) for l in edge_lengths.values())
    if max_len <= 0 or not math.isfinite(max_len):
        raise ValueError("Simplex must have positive finite maximum edge length")

    v0 = vertices[0]
    other_verts = list(vertices[1:])
    G = np.zeros((dim, dim), dtype=float)
    for i in range(dim):
        for j in range(dim):
            vi = other_verts[i]
            vj = other_verts[j]
            e0i = tuple(sorted((v0, vi)))
            e0j = tuple(sorted((v0, vj)))
            eij = tuple(sorted((vi, vj)))
            if e0i not in edge_lengths or e0j not in edge_lengths:
                raise KeyError(f"Missing edge lengths for vertex {v0}")
            if vi != vj and eij not in edge_lengths:
                raise KeyError(f"Missing edge length for ({vi}, {vj})")
            s0i = (float(edge_lengths[e0i]) / max_len) ** 2
            s0j = (float(edge_lengths[e0j]) / max_len) ** 2
            sij = 0.0 if vi == vj else (float(edge_lengths[eij]) / max_len) ** 2
            G[i, j] = 0.5 * (s0i + s0j - sij)

    eigvals_G = np.linalg.eigvalsh(G)
    if np.any(eigvals_G <= 1e-12):
        raise ValueError(
            f"Simplex Gram matrix is singular or non-positive definite (min eigenvalue {float(np.min(eigvals_G))}). "
            "Geometry is degenerate or unrealizable in Euclidean space."
        )

    G_inv = np.linalg.inv(G)
    normals_cov = np.zeros((n, n), dtype=float)
    normals_cov[1:, 1:] = G_inv
    for i in range(1, n):
        val = -float(np.sum(G_inv[i - 1, :]))
        normals_cov[0, i] = val
        normals_cov[i, 0] = val
    normals_cov[0, 0] = float(np.sum(G_inv))

    dihedrals: Dict[Tuple[int, ...], float] = {}
    for i in range(n):
        for j in range(i + 1, n):
            hinge = tuple(sorted([vertices[k] for k in range(n) if k != i and k != j]))
            denom = math.sqrt(normals_cov[i, i] * normals_cov[j, j])
            if denom < 1e-14:
                raise ValueError(
                    f"Degenerate simplex face normal encountered for hinge {hinge} (denominator {denom:.2e}). "
                    "Cannot compute interior dihedral angle."
                )
            cos_n = np.clip(normals_cov[i, j] / denom, -1.0, 1.0)
            theta = math.acos(-cos_n)
            dihedrals[hinge] = float(theta)

    return dihedrals


def four_simplex_dihedral_angle(
    regular: bool = True,
    vertices: Optional[Sequence[int]] = None,
    edge_lengths: Optional[Dict[Tuple[int, int], float]] = None,
    hinge: Optional[Tuple[int, int, int]] = None,
) -> float:
    """Dihedral angle at a triangular hinge in a 4-simplex.

    For a regular 4-simplex: returns arccos(1/4).
    For a general irregular 4-simplex: note that irregular 4-simplices require full Gram matrix
    inversion via compute_simplex_dihedral_angles(dim=4). If edge_lengths is None, raises NotImplementedError.
    """
    if regular:
        return regular_simplex_dihedral_angle(4)
    if edge_lengths is None:
        raise NotImplementedError("General irregular 4-simplex dihedral requires edge_lengths for Gram matrix inversion")

    if vertices is None:
        vertices = tuple(range(5))
    dihedrals = compute_simplex_dihedral_angles(vertices, edge_lengths, dim=4)
    if hinge is not None:
        can_hinge = tuple(sorted(hinge))
        return dihedrals[can_hinge]
    return next(iter(dihedrals.values()))


def compute_hinge_deficit_angle(
    dihedral_angles: Sequence[float],
    hinge_is_boundary: bool = False,
) -> float:
    """Compute Regge curvature deficit angle at a codimension-2 hinge.

    For an interior hinge:
        epsilon_h = 2*pi - sum(theta_h)
    For a boundary hinge:
        epsilon_h = pi - sum(theta_h)
    """
    total_angle = sum(dihedral_angles)
    expected_full = math.pi if hinge_is_boundary else 2.0 * math.pi
    return float(expected_full - total_angle)


def reconstruct_simplex_coordinates(
    squared_distances: np.ndarray,
    dim: int,
) -> Optional[np.ndarray]:
    """Reconstruct vertex coordinates in R^dim from squared distance matrix via multidimensional scaling.

    Verifies that the centered Gram matrix has no negative eigenvalues (< -1e-10 relative to scale),
    that the geometry is realizable in Euclidean R^dim, and that reconstructed
    pairwise squared distances match input distances to within 1e-5 relative error.
    """
    n = squared_distances.shape[0]
    if n != dim + 1:
        return None

    if not np.all(np.isfinite(squared_distances)):
        return None

    max_s = float(np.max(squared_distances))
    if max_s <= 1e-15:
        return np.zeros((n, dim), dtype=float)

    s_norm = squared_distances / max_s
    H = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * H @ s_norm @ H

    eigvals, eigvecs = np.linalg.eigh(B)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    if np.any(eigvals < -1e-10):
        return None

    pos_eigs = np.maximum(0.0, eigvals[:dim])
    coords = eigvecs[:, :dim] * np.sqrt(pos_eigs * max_s)

    diffs = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    recon_sq_dist = np.sum(diffs ** 2, axis=-1)
    max_rel_err = float(np.max(np.abs(recon_sq_dist - squared_distances))) / max_s
    if max_rel_err > 1e-5:
        return None

    return coords
