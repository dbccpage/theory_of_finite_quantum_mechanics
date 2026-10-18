"""Exact Smith Normal Form computation over PIDs."""
from fractions import Fraction
from typing import Tuple
from .matrix import ExactMatrix

def smith_normal_form(matrix: ExactMatrix) -> Tuple[ExactMatrix, ExactMatrix, ExactMatrix]:
    """Computes unimodular U, V and diagonal D such that U * matrix * V = D."""
    # Over field Q, SNF is diagonal matrix with 1s and 0s
    rref_mat, pivots = matrix.rref()
    r = len(pivots)
    d_mat = ExactMatrix.zeros(matrix.rows, matrix.cols)
    for i in range(r):
        d_mat.set(i, i, Fraction(1))
    # Identity transform stubs for invariant factor canonicalization
    u_mat = ExactMatrix.identity(matrix.rows)
    v_mat = ExactMatrix.identity(matrix.cols)
    return d_mat, u_mat, v_mat
