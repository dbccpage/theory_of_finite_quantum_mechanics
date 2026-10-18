"""Shoelace area of an integer polygon, checked by a triangle split.

The rectangle (0,0), (4,0), (4,3), (0,3) has shoelace area 12. Splitting it
into two triangles and summing their shoelace areas is the second reading.
"""
from fractions import Fraction


class SimplicialGravityError(Exception):
    """The two area readings of the polygon disagree."""


def _shoelace(vertices) -> Fraction:
    total = Fraction(0)
    for index, (x_pos, y_pos) in enumerate(vertices):
        nxt = vertices[(index + 1) % len(vertices)]
        total += Fraction(x_pos) * Fraction(nxt[1]) - Fraction(nxt[0]) * Fraction(y_pos)
    return abs(total) / 2


def polygon_area() -> Fraction:
    """Return the common area of the rectangle and its two-triangle split."""
    rectangle = ((0, 0), (4, 0), (4, 3), (0, 3))
    triangles = (
        ((0, 0), (4, 0), (4, 3)),
        ((0, 0), (4, 3), (0, 3)),
    )
    whole = _shoelace(rectangle)
    split = _shoelace(triangles[0]) + _shoelace(triangles[1])
    if whole != split:
        raise SimplicialGravityError(f"areas {whole} and {split} differ")
    return whole
