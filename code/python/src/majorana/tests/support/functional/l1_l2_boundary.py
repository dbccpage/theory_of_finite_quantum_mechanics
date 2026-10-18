r"""
The :math:`\ell^1 / \ell^2` boundary: norm comparison, quotient comparison, and the
declared loss.

AuthorityEffect: None.

Canonical Implementation: omega_engine.crates.functional.l1_l2_boundary
"""

from __future__ import annotations
from typing import Any, Dict, Optional, Sequence

import numpy as np

from omega_engine.crates.functional.l1_norm import l1_l2_comparison, l1_norm, l2_norm
from omega_engine.crates.functional.phi import phi1


def phi2(graph, cochain: Sequence[float] | np.ndarray) -> Dict[str, Any]:
    r""":math:`\Phi_2([\omega]) = \min_\alpha \|\omega - d_0\alpha\|_2`, in closed form."""
    omega = np.asarray(cochain, dtype=float)
    d0 = graph.d0_matrix()
    alpha, *_ = np.linalg.lstsq(d0, omega, rcond=None)
    residual = omega - d0 @ alpha
    return {
        "phi2": l2_norm(residual),
        "alpha": alpha,
        "residual": residual,
        "l1_cost_of_l2_representative": l1_norm(residual),
        "authority_effect": "None",
    }


def quotient_comparison(graph, cochain: Sequence[float] | np.ndarray) -> Dict[str, Any]:
    r"""Evaluate FOC_004 Proposition E.3 on a concrete carrier and cochain."""
    omega = np.asarray(cochain, dtype=float)
    m = graph.n_edges
    p1 = phi1(graph.vertices, graph.edges, omega)
    p2_report = phi2(graph, omega)
    p2 = p2_report["phi2"]

    return {
        "n_edges": m,
        "phi1": p1,
        "phi2": p2,
        "lower_bound_holds": bool(p2 <= p1 + 1e-7),
        "upper_bound_holds": bool(p1 <= np.sqrt(m) * p2 + 1e-7),
        "sqrt_m": float(np.sqrt(m)),
        "ratio_phi1_over_phi2": float(p1 / p2) if p2 > 1e-12 else float("nan"),
        "source": "FOC_004 Prop E.3",
        "authority_effect": "None",
    }


def hodge_inflation(graph, cochain: Sequence[float] | np.ndarray) -> Dict[str, Any]:
    r"""FOC_004 §1.1 item 4 / Remark E.3a: the :math:`\ell^1` cost of :math:`\ell^2` bookkeeping."""
    omega = np.asarray(cochain, dtype=float)
    d0 = graph.d0_matrix()
    f, *_ = np.linalg.lstsq(d0, omega, rcond=None)
    exact = d0 @ f
    harmonic = omega - exact

    raw = l1_norm(omega)
    split_cost = l1_norm(exact) + l1_norm(harmonic)

    return {
        "l1_of_omega": raw,
        "l1_of_exact_part": l1_norm(exact),
        "l1_of_harmonic_part": l1_norm(harmonic),
        "l1_of_split_components": split_cost,
        "inflation_ratio": float(split_cost / raw) if raw > 1e-12 else float("nan"),
        "l2_orthogonality_verified": bool(
            abs(float(np.dot(exact, harmonic))) < 1e-9 * max(1.0, raw)
        ),
        "split_costs_more_than_the_whole": bool(split_cost > raw + 1e-9),
        "warning": (
            "this is Remark E.3a and is NOT bounded by sqrt(d); the sqrt(d) comparison "
            "is between optimal VALUES (Prop E.3), not the l1 cost of l2 bookkeeping"
        ),
        "authority_effect": "None",
    }


