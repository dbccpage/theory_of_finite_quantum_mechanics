"""Image (column space) and Kernel (null space) exact decompositions."""
from typing import List
from .matrix import ExactMatrix

def image_basis(matrix: ExactMatrix) -> List[List[object]]:
    """Returns a basis for the column space (image) of the matrix."""
    _, pivots = matrix.rref()
    return [matrix.col(c) for c in pivots]

def kernel_basis(matrix: ExactMatrix) -> List[List[object]]:
    """Returns a basis for the null space (kernel) of the matrix."""
    return matrix.kernel_basis()
