"""Tests for PROD-KERNEL-KILL witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_kernel_kill_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_kernel_kill() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-KERNEL-KILL"
    assert out["usable_budget"] == "3"
    assert out["initial_value"] == "3"
    assert out["kill_no_finite_arena"] is False
    assert out["kill_receipts_unreplayed"] is False
    assert out["any_kill_condition_holds"] is False
    assert out["authority_effect"] == "None"


def test_refuse_tampered_pilot_certificate() -> None:
    with pytest.raises(ValueError, match="kill_no_finite_arena"):
        _load().refuse_tampered_pilot_certificate()
