"""Tests for PROD-P2-NEXT-2 witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p2_next_2_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p2_next_2() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P2-NEXT-2"
    assert out["step_count"] == 12
    assert len(out["isolated_steps"]) == 12
    assert out["authority_effect"] == "None"


def test_refuse_admitted_report_with_failure_fixture() -> None:
    with pytest.raises(ValueError, match="G5 step failure"):
        _load().refuse_admitted_report_with_failure_fixture()
