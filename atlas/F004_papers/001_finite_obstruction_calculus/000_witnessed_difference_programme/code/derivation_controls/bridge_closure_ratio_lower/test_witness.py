from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("bridge_closure_ratio_lower_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bridge_closure_ratio_lower_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 1
    assert result["secondary_pair"] == (1, 2)
    assert result["secondary_ratio"] == Fraction(1, 2)
    assert result["coboundary_cycle_zero"] == 0


def test_bridge_closure_ratio_lower_refuses_expansion_implies_unconditional_termination() -> None:
    module = _load()
    for bad in ("expansion_implies_unconditional_termination", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="expansion_implies_unconditional_termination"):
            module.reject_expansion_implies_unconditional_termination(bad)
    module.reject_expansion_implies_unconditional_termination("admissible_scoped_control")
