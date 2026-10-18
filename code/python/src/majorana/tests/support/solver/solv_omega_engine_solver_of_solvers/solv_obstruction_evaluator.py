"""OESOS–DDA exact rational obstruction evaluator (Gate 11).

Public façade over the existing FiniteCochainComplex + analyze_finite_cochain.
AuthorityEffect: None. Independently verifiable over Q. Claim-bounded.

Paper vocabulary (Prop 4.1 / 4.4):
  NONCLOSED         ↔ Γ₂ > 0
  EXACT             ↔ Γ₂ = 0 ∧ Φ₁ = 0
  CLOSED_NONEXACT   ↔ Γ₂ = 0 ∧ Φ₁ > 0
  INVALID_COMPLEX   ↔ d₁d₀ ≠ 0
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Sequence

from omega_engine.crates.homology_theory.finite_cochain_complex import (
    FiniteCochainComplex,
    Vector,
    Scalar,
)
from omega_engine.crates.solver.solv_finite_cochain_obstruction import (
    analyze_finite_cochain,
    CochainAnalysis,
    Verdict,
)


class ObstructionClass(str, Enum):
    """Paper trichotomy + invalid-complex sentinel."""

    NONCLOSED = "NONCLOSED"
    EXACT = "EXACT"
    CLOSED_NONEXACT = "CLOSED_NONEXACT"
    INVALID_COMPLEX = "INVALID_COMPLEX"


def _l1_norm(vec: Vector, weights: Sequence[Scalar] | None = None) -> Scalar:
    if not vec:
        return Fraction(0)
    if weights is None:
        return sum((abs(x) for x in vec), Fraction(0))
    if len(weights) != len(vec):
        raise ValueError("weights length must match vector length")
    return sum((w * abs(x) for w, x in zip(weights, vec)), Fraction(0))


@dataclass(frozen=True)
class ObstructionReceipt:
    """Independently verifiable Exact-status receipt. AuthorityEffect: None."""

    classification: ObstructionClass
    phi1: Scalar | None
    gamma2: Scalar | None
    alpha: Vector | None
    dual_phi: Vector | None
    residual: Vector | None
    evidence_sha256: str
    independently_verifiable: bool
    coefficient_domain: str = "Q"
    authority_effect: str = "None"
    # Optional future: model_digest, protected_set, weights, dual feasibility checks


def evaluate_obstruction(
    complex_: FiniteCochainComplex,
    omega: Sequence[int | str | Fraction],
    w: Sequence[Fraction] | None = None,
    v: Sequence[Fraction] | None = None,
) -> ObstructionReceipt:
    """Single public Exact entry point required by OESOS–DDA canonical v0.1.

    - Exact arithmetic over Q only (floats forbidden upstream).
    - Maps existing CochainAnalysis onto paper trichotomy.
    - Surfaces quantitative Φ₁ = ‖residual‖₁,w and Γ₂ = ‖d₁ω‖₁,v.
    - Dual period witness for CLOSED_NONEXACT (cohomological separator).
    - AuthorityEffect hard-coded to None; never a license.
    """
    analysis: CochainAnalysis = analyze_finite_cochain(complex_, omega)

    # Quantitative closure defect Γ₂
    gamma2 = _l1_norm(analysis.closure_defect, v)

    # Quantitative Φ₁ and residual / repair
    if analysis.verdict is Verdict.EXACT_REPAIR:
        phi1 = Fraction(0)
        residual = tuple(Fraction(0) for _ in analysis.beta)
        alpha = analysis.primitive_witness
        dual_phi = None
        classification = ObstructionClass.EXACT
    elif analysis.verdict is Verdict.CLOSED_RESIDUAL:
        residual = analysis.residual_representative or analysis.beta
        phi1 = _l1_norm(residual, w)
        alpha = None
        dual_phi = analysis.period_witness
        classification = ObstructionClass.CLOSED_NONEXACT
    elif analysis.verdict is Verdict.CURVATURE:
        residual = analysis.beta
        phi1 = _l1_norm(residual, w)  # residual after attempted gauge still carries curvature
        alpha = None
        dual_phi = None
        classification = ObstructionClass.NONCLOSED
    else:
        residual = analysis.beta
        phi1 = None
        gamma2 = None
        alpha = None
        dual_phi = None
        classification = ObstructionClass.INVALID_COMPLEX

    # Independent verifiability is already enforced by the exact solver
    # (assertions on witnesses, SHA-256 binding of the full computation).
    independently_verifiable = True

    return ObstructionReceipt(
        classification=classification,
        phi1=phi1,
        gamma2=gamma2,
        alpha=alpha,
        dual_phi=dual_phi,
        residual=residual,
        evidence_sha256=analysis.evidence_sha256,
        independently_verifiable=independently_verifiable,
        coefficient_domain=analysis.coefficient_domain,
        authority_effect="None",
    )


# Convenience re-export for cascade / self-solver layers
solve_obstruction = evaluate_obstruction

__all__ = [
    "ObstructionClass",
    "ObstructionReceipt",
    "evaluate_obstruction",
    "solve_obstruction",
]
