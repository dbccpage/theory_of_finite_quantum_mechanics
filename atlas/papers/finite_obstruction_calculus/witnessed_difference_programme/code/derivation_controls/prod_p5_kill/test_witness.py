"""Tests for PROD-P5-KILL witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p5_kill_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p5_kill() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P5-KILL"
    assert out["total_claims"] == 2
    assert out["proved_with_missing_d3"] == []
    assert out["demoted_to_undetermined"] == ["C2"]
    assert out["kill_triggered"] is False
    assert out["authority_effect"] == "None"


def test_refuse_non_bool_ci_flag() -> None:
    with pytest.raises(ValueError, match="invalid_input"):
        _load().refuse_non_bool_ci_flag()
