"""Exact finite witnesses for Lane E's circle presentation.

AuthorityEffect: None. Run this file with Python 3.12 to replay the witnesses.
Circle values are rational turns, not approximate complex exponentials. The
executable checks finite instances and constructs a witness for any supplied
positive rational radius. Infinite character classification, convergence,
non-local compactness, and duality are analytic statements in the companion
derivation; passing this executable does not mechanize those theorems.
"""

from __future__ import annotations

import json
from fractions import Fraction

from continuous_haar_limit import TrigPolynomial
from interval_calculus import _validate_exact_int, _validate_exact_rational
from presentation_closure_examples import character_average_by_polynomial

OBSTRUCTION_CHARACTER_DISCONTINUOUS = "OBSTRUCTION_CHARACTER_DISCONTINUOUS"


def _positive(value: Fraction | int, name: str) -> Fraction:
    result = _validate_exact_rational(value, name)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _natural(value: int, name: str) -> int:
    result = _validate_exact_int(value, name)
    if result < 0:
        raise ValueError(f"{name} must be nonnegative")
    return result


def circle_distance(x: Fraction | int, y: Fraction | int = 0) -> Fraction:
    """Distance on R/Z, with exact rational representatives in turns."""
    difference = (_validate_exact_rational(x, "x") - _validate_exact_rational(y, "y")) % 1
    return min(difference, 1 - difference)


def integer_character(frequency: int, x: Fraction | int) -> Fraction:
    """The integer character j evaluated at x, represented modulo one."""
    return (_validate_exact_int(frequency, "frequency") * _validate_exact_rational(x, "x")) % 1


def minus_one_third_residue(level: int) -> int:
    """The unique r in [0, 2**level) with 3*r = -1 modulo 2**level."""
    order = 1 << _natural(level, "level")
    return (-pow(3, -1, order)) % order


def minus_one_third_character(x: Fraction | int) -> Fraction:
    """Evaluate the algebraic 2-adic character on a dyadic circle point."""
    point = _validate_exact_rational(x, "x") % 1
    order = point.denominator
    if order & (order - 1):
        raise ValueError("character domain requires a dyadic denominator")
    residue = minus_one_third_residue(order.bit_length() - 1)
    return Fraction(residue * point.numerator, order) % 1


def minus_one_third_pc_witness(delta: Fraction | int) -> dict:
    """Construct x=4**(-m) with d(x,0)<delta and d(chi(x),0)>=1/5.

    For every m>=1, chi(x)=(4**m-1)/(3*4**m)>=1/4. Multiplying
    the integer denominator by four terminates for each positive rational
    delta. This construction is for the circle subspace metric; in the
    discrete metric d(x,0)=1 and does not tend to zero.
    """
    radius = _positive(delta, "delta")
    m, order = 1, 4
    while Fraction(1, order) >= radius:
        m, order = m + 1, order * 4
    return {
        "obstruction": OBSTRUCTION_CHARACTER_DISCONTINUOUS,
        "topology": "circle_subspace",
        "delta": radius,
        "epsilon": Fraction(1, 5),
        "m": m,
        "residue": (order - 1) // 3,
        "x": Fraction(1, order),
        "image": Fraction(order - 1, 3 * order),
    }


def verify_pc_witness(witness: dict) -> bool:
    """Independently check a submitted finite witness without repairing it."""
    required = {"obstruction", "topology", "delta", "epsilon", "m", "residue", "x", "image"}
    if not isinstance(witness, dict) or set(witness) != required:
        return False
    try:
        m = _natural(witness["m"], "m")
        residue = _natural(witness["residue"], "residue")
        delta = _positive(witness["delta"], "delta")
        epsilon = _positive(witness["epsilon"], "epsilon")
        x = _validate_exact_rational(witness["x"], "x")
        image = _validate_exact_rational(witness["image"], "image")
    except (TypeError, ValueError):
        return False
    order = 1 << (2 * m)
    return (
        witness["obstruction"] == OBSTRUCTION_CHARACTER_DISCONTINUOUS
        and witness["topology"] == "circle_subspace"
        and m >= 1
        and epsilon == Fraction(1, 5)
        and 0 <= residue < order
        and (3 * residue + 1) % order == 0
        and x == Fraction(1, order)
        and image == Fraction(residue, order)
        and image == minus_one_third_character(x)
        and circle_distance(x) < delta
        and circle_distance(image) >= epsilon
    )


def scaled_third_in_ball(radius: Fraction | int) -> Fraction:
    """Choose a=1/(3*2**s)<min(radius,1/4), which is never dyadic."""
    bound = min(_positive(radius, "radius"), Fraction(1, 4))
    scale = 2
    while Fraction(1, 3 * scale) >= bound:
        scale *= 2
    return Fraction(1, 3 * scale)


