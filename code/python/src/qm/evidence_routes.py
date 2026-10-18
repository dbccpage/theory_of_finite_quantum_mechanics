"""Route a rational witness through a recomputed digest.

The parent digest is the SHA-256 of the two child digests concatenated.
A second hashing of those same bytes is compared with the parent.
"""
import hashlib
from fractions import Fraction


class EvidenceRouteError(Exception):
    """The routed digest did not reproduce."""


def route_digest_length() -> int:
    """Return the byte length of a parent digest that matches its rebuild."""
    left = hashlib.sha256(f"{Fraction(2, 3)}".encode("ascii")).digest()
    right = hashlib.sha256(f"{Fraction(4, 5)}".encode("ascii")).digest()
    parent = hashlib.sha256(left + right).digest()
    rebuilt = hashlib.sha256(bytes(left) + bytes(right)).digest()
    if parent != rebuilt:
        raise EvidenceRouteError("parent digest did not rebuild")
    if len(parent) != 32:
        raise EvidenceRouteError(f"digest length is {len(parent)}")
    return len(parent)
