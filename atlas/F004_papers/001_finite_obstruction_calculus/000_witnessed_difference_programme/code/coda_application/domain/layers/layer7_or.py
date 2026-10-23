# -*- coding: utf-8 -*-
"""
Layer 7: CODA-OR (Omniversal Re-Presentation).

Enforces:
- Hard refusal sieve: empty support sieve -> Refused (OR-T5, GTLA-T6)
- Incompatible overlap detection: b != b' -> Refused (OR-T3)
- Anti-Consensus discipline: Averaging incompatible derivations is strictly forbidden
- Route to Refused / F_term on structural inconsistency

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Tuple

from coda_application.domain.entities import LayerExecutionRecord
from coda_application.domain.intake import IntakeData, intake
from coda_application.domain.value_objects import ExactRational, LayerId


def _data(problem: Any) -> IntakeData:
    return problem if isinstance(problem, IntakeData) else intake(problem)


def _er(value: Fraction) -> ExactRational:
    return ExactRational(value.numerator, value.denominator)


class Layer7OR:
    """Evaluates Layer 7: Omniversal Re-Presentation."""

    @staticmethod
    def evaluate(problem: Any, gamma2: ExactRational) -> Tuple[LayerExecutionRecord, bool]:
        """
        Executes Layer 7 refusal sieve.
        Returns LayerExecutionRecord and boolean indicating whether refusal was triggered (True = refused).
        """
        data = _data(problem)
        reasons = []
        admitted = [c for c in data.sieve if c.strip()]
        if not admitted:
            reasons.append("Empty support sieve: no admitted (non-blank) candidate hypothesis (OR-T5)")
        incompatible = [pair for pair, comp in data.overlaps if not comp]
        if incompatible:
            reasons.append(f"Incompatible boundary overlaps detected: {incompatible} (OR-T3)")
        if gamma2.is_positive or not gamma2.is_zero:
            reasons.append(f"Cocycle gluing failure: Gamma_2={gamma2.sympy_rational} != 0")
        is_refused = bool(reasons)
        msg = (
            "OR Hard Refusal triggered: " + "; ".join(reasons)
            if is_refused
            else "OR Refusal sieve passed: candidate sieve inhabited, overlaps compatible, Gamma_2 == 0"
        )
        record = LayerExecutionRecord(
            layer_id=LayerId.OR,
            succeeded=not is_refused,
            diagnostic_message=msg,
            defect_mass=ExactRational(len(reasons), 1),
            metadata={"is_refused": is_refused, "reasons": tuple(reasons), "sieve_size": len(admitted)},
        )
        return record, is_refused
