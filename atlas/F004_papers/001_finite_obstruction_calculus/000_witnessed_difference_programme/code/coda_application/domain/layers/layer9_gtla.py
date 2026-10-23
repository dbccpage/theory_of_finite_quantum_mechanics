# -*- coding: utf-8 -*-
"""
Layer 9: CODA-GTLA (General Theory of Layered Authority & Master Normal Form).

Routes a checked finite run into one of three disjoint terminal record types.
It does not establish the paper's general Kleisli factorization or a
universal Master Normal Form theorem.

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

from typing import List

from coda_application.domain.entities import AuthorityToken, MasterNormalFormOutcome, ResidualPair, TerminalKind
from coda_application.domain.value_objects import DualWitness, FirewallDecision


class Layer9GTLA:
    """Evaluates Layer 9: GTLA Master Normal Form Terminalization."""

    @staticmethod
    def terminalize(
        problem: Any,
        phi1: Optional[ExactRational],
        gamma2: Optional[ExactRational],
        dual_witness: Optional[DualWitness],
        firewall_decision: FirewallDecision,
        authority_token: Optional[AuthorityToken],
        layer_records: List[LayerExecutionRecord],
        reason: Optional[str] = None,
        primal_repair: Optional[Tuple[ExactRational, ...]] = None,
        evidence_digest: str = "",
    ) -> MasterNormalFormOutcome:
        """
        Terminalizes the 9-layer pipeline execution into the definitive MasterNormalFormOutcome.
        Unknown evidence (phi1 or gamma2 None) is carried as an unknown residual pair.
        """
        residual_pair = None if phi1 is None or gamma2 is None else ResidualPair(phi1=phi1, gamma2=gamma2)
        if firewall_decision == FirewallDecision.PERMIT_AUTHORIZED and authority_token is not None:
            terminal_kind = TerminalKind.AUTHORIZED
            default_reason = "Pipeline authorized under a verified external grant"
            defect_mass = ExactRational(0, 1)
        elif firewall_decision == FirewallDecision.ROUTE_CLOSED_RESIDUAL:
            terminal_kind = TerminalKind.CLOSED_RESIDUAL
            default_reason = "Pipeline terminated in CLOSED_RESIDUAL; non-promoted"
            defect_mass = phi1 if phi1 is not None else ExactRational(1, 1)
        else:
            terminal_kind = TerminalKind.REFUSED
            default_reason = "Pipeline terminated in REFUSED: a halt guard or layer refused"
            defect_mass = ExactRational(1, 1)
        gtla_record = LayerExecutionRecord(
            layer_id=LayerId.GTLA,
            succeeded=True,
            diagnostic_message=f"GTLA Terminalization complete: outcome={terminal_kind.value}",
            defect_mass=defect_mass,
            metadata={
                "terminal_kind": terminal_kind.value,
                "is_authorized": terminal_kind == TerminalKind.AUTHORIZED,
                "is_closed_residual": terminal_kind == TerminalKind.CLOSED_RESIDUAL,
                "is_refused": terminal_kind == TerminalKind.REFUSED,
            },
        )
        return MasterNormalFormOutcome(
            problem_id=problem.problem_id if isinstance(getattr(problem, "problem_id", None), str) else "<malformed>",
            terminal_kind=terminal_kind,
            residual_pair=residual_pair,
            dual_witness=dual_witness,
            authority_token=authority_token if terminal_kind == TerminalKind.AUTHORIZED else None,
            layer_records=tuple(layer_records) + (gtla_record,),
            firewall_decision=firewall_decision,
            reason=reason or default_reason,
            primal_repair=primal_repair,
            evidence_digest=evidence_digest,
        )
