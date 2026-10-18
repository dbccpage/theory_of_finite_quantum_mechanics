"""Theory of Finite Quantum Mechanics: Core Exact Computational Engine."""

from .linear_algebra import ExactMatrix, GaussianRational
from .homology import Carrier
from .qm import DensityOperator

__all__ = ["ExactMatrix", "GaussianRational", "Carrier", "DensityOperator", "exported_identity_trace"]


def exported_identity_trace(size: int = 2):
    """Sum the diagonal of the exported identity. The sum equals the dimension."""
    from fractions import Fraction

    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        raise ValueError(f"identity size must be a nonnegative int, got {size!r}")
    eye = ExactMatrix.identity(size)
    total = Fraction(0)
    for index in range(size):
        total += Fraction(eye.get(index, index))
    if total != size:
        raise ValueError(f"exported identity trace is {total}, not {size}")
    return total