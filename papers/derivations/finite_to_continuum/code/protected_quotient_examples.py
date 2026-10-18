"""Exact finite replay of the proper-dense protected-subgroup obstruction.

AuthorityEffect: None. The all-level argument is in the companion derivation.
Reuse the existing dyadic presentation owner and exact circle metric. The
six-primary coordinate functions add only the new tower's arithmetic; the
dyadic owner is not relabelled as a six-primary presentation.
"""

from __future__ import annotations

import json
from fractions import Fraction

from coda_inductive_presentation import CyclicPresentation
from interval_calculus import _validate_exact_int, _validate_exact_rational
from presentation_duality import circle_distance

OBSTRUCTION = "PROTECTED_QUOTIENT_NOT_PC"


def _level(value: int) -> int:
    value = _validate_exact_int(value, "level")
    if value < 0:
        raise ValueError("level must be nonnegative")
    return value


def crt_residue(level: int) -> int:
    """Unique a in [0,6**n) with a=0 mod 2**n and a=1 mod 3**n."""
    level = _level(level)
    two, three = 2**level, 3**level
    return (two * pow(two, -1, three)) % (two * three)


def six_coordinate(level: int, numerator: int) -> Fraction:
    order = 6 ** _level(level)
    numerator = _validate_exact_int(numerator, "numerator")
    if not 0 <= numerator < order:
        raise ValueError("numerator outside the finite cyclic carrier")
    return Fraction(numerator, order)


def six_transition(level: int, numerator: int) -> int:
    six_coordinate(level, numerator)
    return 6 * numerator


def six_coordinates(point: Fraction | int | str) -> tuple[int, int]:
    """Normalize a point of Z[1/6]/Z; reject other rational denominators."""
    point = _validate_exact_rational(point, "point") % 1
    rest = point.denominator
    valuations = []
    for prime in (2, 3):
        exponent = 0
        while rest % prime == 0:
            rest //= prime
            exponent += 1
        valuations.append(exponent)
    if rest != 1:
        raise ValueError("point is outside Z[1/6]/Z")
    level = max(valuations)
    return level, point.numerator * (6**level // point.denominator)


def three_primary_character(point: Fraction | int | str) -> Fraction:
    level, numerator = six_coordinates(point)
    return Fraction(crt_residue(level) * numerator, 6**level) % 1


def discontinuity_point(level: int) -> Fraction:
    level = _level(level)
    if level == 0:
        raise ValueError("the discontinuity sequence starts at level one")
    order = 2**level
    return Fraction(1, 3) - Fraction(order // 3, order)


def protected_quotient_witness(delta: Fraction | int | str) -> dict:
    """Construct a strict PC refusal for each supplied positive rational delta."""
    delta = _validate_exact_rational(delta, "delta")
    if delta <= 0:
        raise ValueError("delta must be positive")
    level = 1
    while Fraction(1, 2**level) >= delta:
        level += 1
    point = discontinuity_point(level)
    scaled = point * 6**level
    if scaled.denominator != 1:
        raise ArithmeticError("sequence point lacks its displayed six-primary coordinate")
    numerator = scaled.numerator
    return {
        "obstruction": OBSTRUCTION,
        "topology": "circle_subspace",
        "delta": delta,
        "epsilon": Fraction(1, 4),
        "level": level,
        "residue": crt_residue(level),
        "next_residue": crt_residue(level + 1),
        "numerator": numerator,
        "next_numerator": six_transition(level, numerator),
        "point": point,
        "character_value": three_primary_character(point),
    }


def verify_protected_witness(witness: dict) -> bool:
    """Verify supplied equations independently, without calling the constructor.

    In particular the CRT residues are checked by their congruences, not by
    repeating modular inversion. Submitted fields are never repaired.
    """
    fields = {
        "obstruction",
        "topology",
        "delta",
        "epsilon",
        "level",
        "residue",
        "next_residue",
        "numerator",
        "next_numerator",
        "point",
        "character_value",
    }
    if type(witness) is not dict or set(witness) != fields:
        return False
    try:
        level = _validate_exact_int(witness["level"], "level")
        residue = _validate_exact_int(witness["residue"], "residue")
        next_residue = _validate_exact_int(witness["next_residue"], "next_residue")
        numerator = _validate_exact_int(witness["numerator"], "numerator")
        next_numerator = _validate_exact_int(witness["next_numerator"], "next_numerator")
        delta = _validate_exact_rational(witness["delta"], "delta")
        epsilon = _validate_exact_rational(witness["epsilon"], "epsilon")
        point = _validate_exact_rational(witness["point"], "point")
        value = _validate_exact_rational(witness["character_value"], "character_value")
    except (TypeError, ValueError):
        return False
    if level < 1 or delta <= 0:
        return False
    order, two, three = 6**level, 2**level, 3**level
    return (
        witness["obstruction"] == OBSTRUCTION
        and witness["topology"] == "circle_subspace"
        and epsilon == Fraction(1, 4)
        and 0 <= residue < order
        and residue % two == 0
        and residue % three == 1
        and 0 <= next_residue < 6 * order
        and next_residue % (2 * two) == 0
        and next_residue % (3 * three) == 1
        and next_residue % order == residue
        and 0 <= numerator < order
        and next_numerator == 6 * numerator
        and point == Fraction(numerator, order) == Fraction(next_numerator, 6 * order)
        and point == Fraction(1, 3) - Fraction(two // 3, two)
        and value == Fraction(residue * numerator, order) % 1 == Fraction(1, 3)
        and 0 < circle_distance(point) < delta
        and circle_distance(value) >= epsilon
    )


def replay() -> dict:
    """A bounded replay; its status does not assert an infinite quantifier."""
    for level in range(9):
        dyadic = CyclicPresentation(level)
        for k in dyadic.elements:
            point = dyadic.dyadic_coordinate(k)
            if point != six_coordinate(level, k * 3**level):
                raise ArithmeticError("dyadic owner embedding disagrees")
            if three_primary_character(point) != 0:
                raise ArithmeticError("protected dyadic subgroup is not annihilated")
    radii = [Fraction(2), Fraction(1, 3), Fraction(1, 10), Fraction(1, 10**100)]
    witnesses = [protected_quotient_witness(delta) for delta in radii]
    if not all(verify_protected_witness(witness) for witness in witnesses):
        raise ArithmeticError("independent witness verification failed")
    return {
        "status": "PASS",
        "authority_effect": "None",
        "scope": "finite dyadic-owner levels 0..8 and four supplied rational radii",
        "infinite_quantifiers_checked": False,
        "witnesses": witnesses,
    }


if __name__ == "__main__":
    print(json.dumps(replay(), indent=2, default=str))
