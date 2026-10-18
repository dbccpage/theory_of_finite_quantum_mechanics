"""A matrix functor on a two-arrow diagram.

F sends composition of rational matrices to multiplication, and the identity
arrow to the identity matrix. The defect is the entrywise gap of those two
readings of F(g ∘ f).
"""
from fractions import Fraction


class ObserverFunctorError(Exception):
    """The functor failed to preserve composition or identities."""


def _matmul(left, right):
    return tuple(
        tuple(
            left[row][0] * right[0][col] + left[row][1] * right[1][col]
            for col in range(2)
        )
        for row in range(2)
    )


def _gap(left, right) -> Fraction:
    total = Fraction(0)
    for row in range(2):
        for col in range(2):
            total += abs(left[row][col] - right[row][col])
    return total


def _apply(matrix, vector):
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def composition_defect() -> Fraction:
    """Return the gap between matrix multiplication and action on the basis."""
    arrow_f = ((Fraction(1), Fraction(1, 2)), (Fraction(0), Fraction(1)))
    arrow_g = ((Fraction(1), Fraction(0)), (Fraction(1, 3), Fraction(1)))
    identity = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    columns = (
        _apply(arrow_g, _apply(arrow_f, (Fraction(1), Fraction(0)))),
        _apply(arrow_g, _apply(arrow_f, (Fraction(0), Fraction(1)))),
    )
    by_action = (
        (columns[0][0], columns[1][0]),
        (columns[0][1], columns[1][1]),
    )
    by_product = _matmul(arrow_g, arrow_f)
    image = _apply(identity, (Fraction(1, 2), Fraction(3, 7)))
    identity_gap = abs(image[0] - Fraction(1, 2)) + abs(image[1] - Fraction(3, 7))
    defect = _gap(by_action, by_product)
    if defect != 0 or identity_gap != 0:
        raise ObserverFunctorError(f"functor defect is {defect}, identity gap {identity_gap}")
    return by_action[0][0] + by_action[1][1]
