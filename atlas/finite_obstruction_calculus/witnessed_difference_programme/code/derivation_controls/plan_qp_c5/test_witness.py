from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_c5_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_c5_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 3
    assert result["secondary_pair"] == (2, 2)
    assert result["secondary_ratio"] == Fraction(2, 2)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_c5_refuses_undeclared_d1_or_phantom_artifacts() -> None:
    module = _load()
    for bad in ("undeclared_d1_or_phantom_artifacts", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="undeclared_d1_or_phantom_artifacts"):
            module.reject_undeclared_d1_or_phantom_artifacts(bad)
    module.reject_undeclared_d1_or_phantom_artifacts("admissible_scoped_control")
