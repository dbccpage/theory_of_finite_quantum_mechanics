"""
Interactive falsification helpers for PO-000.

Readers are meant to *break* hypotheses and observe clean failure above 1e-12.
AuthorityEffect: None. Finite floating-point replays only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

import numpy as np

from inline_code_companion import run_example_61_bell_state_leakage

TOL = 1e-12


@dataclass(frozen=True)
class FalsificationResult:
    """Outcome of one deliberate break attempt."""

    name: str
    broken_hypothesis: str
    expected_failure: bool
    residual: float
    detail: str

    @property
    def tripped(self) -> bool:
        """True when residual exceeds the publication tolerance."""
        return self.residual > TOL


def bell_closed_form(theta: float) -> float:
    """Signed-safe closed form for Example 6.1: 2|cs| + 2 c^2 s^2."""
    c, s = np.cos(theta), np.sin(theta)
    return float(2.0 * abs(c * s) + 2.0 * (c * c * s * s))


def unsigned_formula_bug(theta: float) -> float:
    """
    Deliberately wrong formula that drops absolute value on cs.

    For theta = -pi/8 this yields a *negative* pseudo-trace-norm and fails
    the positive closed form 1/sqrt(2)+1/4.
    """
    c, s = np.cos(theta), np.sin(theta)
    return float(2.0 * (c * s) + 2.0 * (c * c * s * s))


def break_unsigned_bell_formula(theta: float = -np.pi / 8) -> FalsificationResult:
    """Break: use unsigned cs while evolving at negative angle."""
    numerical, signed = run_example_61_bell_state_leakage(theta=theta)
    buggy = unsigned_formula_bug(theta)
    residual = abs(numerical - buggy)
    return FalsificationResult(
        name="unsigned_bell_formula",
        broken_hypothesis="D = 2 cs + 2 c^2 s^2 is valid for both signs of Jt",
        expected_failure=True,
        residual=float(residual),
        detail=(
            f"theta={theta:.6f}, numerical={numerical:.16f}, "
            f"signed_formula={signed:.16f}, unsigned_bug={buggy:.16f}"
        ),
    )


def edgewise_l1(edges: Sequence[float]) -> float:
    """RE3-style edgewise sum of non-negative local gauges."""
    return float(sum(abs(float(x)) for x in edges))


def global_max_aggregator(edges: Sequence[float]) -> float:
    """Global max aggregation — contractive-looking but not edge-additive."""
    values = [abs(float(x)) for x in edges]
    if not values:
        return 0.0
    return float(max(values))


def break_max_is_not_edge_additive(
    x: Sequence[float] = (1.0, 0.0),
    y: Sequence[float] = (0.0, 1.0),
) -> FalsificationResult:
    """
    Break: claim global max aggregation is edge-additive (P1 / RE3 style).

    For unit e1, e2: max(e1+e2)=1 but max(e1)+max(e2)=2.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    left = global_max_aggregator((x_arr + y_arr).tolist())
    right = global_max_aggregator(x_arr.tolist()) + global_max_aggregator(y_arr.tolist())
    residual = abs(left - right)
    return FalsificationResult(
        name="max_not_edge_additive",
        broken_hypothesis="nu = max_e |delta_e| is edge-additive",
        expected_failure=True,
        residual=float(residual),
        detail=f"max(x+y)={left}, max(x)+max(y)={right}",
    )


def short_time_lower_bound(nu_e: float, g: float, t: float) -> float:
    """Theorem 5.1 lower bound expression nu t - 24 g^2 t^2 (may be negative)."""
    return float(nu_e * t - 24.0 * (g**2) * (t**2))


def break_short_time_outside_window(
    nu_e: float = 1.0,
    g: float = 1.0,
    t: float = 1.0,
) -> FalsificationResult:
    """
    Break: treat the short-time lower bound as a global-in-t positivity claim.

    At large t the expression nu t - 24 g^2 t^2 becomes negative, so it cannot
    certify a positive defect density outside the near-zero window.
    """
    bound = short_time_lower_bound(nu_e, g, t)
    # Residual = how far the "bound is always >= 0" claim fails.
    residual = max(0.0, -bound)
    return FalsificationResult(
        name="short_time_outside_window",
        broken_hypothesis="nu t - 24 g^2 t^2 is a positive lower bound for all t >= 0",
        expected_failure=True,
        residual=float(residual),
        detail=f"nu={nu_e}, g={g}, t={t}, bound={bound:.16f}",
    )


def break_raw_equals_watched_without_observer(
    raw_I: float = 6.0,
    watched_J: Sequence[float] = (0.0, 0.0, 0.0),
) -> FalsificationResult:
    """
    Break: identify raw edge tally I with watched observer loss J without declaring
    observation maps (Section 7.4.5 local-green / global-red separation).
    """
    j_sum = float(sum(abs(float(v)) for v in watched_J))
    residual = abs(float(raw_I) - j_sum)
    return FalsificationResult(
        name="raw_vs_watched_without_observer",
        broken_hypothesis="I(s) equals sum_alpha J^alpha(s) with no declared watchers",
        expected_failure=True,
        residual=float(residual),
        detail=f"I={raw_I}, sum|J|={j_sum}",
    )


def run_all_breaks() -> List[FalsificationResult]:
    """Run the standard PO-000 falsification panel."""
    return [
        break_unsigned_bell_formula(),
        break_max_is_not_edge_additive(),
        break_short_time_outside_window(),
        break_raw_equals_watched_without_observer(),
    ]


def assert_all_breaks_trip(results: Sequence[FalsificationResult] | None = None) -> None:
    """Hard gate: every expected failure must exceed TOL."""
    panel = list(results) if results is not None else run_all_breaks()
    for item in panel:
        if item.expected_failure and not item.tripped:
            raise RuntimeError(
                f"Falsification '{item.name}' did not trip: residual={item.residual} "
                f"(tol={TOL}); {item.detail}"
            )


def control_signed_bell_both_signs() -> Tuple[float, float]:
    """Control: signed formula matches numerical replay for both signs."""
    pos_n, pos_f = run_example_61_bell_state_leakage(theta=np.pi / 8)
    neg_n, neg_f = run_example_61_bell_state_leakage(theta=-np.pi / 8)
    expected = 1.0 / np.sqrt(2.0) + 0.25
    if abs(pos_n - expected) > TOL:
        raise ArithmeticError(f"pos_n discrepancy: {pos_n} vs {expected}")
    if abs(pos_f - expected) > TOL:
        raise ArithmeticError(f"pos_f discrepancy: {pos_f} vs {expected}")
    if abs(neg_n - expected) > TOL:
        raise ArithmeticError(f"neg_n discrepancy: {neg_n} vs {expected}")
    if abs(neg_f - expected) > TOL:
        raise ArithmeticError(f"neg_f discrepancy: {neg_f} vs {expected}")
    return float(pos_n), float(neg_n)
