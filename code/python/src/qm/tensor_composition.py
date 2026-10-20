"""Exact witnesses for the operational tensor-composition derivation.

AuthorityEffect: None. Gaussian-rational examples check formulas and distinguish
countermodels; the all-dimension result is the proof in TFQ-0410--TFQ-0413.
No floating-point SVD or numerical cone classification is used here.
"""
from fractions import Fraction

from ..linear_algebra.scalars import GaussianRational as G


def dimension(n):
    if type(n) is not int or n < 1:
        raise ValueError("positive integer dimension required")
    return n


def matrix(rows):
    a = tuple(tuple(G(x) for x in row) for row in rows)
    if not a or not a[0] or any(len(row) != len(a[0]) for row in a):
        raise ValueError("nonempty rectangular matrix required")
    return a


def adjoint(a):
    a = matrix(a)
    return tuple(tuple(x.conjugate() for x in row) for row in zip(*a))


def multiply(a, b):
    a, b = matrix(a), matrix(b)
    if len(a[0]) != len(b):
        raise ValueError("matrix product shape mismatch")
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def tensor(a, b):
    a, b = matrix(a), matrix(b)
    return tuple(tuple(x * y for x in r for y in s) for r in a for s in b)


def outer(v):
    v = tuple(G(x) for x in v)
    if not v:
        raise ValueError("nonempty vector required")
    return tuple(tuple(x * y.conjugate() for y in v) for x in v)


def scale(c, a):
    c, a = G(c), matrix(a)
    return tuple(tuple(c * x for x in row) for row in a)


def conjugate(u, a):
    return multiply(multiply(u, a), adjoint(u))


def identity(n):
    return matrix([[int(i == j) for j in range(dimension(n))] for i in range(n)])


def trace(a):
    a = matrix(a)
    if len(a) != len(a[0]):
        raise ValueError("square matrix required")
    return sum(a[i][i] for i in range(len(a)))


def pairing(a, b):
    return trace(multiply(a, b))


def quadratic(a, v):
    return pairing(a, outer(v))


def hermitian_coordinates(a):
    a = matrix(a)
    if a != adjoint(a):
        raise ValueError("Hermitian matrix required")
    d = len(a)
    return (tuple(a[i][i].real for i in range(d)) +
            tuple(part for i in range(d) for j in range(i + 1, d)
                  for part in (a[i][j].real, a[i][j].imag)))


def fiducial_projectors(d):
    """d^2 normalized rank-one projectors spanning Herm(d), over Q(i)."""
    d = dimension(d)
    out = [outer([int(i == j) for j in range(d)]) for i in range(d)]
    for i in range(d):
        for j in range(i + 1, d):
            for phase in (G(1), G(0, 1)):
                v = [G(0) for _ in range(d)]
                v[i], v[j] = G(1), phase
                out.append(scale(Fraction(1, 2), outer(v)))
    return tuple(out)


def controlled_shift(n, m):
    """C|a,b> = |a,b+a mod m>. The theorem chooses n <= m."""
    n, m = dimension(n), dimension(m)
    return matrix([[int(i == (j // m) * m + (j % m + j // m) % m)
                    for j in range(n * m)] for i in range(n * m)])


def partial_transpose_first(a, n, m):
    a, n, m = matrix(a), dimension(n), dimension(m)
    if len(a) != n * m or len(a[0]) != n * m:
        raise ValueError("bipartite matrix shape mismatch")
    return tuple(tuple(a[(j // m) * m + i % m][(i // m) * m + j % m]
                       for j in range(n * m)) for i in range(n * m))


def twisted_gate(u, a, n, m):
    """Partial-transpose conjugation of a unitary channel, a rival convention."""
    return partial_transpose_first(conjugate(u, partial_transpose_first(a, n, m)), n, m)


def calibration_table(transform, n, m):
    """Exact probabilities on a complete product-preparation/effect frame."""
    products = tuple(tensor(a, b) for a in fiducial_projectors(n)
                     for b in fiducial_projectors(m))
    return tuple(tuple(pairing(e, transform(s)) for e in products) for s in products)


def real_rank(rows):
    """Exact rank used to check finite tomographic fixtures."""
    a = [list(row) for row in rows]
    if not a or not a[0] or any(len(row) != len(a[0]) for row in a):
        raise ValueError("nonempty rectangular matrix required")
    if any(type(x) not in (int, Fraction) for row in a for x in row):
        raise TypeError("exact rational coordinates required")
    a = [[Fraction(x) for x in row] for row in a]
    rank = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        value = a[rank][j]
        a[rank] = [x / value for x in a[rank]]
        for i in range(rank + 1, len(a)):
            value = a[i][j]
            a[i] = [x - value * y for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank
