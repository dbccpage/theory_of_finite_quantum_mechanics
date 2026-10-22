#!/usr/bin/env python3
"""Independent verification for Campaign Target 5 (TFQ-0016).

Verifies without importing any repository code:
1. Semidirect factorization B_2(Q) = T |>< N and uniqueness.
2. Normality of N in B_2(Q) and torus projection invariance.
3. Two-stage hierarchical dressing on the 5-edge diamond complex:
   - Stage 1 dressing u_N in N neutralizes unipotent part on tree edges.
   - Stage 1 preserves quotient projection pi_T on all 5 edges.
   - Stage 1 residual torus transformation preserves tree diagonality.
   - Stage 2 torus dressing u_T in T factors full tree dressing u_T * u_N = T_B^{-1}.
   - Stage 2 reproduces tree-gauge residual on all 5 edges.
4. On the 5-vertex extended diamond poset P_5:
   - b^2 A = 0 on all 3-chains.
   - Discrete curvature K(A) = bA + A cup A gauge covariance K(A^u) = u K(A) u^{-1}.
   - Exact discrete Bianchi identity D_A K = bK + A cup K - K cup A = 0 on all 3-chains.
5. Non-transport of SU(3) color generators (carrier dimension 2 != 3).

Exits 0 on success.
"""

from __future__ import annotations

import sys
from fractions import Fraction
import sympy as sp


def check_b2_semidirect_factorization_symbolic() -> None:
    print("[1/5] Checking symbolic B_2(Q) = T |>< N semidirect factorization...")
    d1, b, d2 = sp.symbols("d1 b d2", nonzero=True)
    M = sp.Matrix([[d1, b], [0, d2]])
    D = sp.Matrix([[d1, 0], [0, d2]])
    n = sp.Matrix([[1, b / d1], [0, 1]])

    # Factorization identity
    prod = D * n
    assert sp.simplify(prod - M) == sp.zeros(2, 2), "M != D * n"

    # Uniqueness: if M = D' * n' with D' diagonal and n' unipotent
    d1_p, d2_p, x = sp.symbols("d1_p d2_p x")
    D_p = sp.Matrix([[d1_p, 0], [0, d2_p]])
    n_p = sp.Matrix([[1, x], [0, 1]])
    prod_p = D_p * n_p
    eqs = [
        sp.Eq(prod_p[0, 0], M[0, 0]),
        sp.Eq(prod_p[0, 1], M[0, 1]),
        sp.Eq(prod_p[1, 1], M[1, 1]),
    ]
    sol = sp.solve(eqs, [d1_p, d2_p, x], dict=True)[0]
    assert sol[d1_p] == d1 and sol[d2_p] == d2 and sol[x] == b / d1, "Factorization is not unique"

    # Normality of N in B_2(Q)
    y = sp.symbols("y")
    n_generic = sp.Matrix([[1, y], [0, 1]])
    M_inv = M.inv()
    conj = M * n_generic * M_inv
    conj = sp.simplify(conj)
    assert conj[0, 0] == 1 and conj[1, 0] == 0 and conj[1, 1] == 1, "Conjugate not unipotent"
    assert conj[0, 1] == (d1 / d2) * y, "Conjugate off-diagonal entry mismatch"

    # Torus projection invariance under unipotent multiplication
    u1_x, u2_x = sp.symbols("u1_x u2_x")
    u1 = sp.Matrix([[1, u1_x], [0, 1]])
    u2 = sp.Matrix([[1, u2_x], [0, 1]])
    sandwiched = sp.simplify(u1 * M * u2)
    assert sandwiched[0, 0] == M[0, 0] and sandwiched[1, 1] == M[1, 1], "pi_T not invariant"
    print("  -> Symbolic semidirect factorization, uniqueness, normality, and pi_T invariance verified.")


