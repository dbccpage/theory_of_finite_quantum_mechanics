"""Tests for PROD-P3-NEXT-2 witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p3_next_2_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p3_next_2() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P3-NEXT-2"
    assert out["candidates"] == 10000
    assert out["saving_at_12_hits"] == "0"
    assert out["strict_benefit_at_12"] is False
    assert out["saving_at_13_hits"] == "1"
    assert out["strict_benefit_at_13"] is True
    assert out["minimum_strict_benefit_hits"] == 13
    assert out["authority_effect"] == "None"


def test_refuse_twelve_hits_as_strict_benefit() -> None:
    with pytest.raises(ValueError, match="requires at least 13 hits"):
        _load().refuse_twelve_hits_as_strict_benefit()
