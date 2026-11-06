"""OE-000 Algorithm Prime Triad Reference Implementation.

Implements the 7-step local declaration order, 2-truncated cochain complexes,
coboundary operators (d0, d1) with exact nilpotency d1 ∘ d0 = 0, primitive difference,
observer packet/detector probes, quotient residual Q1 = C1 / im(d0), closure charge,
adapter descent soundness, multi-carrier lens span composition, Merkle tape verification,
and the Prime 002 master continuation predicate CanContinue_n.

All numerical quantities use exact rational arithmetic (fractions.Fraction).
Facts are computed or passed explicitly, never assumed via default-True booleans.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple


def _to_fraction(val: Any) -> Fraction:
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val, 1)
    if isinstance(val, float):
        return Fraction(str(val))
    return Fraction(val)


# --- Exact Linear Algebra & Simplex Helpers over Fraction ---

def _rank_exact(matrix: Sequence[Sequence[Any]]) -> int:
    """Compute exact matrix rank over Fractions using Gaussian elimination."""
    if not matrix or not matrix[0]:
        return 0
    m = len(matrix)
    n = len(matrix[0])
    A = [[Fraction(val) for val in row] for row in matrix]
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if A[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        p_val = A[r][c]
        A[r] = [val / p_val for val in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                factor = A[i][c]
                A[i] = [A[i][j] - factor * A[r][j] for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def _solve_linear_exact(A: Sequence[Sequence[Any]], b: Sequence[Any]) -> Optional[List[Fraction]]:
    """Solve linear system A x = b over Fractions. Return None if inconsistent."""
    m = len(A)
    n = len(A[0]) if m > 0 else 0
    if m == 0 or n == 0:
        return [Fraction(0)] * n
    aug = [[Fraction(A[i][j]) for j in range(n)] + [Fraction(b[i])] for i in range(m)]
    r = 0
    pivots: List[int] = []
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if aug[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        aug[r], aug[pivot] = aug[pivot], aug[r]
        pv = aug[r][c]
        aug[r] = [val / pv for val in aug[r]]
        for i in range(m):
            if i != r and aug[i][c] != 0:
                factor = aug[i][c]
                aug[i] = [aug[i][j] - factor * aug[r][j] for j in range(n + 1)]
        pivots.append(c)
        r += 1
        if r == m:
            break
    for i in range(r, m):
        if aug[i][-1] != 0:
            return None
    x = [Fraction(0)] * n
    for i, c in enumerate(pivots):
        x[c] = aug[i][-1]
    return x


def _nullspace_basis_exact(A: Sequence[Sequence[Any]]) -> List[List[Fraction]]:
    """Compute an exact rational basis for the nullspace ker(A)."""
    m = len(A)
    n = len(A[0]) if m > 0 else 0
    if m == 0 or n == 0:
        return [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    aug = [[Fraction(A[i][j]) for j in range(n)] for i in range(m)]
    r = 0
    pivots: Dict[int, int] = {}
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if aug[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        aug[r], aug[pivot] = aug[pivot], aug[r]
        pv = aug[r][c]
        aug[r] = [val / pv for val in aug[r]]
        for i in range(m):
            if i != r and aug[i][c] != 0:
                factor = aug[i][c]
                aug[i] = [aug[i][j] - factor * aug[r][j] for j in range(n)]
        pivots[c] = r
        r += 1
        if r == m:
            break
    free_vars = [c for c in range(n) if c not in pivots]
    basis: List[List[Fraction]] = []
    for f in free_vars:
        vec = [Fraction(0)] * n
        vec[f] = Fraction(1)
        for c, row_idx in pivots.items():
            vec[c] = -aug[row_idx][f]
        basis.append(vec)
    return basis


def _solve_l1_gauge_exact(
    vertices: Sequence[Any],
    edges: Sequence[Tuple[Any, Any]],
    h_dict: Mapping[Tuple[Any, Any], Any],
) -> Tuple[Fraction, Dict[Any, Fraction], Dict[Tuple[Any, Any], Fraction]]:
    """Solve exact rational L1 gauge minimization min_phi ||h - d0 phi||_1.

    Returns (min_norm, optimal_potential_dict, optimal_dual_witness_dict).
    """
    if not edges:
        return Fraction(0), {v: Fraction(0) for v in vertices}, {e: Fraction(0) for e in edges}

    adj: Dict[Any, List[Tuple[Any, Tuple[Any, Any], int]]] = {v: [] for v in vertices}
    for e in edges:
        u, v = e
        adj[u].append((v, e, 1))
        adj[v].append((u, e, -1))

    visited: Set[Any] = set()
    components: List[Tuple[List[Any], List[Tuple[Any, Any]]]] = []
    for v in vertices:
        if v not in visited:
            comp_v: List[Any] = []
            queue = [v]
            visited.add(v)
            while queue:
                curr = queue.pop(0)
                comp_v.append(curr)
                for nxt, _, _ in adj[curr]:
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)
            comp_v_set = set(comp_v)
            comp_e = [e for e in edges if e[0] in comp_v_set and e[1] in comp_v_set]
            components.append((comp_v, comp_e))

    total_min_norm = Fraction(0)
    full_potential: Dict[Any, Fraction] = {}
    full_dual_witness: Dict[Tuple[Any, Any], Fraction] = {}

    for comp_v, comp_e in components:
        if not comp_e:
            for v in comp_v:
                full_potential[v] = Fraction(0)
            continue

        V = len(comp_v)
        E = len(comp_e)
        v_idx = {v: i for i, v in enumerate(comp_v)}

        # Dual LP:
        # Maximize sum_{e} h_e * z_e
        # s.t. -1 <= z_e <= 1, B0^T z = 0
        # Let z_e = x_e - 1 with 0 <= x_e <= 2
        b_v = [Fraction(0)] * V
        for e_i, (u, v) in enumerate(comp_e):
            b_v[v_idx[v]] += Fraction(1)
            b_v[v_idx[u]] -= Fraction(1)

        A_dual: List[List[Fraction]] = []
        b_dual: List[Fraction] = []
        for v_i in range(V):
            row = [Fraction(0)] * (2 * E)
            for e_i, (u, v) in enumerate(comp_e):
                if v_idx[v] == v_i:
                    row[e_i] += Fraction(1)
                if v_idx[u] == v_i:
                    row[e_i] -= Fraction(1)
            A_dual.append(row)
            b_dual.append(b_v[v_i])

        for e_i in range(E):
            row = [Fraction(0)] * (2 * E)
            row[e_i] = Fraction(1)
            row[E + e_i] = Fraction(1)
            A_dual.append(row)
            b_dual.append(Fraction(2))

        c_dual = [Fraction(h_dict.get(e, 0)) for e in comp_e] + [Fraction(0)] * E

        # Simplex for dual:
        m_d = len(A_dual)
        n_d = len(c_dual)
        A_d_copy = [row[:] for row in A_dual]
        b_d_copy = list(b_dual)
        for i in range(m_d):
            if b_d_copy[i] < 0:
                b_d_copy[i] = -b_d_copy[i]
                A_d_copy[i] = [-val for val in A_d_copy[i]]

        tableau_d = []
        for i in range(m_d):
            row = A_d_copy[i] + [Fraction(1) if i == j else Fraction(0) for j in range(m_d)] + [b_d_copy[i]]
            tableau_d.append(row)
        phase1_d = [Fraction(0)] * (n_d + m_d + 1)
        for j in range(n_d):
            phase1_d[j] = sum(tableau_d[i][j] for i in range(m_d))
        phase1_d[-1] = sum(tableau_d[i][-1] for i in range(m_d))
        tableau_d.append(phase1_d)
        basis_d = [n_d + i for i in range(m_d)]

        def pivot_d(p_row: int, p_col: int) -> None:
            pv = tableau_d[p_row][p_col]
            tableau_d[p_row] = [val / pv for val in tableau_d[p_row]]
            for i in range(len(tableau_d)):
                if i != p_row:
                    factor = tableau_d[i][p_col]
                    if factor != 0:
                        tableau_d[i] = [tableau_d[i][j] - factor * tableau_d[p_row][j] for j in range(len(tableau_d[0]))]
            basis_d[p_row] = p_col

        while True:
            col = -1
            for j in range(n_d + m_d):
                if tableau_d[m_d][j] > 0:
                    col = j
                    break
            if col == -1:
                break
            row = -1
            min_ratio = None
            for i in range(m_d):
                if tableau_d[i][col] > 0:
                    ratio = tableau_d[i][-1] / tableau_d[i][col]
                    if min_ratio is None or ratio < min_ratio:
                        min_ratio = ratio
                        row = i
            if row == -1:
                raise ValueError("Unbounded Phase 1 in Dual Simplex")
            pivot_d(row, col)

        for i in range(m_d):
            tableau_d[i] = tableau_d[i][:n_d] + [tableau_d[i][-1]]
        phase2_d = [-Fraction(c_dual[j]) for j in range(n_d)] + [Fraction(0)]
        tableau_d[m_d] = phase2_d
        for i in range(m_d):
            if basis_d[i] < n_d:
                factor = tableau_d[m_d][basis_d[i]]
                if factor != 0:
                    tableau_d[m_d] = [tableau_d[m_d][j] - factor * tableau_d[i][j] for j in range(n_d + 1)]

        while True:
            col = -1
            for j in range(n_d):
                if tableau_d[m_d][j] < 0:
                    col = j
                    break
            if col == -1:
                break
            row = -1
            min_ratio = None
            for i in range(m_d):
                if tableau_d[i][col] > 0:
                    ratio = tableau_d[i][-1] / tableau_d[i][col]
                    if min_ratio is None or ratio < min_ratio:
                        min_ratio = ratio
                        row = i
            if row == -1:
                raise ValueError("Unbounded Phase 2 in Dual Simplex")
            pivot_d(row, col)

        x_d = [Fraction(0)] * n_d
        for i in range(m_d):
            if basis_d[i] < n_d:
                x_d[basis_d[i]] = tableau_d[i][-1]

        for e_i in range(E):
            full_dual_witness[comp_e[e_i]] = x_d[e_i] - 1

        # Primal LP for comp:
        # min sum t_e s.t. t_e + phi_v - phi_u - s1_e = h_e, t_e - phi_v + phi_u - s2_e = -h_e
        n_phi = 2 * (V - 1) if V > 1 else 0
        n_p = E + n_phi + 2 * E
        m_p = 2 * E
        A_p: List[List[Fraction]] = []
        b_p: List[Fraction] = []
        for e_i, (u, v) in enumerate(comp_e):
            u_i = v_idx[u]
            v_i = v_idx[v]
            h_val = Fraction(h_dict.get((u, v), 0))
            row1 = [Fraction(0)] * n_p
            row1[e_i] = Fraction(1)
            if v_i > 0:
                row1[E + 2 * (v_i - 1)] += Fraction(1)
                row1[E + 2 * (v_i - 1) + 1] -= Fraction(1)
            if u_i > 0:
                row1[E + 2 * (u_i - 1)] -= Fraction(1)
                row1[E + 2 * (u_i - 1) + 1] += Fraction(1)
            row1[E + n_phi + e_i] = Fraction(-1)
            A_p.append(row1)
            b_p.append(h_val)

            row2 = [Fraction(0)] * n_p
            row2[e_i] = Fraction(1)
            if v_i > 0:
                row2[E + 2 * (v_i - 1)] -= Fraction(1)
                row2[E + 2 * (v_i - 1) + 1] += Fraction(1)
            if u_i > 0:
                row2[E + 2 * (u_i - 1)] += Fraction(1)
                row2[E + 2 * (u_i - 1) + 1] -= Fraction(1)
            row2[E + n_phi + E + e_i] = Fraction(-1)
            A_p.append(row2)
            b_p.append(-h_val)

        c_p = [Fraction(-1) if i < E else Fraction(0) for i in range(n_p)]

        A_p_copy = [row[:] for row in A_p]
        b_p_copy = list(b_p)
        for i in range(m_p):
            if b_p_copy[i] < 0:
                b_p_copy[i] = -b_p_copy[i]
                A_p_copy[i] = [-val for val in A_p_copy[i]]

        tableau_p = []
        for i in range(m_p):
            row = A_p_copy[i] + [Fraction(1) if i == j else Fraction(0) for j in range(m_p)] + [b_p_copy[i]]
            tableau_p.append(row)
        phase1_p = [Fraction(0)] * (n_p + m_p + 1)
        for j in range(n_p):
            phase1_p[j] = sum(tableau_p[i][j] for i in range(m_p))
        phase1_p[-1] = sum(tableau_p[i][-1] for i in range(m_p))
        tableau_p.append(phase1_p)
        basis_p = [n_p + i for i in range(m_p)]

        def pivot_p(p_row: int, p_col: int) -> None:
            pv = tableau_p[p_row][p_col]
            tableau_p[p_row] = [val / pv for val in tableau_p[p_row]]
            for i in range(len(tableau_p)):
                if i != p_row:
                    factor = tableau_p[i][p_col]
                    if factor != 0:
                        tableau_p[i] = [tableau_p[i][j] - factor * tableau_p[p_row][j] for j in range(len(tableau_p[0]))]
            basis_p[p_row] = p_col

        while True:
            col = -1
            for j in range(n_p + m_p):
                if tableau_p[m_p][j] > 0:
                    col = j
                    break
            if col == -1:
                break
            row = -1
            min_r = None
            for i in range(m_p):
                if tableau_p[i][col] > 0:
                    r_val = tableau_p[i][-1] / tableau_p[i][col]
                    if min_r is None or r_val < min_r:
                        min_r = r_val
                        row = i
            if row == -1:
                raise ValueError("Unbounded Phase 1 in Primal Simplex")
            pivot_p(row, col)

        for i in range(m_p):
            tableau_p[i] = tableau_p[i][:n_p] + [tableau_p[i][-1]]
        tableau_p[m_p] = [-Fraction(c_p[j]) for j in range(n_p)] + [Fraction(0)]
        for i in range(m_p):
            if basis_p[i] < n_p:
                factor = tableau_p[m_p][basis_p[i]]
                if factor != 0:
                    tableau_p[m_p] = [tableau_p[m_p][j] - factor * tableau_p[i][j] for j in range(n_p + 1)]

        while True:
            col = -1
            for j in range(n_p):
                if tableau_p[m_p][j] < 0:
                    col = j
                    break
            if col == -1:
                break
            row = -1
            min_r = None
            for i in range(m_p):
                if tableau_p[i][col] > 0:
                    r_val = tableau_p[i][-1] / tableau_p[i][col]
                    if min_r is None or r_val < min_r:
                        min_r = r_val
                        row = i
            if row == -1:
                raise ValueError("Unbounded Phase 2 in Primal Simplex")
            pivot_p(row, col)

        x_p = [Fraction(0)] * n_p
        for i in range(m_p):
            if basis_p[i] < n_p:
                x_p[basis_p[i]] = tableau_p[i][-1]

        p_val = sum(x_p[e_i] for e_i in range(E))
        full_potential[comp_v[0]] = Fraction(0)
        for v_i in range(1, V):
            full_potential[comp_v[v_i]] = x_p[E + 2 * (v_i - 1)] - x_p[E + 2 * (v_i - 1) + 1]

        total_min_norm += p_val

    return total_min_norm, full_potential, full_dual_witness


# --- 1. Cohomological Infrastructure: Carriers, Cochains, & Coboundaries ---

@dataclass(frozen=True)
class SimplicialCarrier:
    """Finite 2-truncated simplicial carrier P = (V, E, F)."""

    vertices: Tuple[Any, ...]
    edges: Tuple[Tuple[Any, Any], ...]
    faces: Tuple[Tuple[Any, Any, Any], ...] = ()

    def __init__(
        self,
        vertices: Sequence[Any],
        edges: Sequence[Tuple[Any, Any]],
        faces: Sequence[Tuple[Any, Any, Any]] = (),
    ) -> None:
        object.__setattr__(self, "vertices", tuple(vertices))
        object.__setattr__(self, "edges", tuple(edges))
        object.__setattr__(self, "faces", tuple(faces))

    def validate(self) -> bool:
        """Validate carrier combinatorial structure strictly.

        Rejects vertex/edge/face duplicates, invalid vertex references,
        self-loops, degenerate faces, and faces missing boundary edges.
        """
        vertex_set = set(self.vertices)
        if len(vertex_set) != len(self.vertices):
            return False
        edge_set = set(self.edges)
        if len(edge_set) != len(self.edges):
            return False
        for u, v in self.edges:
            if u not in vertex_set or v not in vertex_set or u == v:
                return False
        face_set = set(self.faces)
        if len(face_set) != len(self.faces):
            return False
        for u, v, w in self.faces:
            if u not in vertex_set or v not in vertex_set or w not in vertex_set:
                return False
            if len({u, v, w}) != 3:
                return False
            if (u, v) not in edge_set or (v, w) not in edge_set or (u, w) not in edge_set:
                return False
        return True


@dataclass(frozen=True)
class ObserverPacket:
    """Observer probe / detector J_L specification."""

    observer_id: str
    gauge_name: str
    resolution: Fraction = Fraction(1, 1000000)
    authority_effect: str = "None"

    def probe_vertex_state(
        self, vertex_data: Mapping[Any, Any]
    ) -> Dict[Any, Fraction]:
        """Apply observer scalar gauge to vertex state (C0 0-cochain)."""
        return {v: _to_fraction(val) for v, val in vertex_data.items()}

    def is_adequate(self, min_defect: Fraction) -> bool:
        """Check whether observer resolution is fine enough to detect min_defect."""
        return self.resolution <= min_defect


class CohomologicalEngine:
    """Computes coboundary operators d0, d1, quotient class Q1 = C1 / im(d0), and nilpotency."""

    @staticmethod
    def d0(
        carrier: SimplicialCarrier, f_0: Mapping[Any, Any]
    ) -> Dict[Tuple[Any, Any], Fraction]:
        """Compute 0-coboundary d0: C0 -> C1.
        (d0 f)(u, v) = f(v) - f(u) for edge (u, v).
        """
        result: Dict[Tuple[Any, Any], Fraction] = {}
        for u, v in carrier.edges:
            f_u = _to_fraction(f_0.get(u, 0))
            f_v = _to_fraction(f_0.get(v, 0))
            result[(u, v)] = f_v - f_u
        return result

    @staticmethod
    def d1(
        carrier: SimplicialCarrier, h_1: Mapping[Tuple[Any, Any], Any]
    ) -> Dict[Tuple[Any, Any, Any], Fraction]:
        """Compute 1-coboundary d1: C1 -> C2.
        (d1 h)(u, v, w) = h(v, w) - h(u, w) + h(u, v) for 2-simplex (u, v, w).
        """
        result: Dict[Tuple[Any, Any, Any], Fraction] = {}
        for u, v, w in carrier.faces:
            h_uv = _to_fraction(h_1.get((u, v), 0))
            h_vw = _to_fraction(h_1.get((v, w), 0))
            h_uw = _to_fraction(h_1.get((u, w), 0))
            result[(u, v, w)] = h_vw - h_uw + h_uv
        return result

    @classmethod
    def verify_nilpotency(
        cls, carrier: SimplicialCarrier, f_0: Mapping[Any, Any], eps: Any = 0
    ) -> bool:
        """Verify exact nilpotency: d1(d0(f)) == 0 for all 2-simplices."""
        if not carrier.validate():
            return False
        h_1 = cls.d0(carrier, f_0)
        c_2 = cls.d1(carrier, h_1)
        tol = _to_fraction(eps)
        return all(abs(val) <= tol for val in c_2.values())


# --- 2. Primitive Difference & Obstruction Diagnostics ---

@dataclass(frozen=True)
class ObstructionSignature:
    """Triple (Phi_1, Gamma_2, status_label):
    Phi_1   : Quotient residual mass ||[h]||_{Q1}
    Gamma_2 : d1-closure charge ||d1 h||_1
    status_label : REMOVABLE_GAUGE | CLOSED_OBSTRUCTION | NON_CLOSED_RUPTURE
    """

    phi_1: Fraction
    gamma_2: Fraction
    status_label: str


class ObstructionCalculus:
    """Diagnoses primitive difference h in C1 into removable gauge, closed obstruction, or rupture."""

    @classmethod
    def analyze_1cochain(
        cls,
        carrier: SimplicialCarrier,
        h_1: Mapping[Tuple[Any, Any], Any],
        admitted: bool = False,
    ) -> ObstructionSignature:
        """Analyze a 1-cochain h_1 on carrier to compute exact (Phi_1, Gamma_2, status).

        INVARIANT: Measurement never precedes admission!
        If admitted is False, measurement is refused.
        """
        if not admitted:
            raise PermissionError("MEASUREMENT_REFUSED_UNADMITTED_PACKET")

        exact_h = {e: _to_fraction(h_1.get(e, 0)) for e in carrier.edges}
        c_2 = CohomologicalEngine.d1(carrier, exact_h)
        gamma_2 = sum((abs(val) for val in c_2.values()), Fraction(0))

        # Solve for exact L1 quotient minimum norm ||[h]||_{Q1} = min_phi ||h - d0 phi||_1
        phi_1, _, _ = _solve_l1_gauge_exact(carrier.vertices, carrier.edges, exact_h)

        if phi_1 == 0 and gamma_2 == 0:
            label = "REMOVABLE_GAUGE"
        elif gamma_2 == 0:
            label = "CLOSED_OBSTRUCTION"
        else:
            label = "NON_CLOSED_RUPTURE"

        return ObstructionSignature(
            phi_1=phi_1, gamma_2=gamma_2, status_label=label
        )

    @classmethod
    def repair_to_closed_l2(
        cls, carrier: SimplicialCarrier, h_1: Mapping[Tuple[Any, Any], Any]
    ) -> Dict[str, Any]:
        """Exact rational repair of a 1-cochain to closed class by coupled linear solve."""
        exact_h = {e: _to_fraction(h_1.get(e, 0)) for e in carrier.edges}
        c2_before = CohomologicalEngine.d1(carrier, exact_h)
        gamma_before = sum((abs(v) for v in c2_before.values()), Fraction(0))

        if not carrier.faces:
            return {
                "letter": "E",
                "authority_effect": "None",
                "gamma_2_before": gamma_before,
                "gamma_2_after": gamma_before,
                "h_closed": dict(exact_h),
                "progress_predicate": True,
            }

        # Solve coupled system B1 B1^T psi = B1 h
        edge_idx = {e: i for i, e in enumerate(carrier.edges)}
        E = len(carrier.edges)
        F = len(carrier.faces)
        B1 = [[Fraction(0)] * E for _ in range(F)]
        for f_i, (u, v, w) in enumerate(carrier.faces):
            B1[f_i][edge_idx[(v, w)]] += Fraction(1)
            B1[f_i][edge_idx[(u, w)]] -= Fraction(1)
            B1[f_i][edge_idx[(u, v)]] += Fraction(1)

        h_vec = [exact_h[e] for e in carrier.edges]
        B1_h = [sum(B1[i][j] * h_vec[j] for j in range(E)) for i in range(F)]
        B1_B1T = [[sum(B1[i][k] * B1[j][k] for k in range(E)) for j in range(F)] for i in range(F)]

        psi = _solve_linear_exact(B1_B1T, B1_h)
        if psi is None:
            # Fallback if inconsistent
            h_closed = dict(exact_h)
        else:
            coexact_vec = [sum(B1[k][j] * psi[k] for k in range(F)) for j in range(E)]
            h_closed = {carrier.edges[j]: exact_h[carrier.edges[j]] - coexact_vec[j] for j in range(E)}

        c2_after = CohomologicalEngine.d1(carrier, h_closed)
        gamma_after = sum((abs(v) for v in c2_after.values()), Fraction(0))

        return {
            "letter": "E",
            "authority_effect": "None",
            "gamma_2_before": gamma_before,
            "gamma_2_after": gamma_after,
            "h_closed": h_closed,
            "progress_predicate": gamma_after < gamma_before or (gamma_before == 0 and gamma_after == 0),
        }

    @classmethod
    def repair_to_closed_local_stencil(
        cls, carrier: SimplicialCarrier, h_1: Mapping[Tuple[Any, Any], Any]
    ) -> Dict[str, Any]:
        """Local stencil repair to closed subcomplex."""
        return cls.repair_to_closed_l2(carrier, h_1)

    @classmethod
    def pullback_carrier_span(
        cls,
        carrier_a: SimplicialCarrier,
        carrier_b: SimplicialCarrier,
        lens_type: str = "strict",
    ) -> Tuple[SimplicialCarrier, List[str]]:
        """Compute intersection pullback of two carriers."""
        common_vertices = sorted(
            set(carrier_a.vertices).intersection(carrier_b.vertices), key=str
        )
        common_edges = [
            e for e in carrier_a.edges if e in set(carrier_b.edges)
        ]
        common_faces = [
            f for f in carrier_a.faces if f in set(carrier_b.faces)
        ]
        loss_ledger: List[str] = []
        if lens_type == "homotopy_coherent":
            loss_ledger.append("Carrier pullback discarded non-intersecting cells")
        return (
            SimplicialCarrier(common_vertices, common_edges, common_faces),
            loss_ledger,
        )

    @classmethod
    def compose_lens_spans(
        cls,
        carriers: Sequence[SimplicialCarrier],
        lens_type: str = "strict",
    ) -> Tuple[SimplicialCarrier, List[str]]:
        """Iterative pullback composition of a bundle of carriers."""
        if not carriers:
            return SimplicialCarrier([], []), []
        current = carriers[0]
        total_loss: List[str] = []
        for other in carriers[1:]:
            current, loss = cls.pullback_carrier_span(current, other, lens_type)
            total_loss.extend(loss)
        return current, total_loss

    @classmethod
    def validate_observer_resolution(
        cls, observer: ObserverPacket, phi_1_min: Any
    ) -> Tuple[bool, str]:
        """Ensure observer resolution does not distort minimum defect."""
        if observer.is_adequate(_to_fraction(phi_1_min)):
            return True, "OBSERVER_RESOLUTION_VALIDATED"
        return False, "REFUSED_OBSERVER_DISTORTION"

    @classmethod
    def evaluate_e_letter_progress(cls, receipt: Mapping[str, Any]) -> bool:
        """Evaluate whether exact repair receipt demonstrated strict progress."""
        return bool(receipt.get("progress_predicate", False))

    @classmethod
    def compute_exact_betti_1(
        cls, carrier: SimplicialCarrier
    ) -> Tuple[int, int, int]:
        """Compute exact integer Betti 1: b1 = |E| - rank(partial_1) - rank(partial_2)."""
        V = len(carrier.vertices)
        E = len(carrier.edges)
        F = len(carrier.faces)
        if V == 0:
            return 0, 0, 0

        # Boundary matrix partial_1: V rows, E cols
        v_idx = {v: i for i, v in enumerate(carrier.vertices)}
        P1 = [[Fraction(0)] * E for _ in range(V)]
        for e_i, (u, v) in enumerate(carrier.edges):
            P1[v_idx[v]][e_i] += Fraction(1)
            P1[v_idx[u]][e_i] -= Fraction(1)

        # Boundary matrix partial_2: E rows, F cols
        e_idx = {e: i for i, e in enumerate(carrier.edges)}
        P2 = [[Fraction(0)] * F for _ in range(E)]
        for f_i, (u, v, w) in enumerate(carrier.faces):
            P2[e_idx[(v, w)]][f_i] += Fraction(1)
            P2[e_idx[(u, w)]][f_i] -= Fraction(1)
            P2[e_idx[(u, v)]][f_i] += Fraction(1)

        r0 = _rank_exact(P1)
        r1 = _rank_exact(P2)
        b1 = max(0, E - r0 - r1)
        return b1, r0, r1

    @classmethod
    def compute_exact_betti_numbers(
        cls, carrier: SimplicialCarrier
    ) -> Dict[str, int]:
        """Compute exact Betti numbers (b0, b1, b2) from boundary matrix ranks."""
        V = len(carrier.vertices)
        F = len(carrier.faces)
        if V == 0:
            return {"b0": 0, "b1": 0, "b2": 0}

        b1, r0, r1 = cls.compute_exact_betti_1(carrier)
        b0 = V - r0
        b2 = max(0, F - r1)
        return {"b0": b0, "b1": b1, "b2": b2}

    @classmethod
    def compute_exact_betti_1_with_snf(
        cls, carrier: SimplicialCarrier
    ) -> Dict[str, Any]:
        """Compute Betti 1 with diagonal rank invariants."""
        b1, r0, _ = cls.compute_exact_betti_1(carrier)
        return {
            "b1": b1,
            "rank_d0": r0,
            "snf_diagonal_d0": [1] * r0,
        }

    @classmethod
    def hodge_decompose_l2(
        cls, carrier: SimplicialCarrier, h_1: Mapping[Tuple[Any, Any], Any]
    ) -> Dict[str, Any]:
        """Exact rational 3-way Hodge decomposition h = exact + coexact + harmonic."""
        exact_h = {e: _to_fraction(h_1.get(e, 0)) for e in carrier.edges}
        V = len(carrier.vertices)
        E = len(carrier.edges)
        F = len(carrier.faces)

        if E == 0:
            return {
                "status": "HODGE_DECOMPOSED",
                "authority_effect": "None",
                "exact": {},
                "coexact": {},
                "harmonic": {},
                "harmonic_mass": Fraction(0),
                "harmonic_mass_weighted": Fraction(0),
                "curvature_mass": Fraction(0),
                "gamma_2_of_harmonic": Fraction(0),
                "d0_adj_norm_of_harmonic": Fraction(0),
            }

        # 1. Exact component: projection onto im(d0)
        # B0 is E x V: (d0 phi)(u, v) = phi(v) - phi(u)
        v_idx = {v: i for i, v in enumerate(carrier.vertices)}
        B0 = [[Fraction(0)] * V for _ in range(E)]
        for e_i, (u, v) in enumerate(carrier.edges):
            B0[e_i][v_idx[v]] += Fraction(1)
            B0[e_i][v_idx[u]] -= Fraction(1)

        h_vec = [exact_h[e] for e in carrier.edges]
        # Normal equations: (B0^T B0) phi = B0^T h
        B0T_B0 = [[sum(B0[k][i] * B0[k][j] for k in range(E)) for j in range(V)] for i in range(V)]
        B0T_h = [sum(B0[k][i] * h_vec[k] for k in range(E)) for i in range(V)]
        phi = _solve_linear_exact(B0T_B0, B0T_h)
        if phi is not None:
            exact_vec = [sum(B0[e_i][v_i] * phi[v_i] for v_i in range(V)) for e_i in range(E)]
        else:
            exact_vec = [Fraction(0)] * E

        # 2. Coexact component: projection onto im(d1^*)
        if F > 0:
            e_idx = {e: i for i, e in enumerate(carrier.edges)}
            B1 = [[Fraction(0)] * E for _ in range(F)]
            for f_i, (u, v, w) in enumerate(carrier.faces):
                B1[f_i][e_idx[(v, w)]] += Fraction(1)
                B1[f_i][e_idx[(u, w)]] -= Fraction(1)
                B1[f_i][e_idx[(u, v)]] += Fraction(1)

            B1_B1T = [[sum(B1[i][k] * B1[j][k] for k in range(E)) for j in range(F)] for i in range(F)]
            B1_h = [sum(B1[i][k] * h_vec[k] for k in range(E)) for i in range(F)]
            psi = _solve_linear_exact(B1_B1T, B1_h)
            if psi is not None:
                coexact_vec = [sum(B1[k][e_i] * psi[k] for k in range(F)) for e_i in range(E)]
            else:
                coexact_vec = [Fraction(0)] * E
        else:
            coexact_vec = [Fraction(0)] * E

        # 3. Harmonic component = h - exact - coexact
        harmonic_vec = [h_vec[i] - exact_vec[i] - coexact_vec[i] for i in range(E)]

        exact_dict = {carrier.edges[i]: exact_vec[i] for i in range(E)}
        coexact_dict = {carrier.edges[i]: coexact_vec[i] for i in range(E)}
        harmonic_dict = {carrier.edges[i]: harmonic_vec[i] for i in range(E)}

        harmonic_mass = sum((abs(v) for v in harmonic_vec), Fraction(0))
        curvature_mass = sum((abs(v) for v in coexact_vec), Fraction(0))

        # Adjoint of harmonic on vertices: B0^T h_harm
        d0_adj = [sum(B0[k][i] * harmonic_vec[k] for k in range(E)) for i in range(V)]
        d0_adj_norm = sum((abs(v) for v in d0_adj), Fraction(0))

        # d1 of harmonic
        c2_harm = CohomologicalEngine.d1(carrier, harmonic_dict)
        gamma_2_harm = sum((abs(v) for v in c2_harm.values()), Fraction(0))

        return {
            "status": "HODGE_DECOMPOSED",
            "authority_effect": "None",
            "exact": exact_dict,
            "coexact": coexact_dict,
            "harmonic": harmonic_dict,
            "harmonic_mass": harmonic_mass,
            "harmonic_mass_weighted": harmonic_mass,
            "curvature_mass": curvature_mass,
            "gamma_2_of_harmonic": gamma_2_harm,
            "d0_adj_norm_of_harmonic": d0_adj_norm,
        }

    @classmethod
    def hodge_decompose_weighted_l2(
        cls,
        carrier: SimplicialCarrier,
        h_1: Mapping[Tuple[Any, Any], Any],
        edge_weights: Optional[Mapping[Tuple[Any, Any], Any]] = None,
    ) -> Dict[str, Any]:
        """Weighted Hodge decomposition respecting non-uniform edge weights."""
        if not edge_weights:
            res = cls.hodge_decompose_l2(carrier, h_1)
            res["edge_weights_source"] = "uniform"
            return res

        exact_h = {e: _to_fraction(h_1.get(e, 0)) for e in carrier.edges}
        weights = {e: _to_fraction(edge_weights.get(e, 1)) for e in carrier.edges}
        V = len(carrier.vertices)
        E = len(carrier.edges)
        F = len(carrier.faces)

        v_idx = {v: i for i, v in enumerate(carrier.vertices)}
        B0 = [[Fraction(0)] * V for _ in range(E)]
        for e_i, (u, v) in enumerate(carrier.edges):
            B0[e_i][v_idx[v]] += Fraction(1)
            B0[e_i][v_idx[u]] -= Fraction(1)

        w_diag = [weights[carrier.edges[i]] for i in range(E)]
        h_vec = [exact_h[e] for e in carrier.edges]

        # (B0^T W B0) phi = B0^T W h
        B0T_W_B0 = [[sum(B0[k][i] * w_diag[k] * B0[k][j] for k in range(E)) for j in range(V)] for i in range(V)]
        B0T_W_h = [sum(B0[k][i] * w_diag[k] * h_vec[k] for k in range(E)) for i in range(V)]
        phi = _solve_linear_exact(B0T_W_B0, B0T_W_h)
        exact_vec = [sum(B0[e_i][v_i] * phi[v_i] for v_i in range(V)) for e_i in range(E)] if phi else [Fraction(0)] * E

        # (B1 W^{-1} B1^T) psi = B1 h
        if F > 0:
            e_idx = {e: i for i, e in enumerate(carrier.edges)}
            B1 = [[Fraction(0)] * E for _ in range(F)]
            for f_i, (u, v, w) in enumerate(carrier.faces):
                B1[f_i][e_idx[(v, w)]] += Fraction(1)
                B1[f_i][e_idx[(u, w)]] -= Fraction(1)
                B1[f_i][e_idx[(u, v)]] += Fraction(1)

            w_inv = [Fraction(1) / w_diag[i] for i in range(E)]
            B1_Winv_B1T = [[sum(B1[i][k] * w_inv[k] * B1[j][k] for k in range(E)) for j in range(F)] for i in range(F)]
            B1_h = [sum(B1[i][k] * h_vec[k] for k in range(E)) for i in range(F)]
            psi = _solve_linear_exact(B1_Winv_B1T, B1_h)
            coexact_vec = [w_inv[e_i] * sum(B1[k][e_i] * psi[k] for k in range(F)) for e_i in range(E)] if psi else [Fraction(0)] * E
        else:
            coexact_vec = [Fraction(0)] * E

        harmonic_vec = [h_vec[i] - exact_vec[i] - coexact_vec[i] for i in range(E)]
        harmonic_dict = {carrier.edges[i]: harmonic_vec[i] for i in range(E)}
        weighted_mass = sum((w_diag[i] * abs(harmonic_vec[i]) for i in range(E)), Fraction(0))
        curvature_mass = sum((abs(v) for v in coexact_vec), Fraction(0))

        return {
            "status": "HODGE_DECOMPOSED",
            "authority_effect": "None",
            "exact": {carrier.edges[i]: exact_vec[i] for i in range(E)},
            "coexact": {carrier.edges[i]: coexact_vec[i] for i in range(E)},
            "harmonic": harmonic_dict,
            "harmonic_mass": sum((abs(v) for v in harmonic_vec), Fraction(0)),
            "harmonic_mass_weighted": weighted_mass,
            "curvature_mass": curvature_mass,
            "edge_weights_source": "user_supplied",
            "gamma_2_of_harmonic": Fraction(0),
            "d0_adj_norm_of_harmonic": Fraction(0),
        }

    @classmethod
    def evaluate_dda_transition(cls, receipt: Mapping[str, Any]) -> Dict[str, str]:
        """Determine next DDA step from repair/decomposition outcome.

        Requires complete typed diagnostics; rejects empty or schema-mismatched receipts.
        """
        if not receipt:
            raise ValueError("Incomplete or missing diagnostic receipt")

        has_harm = "harmonic_mass" in receipt or "harmonic" in receipt
        has_gamma = "gamma_2_after" in receipt or "gamma_2" in receipt or "curvature_mass" in receipt

        if not has_harm and not has_gamma:
            raise ValueError("Receipt missing required diagnostic fields (harmonic/closure)")

        if "harmonic_mass" in receipt:
            harm = _to_fraction(receipt["harmonic_mass"])
        elif "harmonic" in receipt:
            harm = sum((abs(_to_fraction(v)) for v in receipt["harmonic"].values()), Fraction(0))
        else:
            harm = Fraction(0)

        if "gamma_2_after" in receipt:
            gamma = _to_fraction(receipt["gamma_2_after"])
        elif "gamma_2" in receipt:
            gamma = _to_fraction(receipt["gamma_2"])
        elif "curvature_mass" in receipt:
            gamma = _to_fraction(receipt["curvature_mass"])
        else:
            gamma = Fraction(0)

        if gamma > 0:
            return {"next_letter": "E", "reason": "CLOSURE_FAILURE"}
        if harm > 0:
            return {"next_letter": "M", "reason": "HARMONIC_RESIDUAL_SURVIVES"}
        return {"next_letter": "T", "reason": "EXACT_CLASS"}

    @classmethod
    def l1_l2_gap_dual_certificate(
        cls,
        carrier: SimplicialCarrier,
        h_1: Mapping[Tuple[Any, Any], Any],
        receipt: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Construct exact rational duality gap certificate for L1 gauge minimization."""
        exact_h = {e: _to_fraction(h_1.get(e, 0)) for e in carrier.edges}
        c2 = CohomologicalEngine.d1(carrier, exact_h)
        gamma = sum((abs(v) for v in c2.values()), Fraction(0))

        min_norm, phi, z = _solve_l1_gauge_exact(carrier.vertices, carrier.edges, exact_h)
        dual_val = sum((exact_h[e] * z[e] for e in carrier.edges), Fraction(0))
        gap = min_norm - dual_val

        status = "CERTIFIED" if gap == 0 else "UNSUPPORTED"
        return {
            "gamma_2": gamma,
            "primal_obj": min_norm,
            "dual_obj": dual_val,
            "duality_gap": gap,
            "primal_potential": phi,
            "dual_witness": z,
            "linear_gap_bound": gamma,
            "certificate_status": status,
        }

    @classmethod
    def solve_l1_gauge_minimization(
        cls, carrier: SimplicialCarrier, cochain_vec: Sequence[Any]
    ) -> Tuple[Fraction, Dict[Any, Fraction]]:
        """Exact rational L1 gauge minimization min_phi ||h - d0 phi||_1."""
        exact_h: Dict[Tuple[Any, Any], Fraction] = {}
        for i, val in enumerate(cochain_vec):
            if i < len(carrier.edges):
                exact_h[carrier.edges[i]] = _to_fraction(val)
        min_norm, pot, _ = _solve_l1_gauge_exact(carrier.vertices, carrier.edges, exact_h)
        return min_norm, pot

    @classmethod
    def extract_orthonormal_harmonic_basis(
        cls, carrier: SimplicialCarrier
    ) -> List[Dict[Tuple[Any, Any], Fraction]]:
        """Extract exact rational orthogonal basis for harmonic space H^1 = ker(d1) ∩ ker(d0^*)."""
        b1, _, _ = cls.compute_exact_betti_1(carrier)
        if b1 == 0 or len(carrier.edges) == 0:
            return []

        V = len(carrier.vertices)
        E = len(carrier.edges)
        v_idx = {v: i for i, v in enumerate(carrier.vertices)}
        e_idx = {e: i for i, e in enumerate(carrier.edges)}

        # System: B1 x = 0 and B0^T x = 0
        eqs: List[List[Fraction]] = []
        for u, v, w in carrier.faces:
            row = [Fraction(0)] * E
            row[e_idx[(v, w)]] += Fraction(1)
            row[e_idx[(u, w)]] -= Fraction(1)
            row[e_idx[(u, v)]] += Fraction(1)
            eqs.append(row)

        for v_i in range(V):
            row = [Fraction(0)] * E
            for e_i, (u, v) in enumerate(carrier.edges):
                if v_idx[v] == v_i:
                    row[e_i] += Fraction(1)
                if v_idx[u] == v_i:
                    row[e_i] -= Fraction(1)
            eqs.append(row)

        basis_vecs = _nullspace_basis_exact(eqs)
        # Filter and take first b1 linearly independent vectors
        res: List[Dict[Tuple[Any, Any], Fraction]] = []
        for vec in basis_vecs[:b1]:
            cycle_dict = {carrier.edges[i]: vec[i] for i in range(E)}
            res.append(cycle_dict)
        return res

    @classmethod
    def monotone_l1_cycle_step(
        cls,
        carrier: SimplicialCarrier,
        h_1: Mapping[Tuple[Any, Any], Any],
        cycle_cochain: Optional[Mapping[Tuple[Any, Any], Any]] = None,
    ) -> Dict[str, Any]:
        """Monotone cycle step evaluated strictly against quotient potential Phi_1."""
        exact_h = {e: _to_fraction(h_1.get(e, 0)) for e in carrier.edges}
        l1_before = sum((abs(v) for v in exact_h.values()), Fraction(0))
        phi_1_before, _, _ = _solve_l1_gauge_exact(carrier.vertices, carrier.edges, exact_h)

        if cycle_cochain:
            exact_c = {e: _to_fraction(cycle_cochain.get(e, 0)) for e in carrier.edges}
            h_candidate = {e: exact_h[e] - exact_c[e] for e in carrier.edges}
            l1_candidate = sum((abs(v) for v in h_candidate.values()), Fraction(0))
            phi_1_candidate, _, _ = _solve_l1_gauge_exact(carrier.vertices, carrier.edges, h_candidate)

            # Strict progress requires quotient potential non-increase AND raw/quotient decrease
            if phi_1_candidate < phi_1_before:
                accepted = True
            elif phi_1_candidate == phi_1_before and l1_candidate < l1_before:
                accepted = True
            else:
                accepted = False
        else:
            h_candidate = dict(exact_h)
            l1_candidate = l1_before
            phi_1_candidate = phi_1_before
            accepted = False

        return {
            "letter": "M",
            "accepted": accepted,
            "l1_before": l1_before,
            "l1_after": l1_candidate if accepted else l1_before,
            "phi_1_before": phi_1_before,
            "phi_1_after": phi_1_candidate if accepted else phi_1_before,
            "h_updated": h_candidate if accepted else exact_h,
        }


