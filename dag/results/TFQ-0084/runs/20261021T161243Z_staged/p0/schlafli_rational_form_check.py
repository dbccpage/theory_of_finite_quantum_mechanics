"""Finite-carrier check (exact, over Q) of the P0 composition plan that makes T1 arccos-free.

Composition plan (P0, M2): with C the cofactor matrix of the bordered Cayley-Menger matrix of an
n-simplex in the squared edge lengths x, c_n = (-1)^n 2^(n-1) ((n-1)!)^2, and h = (a, b) the hinge
shared by the facets opposite vertices a and b:

  R_SIN  :  A_h / sin(theta_h) = ((n-1)/n) * V_a V_b / V_sigma
  R_COS  :  V_a V_b cos(theta_h) = -C_ab / c_n                (rational in x)
  R_COF  :  C_aa = c_n V_a^2                                  (so d_e log(V_a V_b) = (d_e C_aa/C_aa + d_e C_bb/C_bb)/2)

so that, whenever V_sigma != 0 and every C_aa != 0,

  sum_h A_h d_e theta_h = -(n/((n-1) V_sigma)) * sum_h V_a V_b d_e cos(theta_h)
                        =  (n/((n-1) V_sigma c_n)) * sum_{a<b} [ d_e C_ab - (C_ab/2)(d_e C_aa/C_aa + d_e C_bb/C_bb) ].

Hence T1 is equivalent, under those nondegeneracy hypotheses, to the RATIONAL identity

  R_e(x) := sum_{a<b} [ d_e C_ab - (C_ab/2)(d_e C_aa/C_aa + d_e C_bb/C_bb) ] = 0   for every edge e,

and after multiplying by prod_c C_cc it is a polynomial identity in Z[x]. This script evaluates R_e
exactly at rational points using dual numbers Q[eps]/(eps^2) for d_e (division-free Laplace
determinants). A zero here is evidence for the composition plan on a finite carrier; it is not a proof
of the polynomial identity, which is the P1 target.
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

    def __truediv__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        if o.a == 0:
            raise ZeroDivisionError('dual with zero real part')
        return Dual(self.a / o.a, (self.b * o.a - self.a * o.b) / (o.a * o.a))

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


def factorial(m):
    out = 1
    for i in range(2, m + 1):
        out *= i
    return out


def cofactors_dual(pts, edge):
    """Cofactor matrix (vertex block) of the bordered CM matrix with x_edge -> x_edge + eps."""
    k = len(pts)
    B = [[Dual(0)] * (k + 1) for _ in range(k + 1)]
    for i in range(k):
        B[0][i + 1] = B[i + 1][0] = Dual(1)
        for j in range(k):
            if i != j:
                d = Dual(sqdist(pts[i], pts[j]), 1 if {i, j} == set(edge) else 0)
                B[i + 1][j + 1] = d
    C = [[None] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            minor = [row[:j + 1] + row[j + 2:] for r, row in enumerate(B) if r != i + 1]
            C[i][j] = laplace_det(minor) * ((-1) ** (i + j))
    return C


def residual(pts, edge):
    n = len(pts) - 1
    C = cofactors_dual(pts, edge)
    total = Dual(0)
    for a, b in combinations(range(n + 1), 2):
        if C[a][a].a == 0 or C[b][b].a == 0:
            raise ValueError('degenerate facet')
        dlog = Dual(C[a][a].b / C[a][a].a + C[b][b].b / C[b][b].a)
        total = total + Dual(C[a][b].b) - Dual(C[a][b].a) * dlog * F(1, 2)
    return total.a


CASES = [
    ([(0, 0, 0), (1, 0, 0), (0, 2, 0), (1, 1, 3)], 'tetra-A'),
    ([(0, 0, 0), (2, 0, 0), (0, 3, 0), (0, 0, 5)], 'tetra-right'),
    ([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], 'tetra-regular-lattice'),
    ([(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)], 'tetra-kuhn'),
    ([(0, 0, 0), (3, 0, 0), (1, 4, 0), (2, 1, 5)], 'tetra-B'),
    ([(0, 0, 0, 0), (1, 0, 0, 0), (0, 2, 0, 0), (1, 1, 3, 0), (1, 2, 1, 4)], 'pentatope-A'),
    ([(0, 0, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0), (1, 1, 1, 0), (1, 1, 1, 1)], 'pentatope-kuhn'),
    ([(0, 0, 0, 0), (2, 0, 0, 0), (1, 3, 0, 0), (1, 1, 2, 0), (1, 1, 1, 3)], 'pentatope-B'),
]


def near_miss_shape(pts, edge):
    """Companion: the same cofactor sum with the A_h -> A_h^2 reweighting is NOT rational in general; for
    n=3 it carries sqrt(x_h) per hinge. Here only the rational part is evaluated to show it differs:
    sum_{a<b} x_h * [d_e C_ab - (C_ab/2)(...)] with x_h the squared hinge length (n=3 only)."""
    n = len(pts) - 1
    if n != 3:
        return None
    C = cofactors_dual(pts, edge)
    total = F(0)
    for a, b in combinations(range(4), 2):
        h = [k for k in range(4) if k not in (a, b)]
        xh = F(sqdist(pts[h[0]], pts[h[1]]))
        dlog = C[a][a].b / C[a][a].a + C[b][b].b / C[b][b].a
        total += xh * (C[a][b].b - C[a][b].a * dlog / 2)
    return total


if __name__ == '__main__':
    all_zero = True
    for pts, label in CASES:
        n = len(pts) - 1
        edges = list(combinations(range(n + 1), 2))
        res = [residual(pts, e) for e in edges]
        zero = all(r == 0 for r in res)
        all_zero &= zero
        nm = [near_miss_shape(pts, e) for e in edges] if n == 3 else None
        print(label, '| n =', n, '| R_e = 0 for all', len(edges), 'edges:', zero,
              '| x_h-weighted rational companion nonzero on some edge:',
              (any(v != 0 for v in nm) if nm else 'n/a'))
    print('COMPOSITION_PLAN_HOLDS_ON_FINITE_CARRIER' if all_zero else 'COMPOSITION_PLAN_FAILED')
    raise SystemExit(0 if all_zero else 1)