def representative_inflation(graph, cochain: Sequence[float] | np.ndarray) -> Dict[str, Any]:
    r"""How much :math:`\ell^1` mass you pay for letting :math:`\ell^2` pick the representative."""
    omega = np.asarray(cochain, dtype=float)
    p1 = phi1(graph.vertices, graph.edges, omega)
    rep = phi2(graph, omega)
    l1_of_l2_rep = rep["l1_cost_of_l2_representative"]

    return {
        "phi1_optimal": p1,
        "l1_cost_of_l2_representative": l1_of_l2_rep,
        "inflation_ratio": float(l1_of_l2_rep / p1) if p1 > 1e-12 else float("nan"),
        "l2_representative_is_not_l1_optimal": bool(l1_of_l2_rep > p1 + 1e-7),
        "authority_effect": "None",
    }


def cycle_inflation_prediction(n: int) -> float:
    r"""The analytic cycle-graph inflation :math:`3 - 2/n` quoted by FOC_004 §1.1 item 4."""
    if n < 3:
        raise ValueError("cycle_inflation_prediction: a cycle needs at least 3 vertices")
    return 3.0 - 2.0 / float(n)


def forgetful_loss_ledger(w: Sequence[float] | np.ndarray) -> Dict[str, Any]:
    r"""Price :math:`\Delta = \|w\|_1 - \|w\|_2` and carry both framings of what it means."""
    v = np.asarray(w, dtype=float)
    comp = l1_l2_comparison(v)

    return {
        "dim": comp["dim"],
        "norm_l1": comp["norm_l1"],
        "norm_l2": comp["norm_l2"],
        "delta_forgetful": comp["delta"],
        "delta_max_permitted": comp["delta_max_permitted"],
        "delta_nonnegative": bool(comp["delta"] >= -1e-12),
        "sharpness_case": comp["sharpness_case"],
        "loss_ledger": [
            {
                "discarded": "the sign/support pattern that l1 separates and l2 averages",
                "priced_as": comp["delta"],
                "recovery_requirement": "the l1 representative itself; delta alone is not invertible",
                "disposition": "PROJECTION_LOSS" if comp["delta"] > 1e-12 else "PRESERVED_VISIBLE",
            }
        ],
        "framing_dispute": {
            "operator": "forgetful functor F: L1 -> L2; delta is discarded topological debt",
            "foc_004_a4": (
                "finite-dimensional l2 completion adds no vectors, so this is a change of "
                "gauge on one underlying set, not a forgetful map"
            ),
            "status": "OPEN — both framings recorded, neither adopted here",
        },
        "authority_effect": "None",
    }


def delta_is_gauge_dependent(graph, cochain: Sequence[float] | np.ndarray) -> Dict[str, Any]:
    r"""Show that :math:`\Delta` depends on the representative, while :math:`\Phi_1,\Phi_2` do not."""
    omega = np.asarray(cochain, dtype=float)
    d0 = graph.d0_matrix()
    rng_alpha = np.linspace(0.3, 1.1, graph.n_vertices)
    omega_shifted = omega + d0 @ rng_alpha

    d_before = forgetful_loss_ledger(omega)["delta_forgetful"]
    d_after = forgetful_loss_ledger(omega_shifted)["delta_forgetful"]

    p1_before = phi1(graph.vertices, graph.edges, omega)
    p1_after = phi1(graph.vertices, graph.edges, omega_shifted)
    p2_before = phi2(graph, omega)["phi2"]
    p2_after = phi2(graph, omega_shifted)["phi2"]

    return {
        "delta_before": d_before,
        "delta_after": d_after,
        "delta_moved": bool(not np.isclose(d_before, d_after, atol=1e-9)),
        "phi1_invariant": bool(np.isclose(p1_before, p1_after, atol=1e-6)),
        "phi2_invariant": bool(np.isclose(p2_before, p2_after, atol=1e-6)),
        "verdict": (
            "delta is representative-dependent; Phi_1 and Phi_2 are class invariants"
        ),
        "authority_effect": "None",
    }


__all__ = [
    "phi2",
    "quotient_comparison",
    "hodge_inflation",
    "representative_inflation",
    "cycle_inflation_prediction",
    "forgetful_loss_ledger",
    "delta_is_gauge_dependent",
]



