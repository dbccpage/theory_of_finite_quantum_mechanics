"""CLI boundary check that the rational identity trace equals its dimension.

Origin: lean4/H056ContinuumLiftBoundary.lean theorem trace_scalar_identity
(Tr(k * I_2) = 2 * k) and lean4/H047StoneVonNeumannObstruction.lean theorem
tr_eye3_nonzero (tr3 eye3 = 3).
Claim: urn:omega:fqm:linear-algebra:cli-identity-trace:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_finite_cli.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: cli_identity_trace sums the diagonal of the rational identity of
the size it is given, before any CLI dispatch. The cited theorems cover
dimension 2 for any integer scale and dimension 3 for the unscaled identity
only. This file does not prove Tr(k I_n) = n * k for arbitrary n, and it does
not prove the Heisenberg or Wintner-Wielandt obstruction.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from ..linear_algebra.matrix import ExactMatrix as ExactMatrix
from ..qm.cli import main as main


class CliTraceError(Exception):
    """One violated CLI identity-trace invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CliTraceError:
    return CliTraceError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the cli boundary", role=role, received="float")


def _require_size(value: object) -> int:
    _refuse_float(value, "size")
    if type(value) is bool:
        raise _fail("boolean refused where a cli size was required", role="size")
    if type(value) is int:
        size = value
        if size < 0:
            raise _fail("cli size is negative", role="size", received=size)
        return size
    raise _fail("cli size is not an integer", role="size", received=type(value).__name__)


def _require_diagonal(entry: object, index: int) -> Fraction:
    if type(entry) is float:
        raise _fail("float refused on the cli diagonal", index=index)
    if type(entry) is bool:
        raise _fail("boolean refused on the cli diagonal", index=index)
    if isinstance(entry, Fraction):
        return entry
    if type(entry) is int:
        return Fraction(entry)
    raise _fail(
        "cli diagonal entry is not an exact rational",
        index=index,
        received=type(entry).__name__,
    )


def _sum_diagonal(eye: ExactMatrix) -> Fraction:
    total = Fraction(0)
    width = eye.rows
    for index in range(width):
        total += _require_diagonal(eye.get(index, index), index)
    return total


def _require_trace(total: Fraction, size: int) -> Fraction:
    expected = Fraction(size)
    if total != expected:
        raise _fail("cli identity trace is not the dimension", trace=str(total), size=size)
    return total


def cli_identity_trace(size: int = 2) -> Fraction:
    """Sum the diagonal of the rational identity before CLI dispatch."""
    width = _require_size(size)
    return _require_trace(_sum_diagonal(ExactMatrix.identity(width)), width)


if __name__ == "__main__":
    main()
