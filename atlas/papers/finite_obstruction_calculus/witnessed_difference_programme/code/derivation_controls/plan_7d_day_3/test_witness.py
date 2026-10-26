"""Tests for PLAN-7D-DAY-3 derivation control.

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_7d_day_3_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_7d_day_3_witness_passes() -> None:
    module = _load()
    res = module.witness()
    assert res["lane_e"]["le1_dual_size"] == 6
    assert res["lane_e"]["le2_kernel_size"] == 1
    assert res["lane_e"]["le3_discrete_q_noncompact_documented"] is True
    assert res["lane_e"]["le4_exponents"] == (4, 2)
    assert res["next_2"]["lane_b"]["instance_count"] == 5
    assert res["preflight"]["legacy_live_refusal_exit_code"] == 2


def test_plan_7d_day_3_rejects_rank_deficiency_and_bad_types() -> None:
    module = _load()
    with pytest.raises(ValueError, match="LE-2 insufficient rank"):
        module.verify_lane_e_maps(m=6, p=3, n=3, rank=2)
    with pytest.raises(ValueError, match="invalid Lane E parameters"):
        module.verify_lane_e_maps(m=True)
