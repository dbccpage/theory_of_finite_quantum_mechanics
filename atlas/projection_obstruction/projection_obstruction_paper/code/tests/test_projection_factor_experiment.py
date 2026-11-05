"""Tests for the PO-000 projection-is-not-authorization experiment."""

from __future__ import annotations

import sys
from pathlib import Path


_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from exactsym import Matrix

from exact import exact_equal
from projection_factor_experiment import (
    collapse_tally_to_auth,
    on_factorized_slice,
    product_retract,
    prop3b_witness,
    residual_triple,
    run_experiment,
    slots_from_residual,
)


def test_retract_is_idempotent() -> None:
    point = Matrix([2, 5])
    once = product_retract(point)
    assert exact_equal(product_retract(once), once)
    assert on_factorized_slice(once)


def test_prop3b_leaves_manifold_but_projection_is_identity() -> None:
    witness = prop3b_witness()
    assert witness.left_manifold
    assert witness.projected_is_identity
    assert not on_factorized_slice(witness.ambient_image)
    assert on_factorized_slice(witness.projected_image)


def test_three_residuals_are_not_identified() -> None:
    triple = residual_triple()
    assert not exact_equal(triple.normal_leak, Matrix.zeros(2, 1))
    assert not exact_equal(triple.retraction_residual, Matrix.zeros(2, 1))
    assert exact_equal(triple.semigroup_defect, Matrix.zeros(2, 1))
    assert not exact_equal(triple.normal_leak, triple.retraction_residual)
    assert not exact_equal(triple.retraction_residual, triple.semigroup_defect)


def test_positive_residual_does_not_authorize() -> None:
    triple = residual_triple()
    slots = slots_from_residual(triple.retraction_residual, authorize=False)
    assert slots.authorized is False
    assert collapse_tally_to_auth(slots.evaluation_tally) is True


def test_run_experiment_blocks_collapse() -> None:
    report = run_experiment()
    assert report["left_manifold"] is True
    assert report["projected_is_identity"] is True
    assert report["authorized"] is False
    assert report["collapse_would_authorize"] is True
    assert report["collapse_blocked"] is True
