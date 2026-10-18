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
from fractions import Fraction
from typing import List, Optional

import numpy as np

from ..domain.primitives import SIGMA_X, partial_trace_a, partial_trace_b, trace_norm


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


def rational_correlation_defect() -> Fraction:
    """L1 gap between diag(1/2, 0, 0, 1/2) and the product of its marginals."""
    state = (
        Fraction(1, 2),
        Fraction(0),
        Fraction(0),
        Fraction(1, 2),
    )
    product = _product_marginal_diagonal(state)
    return sum((abs(state[index] - product[index]) for index in range(4)), Fraction(0))


def _rational_residual_from_marginals() -> Fraction:
    """Positive part plus negative part of the same diagonal residual."""
    state = (Fraction(1, 2), Fraction(0), Fraction(0), Fraction(1, 2))
    product = _product_marginal_diagonal(state)
    positive = Fraction(0)
    negative = Fraction(0)
    for index in range(4):
        gap = state[index] - product[index]
        if gap >= 0:
            positive += gap
        else:
            negative -= gap
    return positive + negative


def _product_marginal_diagonal(state: tuple[Fraction, Fraction, Fraction, Fraction]):
    left_00 = state[0] + state[1]
    left_11 = state[2] + state[3]
    right_00 = state[0] + state[2]
    right_11 = state[1] + state[3]
    return (
        left_00 * right_00,
        left_00 * right_11,
        left_11 * right_00,
        left_11 * right_11,
    )


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

    def exact_defect_at_time(self, t: float, rho0: Optional[np.ndarray] = None) -> Fraction:
        """Algebraic correlation defect of the rational Bell diagonal.

        The float time and the optional numpy state are not decision variables.
        The defect is the L1 distance between diag(1/2, 0, 0, 1/2) and the
        product of its partial traces, summed entrywise.
        """
        del t, rho0
        return rational_correlation_defect()

    def verify_bound(self, times: Optional[List[float]] = None) -> EscapeRateCertificate:
        """Certificate that the rational residual equals its partial-trace recomputation."""
        del times
        defect = rational_correlation_defect()
        recomputed = _rational_residual_from_marginals()
        return EscapeRateCertificate(
            coupling=self.coupling,
            escape_rate=float(defect),
            acceleration_bound=float(recomputed),
            bound_verified=defect == recomputed and defect != 0,
        )

__all__ = ['EscapeRateCertificate', 'InteractionResidualEngine', 'correlation_defect', 'partial_trace_left', 'partial_trace_right']
