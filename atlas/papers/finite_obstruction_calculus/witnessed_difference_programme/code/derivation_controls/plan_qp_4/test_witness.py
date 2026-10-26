from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_4_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_4_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 18
    assert result["secondary_pair"] == (9, 4)
    assert result["secondary_ratio"] == Fraction(9, 4)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_4_refuses_noncontextual_18ray_assignment() -> None:
    module = _load()
    for bad in ("noncontextual_18ray_assignment", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="noncontextual_18ray_assignment"):
            module.reject_noncontextual_18ray_assignment(bad)
    module.reject_noncontextual_18ray_assignment("admissible_scoped_control")
