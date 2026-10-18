"""Exact collision bound for a rational probability vector.

Cauchy's inequality on the uniform vector says n * sum p_i^2 >= (sum p_i)^2.
Both sides are computed from the same weights.
"""
from fractions import Fraction


class EntropyBoundError(Exception):
    """The weights are not a probability vector, or Cauchy fails."""


def collision_probability() -> Fraction:
    """Return sum p_i^2 for (1/2, 1/3, 1/6) after checking Cauchy.

    The collision sum and n times that sum are different expressions. The
    second is compared with (sum p_i)^2.
    """
    weights = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
    for weight in weights:
        if weight < 0:
            raise EntropyBoundError(f"weight {weight} is negative")
    mass = sum(weights, Fraction(0))
    if mass != 1:
        raise EntropyBoundError(f"weights sum to {mass}")
    collision = sum((weight * weight for weight in weights), Fraction(0))
    cauchy_left = Fraction(len(weights)) * collision
    cauchy_right = mass * mass
    if cauchy_left < cauchy_right:
        raise EntropyBoundError(f"Cauchy failed: {cauchy_left} < {cauchy_right}")
    return collision
