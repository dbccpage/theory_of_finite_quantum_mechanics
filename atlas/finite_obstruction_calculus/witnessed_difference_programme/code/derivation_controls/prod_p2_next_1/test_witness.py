"""Tests for PROD-P2-NEXT-1 executable witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p2_next_1_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prod_p2_next_1_witness_g5_steps() -> None:
    data = _load().witness()
    assert data["goal_id"] == "PROD-P2-NEXT-1"
    assert data["emitted"] is True
    assert len(str(data["receipt_digest"])) == 64
    assert data["g5_step_count"] == 12
    assert data["empty_claim_refusal"] == "invalid_input"
    assert data["authority_effect"] == "None"


def test_prod_p2_next_1_refuses_receipt_on_failing_report() -> None:
    with pytest.raises(ValueError, match="a failing report carries no receipt"):
        _load().refuse_receipt_on_failing_report()
