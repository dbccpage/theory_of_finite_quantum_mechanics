"""Tests for PROD-P1-KILL witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p1_kill_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p1_kill() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P1-KILL"
    assert out["arena_state_count"] == 4
    assert out["loss_certificate_verified"] is True
    assert out["any_kill_condition_holds"] is False
    assert out["authority_effect"] == "None"


def test_refuse_invalid_termination_label() -> None:
    with pytest.raises((TypeError, ValueError, KeyError)):
        _load().refuse_invalid_termination_label()
