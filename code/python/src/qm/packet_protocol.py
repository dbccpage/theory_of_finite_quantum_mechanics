"""Checksum of a rational packet payload.

The header stores the sum of the payload. A second pass recomputes that sum
from the payload alone and compares it with the header.
"""
from fractions import Fraction


class PacketProtocolError(Exception):
    """The packet checksum did not match the payload."""


def payload_checksum() -> Fraction:
    """Return the checksum of (1/2, 1/3, 1/7) after a second summation."""
    payload = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 7))
    header = Fraction(41, 42)
    recomputed = Fraction(0)
    for entry in payload:
        recomputed += entry
    if header != recomputed:
        raise PacketProtocolError(f"header {header} does not match {recomputed}")
    if any(entry <= 0 for entry in payload):
        raise PacketProtocolError("payload entries must be positive")
    return recomputed
