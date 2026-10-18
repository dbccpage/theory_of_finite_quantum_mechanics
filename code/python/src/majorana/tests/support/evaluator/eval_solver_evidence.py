"""Checks and policy decisions over unverified solver evidence."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable, Optional, Sequence

from omega_engine.crates.type.solver_evidence import (
    CertificateKind,
    SolverDiagnostics,
    SolverError,
    SolverResult,
)


def assert_deterministic(solver: object, problem: object) -> None:
    first = solver.solve(problem)  # type: ignore[attr-defined]
    second = solver.solve(problem)  # type: ignore[attr-defined]
    if first != second:
        raise AssertionError("solver output drifted on identical input")


def assert_disclosure(result: SolverResult[object]) -> None:
    diagnostics = result.diagnostics
    if not diagnostics.converged:
        if (
            diagnostics.primal_residual is None
            and diagnostics.dual_residual is None
        ):
            raise AssertionError("approximate solver did not disclose residuals")
        if diagnostics.iteration_count is None:
            raise AssertionError("approximate solver did not disclose iteration_count")


def assert_non_finite_rejected(solver: object, bad_input: object) -> None:
    try:
        solver.solve(bad_input)  # type: ignore[attr-defined]
    except SolverError as error:
        if error.kind == SolverError.NON_FINITE_INPUT:
            return
    raise AssertionError("solver did not reject non-finite input")


def assert_repeated_same_input(
    solver: object,
    problem: object,
    runs: int,
) -> None:
    baseline = solver.solve(problem)  # type: ignore[attr-defined]
    for _ in range(runs):
        if solver.solve(problem) != baseline:  # type: ignore[attr-defined]
            raise AssertionError("hidden state affected semantic output")


def assert_canonical_equivalent_input(
    solver: object,
    first_input: object,
    second_input: object,
    canonicalize_out: Callable[[object], object],
) -> None:
    first = solver.solve(first_input)  # type: ignore[attr-defined]
    second = solver.solve(second_input)  # type: ignore[attr-defined]
    if canonicalize_out(first.value) != canonicalize_out(second.value):
        raise AssertionError("equivalent inputs yielded non-equivalent outputs")


@dataclass(frozen=True)
class TrustPolicy:
    """External consumption policy; not part of SolverKernel."""

    required_certificates: tuple[CertificateKind, ...] = ()
    allow_approximate: bool = False
    max_residual: Optional[float] = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "required_certificates",
            tuple(self.required_certificates),
        )


@dataclass(frozen=True)
class TrustDecision:
    trusted: bool
    reason: str = ""

    @classmethod
    def new_trusted(cls) -> "TrustDecision":
        return cls(True)

    @classmethod
    def untrusted(cls, reason: str) -> "TrustDecision":
        return cls(False, reason)


def decide_trust(
    result: SolverResult[object],
    policy: TrustPolicy,
) -> TrustDecision:
    diagnostics: SolverDiagnostics = result.diagnostics
    for required in policy.required_certificates:
        if not any(item.kind == required for item in diagnostics.certificates):
            return TrustDecision.untrusted(
                f"Missing required proof-artifact candidate kind: {required}"
            )
    if not diagnostics.converged and not policy.allow_approximate:
        return TrustDecision.untrusted("Approximate solution not allowed")
    for residual in (
        diagnostics.primal_residual,
        diagnostics.dual_residual,
        diagnostics.primal_dual_gap,
    ):
        if residual is None:
            continue
        if not math.isfinite(residual):
            return TrustDecision.untrusted("Non-finite residual or gap")
        if residual < 0:
            return TrustDecision.untrusted("Negative residual or gap")
        if policy.max_residual is not None and residual > policy.max_residual:
            return TrustDecision.untrusted("Residual or gap exceeds policy")
    return TrustDecision.new_trusted()


class TrustRefusal(Exception):
    """External policy refusal; never a SolverKernel completion state."""


def enforce_trust_or_refuse(decision: TrustDecision) -> None:
    if not decision.trusted:
        raise TrustRefusal(
            f"Untrusted solver evidence; external policy refused use: {decision.reason}"
        )


__all__ = [
    "TrustDecision",
    "TrustPolicy",
    "TrustRefusal",
    "assert_canonical_equivalent_input",
    "assert_deterministic",
    "assert_disclosure",
    "assert_non_finite_rejected",
    "assert_repeated_same_input",
    "decide_trust",
    "enforce_trust_or_refuse",
]
