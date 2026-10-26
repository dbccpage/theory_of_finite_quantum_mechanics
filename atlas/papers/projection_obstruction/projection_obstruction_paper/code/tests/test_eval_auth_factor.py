"""Tests for eval × auth factorization."""

from __future__ import annotations

import sys
from pathlib import Path

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from eval_auth_factor import (
    PAIRS,
    eval_always_exact,
    eval_hidden,
    exact,
    fiber_splits,
    joint_close,
    p_prod,
    valid_all,
    valid_hidden,
)


def test_model_a_auth_splits_eval_does_not() -> None:
    assert fiber_splits(PAIRS, p_prod, valid_hidden)
    assert not fiber_splits(PAIRS, p_prod, lambda x: exact(eval_always_exact, x))


def test_model_a_no_joint_close() -> None:
    reports = {p_prod(x) for x in PAIRS}
    for bits_e in (False, True):
        for bits_v in (False, True):
            k = {r: (bits_e, bits_v) for r in reports}.__getitem__
            assert not joint_close(
                PAIRS, p_prod, eval_always_exact, valid_hidden, k
            )


def test_model_b_eval_splits_auth_does_not() -> None:
    assert fiber_splits(PAIRS, p_prod, lambda x: exact(eval_hidden, x))
    assert not fiber_splits(PAIRS, p_prod, valid_all)


def test_model_b_no_joint_close() -> None:
    reports = {p_prod(x) for x in PAIRS}
    for bits_e in (False, True):
        for bits_v in (False, True):
            k = {r: (bits_e, bits_v) for r in reports}.__getitem__
            assert not joint_close(PAIRS, p_prod, eval_hidden, valid_all, k)


def test_model_c_license_in_report_closes() -> None:
    xs = (False, True)
    p = lambda x: x
    ev = lambda _x: 0
    valid = lambda x: bool(x)
    k = lambda m: (True, bool(m))
    assert joint_close(xs, p, ev, valid, k)
    assert not fiber_splits(xs, p, valid)
