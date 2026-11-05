"""CH17: exact rational endpoint-block path-sum classification.

Row-source transitions M and membership H preserve endpoint-block aggregates
for every source representative and finite length iff M H = H B. Length one
is necessary; associativity gives M^(n+1) H = M(H B^n) = H B^(n+1).
This selected semiring Q allows signed weights. No pathwise preservation or
physical interpretation is claimed. AuthorityEffect: None.
"""
from fractions import Fraction


def _matrix(rows):
    rows = tuple(tuple(row) for row in rows)
    if rows and any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("ragged matrix")
    if any(type(x) not in (int, Fraction) for row in rows for x in row):
        raise TypeError("exact rational entries required")
    return tuple(tuple(Fraction(x) for x in row) for row in rows)


def product(left, right):
    left, right = _matrix(left), _matrix(right)
    inner = len(left[0]) if left else 0
    if inner != len(right):
        raise ValueError("matrix dimensions disagree")
    columns = len(right[0]) if right else 0
    return tuple(tuple(sum((left[i][k] * right[k][j] for k in range(inner)), Fraction(0))
                       for j in range(columns)) for i in range(len(left)))


def membership(vertices, blocks):
    if type(vertices) is not int or vertices < 0:
        raise ValueError("invalid carrier size")
    blocks = tuple(tuple(block) for block in blocks)
    flat = [v for block in blocks for v in block]
    if any(not block for block in blocks) or any(type(v) is not int for v in flat):
        raise ValueError("partition blocks must contain integer vertices")
    if len(flat) != vertices or set(flat) != set(range(vertices)):
        raise ValueError("blocks must partition the carrier")
    return tuple(tuple(Fraction(int(v in block)) for block in blocks) for v in range(vertices))


def quotient(matrix, blocks):
    matrix = _matrix(matrix)
    if any(len(row) != len(matrix) for row in matrix):
        raise ValueError("transition matrix must be square")
    blocks = tuple(tuple(block) for block in blocks)
    h = membership(len(matrix), blocks)
    sums = product(matrix, h)
    result = tuple(sums[block[0]] for block in blocks)
    return result if product(h, result) == sums else None


def partitions(vertices):
    """Every set partition once, in canonical restricted-growth order."""
    if type(vertices) is not int or vertices < 0:
        raise ValueError("invalid carrier size")
    def extend(v, blocks):
        if v == vertices:
            yield blocks
            return
        for i in range(len(blocks)):
            yield from extend(v + 1, blocks[:i] + (blocks[i] + (v,),) + blocks[i + 1:])
        yield from extend(v + 1, blocks + ((v,),))
    yield from extend(0, ())


def classify(matrix):
    """Exhaustive finite classification for the selected rational semiring.

    Bell-number growth is explicit; this is a reference for small carriers.
    """
    matrix = _matrix(matrix)
    return tuple((blocks, quotient(matrix, blocks)) for blocks in partitions(len(matrix)))
