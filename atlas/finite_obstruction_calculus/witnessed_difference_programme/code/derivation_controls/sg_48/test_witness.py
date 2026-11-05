"""Tests for SG-48 derivation control.

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("sg_48_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["sg_48_witness"] = module
    spec.loader.exec_module(module)
    return module


def test_sg_48_witness_passes() -> None:
    module = _load()
    res = module.witness()
    assert res["r0_size"] == 2
    assert res["r1_size"] == 3
    assert res["episode_1_receipt"]["initial_reachable"] == ("a", "b")
    assert res["episode_1_receipt"]["terminal_state"] == "c"
    assert res["episode_2_receipt"]["terminal_state"] == "c"
    assert res["episode_2_receipt"]["word"] == ("swap_bc",)


def test_sg_48_adversarial_refusals() -> None:
    module = _load()
    with pytest.raises(ValueError, match="pre-verification operator execution refused"):
        module.run_sg_48_episodes(verify_stage_5_before_use=False)
    with pytest.raises(ValueError, match="cached Episode 1 receipt refused"):
        module.run_sg_48_episodes(reuse_ep1_receipt_for_ep2=True)
    with pytest.raises(ValueError, match="task_1 target mutation refused"):
        module.run_sg_48_episodes(mutate_task1_target="b")
    with pytest.raises(ValueError, match="uncertified MetaLift promotion refused"):
        module.run_sg_48_episodes(promote_uncertified_metalift=True)
    with pytest.raises(ValueError, match="task_2 must remain sealed"):
        module.run_sg_48_episodes(task2_sealed_during_ep1=False)
    with pytest.raises(ValueError, match="non-involution candidate operator"):
        module.run_sg_48_episodes(candidate_op={"a": "a", "b": "c", "c": "c"})
