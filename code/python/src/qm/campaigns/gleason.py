"""Finite Gleason check: a quadratic frame function sums to the squared norm.

Origin: code/python/src/qm/campaigns/gleason.py
Claim: for v = (1/3, 2/3, 2/3), the coordinate frame and a coordinate permutation give the same sum 1.
AuthorityEffect: None. This is not Gleason's classification of measures on the sphere.
"""
from fractions import Fraction


class GleasonError(Exception):
    """The two frames assigned different totals to the same vector."""


def _dot(left, right) -> Fraction:
    return sum((left[i] * right[i] for i in range(len(left))), Fraction(0))


def frame_total(vector, frame) -> Fraction:
    total = Fraction(0)
    for axis in frame:
        amplitude = _dot(vector, axis)
        total += amplitude * amplitude
    return total


def gleason_frame_gap() -> Fraction:
    vector = (Fraction(1, 3), Fraction(2, 3), Fraction(2, 3))
    if _dot(vector, vector) != 1:
        raise GleasonError("the witness vector is not a unit vector")
    coordinate = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    )
    permuted = (coordinate[1], coordinate[2], coordinate[0])
    left = frame_total(vector, coordinate)
    right = frame_total(vector, permuted)
    if left != right or left != 1:
        raise GleasonError(f"frame totals {(left, right)} are not both 1")
    return left - right
