"""Package certificate that the filled triangle is nilpotent with Betti (2, 1, 0).

Origin: lean4/FiniteCochain.lean theorem d1_d0_zero and lean4/CellGrammar.lean
structure ChainGrammar field boundarySquare. The export rechecks those two
certificates together.
Claim: urn:omega:fqm:homology:exported-triangle-rank-sum:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_homology_export.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 4; AST Sonar cognitive complexity max 3; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 4.
Scope Fence: This file does not recompute ranks or boundary matrices. It
checks the triangle Betti certificate and the boundary-defect certificate,
then adds them. It does not prove either Lean theorem.
"""

from __future__ import annotations

from fractions import Fraction

from .boundary import BoundaryOperator, triangle_boundary_defect
from .carrier import Carrier
from .chain import Chain
from .chain_complex import ChainComplex
from .cochain import Cochain
from .cochain_complex import CochainComplex
from .coboundary import CoboundaryOperator
from .errors import DimensionMismatchError, HomologyError, NonZeroCompositionError
from .exact_carrier import ExactCarrier, triangle_betti
from .hashing import hash_bytes, hash_matrix
from .ids import ComplexId, SimplexId
from .simplicial import Simplex, SimplicialComplex
from .witness import HomologyWitness


def _fail(kind: type[HomologyError], invariant: str, **parameters: object) -> HomologyError:
    return kind(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail(DimensionMismatchError, "float refused at the public boundary", role=role, received="float")


def _require_count(value: object, role: str) -> int:
    _refuse_float(value, role)
    if isinstance(value, bool):
        raise _fail(DimensionMismatchError, "boolean refused where an integer was required", role=role)
    if type(value) is not int:
        raise _fail(
            DimensionMismatchError,
            "triangle count is not an integer",
            role=role,
            received=type(value).__name__,
        )
    return value


def _require_triple(value: object) -> tuple[int, int, int]:
    if isinstance(value, (str, bytes)) or not isinstance(value, tuple) or len(value) != 3:
        raise _fail(
            DimensionMismatchError,
            "triangle Betti certificate is not a triple",
            received=type(value).__name__,
        )
    return (
        _require_count(value[0], "rank0"),
        _require_count(value[1], "rank1"),
        _require_count(value[2], "betti"),
    )


def _require_defect(value: object) -> Fraction:
    _refuse_float(value, "defect")
    if type(value) is bool:
        raise _fail(DimensionMismatchError, "boolean refused where a rational was required", role="defect")
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail(
        DimensionMismatchError,
        "boundary defect is not an exact rational",
        received=type(value).__name__,
    )


def _require_square(defect: Fraction) -> None:
    if defect != 0:
        raise _fail(NonZeroCompositionError, "triangle boundary square has a defect", defect=str(defect))


_FILLED_BETTI = (2, 1, 0)


def _require_betti(rank0: int, rank1: int, betti: int) -> None:
    if (rank0, rank1, betti) != _FILLED_BETTI:
        raise _fail(
            DimensionMismatchError,
            "triangle Betti triple is not (2, 1, 0)",
            rank0=rank0,
            rank1=rank1,
            betti=betti,
        )


def _closure_bit(defect: Fraction) -> int:
    if defect == 0:
        return 1
    return 0


def exported_triangle_rank_sum() -> int:
    """Return 4 when the Betti triple is (2, 1, 0) and the boundary defect is 0."""
    rank0, rank1, betti = _require_triple(triangle_betti())
    defect = _require_defect(triangle_boundary_defect())
    _require_square(defect)
    _require_betti(rank0, rank1, betti)
    return rank0 + rank1 + betti + _closure_bit(defect)


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
    "exported_triangle_rank_sum",
]
