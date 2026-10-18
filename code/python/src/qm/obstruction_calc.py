"""Coboundary obstruction of a rational 0-cochain on a triangle.

Edge values are differences of vertex values. The face evaluation
e01 - e02 + e12 is computed from those edges and must vanish.
"""
from fractions import Fraction


class ObstructionError(Exception):
    """The face obstruction of a coboundary was nonzero."""


def face_obstruction() -> Fraction:
    """Return e01 - e02 + e12 for the coboundary of (0, 1/2, 3/5)."""
    vertices = (Fraction(0), Fraction(1, 2), Fraction(3, 5))
    edge_01 = vertices[1] - vertices[0]
    edge_02 = vertices[2] - vertices[0]
    edge_12 = vertices[2] - vertices[1]
    signed = ((1, edge_01, 0, 1), (-1, edge_02, 0, 2), (1, edge_12, 1, 2))
    from_edges = sum((sign * value for sign, value, _start, _end in signed), Fraction(0))
    coefficient = [Fraction(0), Fraction(0), Fraction(0)]
    for sign, _value, start, end in signed:
        coefficient[end] += sign
        coefficient[start] -= sign
    from_vertices = sum(
        (coefficient[index] * vertices[index] for index in range(3)),
        Fraction(0),
    )
    if from_edges != from_vertices:
        raise ObstructionError(f"edge reading {from_edges} differs from {from_vertices}")
    if from_edges != 0:
        raise ObstructionError(f"face obstruction is {from_edges}")
    return from_edges
