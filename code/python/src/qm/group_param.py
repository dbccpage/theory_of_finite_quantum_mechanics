"""One-parameter shear group over the rationals.

S(t) = [[1, t], [0, 1]] satisfies S(m) S(n) = S(m + n). The (0, 1) entry of
the product is compared with the parameter sum.
"""
from fractions import Fraction


class GroupParamError(Exception):
    """The shear law failed."""


def _shear(parameter: Fraction):
    return (
        (Fraction(1), parameter),
        (Fraction(0), Fraction(1)),
    )


def _product(left, right):
    return tuple(
        tuple(
            left[row][0] * right[0][col] + left[row][1] * right[1][col]
            for col in range(2)
        )
        for row in range(2)
    )


def shear_parameter() -> Fraction:
    """Return the shear parameter of S(2/3) S(4/5), which is 22/15."""
    left = Fraction(2, 3)
    right = Fraction(4, 5)
    product = _product(_shear(left), _shear(right))
    expected = _shear(left + right)
    defect = Fraction(0)
    for row in range(2):
        for col in range(2):
            defect += abs(product[row][col] - expected[row][col])
    if defect != 0:
        raise GroupParamError(f"shear defect is {defect}")
    return product[0][1]
