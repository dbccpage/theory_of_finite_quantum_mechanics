"""Exact algebraic homology, carrier complexes, and cryptographic witnesses."""
from .ids import SimplexId, ComplexId
from .errors import HomologyError, NonZeroCompositionError, DimensionMismatchError
from .hashing import hash_matrix, hash_bytes
from .simplicial import Simplex, SimplicialComplex
from .chain import Chain
from .cochain import Cochain
from .boundary import BoundaryOperator
from .coboundary import CoboundaryOperator
from .chain_complex import ChainComplex
from .cochain_complex import CochainComplex
from .carrier import Carrier
from .exact_carrier import ExactCarrier
from .witness import HomologyWitness
from .exact_carrier import triangle_betti

__all__ = [
    "SimplexId",
    "ComplexId",
    "HomologyError",
    "NonZeroCompositionError",
    "DimensionMismatchError",
    "hash_matrix",
    "hash_bytes",
    "Simplex",
    "SimplicialComplex",
    "Chain",
    "Cochain",
    "BoundaryOperator",
    "CoboundaryOperator",
    "ChainComplex",
    "CochainComplex",
    "Carrier",
    "ExactCarrier",
    "HomologyWitness",
    "triangle_betti",
]


def exported_triangle_rank_sum() -> int:
    """Computed triangle ranks. Nilpotency is rechecked, then the Betti number is returned."""
    from fractions import Fraction
    from .boundary import triangle_boundary_defect

    rank0, rank1, betti = triangle_betti()
    defect = triangle_boundary_defect()
    if defect != 0:
        raise ValueError(f"triangle boundary square has defect {defect}")
    if rank0 != 2 or rank1 != 1 or betti != 0:
        raise ValueError(f"triangle Betti data {(rank0, rank1, betti)} is not (2, 1, 0)")
    return rank0 + rank1 + betti + int(defect == Fraction(0))
