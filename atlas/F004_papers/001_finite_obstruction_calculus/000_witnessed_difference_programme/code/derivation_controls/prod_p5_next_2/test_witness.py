"""Tests for PROD-P5-NEXT-2 witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p5_next_2_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p5_next_2() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P5-NEXT-2"
    assert out["statuses"] == {
        "C1": "Undetermined",
        "C2": "Undetermined",
        "C3": "Undetermined",
        "C_IND": "Proved",
    }
    assert out["authority_effect"] == "None"


def test_refuse_dependency_cycle() -> None:
    with pytest.raises(ValueError, match="dependency_cycle"):
        _load().refuse_dependency_cycle()
