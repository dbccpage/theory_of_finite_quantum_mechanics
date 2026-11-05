"""Tests for PLAN-7D-DAY-7 derivation control.

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
    spec = importlib.util.spec_from_file_location("plan_7d_day_7_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["plan_7d_day_7_witness"] = module
    spec.loader.exec_module(module)
    return module


def test_plan_7d_day_7_witness_passes() -> None:
    module = _load()
    res = module.witness()
    assert res["lanes_audited"] == ("A", "B", "C", "D", "E")
    assert res["sg_total_episodes"] == 50
    assert res["sg_local_staged_pass_count"] == 2
    assert res["sg_not_run_count"] == 48
    assert res["actual_paid_spend_usd"] == Fraction(0, 1)


def test_plan_7d_day_7_rejects_false_promotions_and_budget_overrun() -> None:
    module = _load()
    with pytest.raises(ValueError, match="deadline-driven promotion of NOT_RUN SG episodes refused"):
        module.verify_day_7_audit_report(promote_unrun_sg_episodes=True)
    with pytest.raises(ValueError, match="promotion of open infinite locally compact duality"):
        module.verify_day_7_audit_report(promote_open_lane_e_continuum_duality=True)
    with pytest.raises(ValueError, match="spend ledger violated"):
        module.verify_day_7_audit_report(actual_paid_spend_usd=Fraction(1, 2))
