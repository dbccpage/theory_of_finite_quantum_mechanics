"""Simplicial Bianchi identities and discrete curvature conservation in 3D and 4D.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple
import numpy as np

from simplex import regular_simplex_dihedral_angle, compute_hinge_deficit_angle
from complex import SimplicialComplex


def contracted_bianchi_vertex_flux_3d(
    vertex_idx: int,
    vertex_coords: Dict[int, np.ndarray],
    incident_edges: List[Tuple[int, int]],
    deficit_angles: Dict[Tuple[int, int], float],
) -> np.ndarray:
    """Compute the 3D discrete contracted Bianchi vector at a vertex.

    In 3D Regge calculus, invariance of the action under vertex variation delta x_v
    implies the discrete contracted Bianchi identity:
        V_v = sum_{e = (v, w)} epsilon_e * hat{e}_{vw} = 0
    where hat{e}_{vw} = (x_w - x_v) / ||x_w - x_v|| is the unit vector along edge e.
    """
    x_v = vertex_coords[vertex_idx]
    flux = np.zeros(3, dtype=float)

    for edge in incident_edges:
        u, w = edge
        neighbor = w if u == vertex_idx else u
        x_w = vertex_coords[neighbor]
        diff = x_w - x_v
        dist = np.linalg.norm(diff)
        if dist < 1e-14:
            raise ValueError(f"Undefined edge direction between coincident vertices {vertex_idx} and {neighbor}")
        e_hat = diff / dist
        can_edge = tuple(sorted(edge))
        eps = deficit_angles.get(can_edge, 0.0)
        flux += eps * e_hat

    return flux


def simplicial_bianchi_boundary_flux(
    complex_: SimplicialComplex,
    deficit_cochain: np.ndarray,
    hinge_dim: int,
) -> float:
    """Evaluate dual curvature boundary flux sum_{h in dK} star epsilon_h over a simplicial complex.

    Note on Mathematical Scope:
    For a general curved 4D simplicial manifold, the exact Bianchi identity is formulated in terms of
    non-abelian SO(4) holonomies around 3-cells (Hamber & Kagel 2001). Because the logarithm of a product
    of non-commuting matrices does not equal the sum of their logarithms, projecting to a scalar deficit
    cochain epsilon does NOT satisfy d_2 epsilon = 0 on generic non-uniform curved geometries.
    The scalar cochain satisfies d_2 epsilon = 0 on:
      (a) Uniform/symmetric complexes where deficits are equal across all hinges (e.g., regular boundary complexes),
      (b) Abelian or linearized gauge models (F = dA), or
      (c) Topological coboundary test fixtures.
    """
    b_next = complex_.boundary_matrix(hinge_dim + 1)
    if b_next.shape[1] == 0:
        return 0.0
    fluxes = b_next.T @ deficit_cochain
    return float(np.linalg.norm(fluxes, ord=1))


def verify_contracted_bianchi_3d(
    vertex_coords: Dict[int, np.ndarray],
    edges: List[Tuple[int, int]],
    deficit_angles: Dict[Tuple[int, int], float],
    interior_vertices: Optional[Sequence[int]] = None,
    tol: float = 1e-10,
) -> Dict[str, Any]:
    """Verify that contracted Bianchi flux vanishes at declared interior vertices."""
    vertex_fluxes: Dict[int, float] = {}
    max_flux = 0.0

    target_vertices = list(vertex_coords.keys()) if interior_vertices is None else list(interior_vertices)

    has_nonfinite = False
    for v in target_vertices:
        incident = [e for e in edges if v in e]
        try:
            flux_vec = contracted_bianchi_vertex_flux_3d(v, vertex_coords, incident, deficit_angles)
            if np.any(np.isnan(flux_vec)) or np.any(np.isinf(flux_vec)):
                has_nonfinite = True
                norm_val = float("nan")
            else:
                norm_val = float(np.linalg.norm(flux_vec))
        except (ValueError, KeyError):
            has_nonfinite = True
            norm_val = float("nan")

        vertex_fluxes[v] = norm_val
        if np.isnan(norm_val) or norm_val > max_flux:
            max_flux = norm_val

    is_satisfied = (not has_nonfinite) and (not np.isnan(max_flux)) and (max_flux < tol)
    return {
        "is_satisfied": is_satisfied,
        "max_flux": max_flux,
        "has_nonfinite": has_nonfinite,
        "tolerance": tol,
        "vertex_fluxes": vertex_fluxes,
        "authority_effect": "None",
    }


def verify_closed_bianchi_flux(
    complex_: SimplicialComplex,
    deficit_cochain: np.ndarray,
    hinge_dim: int = 1,
    tol: float = 1e-10,
) -> Dict[str, Any]:
    """Evaluate discrete scalar Bianchi cochain-closure diagnostic on a simplicial complex.

    Computes ||d_{hinge_dim} epsilon||_1.
    Note: On generic curved 4-manifolds, non-abelian holonomy effects mean the scalar
    curvature deficit cochain does NOT generally satisfy d_2 epsilon = 0 (Hamber & Kagel 2001).
    Scalar cochain closure holds on uniform/symmetric complexes and abelian models.
    """
    total_l1_flux = simplicial_bianchi_boundary_flux(complex_, deficit_cochain, hinge_dim)
    if np.isnan(total_l1_flux) or np.isinf(total_l1_flux):
        is_satisfied = False
    else:
        is_satisfied = total_l1_flux < tol
    return {
        "is_satisfied": is_satisfied,
        "total_l1_flux": total_l1_flux,
        "tolerance": tol,
        "hinge_dimension": hinge_dim,
        "authority_effect": "None",
    }
