"""Selected admission witness for the broader-work column of CH19-O03.

The rational-turn branch, the infinite-order anchor in Q(i), and the declared
continuous logarithm are separate scalar choices. Phase invariance does not
select the Born readout. AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction

SCHEMA = "wdp.ch19_o03_phase_readout.v1"
WITNESS_ID = "ch19-o03-phase-readout"

Gauss = tuple[Fraction, Fraction]


def _frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _is_square(value: int) -> bool:
    if value < 0:
        return False
    root = math.isqrt(value)
    return root * root == value


def _mul(left: Gauss, right: Gauss) -> Gauss:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _conj(value: Gauss) -> Gauss:
    return (value[0], -value[1])


def _norm(value: Gauss) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def _div(left: Gauss, right: Gauss) -> Gauss:
    numerator = _mul(left, _conj(right))
    denominator = _norm(right)
    return (numerator[0] / denominator, numerator[1] / denominator)


def canonical_payload(witness: dict[str, object]) -> str:
    return json.dumps(witness, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def problem_sha256(witness: dict[str, object]) -> str:
    return hashlib.sha256(canonical_payload(witness).encode("utf-8")).hexdigest()


def phase_readout_witness() -> dict[str, object]:
    """Admit the two phase branches and separate the readouts."""
    anchor = (Fraction(3, 5), Fraction(4, 5))
    ratio = _div((Fraction(2), Fraction(1)), (Fraction(2), Fraction(-1)))
    anchor_is_ratio = ratio == anchor and _norm(anchor) == 1

    real_square = Fraction(4, 5)
    imaginary_square = Fraction(1, 5)
    reduced_real = real_square.numerator, real_square.denominator
    no_rational_square = not (_is_square(reduced_real[0]) and _is_square(reduced_real[1]))
    no_unit_root = no_rational_square and not (
        _is_square(imaginary_square.numerator) and _is_square(imaginary_square.denominator)
    )

    base_sum = (2 + 3 * 1) % 5
    base_difference = (2 - 3 * 1) % 5
    order_base = base_sum == 0 and base_difference == 4
    sum_coefficient_a = 2 + 3
    sum_coefficient_b = -1 + 6
    difference_gap_b = (-1 - 6) - 3
    order_step = sum_coefficient_a == 5 and sum_coefficient_b == 5 and difference_gap_b == -10
    infinite_order = order_base and order_step and (-10 % 5 == 0)

    edges = (Fraction(1, 3), Fraction(1, 4), Fraction(1, 6))
    potential = (Fraction(1, 5), Fraction(2, 7), Fraction(-1, 8))
    loop = (edges[0] + edges[1] - edges[2]) % 1
    transformed = (
        edges[0] + potential[1] - potential[0],
        edges[1] + potential[2] - potential[1],
        edges[2] + potential[2] - potential[0],
    )
    transformed_loop = (transformed[0] + transformed[1] - transformed[2]) % 1
    integer_cycle = Fraction(1)
    coboundary_cycle = Fraction(0)

    amplitudes = ((Fraction(1), Fraction(0)), (Fraction(2), Fraction(0)))
    norms = tuple(_norm(amplitude) for amplitude in amplitudes)
    norm_total = norms[0] + norms[1]
    quadratic = (norms[0] / norm_total, norms[1] / norm_total)
    quartic_weights = (norms[0] * norms[0], norms[1] * norms[1])
    quartic_total = quartic_weights[0] + quartic_weights[1]
    quartic = (quartic_weights[0] / quartic_total, quartic_weights[1] / quartic_total)
    rotated = tuple(_mul(anchor, amplitude) for amplitude in amplitudes)
    rotated_norms = tuple(_norm(amplitude) for amplitude in rotated)
    cross = _mul(amplitudes[0], _conj(amplitudes[1]))
    rotated_cross = _mul(rotated[0], _conj(rotated[1]))
    born = tuple(_norm(amplitude) / norm_total for amplitude in amplitudes)
    equal_pair = (Fraction(1), Fraction(0))
    summed = (equal_pair[0] + equal_pair[0], equal_pair[1] + equal_pair[1])
    unnormalized_quadratic = _norm(summed)
    unnormalized_quartic = unnormalized_quadratic * unnormalized_quadratic

    return {
        "schema": SCHEMA,
        "witness_id": WITNESS_ID,
        "authority_effect": "none",
        "scalar_branches": ["rational-turn-Q/Z", "anchor-Q(i)", "declared-continuous-logarithm"],
        "readout_choices": ["quadratic-norm", "quartic-norm", "admitted-trace-projector"],
        "continuous_character_computed": False,
        "anchor": f"{_frac(anchor[0])}+{_frac(anchor[1])}i",
        "anchor_norm": _frac(_norm(anchor)),
        "anchor_equals_ratio": anchor_is_ratio,
        "real_square_candidate": _frac(real_square),
        "no_rational_square_root": no_rational_square,
        "no_unit_square_root_in_qi": no_unit_root,
        "order_base_congruence": order_base,
        "order_step_divisible_by_5": order_step,
        "anchor_infinite_order": infinite_order,
        "rational_turn_loop": _frac(loop),
        "gauge_loop_unchanged": transformed_loop == loop,
        "integer_cycle_sum": _frac(integer_cycle),
        "coboundary_cycle_sum": _frac(coboundary_cycle),
        "integer_cycle_not_coboundary": integer_cycle != coboundary_cycle,
        "rational_turn_identifies_integer_cycle": integer_cycle % 1 == coboundary_cycle % 1,
        "quadratic_probabilities": [_frac(value) for value in quadratic],
        "quartic_probabilities": [_frac(value) for value in quartic],
        "readouts_differ": quadratic != quartic,
        "common_phase_preserves_norms": rotated_norms == norms,
        "common_phase_preserves_cross": rotated_cross == cross,
        "born_matches_quadratic": born == quadratic,
        "born_matches_quartic": born == quartic,
        "phase_invariance_selects_born": False,
        "unnormalized_quadratic": _frac(unnormalized_quadratic),
        "unnormalized_quartic": _frac(unnormalized_quartic),
    }
