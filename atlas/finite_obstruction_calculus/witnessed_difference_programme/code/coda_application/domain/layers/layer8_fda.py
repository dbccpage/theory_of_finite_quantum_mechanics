# -*- coding: utf-8 -*-
"""
Layer 8: CODA-FDA (Finite Descent Authority).

Enforces:
- The Authority Conservation Law: Authority cannot be minted by internal derivation
- Strict Role Split: Runner != Authorizer, Proposer != Evaluator
- Non-Promotion Firewall: Zero defect (Phi_1=0, Gamma_2=0) WITHOUT external license NEVER promotes to Authorized
- Countermodels to Internal Self-Authorization (FDA-04)

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

from coda_application.domain.entities import AuthorityToken
from coda_application.domain.value_objects import FirewallDecision


class Layer8FDA:
    """Evaluates Layer 8: Finite Descent Authority."""

    @staticmethod
    def record(decision: FirewallDecision, message: str, guards: dict, token_issued: bool) -> LayerExecutionRecord:
        """The Layer 8 audit record the authority firewall emits for its decision."""
        return LayerExecutionRecord(
            layer_id=LayerId.FDA,
            succeeded=decision != FirewallDecision.ROUTE_REFUSED,
            diagnostic_message=message,
            defect_mass=ExactRational(0 if token_issued else 1, 1),
            metadata={"firewall_decision": decision.value, "token_issued": token_issued, "guards": dict(guards)},
        )

    @staticmethod
    def evaluate(
        problem: Any,
        phi1: ExactRational,
        gamma2: ExactRational,
        refused_by_or: bool,
    ) -> Tuple[LayerExecutionRecord, FirewallDecision, Optional[AuthorityToken]]:
        """
        Layer 8 routing for evidence alone. Returns the record, the decision and no token.

        This gate never mints authority. A token is issued only by
        ``AuthorityFirewallEngine`` for a grant verified against a keyring and bound to
        this evidence; a license flag on the problem is a claim, not a grant.
        """
        if refused_by_or is not False:
            decision, msg = FirewallDecision.ROUTE_REFUSED, "FDA gate: upstream refusal"
        elif not gamma2.is_zero:
            decision, msg = FirewallDecision.ROUTE_REFUSED, f"FDA gate: incoherent cocycle defect Gamma_2={gamma2.sympy_rational}"
        elif phi1.is_positive or not phi1.is_zero:
            decision = FirewallDecision.ROUTE_CLOSED_RESIDUAL
            msg = f"FDA gate: non-zero quotient defect Phi_1={phi1.sympy_rational} retained; non-promotion"
        else:
            decision = FirewallDecision.ROUTE_CLOSED_RESIDUAL
            msg = "FDA gate: zero defect; authorization requires a verified external grant at the firewall"
        guards = {"upstream_refusal": refused_by_or is not False, "coherent": gamma2.is_zero, "zero_defect": phi1.is_zero}
        return Layer8FDA.record(decision, msg, guards, False), decision, None
