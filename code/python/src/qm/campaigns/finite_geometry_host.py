"""The Fano plane as a host geometry: 7 points, 7 lines, one line through each pair.

Origin: code/python/src/qm/campaigns/finite_geometry_host.py
Claim: every point lies on 3 lines and every pair lies on exactly one line. Both counts are enumerated.
AuthorityEffect: None.
"""
from fractions import Fraction


class FanoError(Exception):
    """The line list failed the Fano incidence count."""


FANO_LINES = (
    frozenset({0, 1, 2}),
    frozenset({0, 3, 4}),
    frozenset({0, 5, 6}),
    frozenset({1, 3, 5}),
    frozenset({1, 4, 6}),
    frozenset({2, 3, 6}),
    frozenset({2, 4, 5}),
)


def lines_through(point: int) -> int:
    return sum(1 for line in FANO_LINES if point in line)


def pair_line_count(left: int, right: int) -> int:
    pair = frozenset({left, right})
    return sum(1 for line in FANO_LINES if pair <= line)


def fano_incidence_defect() -> Fraction:
    """Zero when every point has 3 lines and every pair has one line."""
    defect = Fraction(0)
    for point in range(7):
        defect += abs(lines_through(point) - 3)
    for left in range(7):
        for right in range(left + 1, 7):
            defect += abs(pair_line_count(left, right) - 1)
    if defect != 0:
        raise FanoError(f"Fano incidence defect is {defect}")
    return defect