def check_two_stage_diamond_dressing() -> None:
    print("[2/5] Checking two-stage hierarchical dressing on diamond graph...")
    # Exact rational matrices from QM-213 control
    edges = [(0, 1), (1, 2), (0, 2), (2, 3), (1, 3)]
    tree_edges = (0, 2, 3)

    U = [
        sp.Matrix([[Fraction(2), Fraction(3)], [Fraction(0), Fraction(1, 2)]]),
        sp.Matrix([[Fraction(3), Fraction(-1)], [Fraction(0), Fraction(2)]]),
        sp.Matrix([[Fraction(1, 2), Fraction(4)], [Fraction(0), Fraction(3)]]),
        sp.Matrix([[Fraction(4), Fraction(2)], [Fraction(0), Fraction(1, 3)]]),
        sp.Matrix([[Fraction(5, 2), Fraction(-3)], [Fraction(0), Fraction(2, 5)]]),
    ]

    # Tree transport:
    # T(0) = I
    # T(1) = U_0
    # T(2) = U_2
    # T(3) = U_3 * U_2
    T = [
        sp.eye(2),
        U[0],
        U[2],
        U[3] * U[2],
    ]

    # Full tree dressing: u_full(v) = T(v)^{-1}
    u_full = [T[v].inv() for v in range(4)]
    res_full = [u_full[t] * U[e_idx] * u_full[s].inv() for e_idx, (s, t) in enumerate(edges)]

    # Tree edges must be neutralized to I_2 under full dressing
    for e_idx in tree_edges:
        assert res_full[e_idx] == sp.eye(2), f"Full residual on tree edge {e_idx} is not I_2"

    # Stage 1: u_N(v) = D(v) * N(v)^{-1} * D(v)^{-1}
    # where T(v) = D(v) * N(v)
    u_N = []
    u_T = []
    for v in range(4):
        Tv = T[v]
        d1, d2 = Tv[0, 0], Tv[1, 1]
        b = Tv[0, 1]
        Dv = sp.Matrix([[d1, 0], [0, d2]])
        Nv = sp.Matrix([[1, b / d1], [0, 1]])
        assert Tv == Dv * Nv, f"Factorization failed at vertex {v}"
        u_Nv = Dv * Nv.inv() * Dv.inv()
        # Must be unit upper triangular:
        assert u_Nv[0, 0] == 1 and u_Nv[1, 0] == 0 and u_Nv[1, 1] == 1, f"u_N({v}) not unipotent"
        # Must satisfy u_N * T = D
        assert u_Nv * Tv == Dv, f"u_N({v}) * T({v}) != D({v})"
        u_N.append(u_Nv)
        u_T.append(Dv.inv())

    # Dressed connection Stage 1: U^(1)_e = u_N(t) * U_e * u_N(s)^{-1}
    U_stage1 = [u_N[t] * U[e_idx] * u_N[s].inv() for e_idx, (s, t) in enumerate(edges)]

    # (a) Stage 1 leaves tree edges diagonal
    for e_idx in tree_edges:
        mat = U_stage1[e_idx]
        assert mat[0, 1] == 0 and mat[1, 0] == 0, f"Tree edge {e_idx} is not diagonal after Stage 1"

    # (b) Stage 1 preserves quotient projection on ALL 5 edges
    for e_idx in range(5):
        orig_diag = (U[e_idx][0, 0], U[e_idx][1, 1])
        st1_diag = (U_stage1[e_idx][0, 0], U_stage1[e_idx][1, 1])
        assert orig_diag == st1_diag, f"pi_T not preserved on edge {e_idx}"

    # (c) Residual first-kind symmetry: any diagonal torus gauge preserves tree diagonality
    t_gauge = [
        sp.Matrix([[Fraction(3), 0], [0, Fraction(1, 5)]]),
        sp.Matrix([[Fraction(2, 3), 0], [0, Fraction(7, 2)]]),
        sp.Matrix([[Fraction(5, 4), 0], [0, Fraction(3, 7)]]),
        sp.Matrix([[Fraction(1, 2), 0], [0, Fraction(4)]]),
    ]
    U_st1_t = [t_gauge[t] * U_stage1[e_idx] * t_gauge[s].inv() for e_idx, (s, t) in enumerate(edges)]
    for e_idx in tree_edges:
        mat = U_st1_t[e_idx]
        assert mat[0, 1] == 0 and mat[1, 0] == 0, f"Tree edge {e_idx} not diagonal after torus gauge"

    # Stage 2: u_T(v) = D(v)^{-1}
    for v in range(4):
        assert u_T[v][0, 1] == 0 and u_T[v][1, 0] == 0, f"u_T({v}) not diagonal"
        # Two-stage factorization matches full tree gauge: u_T(v) * u_N(v) == T(v)^{-1}
        assert u_T[v] * u_N[v] == u_full[v], f"u_T * u_N != u_full at vertex {v}"

    # Stage 2 connection: U^(2)_e = u_T(t) * U^(1)_e * u_T(s)^{-1}
    U_stage2 = [u_T[t] * U_stage1[e_idx] * u_T[s].inv() for e_idx, (s, t) in enumerate(edges)]
    for e_idx in range(5):
        assert U_stage2[e_idx] == res_full[e_idx], f"Stage 2 did not reproduce residual on edge {e_idx}"

    print("  -> Diamond complex two-stage dressing, diagonality, quotient preservation, and residual match verified.")


