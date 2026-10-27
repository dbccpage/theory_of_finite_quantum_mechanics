"""Canonical digest of reduced rational matrix entries.

Origin: lean4/HilbertWalkRationals.lean definition qrel, equality of integer pairs by
cross-multiplication. Fraction reduction makes 1/2 and 2/4 the same entry.
Claim: urn:omega:fqm:homology:reduced-entry-digest:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_hashing.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 10; AST Sonar cognitive complexity max 9; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 10.
Scope Fence: The digest is a commitment to reduced entries. It is not a proof
of nilpotency, not a proof of the H001 star-ring pack, and not an authority grant.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from typing import Mapping, Sequence


class HashWitnessError(ValueError):
    """One violated digest invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> HashWitnessError:
    return HashWitnessError(invariant, parameters)


def _canonical_entry(value: object) -> bytes:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational entry was required", received="bool")
    canonical = getattr(value, "canonical_bytes", None)
    if callable(canonical):
        encoded = canonical()
        if isinstance(encoded, bytes):
            return encoded
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}".encode("utf-8")
    if isinstance(value, int):
        return f"{value}/1".encode("utf-8")
    raise _fail("matrix entry has no canonical rational encoding", received=type(value).__name__)


def _require_shape(rows: object, cols: object, data: object) -> tuple[int, int, Sequence[object]]:
    if isinstance(rows, bool) or isinstance(cols, bool):
        raise _fail("matrix shape refuses booleans", rows=type(rows).__name__, cols=type(cols).__name__)
    if not isinstance(rows, int) or not isinstance(cols, int) or not isinstance(data, Sequence) or isinstance(data, (str, bytes)):
        raise _fail(
            "hash_matrix requires rows, cols, and data",
            rows=type(rows).__name__,
            cols=type(cols).__name__,
            data=type(data).__name__,
        )
    if rows < 0 or cols < 0 or len(data) != rows * cols:
        raise _fail("data length does not match shape", rows=rows, cols=cols, length=len(data))
    return rows, cols, data


def hash_matrix(mat: object) -> str:
    """Digest reduced entries. Objects with sha256 delegate to that commitment."""
    digest_method = getattr(mat, "sha256", None)
    if callable(digest_method):
        digest = digest_method()
        if isinstance(digest, str):
            return digest
    rows, cols, data = _require_shape(
        getattr(mat, "rows", None),
        getattr(mat, "cols", None),
        getattr(mat, "data", None),
    )
    digest = hashlib.sha256()
    digest.update(f"{rows}x{cols}:".encode("utf-8"))
    for entry in data:
        digest.update(_canonical_entry(entry))
        digest.update(b",")
    return digest.hexdigest()


def hash_bytes(data: object) -> str:
    """SHA-256 of an exact byte string. Non-bytes are refused."""
    if not isinstance(data, bytes):
        raise _fail("hash_bytes requires bytes", received=type(data).__name__)
    return hashlib.sha256(data).hexdigest()


class _Grid:
    def __init__(self, rows: int, cols: int, data: Sequence[object]) -> None:
        self.rows = rows
        self.cols = cols
        self.data = data


def hash_distinguishes_entry() -> bool:
    """A one-entry change must change the digest. Reduced duplicates must not."""
    left = hash_matrix(_Grid(2, 2, [Fraction(1, 2), Fraction(0), Fraction(0), Fraction(1)]))
    right = hash_matrix(_Grid(2, 2, [Fraction(1, 2), Fraction(0), Fraction(0), Fraction(2)]))
    same = hash_matrix(_Grid(2, 2, [Fraction(2, 4), Fraction(0), Fraction(0), Fraction(1, 1)]))
    return left == same and left != right


__all__ = [
    "HashWitnessError",
    "hash_bytes",
    "hash_distinguishes_entry",
    "hash_matrix",
]
