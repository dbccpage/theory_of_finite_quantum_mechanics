"""
Smith Normal Form (SNF) & Torsion Homology Engine
Exact integer decomposition S = P * B * Q over Z, computing Betti numbers and torsion coefficients.
AuthorityEffect: None
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class SNFReceipt:
    """Certified result of integer Smith Normal Form decomposition S = P * B * Q."""

    S: List[List[int]]
    P: List[List[int]]
    Q: List[List[int]]
    invariant_factors: List[int]
    rank: int
    is_valid_decomposition: bool
    divisibility_satisfied: bool
    det_P: int
    det_Q: int
    authority_effect: str = "None"


@dataclass
class HomologyReceipt:
    """Certified integral homology group H_k(K; Z) decomposition."""

    dimension: int
    n_k: int
    rank_k: int
    rank_k_plus_1: int
    betti_number: int
    torsion_coefficients: List[int]
    homology_group_str: str
    authority_effect: str = "None"


def _mat_mul(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """Exact integer matrix multiplication."""
    if not A or not B:
        return []
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for p in range(k):
            if A[i][p] != 0:
                for j in range(n):
                    C[i][j] += A[i][p] * B[p][j]
    return C


def _det_bareiss(M: List[List[int]]) -> int:
    """Exact integer determinant via Bareiss fraction-free algorithm."""
    n = len(M)
    if n == 0:
        return 1
    if any(len(row) != n for row in M):
        raise ValueError("Matrix must be square to compute determinant.")
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]

    A = [row[:] for row in M]
    sign = 1
    prev_pivot = 1

    for k in range(n - 1):
        # Pivot selection
        pivot = A[k][k]
        if pivot == 0:
            swap_row = -1
            for r in range(k + 1, n):
                if A[r][k] != 0:
                    swap_row = r
                    break
            if swap_row == -1:
                return 0
            A[k], A[swap_row] = A[swap_row], A[k]
            sign = -sign
            pivot = A[k][k]

        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = pivot * A[i][j] - A[i][k] * A[k][j]
                assert num % prev_pivot == 0, "Bareiss division remainder non-zero"
                A[i][j] = num // prev_pivot

        prev_pivot = pivot

    return sign * A[n - 1][n - 1]


class SmithNormalForm:
    """
    Computes exact Smith Normal Form (SNF) of an m x n integer matrix B over Z:
    S = P * B * Q
    where P in GL_m(Z), Q in GL_n(Z), and S is diagonal with d_1 | d_2 | ... | d_r.
    """

    @staticmethod
    def decompose(matrix: List[List[int]]) -> SNFReceipt:
        m = len(matrix)
        n = len(matrix[0]) if m > 0 else 0

        if m == 0 or n == 0:
            return SNFReceipt(
                S=[[0] * n for _ in range(m)],
                P=[[1 if i == j else 0 for j in range(m)] for i in range(m)],
                Q=[[1 if i == j else 0 for j in range(n)] for i in range(n)],
                invariant_factors=[],
                rank=0,
                is_valid_decomposition=True,
                divisibility_satisfied=True,
                det_P=1,
                det_Q=1,
            )

        A = [row[:] for row in matrix]
        P = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
        Q = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

        def row_swap(r1: int, r2: int) -> None:
            if r1 == r2:
                return
            A[r1], A[r2] = A[r2], A[r1]
            P[r1], P[r2] = P[r2], P[r1]

        def col_swap(c1: int, c2: int) -> None:
            if c1 == c2:
                return
            for r in range(m):
                A[r][c1], A[r][c2] = A[r][c2], A[r][c1]
            for r in range(n):
                Q[r][c1], Q[r][c2] = Q[r][c2], Q[r][c1]

        def row_add(r_dst: int, r_src: int, c: int) -> None:
            if c == 0:
                return
            for j in range(n):
                A[r_dst][j] += c * A[r_src][j]
            for j in range(m):
                P[r_dst][j] += c * P[r_src][j]

        def col_add(c_dst: int, c_src: int, c: int) -> None:
            if c == 0:
                return
            for r in range(m):
                A[r][c_dst] += c * A[r][c_src]
            for r in range(n):
                Q[r][c_dst] += c * Q[r][c_src]

        def row_scale(r: int, s: int) -> None:
            for j in range(n):
                A[r][j] *= s
            for j in range(m):
                P[r][j] *= s

        diag_limit = min(m, n)
        for k in range(diag_limit):
            while True:
                # 1. Pivot selection: minimum non-zero absolute value in submatrix [k..m-1, k..n-1]
                min_val = None
                piv_r, piv_c = None, None
                for r in range(k, m):
                    for c in range(k, n):
                        val = abs(A[r][c])
                        if val != 0 and (min_val is None or val < min_val):
                            min_val = val
                            piv_r, piv_c = r, c

                if min_val is None:
                    # Rest of submatrix is identically zero
                    break

                row_swap(k, piv_r)
                col_swap(k, piv_c)

                # 2. Row reduction
                restarted = False
                for r in range(k + 1, m):
                    if A[r][k] != 0:
                        q = A[r][k] // A[k][k]
                        row_add(r, k, -q)
                        if A[r][k] != 0:
                            restarted = True
                            break
                if restarted:
                    continue

                # 3. Column reduction
                for c in range(k + 1, n):
                    if A[k][c] != 0:
                        q = A[k][c] // A[k][k]
                        col_add(c, k, -q)
                        if A[k][c] != 0:
                            restarted = True
                            break
                if restarted:
                    continue

                # Verify entries in col k and row k are zeroed
                if any(A[r][k] != 0 for r in range(k + 1, m)) or any(
                    A[k][c] != 0 for c in range(k + 1, n)
                ):
                    continue

                # 4. Divisibility check: A[k][k] must divide all entries in submatrix
                div_failed = False
                for r in range(k + 1, m):
                    for c in range(k + 1, n):
                        if A[r][c] % A[k][k] != 0:
                            row_add(k, r, 1)
                            div_failed = True
                            break
                    if div_failed:
                        break
                if div_failed:
                    continue

                # Finished with pivot at (k, k)
                break

            # Ensure non-negative diagonal entry
            if k < diag_limit and A[k][k] < 0:
                row_scale(k, -1)

        # Collect invariant factors
        factors = []
        for i in range(diag_limit):
            if A[i][i] != 0:
                factors.append(A[i][i])

        # Verify divisibility law: d_i | d_{i+1}
        divisibility_satisfied = True
        for i in range(len(factors) - 1):
            if factors[i + 1] % factors[i] != 0:
                divisibility_satisfied = False

        # Verify identity: P * matrix * Q == A (which is S)
        prod = _mat_mul(_mat_mul(P, matrix), Q)
        is_valid_decomposition = prod == A

        det_P = _det_bareiss(P)
        det_Q = _det_bareiss(Q)
        assert abs(det_P) == 1, f"Unimodular P violation: det(P) = {det_P}"
        assert abs(det_Q) == 1, f"Unimodular Q violation: det(Q) = {det_Q}"

        return SNFReceipt(
            S=A,
            P=P,
            Q=Q,
            invariant_factors=factors,
            rank=len(factors),
            is_valid_decomposition=is_valid_decomposition,
            divisibility_satisfied=divisibility_satisfied,
            det_P=det_P,
            det_Q=det_Q,
        )

    @classmethod
    def compute_homology(
        cls,
        B_k: Optional[List[List[int]]],
        B_k_plus_1: Optional[List[List[int]]],
        n_k: int,
        dim: int = 0,
    ) -> HomologyReceipt:
        """
        Computes integral homology H_k(K; Z) = ker(d_k) / im(d_{k+1}).
        B_k: boundary matrix d_k : C_k -> C_{k-1} (dimension n_{k-1} x n_k)
        B_k_plus_1: boundary matrix d_{k+1} : C_{k+1} -> C_k (dimension n_k x n_{k+1})
        """
        if B_k is not None and len(B_k) > 0 and len(B_k[0]) > 0:
            receipt_k = cls.decompose(B_k)
            rank_k = receipt_k.rank
        else:
            rank_k = 0

        if B_k_plus_1 is not None and len(B_k_plus_1) > 0 and len(B_k_plus_1[0]) > 0:
            receipt_k_plus_1 = cls.decompose(B_k_plus_1)
            rank_k_plus_1 = receipt_k_plus_1.rank
            torsion = [d for d in receipt_k_plus_1.invariant_factors if d > 1]
        else:
            rank_k_plus_1 = 0
            torsion = []

        betti = n_k - rank_k - rank_k_plus_1
        assert betti >= 0, (
            f"Negative Betti number encountered: {betti} (n_k={n_k}, r_k={rank_k}, r_{k + 1}={rank_k_plus_1})"
        )

        # Format string description
        parts = []
        if betti > 0:
            parts.append(f"Z^{betti}" if betti > 1 else "Z")
        for t in torsion:
            parts.append(f"Z/{t}Z")
        group_str = " (+) ".join(parts) if parts else "0"

        return HomologyReceipt(
            dimension=dim,
            n_k=n_k,
            rank_k=rank_k,
            rank_k_plus_1=rank_k_plus_1,
            betti_number=betti,
            torsion_coefficients=torsion,
            homology_group_str=group_str,
        )


def build_rp2_complex() -> Tuple[List[int], List[List[int]], List[List[int]]]:
    """Minimal 6-vertex triangulation of real projective plane RP^2."""
    triangles = [
        (0, 1, 2),
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 0),
        (4, 0, 1),
        (0, 2, 5),
        (2, 4, 5),
        (4, 1, 5),
        (1, 3, 5),
        (3, 0, 5),
    ]
    edges = sorted(
        list(
            set(
                (min(u, v), max(u, v))
                for u, v, w in triangles
                for (u, v) in [(u, v), (u, w), (v, w)]
            )
        )
    )
    edge_map = {e: i for i, e in enumerate(edges)}

    d1 = [[0] * 15 for _ in range(6)]
    for j, (u, v) in enumerate(edges):
        d1[v][j] += 1
        d1[u][j] -= 1

    d2 = [[0] * 10 for _ in range(15)]
    for j, (u, v, w) in enumerate(triangles):
        for a, b in [(v, w), (w, u), (u, v)]:
            e = (min(a, b), max(a, b))
            sgn = 1 if a < b else -1
            d2[edge_map[e]][j] += sgn

    return [6, 15, 10], d1, d2


def build_klein_bottle_complex() -> Tuple[List[int], List[List[int]], List[List[int]]]:
    """3x4 grid triangulation of Klein Bottle: 12 vertices, 36 edges, 24 triangles."""
    nx, ny = 3, 4

    def v(x: int, y: int) -> Tuple[int, int]:
        x = x % nx
        if y >= ny:
            return ((nx - (x % nx)) % nx, 0)
        return (x, y % ny)

    triangles = []
    for x in range(nx):
        for y in range(ny):
            v00 = v(x, y)
            v10 = v(x + 1, y)
            v01 = v(x, y + 1)
            v11 = v(x + 1, y + 1)
            triangles.append((v00, v10, v11))
            triangles.append((v00, v11, v01))

    verts = sorted(list(set(vert for t in triangles for vert in t)))
    vert_map = {vert: i for i, vert in enumerate(verts)}

    edges = set()
    for u, w, z in triangles:
        edges.add((min(vert_map[u], vert_map[w]), max(vert_map[u], vert_map[w])))
        edges.add((min(vert_map[u], vert_map[z]), max(vert_map[u], vert_map[z])))
        edges.add((min(vert_map[w], vert_map[z]), max(vert_map[w], vert_map[z])))
    edge_list = sorted(list(edges))
    edge_map = {e: i for i, e in enumerate(edge_list)}

    d1 = [[0] * len(edge_list) for _ in range(len(verts))]
    for j, (u, w) in enumerate(edge_list):
        d1[w][j] += 1
        d1[u][j] -= 1

    d2 = [[0] * len(triangles) for _ in range(len(edge_list))]
    for j, (u, w, z) in enumerate(triangles):
        iu, iw, iz = vert_map[u], vert_map[w], vert_map[z]
        for a, b in [(iw, iz), (iz, iu), (iu, iw)]:
            e = (min(a, b), max(a, b))
            sgn = 1 if a < b else -1
            d2[edge_map[e]][j] += sgn

    return [len(verts), len(edge_list), len(triangles)], d1, d2


def build_sphere_complex() -> Tuple[List[int], List[List[int]], List[List[int]]]:
    """Boundary shell of tetrahedron: S^2 (4 vertices, 6 edges, 4 triangles)."""
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    edge_map = {e: i for i, e in enumerate(edges)}

    d1 = [[0] * 6 for _ in range(4)]
    for j, (u, v) in enumerate(edges):
        d1[v][j] += 1
        d1[u][j] -= 1

    d2 = [[0] * 4 for _ in range(6)]
    # Oriented faces of tetrahedron with consistent outwards orientation
    # d(0,1,2) = (1,2) - (0,2) + (0,1)
    # d(0,3,1) = (3,1) - (0,1) + (0,3) = -(1,3) - (0,1) + (0,3)
    # d(0,2,3) = (2,3) - (0,3) + (0,2)
    # d(1,3,2) = (3,2) - (1,2) + (1,3) = -(2,3) - (1,2) + (1,3)
    # Sum of boundaries: (1,2)-(0,2)+(0,1) - (1,3)-(0,1)+(0,3) + (2,3)-(0,3)+(0,2) - (2,3)-(1,2)+(1,3) = 0!
    oriented_faces = [
        (0, 1, 2, [(1, (1, 2)), (-1, (0, 2)), (1, (0, 1))]),
        (0, 3, 1, [(-1, (1, 3)), (-1, (0, 1)), (1, (0, 3))]),
        (0, 2, 3, [(1, (2, 3)), (-1, (0, 3)), (1, (0, 2))]),
        (1, 3, 2, [(-1, (2, 3)), (-1, (1, 2)), (1, (1, 3))]),
    ]
    for k, (_, _, _, b_spec) in enumerate(oriented_faces):
        for sign, e in b_spec:
            d2[edge_map[e]][k] += sign

    return [4, 6, 4], d1, d2


def build_moore_space_complex(m: int) -> Tuple[List[int], List[List[int]], List[List[int]]]:
    """
    Constructs a 2-complex Moore space M(Z/mZ, 1) having H_1 = Z/mZ and H_2 = 0.
    Built with 1 vertex, 1 edge, and 1 face attached with degree m.
    Matrix d1 = [[0]], d2 = [[m]].
    """
    f_vector = [1, 1, 1]
    d1 = [[0]]
    d2 = [[m]]
    return f_vector, d1, d2
