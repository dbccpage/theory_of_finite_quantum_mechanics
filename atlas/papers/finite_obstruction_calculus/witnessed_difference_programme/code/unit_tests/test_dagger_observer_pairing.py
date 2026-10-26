from __future__ import annotations

import copy

import pytest

from dagger_pairing.model import (
    apply_dagger,
    gram,
    observe,
    subtract,
    tensor_dagger,
    tensor_product,
    validate_involution,
)
from dagger_pairing.replay import check, produce, reference_problem


def test_dagger_is_involutive_and_additive_on_sparse_coordinates() -> None:
    dagger = {"a": "A", "A": "a", "b": "b"}
    value = {"a": 2, "A": -1, "b": 3}
    assert apply_dagger(apply_dagger(value, dagger), dagger) == value


def test_invalid_dagger_is_refused() -> None:
    with pytest.raises(ValueError, match="involutive"):
        validate_involution({"a": "b", "b": "c", "c": "a"})


def test_dagger_commutes_with_tensor_pairing() -> None:
    problem = reference_problem()
    raw = tensor_product(problem["left_vector"], problem["right_vector"])
    assert tensor_dagger(raw, problem["left_dagger"], problem["right_dagger"]) == tensor_product(
        apply_dagger(problem["left_vector"], problem["left_dagger"]),
        apply_dagger(problem["right_vector"], problem["right_dagger"]),
    )


def test_observer_gram_radical_is_the_blind_kernel() -> None:
    problem = reference_problem()
    blind = problem["blind_difference"]
    visible = problem["visible_difference"]
    rows = problem["observer_rows"]
    assert observe(blind, rows) == (0, 0)
    assert gram(blind, blind, rows) == 0
    assert observe(visible, rows) == (1, -2)
    assert gram(visible, visible, rows) == 5


def test_equal_reports_are_null_differences() -> None:
    problem = reference_problem()
    left, right = problem["equal_report_states"]
    rows = problem["observer_rows"]
    difference = subtract(left, right)
    assert observe(left, rows) == observe(right, rows)
    assert gram(difference, difference, rows) == 0


def test_exact_integer_admission_rejects_float() -> None:
    with pytest.raises(ValueError, match="exact integers"):
        observe({"a": 0.5}, [{"a": 1}])  # type: ignore[arg-type]


def test_exhaustive_bound_rejects_bool_and_truncated_values() -> None:
    problem = reference_problem()
    for bad in (True, 1.5, -1):
        changed = copy.deepcopy(problem)
        changed["exhaustive_coefficient_bound"] = bad
        with pytest.raises(ValueError, match="nonnegative integer"):
            produce(changed)


def test_receipt_is_bound_and_tamper_evident() -> None:
    problem = reference_problem()
    receipt = produce(problem)
    check(problem, receipt)
    tampered = copy.deepcopy(receipt)
    tampered["observer_pairing"]["visible_norm_square"] = 0
    with pytest.raises(ValueError, match="does not replay"):
        check(problem, tampered)
