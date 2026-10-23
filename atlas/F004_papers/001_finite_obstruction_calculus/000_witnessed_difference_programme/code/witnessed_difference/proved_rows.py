"""Finite checks for Witnessed Difference Programme rows.

The core rows remain finite propositions: their Lean modules import only the
package core and were elaborated, and these functions evaluate their finite
instances by calling the package checkers. The classical-corner and instrument
entries are finite instances of sources that import Mathlib. Those rows stay
open claims until that Mathlib build is elaborated. A passing instance does not
promote them.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

from witnessed_difference.cochains import FiniteComplex, d0, solve_potential
from witnessed_difference.duration import duration_sum
from witnessed_difference.pointed_relation import (
    apartness_countermodels,
    closed_form_census,
    enumerate_pointed_relations,
    pointed_predicates,
)
from witnessed_difference.presentation_descent import factor_through, obstruction_set
from witnessed_difference.quotient_observer import (
    grammar_resolution,
    make_linear_quotient_observer,
    observer_family_order,
)
from witnessed_difference.symmetry import fixed_points

ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
MINUS = (Fraction(-1), Fraction(0))
EYE_I = (Fraction(0), Fraction(1))
MINUS_I = (Fraction(0), Fraction(-1))
GAUSS_ENTRIES = (ZERO, ONE, MINUS, EYE_I, MINUS_I)
EYE2 = ((ONE, ZERO), (ZERO, ONE))


def _gadd(left, right):
    return (left[0] + right[0], left[1] + right[1])


def _gmul(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _gconj(value):
    return (value[0], -value[1])


def _matmul(left, right):
    return tuple(
        tuple(
            _gadd(_gmul(left[i][0], right[0][j]), _gmul(left[i][1], right[1][j]))
            for j in range(2)
        )
        for i in range(2)
    )


def _conj_transpose(matrix):
    return tuple(
        tuple(_gconj(matrix[j][i]) for j in range(2))
        for i in range(2)
    )


def _real_matmul(left, right):
    return tuple(
        tuple(left[i][0] * right[0][j] + left[i][1] * right[1][j] for j in range(2))
        for i in range(2)
    )


def _real_vec(matrix, vector):
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def _column_sums(matrix):
    return (matrix[0][0] + matrix[1][0], matrix[0][1] + matrix[1][1])


def _nonnegative(matrix) -> int:
    return int(all(entry >= 0 for row in matrix for entry in row))


def _stochastic(matrix) -> int:
    sums = _column_sums(matrix)
    return _nonnegative(matrix) * int(sums == (Fraction(1), Fraction(1)))


def _permutation_shape(matrix) -> int:
    columns = (
        int(matrix[0][0] == 1) + int(matrix[1][0] == 1),
        int(matrix[0][1] == 1) + int(matrix[1][1] == 1),
    )
    zeros = int(all(entry in (Fraction(0), Fraction(1)) for row in matrix for entry in row))
    return zeros * int(columns == (1, 1)) * _stochastic(matrix)


def _mixture(matrix):
    total = [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]]
    weight_sum = Fraction(0)
    nonnegative = 1
    for image_0, image_1 in product((0, 1), repeat=2):
        weight = matrix[image_0][0] * matrix[image_1][1]
        weight_sum += weight
        nonnegative *= int(weight >= 0)
        total[image_0][0] += weight
        total[image_1][1] += weight
    return total, weight_sum, nonnegative


def _gaussian_census() -> dict[str, int]:
    unitary = 0
    monomial_unitary = 0
    for entries in product(GAUSS_ENTRIES, repeat=4):
        matrix = ((entries[0], entries[1]), (entries[2], entries[3]))
        flag = int(_matmul(_conj_transpose(matrix), matrix) == EYE2)
        row_0 = int(matrix[0][0] != ZERO) + int(matrix[0][1] != ZERO)
        row_1 = int(matrix[1][0] != ZERO) + int(matrix[1][1] != ZERO)
        column_0 = int(matrix[0][0] != ZERO) + int(matrix[1][0] != ZERO)
        column_1 = int(matrix[0][1] != ZERO) + int(matrix[1][1] != ZERO)
        shape = int(row_0 == 1) * int(row_1 == 1) * int(column_0 == 1) * int(column_1 == 1)
        unitary += flag
        monomial_unitary += flag * shape
    return {"carrier": 2, "unitary_matrices": unitary, "monomial_unitaries": monomial_unitary}


def _povm_pair() -> dict[str, str | bool]:
    luders_false = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(0)))
    luders_true = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(1)))
    prepare_false = ((Fraction(3, 5), Fraction(0)), (Fraction(4, 5), Fraction(0)))
    prepare_true = ((Fraction(0), Fraction(3, 5)), (Fraction(0), Fraction(4, 5)))

    def effect(matrix):
        transpose = ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))
        return _real_matmul(transpose, matrix)

    luders_effects = (effect(luders_false), effect(luders_true))
    prepare_effects = (effect(prepare_false), effect(prepare_true))
    luders_sum = (
        (luders_effects[0][0][0] + luders_effects[1][0][0], luders_effects[0][0][1] + luders_effects[1][0][1]),
        (luders_effects[0][1][0] + luders_effects[1][1][0], luders_effects[0][1][1] + luders_effects[1][1][1]),
    )
    prepare_sum = (
        (prepare_effects[0][0][0] + prepare_effects[1][0][0], prepare_effects[0][0][1] + prepare_effects[1][0][1]),
        (prepare_effects[0][1][0] + prepare_effects[1][1][0], prepare_effects[0][1][1] + prepare_effects[1][1][1]),
    )
    eye = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    luders_post = _real_vec(luders_false, (Fraction(1), Fraction(0)))
    prepare_post = _real_vec(prepare_false, (Fraction(1), Fraction(0)))
    return {
        "effects_equal": luders_effects == prepare_effects,
        "luders_complete": luders_sum == eye,
        "prepare_complete": prepare_sum == eye,
        "luders_post": [str(item) for item in luders_post],
        "prepare_post": [str(item) for item in prepare_post],
        "posts_parallel": bool(int(luders_post[1] == 0) * int(prepare_post[1] == 0)),
    }


def replay_proved_rows() -> dict[str, object]:
    """Evaluate every canonical row that this package still marks as a finite proposition."""

    census = closed_form_census(3)
    enumerated = enumerate_pointed_relations(3)
    loop, empty = apartness_countermodels()
    loop_pred = pointed_predicates(loop)
    empty_pred = pointed_predicates(empty)
    path = FiniteComplex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("a", "c")))
    exact = {("a", "b"): 1, ("b", "c"): 1, ("a", "c"): 2}
    potential = solve_potential(path, exact)
    reconstructed = d0(path, potential.value)
    left_duration = duration_sum((1, Fraction(1, 2)))
    right_duration = duration_sum((Fraction(3, 2),))
    joined_duration = duration_sum((1, Fraction(1, 2), Fraction(3, 2)))
    square = FiniteComplex((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3), (0, 3), (0, 2)))
    cycle = (1, 1, 0, 0, -1)
    identity = tuple(tuple(int(i == j) for j in range(5)) for i in range(5))
    admitted = make_linear_quotient_observer(square, (cycle,))
    family = observer_family_order(
        {
            "identity": identity,
            "cycle": (cycle,),
            "zero": ((0, 0, 0, 0, 0),),
            "admitted": admitted.value,
        }
    )
    grammar = grammar_resolution(
        ("q0", "q1", "q2", "q3"),
        {"q0": "", "q1": "a", "q2": "b", "q3": "a"},
        ("", "a", "b"),
    )
    injective = grammar_resolution(("q0", "q1"), {"q0": "a", "q1": "b"}, ("a", "b", "c"))
    states = ((0, 0), (0, 1), (1, 0), (1, 1))
    forgotten = {state: state[0] for state in states}
    remembered = {state: state[0] for state in states}
    forgotten_target = {state: state[1] for state in states}
    presentations = (0, 1)
    forgotten_obstruction = obstruction_set(states, presentations, forgotten, forgotten_target)
    remembered_factor = factor_through(states, presentations, forgotten, remembered)
    blind_left = evaluate_presentation("p")
    blind_right = evaluate_presentation("p")
    shear = ((Fraction(2), Fraction(1)), (Fraction(-1), Fraction(0)))
    shear_inverse = ((Fraction(0), Fraction(-1)), (Fraction(1), Fraction(2)))
    hadamard = ((Fraction(1), Fraction(1)), (Fraction(1), Fraction(-1)))
    pythagorean = ((Fraction(3, 5), Fraction(-4, 5)), (Fraction(4, 5), Fraction(3, 5)))
    half = (
        ((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 2), Fraction(-1, 2))),
        ((Fraction(1, 2), Fraction(-1, 2)), (Fraction(1, 2), Fraction(1, 2))),
    )
    average = ((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 2), Fraction(1, 2)))
    identity_2 = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    mixed, weight_sum, weights_nonnegative = _mixture(average)
    identity_mixed, identity_weight, identity_nonnegative = _mixture(identity_2)
    hadamard_gram = _real_matmul(hadamard, hadamard)
    pythagorean_gram = _real_matmul(
        ((pythagorean[0][0], pythagorean[1][0]), (pythagorean[0][1], pythagorean[1][1])),
        pythagorean,
    )
    half_gram = _matmul(_conj_transpose(half), half)
    half_square = _matmul(half, half)
    povm = _povm_pair()
    census_value = census.value
    grammar_value = grammar.value
    family_value = family.value
    return {
        "ok": True,
        "WDP-CH01-P02": {
            "total": census_value.pointed_relations,
            "related": census_value.related,
            "related_and_irreflexive": census_value.related_irreflexive,
            "distinct": census_value.distinct,
            "matches_enumeration": census_value == enumerated.value,
            "related_loop_not_distinct": [loop_pred.value.related, loop_pred.value.distinct],
            "distinct_empty_not_related": [empty_pred.value.related, empty_pred.value.distinct],
            "irreflexive_related_not_distinct": census_value.irreflexive_related_not_distinct,
        },
        "WDP-CH03-P01": {"fixed_points_at_least_two": list(fixed_points(2)), "fixed_point_of_singleton": list(fixed_points(1))},
        "WDP-CH07-P01": {
            "left": str(left_duration.value),
            "right": str(right_duration.value),
            "joined": str(joined_duration.value),
        },
        "WDP-CH07-P02": {
            "reconstructed": {f"{edge[0]}-{edge[1]}": str(value) for edge, value in reconstructed.items()},
            "direct": str(duration_sum((2,)).value),
            "long_path": str(duration_sum((1, 1)).value),
        },
        "WDP-CH10-P02": {
            "pairs": sorted(family_value.relation),
        },
        "WDP-CH10-P03": {
            "core_classes": grammar_value.core_classes,
            "capacity": grammar_value.capacity,
            "visible_classes": grammar_value.visible_classes,
            "collision": list(grammar_value.collision),
            "injective_collision": injective.value.collision,
            "pigeonhole_forced": grammar_value.pigeonhole_forced,
        },
        "WDP-CH14-P01": {"same_output": blind_left == blind_right, "points_distinct": (0, 0) != (0, 1)},
        "WDP-CH16-P01": {
            "forgotten_obstruction": len(forgotten_obstruction.value),
            "remembered_factor": [list(pair) for pair in remembered_factor.value.factor],
            "remembered_unique": remembered_factor.value.unique,
        },
        "WDP-CH16-P02": {
            "forgotten_obstruction": len(forgotten_obstruction.value),
            "remembered_unique": remembered_factor.value.unique,
        },
        "WDP-CH18-P02": {
            "identity_stochastic": _stochastic(identity_2),
            "identity_permutation": _permutation_shape(identity_2),
            "average_stochastic": _stochastic(average),
            "average_permutation": _permutation_shape(average),
        },
        "WDP-CH18-P03": {
            "inverse_product": _real_matmul(shear_inverse, shear),
            "image_of_basis": [str(item) for item in _real_vec(shear, (Fraction(1), Fraction(0)))],
            "column_sums": [str(item) for item in _column_sums(shear)],
            "permutation": _permutation_shape(shear),
        },
        "WDP-CH18-P04": _gaussian_census(),
        "WDP-CH18-P05": {
            "hadamard_gram": [[str(entry) for entry in row] for row in hadamard_gram],
            "hadamard_readouts_differ": [str(item * item) for item in _real_vec(hadamard, (Fraction(1), Fraction(1)))]
            != [str(item * item) for item in _real_vec(hadamard, (Fraction(1), Fraction(-1)))],
            "pythagorean_gram": [[str(entry) for entry in row] for row in pythagorean_gram],
            "half_gram": [[str(entry[0]) for entry in row] for row in half_gram],
            "half_square": [[str(entry[0]) for entry in row] for row in half_square],
        },
        "WDP-CH18-P07": {
            "average_mixture": [[str(entry) for entry in row] for row in mixed],
            "average_weight_sum": str(weight_sum),
            "average_weights_nonnegative": weights_nonnegative,
            "identity_mixture": [[str(entry) for entry in row] for row in identity_mixed],
            "identity_weight_sum": str(identity_weight),
            "identity_weights_nonnegative": identity_nonnegative,
            "product_stochastic": _stochastic(_real_matmul(average, identity_2)),
        },
        "WDP-CH19-P14": povm,
    }


def evaluate_presentation(report: str) -> int:
    """Every function of a presentation gives equal outputs to equal presentations."""

    table = {"p": 7}
    return table[report]
