"""Tests for PROD-P4-KILL witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p4_kill_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p4_kill() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P4-KILL"
    assert out["replay_fixture_count"] == 5
    assert out["planned_suite"] == ["I_pair01", "I_pair12"]
    assert out["planned_cost"] == "7/2"
    assert out["buyer_baseline_cost"] == "5"
    assert out["kill_exceeds_solver"] is False
    assert out["kill_never_differs"] is False
    assert out["any_kill_condition_holds"] is False
    assert out["authority_effect"] == "None"


def test_refuse_unimproved_buyer_baseline() -> None:
    with pytest.raises(ValueError, match="kill_never_differs"):
        _load().refuse_unimproved_buyer_baseline()
