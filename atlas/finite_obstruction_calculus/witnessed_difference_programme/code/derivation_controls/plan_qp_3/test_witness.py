from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_3_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_3_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 8
    assert result["secondary_pair"] == (196, 25)
    assert result["secondary_ratio"] == Fraction(196, 25)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_3_refuses_gaussian_rational_tsirelson_attainment() -> None:
    module = _load()
    for bad in ("gaussian_rational_tsirelson_attainment", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="gaussian_rational_tsirelson_attainment"):
            module.reject_gaussian_rational_tsirelson_attainment(bad)
    module.reject_gaussian_rational_tsirelson_attainment("admissible_scoped_control")
