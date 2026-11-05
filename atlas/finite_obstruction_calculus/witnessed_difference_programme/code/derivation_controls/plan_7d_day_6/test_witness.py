"""Tests for PLAN-7D-DAY-6 derivation control.

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_7d_day_6_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["plan_7d_day_6_witness"] = module
    spec.loader.exec_module(module)
    return module


def test_plan_7d_day_6_witness_passes() -> None:
    module = _load()
    res = module.witness()
    assert res["binary_sha256"] == module.EXPECTED_BINARY_SHA256
    assert res["cargo_lock_sha256"] == module.EXPECTED_LOCK_SHA256
    assert res["checkpoint_resume_spent"] == (11, 3, 14)
    assert res["day_4_verified"] is True
    assert res["day_5_verified"] is True


def test_plan_7d_day_6_rejects_wrappers_checkpoint_tampering_and_scope_creep() -> None:
    module = _load()
    with pytest.raises(ValueError, match="static-label wrapper"):
        module.verify_day_6_freeze(static_success_wrapper=True)
    with pytest.raises(ValueError, match="tampered checkpoint state digest"):
        module.verify_day_6_freeze(tamper_checkpoint_digest=True)
    with pytest.raises(ValueError, match="zero previously spent fuel"):
        module.verify_day_6_freeze(reset_checkpoint_fuel=True)
    with pytest.raises(ValueError, match="Day 6 scope freeze violation"):
        module.verify_day_6_freeze(new_unscheduled_scope_added=True)
