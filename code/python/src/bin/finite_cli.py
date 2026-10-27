"""CLI boundary check that the rational identity trace equals its dimension.

Origin: lean4/ContinuumLiftBoundary.lean theorem trace_scalar_identity
(Tr(k * I_2) = 2 * k) and lean4/StoneVonNeumannObstruction.lean theorem
tr_eye3_nonzero (tr3 eye3 = 3).
Claim: urn:omega:fqm:linear-algebra:cli-identity-trace:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_finite_cli.py.
Gate 5: use the source-bound measurements in the companion history.
Scope Fence: cli_identity_trace sums the diagonal of the rational identity
when explicitly called. main is a bounded argument/status adapter to qm.cli;
it does not automatically run this trace check. The cited theorems cover
dimension 2 for any integer scale and dimension 3 for the unscaled identity
only. This file does not prove Tr(k I_n) = n * k for arbitrary n, and it does
not prove the Heisenberg or Wintner-Wielandt obstruction.
"""

from __future__ import annotations

from fractions import Fraction
import sys
from typing import Mapping

from ..linear_algebra.matrix import ExactMatrix as ExactMatrix, MatrixError
from ..qm.cli import main as _dispatch

# Explicit adapter budgets, not bounds claimed for delegated scientific suites.
MAX_IDENTITY_DIMENSION = 256
MAX_ARGUMENTS = 64
MAX_ARGUMENT_CHARACTERS = 4096


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
    if issubclass(type(value), float):
        raise _fail("float refused at the cli boundary", role=role, received="float")


def _require_size(value: object) -> int:
    _refuse_float(value, "size")
    if type(value) is bool:
        raise _fail("boolean refused where a cli size was required", role="size")
    if type(value) is int:
        size = value
        if size.bit_length() > MAX_IDENTITY_DIMENSION.bit_length():
            raise _fail("cli identity dimension budget exceeded", limit=MAX_IDENTITY_DIMENSION)
        if size < 0:
            raise _fail("cli size is negative", role="size", received=size)
        if size > MAX_IDENTITY_DIMENSION:
            raise _fail("cli identity dimension budget exceeded", limit=MAX_IDENTITY_DIMENSION)
        return size
    raise _fail("cli size is not an integer", role="size", received=type(value).__name__)


def _require_diagonal(entry: object, index: int) -> Fraction:
    if type(entry) is float:
        raise _fail("float refused on the cli diagonal", index=index)
    if type(entry) is bool:
        raise _fail("boolean refused on the cli diagonal", index=index)
    if type(entry) is Fraction:
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
    try:
        eye = ExactMatrix.identity(width)
        return _require_trace(_sum_diagonal(eye), width)
    except MatrixError as error:
        raise _fail("identity matrix provider failed", provider_error=type(error).__name__) from error


def _arguments(argv: object) -> list[str]:
    if type(argv) not in (list, tuple):
        raise _fail("cli arguments must be a built-in sequence", received=type(argv).__name__)
    if len(argv) > MAX_ARGUMENTS:
        raise _fail("cli argument count budget exceeded", limit=MAX_ARGUMENTS)
    result = []
    for argument in argv:
        if type(argument) is not str:
            raise _fail("cli argument must be a built-in string", received=type(argument).__name__)
        if len(argument) > MAX_ARGUMENT_CHARACTERS:
            raise _fail("cli argument length budget exceeded", limit=MAX_ARGUMENT_CHARACTERS)
        result.append(argument)
    return result


def main(argv: object = None) -> int:
    """Bound adapter inputs and preserve dispatcher success/help/error statuses.

    Suite computation and file/evidence validation are delegated to qm.cli;
    this adapter does not certify their scientific claims or resource bounds.
    """
    try:
        arguments = _arguments(sys.argv[1:] if argv is None else argv)
        result = _dispatch(arguments)
    except SystemExit as error:
        return error.code if type(error.code) is int and error.code in (0, 1, 2) else 2
    except (CliTraceError, OSError, ValueError):
        return 2
    return result if type(result) is int and result in (0, 1, 2) else 2


if __name__ == "__main__":
    raise SystemExit(main())
