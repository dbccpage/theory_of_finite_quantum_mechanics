"""Born weights as a frame function on a rational orthonormal basis.

Origin: code/python/src/qm/campaigns/born_gleason.py
Claim: sum_i (v · e_i)^2 equals ||v||^2 on two rational orthonormal frames.
AuthorityEffect: None. This is not Gleason's theorem.
"""
from fractions import Fraction


class BornGleasonError(Exception):
    """A frame was not orthonormal or the two frame sums disagreed."""


def _dot(left, right) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def frame_sum(vector, frame) -> Fraction:
    total = Fraction(0)
    for axis in frame:
        amplitude = _dot(vector, axis)
        total += amplitude * amplitude
    norm = _dot(vector, vector)
    for i, axis in enumerate(frame):
        if _dot(axis, axis) != 1:
            raise BornGleasonError(f"frame vector {i} is not a unit vector")
        for other in frame[i + 1 :]:
            if _dot(axis, other) != 0:
                raise BornGleasonError("frame vectors are not orthogonal")
    if total != norm:
        raise BornGleasonError(f"frame sum {total} disagrees with the norm {norm}")
    return total


def born_frame_gap() -> Fraction:
    """Difference of the frame sums on the coordinate basis and a Pythagorean basis."""
    vector = (Fraction(3, 5), Fraction(4, 5))
    coordinate = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    rotated = ((Fraction(3, 5), Fraction(4, 5)), (Fraction(-4, 5), Fraction(3, 5)))
    return frame_sum(vector, coordinate) - frame_sum(vector, rotated)
