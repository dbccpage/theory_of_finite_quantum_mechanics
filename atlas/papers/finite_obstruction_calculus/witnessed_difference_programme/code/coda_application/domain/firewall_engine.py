# -*- coding: utf-8 -*-
"""
Authority Firewall Engine (Paper 027 & Paper 030).
Enforces the Coproduct Separation Invariant:
    T = T_auth + T_res + F_term

Evaluates the 7 explicit halt guards to prevent authority fabrication,
role impersonation, or unearned promotion of epistemic evidence.

The firewall trusts nothing it is handed:

* evidence must name this problem and its digest; evidence the stack did not seal is
  recomputed, and every claimed value (Phi_1, Gamma_2, validity, layer outcomes) must
  match the recomputation;
* a supplied dual witness is checked for kernel membership, ||y||_inf <= 1 and the
  pairing, whatever Phi_1 is;
* routing uses the verified evidence and requires every layer record to succeed;
* authority is an ``AuthorityGrant`` verified against a keyring, bound to this problem,
  this evidence and this proposer, and spent once. A boolean, a string or any other
  claim is not a grant; presenting one for zero-defect evidence is refused.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from coda_application.domain.anomalon_registry import AnomalonRegistry
from coda_application.domain.authority import AuthorityGrant, AuthorityKeyring, _mint_token
from coda_application.domain.budget import BudgetExhaustedError, NonTerminalBudgetGuard
from coda_application.domain.contracts import (
    GUARD_3_NOT_APPLICABLE,
    AuthorityContract,
    EvaluationContract,
    ProposalContract,
)
from coda_application.domain.entities import AuthorityToken, LayerExecutionRecord, ProblemInstance, TerminalKind
from coda_application.domain.evaluator import compute_evidence
from coda_application.domain.intake import IntakeData, IntakeError, intake
from coda_application.domain.layers import Layer8FDA, Layer9GTLA
from coda_application.domain.value_objects import DualWitness, ExactRational, FirewallDecision

ROLES = frozenset({"PROPOSER", "REFEREE", "AUTHORITY"})


class _Refusal(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason




class AuthorityFirewallEngine:
    """
    Routes verified evidence and independently supplied authority grants.
    Strictly separates epistemic evidence (EvaluationContract) from normative authorization (AuthorityContract).
    """

    GUARD_1_ROLE_SEPARATION = "GUARD_1_ROLE_SEPARATION"
    GUARD_2_EXACT_ARITHMETIC = "GUARD_2_EXACT_ARITHMETIC"
    GUARD_3_DUAL_WITNESS_VALIDATION = "GUARD_3_DUAL_WITNESS_VALIDATION"
    GUARD_4_COCYCLE_CONSISTENCY = "GUARD_4_COCYCLE_CONSISTENCY"
    GUARD_5_AUTHORITY_GAP = "GUARD_5_AUTHORITY_GAP"
    GUARD_6_NON_TERMINAL_BUDGET = "GUARD_6_NON_TERMINAL_BUDGET"
    GUARD_7_VERIFICATION_LIMITS = "GUARD_7_VERIFICATION_LIMITS"

    @classmethod
    def evaluate_authority(
        cls,
        proposal: ProposalContract,
        evaluation: EvaluationContract,
        problem: ProblemInstance,
        caller_role: Any = "PROPOSER",
        external_license_granted: Any = None,
        is_self_referential_or_undecidable: Any = None,
        keyring: Optional[AuthorityKeyring] = None,
        max_seconds: float = NonTerminalBudgetGuard.DEFAULT_MAX_SECONDS,
        max_steps: int = NonTerminalBudgetGuard.DEFAULT_MAX_STEPS,
        clock: Any = None,
        functional_evaluator: Any = None,
    ) -> AuthorityContract:
        """
        Passes proposal and evaluation evidence through all 7 halt guards.
        Emits an AuthorityContract routing strictly into T_auth, T_res, or F_term.

        ``external_license_granted`` must be an ``AuthorityGrant`` to authorize; ``None``
        and ``False`` mean no license. ``is_self_referential_or_undecidable`` can only
        refuse: ``None``/``False`` pass, anything else halts into refusal. ``keyring``
        holds the recognised authorities' verification keys (operator configuration).
        ``functional_evaluator`` is likewise trusted operator configuration, not
        proposal data. Public use cases construct the canonical native adapter.
        The process-private seal does not isolate hostile same-process code.
        """
        passed: List[str] = []
        guards: Dict[str, bool] = {}
        try:
            return cls._evaluate(
                proposal, evaluation, problem, caller_role, external_license_granted,
                is_self_referential_or_undecidable, keyring, max_seconds, max_steps, clock, passed, guards, functional_evaluator,
            )
        except BudgetExhaustedError as exc:
            return cls._emit(
                problem, evaluation, None, TerminalKind.REFUSED,
                f"HALT_GUARD_6_BREACH: budget exhausted during certificate verification: {exc}"[:300],
                passed, guards,
            )
        except _Refusal as refusal:
            return cls._emit(problem, evaluation, None, TerminalKind.REFUSED, refusal.reason, passed, guards)
        except Exception as exc:  # fail closed: an internal fault is a refusal, never a fourth terminal
            return cls._emit(
                problem, evaluation, None, TerminalKind.REFUSED,
                f"HALT_INTERNAL_FAULT: {type(exc).__name__}: {exc}"[:300], passed, guards,
            )

    @classmethod
    def _evaluate(cls, proposal, evaluation, problem, caller_role, license_value, self_ref, keyring,
                  max_seconds, max_steps, clock, passed, guards, functional_evaluator) -> AuthorityContract:
        grant = license_value if type(license_value) is AuthorityGrant else None
        grant_verified = grant is not None and isinstance(keyring, AuthorityKeyring) and keyring.verify(grant)

        # GUARD 1: Role Non-Impersonation (Paper 004). Exact ASCII roles only.
        role = caller_role.upper() if isinstance(caller_role, str) and caller_role.isascii() else None
        if role not in ROLES:
            raise _Refusal(f"HALT_GUARD_1_BREACH: Unknown or malformed caller role {caller_role!r}")
        if role == "AUTHORITY" and not grant_verified:
            raise _Refusal("HALT_GUARD_1_BREACH: Caller attempted unauthorized role impersonation as AUTHORITY")
        passed.append(cls.GUARD_1_ROLE_SEPARATION)
        guards["role"] = True

        # GUARD 6: Non-Terminal Budget Guard (Paper 028). Incomplete evidence carries no certificate.
        if not isinstance(evaluation, EvaluationContract):
            raise _Refusal("HALT_GUARD_2_BREACH: evidence is not an EvaluationContract")
        if evaluation.budget_satisfied is not True:
            raise _Refusal("HALT_GUARD_6_BREACH: Non-terminal computational budget exhausted (BudgetUnknown)")

        # GUARD 2: Exact arithmetic and well-formed, fully known evidence.
        if evaluation.refusal_reason:
            raise _Refusal(f"HALT_GUARD_2_BREACH: {evaluation.refusal_reason}")
        if not isinstance(evaluation.phi1, ExactRational) or not isinstance(evaluation.gamma2, ExactRational):
            raise _Refusal("HALT_GUARD_2_BREACH: evidence does not carry exact Phi_1 and Gamma_2")
        if not isinstance(proposal, ProposalContract) or not isinstance(problem, ProblemInstance):
            raise _Refusal("HALT_GUARD_2_BREACH: proposal or problem has the wrong type")
        try:
            data = intake(problem)
            proposed_data = intake(proposal.problem)
        except IntakeError as exc:
            raise _Refusal(f"HALT_GUARD_2_BREACH: malformed instance: {exc}") from exc
        # Binding: the evidence and the proposal must be about this problem.
        if evaluation.problem_id != data.problem_id or proposal.problem.problem_id != data.problem_id:
            raise _Refusal("HALT_GUARD_2_BREACH: evidence or proposal names a different problem")
        if proposed_data.digest != data.digest:
            raise _Refusal("HALT_GUARD_2_BREACH: proposal contains a different problem digest")
        if evaluation.problem_digest and evaluation.problem_digest != data.digest:
            raise _Refusal("HALT_GUARD_2_BREACH: evidence was computed for a different problem digest")

        # GUARD 3: every supplied witness must certify the claimed Phi_1 for this problem.
        claimed_phi1 = evaluation.phi1.fraction
        if claimed_phi1 < 0:
            raise _Refusal("HALT_GUARD_3_BREACH: negative quotient defect Phi_1")
        if claimed_phi1 > 0 and evaluation.dual_witness is None:
            raise _Refusal("HALT_GUARD_3_BREACH: Non-zero Phi_1 lacks dual witness certificate")
        if evaluation.dual_witness is not None:
            if len(evaluation.dual_witness.fractions) != data.d0_shape[0]:
                raise _Refusal("HALT_GUARD_3_BREACH: Dual witness shape mismatch")

        # GUARD 4: Cocycle consistency.
        if evaluation.gamma2.fraction < 0:
            raise _Refusal("HALT_GUARD_4_BREACH: Negative cocycle defect Gamma_2")

        # Evidence the stack did not seal is recomputed; the claim must match exactly.
        trusted = evaluation
        if not (evaluation.is_sealed and evaluation.problem_digest == data.digest):
            guard = NonTerminalBudgetGuard(max_seconds=max_seconds, max_steps=max_steps, clock=clock)
            with guard:
                trusted = compute_evidence(problem, guard, evaluator=functional_evaluator)
            if trusted.budget_satisfied is not True:
                raise _Refusal("HALT_GUARD_6_BREACH: budget exhausted while recomputing unsealed evidence")
            if trusted.refusal_reason:
                raise _Refusal(f"HALT_GUARD_2_BREACH: {trusted.refusal_reason}")
            if trusted.phi1 != evaluation.phi1:
                raise _Refusal(
                    f"HALT_GUARD_3_BREACH: claimed Phi_1 {claimed_phi1} differs from the certified Phi_1 {trusted.phi1.fraction}"
                )
            if trusted.gamma2 != evaluation.gamma2:
                raise _Refusal(
                    f"HALT_GUARD_4_BREACH: claimed Gamma_2 {evaluation.gamma2.fraction} differs from the recomputed {trusted.gamma2.fraction}"
                )
            if trusted.is_mathematically_valid != evaluation.is_mathematically_valid:
                raise _Refusal("HALT_GUARD_2_BREACH: claimed validity flag contradicts the recomputed evidence")
            if evaluation.layer_records and [(r.layer_id, r.succeeded) for r in evaluation.layer_records] != [
                (r.layer_id, r.succeeded) for r in trusted.layer_records
            ]:
                raise _Refusal("HALT_GUARD_2_BREACH: claimed layer records contradict the recomputed evaluation")
        passed.append(cls.GUARD_2_EXACT_ARITHMETIC)
        guards["exact"] = True
        passed.append(cls.GUARD_4_COCYCLE_CONSISTENCY)
        guards["cocycle"] = True

        if evaluation.dual_witness is not None:
            if functional_evaluator is None or trusted.primal_repair is None:
                raise _Refusal("HALT_GUARD_3_BREACH: a native evaluator and checked primal repair are required")
            guard = NonTerminalBudgetGuard(max_seconds=max_seconds, max_steps=max_steps, clock=clock)
            with guard:
                valid = functional_evaluator.verify_repair(
                    data.d0_rows, data.d0_shape[1], data.cochain,
                    [r.fraction for r in trusted.primal_repair], evaluation.dual_witness.fractions,
                    claimed_phi1, guard.check,
                )
            if not valid:
                raise _Refusal("HALT_GUARD_3_BREACH: native primal-dual certificate verification failed")
            passed.append(cls.GUARD_3_DUAL_WITNESS_VALIDATION)
        else:
            passed.append(GUARD_3_NOT_APPLICABLE)
        guards["witness"] = True
        passed.append(cls.GUARD_6_NON_TERMINAL_BUDGET)
        guards["budget"] = True

        # GUARD 7: Verification Limits (Paper 030). The flag can only refuse.
        if self_ref is not None and self_ref is not False:
            raise _Refusal("HALT_GUARD_7_BREACH: Self-referential or undecidable envelope halted closed into refusal")
        passed.append(cls.GUARD_7_VERIFICATION_LIMITS)
        guards["verification_limits"] = True

        # ROUTING INTO COPRODUCT on verified evidence: T = T_auth + T_res + F_term
        failed = [r.layer_id.value for r in trusted.layer_records if not r.succeeded]
        if failed or not trusted.gamma2.is_zero:
            raise _Refusal(f"REFUSED: layer(s) {failed or ['FOC']} failed; Gamma_2={trusted.gamma2.fraction}")
        if trusted.phi1.is_positive:
            anomalon = AnomalonRegistry.get_global_registry().register_anomalon(
                problem_id=data.problem_id,
                phi1=trusted.phi1,
                gamma2=trusted.gamma2,
                d0=problem.d0,
                d1=problem.d1,
                defect=problem.defect_cochain,
                dual_witness=trusted.dual_witness,
            )
            passed.append(cls.GUARD_5_AUTHORITY_GAP)
            guards["authority_gap"] = True
            return cls._emit(
                problem, trusted, None, TerminalKind.CLOSED_RESIDUAL,
                f"CLOSED_RESIDUAL: Phi_1={trusted.phi1.fraction} retained as anomalon {anomalon.anomalon_id[:12]}",
                passed, guards, anomalon.anomalon_id,
            )

        # Zero defect, every layer succeeded: GTLA-T9 Non-Promotion Firewall.
        # An unlicensed Phi_1 = 0 yields F_term: REFUSED.
        if license_value is None or license_value is False:
            passed.append(cls.GUARD_5_AUTHORITY_GAP)
            guards["authority_gap"] = True
            return cls._emit(
                problem, trusted, None, TerminalKind.REFUSED,
                "REFUSED: zero defect verified, but no external grant was presented (GTLA-T9 Non-Promotion Firewall)",
                passed, guards,
            )
        if grant is None:
            raise _Refusal(
                f"HALT_GUARD_5_BREACH: license claim {type(license_value).__name__} is not a verified external grant"
            )
        if not grant_verified:
            raise _Refusal("HALT_GUARD_5_BREACH: grant is not signed by a recognised external authority")
        if grant.problem_digest != data.digest or grant.evidence_digest != trusted.evidence_digest:
            raise _Refusal("HALT_GUARD_5_BREACH: grant is bound to a different problem or different evidence")
        if grant.licensee != proposal.proposer_id:
            raise _Refusal("HALT_GUARD_5_BREACH: grant names a different licensee than this proposal")
        if not keyring.spend(grant):
            raise _Refusal("HALT_GUARD_5_BREACH: grant nonce already spent")
        passed.append(cls.GUARD_5_AUTHORITY_GAP)
        guards["authority_gap"] = True
        token = _mint_token(grant, keyring)
        return cls._emit(
            problem, trusted, token, TerminalKind.AUTHORIZED,
            f"AUTHORIZED: zero-defect evidence and a verified grant from {grant.authority_id}", passed, guards,
        )

    @classmethod
    def _emit(
        cls,
        problem: Any,
        evaluation: Any,
        token: Optional[AuthorityToken],
        terminal: TerminalKind,
        reason: str,
        passed: List[str],
        guards: Dict[str, bool],
        fingerprint: Optional[str] = None,
    ) -> AuthorityContract:
        decision = {
            TerminalKind.AUTHORIZED: FirewallDecision.PERMIT_AUTHORIZED,
            TerminalKind.CLOSED_RESIDUAL: FirewallDecision.ROUTE_CLOSED_RESIDUAL,
            TerminalKind.REFUSED: FirewallDecision.ROUTE_REFUSED,
        }[terminal]
        ev = evaluation if isinstance(evaluation, EvaluationContract) else None
        records: Tuple[LayerExecutionRecord, ...] = tuple(ev.layer_records) if ev else ()
        records += (Layer8FDA.record(decision, f"FDA firewall: {reason}", guards, token is not None),)
        outcome = Layer9GTLA.terminalize(
            problem=problem,
            phi1=ev.phi1 if ev and isinstance(ev.phi1, ExactRational) else None,
            gamma2=ev.gamma2 if ev and isinstance(ev.gamma2, ExactRational) else None,
            dual_witness=ev.dual_witness if ev else None,
            firewall_decision=decision,
            authority_token=token,
            layer_records=list(records),
            reason=reason,
            primal_repair=ev.primal_repair if ev else None,
            evidence_digest=ev.evidence_digest if ev else "",
        )
        return AuthorityContract(
            terminal_kind=terminal,
            authority_token=token,
            anomalon_fingerprint=fingerprint,
            halt_guards_passed=tuple(passed),
            decision_reason=reason,
            outcome=outcome,
        )
