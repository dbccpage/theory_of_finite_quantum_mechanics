"""Tests for PROD-P5-NEXT-1 witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("prod_p5_next_1_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_prod_p5_next_1() -> None:
    out = _load().witness()
    assert out["goal_id"] == "PROD-P5-NEXT-1"
    assert out["total_claim_statuses"] == 15
    assert out["mapped_count"] == 11
    assert out["refused_count"] == 4
    assert out["refused_statuses"] == [
        "DEFINITION",
        "INTERPRETIVE",
        "NONCLAIM",
        "SYNTHESIS_CONCLUSION",
    ]
    assert out["ch20_statuses_covered"] == [
        "OutsideProfile",
        "Proved",
        "Refused",
        "Refuted",
        "Undetermined",
    ]
    assert out["recomputed_status"] == "Undetermined"
    assert out["authority_effect"] == "None"


def test_refuse_unmapped_definition_status() -> None:
    with pytest.raises(ValueError, match="unmapped_claim_status"):
        _load().refuse_unmapped_definition_status()
