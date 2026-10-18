"""A two-amplitude rational packet and its squared norm.

The norm is the sum of squares. It is also the value of the Born weights
summed after each weight is formed on its own.
"""
from fractions import Fraction


class QuantumPacketError(Exception):
    """The packet norm was not 1."""


def packet_norm() -> Fraction:
    """Return ||(3/5, 4/5)||^2, checked against the sum of Born weights."""
    amplitudes = (Fraction(3, 5), Fraction(4, 5))
    norm = amplitudes[0] ** 2 + amplitudes[1] ** 2
    born = sum((amplitude * amplitude for amplitude in amplitudes), Fraction(0))
    if norm != born:
        raise QuantumPacketError(f"norm readings {norm} and {born} differ")
    if norm != 1:
        raise QuantumPacketError(f"packet norm is {norm}")
    return norm
