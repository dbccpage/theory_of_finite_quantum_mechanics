r"""
Product-manifold retraction: normal velocity, the second-order coefficient, and the
short-time defect bound.

AuthorityEffect: None.

Canonical Implementation: omega_engine.crates.quantum_physics.bipartite_retraction
"""

from __future__ import annotations
from typing import Any, Dict

import numpy as np

from omega_engine.crates.quantum_physics.bipartite_carrier import BipartiteEdge
from omega_engine.crates.quantum_physics.primitives import (
    I2,
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    mutual_information,
    partial_trace_a,
    partial_trace_b,
    trace_norm,
)


def d1_witness() -> BipartiteEdge:
    r"""The interacting edge that pins defect D1 in the skeleton's table."""
    h = np.kron(SIGMA_X, SIGMA_X) + 0.9 * np.kron(SIGMA_X, I2) + 0.8 * np.kron(I2, SIGMA_Y)
    psi = np.zeros(4, dtype=complex)
    psi[0] = 1.0
    return BipartiteEdge(hamiltonian=h, rho0=np.outer(psi, psi.conj()))


def product_witness() -> BipartiteEdge:
    r"""A non-interacting edge: the product manifold is invariant, so :math:`\nu_e = 0`."""
    h = 0.7 * np.kron(SIGMA_Z, I2) + 0.4 * np.kron(I2, SIGMA_X)
    psi = np.zeros(4, dtype=complex)
    psi[0] = 1.0
    return BipartiteEdge(hamiltonian=h, rho0=np.outer(psi, psi.conj()))


def short_time_defect_report(edge: BipartiteEdge, t: float = 0.1) -> Dict[str, Any]:
    r"""Evaluate the short-time bound against the exact defect, and price the Pinsker floor."""
    nu = edge.nu_e()
    a_true = edge.a_e_true()
    bar_a_sampled, bar_a_bound = edge.bar_a_e_interval(t)
    exact = edge.exact_defect(t)

    bound_true = nu * t - a_true * t * t
    bound_sampled = nu * t - bar_a_sampled * t * t
    bound_certified = nu * t - bar_a_bound * t * t
    floor = max(0.0, bound_certified)

    return {
        "t": t,
        "nu_e": nu,
        "a_e_as_defined": edge.a_e_as_defined(),
        "a_e_true": a_true,
        "bar_a_e_sampled": bar_a_sampled,
        "bar_a_e_upper_bound": bar_a_bound,
        "bound_true": bound_true,
        "bound_sampled": bound_sampled,
        "bound_certified": bound_certified,
        "exact_defect": exact,
        "bound_true_holds": bool(bound_true <= exact + 1e-9),
        "bound_sampled_holds": bool(bound_sampled <= exact + 1e-9),
        "bound_certified_holds": bool(bound_certified <= exact + 1e-9),
        "pinsker_qmi_floor": (1.0 / (2.0 * np.log(2.0))) * floor**2,
        "authority_effect": "None",
    }


def projection_loss_ledger(edge: BipartiteEdge, t: float = 0.1) -> Dict[str, Any]:
    r"""What the product retraction discards, priced in the trace norm."""
    from scipy.linalg import expm

    u = expm(-1j * edge.hamiltonian * t)
    rho_t = u @ edge.rho0 @ u.conj().T
    ra, rb = edge.marginals()

    ra_t = partial_trace_b(rho_t, edge.da, edge.db)
    rb_t = partial_trace_a(rho_t, edge.da, edge.db)
    discarded = rho_t - np.kron(ra_t, rb_t)

    return {
        "t": t,
        "discarded_trace_norm": trace_norm(discarded),
        "mutual_information_bits": mutual_information(rho_t, edge.da, edge.db),
        "recovery_requirement": "joint state; marginals alone do not determine rho_ab",
        "disposition": (
            "PROJECTION_LOSS" if trace_norm(discarded) > 1e-9 else "PRESERVED_VISIBLE"
        ),
        "authority_effect": "None",
    }


def _qubit_projector(n: np.ndarray) -> np.ndarray:
    n = np.asarray(n, dtype=float)
    return 0.5 * (np.eye(2, dtype=complex) + n[0] * SIGMA_X + n[1] * SIGMA_Y + n[2] * SIGMA_Z)


def non_born_frame_function(n: np.ndarray) -> float:
    n = np.asarray(n, dtype=float)
    return float((1.0 + n[2] ** 3) / 2.0)


def gleason_d2_falsifier_check(n_samples: int = 64) -> Dict[str, Any]:
    r"""Gleason / Born boundary test at :math:`d = 2`."""
    rng_angles = np.linspace(0.0, np.pi, n_samples)
    worst_frame_error = 0.0
    max_born_deviation = 0.0

    for theta in rng_angles:
        for phi in np.linspace(0.0, 2.0 * np.pi, 4, endpoint=False):
            n = np.array(
                [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)]
            )
            s = non_born_frame_function(n) + non_born_frame_function(-n)
            worst_frame_error = max(worst_frame_error, abs(s - 1.0))
            affine_best = 0.5 * (1.0 + n[2])
            max_born_deviation = max(
                max_born_deviation, abs(non_born_frame_function(n) - affine_best)
            )

    return {
        "dimension": 2,
        "frame_condition_max_error": worst_frame_error,
        "is_a_frame_function": bool(worst_frame_error < 1e-12),
        "max_deviation_from_affine_born_form": max_born_deviation,
        "is_non_born": bool(max_born_deviation > 1e-6),
        "gleason_applies_at_d2": False,
        "why": (
            "at d=2 every orthonormal basis is an antipodal pair, so the frame condition "
            "links no two distinct bases; Gleason's argument needs d >= 3"
        ),
        "status": "GLEASON_UNIQUENESS_FALSIFIED_AT_D2",
        "authority_effect": "None",
    }


__all__ = [
    "d1_witness",
    "product_witness",
    "short_time_defect_report",
    "projection_loss_ledger",
    "non_born_frame_function",
    "gleason_d2_falsifier_check",
]



