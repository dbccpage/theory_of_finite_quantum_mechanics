"""Tests for PROD-P3-KILL witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p3_kill_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p3_kill() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P3-KILL"
    assert out["transferred_rule_id"] == "circulation"
    assert out["saving_at_13_hits"] == "1"
    assert out["any_kill_condition_holds"] is False
    assert out["authority_effect"] == "None"


def test_refuse_unsafe_point_transfer() -> None:
    with pytest.raises(ValueError, match="transfer_unsafe"):
        _load().refuse_unsafe_point_transfer()
