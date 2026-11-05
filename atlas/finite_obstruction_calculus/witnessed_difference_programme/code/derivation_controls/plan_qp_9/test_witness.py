from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_9_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_9_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 13
    assert result["secondary_pair"] == (13, 12)
    assert result["secondary_ratio"] == Fraction(13, 12)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_9_refuses_uncertified_neville_continuum_bound() -> None:
    module = _load()
    for bad in ("uncertified_neville_continuum_bound", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="uncertified_neville_continuum_bound"):
            module.reject_uncertified_neville_continuum_bound(bad)
    module.reject_uncertified_neville_continuum_bound("admissible_scoped_control")
