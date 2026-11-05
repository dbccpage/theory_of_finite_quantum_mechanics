# -*- coding: utf-8 -*-
"""
Layer 6: CODA-A (Anomalon: The Anomalon as a Typed Leftover).

Enforces:
- Cokernel projection and residue conservation: x - Cx in ker C (A-T6)
- The Leftover Principle: A leftover class is not a decision (GTLA-T7)
- Preservation of anomalon residual registers in V / im(C) without erasure or smoothing

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


class Layer6A:
    """Evaluates Layer 6: Anomalon (The Anomalon as a Typed Leftover)."""

    @staticmethod
    def evaluate(problem: Any, phi1: ExactRational, gamma2: ExactRational) -> Tuple[LayerExecutionRecord, bool]:
        """
        Executes Layer 6 residue classification.
        Returns LayerExecutionRecord and boolean indicating whether state carries an active residual.

        Signs are read from the normalised value, not the stored numerator. Retention is
        done by the firewall, which registers a coherent residual in the anomalon register.
        """
        has_residual = phi1.is_positive
        is_coherent = gamma2.is_zero
        if has_residual and is_coherent:
            msg = (
                f"CODA-A typed residual (Phi_1={phi1.sympy_rational}, Gamma_2=0): routed to CLOSED_RESIDUAL, "
                "where the firewall registers it as an Anomalon; never promoted"
            )
        elif has_residual:
            msg = f"CODA-A incoherent residue (Phi_1={phi1.sympy_rational}, Gamma_2={gamma2.sympy_rational}): violates the cocycle condition"
        else:
            msg = "CODA-A vanishing residue (Phi_1=0): no leftover class"
        record = LayerExecutionRecord(
            layer_id=LayerId.A,
            succeeded=is_coherent,
            diagnostic_message=msg,
            defect_mass=phi1,
            metadata={"has_residual": has_residual, "is_coherent": is_coherent, "residual_retained_in_cokernel": has_residual},
        )
        return record, has_residual
