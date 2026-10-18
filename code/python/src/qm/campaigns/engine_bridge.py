"""Bridge from a rational qubit amplitude to the expectation of Z.

Origin: code/python/src/qm/campaigns/engine_bridge.py
Claim: the state (3/5, 4/5) has <Z> = 9/25 − 16/25 = −7/25, and its norm is 1.
AuthorityEffect: None.
"""
from fractions import Fraction


class BridgeError(Exception):
    """The amplitude was not a rational unit vector."""


def z_expectation(amplitude) -> Fraction:
    if len(amplitude) != 2:
        raise BridgeError("the bridge expects a qubit amplitude")
    up = Fraction(amplitude[0])
    down = Fraction(amplitude[1])
    norm = up * up + down * down
    if norm != 1:
        raise BridgeError(f"amplitude norm is {norm}, not 1")
    return up * up - down * down


def pythagorean_expectation() -> Fraction:
    value = z_expectation((Fraction(3, 5), Fraction(4, 5)))
    if value != Fraction(9, 25) - Fraction(16, 25):
        raise BridgeError(f"expectation {value} disagrees with the population difference")
    return value
