"""Tests for SG-40 derivation control.

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("sg_40_witness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["sg_40_witness"] = module
    spec.loader.exec_module(module)
    return module


def test_sg_40_witness_passes() -> None:
    module = _load()
    res = module.witness()
    assert res["stages_executed"] == (0, 1, 2, 3, 4, 5, 6, 7, 8)
    assert res["before_receipt"]["free_h1_rank"] == 1
    assert res["after_receipt"]["free_h1_rank"] == 0
    assert res["after_receipt"]["d1_d2"] == (0, 0, 0)
    assert res["after_receipt"]["d2_beta"] == (1, 1, 1)
    assert res["answer_verified"] is True


def test_sg_40_rejects_bad_witness_sign_flip_and_self_receipt() -> None:
    module = _load()
    with pytest.raises(ValueError, match="witness equation d2 \\* beta = z failed"):
        module.run_sg_40_episode(beta=0)
    with pytest.raises(ValueError, match="chain complex identity d1 \\* d2 = 0 failed"):
        module.run_sg_40_episode(partial_2=(1, 1, -1))
    with pytest.raises(ValueError, match="parser self-receipt refused"):
        module.run_sg_40_episode(receipt_issuer="parser_stage_3")
    with pytest.raises(ValueError, match="undeclared 2-cell attachment refused"):
        module.run_sg_40_episode(extension_declared=False)
