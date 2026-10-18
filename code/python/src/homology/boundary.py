"""Boundary operator matrix representations."""
from ..linear_algebra import ExactMatrix

class BoundaryOperator:
    def __init__(self, matrix: ExactMatrix):
        self.matrix = matrix

    def apply(self, vec):
        return self.matrix.mul_vec(vec)
