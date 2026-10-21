"""Exported zero Phi1 certificate on the two-row boundary (1, -1).

Origin: lean4/DerivationDagQMClosure.lean theorem
l1_gs001_replica_and_phi1_quotient_invariance, recomputed by
code/python/src/functional/l1_seminorm.py.
Claim: urn:omega:fqm:phi1:exported-zero-quotient:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/functional/test_exported_zero_phi1.py.
Gate 5: use source-bound measurements in the companion history.
Scope Fence: exported_zero_phi1 checks one zero residual against the weights
(1, 1) and the boundary column (1, -1). It does not select L1 over a rival
seminorm and does not claim an authority grant from the zero value.
"""

from __future__ import annotations

from fractions import Fraction
from .l1_seminorm import (
    ExactPhi1Certificate,
    L1Seminorm,
    L1SeminormError,
    MAX_INPUT_BITS,
    VerifiedExactPhi1,
    evaluate_weighted_l1_quotient,
    require_positive_weights,
    require_rational,
    require_vector,
)

__all__ = [
    "ExactPhi1Certificate",
    "L1Seminorm",
    "L1SeminormError",
    "VerifiedExactPhi1",
    "evaluate_weighted_l1_quotient",
    "exported_zero_phi1",
    "require_positive_weights",
    "require_rational",
    "require_vector",
]


def _fail(invariant: str, **parameters: object) -> L1SeminormError:
    return L1SeminormError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _exact_int(value: object, role: str) -> int:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where an integer witness entry was required", role=role)
    if type(value) is not int:
        raise _fail("witness entry is not an exact integer", role=role, received=type(value).__name__)
    if value.bit_length() > MAX_INPUT_BITS:
        raise _fail("integer witness bit budget exceeded", role=role, bits=value.bit_length(), limit=MAX_INPUT_BITS)
    return value


def _pair(row: object, role: str) -> tuple[int, int]:
    if type(row) is not tuple or len(row) != 2:
        raise _fail("witness row must contain two entries", role=role, received=type(row).__name__)
    return (_exact_int(row[0], role + "_0"), _exact_int(row[1], role + "_1"))


def _rows(value: object, role: str) -> tuple[tuple[int, int], tuple[int, int]]:
    if type(value) is not tuple or len(value) != 2:
        raise _fail("witness must contain two rows", role=role, received=type(value).__name__)
    return (_pair(value[0], role + "_0"), _pair(value[1], role + "_1"))


def _column(rows: tuple[tuple[int, int], tuple[int, int]]) -> list[list[int]]:
    if rows[0][1] != 0 or rows[1][1] != 0:
        raise _fail("zero Phi1 witness must be a single boundary column")
    return [[rows[0][0]], [rows[1][0]]]


def _weights(rows: tuple[tuple[int, int], tuple[int, int]]) -> list[int]:
    if rows[0][0] != rows[0][1] or rows[1][0] != rows[1][1]:
        raise _fail("zero Phi1 weights must be a repeated positive pair")
    return [rows[0][0], rows[1][0]]


def exported_zero_phi1(boundary: object = None, weights: object = None) -> Fraction:
    """Phi1 of the zero section. Defaults are boundary (1, -1) and weights (1, 1)."""
    column = ((1, 0), (-1, 0)) if boundary is None else boundary
    repeated = ((1, 1), (1, 1)) if weights is None else weights
    parsed_column = _rows(column, "boundary")
    parsed_weights = _rows(repeated, "weights")
    return evaluate_weighted_l1_quotient(
        _column(parsed_column),
        _weights(parsed_weights),
        [0, 0],
        [0],
        [0, 0],
        [0, 0],
        0,
    )