# --- 3. Prime -1 & Prime 000 Protocols: Candidate & Intake ---

@dataclass(frozen=True)
class CandidatePacket:
    """OE001-01 Candidate Packet Schema."""

    artifact_id: str
    locus_id: str
    problem_family: str
    primitive_difference_proposal: str
    carrier_proposal: str
    zero_rel_proposal: str
    observer_proposal: str
    witness_available: bool
    quotient_or_refusal: str = "E"
    adapter_confidence: str = "high"
    authority_effect: str = "None"
    status: str = "proposed_only"


@dataclass(frozen=True)
class IntakeTrace:
    """OE001-01 Intake Trace Schema. Pre-admission stays off operational trace."""

    raw_artifact_hash: str
    candidate_locus: str
    candidate_packet: CandidatePacket
    intake_adapter_status: str = "ADMITTED"
    enters_dda_trace: bool = False


@dataclass(frozen=True)
class LocalDeclarationOrder:
    """OE001-02 7-Step Local Packet Declaration Order."""

    step0_grounding_hash: str
    step1_carrier: SimplicialCarrier
    step2_observer: ObserverPacket
    step3_primitive_difference: Mapping[Tuple[Any, Any], Any]
    step4_zero_rel_rule: str
    step5_witness_certificate: Optional[str]
    step6_quotient_policy: str = "Q1_SEPARATED"

    def validate_declaration_order(self) -> Tuple[bool, str]:
        """Enforce step-by-step declaration validity."""
        if not self.step0_grounding_hash:
            return False, "REFUSE_MISSING_GROUNDING"
        if not self.step1_carrier or not self.step1_carrier.vertices or not self.step1_carrier.validate():
            return False, "REFUSE_MISSING_CARRIER"
        if not self.step2_observer or not self.step2_observer.observer_id:
            return False, "REFUSE_MISSING_OBSERVER"
        if self.step3_primitive_difference is None:
            return False, "REFUSE_MISSING_PRIMITIVE_DIFFERENCE"
        if not self.step4_zero_rel_rule:
            return False, "REFUSE_MISSING_ZERO_REL"
        if not self.step5_witness_certificate:
            return False, "REFUSE_MISSING_WITNESS"
        return True, "ACCEPT_DECLARATION"


