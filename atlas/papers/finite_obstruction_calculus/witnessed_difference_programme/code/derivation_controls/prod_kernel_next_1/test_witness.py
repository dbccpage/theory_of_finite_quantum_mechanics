"""Tests for PROD-KERNEL-NEXT-1 executable witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_kernel_next_1_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prod_kernel_next_1_witness_parity() -> None:
    data = _load().witness()
    assert data["goal_id"] == "PROD-KERNEL-NEXT-1"
    assert data["claim_ids"] == ("claim_a", "claim_b")
    assert len(str(data["input_digest"])) == 64
    assert len(str(data["output_digest"])) == 64
    assert len(str(data["receipt_digest"])) == 64
    assert data["verified"] is True
    assert data["tampered_refusal_code"] == "digest_mismatch"
    assert data["empty_subject_refusal_code"] == "invalid_input"
    assert data["mapped_refusal_code"] == "receipt_mismatch"
    assert data["authority_effect"] == "None"


def test_prod_kernel_next_1_refuses_authority_promotion() -> None:
    with pytest.raises(ValueError, match="forbid authority_effect"):
        _load().refuse_authority_promotion("Granted")
