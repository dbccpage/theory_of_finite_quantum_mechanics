"""Forward the scoring certificate without widening its authority.

Origin: SCORING.md section 1.2, The Fail-Closed Weakest Link Rule.
Claim: urn:omega:scoring:grade-minimum-forwarder:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/operations/test_forwarder_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: forwarder_seal repeats the grade-minimum certificate. It does
not score arbitrary repositories and does not grant AuthorityEffect.
"""

from __future__ import annotations

from typing import Mapping, Sequence

from .cicd.code_scoring_evaluator import (
    GRADE_ORDER,
    GRADE_RANKS,
    CodeScoringReceipt,
    FileScoreRecord,
    GateScore,
    ScoringError,
    evaluate_scoring_rubric,
    grade_minimum_witness,
    min_grade,
    score_source_file,
)
from .cicd.code_scoring_evaluator import main as evaluate_main


class ForwarderError(ValueError):
    """One violated forwarder invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ForwarderError:
    return ForwarderError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the forwarder boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def checked_int(value: object) -> int:
    """Return one integer after refusing float and bool."""
    return _require_int(value, "checked")


def _sum(left: int, right: int) -> int:
    return left + right


def _gap(left: int, right: int) -> int:
    return left - right


def _product(left: int, right: int) -> int:
    return left * right


def forwarder_seal() -> int:
    """Return 0 when the forwarded minimum-grade witness agrees."""
    value = _require_int(grade_minimum_witness(), "certificate")
    if value != 0:
        raise _fail("forwarded certificate drifted", value=value)
    if _sum(1, 3) != 4:
        raise _fail("forwarder sum drifted", total=_sum(1, 3))
    if _gap(6, 2) != 4:
        raise _fail("forwarder gap drifted", gap=_gap(6, 2))
    if _product(2, 3) != 6:
        raise _fail("forwarder product drifted", product=_product(2, 3))
    return value


def main(argv: Sequence[str] | None = None) -> int:
    """Print the forwarder seal, then the evaluator receipt when arguments are present."""
    try:
        sealed = forwarder_seal()
    except ForwarderError as error:
        print(error.invariant)
        return 1
    if argv is None or len(argv) == 0:
        print(sealed)
        return 0 if sealed == 0 else 1
    return evaluate_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = (
    "GRADE_ORDER",
    "GRADE_RANKS",
    "CodeScoringReceipt",
    "FileScoreRecord",
    "ForwarderError",
    "GateScore",
    "ScoringError",
    "checked_int",
    "evaluate_main",
    "evaluate_scoring_rubric",
    "forwarder_seal",
    "grade_minimum_witness",
    "main",
    "min_grade",
    "score_source_file",
)
