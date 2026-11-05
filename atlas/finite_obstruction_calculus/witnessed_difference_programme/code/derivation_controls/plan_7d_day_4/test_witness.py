"""Tests for PLAN-7D-DAY-4 derivation control.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import sys

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_7d_day_4_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["plan_7d_day_4_witness"] = module
    spec.loader.exec_module(module)
    return module


def test_plan_7d_day_4_witness_passes() -> None:
    module = _load()
    res = module.witness()
    assert res["lane_b"]["disturbance_repair_cost"] == Fraction(15, 4)
    assert res["lane_b"]["overall_optimum"] == Fraction(15, 4)
    assert res["lane_c"]["total_cost"] == Fraction(17, 1)
    assert res["lanes_a_and_d"]["lane_a_extension_counts"] == (24, 30, 90)
    assert res["lanes_a_and_d"]["lane_d_class_count"] == 29771


def test_plan_7d_day_4_changed_input_refusals() -> None:
    module = _load()
    shifted = module.verify_lane_b_correspondence(restore_cost=Fraction(4, 1))
    assert shifted["disturbance_repair_cost"] == Fraction(15, 2)
    assert shifted["overall_optimum"] == Fraction(4, 1)

    with pytest.raises(ValueError, match="collapses original classes"):
        module.verify_lane_b_correspondence(drop_initial_projection=True)
    with pytest.raises(ValueError, match="omitting restore"):
        module.verify_lane_b_correspondence(include_restore=False)
    with pytest.raises(ValueError, match="changed task target d"):
        module.verify_lane_c_correspondence(task_target_d=2, cached_table_d=1)
    with pytest.raises(ValueError, match="stale parent digest"):
        module.verify_lane_c_correspondence(parent_digest_matches=False)
    with pytest.raises(ValueError, match="exceeds budget cap"):
        module.verify_lane_c_correspondence(repeat_child_without_reuse=True)
    with pytest.raises(ValueError, match="undeclared Lane D bound extension"):
        module.verify_lanes_a_and_d_scoped_reuse(max_terms=4)
