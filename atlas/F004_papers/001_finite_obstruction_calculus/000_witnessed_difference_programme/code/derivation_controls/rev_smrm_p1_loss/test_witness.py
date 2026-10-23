"""Tests for REV-SMRM-P1-LOSS witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("rev_smrm_p1_loss_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_rev_smrm_p1_loss() -> None:
    out = _load().witness()
    assert out["goal_id"] == "REV-SMRM-P1-LOSS"
    assert out["missing_b0_label"] == "RefusedCertificate"
    assert out["missing_b0_verified"] is False
    assert out["stalled_label"] == "Stalled"
    assert out["exhausted_label"] == "Exhausted"
    assert out["impossible_label"] == "Impossible"
    assert out["distinct_outcome_count"] == 3
    assert out["authority_effect"] == "None"


def test_refuse_loss_certificate_missing_b0() -> None:
    with pytest.raises(ValueError, match="b_0 not in trap_set"):
        _load().refuse_loss_certificate_missing_b0()
