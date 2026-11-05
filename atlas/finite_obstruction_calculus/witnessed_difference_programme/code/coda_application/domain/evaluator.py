# -*- coding: utf-8 -*-
"""
The single evaluation path: intake, then Layers 1-7, producing sealed evidence.

Both entry points (the nine-layer pipeline and the proposal/evaluation/authority
triad) call ``compute_evidence``, so they cannot disagree about evidence. The budget
guard is checked while the native process runs; exhaustion terminates that process.
Native simplex pivots have a separate limit of 100000.
Exhaustion yields evidence with ``budget_satisfied=False`` and unknown Phi_1/Gamma_2;
a malformed instance yields evidence carrying ``refusal_reason``; any other fault is
caught and named. Nothing escapes as an exception, and nothing is fabricated.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Any, List, Optional

from coda_application.domain._seal import digest, seal
from coda_application.domain.budget import BudgetExhaustedError, NonTerminalBudgetGuard
from coda_application.domain.contracts import EvaluationContract, evidence_body
from coda_application.domain.entities import LayerExecutionRecord
from coda_application.domain.intake import IntakeData, IntakeError, intake
from coda_application.domain.layers import Layer1FOC, Layer2MUR, Layer3CS, Layer4CSQ, Layer5Q, Layer6A, Layer7OR
from coda_application.domain.value_objects import ExactRational, LayerId


def _sealed(**fields: Any) -> EvaluationContract:
    draft = EvaluationContract(**fields)
    body = evidence_body(draft)
    return EvaluationContract(**{**fields, "evidence_digest": digest(body), "seal": seal("evaluation", body)})


def compute_evidence(problem: Any, guard: NonTerminalBudgetGuard, *, evaluator) -> EvaluationContract:
    """Evaluate with an operator-supplied trusted port and an entered guard.

    Proposals cannot choose this port. The outer application composition root supplies the native
    adapter. Seals protect submitted data, not hostile code in this interpreter.
    """
    records: List[LayerExecutionRecord] = []
    pid = getattr(problem, "problem_id", "")
    pid = pid if isinstance(pid, str) else repr(pid)
    data: Optional[IntakeData] = None
    try:
        data = intake(problem)
        guard.tick()
        rec1, phi1, gamma2, witness, cert = Layer1FOC.evaluate_certified(data, guard.check, evaluator=evaluator)
        records.append(rec1)
        for layer in (Layer2MUR, Layer3CS, Layer4CSQ, Layer5Q):
            guard.tick()
            records.append(layer.evaluate(data, evaluator=evaluator, tick=guard.check)[0]
                           if layer in (Layer2MUR, Layer4CSQ) else layer.evaluate(data)[0])
        guard.tick()
        records.append(Layer6A.evaluate(data, phi1, gamma2)[0])
        guard.tick()
        records.append(Layer7OR.evaluate(data, gamma2)[0])
    except BudgetExhaustedError as exc:
        return _sealed(
            problem_id=pid,
            phi1=None,
            gamma2=None,
            dual_witness=None,
            is_mathematically_valid=False,
            layer_records=tuple(records),
            elapsed_seconds=guard.exact_elapsed_rational,
            budget_satisfied=False,
            problem_digest=data.digest if data else "",
            refusal_reason=f"budget exhausted before a terminal certificate: {exc}",
        )
    except IntakeError as exc:
        return _sealed(
            problem_id=pid,
            phi1=None,
            gamma2=None,
            dual_witness=None,
            is_mathematically_valid=False,
            layer_records=(
                LayerExecutionRecord(
                    layer_id=LayerId.FOC,
                    succeeded=False,
                    diagnostic_message=f"Intake refused a malformed instance: {exc}",
                    defect_mass=ExactRational(1, 1),
                ),
            ),
            elapsed_seconds=guard.exact_elapsed_rational,
            budget_satisfied=True,
            refusal_reason=f"malformed instance: {exc}",
        )
    except Exception as exc:  # fail closed with a named reason; never a fourth terminal
        return _sealed(
            problem_id=pid,
            phi1=None,
            gamma2=None,
            dual_witness=None,
            is_mathematically_valid=False,
            layer_records=tuple(records),
            elapsed_seconds=guard.exact_elapsed_rational,
            budget_satisfied=True,
            problem_digest=data.digest if data else "",
            refusal_reason=f"evaluation fault: {type(exc).__name__}: {exc}"[:300],
        )
    return _sealed(
        problem_id=pid,
        phi1=phi1,
        gamma2=gamma2,
        dual_witness=witness,
        is_mathematically_valid=phi1.is_zero and gamma2.is_zero,
        layer_records=tuple(records),
        elapsed_seconds=guard.exact_elapsed_rational,
        budget_satisfied=True,
        primal_repair=tuple(ExactRational(v.numerator, v.denominator) for v in cert.repair),
        problem_digest=data.digest,
    )
