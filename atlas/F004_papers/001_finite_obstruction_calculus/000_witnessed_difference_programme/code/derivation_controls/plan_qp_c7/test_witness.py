from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_c7_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_c7_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 3
    assert result["secondary_pair"] == (13, 12)
    assert result["secondary_ratio"] == Fraction(13, 12)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_c7_refuses_rigorous_bound_claim_for_neville_proxy() -> None:
    module = _load()
    for bad in ("rigorous_bound_claim_for_neville_proxy", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="rigorous_bound_claim_for_neville_proxy"):
            module.reject_rigorous_bound_claim_for_neville_proxy(bad)
    module.reject_rigorous_bound_claim_for_neville_proxy("admissible_scoped_control")
