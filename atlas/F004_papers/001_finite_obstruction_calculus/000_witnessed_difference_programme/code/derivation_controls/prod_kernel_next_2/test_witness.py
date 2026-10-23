"""Tests for PROD-KERNEL-NEXT-2 witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_kernel_next_2_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_kernel_next_2() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-KERNEL-NEXT-2"
    assert out["task_id"] == "pilot-g5-provenance-repair-loop"
    assert out["usable_budget"] == "3"
    assert out["initial_value"] == "3"
    assert out["label_at_usable_budget"] == "ResolvedWithinBudget"
    assert out["label_at_tight_budget"] == "Exhausted"
    assert out["authority_effect"] == "None"


def test_refuse_negative_pilot_budget() -> None:
    with pytest.raises(ValueError, match="invalid_input"):
        _load().refuse_negative_pilot_budget()
