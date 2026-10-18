"""Square-free decomposition of a positive integer: n = square * square * radical.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/primitive_decomposition.py
Claim: urn:omega:fqm:ms-majorana:primitive-decomposition:square-split:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: This is integer arithmetic. It does not classify topological primitive cycles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class PrimitiveError(ValueError):
    """One violated decomposition invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> PrimitiveError:
    return PrimitiveError(invariant, parameters)


def _positive(value: object) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", received="float")
    if isinstance(value, bool) or type(value) is not int:
        raise _fail("boolean or non-integer refused", received=type(value).__name__)
    if value <= 0:
        raise _fail("positive integer required", received=value)
    return value


def _peel(rest: int, prime: int) -> tuple[int, int]:
    square = 1
    while rest % (prime * prime) == 0:
        rest //= prime * prime
        square *= prime
    return rest, square


def _split(value: int) -> tuple[int, int]:
    rest = value
    square = 1
    prime = 2
    while prime * prime <= rest:
        rest, factor = _peel(rest, prime)
        square *= factor
        if prime == 2:
            prime = 3
        else:
            prime += 2
    return square, rest


def _square_divides(radical: int) -> bool:
    prime = 2
    while prime * prime <= radical:
        if radical % (prime * prime) == 0:
            return True
        if prime == 2:
            prime = 3
        else:
            prime += 2
    return False


@dataclass(frozen=True)
class SquareSplitCertificate:
    """Witness that n = square^2 * radical and the radical is square-free."""

    value: int
    square: int
    radical: int


def certify_square_split(value: object) -> SquareSplitCertificate:
    """Split a positive integer and recheck the square-free identity."""
    parsed = _positive(value)
    square, radical = _split(parsed)
    if square * square * radical != parsed:
        raise _fail("square split does not rebuild the integer", value=parsed, square=square, radical=radical)
    if _square_divides(radical):
        raise _fail("radical is not square-free", radical=radical)
    return SquareSplitCertificate(parsed, square, radical)


__all__ = ["PrimitiveError", "SquareSplitCertificate", "certify_square_split"]