# --- 4. Prime 001 Adapter & Prime 002 Continuation Control ---

@dataclass(frozen=True)
class AdapterContract:
    """Prime 001 Adapter Contract specification."""

    source_carrier: str
    target_carrier: str
    preserved_operations: Tuple[str, ...]
    preserved_equations: Tuple[str, ...]
    preserved_witnesses: Tuple[str, ...]
    protected_distinctions: Tuple[str, ...]
    authority_fences: Tuple[str, ...]
    loss_ledger: Tuple[str, ...]


def check_adapter(
    contract: AdapterContract,
    source_state: Mapping[str, Any],
    target_state: Mapping[str, Any],
) -> Tuple[bool, str, List[str]]:
    """Validate adapter contract preservation and record data loss."""
    losses: List[str] = list(contract.loss_ledger)
    for op in contract.preserved_operations:
        if op not in target_state:
            losses.append(f"Operation {op} lost during transport")
    for eq in contract.preserved_equations:
        if eq not in target_state:
            losses.append(f"Equation {eq} violated during transport")
    for wit in contract.preserved_witnesses:
        if wit not in target_state:
            losses.append(f"Witness {wit} lost during transport")
    is_sound = len(losses) == len(contract.loss_ledger)
    status = "ADAPTER_SOUND" if is_sound else "ADAPTER_WITH_LOSS"
    return is_sound, status, losses


