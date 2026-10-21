"""Finite-carrier check (exact, over Q) of the P0 composition plan that makes T1 arccos-free, plus the
exact T4 near-miss evaluation on integer-edge tetrahedra.

Composition plan (P0, M2): with C the cofactor matrix of the bordered Cayley-Menger matrix of an
n-simplex in the squared edge lengths x, c_n = (-1)^n 2^(n-1) ((n-1)!)^2, and h = (a, b) the hinge
shared by the facets opposite vertices a and b:

  R_SIN  :  A_h / sin(theta_h) = ((n-1)/n) * V_a V_b / V_sigma
  R_COS  :  V_a V_b cos(theta_h) = -C_ab / c_n                (rational in x)
  R_COF  :  C_aa = c_n V_a^2                                  (so d_e log(V_a V_b) = (d_e C_aa/C_aa + d_e C_bb/C_bb)/2)

so that, whenever V_sigma != 0 and every C_aa != 0, with the per-hinge bracket

  bracket_h(e) := d_e C_ab - (C_ab/2)(d_e C_aa/C_aa + d_e C_bb/C_bb),

  A_h d_e theta_h = (n/((n-1) V_sigma c_n)) * bracket_h(e).

Hence T1 is equivalent, under those nondegeneracy hypotheses, to the RATIONAL identity

  R_e(x) := sum_h bracket_h(e) = 0   for every edge e,

and after multiplying by prod_c C_cc it is a polynomial identity in Z[x]. The T4 near miss reweights
each hinge by A_h^2 instead of A_h:

  sum_h A_h^2 d_e theta_h = (n/((n-1) V_sigma c_n)) * sum_h A_h * bracket_h(e),

so it is exactly evaluable only when every hinge volume A_h is rational; for n = 3 that means every
edge length is rational, i.e. every x_h is a perfect square. This script therefore evaluates the near
miss on integer-edge tetrahedra given by their six edge LENGTHS (no coordinates needed) and the
control R_e on the same simplex with the same cofactors.

Derivatives d_e are exact: dual numbers Q[eps]/(eps^2) with division-free Laplace determinants. A zero
residual here is evidence for the composition plan on a finite carrier; it is not a proof of the
polynomial identity, which is the P1 target.
"""
from fractions import Fraction as F
from itertools import combinations


