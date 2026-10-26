# -*- coding: utf-8 -*-
"""
Layer 1: CODA-FOC (Finite Obstruction Calculus).

Computes:
- Exact L1 quotient distance Phi_1([x]) = min_f ||x - D_0 f||_1
- Coherent cocycle violation Gamma_2([d_1 x]) = ||d_1 x||_1
- Dual witness certificates y* in ker(D_0^T) with ||y*||_infty <= 1
- Coherent residual classification (Phi_1 > 0, Gamma_2 == 0)

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Optional, Tuple

from coda_application.domain.entities import LayerExecutionRecord
from coda_application.domain.intake import IntakeData, intake
from coda_application.domain.value_objects import ExactRational, LayerId


def _data(problem: Any) -> IntakeData:
    return problem if isinstance(problem, IntakeData) else intake(problem)


def _er(value: Fraction) -> ExactRational:
    return ExactRational(value.numerator, value.denominator)

from coda_application.domain.l1_quotient import FunctionalEvaluator, QuotientCertificate, Tick, solve_l1_quotient
from coda_application.domain.value_objects import DualWitness


class Layer1FOC:
    """Evaluates Layer 1: Finite Obstruction Calculus."""

    @staticmethod
    def evaluate_certified(
        problem: Any, tick: Optional[Tick] = None, *, evaluator: FunctionalEvaluator
    ) -> Tuple[LayerExecutionRecord, ExactRational, ExactRational, Optional[DualWitness], QuotientCertificate]:
        """Layer 1 with its checked primal/dual certificate (see ``l1_quotient``)."""
        data = _data(problem)
        tick = tick or (lambda: None)
        gamma2 = _er(evaluator.closure(data.d0_rows, data.d0_shape[1], data.d1_rows, data.cochain, tick))
        cert = solve_l1_quotient(data.d0_rows, data.d0_shape[1], data.cochain, tick, evaluator=evaluator)
        phi1 = _er(cert.distance)
        witness = DualWitness.from_fractions(cert.witness, cert.distance) if cert.distance > 0 else None
        if cert.distance == 0:
            msg = "Cochain is in im(d0): exact zero quotient defect with an exact repair"
        else:
            msg = f"Non-trivial quotient obstruction Phi_1={cert.distance} (primal repair and dual witness agree)"
        record = LayerExecutionRecord(
            layer_id=LayerId.FOC,
            succeeded=gamma2.is_zero,
            diagnostic_message=msg,
            defect_mass=phi1,
            metadata={
                "phi1": phi1.to_tuple(),
                "gamma2": gamma2.to_tuple(),
                "is_coherent": gamma2.is_zero,
                "solver": cert.method,
                "certificate_verified": True,
            },
        )
        return record, phi1, gamma2, witness, cert

    @staticmethod
    def evaluate(problem: Any, *, evaluator: FunctionalEvaluator) -> Tuple[LayerExecutionRecord, ExactRational, ExactRational, Optional[DualWitness]]:
        """
        Executes Layer 1 obstruction and quotient evaluation.
        Returns LayerExecutionRecord, Phi_1, Gamma_2, and optional DualWitness.
        """
        record, phi1, gamma2, witness, _cert = Layer1FOC.evaluate_certified(problem, evaluator=evaluator)
        return record, phi1, gamma2, witness