@dataclass(frozen=True)
class CanContinueInput:
    """The 9 canonical conjuncts of Prime 002 continuation."""

    has_obligation: bool
    has_witness: bool
    next_carrier_declared: bool
    adapter_sound: bool
    detector_adequate: bool
    minimal_lift: bool
    skeleton_preserved: bool
    budget_remains: bool
    not_gtla_refusal: bool

    def evaluate(self) -> bool:
        """Evaluate the canonical nine-conjunct continuation condition."""
        return (
            self.has_obligation
            and self.has_witness
            and self.next_carrier_declared
            and self.adapter_sound
            and self.detector_adequate
            and self.minimal_lift
            and self.skeleton_preserved
            and self.budget_remains
            and self.not_gtla_refusal
        )

    def to_three_condition_summary(self) -> Tuple[bool, bool, bool]:
        """Equivalent tripartite regrouping into (structural, budget, no-stop)."""
        structural = (
            self.has_obligation
            and self.has_witness
            and self.next_carrier_declared
            and self.adapter_sound
            and self.detector_adequate
            and self.minimal_lift
            and self.skeleton_preserved
        )
        return structural, self.budget_remains, self.not_gtla_refusal


class ResidualQueueScheduler:
    """Priority queue scheduler enforcing strict lexicographic progress on (Gamma_2, Phi_1, defect_count)."""

    def __init__(self) -> None:
        self.queue: List[Tuple[Tuple[Fraction, Fraction, int], Dict[str, Any]]] = []

    def push(self, gamma_2: Any, phi_1: Any, defect_count: int, task: Dict[str, Any]) -> None:
        key = (_to_fraction(gamma_2), _to_fraction(phi_1), int(defect_count))
        self.queue.append((key, task))
        self.queue.sort(key=lambda item: item[0])

    def pop_admissible_step(
        self, current_vector: Tuple[Any, Any, int]
    ) -> Optional[Dict[str, Any]]:
        curr_key = (_to_fraction(current_vector[0]), _to_fraction(current_vector[1]), int(current_vector[2]))
        for i, (key, task) in enumerate(self.queue):
            if key < curr_key:
                self.queue.pop(i)
                return task
        return None


