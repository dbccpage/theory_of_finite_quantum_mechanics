"""Eval × auth factorization. AuthorityEffect: None.

A proposer map out of a report cannot recover both exact evaluation
and independently supplied authorization when either measurement
splits a report fiber. License-in-the-report jointly closes only
because it is evaluation of an operational field, not independent auth.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Pair:
    report: bool
    hidden: bool


def exact(eval_fn: Callable[[object], int], x: object) -> bool:
    return eval_fn(x) == 0


def joint_close(
    xs: tuple[object, ...],
    p: Callable[[object], object],
    eval_fn: Callable[[object], int],
    valid: Callable[[object], bool],
    k: Callable[[object], tuple[bool, bool]],
) -> bool:
    return all(k(p(x)) == (exact(eval_fn, x), valid(x)) for x in xs)


def fiber_splits(
    xs: tuple[object, ...],
    p: Callable[[object], object],
    meas: Callable[[object], bool],
) -> bool:
    seen: dict[object, bool] = {}
    for x in xs:
        r = p(x)
        v = meas(x)
        if r in seen and seen[r] != v:
            return True
        seen[r] = v
    return False


def p_prod(x: object) -> object:
    if not isinstance(x, Pair):
        raise TypeError(f"Expected Pair instance, got {type(x)}")
    return x.report


def eval_always_exact(_x: object) -> int:
    return 0


def valid_hidden(x: object) -> bool:
    if not isinstance(x, Pair):
        raise TypeError(f"Expected Pair instance, got {type(x)}")
    return x.hidden


def eval_hidden(x: object) -> int:
    if not isinstance(x, Pair):
        raise TypeError(f"Expected Pair instance, got {type(x)}")
    return 0 if x.hidden else 1


def valid_all(_x: object) -> bool:
    return True


PAIRS: tuple[Pair, ...] = (
    Pair(False, False),
    Pair(False, True),
    Pair(True, False),
    Pair(True, True),
)
