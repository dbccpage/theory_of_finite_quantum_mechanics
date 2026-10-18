"""One step of the simple random walk on the 3-cycle.

Origin: code/python/src/qm/campaigns/quantum_walk.py
Claim: P^2 at the start vertex is 1/2, and the uniform measure 1/3 is fixed by P.
AuthorityEffect: None. The step is the classical stochastic matrix, not a unitary coin.
"""
from fractions import Fraction


class WalkError(Exception):
    """The walk matrix was not stochastic or failed the stationary check."""


def _mul(left, right):
    size = len(left)
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(size)) for j in range(size))
        for i in range(size)
    )


def cycle_return() -> Fraction:
    half = Fraction(1, 2)
    step = (
        (Fraction(0), half, half),
        (half, Fraction(0), half),
        (half, half, Fraction(0)),
    )
    for col in range(3):
        if sum(step[row][col] for row in range(3)) != 1:
            raise WalkError("the walk is not column-stochastic")
    square = _mul(step, step)
    uniform = (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3))
    image = tuple(sum(step[i][j] * uniform[j] for j in range(3)) for i in range(3))
    if image != uniform:
        raise WalkError(f"uniform measure moved to {image}")
    return square[0][0]
