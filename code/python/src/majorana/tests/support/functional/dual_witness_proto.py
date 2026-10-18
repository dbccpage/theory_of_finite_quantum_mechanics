"""PROTO dual-witness surfaces (Wave G) — two *different* morphisms.

AuthorityEffect: None.

1. **Display builder** (``display_dual_witness``) — STRUCTURAL_MIRROR of the
   Rust ``DualWitness`` *field shape* only. Accepts arbitrary finite ``phi`` and
   **caller-supplied** ``is_circulation`` / ``is_bounded`` (including states
   impossible via Rust ``DualWitness::from_verified``). Optional f64 residual
   pairing for ``dual_value`` is a convenience, **not** transport of an exact
   rational certified objective. This is **not** FORMULA_MIRROR of
   ``from_verified`` (verified-domain boundary).

2. **Float post-solve dual checks** (``float_dual_checks``) — PROTO_ONLY
   diagnostic. Recomputes B^T φ ≈ 0, ‖φ‖_∞ ≤ 1, ⟨φ,h⟩ ≈ Φ. This is **not**
   a formula mirror of ``dual_witness.rs`` and **not** exact-certificate
   authority. Evidence ceiling is diagnostic consistency only
   (``float_checks_pass``); never use that flag for Φ₁ certificate admission.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple


def dual_pairing(
    dual_functional: Sequence[float],
    primal_vector: Sequence[float],
) -> float:
    """⟨φ, x⟩ = sum_i φ_i x_i. Finite inputs required."""
    if len(dual_functional) != len(primal_vector):
        raise ValueError("dual_functional and primal_vector length mismatch")
    acc = 0.0
    for i, (a, b) in enumerate(zip(dual_functional, primal_vector)):
        fa = float(a)
        fb = float(b)
        if not (math.isfinite(fa) and math.isfinite(fb)):
            raise ValueError(f"non-finite entry at index {i}")
        acc += fa * fb
    return float(acc)


def linf_norm(vector: Sequence[float]) -> float:
    """‖v‖_∞. Finite inputs required."""
    if not vector:
        raise ValueError("vector must be non-empty")
    m = 0.0
    for i, x in enumerate(vector):
        v = float(x)
        if not math.isfinite(v):
            raise ValueError(f"non-finite entry at index {i}")
        m = max(m, abs(v))
    return float(m)


@dataclass(frozen=True)
class DisplayDualWitness:
    """Display/diagnostic dual-witness view (float). Not a certificate.

    Flags are inherited from the caller (mirrors Rust inheritance from
    VerifiedExactPhi1), not recomputed here.
    """

    phi: Tuple[float, ...]
    dual_value: float
    is_circulation: bool
    is_bounded: bool
    evidence_ceiling: str = "display_only"


def display_dual_witness(
    phi: Sequence[float],
    *,
    residual: Optional[Sequence[float]] = None,
    dual_value: Optional[float] = None,
    is_circulation: bool = False,
    is_bounded: bool = False,
) -> DisplayDualWitness:
    """Structural display builder (not DualWitness::from_verified formula mirror).

    If residual is provided and dual_value is None, dual_value = f64 ⟨phi, residual⟩
    (not exact rational transport). Flags are **caller-supplied** and may be false;
    Rust from_verified always forces them true from VerifiedExactPhi1.
    """
    phi_t: List[float] = []
    for i, x in enumerate(phi):
        v = float(x)
        if not math.isfinite(v):
            raise ValueError(f"phi[{i}] is not finite")
        phi_t.append(v)
    if dual_value is None:
        if residual is None:
            raise ValueError("dual_value or residual is required")
        dv = dual_pairing(phi_t, residual)
    else:
        dv = float(dual_value)
        if not math.isfinite(dv):
            raise ValueError("dual_value must be finite")
    return DisplayDualWitness(
        phi=tuple(phi_t),
        dual_value=dv,
        is_circulation=bool(is_circulation),
        is_bounded=bool(is_bounded),
        evidence_ceiling="display_only",
    )


def float_dual_checks(
    B: Sequence[Sequence[float]],
    phi_star: Sequence[float],
    h: Sequence[float],
    Phi: float,
    *,
    tol: float = 1e-8,
) -> Dict[str, object]:
    """PROTO_ONLY float post-solve dual diagnostic (not dual_witness.rs).

    Checks B^T φ ≈ 0, ‖φ‖_∞ ≤ 1, ⟨φ, h⟩ ≈ Phi. Diagnostic only.
    ``float_checks_pass`` is **not** an exact Φ₁ certificate and must not
    admit authority. Evidence ceiling is explicit on the payload.
    """
    if not math.isfinite(float(tol)) or float(tol) < 0.0:
        raise ValueError("tol must be finite non-negative")
    if not math.isfinite(float(Phi)) or float(Phi) < 0.0:
        raise ValueError("Phi must be finite non-negative")
    rows = len(B)
    if rows == 0:
        raise ValueError("B must be non-empty")
    cols = len(B[0])
    phi = [float(x) for x in phi_star]
    hh = [float(x) for x in h]
    if any(not math.isfinite(x) for x in phi + hh):
        raise ValueError("phi_star and h must be finite")
    if len(phi) != rows or len(hh) != rows:
        raise ValueError("phi_star/h length must match B rows (edges)")
    for r, row in enumerate(B):
        if len(row) != cols:
            raise ValueError("B must be rectangular")
        for c, v in enumerate(row):
            if not math.isfinite(float(v)):
                raise ValueError(f"B[{r},{c}] is not finite")

    div: List[float] = []
    for c in range(cols):
        s = 0.0
        for r in range(rows):
            s += float(B[r][c]) * phi[r]
        div.append(s)
    div_norm = max((abs(x) for x in div), default=0.0)
    div_ok = div_norm <= float(tol)
    linf = linf_norm(phi)
    linf_ok = linf <= 1.0 + float(tol)
    pairing = dual_pairing(phi, hh)
    tight_err = abs(pairing - float(Phi))
    tight = tight_err <= float(tol)
    float_checks_pass = bool(div_ok and linf_ok and tight)
    return {
        "divergence_free": bool(div_ok),
        "divergence_norm": float(div_norm),
        "linf_ok": bool(linf_ok),
        "linf_value": float(linf),
        "duality_tight": bool(tight),
        "tightness_error": float(tight_err),
        "dual_pairing": float(pairing),
        "tol": float(tol),
        "float_checks_pass": float_checks_pass,
        "evidence_ceiling": "float_diagnostic",
        "authority_effect": "None",
    }


__all__ = [
    "dual_pairing",
    "linf_norm",
    "DisplayDualWitness",
    "display_dual_witness",
    "float_dual_checks",
]
