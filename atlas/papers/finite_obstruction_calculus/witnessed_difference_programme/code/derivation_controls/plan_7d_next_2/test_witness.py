"""Tests for PLAN-7D-NEXT-2 derivation control.

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_7d_next_2_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_7d_next_2_witness_passes() -> None:
    module = _load()
    res = module.witness()
    assert res["lane_b"]["disturbance_repair_optimum"] == Fraction(15, 4)
    assert res["lane_b"]["adaptive_nondisturbing_optimum"] == Fraction(4, 1)
    assert res["lane_b"]["instance_count"] == 5
    assert res["lane_b"]["hostile_control_count"] == 12
    assert res["lane_c"]["carrier_sizes"] == (9, 9, 9)
    assert res["lane_c"]["solution_counts"] == (2, 3, 2, 1)
    assert res["lane_c"]["probe_in_x1"] is False
    assert res["lane_c"]["probe_in_x2"] is True
    assert res["lane_c"]["decoded_from_x1"] == (Fraction(1, 2), Fraction(1, 2))
    assert res["lane_c"]["decoded_from_x2"] == (Fraction(0, 1), Fraction(1, 1))
    assert res["lane_c"]["remaining_budget"] == 13
    assert res["lane_c"]["max_total_spend"] == 18


def test_plan_7d_next_2_rejects_budget_reset_and_bad_types() -> None:
    module = _load()
    with pytest.raises(ValueError, match="budget reset allowed cumulative spend above cap"):
        module.verify_lane_c_carriers(reset_between_rounds=True)
    with pytest.raises(ValueError, match="invalid parameter types"):
        module.verify_lane_c_carriers(budget_cap=True)
    assert module.verify_lane_b_binding()["original_class_only_cost"] == Fraction(7, 2)