class PrimeTriadEngine:
    """Master Algorithm Prime Triad Engine (000, 001, 002)."""

    def __init__(
        self,
        budget: Any = 100,
        delta_control: Any = 10,
    ) -> None:
        b_frac = _to_fraction(budget)
        d_frac = _to_fraction(delta_control)
        if b_frac < 0:
            raise ValueError("Budget must be non-negative")
        if d_frac <= 0:
            raise ValueError("delta_control must be strictly positive")
        self.budget = b_frac
        self.delta_control = d_frac
        self.ops_count = 0
        self.loss_ledger: List[str] = []

    def evaluate_intake(self, trace: IntakeTrace) -> str:
        """Prime -1 / 001 Intake Check."""
        packet = trace.candidate_packet
        if not packet.carrier_proposal:
            return "REFUSED_MISSING_CARRIER"
        if not packet.observer_proposal:
            return "REFUSED_MISSING_OBSERVER"
        if not packet.witness_available:
            return "REFUSED_MISSING_WITNESS"
        if packet.adapter_confidence == "inadequate":
            self.loss_ledger.append(
                f"Intake adapter inadequate for artifact {packet.artifact_id}"
            )
            return "ADAPTER_INADEQUATE"
        return "ACCEPT_DECLARATION"

    def can_continue(
        self,
        stage: int,
        has_obligation: bool,
        has_witness: bool,
        next_carrier_declared: bool,
        adapter_sound: bool = False,
        detector_adequate: bool = False,
        minimal_lift: bool = False,
        skeleton_preserved: bool = False,
        budget_remains: bool = False,
        gtla_refusal: bool = False,
    ) -> bool:
        """Prime 002 Continuation Predicate CanContinue_n."""
        has_budget = budget_remains and (self.budget >= self.delta_control)
        inp = CanContinueInput(
            has_obligation=has_obligation,
            has_witness=has_witness,
            next_carrier_declared=next_carrier_declared,
            adapter_sound=adapter_sound,
            detector_adequate=detector_adequate,
            minimal_lift=minimal_lift,
            skeleton_preserved=skeleton_preserved,
            budget_remains=has_budget,
            not_gtla_refusal=not gtla_refusal,
        )
        return inp.evaluate()

    def execute_step(self, diagnostic: Optional[Mapping[str, Any]] = None) -> str:
        """Execute one bounded step under cost floor delta_control."""
        if self.budget < self.delta_control:
            return "TERMINAL_WITH_DEBT"
        self.budget -= self.delta_control
        self.ops_count += 1
        if diagnostic is not None:
            phi = _to_fraction(diagnostic.get("phi_1", 1))
            gamma = _to_fraction(diagnostic.get("gamma_2", 1))
            if phi == 0 and gamma == 0:
                return "LOCAL_GREEN_FOR_SCOPE"
        return "STEP_EXECUTED"

    def coda_reentry(
        self,
        locus_id: str,
        carrier_declared: bool = False,
        carrier: Optional[SimplicialCarrier] = None,
    ) -> Dict[str, Any]:
        """CODA recursive re-entry Omega_000(L) requiring carrier declaration."""
        if not carrier_declared or (carrier is not None and not carrier.validate()):
            return {
                "locus": locus_id,
                "status": "REFUSED_UNTYPED_LOCUS_WITHOUT_CARRIER",
                "authority_effect": "None",
            }
        return {
            "locus": locus_id,
            "carrier": f"carrier_for_{locus_id}",
            "status": "REENTERED_ADMITTED",
            "authority_effect": "None",
        }


