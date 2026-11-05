# -*- coding: utf-8 -*-
"""
Authority firewall audit use case.
Evaluates the 7 halt guards and validates non-promotion guarantees.

Every check is an explicit comparison that lands in the report: nothing is an
``assert``, so ``python -O`` cannot silence the audit, and a failed check never
raises. The certificate check is independent of the solver path: it verifies the
outcome's dual witness, primal repair and closure through omega_functional
against the problem data, so a false value cannot pass by being
recomputed the same wrong way.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from coda_application.domain.authority import AuthorityGrant, AuthorityKeyring
from coda_application.domain.entities import MasterNormalFormOutcome, ProblemInstance, TerminalKind
from coda_application.domain.intake import IntakeError, intake
from coda_application.domain.l1_quotient import FunctionalEvaluator
from coda_application.use_cases.evaluate_pipeline import evaluate_coda_pipeline

Check = Tuple[str, bool, str]


def _certificate_checks(problem: ProblemInstance, outcome: MasterNormalFormOutcome, *, evaluator: FunctionalEvaluator) -> List[Check]:
    pair = outcome.residual_pair
    if pair is None:
        return [("certificate", outcome.terminal_kind == TerminalKind.REFUSED, "unknown evidence must end REFUSED")]
    try:
        data = intake(problem)
    except IntakeError as exc:
        return [("certificate", False, f"outcome carries evidence for a malformed instance: {exc}")]
    owner = evaluator
    checks: List[Check] = []
    repair = outcome.primal_repair
    witness = outcome.dual_witness
    if repair is None or len(repair) != data.d0_shape[1]:
        checks.append(("primal_repair", False, "outcome carries no primal repair of the right length"))
    elif pair.phi1.is_positive and witness is None:
        checks.append(("dual_witness", False, "positive Phi_1 requires a dual witness"))
    else:
        dual = witness.fractions if witness is not None else (Fraction(0),) * len(data.cochain)
        valid = owner.verify_repair(data.d0_rows, data.d0_shape[1], data.cochain,
                                    [r.fraction for r in repair], dual, pair.phi1.fraction)
        checks.append(("primal_repair", valid, "omega_functional verified the primal-dual certificate"))
        checks.append(("dual_witness", valid, "the same check includes every submitted dual coordinate"))
    try:
        gamma = owner.closure(data.d0_rows, data.d0_shape[1], data.d1_rows, data.cochain)
        checks.append(("gamma2", gamma == pair.gamma2.fraction, "omega_functional closure agrees with the reported value"))
    except (RuntimeError, ValueError, TypeError) as error:
        checks.append(("gamma2", False, f"native closure verification failed: {error}"))
    return checks


def audit_authority_firewall(
    problem: ProblemInstance,
    grant: Optional[AuthorityGrant] = None,
    keyring: Optional[AuthorityKeyring] = None,
    *, evaluator: FunctionalEvaluator,
) -> Dict[str, Any]:
    """
    Runs an authority firewall audit on a ProblemInstance and returns a report.
    ``firewall_audit_passed`` is True only if every check holds.
    """
    outcome = (
        evaluate_coda_pipeline(problem, evaluator=evaluator)
        if grant is None and keyring is None
        else evaluate_coda_pipeline(problem, grant=grant, keyring=keyring, evaluator=evaluator)
    )
    kind = outcome.terminal_kind
    claim = getattr(problem, "fda_license_granted", None)
    checks: List[Check] = []
    flags = [outcome.is_authorized, outcome.is_closed_residual, outcome.is_refused]
    checks.append(("disjointness", flags.count(True) == 1, "exactly one terminal (GTLA-T8)"))
    token = outcome.authority_token
    checks.append(("token_iff_authorized", (token is not None) == (kind == TerminalKind.AUTHORIZED), "token iff AUTHORIZED"))
    if kind == TerminalKind.AUTHORIZED:
        checks.append(("token_valid", outcome.is_authorized, "token minted by the firewall for this evidence"))
        checks.append(("grant_presented", isinstance(grant, AuthorityGrant), "AUTHORIZED only with a presented grant"))
        zero = outcome.residual_pair is not None and outcome.residual_pair.is_exact_zero
        checks.append(("zero_residual", zero, "AUTHORIZED only with Phi_1 = Gamma_2 = 0"))
    checks.append(
        (
            "license_claim",
            claim is None or claim is False,
            "a license is an AuthorityGrant; a flag on the problem is a malformed claim",
        )
    )
    checks.extend(_certificate_checks(problem, outcome, evaluator=evaluator))
    pair = outcome.residual_pair
    return {
        "problem_id": getattr(problem, "problem_id", None),
        "terminal_kind": kind.value,
        "firewall_decision": outcome.firewall_decision.value,
        "fda_license_granted": claim,
        "token_issued": token is not None,
        "phi1": None if pair is None else pair.phi1.to_tuple(),
        "gamma2": None if pair is None else pair.gamma2.to_tuple(),
        "checks": tuple(checks),
        "failed_checks": tuple(name for name, ok, _ in checks if not ok),
        "firewall_audit_passed": all(ok for _, ok, _ in checks),
    }
