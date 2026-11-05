from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("bridge_nc_identity_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bridge_nc_identity_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 12
    assert result["secondary_pair"] == (1, 1)
    assert result["secondary_ratio"] == Fraction(1, 1)
    assert result["coboundary_cycle_zero"] == 0


def test_bridge_nc_identity_refuses_totalized_zero_inverse() -> None:
    module = _load()
    for bad in ("totalized_zero_inverse", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="totalized_zero_inverse"):
            module.reject_totalized_zero_inverse(bad)
    module.reject_totalized_zero_inverse("admissible_scoped_control")
