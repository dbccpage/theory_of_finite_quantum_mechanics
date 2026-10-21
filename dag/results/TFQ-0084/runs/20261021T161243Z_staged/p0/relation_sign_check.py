"""Exact (Fraction) finite-carrier check of relation candidates mined at P0 for TFQ-0084.

This is mining evidence for the operad record, not a certificate for the target. It takes no
square roots: every relation is checked through squares and signs over Q on integer-coordinate
simplices, so it exercises exactly the field-free part that a P1 polynomial identity must use.

R_CM  : det(B_sigma) = (-1)^(n+1) * 2^n * (n!)^2 * V_sigma^2 for the bordered Cayley-Menger matrix
        B_sigma of an n-simplex (vertex rows/columns 1..n+1, border row/column 0).
R_COF : C_ii = c_n * V_i^2 with c_n = (-1)^n * 2^(n-1) * ((n-1)!)^2, where C is the cofactor matrix of
        B_sigma and V_i the (n-1)-volume of the facet opposite vertex i.
R_COS : cos(theta_ij) = -C_ij / (c_n * V_i * V_j), theta_ij the interior dihedral angle between the
        facets opposite vertices i and j (i.e. at the hinge spanned by the other n-1 vertices).
        NOTE: the naive form -C_ij/sqrt(C_ii*C_jj) is correct only when c_n > 0 (even n); for odd n
        the sign flips. The c_n form is dimension-uniform.
R_SIN : sin(theta_h) = (n/(n-1)) * V_sigma * A_h / (V_a * V_b), hinge h = facet_a cap facet_b, checked as
        sin^2 + cos^2 = 1 exactly.
Coordinate truth for cos(theta_ij) is -(o_i . o_j)/(|o_i||o_j|) with o_i the outward facet normals built
from the dual basis of the edge Gram matrix; only its square and sign are compared.
"""
from fractions import Fraction as F
from itertools import combinations
from math import factorial


def det(m):
    m = [row[:] for row in m]
    n = len(m)
    d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            if f:
                m[r] = [a - f * b for a, b in zip(m[r], m[c])]
    return d


def sqdist(p, q):
    return sum((a - b) ** 2 for a, b in zip(p, q))


def cm_matrix(pts):
    k = len(pts)
    B = [[F(0)] * (k + 1) for _ in range(k + 1)]
    for i in range(k):
        B[0][i + 1] = B[i + 1][0] = F(1)
        for j in range(k):
            B[i + 1][j + 1] = F(sqdist(pts[i], pts[j]))
    return B


def minor(m, r, c):
    return det([row[:c] + row[c + 1:] for i, row in enumerate(m) if i != r])


def vol2(pts):
    """Squared m-volume of an m-simplex via R_CM."""
    m = len(pts) - 1
    return det(cm_matrix(pts)) / ((-1) ** (m + 1) * 2 ** m * factorial(m) ** 2)


def inv(m):
    n = len(m)
    a = [row[:] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(m)]
    for c in range(n):
        p = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [x / piv for x in a[c]]
        for r in range(n):
            if r != c and a[r][c]:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [row[n:] for row in a]


def outward_normals(pts):
    """Unnormalised outward normals o_i of the facet opposite vertex i, exact over Q."""
    n = len(pts) - 1
    E = [[F(pts[k][d] - pts[0][d]) for k in range(1, n + 1)] for d in range(n)]
    G = [[sum(E[d][a] * E[d][b] for d in range(n)) for b in range(n)] for a in range(n)]
    Gi = inv(G)
    w = [[sum(E[d][a] * Gi[a][k] for a in range(n)) for d in range(n)] for k in range(n)]
    o = [[sum(w[k][d] for k in range(n)) for d in range(n)]]
    o += [[-x for x in w[k]] for k in range(n)]
    return o


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sign(x):
    return (x > 0) - (x < 0)


def check(pts, label):
    n = len(pts) - 1
    c_n = (-1) ** n * 2 ** (n - 1) * factorial(n - 1) ** 2
    B = cm_matrix(pts)
    detB = det(B)
    C = [[(-1) ** (i + j) * minor(B, i + 1, j + 1) for j in range(n + 1)] for i in range(n + 1)]
    o = outward_normals(pts)
    V2 = vol2(pts)
    facet_v2 = [vol2([p for k, p in enumerate(pts) if k != i]) for i in range(n + 1)]
    results = {'R_CM': True, 'R_COF': True, 'R_COS': True, 'R_SIN': True}
    if detB != (-1) ** (n + 1) * 2 ** n * factorial(n) ** 2 * V2:
        results['R_CM'] = False
    cos2 = {}
    for i in range(n + 1):
        if C[i][i] != c_n * facet_v2[i]:
            results['R_COF'] = False
            print(label, 'R_COF FAIL at', i, C[i][i], c_n * facet_v2[i])
    for i, j in combinations(range(n + 1), 2):
        cos2_true = dot(o[i], o[j]) ** 2 / (dot(o[i], o[i]) * dot(o[j], o[j]))
        sgn_true = -sign(dot(o[i], o[j]))
        # R_COS through its square and sign: cos = -C_ij/(c_n V_i V_j); (V_i V_j)^2 = C_ii C_jj / c_n^2
        cos2_cm = C[i][j] ** 2 / (C[i][i] * C[j][j])
        sgn_cm = -sign(C[i][j]) * sign(c_n)
        cos2[(i, j)] = cos2_true
        if cos2_true != cos2_cm or sgn_true != sgn_cm:
            results['R_COS'] = False
            print(label, 'R_COS FAIL at', (i, j), cos2_true, cos2_cm, sgn_true, sgn_cm)
        hinge = [p for k, p in enumerate(pts) if k not in (i, j)]
        sin2 = F(n, n - 1) ** 2 * V2 * vol2(hinge) / (facet_v2[i] * facet_v2[j])
        if sin2 + cos2_true != 1:
            results['R_SIN'] = False
            print(label, 'R_SIN FAIL at', (i, j), sin2, cos2_true)
    print(label, '| n =', n, '| det(CM) =', detB, '| V^2 =', V2, '| c_n =', c_n,
          '| cos^2 set =', sorted(set(cos2.values())), '|', results)
    return all(results.values())


CASES = [
    ([(0, 0, 0), (1, 0, 0), (0, 2, 0), (1, 1, 3)], 'tetra-A'),
    ([(0, 0, 0), (2, 0, 0), (0, 3, 0), (0, 0, 5)], 'tetra-right'),
    ([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], 'tetra-regular-lattice'),
    ([(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)], 'tetra-kuhn'),
    ([(0, 0, 0, 0), (1, 0, 0, 0), (0, 2, 0, 0), (1, 1, 3, 0), (1, 2, 1, 4)], 'pentatope-A'),
    ([(0, 0, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0), (1, 1, 1, 0), (1, 1, 1, 1)], 'pentatope-kuhn'),
]
if __name__ == '__main__':
    ok = all(check(pts, label) for pts, label in CASES)
    print('ALL_RELATIONS_HOLD_ON_FINITE_CARRIER' if ok else 'SOME_RELATION_FAILED')
    raise SystemExit(0 if ok else 1)