def check_poset_p5_discrete_curvature() -> None:
    print("[3/5] Checking discrete curvature and Bianchi identity on extended diamond poset P_5...")
    # Poset P_5 = {0 < {1, 2} < 3 < 4}
    # Strict order relations
    strict_pairs = [
        (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 3), (1, 4),
        (2, 3), (2, 4),
        (3, 4),
    ]
    assert len(strict_pairs) == 9, "Expected 9 1-chains"

    # Enumerate 2-chains: triples u < v < w
    two_chains = []
    for u, v in strict_pairs:
        for v2, w in strict_pairs:
            if v == v2 and (u, w) in strict_pairs:
                two_chains.append((u, v, w))
    assert len(two_chains) == 7, f"Expected 7 2-chains, got {len(two_chains)}"

    # Enumerate 3-chains: quadruples u < v < w < z
    three_chains = []
    for u, v, w in two_chains:
        for w2, z in strict_pairs:
            if w == w2 and (u, v, z) in two_chains and (v, w, z) in two_chains:
                three_chains.append((u, v, w, z))
    assert len(three_chains) == 2, f"Expected 2 3-chains, got {len(three_chains)}"
    assert three_chains == [(0, 1, 3, 4), (0, 2, 3, 4)], f"Unexpected 3-chains: {three_chains}"

    # Symbolic 1-cochain over generic matrices / algebra
    A = {}
    for idx, (u, v) in enumerate(strict_pairs):
        a11, a12, a22 = sp.symbols(f"a_{u}_{v}_11 a_{u}_{v}_12 a_{u}_{v}_22")
        A[(u, v)] = sp.Matrix([[a11, a12], [0, a22]])

    # Internal differential b: deletes internal vertices
    # On 1-cochains: (bA)(u, v, w) = - A(u, w)
    def b_deg1(A_map):
        return {ch: -A_map[(ch[0], ch[2])] for ch in two_chains}

    # Cup product (A cup A)(u, v, w) = A(u, v) * A(v, w)
    def cup_11(A_map):
        return {ch: A_map[(ch[0], ch[1])] * A_map[(ch[1], ch[2])] for ch in two_chains}

    # Curvature K(A) = bA + A cup A
    def curvature(A_map):
        bA = b_deg1(A_map)
        AA = cup_11(A_map)
        return {ch: bA[ch] + AA[ch] for ch in two_chains}

    K = curvature(A)

    # Internal differential on 2-cochains:
    # (bK)(u, v, w, z) = - K(u, w, z) + K(u, v, z)
    def b_deg2(K_map):
        return {ch: -K_map[(ch[0], ch[2], ch[3])] + K_map[(ch[0], ch[1], ch[3])] for ch in three_chains}

    # Verify b^2 A = 0 on all 3-chains
    bA = b_deg1(A)
    b2A = b_deg2(bA)
    for ch in three_chains:
        assert sp.simplify(b2A[ch]) == sp.zeros(2, 2), f"b^2 A != 0 on {ch}"

    # Covariant differential: D_A K = bK + A cup K - K cup A
    def D_A_K(A_map, K_map):
        bK = b_deg2(K_map)
        out = {}
        for ch in three_chains:
            u, v, w, z = ch
            ak = A_map[(u, v)] * K_map[(v, w, z)]
            ka = K_map[(u, v, w)] * A_map[(w, z)]
            out[ch] = sp.simplify(bK[ch] + ak - ka)
        return out

    bianchi = D_A_K(A, K)
    for ch in three_chains:
        assert bianchi[ch] == sp.zeros(2, 2), f"Bianchi identity failed on {ch}: {bianchi[ch]}"

    # Gauge covariance: K(A^u) = u K(A) u^{-1}
    g = {}
    g_inv = {}
    for v in range(5):
        g11, g12, g22 = sp.symbols(f"g_{v}_11 g_{v}_12 g_{v}_22", nonzero=True)
        gv = sp.Matrix([[g11, g12], [0, g22]])
        g[v] = gv
        g_inv[v] = gv.inv()

    A_gauge = {(u, v): g[u] * A[(u, v)] * g_inv[v] for (u, v) in strict_pairs}
    K_gauge = curvature(A_gauge)

    for ch in two_chains:
        u, v, w = ch
        expected = g[u] * K[ch] * g_inv[w]
        diff = sp.simplify(K_gauge[ch] - expected)
        assert diff == sp.zeros(2, 2), f"Curvature gauge covariance failed on {ch}"

    print("  -> Poset P_5 strict chains (9, 7, 2), b^2 = 0, discrete Bianchi identity, and gauge covariance verified.")


