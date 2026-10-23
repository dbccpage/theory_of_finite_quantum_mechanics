from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_1_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_1_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 512
    assert result["secondary_pair"] == (1, 1)
    assert result["secondary_ratio"] == Fraction(1, 1)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_1_refuses_unconditional_h1_promotion_without_d1() -> None:
    module = _load()
    for bad in ("unconditional_h1_promotion_without_d1", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="unconditional_h1_promotion_without_d1"):
            module.reject_unconditional_h1_promotion_without_d1(bad)
    module.reject_unconditional_h1_promotion_without_d1("admissible_scoped_control")
