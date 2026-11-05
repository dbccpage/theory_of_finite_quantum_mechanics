"""Exact input admission for the independent-checking bounded context.

Collection admission returns immutable snapshots in linear work and storage.
Rational components have at most 4096 bits; sequences at most 4096 entries.
Refusals are converted to Railway failures by evaluate. AuthorityEffect: None.
"""
from fractions import Fraction
from typing import cast
from dataclasses import dataclass
from typing import Literal


FailureKind = Literal["input", "resource", "check", "duplicate"]
FAILURE_KINDS = frozenset(("input", "resource", "check", "duplicate"))


@dataclass(frozen=True, slots=True)
class Failure:
    """A refused input, exceeded resource budget, or failed verification invariant."""

    kind: FailureKind
    message: str

    def __post_init__(self) -> None:
        if type(self.kind) is not str or self.kind not in FAILURE_KINDS:
            raise ValueError("unknown independent-checker failure kind")
        if type(self.message) is not str or not self.message.strip():
            raise ValueError("failure message must be nonempty text")

    def to_record(self) -> dict[str, str]:
        """Stable wire representation, copied so callers cannot mutate the value object."""
        return {"kind": self.kind, "message": self.message}


def _violation(kind: FailureKind, message: str) -> ValueError:
    from .boundary import Violation
    return Violation(kind, message)

MAX_RATIONAL_BITS = 4096
MAX_SEQUENCE_LENGTH = 4096


def _limits(minimum: int | None, maximum: int | None) -> None:
    for bound in (minimum, maximum):
        if bound is not None and type(bound) is not int:
            raise _violation("input", "integer limits exclude bool and non-integers")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise _violation("input", "minimum exceeds maximum")


def integer(value: object, name: str = "integer", minimum: int | None = None,
            maximum: int | None = None) -> int:
    _limits(minimum, maximum)
    if type(value) is not int:
        raise _violation("input", f"{name} must be an integer, excluding bool")
    if minimum is not None and value < minimum:
        raise _violation("input", f"{name} must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise _violation("resource", f"{name} must be <= {maximum}")
    return value


def _exact_fraction(value: object, name: str) -> Fraction:
    if type(value) is int:
        value = Fraction(value)
    if type(value) is not Fraction:
        raise _violation("input", f"{name} requires int or Fraction, excluding bool/float")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_RATIONAL_BITS:
        raise _violation("resource", f"{name} exceeds the {MAX_RATIONAL_BITS}-bit rational budget")
    return value


def rational(value: object, name: str = "rational", minimum: int | Fraction | None = None,
             strictly_positive: bool = False) -> Fraction:
    admitted = _exact_fraction(value, name)
    if type(strictly_positive) is not bool:
        raise _violation("input", "strictly_positive must be a bool")
    if minimum is not None and admitted < _exact_fraction(minimum, "minimum"):
        raise _violation("input", f"{name} must be >= {minimum}")
    if strictly_positive and admitted <= 0:
        raise _violation("input", f"{name} must be positive")
    return admitted


def sequence(value: object, name: str = "sequence", size: int | None = None,
             maximum: int = MAX_SEQUENCE_LENGTH) -> tuple[object, ...]:
    integer(maximum, "sequence budget", 0, MAX_SEQUENCE_LENGTH)
    if size is not None:
        integer(size, "sequence size", 0, maximum)
    if type(value) not in (tuple, list):
        raise _violation("input", f"{name} must be a list or tuple")
    carrier = cast("tuple[object, ...] | list[object]", value)
    if len(carrier) > maximum:
        raise _violation("resource", f"{name} exceeds {maximum} entries")
    snapshot = tuple(carrier)
    if size is not None and len(snapshot) != size:
        raise _violation("input", f"{name} must have {size} entries")
    return snapshot


def integer_matrix(value: object, rows: int | None = None,
                   cols: int | None = None) -> tuple[tuple[int, ...], ...]:
    carrier = sequence(value, "matrix", rows)
    if not carrier:
        raise _violation("input", "matrix must be nonempty")
    first = sequence(carrier[0], "row", cols)
    if not first:
        raise _violation("input", "matrix rows must be nonempty")
    if len(carrier) * len(first) > MAX_SEQUENCE_LENGTH:
        raise _violation("resource", "matrix exceeds the 4096-entry budget")
    return tuple(tuple(integer(x, "matrix entry") for x in sequence(row, "row", len(first)))
                 for row in carrier)


def flat_matrix2(value: object) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    a, b, c, d = sequence(value, "2x2 matrix", 4)
    return rational(a), rational(b), rational(c), rational(d)


def binary_word(word: object) -> tuple[bool, ...]:
    snapshot = sequence(word, "binary word", maximum=64)
    if any(type(x) is not bool for x in snapshot):
        raise _violation("input", "binary words contain bool values only")
    return cast(tuple[bool, ...], snapshot)


def permutation3(value: object) -> tuple[int, int, int]:
    snapshot = sequence(value, "S3 permutation", 3)
    if any(type(x) is not int for x in snapshot):
        raise _violation("input", "S3 entries must be integers excluding bool")
    if set(snapshot) != {0, 1, 2}:
        raise _violation("input", "S3 permutation must contain 0, 1, 2 exactly once")
    return cast(tuple[int, int, int], snapshot)


def hole(word: object, left: object, lhs: object, rhs: object, right: object) -> list[int]:
    segments = [tuple(integer(x, "symbol") for x in sequence(segment, "word segment"))
                for segment in (word, left, lhs, rhs, right)]
    word_value, prefix, before, after, suffix = segments
    if word_value != prefix + before + suffix:
        raise _violation("input", "word does not match the supplied one-hole split")
    result = prefix + after + suffix
    sequence(result, "replacement word")
    return list(result)
