"""Higher-dimensional clock: the 3-cycle permutation and its order.

Origin: code/python/src/qm/campaigns/higher_dim.py
Claim: the qutrit clock X satisfies X^3 = I, and the order found by multiplication is 3.
AuthorityEffect: None. The Weyl relation with a root of unity is not claimed here.
"""
from fractions import Fraction


class ClockError(Exception):
    """The clock did not return to the identity at the computed order."""


def _mul(left, right):
    size = len(left)
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(size)) for j in range(size))
        for i in range(size)
    )


def _identity(size: int):
    return tuple(tuple(Fraction(1 if i == j else 0) for j in range(size)) for i in range(size))


def clock_order(dimension: int = 3) -> int:
    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension < 2:
        raise ClockError(f"clock dimension must be an int >= 2, got {dimension!r}")
    clock = tuple(
        tuple(Fraction(1 if i == (j + 1) % dimension else 0) for j in range(dimension))
        for i in range(dimension)
    )
    current = _identity(dimension)
    for exponent in range(1, dimension + 2):
        current = _mul(current, clock)
        if current == _identity(dimension):
            if exponent != dimension:
                raise ClockError(f"clock order is {exponent}, not {dimension}")
            return exponent
    raise ClockError("clock power did not return to the identity")
