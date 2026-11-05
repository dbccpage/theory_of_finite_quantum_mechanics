"""Tests for PROD-P4-NEXT-1 witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p4_next_1_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p4_next_1() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P4-NEXT-1"
    assert out["feasible_suite"] == ["I_pair01", "I_pair12"]
    assert out["feasible_cost"] == "7/2"
    assert out["verified_optimal"] is True
    assert out["infeasible_unresolved_pairs"] == [["s1", "s2"]]
    assert out["authority_effect"] == "None"


def test_refuse_suboptimal_suite_verdict() -> None:
    with pytest.raises(ValueError, match="suboptimal suite rejected"):
        _load().refuse_suboptimal_suite_verdict()
