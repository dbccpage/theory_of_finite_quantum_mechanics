"""Tests for PLAN-7D-NEXT-3 derivation control.

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_7d_next_3_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["plan_7d_next_3_witness"] = module
    spec.loader.exec_module(module)
    return module


def test_plan_7d_next_3_witness_passes() -> None:
    module = _load()
    res = module.witness()
    assert res["execution_order"] == ("SG-40", "SG-48")
    assert res["sg_40"]["after_receipt"]["free_h1_rank"] == 0
    assert res["sg_48"]["episode_2_receipt"]["reused_operator"] == "swap_bc"
    assert res["anti_substitution_verified"] is True


def test_plan_7d_next_3_rejects_substitutions_and_unsealed_task2() -> None:
    module = _load()
    with pytest.raises(ValueError, match="Q.6 continuation record cannot substitute"):
        module.run_workflow_endpoints(substitute_q6_continuation=True)
    with pytest.raises(ValueError, match="generic research-controller stage log cannot substitute"):
        module.run_workflow_endpoints(substitute_generic_controller_stages=True)
    with pytest.raises(ValueError, match="SG-48 Task 2 must remain withheld"):
        module.run_workflow_endpoints(withhold_sg48_task2_until_admission=False)
