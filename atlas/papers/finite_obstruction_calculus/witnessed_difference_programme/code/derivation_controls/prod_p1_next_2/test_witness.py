"""Tests for PROD-P1-NEXT-2 witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p1_next_2_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p1_next_2() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P1-NEXT-2"
    assert out["label_without_policy"] == "LosingInDeclaredArena"
    assert out["label_with_policy"] == "Impossible"
    assert out["forged_task_id_label"] == "RefusedCertificate"
    assert out["forged_task_id_verified"] is False
    assert out["forged_win_label"] == "RefusedCertificate"
    assert out["forged_win_verified"] is False
    assert out["authority_effect"] == "None"


def test_refuse_impossible_without_task_policy() -> None:
    with pytest.raises(ValueError, match="Impossible is not supported"):
        _load().refuse_impossible_without_task_policy()