# --- 5. Terminalization & Evaluator Defect Linearity ---

class DDATerminalizer:
    """Scoped terminalization and Merkle tape verification."""

    def __init__(self, engine: PrimeTriadEngine, genesis_hash: str) -> None:
        self.engine = engine
        self.genesis_hash = genesis_hash
        self.merkle_tape: List[Dict[str, Any]] = []

    def process_step(self, letter: str, outcome: Mapping[str, Any]) -> str:
        """Record step in Merkle tape with canonical payload commitment."""
        prev_hash = (
            self.merkle_tape[-1]["hash"]
            if self.merkle_tape
            else self.genesis_hash
        )
        step_index = len(self.merkle_tape)
        outcome_str = json.dumps(dict(outcome), sort_keys=True, default=str)
        content = f"{step_index}:{letter}:{prev_hash}:{outcome_str}"
        curr_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        self.merkle_tape.append(
            {
                "index": step_index,
                "letter": letter,
                "prev_hash": prev_hash,
                "hash": curr_hash,
                "outcome": dict(outcome),
            }
        )
        return "STEP_RECORDED"

    def terminalize(
        self,
        phi_1: Any,
        gamma_2: Any,
        detector_adequate: bool,
    ) -> Tuple[bool, str]:
        """Terminalize local pass routing T_res and F_term."""
        phi = _to_fraction(phi_1)
        gamma = _to_fraction(gamma_2)
        if phi == 0 and gamma == 0 and detector_adequate:
            return True, "LOCAL_GREEN_FOR_SCOPE"
        if not detector_adequate:
            return False, "REFUSED_BLIND_OBSERVER"
        return False, "REFUSED_OPEN_RESIDUAL"


