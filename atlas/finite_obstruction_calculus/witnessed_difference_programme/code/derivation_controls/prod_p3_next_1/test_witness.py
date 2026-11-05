"""Tests for PROD-P3-NEXT-1 executable witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p3_next_1_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prod_p3_next_1_witness_transfer_and_price() -> None:
    data = _load().witness()
    assert data["goal_id"] == "PROD-P3-NEXT-1"
    assert data["transferred_rule_id"] == "circulation"
    assert data["unsafe_refusal_code"] == "transfer_unsafe"
    assert data["unsound_refusal_code"] == "source_unsound"
    assert data["reference_saving"] == "3/5"
    assert data["q4_saving_at_12_hits"] == "0"
    assert data["q4_saving_at_13_hits"] == "1"
    assert data["authority_effect"] == "None"


def test_prod_p3_next_1_refuses_hits_exceeding_candidates() -> None:
    with pytest.raises(ValueError, match="hits cannot exceed candidates"):
        _load().refuse_hits_exceeding_candidates()
