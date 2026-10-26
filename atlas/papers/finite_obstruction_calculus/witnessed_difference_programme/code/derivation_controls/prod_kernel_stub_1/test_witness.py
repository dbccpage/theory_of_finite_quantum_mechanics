"""Tests for PROD-KERNEL-STUB-1 executable witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_kernel_stub_1_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prod_kernel_stub_1_witness_parity() -> None:
    data = _load().witness()
    assert data["goal_id"] == "PROD-KERNEL-STUB-1"
    assert data["optimal_claim"] == "WIN_OPTIMAL"
    assert data["optimal_initial_value"] == "2"
    assert data["feasible_claim"] == "WIN_FEASIBLE"
    assert data["feasible_initial_value"] == "5"
    assert data["forged_accepted"] is False
    assert data["forged_failures"] == ("lower inequality failed: a cheaper action exists",)
    assert data["stalled_initial_stalled"] is True
    assert data["trapped_initial_stalled"] is False
    assert data["authority_effect"] == "None"


def test_prod_kernel_stub_1_refuses_producer_substitution() -> None:
    with pytest.raises(ValueError, match="never calls the producer"):
        _load().refuse_producer_substitution(True)
