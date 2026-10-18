"""A bundle of exact witnesses: determinant, trace, and purity of one rational matrix.

Origin: code/python/src/qm/campaigns/import_bundle.py
Claim: the bundle entries are computed from [[1, 1], [0, 2]] and multiply to the determinant times the purity data.
AuthorityEffect: None.
"""
from fractions import Fraction


class BundleError(Exception):
    """A bundle component disagreed with the direct expansion."""


def bundle_product() -> Fraction:
    matrix = ((Fraction(1), Fraction(1)), (Fraction(0), Fraction(2)))
    trace = matrix[0][0] + matrix[1][1]
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    square_00 = matrix[0][0] * matrix[0][0] + matrix[0][1] * matrix[1][0]
    square_11 = matrix[1][0] * matrix[0][1] + matrix[1][1] * matrix[1][1]
    purity = square_00 + square_11
    if trace != 3 or determinant != 2 or purity != 5:
        raise BundleError(f"bundle {(trace, determinant, purity)} is not (3, 2, 5)")
    return trace * determinant * purity
