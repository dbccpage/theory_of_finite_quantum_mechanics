from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_c8_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_c8_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 5
    assert result["secondary_pair"] == (9, 1)
    assert result["secondary_ratio"] == Fraction(9, 1)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_c8_refuses_mub6_subgap_global_promotion() -> None:
    module = _load()
    for bad in ("mub6_subgap_global_promotion", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="mub6_subgap_global_promotion"):
            module.reject_mub6_subgap_global_promotion(bad)
    module.reject_mub6_subgap_global_promotion("admissible_scoped_control")
