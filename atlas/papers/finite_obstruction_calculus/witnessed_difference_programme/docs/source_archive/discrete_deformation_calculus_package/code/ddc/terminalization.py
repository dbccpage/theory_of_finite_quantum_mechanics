"""DDC letter T: terminalization under ``CanContinue_n``.

``CanContinue_n`` is the conjunction of the nine conjuncts named by the engine
(``omega_discrete_deformation_calculus::oeprmalg2::CONTINUATION_CONJUNCTS``).
When supplied as continuation_facts, its failure permits a seal subject to
T's safety conditions. Without those facts the evaluator applies a separate
residual/budget/history policy. The abstract Lean T law contains neither policy:

* the state is left unchanged;
* ``Gamma2 = 0``: an open obstruction is never sealed (witness dominance). An
  out-of-budget open obstruction ends in M (``REFUSED_OPEN_OBSTRUCTION``);
* the detector is adequate: a blind detector cannot seal a green.

A LOCAL_GREEN_FOR_SCOPE verdict is a routing terminal (CheckPassed) inside the
declared scope. It licenses nothing: on the authority axis an unlicensed
``Phi1 = 0`` is F_term REFUSED by this package's explicit local policy.

Leaf module: standard library only, loadable by path. AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from fractions import Fraction
from typing import Sequence, Tuple

CONTINUATION_CONJUNCTS: Tuple[str, ...] = (
    "outstanding_obligation",
    "higher_obligation_witness",
    "next_carrier_declared",
    "adapter_sound",
    "detector_adequate",
    "minimal_licensed_lift",
    "skeleton_preserved",
    "budget_available",
    "gtla_continuation_refusal",
)

UNLICENSED_AUTHORITY_TERMINAL = "F_term:REFUSED"


def _exact(value: object) -> Fraction:
    if isinstance(value, (bool, float)) or not isinstance(value, (int, Fraction)):
        raise ValueError(f"NOT_EXACT: {value!r}")
    return Fraction(value)


@dataclass(frozen=True)
class ContinuationFacts:
    """One truth value per conjunct; ``gtla_continuation_refusal`` is true when none was issued."""

    outstanding_obligation: bool
    higher_obligation_witness: bool
    next_carrier_declared: bool
    adapter_sound: bool
    detector_adequate: bool
    minimal_licensed_lift: bool
    skeleton_preserved: bool
    budget_available: bool
    gtla_continuation_refusal: bool

    def __post_init__(self) -> None:
        for f in fields(self):
            if type(getattr(self, f.name)) is not bool:
                raise TypeError(f"{f.name} must be bool, not {type(getattr(self, f.name)).__name__}")


def can_continue(facts: ContinuationFacts) -> bool:
    return all(getattr(facts, name) for name in CONTINUATION_CONJUNCTS)


def failed_conjuncts(facts: ContinuationFacts) -> Tuple[str, ...]:
    return tuple(name for name in CONTINUATION_CONJUNCTS if not getattr(facts, name))


@dataclass(frozen=True)
class TerminalReceipt:
    operation: str
    paper_id: str
    is_terminal: bool
    verdict: str
    final_residual: Fraction
    remaining_budget: Fraction
    step_count: int
    authority_terminal: str = UNLICENSED_AUTHORITY_TERMINAL
    authority_effect: str = "None"


class TerminalizationEvaluator:
    """Scope-bounded terminal verdicts; refuses to seal open or blind states."""

    def __init__(self, progress_lookback: int = 3):
        if type(progress_lookback) is not int or progress_lookback < 2:
            raise ValueError("progress_lookback must be an integer >= 2")
        self.progress_lookback = progress_lookback

    def _receipt(self, terminal: bool, verdict: str, residual: Fraction, budget: Fraction, steps: int) -> TerminalReceipt:
        return TerminalReceipt(
            operation="T",
            paper_id="DDC-T",
            is_terminal=terminal,
            verdict=verdict,
            final_residual=residual,
            remaining_budget=budget,
            step_count=steps,
        )

    def evaluate(
        self,
        residual_norm: Fraction,
        remaining_budget: Fraction,
        residual_history: Sequence[Fraction],
        closure_defect: Fraction = Fraction(0),
        detector_adequate: bool = True,
        continuation_facts: ContinuationFacts | None = None,
    ) -> TerminalReceipt:
        """Verdict for the current residual (Phi1-sized) and closure defect (Gamma2)."""
        if type(detector_adequate) is not bool:
            raise TypeError(f"detector_adequate must be bool, not {type(detector_adequate).__name__}")
        residual_norm = _exact(residual_norm)
        remaining_budget = _exact(remaining_budget)
        closure_defect = _exact(closure_defect)
        residual_history = [_exact(value) for value in residual_history]
        if residual_norm < 0 or closure_defect < 0 or any(x < 0 for x in residual_history):
            raise ValueError("NEGATIVE_DIAGNOSTIC")
        steps = len(residual_history)
        if closure_defect > 0:
            return self._receipt(False, "SEAL_REFUSED_OPEN_OBSTRUCTION", residual_norm, remaining_budget, steps)
        if not detector_adequate:
            return self._receipt(False, "SEAL_REFUSED_DETECTOR_INADEQUATE", residual_norm, remaining_budget, steps)
        if continuation_facts is not None:
            if continuation_facts.detector_adequate != detector_adequate:
                raise ValueError("CONTRADICTORY_DETECTOR_FACT")
            if continuation_facts.budget_available and remaining_budget <= 0:
                raise ValueError("CONTRADICTORY_BUDGET_FACT")
            if can_continue(continuation_facts):
                return self._receipt(False, "CAN_CONTINUE", residual_norm, remaining_budget, steps)
            if residual_norm > 0:
                return self._receipt(True, "HALTED_CONTINUATION_POLICY", residual_norm, remaining_budget, steps)
        if residual_norm == 0:
            return self._receipt(True, "LOCAL_GREEN_FOR_SCOPE", residual_norm, remaining_budget, steps)
        if remaining_budget <= 0:
            return self._receipt(True, "HALTED_OUT_OF_BUDGET", residual_norm, remaining_budget, steps)
        if len(residual_history) >= self.progress_lookback:
            recent = residual_history[-self.progress_lookback :]
            if recent[-1] >= recent[0]:
                return self._receipt(True, "HALTED_STAGNANT_PROGRESS", residual_norm, remaining_budget, steps)
        return self._receipt(False, "CAN_CONTINUE", residual_norm, remaining_budget, steps)
