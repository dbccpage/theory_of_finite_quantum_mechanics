from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_qp_2_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plan_qp_2_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 14
    assert result["secondary_pair"] == (14, 5)
    assert result["secondary_ratio"] == Fraction(14, 5)
    assert result["coboundary_cycle_zero"] == 0


def test_plan_qp_2_refuses_mixture_table_as_quantum() -> None:
    module = _load()
    for bad in ("mixture_table_as_quantum", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="mixture_table_as_quantum"):
            module.reject_mixture_table_as_quantum(bad)
    module.reject_mixture_table_as_quantum("admissible_scoped_control")
