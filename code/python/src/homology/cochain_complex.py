"""Cochain complexes with coboundary operators delta^k . delta^{k-1} = 0."""
from typing import List
from .errors import NonZeroCompositionError
from ..linear_algebra import ExactMatrix

class CochainComplex:
    def __init__(self, coboundaries: List[ExactMatrix]):
        for i in range(len(coboundaries) - 1):
            prod = coboundaries[i + 1] * coboundaries[i]
            z = ExactMatrix.zeros(prod.rows, prod.cols)
            if prod != z:
                raise NonZeroCompositionError(f"delta^{i+1} . delta^{i} != 0")
        self.coboundaries = coboundaries
