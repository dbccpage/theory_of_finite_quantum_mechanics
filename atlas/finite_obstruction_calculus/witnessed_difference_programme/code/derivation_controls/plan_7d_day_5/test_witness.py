"""Tests for PLAN-7D-DAY-5 derivation control.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import sys

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_7d_day_5_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["plan_7d_day_5_witness"] = module
    spec.loader.exec_module(module)
    return module


def test_plan_7d_day_5_witness_passes() -> None:
    module = _load()
    res = module.witness()
    assert res["fuel_spent"] == 14
    assert res["fuel_remaining"] == 6
    assert res["crt_residues_n1_to_4"] == (4, 28, 136, 1216)
    assert res["dyadic_discrepancies_n1_to_4"] == (
        Fraction(1, 3),
        Fraction(1, 12),
        Fraction(1, 12),
        Fraction(1, 48),
    )
    assert res["next_3"]["execution_order"] == ("SG-40", "SG-48")


def test_plan_7d_day_5_rejects_fuel_reset_and_crt_corruption() -> None:
    module = _load()
    with pytest.raises(ValueError, match="fuel ledger reset between episodes refused"):
        module.verify_day_5_campaign(reset_fuel_between_episodes=True)
    with pytest.raises(ValueError, match="omitting raw proposal retention refused"):
        module.verify_day_5_campaign(retain_raw_proposals=False)
    with pytest.raises(ValueError, match="CRT residue"):
        module.verify_day_5_campaign(corrupt_crt_residue=True)
    with pytest.raises(ValueError, match="campaign fuel spend exceeded cap"):
        module.verify_day_5_campaign(fuel_cap=10)
