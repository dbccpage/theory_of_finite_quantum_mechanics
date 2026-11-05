"""Tests for PROD-P1-NEXT-1 executable witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p1_next_1_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prod_p1_next_1_witness_round_trip() -> None:
    data = _load().witness()
    assert data["goal_id"] == "PROD-P1-NEXT-1"
    assert data["label_count"] == 8
    assert data["observed_labels"] == (
        "Refused",
        "RefusedCertificate",
        "Stalled",
        "Impossible",
        "LosingInDeclaredArena",
        "ResolvedWithinBudget",
        "Exhausted",
        "UndeterminedBudget",
    )
    assert data["negative_budget_refusal"] == "invalid_input"
    assert data["authority_effect"] == "None"


def test_prod_p1_next_1_refuses_impossible_without_policy() -> None:
    with pytest.raises(ValueError, match="WDP-CHS-D03 gives LosingInDeclaredArena"):
        _load().refuse_impossible_without_policy()
