"""Exported binomial witness C(6, 3) = 20, checked against the counting neighbors.

Origin: code/rust/src/combinatorics/enumeration.rs function binomial.
Claim: urn:omega:fqm:combinatorics:exported-binomial-six-three:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/combinatorics/test_exported_binomial.py.
Gate 5: use source-bound measurements in the companion history.
Scope Fence: exported_binomial returns 20 only for the frozen pair (6, 3)
or an explicit equal call. It does not claim a projective plane exists and
does not prove the Weyl trace obstruction.
"""

from __future__ import annotations

from typing import Mapping

from .finite_combinatorics import (
    CombinatoricsBudgetError,
    CombinatoricsError,
    FiniteProjectivePlaneParams,
    MAX_INPUT_BITS,
    binomial_exact,
    enumerate_cartesian_words,
    finite_plane_parameters,
    integer_partitions,
    weyl_heisenberg_displacement_count,
)

__all__ = [
    "CombinatoricsBudgetError",
    "CombinatoricsError",
    "FiniteProjectivePlaneParams",
    "binomial_exact",
    "enumerate_cartesian_words",
    "exported_binomial",
    "finite_plane_parameters",
    "integer_partitions",
    "weyl_heisenberg_displacement_count",
]


def _fail(invariant: str, **parameters: object) -> CombinatoricsError:
    return CombinatoricsError(invariant, parameters)


def _exact_int(value: object, role: str) -> int:
    if issubclass(type(value), float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer was required", role=role)
    if type(value) is not int:
        raise _fail("binomial argument is not an exact integer", role=role, received=type(value).__name__)
    if value.bit_length() > MAX_INPUT_BITS:
        raise CombinatoricsBudgetError("input integer bit budget exceeded", {"role": role, "bits": value.bit_length(), "limit": MAX_INPUT_BITS})
    return value


def _require_pair(n: object, k: object) -> tuple[int, int]:
    left = _exact_int(n, "n")
    right = _exact_int(k, "k")
    if (left, right) != (6, 3):
        raise _fail("exported binomial witness is only (6, 3)", n=left, k=right)
    return left, right


def _require_neighbors(value: int) -> None:
    if value != 20:
        raise _fail("binomial witness drifted from 20", received=value)
    if len(integer_partitions(4)) != 5:
        raise _fail("partition witness of 4 drifted from 5")
    plane = finite_plane_parameters(3)
    if plane.pg_points != 13 or plane.ag_lines != 12:
        raise _fail("plane counting witness drifted", points=plane.pg_points, lines=plane.ag_lines)
    if weyl_heisenberg_displacement_count(6) != (36, 35):
        raise _fail("displacement count witness drifted")


def exported_binomial(n: object = 6, k: object = 3) -> int:
    """Return C(6, 3) after the frozen neighbor counts agree."""
    left, right = _require_pair(n, k)
    value = binomial_exact(left, right)
    _require_neighbors(value)
    return value