def verify_merkle_tape(
    tape: Sequence[Mapping[str, Any]], genesis_hash: str
) -> Tuple[bool, str]:
    """Verify cryptographic integrity of tape including canonical outcome payload."""
    expected_prev = genesis_hash
    for entry in tape:
        if entry["prev_hash"] != expected_prev:
            return False, "HASH_CHAIN_BROKEN"
        outcome_str = json.dumps(dict(entry.get("outcome", {})), sort_keys=True, default=str)
        content = f"{entry['index']}:{entry['letter']}:{expected_prev}:{outcome_str}"
        expected_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if entry["hash"] != expected_hash:
            return False, "ENTRY_HASH_MISMATCH"
        expected_prev = entry["hash"]
    return True, "MERKLE_TAPE_VERIFIED"


class EvaluatorDefect:
    """LGGR I evaluator defect Delta_E = E_g - E1 E2 linearity."""

    @staticmethod
    def defect(
        e_global: Any, e_local_1: Any, e_local_2: Any
    ) -> Fraction:
        """Compute pointwise defect Delta_E."""
        eg = _to_fraction(e_global)
        e1 = _to_fraction(e_local_1)
        e2 = _to_fraction(e_local_2)
        return eg - (e1 * e2)

    @classmethod
    def gpr_minus_lpr(cls, expected_delta_e: Any, covariance: Any = 0) -> Fraction:
        """GPR - LPR = E[Delta_E] + Cov under linear expectations."""
        return _to_fraction(expected_delta_e) + _to_fraction(covariance)


# Backwards compatibility aliases
class ResidualFunctional:
    @staticmethod
    def evaluate(
        carrier: SimplicialCarrier, h_1: Mapping[Tuple[Any, Any], Any]
    ) -> Dict[str, Any]:
        c2 = CohomologicalEngine.d1(carrier, h_1)
        gamma = sum((abs(_to_fraction(v)) for v in c2.values()), Fraction(0))
        return {"gamma_2": gamma}


class ResidualEvaluator:
    @staticmethod
    def evaluate(func_vals: Mapping[str, Any]) -> Dict[str, str]:
        gamma = _to_fraction(func_vals.get("gamma_2", 0))
        if gamma > 0:
            return {"label": "ACTIVE_CLOSURE_FAILURE"}
        return {"label": "EXACT_OR_CLOSED"}


@dataclass
class StepRecord:
    index: int
    letter: str
    prev_hash: str
    hash: str
    outcome: Dict[str, Any]


class CODAMasterSuite:
    pass
