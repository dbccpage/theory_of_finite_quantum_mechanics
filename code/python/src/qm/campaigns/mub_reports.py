"""Report the squared overlap of two rational orthonormal frames.

Origin: code/python/src/qm/campaigns/mub_reports.py
Claim: the coordinate basis and the (3,4,5) frame have max squared overlap 9/25, not the unbiased value 1/2.
AuthorityEffect: None. Dimension 2 has no pair of rational mutually unbiased bases.
"""
from fractions import Fraction


class MubReportError(Exception):
    """A reported frame was not orthonormal."""


def _dot(left, right) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def max_squared_overlap(left_frame, right_frame) -> Fraction:
    for frame in (left_frame, right_frame):
        if _dot(frame[0], frame[0]) != 1 or _dot(frame[1], frame[1]) != 1 or _dot(frame[0], frame[1]) != 0:
            raise MubReportError("a frame in the report is not orthonormal")
    best = Fraction(0)
    for left in left_frame:
        for right in right_frame:
            amplitude = _dot(left, right)
            best = max(best, amplitude * amplitude)
    return best


def overlap_gap() -> Fraction:
    """Unbiased value 1/2 minus the computed maximum squared overlap.

    Parseval on the right-hand frame is checked separately: each coordinate
    vector's squared overlaps sum to its own norm.
    """
    coordinate = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    pythagorean = ((Fraction(3, 5), Fraction(4, 5)), (Fraction(-4, 5), Fraction(3, 5)))
    overlap = max_squared_overlap(coordinate, pythagorean)
    parseval_defect = Fraction(0)
    for left in coordinate:
        total = Fraction(0)
        for right in pythagorean:
            amplitude = _dot(left, right)
            total += amplitude * amplitude
        parseval_defect += total - _dot(left, left)
    if parseval_defect != 0:
        raise MubReportError(f"Parseval defect is {parseval_defect}")
    return Fraction(1, 2) - overlap
