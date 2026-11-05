"""DDC letter M: typed refusal, and the closed refusal vocabulary.

A refusal is a valid outcome. M leaves the cochain state
unchanged and records one reason from ``M_REASONS``. Intake refusals happen
before a request is admitted; they are recorded in the intake trace and never
enter the DDC tape (``enters_ddc_trace`` is false).

The engine carries a refusal reason as a free string
(``omega_discrete_deformation_calculus::dda_alphabet::StepOutcome::RefusedToExecute``),
so this vocabulary is owned by the paper.

Leaf module: standard library only, loadable by path. AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, Optional, Set

INTAKE_REASONS = (
    "REFUSED_UNTYPED",
    "REFUSED_UNGROUNDED_LOCUS",
    "ADAPTER_INADEQUATE",
)


def _exact(value: object) -> Fraction:
    if isinstance(value, (bool, float)) or not isinstance(value, (int, Fraction)):
        raise ValueError(f"NOT_EXACT: {value!r}")
    return Fraction(value)


M_REASONS = (
    "REFUSED_INVALID_WITNESS",
    "REFUSED_BUDGET_EXHAUSTED",
    "REFUSED_NON_ZERO_CURL",
    "REFUSED_UNLICENSED_LIFT",
    "REFUSED_LIFT_TRIGGER",
    "REFUSED_MISSING_LOSS_LEDGER",
    "REFUSED_MISSING_RECEIPT",
    "REFUSED_REQUIRES_LIFT",
    "REFUSED_DETECTOR_INADEQUATE",
    "REFUSED_OPEN_OBSTRUCTION",
)


@dataclass(frozen=True)
class OperationRequest:
    op_letter: str
    locus: str
    witness: Optional[str]
    cost: Fraction
    payload: Dict[str, Any]


@dataclass(frozen=True)
class RefusalReceipt:
    operation: str
    paper_id: str
    refusal_code: str
    locus: str
    state_preserved: bool
    status: str
    enters_ddc_trace: bool = True
    authority_effect: str = "None"


class TypedRefusalGate:
    """Fail-closed gate: grounding at intake, then witness and budget as M."""

    def __init__(self, grounded_loci: Set[str], valid_witnesses: Set[str]):
        self.grounded_loci = frozenset(grounded_loci)
        self.valid_witnesses = frozenset(valid_witnesses)

    def evaluate(
        self,
        request: OperationRequest,
        remaining_budget: Fraction,
    ) -> Optional[RefusalReceipt]:
        """Return a refusal receipt for an invalid request, or ``None`` if it may proceed."""
        cost = _exact(request.cost)
        remaining_budget = _exact(remaining_budget)
        if cost < 0 or remaining_budget < 0:
            raise ValueError("NEGATIVE_BUDGET_OR_COST")
        if request.op_letter not in ("E", "R", "C", "I", "Λ", "D", "M", "T"):
            return RefusalReceipt("INTAKE", "DDC-M", "REFUSED_UNTYPED", request.locus,
                                  True, "INTAKE_REFUSED", enters_ddc_trace=False)
        if request.locus not in self.grounded_loci:
            return RefusalReceipt(
                operation="INTAKE",
                paper_id="DDC-M",
                refusal_code="REFUSED_UNGROUNDED_LOCUS",
                locus=request.locus,
                state_preserved=True,
                status="INTAKE_REFUSED",
                enters_ddc_trace=False,
            )
        if not request.witness or request.witness not in self.valid_witnesses:
            return self._m("REFUSED_INVALID_WITNESS", request.locus)
        if cost > remaining_budget:
            return self._m("REFUSED_BUDGET_EXHAUSTED", request.locus)
        return None

    @staticmethod
    def _m(code: str, locus: str) -> RefusalReceipt:
        return RefusalReceipt(
            operation="M",
            paper_id="DDC-M",
            refusal_code=code,
            locus=locus,
            state_preserved=True,
            status="MUTATION_BLOCKED",
        )
