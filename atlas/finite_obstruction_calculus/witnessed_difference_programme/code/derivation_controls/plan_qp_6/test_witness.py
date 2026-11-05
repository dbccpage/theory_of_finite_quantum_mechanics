from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_6_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_6_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 6
    assert result["secondary_pair"] == (9, 2)
    assert result["secondary_ratio"] == Fraction(9, 2)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_6_refuses_refuted_k23_dual_equality() -> None:
    module = _load()
    for bad in ("refuted_k23_dual_equality", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="refuted_k23_dual_equality"):
            module.reject_refuted_k23_dual_equality(bad)
    module.reject_refuted_k23_dual_equality("admissible_scoped_control")