class Dual:
    __slots__ = ('a', 'b')

    def __init__(self, a, b=F(0)):
        self.a, self.b = F(a), F(b)

    def __add__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        return Dual(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __sub__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        return Dual(self.a - o.a, self.b - o.b)

    def __neg__(self):
        return Dual(-self.a, -self.b)

    def __mul__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        return Dual(self.a * o.a, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def __repr__(self):
        return f'({self.a} + {self.b} eps)'


def laplace_det(m):
    n = len(m)
    if n == 1:
        return m[0][0]
    total = Dual(0)
    for j in range(n):
        sub = [row[:j] + row[j + 1:] for row in m[1:]]
        term = m[0][j] * laplace_det(sub)
        total = total + term if j % 2 == 0 else total - term
    return total


def sqdist(p, q):
    return sum((u - v) ** 2 for u, v in zip(p, q))


def squared_lengths_from_points(pts):
    return {frozenset(e): F(sqdist(pts[e[0]], pts[e[1]])) for e in combinations(range(len(pts)), 2)}


def squared_lengths_from_lengths(lengths):
    """lengths: the six edge lengths of a tetrahedron in the order 01, 02, 03, 12, 13, 23."""
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    return {frozenset(e): F(l) ** 2 for e, l in zip(pairs, lengths)}


def cofactors_dual(x, k, edge):
    """Vertex-block cofactors of the bordered CM matrix of a (k-1)-simplex on k vertices, with
    x_edge -> x_edge + eps so that the eps-part is the exact partial derivative."""
    B = [[Dual(0)] * (k + 1) for _ in range(k + 1)]
    for i in range(k):
        B[0][i + 1] = B[i + 1][0] = Dual(1)
        for j in range(k):
            if i != j:
                B[i + 1][j + 1] = Dual(x[frozenset((i, j))], 1 if frozenset((i, j)) == frozenset(edge) else 0)
    C = [[None] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            minor = [row[:j + 1] + row[j + 2:] for r, row in enumerate(B) if r != i + 1]
            C[i][j] = laplace_det(minor) * ((-1) ** (i + j))
    return C


def brackets(x, k, edge):
    """{(a, b): bracket_h(e)} for every hinge h = (a, b), from one cofactor computation."""
    C = cofactors_dual(x, k, edge)
    out = {}
    for a, b in combinations(range(k), 2):
        if C[a][a].a == 0 or C[b][b].a == 0:
            raise ValueError('degenerate facet')
        dlog = C[a][a].b / C[a][a].a + C[b][b].b / C[b][b].a
        out[(a, b)] = C[a][b].b - C[a][b].a * dlog / 2
    return out


def residual(x, k, edge):
    """R_e(x) = sum over hinges of bracket_h(e); T1 <=> R_e = 0."""
    return sum(brackets(x, k, edge).values(), F(0))


def near_miss_a2(x, lengths, edge):
    """sum_h A_h * bracket_h(e) for a tetrahedron (k = 4) with RATIONAL edge lengths, which is the T4
    near miss sum_h A_h^2 d_e theta_h up to the nonzero prefactor n/((n-1) V_sigma c_n). The hinge of
    (a, b) is the edge joining the two other vertices, and A_h is its length."""
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    length = {frozenset(e): F(l) for e, l in zip(pairs, lengths)}
    br = brackets(x, 4, edge)
    total = F(0)
    for (a, b), value in br.items():
        c, d = [v for v in range(4) if v not in (a, b)]
        total += length[frozenset((c, d))] * value
    return total, sum(br.values(), F(0))


COORDINATE_CASES = [
    ([(0, 0, 0), (1, 0, 0), (0, 2, 0), (1, 1, 3)], 'tetra-A'),
    ([(0, 0, 0), (2, 0, 0), (0, 3, 0), (0, 0, 5)], 'tetra-right'),
    ([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], 'tetra-regular-lattice'),
    ([(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)], 'tetra-kuhn'),
    ([(0, 0, 0), (3, 0, 0), (1, 4, 0), (2, 1, 5)], 'tetra-B'),
    ([(0, 0, 0, 0), (1, 0, 0, 0), (0, 2, 0, 0), (1, 1, 3, 0), (1, 2, 1, 4)], 'pentatope-A'),
    ([(0, 0, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0), (1, 1, 1, 0), (1, 1, 1, 1)], 'pentatope-kuhn'),
    ([(0, 0, 0, 0), (2, 0, 0, 0), (1, 3, 0, 0), (1, 1, 2, 0), (1, 1, 1, 3)], 'pentatope-B'),
]
# Integer-edge tetrahedra (lengths 01, 02, 03, 12, 13, 23) for the exact T4 near miss. Strict
# Cayley-Menger positivity: every face CM determinant < 0 and the solid CM determinant > 0.
LENGTH_CASES = [
    ((1, 1, 1, 1, 1, 1), 'tetra-regular-unit (expected FALSE near miss: A_h constant)'),
    ((2, 4, 5, 4, 6, 3), 'tetra-W1 integer edges, det CM = 448, V^2 = 14/9'),
    ((3, 4, 4, 5, 6, 2), 'tetra-W2 integer edges, det CM = 448, V^2 = 14/9'),
]


def cm_det(x, k):
    """Bordered Cayley-Menger determinant of the (k-1)-simplex on k vertices (real part only)."""
    B = [[Dual(0)] + [Dual(1)] * k] + [[Dual(1)] + [Dual(0) if i == j else Dual(x[frozenset((i, j))]) for j in range(k)] for i in range(k)]
    return laplace_det(B).a


if __name__ == '__main__':
    all_zero = True
    for pts, label in COORDINATE_CASES:
        k = len(pts)
        x = squared_lengths_from_points(pts)
        edges = list(combinations(range(k), 2))
        res = [residual(x, k, e) for e in edges]
        zero = all(r == 0 for r in res)
        all_zero &= zero
        print(label, '| n =', k - 1, '| R_e = 0 for all', len(edges), 'edges:', zero)
    near_miss_ok = True
    for lengths, label in LENGTH_CASES:
        x = squared_lengths_from_lengths(lengths)
        faces_ok = all(cm_det({frozenset((i, j)): x[frozenset((f[i], f[j]))] for i in range(3) for j in range(3) if i != j}, 3) < 0
                       for f in combinations(range(4), 3))
        solid = cm_det(x, 4)
        edges = list(combinations(range(4), 2))
        values = [near_miss_a2(x, lengths, e) for e in edges]
        nm = [v[0] for v in values]
        ctrl = [v[1] for v in values]
        control_zero = all(c == 0 for c in ctrl)
        all_zero &= control_zero
        nonzero_edges = [e for e, v in zip(edges, nm) if v != 0]
        print(label, '| strict CM positivity:', faces_ok and solid > 0, '| det CM =', solid,
              '| control R_e = 0 on all 6 edges:', control_zero,
              '| A_h^2 near miss nonzero on edges:', nonzero_edges,
              '| values:', [str(v) for v in nm])
        if label.startswith('tetra-W'):
            near_miss_ok &= bool(nonzero_edges) and faces_ok and solid > 0 and control_zero
    print('COMPOSITION_PLAN_HOLDS_ON_FINITE_CARRIER' if all_zero else 'COMPOSITION_PLAN_FAILED')
    print('T4_NEAR_MISS_NONZERO_WITH_VALID_CONTROL' if near_miss_ok else 'T4_NEAR_MISS_NOT_ESTABLISHED')
    raise SystemExit(0 if (all_zero and near_miss_ok) else 1)
