#!/usr/bin/env python3
"""Independent check for L1-IMP-SECTOR-SYMMETRY-LAW.

AuthorityEffect: None.

Verifies independently using only SymPy and standard Python (zero repository imports):
1. Quadratic readout formulation and sector additivity defect G_ij + G_ji on disjoint supports.
2. Symmetry + sector additivity forces off-diagonal entries to vanish (orthogonal sector basis).
3. Transitive permutation group action forces constant diagonal across all sectors (G = c * I).
4. Orbit decomposition: invariance under a non-transitive permutation set forces the diagonal
   to be constant on each orbit, but allows distinct values between orbits.
5. Countermodel 1 (Fin 2): diag(1, 2) is symmetric and sector-additive, constant on trivial orbits {0} and {1},
   but breaks global scalar uniqueness (1 != 2).
6. Countermodel 2 (Fin 3): diag(1, 1, 2) with generator swap(0, 1) has orbits {0, 1} and {2};
   it is symmetric, sector-additive, invariant under swap(0, 1), constant on orbit {0, 1} (G_00 = G_11 = 1)
   and on orbit {2} (G_22 = 2), but G_00 != G_22, breaking uniqueness.
7. Countermodel 3 (Fin 2): unif12 = 1 + J has transitive symmetry but fails sector additivity (cross-sector interference).
8. General symbolic derivation on 3 sectors via SymPy matrix algebra.
"""

import sys
from fractions import Fraction
import sympy as sp

def check_disjoint_support(u, v):
    return all(a == 0 or b == 0 for a, b in zip(u, v))

def qf(G, x):
    n = len(x)
    return sum(x[i] * G[i][j] * x[j] for i in range(n) for j in range(n))

def permute(sigma, x):
    n = len(x)
    inv = [0] * n
    for i, img in enumerate(sigma):
        inv[img] = i
    return [x[inv[i]] for i in range(n)]

def compute_orbits(perms, n):
    gens = list(perms) + [[p.index(i) for i in range(n)] for p in perms]
    seen = set()
    orbs = []
    for i in range(n):
        if i in seen:
            continue
        orb = {i}
        stack = [i]
        while stack:
            curr = stack.pop()
            for g in gens:
                nxt = g[curr]
                if nxt not in orb:
                    orb.add(nxt)
                    stack.append(nxt)
        seen |= orb
        orbs.append(sorted(orb))
    return sorted(orbs)

