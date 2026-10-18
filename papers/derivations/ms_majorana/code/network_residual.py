"""Network residual analysis module.

Implements discrete Hodge 1-chain gauge fixing, L1/L2 residual extraction,
and incidence/curl operators over directed graphs with 2-cell faces.

contract_id: urn:omega:math:incidence_matrix:v1.0.0
contract_id: urn:omega:math:boundary_map:v1.0.0
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True, slots=True)
class Network:
    """Directed network topology with optional 2-cell faces and 3-cell tetrahedra.

    contract_id: urn:omega:math:incidence_matrix:v1.0.0

    Accepts both list and tuple inputs; coerces to tuples internally.
    """
    nodes: Tuple[Any, ...]
    edges: Tuple[Tuple[Any, Any], ...]
    faces: Tuple[Tuple[Any, Any, Any], ...] = ()
    tetrahedra: Tuple[Tuple[Any, Any, Any, Any], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "nodes", tuple(self.nodes))
        object.__setattr__(self, "edges", tuple(tuple(e) for e in self.edges))
        if self.faces:
            object.__setattr__(self, "faces", tuple(tuple(f) for f in self.faces))
        if self.tetrahedra:
            object.__setattr__(self, "tetrahedra", tuple(tuple(t) for t in self.tetrahedra))
        node_set = set(self.nodes)
        for u, v in self.edges:
            if u not in node_set or v not in node_set:
                raise ValueError(
                    f"Edge ({u}, {v}) references node(s) not in node set"
                )


def _make_network(
    nodes: List[Any],
    edges: List[Tuple[Any, Any]],
    faces: List[Tuple[Any, Any, Any]] | None = None,
    tetrahedra: List[Tuple[Any, Any, Any, Any]] | None = None,
) -> Network:
    """Construct a Network from list inputs (backward compatibility helper)."""
    return Network(
        nodes=tuple(nodes),
        edges=tuple(edges),
        faces=tuple(faces) if faces else (),
        tetrahedra=tuple(tetrahedra) if tetrahedra else (),
    )


@dataclass(frozen=True, slots=True)
class GaugeFixResult:
    """Result of a gauge-fixing optimization.

    contract_id: urn:omega:math:boundary_map:v1.0.0
    """
    residual_size: float
    residual: Dict[Tuple[Any, Any], float]
    potentials: Dict[Any, float]
    is_pure_gauge: bool

    @property
    def gauge_values(self) -> Dict[Any, float]:
        return self.potentials

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            raise TypeError(f"GaugeFixResult keys must be str, got {type(key).__name__}")
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and hasattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


def build_incidence(network: Network) -> Tuple[np.ndarray, Dict[Any, int]]:
    """Build boundary operator matrix d0 mapping 0-potentials to 1-chain edge differences.

    contract_id: urn:omega:math:incidence_matrix:v1.0.0
    """
    node_idx = {n: i for i, n in enumerate(network.nodes)}
    n_e, n_v = len(network.edges), len(network.nodes)
    d0 = np.zeros((n_e, n_v))
    for e_i, (u, v) in enumerate(network.edges):
        d0[e_i, node_idx[u]] = -1.0
        d0[e_i, node_idx[v]] = 1.0
    return d0, node_idx


def build_face_boundary(network: Network) -> np.ndarray:
    """Build boundary operator matrix d1 mapping 2-cell face coefficients to 1-chain edge values.

    contract_id: urn:omega:math:boundary_map:v1.0.0
    """
    n_e, n_f = len(network.edges), len(network.faces)
    d1 = np.zeros((n_e, n_f))
    edge_idx = {e: i for i, e in enumerate(network.edges)}

    for j, (u, v, w) in enumerate(network.faces):
        for x, y in [(u, v), (v, w), (w, u)]:
            if (x, y) in edge_idx:
                d1[edge_idx[(x, y)], j] += 1.0
            elif (y, x) in edge_idx:
                d1[edge_idx[(y, x)], j] -= 1.0
    return d1


def _face_in_faces(u: Any, v: Any, w: Any, face_set: set) -> bool:
    """Check if any cyclic or anti-cyclic orientation of (u,v,w) is in face_set."""
    for f in [(u, v, w), (v, w, u), (w, u, v), (u, w, v), (w, v, u), (v, u, w)]:
        if f in face_set:
            return True
    return False


def detect_tetrahedra(network: Network) -> List[Tuple[Any, Any, Any, Any]]:
    """Detect or construct 3-cell tetrahedra (u,v,w,x) from network topology."""
    if network.tetrahedra:
        return list(network.tetrahedra)

    if not network.faces or len(network.nodes) < 4:
        return []

    face_set = set(network.faces)
    nodes_sorted = sorted(network.nodes, key=lambda n: str(n))

    tetrahedra = []
    for u, v, w, x in itertools.combinations(nodes_sorted, 4):
        if (
            _face_in_faces(v, w, x, face_set)
            and _face_in_faces(u, w, x, face_set)
            and _face_in_faces(u, v, x, face_set)
            and _face_in_faces(u, v, w, face_set)
        ):
            tetrahedra.append((u, v, w, x))

    return tetrahedra


def build_tetrahedron_boundary(
    network: Network,
) -> Tuple[np.ndarray, List[Tuple[Any, Any, Any, Any]]]:
    """Build boundary operator matrix d2 mapping 3-cell tetrahedra to 2-cell faces.

    contract_id: urn:omega:math:boundary_map:v1.0.0
    """
    tetrahedra = detect_tetrahedra(network)
    n_f, n_t = len(network.faces), len(tetrahedra)
    d2 = np.zeros((n_f, n_t))
    if n_f == 0 or n_t == 0:
        return d2, tetrahedra

    face_idx = {f: i for i, f in enumerate(network.faces)}

    def find_face_entry(fu: Any, fv: Any, fw: Any) -> Tuple[int, float]:
        for f in [(fu, fv, fw), (fv, fw, fu), (fw, fu, fv)]:
            if f in face_idx:
                return face_idx[f], 1.0
        for f in [(fu, fw, fv), (fw, fv, fu), (fv, fu, fw)]:
            if f in face_idx:
                return face_idx[f], -1.0
        return -1, 0.0

    for k, (u, v, w, x) in enumerate(tetrahedra):
        face_specs = [(1.0, v, w, x), (-1.0, u, w, x), (1.0, u, v, x), (-1.0, u, v, w)]
        for coef, fu, fv, fw in face_specs:
            idx, s = find_face_entry(fu, fv, fw)
            if idx >= 0:
                d2[idx, k] += coef * s

    return d2, tetrahedra


def residual_c2_after_gauge_fix(
    network: Network,
    face_values: Dict[Tuple[Any, Any, Any], float],
) -> GaugeFixResult:
    """Extract 1-cochain potential beta minimizing ||c2 - d1^T @ beta|| under L1 norm."""
    if not network.faces:
        return GaugeFixResult(
            residual_size=0.0,
            residual={},
            potentials={},
            is_pure_gauge=True,
        )

    d1 = build_face_boundary(network)
    d1_t = d1.T
    n_e, n_f = d1.shape
    c2 = np.array([face_values.get(f, 0.0) for f in network.faces])

    c = np.concatenate([np.zeros(n_e), np.ones(n_f)])
    eye = np.eye(n_f)
    a_ub = np.vstack([np.hstack([d1_t, -eye]), np.hstack([-d1_t, -eye])])
    b_ub = np.concatenate([c2, -c2])
    bounds = [(None, None)] * n_e + [(0, None)] * n_f

    res = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if res.success:
        beta = res.x[:n_e]
        size = float(res.fun)
        residual_vec = c2 - d1_t @ beta
    else:
        beta = np.zeros(n_e)
        size = float(np.sum(np.abs(c2)))
        residual_vec = c2

    residual = {f: float(residual_vec[j]) for j, f in enumerate(network.faces)}
    pots = {e: float(beta[i]) for i, e in enumerate(network.edges)}
    return GaugeFixResult(
        residual_size=size,
        residual=residual,
        potentials=pots,
        is_pure_gauge=size < 1e-8,
    )


def gradient(network: Network, potentials: Dict[Any, float]) -> Dict[Tuple[Any, Any], float]:
    """Compute exact potential differences along directed edges."""
    return {
        (u, v): potentials.get(v, 0.0) - potentials.get(u, 0.0)
        for u, v in network.edges
    }


def _oriented_lookup(edge_values: Dict[Tuple[Any, Any], float], u: Any, v: Any) -> float:
    """Look up edge value with orientation: try (u,v) first, then -(v,u)."""
    if (u, v) in edge_values:
        return edge_values[(u, v)]
    if (v, u) in edge_values:
        return -edge_values[(v, u)]
    return 0.0


def curl(network: Network, edge_values: Dict[Tuple[Any, Any], float]) -> Dict[Tuple[Any, Any, Any], float]:
    """Compute 2-cell boundary sums around faces (d1 applied to 1-cochains).

    Handles both edge orientations: if (u,v) is absent, looks up -(v,u).
    This ensures d1 o d0 = 0 regardless of edge storage direction.
    """
    result = {}
    for u, v, w in network.faces:
        s = (
            _oriented_lookup(edge_values, u, v)
            + _oriented_lookup(edge_values, v, w)
            + _oriented_lookup(edge_values, w, u)
        )
        result[(u, v, w)] = s
    return result


def _oriented_face_lookup(face_values: Dict[Tuple[Any, Any, Any], float], u: Any, v: Any, w: Any) -> float:
    """Look up 2-cell face value with orientation: cyclic positive, anti-cyclic negative."""
    for f in [(u, v, w), (v, w, u), (w, u, v)]:
        if f in face_values:
            return face_values[f]
    for f in [(u, w, v), (w, v, u), (v, u, w)]:
        if f in face_values:
            return -face_values[f]
    return 0.0


def tetrahedral_boundary_sum(
    tetrahedra: List[Tuple[Any, Any, Any, Any]],
    face_values: Dict[Tuple[Any, Any, Any], float],
) -> Dict[Tuple[Any, Any, Any, Any], float]:
    """Compute 3-cell boundary sums over tetrahedra (d2 applied to 2-cochains).

    For tetrahedron (u,v,w,x), d2 evaluation uses oriented face boundary:
    +(v,w,x) - (u,w,x) + (u,v,x) - (u,v,w).
    Ensures d2 o d1 = 0 nilpotency identically.
    """
    result = {}
    for u, v, w, x in tetrahedra:
        s = (
            _oriented_face_lookup(face_values, v, w, x)
            - _oriented_face_lookup(face_values, u, w, x)
            + _oriented_face_lookup(face_values, u, v, x)
            - _oriented_face_lookup(face_values, u, v, w)
        )
        result[(u, v, w, x)] = s
    return result


def _oriented_tet_lookup(
    tet_values: Dict[Tuple[Any, Any, Any, Any], float],
    u: Any, v: Any, w: Any, x: Any
) -> float:
    """Look up 3-cell tetrahedron value with orientation under 4-element permutations."""
    base = (u, v, w, x)
    for p in itertools.permutations(base):
        if p in tet_values:
            inversions = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
            sign = 1.0 if inversions % 2 == 0 else -1.0
            return sign * tet_values[p]
    return 0.0


def four_simplex_boundary_sum(
    four_simplices: List[Tuple[Any, Any, Any, Any, Any]],
    tet_values: Dict[Tuple[Any, Any, Any, Any], float],
) -> Dict[Tuple[Any, Any, Any, Any, Any], float]:
    """Compute 4-cell boundary sums over 4-simplices (d3 applied to 3-cochains).

    For 4-simplex (u,v,w,x,y), d3 evaluation uses oriented tetrahedron boundary:
    +(v,w,x,y) - (u,w,x,y) + (u,v,x,y) - (u,v,w,y) + (u,v,w,x).
    Ensures d3 o d2 = 0 nilpotency identically.
    """
    result = {}
    for u, v, w, x, y in four_simplices:
        s = (
            _oriented_tet_lookup(tet_values, v, w, x, y)
            - _oriented_tet_lookup(tet_values, u, w, x, y)
            + _oriented_tet_lookup(tet_values, u, v, x, y)
            - _oriented_tet_lookup(tet_values, u, v, w, y)
            + _oriented_tet_lookup(tet_values, u, v, w, x)
        )
        result[(u, v, w, x, y)] = s
    return result


def _oriented_4simplex_lookup(
    four_simp_values: Dict[Tuple[Any, Any, Any, Any, Any], float],
    u: Any, v: Any, w: Any, x: Any, y: Any
) -> float:
    """Look up 4-simplex value with orientation under 5-element permutations."""
    base = (u, v, w, x, y)
    for p in itertools.permutations(base):
        if p in four_simp_values:
            inversions = sum(1 for i in range(5) for j in range(i + 1, 5) if p[i] > p[j])
            sign = 1.0 if inversions % 2 == 0 else -1.0
            return sign * four_simp_values[p]
    return 0.0


def five_simplex_boundary_sum(
    five_simplices: List[Tuple[Any, Any, Any, Any, Any, Any]],
    four_simp_values: Dict[Tuple[Any, Any, Any, Any, Any], float],
) -> Dict[Tuple[Any, Any, Any, Any, Any, Any], float]:
    """Compute 5-cell boundary sums over 5-simplices (d4 applied to 4-cochains).

    For 5-simplex (u,v,w,x,y,z), d4 evaluation uses oriented 4-simplex boundary:
    +(v,w,x,y,z) - (u,w,x,y,z) + (u,v,x,y,z) - (u,v,w,y,z) + (u,v,w,x,z) - (u,v,w,x,y).
    Ensures d4 o d3 = 0 nilpotency identically.
    """
    result = {}
    for u, v, w, x, y, z in five_simplices:
        s = (
            _oriented_4simplex_lookup(four_simp_values, v, w, x, y, z)
            - _oriented_4simplex_lookup(four_simp_values, u, w, x, y, z)
            + _oriented_4simplex_lookup(four_simp_values, u, v, x, y, z)
            - _oriented_4simplex_lookup(four_simp_values, u, v, w, y, z)
            + _oriented_4simplex_lookup(four_simp_values, u, v, w, x, z)
            - _oriented_4simplex_lookup(four_simp_values, u, v, w, x, y)
        )
        result[(u, v, w, x, y, z)] = s
    return result


def _oriented_5simplex_lookup(
    five_simp_values: Dict[Tuple[Any, Any, Any, Any, Any, Any], float],
    v0: Any, v1: Any, v2: Any, v3: Any, v4: Any, v5: Any
) -> float:
    """Look up 5-simplex value with orientation under 6-element permutations."""
    base = (v0, v1, v2, v3, v4, v5)
    for p in itertools.permutations(base):
        if p in five_simp_values:
            inversions = sum(1 for i in range(6) for j in range(i + 1, 6) if p[i] > p[j])
            sign = 1.0 if inversions % 2 == 0 else -1.0
            return sign * five_simp_values[p]
    return 0.0


def six_simplex_boundary_sum(
    six_simplices: List[Tuple[Any, Any, Any, Any, Any, Any, Any]],
    five_simp_values: Dict[Tuple[Any, Any, Any, Any, Any, Any], float],
) -> Dict[Tuple[Any, Any, Any, Any, Any, Any, Any], float]:
    r"""Compute 6-cell boundary sums over 6-simplices (d5 applied to 5-cochains).

    For 6-simplex (v0,v1,v2,v3,v4,v5,v6), d5 evaluation uses oriented 5-simplex boundary:
    sum_{j=0}^6 (-1)^j (v0, ..., \hat{v}_j, ..., v6).
    Ensures d5 o d4 = 0 nilpotency identically.
    """
    result = {}
    for verts in six_simplices:
        s = 0.0
        for j in range(7):
            sub_verts = verts[:j] + verts[j+1:]
            val = _oriented_5simplex_lookup(five_simp_values, *sub_verts)
            sign = 1.0 if j % 2 == 0 else -1.0
            s += sign * val
        result[verts] = s
    return result


def residual_after_gauge_fix(
    network: Network,
    edge_values: Dict[Tuple[Any, Any], float],
    method: str = "l1",
) -> GaugeFixResult:
    """Extract potential field alpha minimizing ||h - d0 @ alpha|| under L1 or L2 norm."""
    if not network.edges:
        return GaugeFixResult(
            residual_size=0.0,
            residual={},
            potentials={},
            is_pure_gauge=True,
        )

    d0, node_idx = build_incidence(network)
    n_v, n_e = len(network.nodes), len(network.edges)
    h = np.array([edge_values.get(e, 0.0) for e in network.edges])

    if method == "l1":
        c = np.concatenate([np.zeros(n_v), np.ones(n_e)])
        eye = np.eye(n_e)
        a_ub = np.vstack([np.hstack([d0, -eye]), np.hstack([-d0, -eye])])
        b_ub = np.concatenate([h, -h])
        bounds = [(None, None)] * n_v + [(0, None)] * n_e
        res = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if res.success:
            alpha = res.x[:n_v]
            size = float(res.fun)
            residual_vec = h - d0 @ alpha
        else:
            alpha = np.zeros(n_v)
            size = float(np.sum(np.abs(h)))
            residual_vec = h
    else:
        alpha, _, _, _ = np.linalg.lstsq(d0, h, rcond=None)
        residual_vec = h - d0 @ alpha
        size = float(np.linalg.norm(residual_vec))

    residual = {e: float(residual_vec[i]) for i, e in enumerate(network.edges)}
    pots = {n: float(alpha[node_idx[n]]) for n in network.nodes}
    return GaugeFixResult(
        residual_size=size,
        residual=residual,
        potentials=pots,
        is_pure_gauge=size < 1e-8,
    )


def multi_cycle_l1_joint(
    network: Network,
    edge_values: Dict[Tuple[Any, Any], float],
) -> Dict[str, Any]:
    """Joint multi-cycle L1 descent minimizing ||h - d0 @ alpha - d1 @ beta||_1.

    Simultaneously extracts potential alpha (exact coboundary) and cycle coefficients beta (coexact curl).
    """
    if not network.edges:
        return {
            "residual_size": 0.0,
            "residual": {},
            "potentials": {},
            "cycle_coeffs": {},
            "is_zero": True,
        }

    d0, node_idx = build_incidence(network)
    d1 = build_face_boundary(network)

    n_v, n_e, n_f = len(network.nodes), len(network.edges), len(network.faces)
    h = np.array([edge_values.get(e, 0.0) for e in network.edges])

    if n_f == 0:
        res = residual_after_gauge_fix(network, edge_values, method="l1")
        return {
            "residual_size": res.residual_size,
            "residual": res.residual,
            "potentials": res.potentials,
            "cycle_coeffs": {},
            "is_zero": res.residual_size < 1e-8,
        }

    c = np.concatenate([np.zeros(n_v + n_f), np.ones(n_e)])
    eye = np.eye(n_e)

    d_joint = np.hstack([d0, d1])
    a_ub = np.vstack([np.hstack([d_joint, -eye]), np.hstack([-d_joint, -eye])])
    b_ub = np.concatenate([h, -h])

    bounds = [(None, None)] * (n_v + n_f) + [(0, None)] * n_e
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if res.success:
        alpha = res.x[:n_v]
        beta = res.x[n_v:n_v + n_f]
        size = float(res.fun)
        residual_vec = h - d0 @ alpha - d1 @ beta
    else:
        alpha = np.zeros(n_v)
        beta = np.zeros(n_f)
        residual_vec = h
        size = float(np.sum(np.abs(h)))

    residual = {e: float(residual_vec[i]) for i, e in enumerate(network.edges)}
    pots = {n: float(alpha[node_idx[n]]) for n in network.nodes}
    cycle_coeffs = {f: float(beta[j]) for j, f in enumerate(network.faces)}

    return {
        "residual_size": size,
        "residual": residual,
        "potentials": pots,
        "cycle_coeffs": cycle_coeffs,
        "is_zero": size < 1e-8,
    }


def vector_residual_after_gauge_fix(
    network: Network,
    vector_edge_values: Dict[Tuple[Any, Any], np.ndarray],
    method: str = "so_k_l2",
) -> Dict[str, Any]:
    """Extract vector potential field alpha minimizing edge residuals under SO(k) Euclidean norms.

    Parameters:
        network: Network topology.
        vector_edge_values: Mapping of edge (u, v) -> vector in R^k.
        method: Optimization norm:
            - 'so_k_l2': Least-squares minimization of sum_e ||r_e||_2^2.
            - 'so_k_l1_l2': Sum of Euclidean norms sum_e ||r_e||_2 (Paper 008 diagnostic).
    """
    if not network.edges:
        return {"residual_size": 0.0, "residual": {}, "potentials": {}, "is_pure_gauge": True}

    d0, node_idx = build_incidence(network)
    n_v, n_e = len(network.nodes), len(network.edges)

    first_val = next(iter(vector_edge_values.values()))
    k_dim = len(first_val)

    h_mat = np.zeros((n_e, k_dim))
    for i, e in enumerate(network.edges):
        h_mat[i, :] = vector_edge_values.get(e, np.zeros(k_dim))

    if method == "so_k_l2":
        alpha_mat, _, _, _ = np.linalg.lstsq(d0, h_mat, rcond=None)
        residual_mat = h_mat - d0 @ alpha_mat
        edge_lengths = np.linalg.norm(residual_mat, axis=1)
        size = float(np.sum(edge_lengths))
    else:
        from scipy.optimize import minimize

        def objective(x_flat):
            alpha = x_flat.reshape((n_v, k_dim))
            res = h_mat - d0 @ alpha
            return float(np.sum(np.linalg.norm(res, axis=1)))

        x0 = np.zeros((n_v, k_dim)).flatten()
        opt_res = minimize(objective, x0, method="BFGS")
        alpha_mat = opt_res.x.reshape((n_v, k_dim))
        residual_mat = h_mat - d0 @ alpha_mat
        edge_lengths = np.linalg.norm(residual_mat, axis=1)
        size = float(np.sum(edge_lengths))

    residual = {e: residual_mat[i, :] for i, e in enumerate(network.edges)}
    pots = {n: alpha_mat[node_idx[n], :] for n in network.nodes}
    return {
        "residual_size": size,
        "residual": residual,
        "potentials": pots,
        "is_pure_gauge": size < 1e-8,
    }
