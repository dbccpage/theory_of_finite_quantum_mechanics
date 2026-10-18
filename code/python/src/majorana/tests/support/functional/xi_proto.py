"""PROTO formula-mirror of omega_functional XiFunctional (typed).

AuthorityEffect: None. FORMULA_MIRROR of Rust ``xi.rs`` — not PyO3 FFI_BOUND.

Faithful to ``XiFunctional::compute`` (see omega_functional/src/xi.rs):
  - ExactZero when finite phi1_value <= tolerance (includes negative Φ₁)
  - density lifts ψ_e = sign(v_e) · √(|v_e|/‖v‖₁)
  - pure-state half-normalized distance √(1 − |⟨ψ|φ⟩|²) (or 2×)
  - saturation: |⟨primal_residual, dual_witness⟩ − phi1_value| <= tolerance
  - typed invalidity: NonFiniteInput / DensityLiftUndefined / SaturationFailed
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Sequence, Tuple, Union


class XiValidity(str, Enum):
    Valid = "Valid"
    SaturationFailed = "SaturationFailed"
    DensityLiftUndefined = "DensityLiftUndefined"
    NonFiniteInput = "NonFiniteInput"
    FirewallNotChecked = "FirewallNotChecked"


@dataclass(frozen=True)
class DensityLiftProto:
    state_vector: Tuple[float, ...]
    total_mass: float


@dataclass(frozen=True)
class XiResult:
    value: float
    validity: XiValidity
    primal_density: Optional[DensityLiftProto]
    dual_density: Optional[DensityLiftProto]
    saturation_verified: bool


class XiComputationKind(str, Enum):
    ExactZero = "ExactZero"
    ValidTieBreaker = "ValidTieBreaker"
    Invalid = "Invalid"


@dataclass(frozen=True)
class XiComputation:
    kind: XiComputationKind
    validity: Optional[XiValidity] = None
    result: Optional[XiResult] = None

    @property
    def is_valid(self) -> bool:
        return self.kind in (
            XiComputationKind.ExactZero,
            XiComputationKind.ValidTieBreaker,
        )

    def value_or_raise(self) -> float:
        if self.kind is XiComputationKind.ExactZero:
            return 0.0
        if self.kind is XiComputationKind.ValidTieBreaker and self.result is not None:
            return float(self.result.value)
        raise ValueError(f"xi computation invalid: {self.validity}")


def residual_l1_mass(vector: Sequence[float]) -> float:
    """Unweighted ell-1 mass M(v) = ‖v‖₁. Helper only — not a residual authority."""
    return float(sum(abs(float(x)) for x in vector))


def compute_density_lift(
    vector: Sequence[float],
    *,
    tolerance: float = 1e-12,
) -> DensityLiftProto:
    """ψ_e = sign(v_e) · √(|v_e|/M). Helper only — not residual authority alone."""
    if not math.isfinite(float(tolerance)) or float(tolerance) < 0.0:
        raise ValueError("tolerance must be a finite non-negative float")
    vec: List[float] = []
    for i, x in enumerate(vector):
        try:
            v = float(x)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"vector[{i}] is not a float") from exc
        if not math.isfinite(v):
            raise ValueError(f"vector[{i}] is not finite")
        vec.append(v)
    mass = residual_l1_mass(vec)
    if mass <= float(tolerance):
        raise ValueError("zero mass: density lift undefined")
    state: List[float] = []
    for v in vec:
        sign = 1.0 if v >= 0.0 else -1.0
        state.append(sign * math.sqrt(abs(v) / mass))
    return DensityLiftProto(state_vector=tuple(state), total_mass=mass)


def pure_state_trace_distance(
    psi: Sequence[float],
    phi: Sequence[float],
    *,
    half_normalized: bool = True,
) -> float:
    """D = √(1 − |⟨ψ|φ⟩|²). Helper only — not residual authority alone."""
    if len(psi) != len(phi):
        raise ValueError("psi/phi length mismatch")
    re = 0.0
    for a, b in zip(psi, phi):
        fa = float(a)
        fb = float(b)
        if not (math.isfinite(fa) and math.isfinite(fb)):
            raise ValueError("psi/phi must be finite")
        re += fa * fb
    overlap = max(0.0, min(1.0, re * re))
    dist = math.sqrt(1.0 - overlap)
    return dist if half_normalized else 2.0 * dist


def _parse_finite_vec(vector: Sequence[float], *, field: str) -> Optional[List[float]]:
    out: List[float] = []
    for i, x in enumerate(vector):
        try:
            v = float(x)
        except (TypeError, ValueError):
            return None
        if not math.isfinite(v):
            return None
        out.append(v)
    return out


def compute(
    primal_residual: Sequence[float],
    dual_witness: Sequence[float],
    phi1_value: float,
    *,
    tolerance: float = 1e-12,
    half_normalized: bool = True,
) -> XiComputation:
    """Typed Ξ computation matching Rust ``XiFunctional::compute`` semantics."""
    if not math.isfinite(float(tolerance)) or float(tolerance) < 0.0:
        return XiComputation(
            kind=XiComputationKind.Invalid, validity=XiValidity.NonFiniteInput
        )
    if not math.isfinite(float(phi1_value)):
        return XiComputation(
            kind=XiComputationKind.Invalid, validity=XiValidity.NonFiniteInput
        )

    if float(phi1_value) <= float(tolerance):
        return XiComputation(kind=XiComputationKind.ExactZero)

    p_vec = _parse_finite_vec(primal_residual, field="primal_residual")
    d_vec = _parse_finite_vec(dual_witness, field="dual_witness")
    if p_vec is None or d_vec is None:
        return XiComputation(
            kind=XiComputationKind.Invalid, validity=XiValidity.NonFiniteInput
        )
    if len(p_vec) != len(d_vec):
        return XiComputation(
            kind=XiComputationKind.Invalid, validity=XiValidity.DensityLiftUndefined
        )

    try:
        primal_lift = compute_density_lift(p_vec, tolerance=tolerance)
        dual_lift = compute_density_lift(d_vec, tolerance=tolerance)
    except ValueError as exc:
        msg = str(exc).lower()
        if "finite" in msg:
            return XiComputation(
                kind=XiComputationKind.Invalid, validity=XiValidity.NonFiniteInput
            )
        return XiComputation(
            kind=XiComputationKind.Invalid, validity=XiValidity.DensityLiftUndefined
        )

    value = pure_state_trace_distance(
        primal_lift.state_vector,
        dual_lift.state_vector,
        half_normalized=half_normalized,
    )

    inner = sum(p * d for p, d in zip(p_vec, d_vec))
    saturation_verified = abs(inner - float(phi1_value)) <= float(tolerance)
    if not saturation_verified:
        return XiComputation(
            kind=XiComputationKind.Invalid, validity=XiValidity.SaturationFailed
        )

    return XiComputation(
        kind=XiComputationKind.ValidTieBreaker,
        validity=XiValidity.Valid,
        result=XiResult(
            value=float(value),
            validity=XiValidity.Valid,
            primal_density=primal_lift,
            dual_density=dual_lift,
            saturation_verified=True,
        ),
    )


def xi(
    primal_residual: Sequence[float],
    dual_witness: Sequence[float],
    phi1_value: float,
    *,
    tolerance: float = 1e-12,
    half_normalized: bool = True,
) -> float:
    """Convenience float API: ExactZero/ValidTieBreaker → float; Invalid → ValueError.

    Prefer ``compute(...)`` when validity must be preserved.
    """
    comp = compute(
        primal_residual,
        dual_witness,
        phi1_value,
        tolerance=tolerance,
        half_normalized=half_normalized,
    )
    return comp.value_or_raise()


__all__ = [
    "XiValidity",
    "DensityLiftProto",
    "XiResult",
    "XiComputationKind",
    "XiComputation",
    "residual_l1_mass",
    "compute_density_lift",
    "pure_state_trace_distance",
    "compute",
    "xi",
]
