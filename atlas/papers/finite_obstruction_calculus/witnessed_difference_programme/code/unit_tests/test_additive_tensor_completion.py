from __future__ import annotations

import copy

import pytest

from additive_tensor.model import (
    add_signed,
    alternative_counts,
    bilinear_value,
    determinant_2x2,
    fold_signed,
    negate_signed,
    normalize_signed,
    tensor_product,
)
from additive_tensor.replay import check, produce, reference_problem


def test_alternative_completion_erases_order_but_retains_multiplicity() -> None:
    assert alternative_counts(["a", "b", "a"]) == alternative_counts(["a", "a", "b"])
    assert alternative_counts(["a", "b", "a"]) != alternative_counts(["a", "b"])


def test_signed_completion_cancels_exactly() -> None:
    value = normalize_signed(["a", "b"], ["a"])
    assert value == {"b": 1}
    assert add_signed(value, negate_signed(value)) == {}
    assert fold_signed({"a": 4}, {"a": 0}) == 0


def test_tensor_is_bilinear_on_exact_integer_coordinates() -> None:
    a = {"a": 2, "b": -1}
    a_prime = {"a": -2, "b": 4}
    b = {"x": 1, "y": 3}
    assert tensor_product(add_signed(a, a_prime), b) == add_signed(
        tensor_product(a, b), tensor_product(a_prime, b)
    )


def test_bilinear_map_factors_through_tensor_coordinates() -> None:
    problem = reference_problem()
    assert bilinear_value(
        problem["left_vector"],
        problem["right_vector"],
        problem["basis_bilinear_values"],
    ) == sum(
        coefficient * problem["basis_bilinear_values"][pair]
        for pair, coefficient in tensor_product(
            problem["left_vector"], problem["right_vector"]
        ).items()
    )


def test_nonfactorable_tensor_is_not_mistaken_for_a_pure_tensor() -> None:
    problem = reference_problem()
    assert determinant_2x2(
        problem["nonfactorable_tensor"], ("a", "b"), ("x", "y")
    ) == 1


def test_exact_integer_admission_rejects_boolean_and_float() -> None:
    with pytest.raises(ValueError, match="exact integers"):
        tensor_product({"a": True}, {"x": 1})
    with pytest.raises(ValueError, match="exact integers"):
        tensor_product({"a": 0.5}, {"x": 1})  # type: ignore[arg-type]


def test_receipt_is_source_bound_and_tamper_evident() -> None:
    problem = reference_problem()
    receipt = produce(problem)
    check(problem, receipt)
    tampered = copy.deepcopy(receipt)
    tampered["tensor"]["factor_value"] += 1
    with pytest.raises(ValueError, match="does not replay"):
        check(problem, tampered)
