"""Higher-Simplex Assembly & Orientation-Consistent Boundary Engine.

Provides degree-generic simplex complex construction, skeleton-filtered higher cell detection,
orientation-consistent boundary matrix assembly d_k: C^k -> C^{k-1}, and d_k o d_{k+1} = 0 nilpotency verification.

AuthorityEffect: None.
"""

from __future__ import annotations
import itertools
from dataclasses import field
from dataclasses import dataclass
from typing import Any, Dict, List, Set, Tuple, Optional
import numpy as np


@dataclass
class SimplexComplex:
    """Finite simplicial complex indexed by dimension k."""

    vertices: List[Any]
    cells: Dict[int, List[Tuple[Any, ...]]] = field(default_factory=dict)
    max_dim: int = 0


def combinatorial_simplices(vertices: List[Any], dim: int) -> List[Tuple[Any, ...]]:
    """Generate all (dim + 1)-element combinations from vertices with canonical ordering."""
    sorted_verts = sorted(vertices)
    return [tuple(c) for c in itertools.combinations(sorted_verts, dim + 1)]


def filter_simplices_by_skeleton(
    candidates: List[Tuple[Any, ...]],
    existing_lower_cells: Set[Tuple[Any, ...]],
) -> List[Tuple[Any, ...]]:
    """Keep only candidate k-simplices whose every (k-1)-face is present in existing_lower_cells."""
    valid_cells = []
    for cell in candidates:
        all_faces_present = True
        # A k-simplex has (k+1) faces obtained by omitting vertex i
        for i in range(len(cell)):
            face = cell[:i] + cell[i + 1 :]
            if face not in existing_lower_cells:
                all_faces_present = False
                break
        if all_faces_present:
            valid_cells.append(cell)
    return valid_cells


def detect_simplices(
    vertices: List[Any],
    existing_lower_cells: Set[Tuple[Any, ...]],
    dim: int,
) -> List[Tuple[Any, ...]]:
    """Discover all valid dim-simplices whose boundary skeleton exists."""
    candidates = combinatorial_simplices(vertices, dim)
    return filter_simplices_by_skeleton(candidates, existing_lower_cells)


def boundary_sum(cell: Tuple[Any, ...], lower_cochain_values: Dict[Tuple[Any, ...], float]) -> float:
    """Evaluate boundary alternating face cochain sum d C = sum_{i=0}^k (-1)^i val(face_i)."""
    total = 0.0
    for i in range(len(cell)):
        face = cell[:i] + cell[i + 1 :]
        sign = (-1) ** i
        val = lower_cochain_values.get(face, 0.0)
        total += sign * val
    return total


def boundary_matrix(
    simplices_k: List[Tuple[Any, ...]],
    simplices_km1: List[Tuple[Any, ...]],
) -> np.ndarray:
    """Assemble exact orientation-consistent boundary matrix d_k of shape (|simplices_{k-1}|, |simplices_k|)."""
    num_km1 = len(simplices_km1)
    num_k = len(simplices_k)
    if num_km1 == 0 or num_k == 0:
        return np.zeros((num_km1, num_k), dtype=float)

    face_index_map = {f: idx for idx, f in enumerate(simplices_km1)}
    mat = np.zeros((num_km1, num_k), dtype=float)

    for col_j, cell in enumerate(simplices_k):
        for i in range(len(cell)):
            face = cell[:i] + cell[i + 1 :]
            sign = (-1) ** i
            if face in face_index_map:
                row_i = face_index_map[face]
                mat[row_i, col_j] += sign

    return mat


def verify_nilpotency(d_km1: np.ndarray, d_k: np.ndarray, atol: float = 1e-12) -> bool:
    """Check that d_{k-1} o d_k = 0 holds exact/numerically within tolerance."""
    if d_km1.size == 0 or d_k.size == 0:
        return True
    if d_km1.shape[1] != d_k.shape[0]:
        return False
    prod = d_km1 @ d_k
    return bool(np.all(np.abs(prod) <= atol))


def assemble_from_network(network: Any, max_dim: int = 4) -> SimplexComplex:
    """Build a SimplexComplex from a Network, discovering cells up to max_dim via skeleton filtering."""
    nodes = sorted(list(network.nodes))
    complex_obj = SimplexComplex(vertices=nodes, max_dim=max_dim)

    # 0-cells
    complex_obj.cells[0] = [(v,) for v in nodes]

    # 1-cells (edges normalized to (u, v) with u < v)
    edges = set()
    for u, v in network.edges:
        edges.add((min(u, v), max(u, v)))
    complex_obj.cells[1] = sorted(list(edges))

    # 2-cells (faces)
    faces = set()
    if hasattr(network, "faces") and network.faces:
        for f in network.faces:
            faces.add(tuple(sorted(f)))
    else:
        # Detect triangles from edges
        triangles = detect_simplices(nodes, edges, dim=2)
        faces.update(triangles)
    complex_obj.cells[2] = sorted(list(faces))

    # Higher k-cells for k >= 3
    lower_set = set(complex_obj.cells[2])
    for k in range(3, max_dim + 1):
        higher_cells = detect_simplices(nodes, lower_set, dim=k)
        if not higher_cells:
            break
        complex_obj.cells[k] = higher_cells
        lower_set = set(higher_cells)

    return complex_obj


