"""Coboundary operator representations."""
from ..linear_algebra import ExactMatrix

class CoboundaryOperator:
    def __init__(self, boundary_matrix: ExactMatrix):
        self.matrix = boundary_matrix.transpose()

    def apply(self, vec):
        return self.matrix.mul_vec(vec)