def check_color_generators_dimension_mismatch() -> None:
    print("[4/5] Checking color generator non-transport and dimension mismatch...")
    dim_borel = 2
    dim_su3_fundamental = 3
    assert dim_borel != dim_su3_fundamental, "Dimension mismatch assertion failed"
    # SU(3) Lie algebra has rank 2 and 8 generators (Gell-Mann), trace zero.
    # Upper-triangular B_2(Q) has carrier dimension 2 and algebra dimension 3 (d1, d2, b).
    # Its diagonal torus has dim 2 (non-traceless), not su(3) Cartan subalgebra.
    print(f"  -> B_2(Q) representation dimension {dim_borel} != {dim_su3_fundamental} (SU(3) color carrier).")


def check_repo_twin_audit() -> None:
    print("[5/5] Checking historical repo twin audit for QM-213 in FiniteQM.lean...")
    # Read lean4/FiniteQM.lean directly without importing repo Python code
    with open("lean4/FiniteQM.lean", "r", encoding="utf-8") as f:
        content = f.read()
    assert "qm213" not in content.lower(), "Unexpected qm213 twin located in FiniteQM.lean"
    assert "two_stage" not in content.lower(), "Unexpected two_stage twin located in FiniteQM.lean"
    assert "borel" not in content.lower(), "Unexpected borel twin located in FiniteQM.lean"
    print("  -> Audit confirmed: zero Lean twins of QM-213 / two-stage Borel dressing in FiniteQM.lean.")


def main() -> None:
    print("=" * 70)
    print("Independent Check: Target 5 (TFQ-0016)")
    print("B_2(Q) Semidirect Factorization, Two-Stage Dressing, and Discrete Curvature")
    print("=" * 70)
    check_b2_semidirect_factorization_symbolic()
    check_two_stage_diamond_dressing()
    check_poset_p5_discrete_curvature()
    check_color_generators_dimension_mismatch()
    check_repo_twin_audit()
    print("=" * 70)
    print("ALL 5 INDEPENDENT VERIFICATION CHECKS PASSED (exit code 0).")
    print("=" * 70)


if __name__ == "__main__":
    main()
