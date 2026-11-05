from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_10_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_10_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 9
    assert result["secondary_pair"] == (31, 800)
    assert result["secondary_ratio"] == Fraction(31, 800)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_10_refuses_mub6_full_resolution_claim() -> None:
    module = _load()
    for bad in ("mub6_full_resolution_claim", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="mub6_full_resolution_claim"):
            module.reject_mub6_full_resolution_claim(bad)
    module.reject_mub6_full_resolution_claim("admissible_scoped_control")