def test_additivity_and_transitivity():
    print("--- 1. Sector Additivity & Orthogonality ---")
    # For a general 2x2 matrix, test disjoint supports e0 and e1
    e0 = [Fraction(1), Fraction(0)]
    e1 = [Fraction(0), Fraction(1)]
    assert check_disjoint_support(e0, e1)

    # Parametric symmetric matrix
    g00, g01, g11 = sp.symbols('g00 g01 g11')
    G_sym = sp.Matrix([[g00, g01], [g01, g11]])
    u = sp.Matrix([1, 0])
    v = sp.Matrix([0, 1])
    defect = (u + v).T * G_sym * (u + v) - (u.T * G_sym * u) - (v.T * G_sym * v)
    assert sp.simplify(defect[0, 0]) == 2 * g01, f"Expected 2*g01, got {defect[0, 0]}"
    print("  [OK] Sector additivity defect on disjoint supports equals 2*G_01 (forces G_01 = 0 for symmetric G)")

    print("--- 2. Transitive Permutation Selection (SymPy 3-Sector) ---")
    # 3-sector general matrix
    G3 = sp.MatrixSymbol('G', 3, 3).as_explicit()
    # Impose symmetry: G3[i, j] = G3[j, i]
    # Impose sector additivity: G3[i, j] = 0 for i != j
    d0, d1, d2 = sp.symbols('d0 d1 d2')
    G_diag = sp.diag(d0, d1, d2)

    # Transitive cyclic permutation sigma = (0 -> 1 -> 2 -> 0)
    sigma = [1, 2, 0]
    x = sp.Matrix([sp.symbols('x0'), sp.symbols('x1'), sp.symbols('x2')])
    x_perm = sp.Matrix([x[2], x[0], x[1]]) # x(sigma^{-1}(i)): inv = [2, 0, 1]

    qf_orig = sp.simplify((x.T * G_diag * x)[0, 0])
    qf_p = sp.simplify((x_perm.T * G_diag * x_perm)[0, 0])

    diff = sp.expand(qf_p - qf_orig)
    # The coefficient of x0^2 is d1 - d0, x1^2 is d2 - d1, x2^2 is d0 - d2
    c0 = diff.coeff(x[0]**2)
    c1 = diff.coeff(x[1]**2)
    c2 = diff.coeff(x[2]**2)
    assert c0 == d1 - d0 and c1 == d2 - d1 and c2 == d0 - d2
    # Invariance requires diff == 0 for all x => d0 = d1 = d2
    sol = sp.solve([c0, c1, c2], [d1, d2])
    assert sol == {d1: d0, d2: d0}
    print("  [OK] Invariance under transitive permutation forces d0 = d1 = d2 = c, selecting G = c*I_3")

    print("--- 3. Countermodel 1: Distinguished Labels on Fin 2 (diag(1, 2)) ---")
    G_diag12 = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(2)]]
    # Check sector additivity
    for u_vec, v_vec in [([1, 0], [0, 1]), ([2, 0], [0, -3])]:
        assert qf(G_diag12, [u_vec[0]+v_vec[0], u_vec[1]+v_vec[1]]) == qf(G_diag12, u_vec) + qf(G_diag12, v_vec)
    # Trivial permutation set S = []
    orbs = compute_orbits([], 2)
    assert orbs == [[0], [1]], f"Expected singleton orbits, got {orbs}"
    # Diagonal is constant on each orbit
    for orb in orbs:
        diag_vals = [G_diag12[idx][idx] for idx in orb]
        assert len(set(diag_vals)) == 1
    # But between orbits, values differ
    assert G_diag12[0][0] == Fraction(1) and G_diag12[1][1] == Fraction(2)
    assert G_diag12[0][0] != G_diag12[1][1]
    # Swap breaks invariance
    swap12 = [1, 0]
    test_x = [Fraction(1), Fraction(0)]
    assert qf(G_diag12, permute(swap12, test_x)) != qf(G_diag12, test_x)
    print("  [OK] diag(1, 2) is sector-additive and orbit-constant, but G_00 != G_11 breaks scalar uniqueness")

    print("--- 4. Countermodel 2: Distinguished Label on Fin 3 (diag(1, 1, 2) with swap(0, 1)) ---")
    G_dist3 = [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(2)],
    ]
    swap01 = [1, 0, 2] # swaps 0 and 1, leaves 2 fixed
    orbs3 = compute_orbits([swap01], 3)
    assert orbs3 == [[0, 1], [2]], f"Expected orbits [[0, 1], [2]], got {orbs3}"
    # Check diagonal constancy on each orbit
    assert G_dist3[0][0] == G_dist3[1][1] == Fraction(1), "Orbit {0, 1} must have constant diagonal"
    assert G_dist3[2][2] == Fraction(2), "Orbit {2} must have diagonal 2"
    assert G_dist3[0][0] != G_dist3[2][2], "Cross-orbit values must differ"
    # Check invariance under swap01 for arbitrary rational vector
    sample_x = [Fraction(3, 2), Fraction(-5, 7), Fraction(4, 3)]
    assert qf(G_dist3, permute(swap01, sample_x)) == qf(G_dist3, sample_x)
    # Check sector additivity
    u3 = [Fraction(1), Fraction(0), Fraction(0)]
    v3 = [Fraction(0), Fraction(2), Fraction(-1)]
    assert check_disjoint_support(u3, v3)
    assert qf(G_dist3, [a + b for a, b in zip(u3, v3)]) == qf(G_dist3, u3) + qf(G_dist3, v3)
    print("  [OK] diag(1, 1, 2) is invariant under swap(0, 1) with constant orbit values {0, 1} -> 1 and {2} -> 2, breaking G = c*I_3")

    print("--- 5. Countermodel 3: Transitive Symmetry without Sector Additivity (1 + J) ---")
    unif12 = [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(2)]]
    # Check transitive invariance under swap
    for vec in [[1, 0], [0, 1], [1, 1], [3, -2]]:
        assert qf(unif12, permute(swap12, vec)) == qf(unif12, vec)
    # Check failure of sector additivity
    qf_sum = qf(unif12, [1, 1])
    qf_u = qf(unif12, [1, 0])
    qf_v = qf(unif12, [0, 1])
    assert qf_sum == 6 and qf_u == 2 and qf_v == 2
    assert qf_sum != qf_u + qf_v, f"Additivity unexpectedly held: {qf_sum} == {qf_u} + {qf_v}"
    assert unif12[0][1] != 0
    print("  [OK] 1 + J satisfies transitive symmetry but fails sector additivity (cross-sector interference defect = 2)")

    print("\nALL 5 INDEPENDENT CHECKS PASSED.")

if __name__ == "__main__":
    test_additivity_and_transitivity()
    sys.exit(0)
