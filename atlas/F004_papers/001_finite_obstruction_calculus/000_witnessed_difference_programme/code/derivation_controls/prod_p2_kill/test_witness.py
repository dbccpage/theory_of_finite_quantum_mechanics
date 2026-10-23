"""Tests for PROD-P2-KILL witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p2_kill_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p2_kill() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P2-KILL"
    assert out["batch_size"] == 4
    assert out["initial_passed"] == 3
    assert out["repaired_passed"] is True
    assert out["any_kill_condition_holds"] is False
    assert out["authority_effect"] == "None"


def test_refuse_empty_claim_id() -> None:
    with pytest.raises(ValueError, match="invalid_input"):
        _load().refuse_empty_claim_id()