def dyadic_approximation(target: Fraction | int, level: int) -> Fraction:
    """Floor at mesh 2**(-level); 0 <= target-result < 2**(-level).

    For a scaled third the error is strictly positive at every level.
    Thus these points lie in the dyadic carrier, approach a point outside
    it, and for a=scaled_third_in_ball(radius) all remain in that ball.
    """
    point = _validate_exact_rational(target, "target")
    order = 1 << _natural(level, "level")
    return Fraction((point.numerator * order) // point.denominator, order)


def cauchy_tail_level(epsilon: Fraction | int) -> int:
    """Choose k with 2**(-k)<epsilon; any two later floors differ <epsilon."""
    bound = _positive(epsilon, "epsilon")
    level = 0
    while Fraction(1, 1 << level) >= bound:
        level += 1
    return level


def haar_quadrature(coefficients: dict, level: int) -> dict:
    """Replay Fourier averages in Q[z]/Phi_N(z) and compare the Haar owner.

    The finite polynomial replay has the owner's level bound 0..6.
    An exact average can result from cancellation of aliased frequencies;
    alias-free is therefore reported separately from a zero error.
    """
    level = _natural(level, "level")
    if level > 6:
        raise ValueError("cyclotomic replay supports levels 0 through 6")
    polynomial = TrigPolynomial(coefficients)
    average = sum(
        (
            coefficient * character_average_by_polynomial(level, frequency)
            for frequency, coefficient in polynomial.coefficients.items()
        ),
        Fraction(0),
    )
    if average != polynomial.discrete_riemann_sum(level):
        raise ArithmeticError("cyclotomic replay disagrees with finite Haar owner")
    order = 1 << level
    aliases = tuple(sorted(j for j in polynomial.coefficients if j != 0 and j % order == 0))
    return {
        "order": order,
        "max_frequency": polynomial.max_frequency,
        "alias_frequencies": aliases,
        "bandlimit_below_order": polynomial.max_frequency < order,
        "average": average,
        "integral": polynomial.exact_haar_integral,
        "error": abs(average - polynomial.exact_haar_integral),
    }


def triangle_wave(order: int, lipschitz: Fraction | int, x: Fraction | int) -> Fraction:
    """H_N(x)=L*dist(x,(1/N)Z), evaluated exactly and periodically."""
    order = _natural(order, "order")
    if order == 0:
        raise ValueError("order must be positive")
    slope = _validate_exact_rational(lipschitz, "lipschitz")
    if slope < 0:
        raise ValueError("lipschitz must be nonnegative")
    return slope * circle_distance(order * _validate_exact_rational(x, "x")) / order


def triangle_quadrature(level: int, lipschitz: Fraction | int) -> dict:
    """Integrate actual affine pieces; compare grid average and L/(2N).

    There are N triangular cells, each with base 1/N and height L/(2N).
    The exact integral and grid error are L/(4N). H_N changes with N;
    this is a sampling obstruction family, not samples of one fixed function.
    """
    level = _natural(level, "level")
    if level > 8:
        raise ValueError("triangle replay supports levels 0 through 8")
    order = 1 << level
    values = [triangle_wave(order, lipschitz, Fraction(k, 2 * order)) for k in range(2 * order + 1)]
    integral = sum((left + right for left, right in zip(values, values[1:])), Fraction(0)) / (
        4 * order
    )
    average = sum(values[:-1:2], Fraction(0)) / order
    slope = _validate_exact_rational(lipschitz, "lipschitz")
    return {
        "order": order,
        "average": average,
        "integral": integral,
        "error": abs(integral - average),
        "bound": slope / (2 * order),
    }


def verify_integer_characters() -> int:
    """Exhaust all ordered pairs at levels 0..8 for j=-5,-1,0,1,5."""
    count = 0
    for level in range(9):
        order = 1 << level
        distances = [circle_distance(Fraction(k, order)) for k in range(order)]
        for frequency in (-5, -1, 0, 1, 5):
            images = [integer_character(frequency, Fraction(k, order)) for k in range(order)]
            for left in range(order):
                for right in range(order):
                    if (
                        circle_distance(images[left], images[right])
                        > abs(frequency) * distances[(left - right) % order]
                    ):
                        raise ArithmeticError("integer character Lipschitz bound failed")
                    count += 1
    return count


def verify_examples() -> dict:
    """Replay finite cases; a PASS is not a check of the infinite theorems."""
    pairs = verify_integer_characters()
    radii = (Fraction(2), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2**80))
    witnesses = [minus_one_third_pc_witness(radius) for radius in radii]
    if not all(verify_pc_witness(witness) for witness in witnesses):
        raise ArithmeticError("PC witness failed")
    for radius in radii:
        target = scaled_third_in_ball(radius)
        if target.denominator & (target.denominator - 1) == 0:
            raise ArithmeticError("missing non-dyadic target")
        for level in range(100):
            point = dyadic_approximation(target, level)
            if not (
                circle_distance(point) < radius and 0 < target - point < Fraction(1, 1 << level)
            ):
                raise ArithmeticError("ball approximation failed")
    for level in range(7):
        fourier = haar_quadrature({-5: Fraction(2, 3), 0: 3, 5: 2}, level)
        if fourier["bandlimit_below_order"] and fourier["error"] != 0:
            raise ArithmeticError("bandlimited Haar recovery failed")
        triangle = triangle_quadrature(level, Fraction(7, 3))
        if not triangle["error"] == Fraction(7, 12 * (1 << level)) <= triangle["bound"]:
            raise ArithmeticError("triangle quadrature failed")
    return {
        "status": "PASS",
        "authority_effect": "None",
        "scope": "Exact finite checks under the declared circle metric presentation assumptions",
        "infinite_theorems_mechanized": False,
        "integer_character_ordered_pairs_checked": pairs,
        "ball_radii_checked": len(radii),
        "ball_levels_checked": 100,
        "haar_levels_checked": 7,
        "pc_witnesses": witnesses,
    }


def _json_rational(value: Fraction) -> str:
    if not isinstance(value, Fraction):
        raise TypeError(f"unsupported output type: {type(value).__name__}")
    return f"{value.numerator}/{value.denominator}"


if __name__ == "__main__":
    print(json.dumps(verify_examples(), indent=2, default=_json_rational))
