from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("bridge_wsc_nonselection_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bridge_wsc_nonselection_witness_invariants() -> None:
    module = _load()
    result = module.witness()
    assert result["carrier_val"] == 2
    assert result["secondary_pair"] == (1, 1)
    assert result["secondary_ratio"] == Fraction(1, 1)
    assert result["coboundary_cycle_zero"] == 0


def test_bridge_wsc_nonselection_refuses_unpriced_labeled_atom_selection() -> None:
    module = _load()
    for bad in ("unpriced_labeled_atom_selection", "promote_unrestricted", "bypass_guard"):
        with pytest.raises(ValueError, match="unpriced_labeled_atom_selection"):
            module.reject_unpriced_labeled_atom_selection(bad)
    module.reject_unpriced_labeled_atom_selection("admissible_scoped_control")