def boundary_operators(complex_obj: SimplexComplex) -> Dict[int, np.ndarray]:
    """Generate all boundary matrices d_k for k = 1..max_dim."""
    operators = {}
    for k in range(1, complex_obj.max_dim + 1):
        cells_k = complex_obj.cells.get(k, [])
        cells_km1 = complex_obj.cells.get(k - 1, [])
        operators[k] = boundary_matrix(cells_k, cells_km1)
    return operators


def rational_boundary_matrix(
    simplices_k: List[Tuple[Any, ...]],
    simplices_km1: List[Tuple[Any, ...]],
) -> Any:
    """Assemble exact rational SymPy boundary matrix d_k of shape (|simplices_{k-1}|, |simplices_k|)."""
    from sympy import Matrix

    num_km1 = len(simplices_km1)
    num_k = len(simplices_k)
    if num_km1 == 0 or num_k == 0:
        return Matrix.zeros(num_km1, num_k)

    face_index_map = {f: idx for idx, f in enumerate(simplices_km1)}
    mat = Matrix.zeros(num_km1, num_k)

    for col_j, cell in enumerate(simplices_k):
        for i in range(len(cell)):
            face = cell[:i] + cell[i + 1 :]
            sign = (-1) ** i
            if face in face_index_map:
                row_i = face_index_map[face]
                mat[row_i, col_j] += sign

    return mat


def exact_quotient_l1_distance(
    complex_obj: SimplexComplex,
    dim: int,
    cochain_raw: Any,
) -> Any:
    """Bridge simplicial boundary matrix with LinearRepairProblem to compute exact rational Phi_k certificate."""
    from omega_engine.crates.homology_theory.cochain_presentation import LinearRepairProblem
    from sympy import Matrix

    cells_k = complex_obj.cells.get(dim, [])
    cells_km1 = complex_obj.cells.get(dim - 1, [])

    # Boundary matrix d_k: C^k -> C^{k-1} transpose is coboundary d_{k-1}^\top: C^{k-1} -> C^k
    d_k_mat = rational_boundary_matrix(cells_k, cells_km1)
    coboundary_mat = d_k_mat.T  # shape (n_k, n_km1)

    problem = LinearRepairProblem(coboundary_mat)
    cochain_mat = Matrix(cochain_raw)
    return problem.quotient_l1_distance(cochain_mat)


def nilpotency_report(complex_obj: SimplexComplex) -> Dict[str, Any]:
    """Generate a certificate-style report checking d_k o d_{k+1} = 0 for all consecutive pairs."""
    ops = boundary_operators(complex_obj)
    results = {}
    all_nilpotent = True

    for k in sorted(ops.keys()):
        if k + 1 in ops:
            d_k = ops[k]
            d_kp1 = ops[k + 1]
            is_nil = verify_nilpotency(d_k, d_kp1)
            results[f"d_{k}_circ_d_{k+1}"] = {
                "is_nilpotent": is_nil,
                "d_k_shape": d_k.shape,
                "d_kp1_shape": d_kp1.shape,
            }
            if not is_nil:
                all_nilpotent = False

    return {
        "all_nilpotent": all_nilpotent,
        "max_dim_assembled": max(complex_obj.cells.keys()) if complex_obj.cells else 0,
        "cell_counts": {dim: len(c) for dim, c in complex_obj.cells.items()},
        "pairs_verified": results,
        "authority_effect": "None",
    }


def discover_higher_cells_for_lift(network: Any, from_degree: int) -> Tuple[List[Tuple[Any, ...]], str]:
    """Lift-compatible entry point returning (cells, lift_kind) for a given degree transition C^k -> C^{k+1}."""
    complex_obj = assemble_from_network(network, max_dim=from_degree + 2)
    target_dim = from_degree + 2  # e.g., for C^1 -> C^2, 3-simplices (tetrahedra, dim 3); for C^2 -> C^3, dim 4
    cells = complex_obj.cells.get(target_dim, [])

    if cells:
        lift_kind = "tetrahedra" if target_dim == 3 else "generic_placeholder"
        return cells, lift_kind
    else:
        return [], "unsupported"






