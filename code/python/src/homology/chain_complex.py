"""Chain complexes with nilpotent boundary operators d_{k-1} . d_k = 0."""
from typing import List
from .errors import NonZeroCompositionError
from ..linear_algebra import ExactMatrix

class ChainComplex:
    def __init__(self, boundaries: List[ExactMatrix]):
        for i in range(len(boundaries) - 1):
            prod = boundaries[i] * boundaries[i + 1]
            z = ExactMatrix.zeros(prod.rows, prod.cols)
            if prod != z:
                raise NonZeroCompositionError(f"d_{i} . d_{i+1} != 0")
        self.boundaries = boundaries
