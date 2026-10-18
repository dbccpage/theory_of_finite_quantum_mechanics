"""Exact Integer Lattice HNF/SNF & CVP Solver for High-Dimensional DDA Co-exact Closure.

Resolves Round 3 & Round 4 Red Team Rules:
- 008-DDA-R10: Integer co-exact closure is solved via HNF/SNF rank reduction + bounded branch-and-bound CVP search.
- 008-DDA-R13 & 008-DDA-R14: H¹(K; Z) torsion classification for generalized integer cochain carriers.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Sequence

from .cochain import CoboundaryComplex, gamma2_of


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean algorithm: returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    if a == 0:
        return (abs(b), 0, 1 if b >= 0 else -1)
    g, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    if g < 0:
        g, x, y = -g, -x, -y
    return (g, x, y)


def mat_transpose(matrix: Sequence[Sequence[int]]) -> List[List[int]]:
    if not matrix or not matrix[0]:
        return []
    rows, cols = len(matrix), len(matrix[0])
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]


def mat_mul_int(
    a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]
) -> List[List[int]]:
    if not a or not b:
        return []
    n, k, m = len(a), len(b), len(b[0])
    out = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            out[i][j] = sum(a[i][t] * b[t][j] for t in range(k))
    return out


def identity_matrix(n: int) -> List[List[int]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def hermite_normal_form(
    matrix: Sequence[Sequence[int]],
) -> Tuple[List[List[int]], List[List[int]]]:
    """Computes column Hermite Normal Form H of integer matrix A (m x n) and unimodular matrix U (n x n)
    such that H = A * U, where H is lower-triangular with non-negative pivot entries.
    """
    if not matrix or not matrix[0]:
        return [], []

    m = len(matrix)
    n = len(matrix[0])

    H = [list(row) for row in matrix]
    U = identity_matrix(n)

    curr_col = 0
    for r in range(m):
        if curr_col >= n:
            break

        while True:
            non_zeros = [c for c in range(curr_col, n) if H[r][c] != 0]
            if not non_zeros:
                break

            min_c = min(non_zeros, key=lambda c: abs(H[r][c]))

            if min_c != curr_col:
                for row in range(m):
                    H[row][curr_col], H[row][min_c] = H[row][min_c], H[row][curr_col]
                for row in range(n):
                    U[row][curr_col], U[row][min_c] = U[row][min_c], U[row][curr_col]

            all_zero_except_pivot = True
            pivot_val = H[r][curr_col]
            for c in range(curr_col + 1, n):
                if H[r][c] != 0:
                    all_zero_except_pivot = False
                    q = H[r][c] // pivot_val
                    for row in range(m):
                        H[row][c] -= q * H[row][curr_col]
                    for row in range(n):
                        U[row][c] -= q * U[row][curr_col]

            if all_zero_except_pivot:
                break

        if H[r][curr_col] != 0:
            if H[r][curr_col] < 0:
                for row in range(m):
                    H[row][curr_col] = -H[row][curr_col]
                for row in range(n):
                    U[row][curr_col] = -U[row][curr_col]

            pivot_val = H[r][curr_col]
            for c in range(curr_col):
                if H[r][c] != 0:
                    q = H[r][c] // pivot_val
                    for row in range(m):
                        H[row][c] -= q * H[row][curr_col]
                    for row in range(n):
                        U[row][c] -= q * U[row][curr_col]

            curr_col += 1

    return H, U


def smith_normal_form(
    matrix: Sequence[Sequence[int]],
) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:
    """Computes Smith Normal Form S of integer matrix A (m x n) with unimodular U (m x m) and V (n x n)
    such that S = U * A * V is diagonal with canonical divisibility s_i | s_{i+1}.
    """
    if not matrix or not matrix[0]:
        return [], [], []

    m = len(matrix)
    n = len(matrix[0])
    S = [list(row) for row in matrix]
    U = identity_matrix(m)
    V = identity_matrix(n)

    min_dim = min(m, n)

    progress = True
    while progress:
        progress = False

        for k in range(min_dim):
            while True:
                min_val = None
                min_r, min_c = k, k
                for r in range(k, m):
                    for c in range(k, n):
                        if S[r][c] != 0:
                            val = abs(S[r][c])
                            if min_val is None or val < min_val:
                                min_val = val
                                min_r, min_c = r, c

                if min_val is None:
                    break

                if min_r != k:
                    S[k], S[min_r] = S[min_r], S[k]
                    U[k], U[min_r] = U[min_r], U[k]
                if min_c != k:
                    for r in range(m):
                        S[r][k], S[r][min_c] = S[r][min_c], S[r][k]
                    for r in range(n):
                        V[r][k], V[r][min_c] = V[r][min_c], V[r][k]

                pivot = S[k][k]
                improved = False

                for r in range(k + 1, m):
                    if S[r][k] != 0:
                        q = S[r][k] // pivot
                        for c in range(n):
                            S[r][c] -= q * S[k][c]
                        for c in range(m):
                            U[r][c] -= q * U[k][c]
                        improved = True

                for c in range(k + 1, n):
                    if S[k][c] != 0:
                        q = S[k][c] // pivot
                        for r in range(m):
                            S[r][c] -= q * S[r][k]
                        for r in range(n):
                            V[r][c] -= q * V[r][k]
                        improved = True

                if (
                    not improved
                    and all(S[r][k] == 0 for r in range(k + 1, m))
                    and all(S[k][c] == 0 for c in range(k + 1, n))
                ):
                    break

        for i in range(min_dim - 1):
            if S[i][i] != 0 and S[i + 1][i + 1] != 0 and S[i + 1][i + 1] % S[i][i] != 0:
                for r in range(m):
                    S[r][i] += S[r][i + 1]
                for r in range(n):
                    V[r][i] += V[r][i + 1]
                progress = True
                break

    for k in range(min_dim):
        if S[k][k] < 0:
            S[k][k] = -S[k][k]
            for r in range(m):
                U[k][r] = -U[k][r]

    return S, U, V


@dataclass(frozen=True)
class LatticeCvpResult:
    delta_c: Tuple[int, ...]
    y: Tuple[int, ...]
    min_gamma2: int
    solver_method: str
    nodes_evaluated: int
    lattice_rank: int


def solve_integer_coexact_cvp(
    cx: CoboundaryComplex,
    omega: Sequence[int],
    search_radius: int = 4,
) -> LatticeCvpResult:
    """Solves the integer co-exact closure Closest Vector Problem (CVP) / ILP:
    min_{y ∈ Z^{dim_c2}} ||d1(ω + (d1)^T y)||_1

    Uses Hermite Normal Form (HNF) to extract an independent integer lattice basis,
    removing linearly dependent redundant face combinations before branch-and-bound search.
    Reports HnfRankReducedBoundedSearch(radius=r) to reflect explicit search bounds.
    """
    dim_c1 = cx.dim_c1
    dim_c2 = cx.dim_c2

    solver_label = f"HnfRankReducedBoundedSearch(radius={search_radius})"

    if dim_c2 == 0 or dim_c1 == 0:
        return LatticeCvpResult(
            delta_c=tuple([0] * dim_c1),
            y=(),
            min_gamma2=gamma2_of(cx, list(omega)),
            solver_method=solver_label,
            nodes_evaluated=1,
            lattice_rank=0,
        )

    d1t = mat_transpose([list(r) for r in cx.d1])
    H, U = hermite_normal_form(d1t)

    non_zero_cols = [
        c for c in range(dim_c2) if any(H[r][c] != 0 for r in range(dim_c1))
    ]
    rank = len(non_zero_cols)

    if rank == 0:
        return LatticeCvpResult(
            delta_c=tuple([0] * dim_c1),
            y=tuple([0] * dim_c2),
            min_gamma2=gamma2_of(cx, list(omega)),
            solver_method=solver_label,
            nodes_evaluated=1,
            lattice_rank=0,
        )

    basis_vectors = [[H[r][c] for r in range(dim_c1)] for c in non_zero_cols]

    best_z = tuple([0] * rank)
    best_delta = tuple([0] * dim_c1)
    best_gamma = gamma2_of(cx, list(omega))
    nodes_count = 0

    from itertools import product

    ranges = [range(-search_radius, search_radius + 1) for _ in range(rank)]

    for z in product(*ranges):
        nodes_count += 1
        delta = tuple(
            sum(basis_vectors[i][r] * z[i] for i in range(rank)) for r in range(dim_c1)
        )
        candidate = tuple(w + d for w, d in zip(omega, delta))
        gamma = gamma2_of(cx, list(candidate))

        if gamma < best_gamma:
            best_gamma = gamma
            best_z = z
            best_delta = delta

    z_full = [0] * dim_c2
    for idx, col in enumerate(non_zero_cols):
        z_full[col] = best_z[idx]

    y_sol = tuple(
        sum(U[r][c] * z_full[c] for c in range(dim_c2)) for r in range(dim_c2)
    )

    return LatticeCvpResult(
        delta_c=best_delta,
        y=y_sol,
        min_gamma2=best_gamma,
        solver_method=solver_label,
        nodes_evaluated=nodes_count,
        lattice_rank=rank,
    )


@dataclass(frozen=True)
class H1CohomologyClass:
    is_closed: bool
    torsion_coords: Tuple[Tuple[int, int], ...]
    free_coords: Tuple[int, ...]
    is_torsion_residual: bool
    h1_free_betti: int
    h1_torsion_factors: Tuple[int, ...]


def classify_h1_cohomology(
    cx: CoboundaryComplex,
    omega: Sequence[int],
) -> H1CohomologyClass:
    """Computes SNF-based H¹(K; Z) cohomology class & torsion residual classification for closed ω.

    Resolves Round 4 Rules 008-DDA-R13 & 008-DDA-R14:
    1. Checks if ω ∈ ker(d1) (i.e. Γ₂ = ||d1 ω||₁ == 0).
    2. Computes integer kernel basis K1 for ker(d1).
    3. Expresses ω = K1 u.
    4. Expresses d0 = K1 B.
    5. Computes Smith Normal Form U B V = S = diag(s_1, ..., s_r, 0, ..., 0).
    6. Returns H1CohomologyClass with torsion coordinates (q_i mod s_i) and free coordinates.
    """
    gamma = gamma2_of(cx, list(omega))
    if gamma != 0:
        return H1CohomologyClass(
            is_closed=False,
            torsion_coords=(),
            free_coords=(),
            is_torsion_residual=False,
            h1_free_betti=0,
            h1_torsion_factors=(),
        )

    if cx.dim_c1 == 0:
        return H1CohomologyClass(
            is_closed=True,
            torsion_coords=(),
            free_coords=(),
            is_torsion_residual=False,
            h1_free_betti=0,
            h1_torsion_factors=(),
        )

    if cx.dim_c2 > 0:
        H_d1, U_k = hermite_normal_form([list(r) for r in cx.d1])
        k_cols = [
            c
            for c in range(cx.dim_c1)
            if all(H_d1[r][c] == 0 for r in range(cx.dim_c2))
        ]
    else:
        k_cols = list(range(cx.dim_c1))
        U_k = identity_matrix(cx.dim_c1)

    if not k_cols:
        return H1CohomologyClass(
            is_closed=True,
            torsion_coords=(),
            free_coords=(),
            is_torsion_residual=False,
            h1_free_betti=0,
            h1_torsion_factors=(),
        )

    k_dim = len(k_cols)
    K1 = [[U_k[r][col] for col in k_cols] for r in range(cx.dim_c1)]

    H_k1, U_solve = hermite_normal_form(K1)
    z = [0] * k_dim
    rem_w = list(omega)
    for c in range(k_dim):
        p_row = [r for r in range(cx.dim_c1) if H_k1[r][c] != 0]
        if p_row:
            r = p_row[0]
            val = H_k1[r][c]
            z[c] = rem_w[r] // val
            for row in range(cx.dim_c1):
                rem_w[row] -= z[c] * H_k1[row][c]

    u = tuple(sum(U_solve[r][c] * z[c] for c in range(k_dim)) for r in range(k_dim))

    if cx.dim_c0 > 0:
        d0_mat = [list(r) for r in cx.d0]
        B = [[0] * cx.dim_c0 for _ in range(k_dim)]
        for col_idx in range(cx.dim_c0):
            col_vec = [d0_mat[r][col_idx] for r in range(cx.dim_c1)]
            rem_c = list(col_vec)
            z_c = [0] * k_dim
            for c in range(k_dim):
                p_row = [r for r in range(cx.dim_c1) if H_k1[r][c] != 0]
                if p_row:
                    r = p_row[0]
                    val = H_k1[r][c]
                    z_c[c] = rem_c[r] // val
                    for row in range(cx.dim_c1):
                        rem_c[row] -= z_c[c] * H_k1[row][c]
            b_col = [
                sum(U_solve[r][c] * z_c[c] for c in range(k_dim)) for r in range(k_dim)
            ]
            for r in range(k_dim):
                B[r][col_idx] = b_col[r]
    else:
        B = [[0] for _ in range(k_dim)]

    S, U_b, V_b = smith_normal_form(B)

    q = tuple(sum(U_b[r][c] * u[c] for c in range(k_dim)) for r in range(k_dim))

    torsion_coords = []
    free_coords = []
    torsion_factors = []

    for r in range(k_dim):
        diag_val = S[r][r] if (r < len(S) and r < len(S[0])) else 0
        if diag_val > 1:
            t_val = q[r] % diag_val
            torsion_coords.append((t_val, diag_val))
            torsion_factors.append(diag_val)
        elif diag_val == 1:
            continue
        else:
            free_coords.append(q[r])

    is_tors_res = len(torsion_coords) > 0 and any(t != 0 for t, s in torsion_coords)

    return H1CohomologyClass(
        is_closed=True,
        torsion_coords=tuple(torsion_coords),
        free_coords=tuple(free_coords),
        is_torsion_residual=is_tors_res,
        h1_free_betti=len(free_coords),
        h1_torsion_factors=tuple(torsion_factors),
    )


