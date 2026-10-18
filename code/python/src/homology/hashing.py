"""Cryptographic hashing for homology complexes and witnesses.

Origin: code/python/src/homology/hashing.py
Claim: two rational matrices with the same reduced entries share a digest, and a changed entry does not.
AuthorityEffect: None. The digest is a commitment, not a proof of nilpotency.
"""
import hashlib
from fractions import Fraction


def _canonical_entry(value) -> bytes:
    if hasattr(value, "canonical_bytes"):
        return value.canonical_bytes()
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}".encode("utf-8")
    if isinstance(value, int) and not isinstance(value, bool):
        return f"{value}/1".encode("utf-8")
    raise TypeError(f"matrix entry {value!r} has no canonical rational encoding")


def hash_matrix(mat) -> str:
    if hasattr(mat, "sha256"):
        return mat.sha256()
    rows = getattr(mat, "rows", None)
    cols = getattr(mat, "cols", None)
    data = getattr(mat, "data", None)
    if not isinstance(rows, int) or not isinstance(cols, int) or data is None:
        raise TypeError("hash_matrix requires a matrix with rows, cols, and data, or a sha256 method")
    if len(data) != rows * cols:
        raise ValueError(f"data length {len(data)} does not match {rows}x{cols}")
    digest = hashlib.sha256()
    digest.update(f"{rows}x{cols}:".encode("utf-8"))
    for entry in data:
        digest.update(_canonical_entry(entry))
        digest.update(b",")
    return digest.hexdigest()


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_distinguishes_entry() -> bool:
    """A one-entry change must change the digest. The two digests are computed, then compared."""

    class _Grid:
        def __init__(self, rows, cols, data):
            self.rows = rows
            self.cols = cols
            self.data = data

    left = hash_matrix(_Grid(2, 2, [Fraction(1, 2), Fraction(0), Fraction(0), Fraction(1)]))
    right = hash_matrix(_Grid(2, 2, [Fraction(1, 2), Fraction(0), Fraction(0), Fraction(2)]))
    same = hash_matrix(_Grid(2, 2, [Fraction(2, 4), Fraction(0), Fraction(0), Fraction(1, 1)]))
    return left == same and left != right
