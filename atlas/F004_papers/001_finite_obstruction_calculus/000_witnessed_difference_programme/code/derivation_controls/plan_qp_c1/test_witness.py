from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_c1_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_c1_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 0
    assert result["secondary_pair"] == (3, 1)
    assert result["secondary_ratio"] == Fraction(3, 1)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_c1_refuses_i3_zero_implies_unique_born() -> None:
    module = _load()
    for bad in ("i3_zero_implies_unique_born", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="i3_zero_implies_unique_born"):
            module.reject_i3_zero_implies_unique_born(bad)
    module.reject_i3_zero_implies_unique_born("admissible_scoped_control")
