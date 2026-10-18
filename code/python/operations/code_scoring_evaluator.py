"""Forwarder for code_scoring_evaluator from operations.cicd.

AuthorityEffect: None.
Origin: code/python/operations/cicd/code_scoring_evaluator.py
Claim: urn:omega:operations:code_scoring_evaluator:forwarder:v2
Compatibility claim: urn:omega:scoring:grade-minimum-forwarder:v1
Scope Fence: forwarder_seal is a local witness, not a repository grade.
Profile: Non-Numeric
Mutation-Kills: 8 non-equivalent local witness mutants, executed by code/python/operations/test_forwarder_control.py.
This count covers the legacy integer/order witness only, not the full static evaluator.
"""

from typing import Mapping
from pathlib import Path
import sys

_current_dir = Path(__file__).resolve().parent
if str(_current_dir) not in sys.path:
    sys.path.insert(0, str(_current_dir))

try:
    from .cicd.code_scoring_evaluator import (
        CodeScoringReceipt,
        FileScoreRecord,
        GateScore,
        GRADE_ORDER,
        GRADE_RANKS,
        ScoringError,
        grade_minimum_witness,
        min_grade,
        score_source_file,
        evaluate_scoring_rubric,
        main,
    )
except (ImportError, ValueError):
    from cicd.code_scoring_evaluator import (
        CodeScoringReceipt,
        FileScoreRecord,
        GateScore,
        GRADE_ORDER,
        GRADE_RANKS,
        ScoringError,
        grade_minimum_witness,
        min_grade,
        score_source_file,
        evaluate_scoring_rubric,
        main,
    )

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


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
