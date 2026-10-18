"""Quantum short-time correlation residual module.

Computes bipartite partial traces, trace-norm correlation defect,
and short-time escape rate lower bounds for 2-qubit interactions.

AuthorityEffect: None.

contract_id: urn:omega:math:partial_trace:v1.0.0
contract_id: urn:omega:math:density_matrix:v1.0.0
contract_id: urn:omega:math:norms:v1.0.0
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np
from scipy.linalg import expm

from omega_engine_projects.ms_majorana.code.tests.support.finite_qm.domain.primitives import I2, SIGMA_X, trace_norm, partial_trace_a, partial_trace_b


def partial_trace_left(rho: np.ndarray) -> np.ndarray:
    """Trace out system A (left qubit) from 4x4 density matrix rho_AB.

    contract_id: urn:omega:math:partial_trace:v1.0.0
    """
    return partial_trace_a(rho, 2, 2)


def partial_trace_right(rho: np.ndarray) -> np.ndarray:
    """Trace out system B (right qubit) from 4x4 density matrix rho_AB.

    contract_id: urn:omega:math:partial_trace:v1.0.0
    """
    return partial_trace_b(rho, 2, 2)


def correlation_defect(rho: np.ndarray) -> float:
    """Trace norm distance between state rho and its product marginals rho_A x rho_B.

    contract_id: urn:omega:math:density_matrix:v1.0.0
    """
    product = np.kron(partial_trace_right(rho), partial_trace_left(rho))
    return trace_norm(rho - product)


@dataclass(frozen=True, slots=True)
class EscapeRateCertificate:
    """Certificate for short-time correlation escape rate bound.

    contract_id: urn:omega:math:density_matrix:v1.0.0
    """
    coupling: float
    escape_rate: float
    acceleration_bound: float
    bound_verified: bool


class InteractionResidualEngine:
    """Computes short-time correlation growth and certifies quadratic lower bounds.

    contract_id: urn:omega:math:density_matrix:v1.0.0
    """

    def __init__(self, coupling: float = 1.0):
        if not np.isfinite(coupling):
            raise ValueError("coupling must be finite")
        self.coupling = coupling
        self.H = coupling * np.kron(SIGMA_X, SIGMA_X)

    def initial_product_state(self) -> np.ndarray:
        """Default initial product state |00><00|."""
        psi = np.array([1, 0, 0, 0], dtype=complex)
        return np.outer(psi, psi.conj())

    def escape_rate(self, rho0: Optional[np.ndarray] = None) -> float:
        """Initial derivative nu = || d/dt (rho - rho_A x rho_B) ||_1 at t=0."""
        if rho0 is None:
            rho0 = self.initial_product_state()
        d_rho = -1j * (self.H @ rho0 - rho0 @ self.H)
        rho_a = partial_trace_right(rho0)
        rho_b = partial_trace_left(rho0)
        d_rho_a = partial_trace_right(d_rho)
        d_rho_b = partial_trace_left(d_rho)
        d_product = np.kron(d_rho_a, rho_b) + np.kron(rho_a, d_rho_b)
        return float(trace_norm(d_rho - d_product))

    def acceleration_bound(self) -> float:
        """Upper bound 'a' on second derivative magnitude."""
        return 2.0 * (self.coupling ** 2)

    def certified_lower_bound(self, t: float, rho0: Optional[np.ndarray] = None) -> float:
        """Short-time certified correlation defect lower bound max(0, nu*t - a*t^2)."""
        nu = self.escape_rate(rho0)
        a = self.acceleration_bound()
        return max(0.0, nu * t - a * (t ** 2))

    def exact_defect_at_time(self, t: float, rho0: Optional[np.ndarray] = None) -> float:
        """Evolves initial state under H and computes exact correlation defect."""
        if rho0 is None:
            rho0 = self.initial_product_state()
        u_t = expm(-1j * self.H * t)
        rho_t = u_t @ rho0 @ u_t.conj().T
        return correlation_defect(rho_t)

    def verify_bound(self, times: Optional[List[float]] = None) -> EscapeRateCertificate:
        """Verifies that certified lower bounds hold across target evaluation times.

        Returns an EscapeRateCertificate rather than a bare bool.
        """
        if times is None:
            times = list(np.linspace(0.0, 0.05, 6))
        all_ok = True
        for t in times:
            exact = self.exact_defect_at_time(t)
            lb = self.certified_lower_bound(t)
            if exact < lb - 1e-10:
                all_ok = False
        return EscapeRateCertificate(
            coupling=self.coupling,
            escape_rate=self.escape_rate(),
            acceleration_bound=self.acceleration_bound(),
            bound_verified=all_ok,
        )

__all__ = ['EscapeRateCertificate', 'InteractionResidualEngine', 'correlation_defect', 'partial_trace_left', 'partial_trace_right']
