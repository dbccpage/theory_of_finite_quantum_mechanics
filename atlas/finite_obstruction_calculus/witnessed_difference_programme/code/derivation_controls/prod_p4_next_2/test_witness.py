"""Tests for PROD-P4-NEXT-2 witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p4_next_2_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p4_next_2() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P4-NEXT-2"
    assert out["raw_minimum"] == 2
    assert out["quotient_minimum"] == 1
    assert out["joint_minimum"] == 2
    assert out["separate_sum"] == 3
    assert out["strict_subadditivity"] is True
    assert out["authority_effect"] == "None"


def test_refuse_non_completion_target() -> None:
    with pytest.raises(ValueError, match="invalid_input"):
        _load().refuse_non_completion_target()
