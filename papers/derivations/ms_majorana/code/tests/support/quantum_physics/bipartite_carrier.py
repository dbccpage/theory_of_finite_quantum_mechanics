r"""
Declared bipartite state carrier: H_a \otimes H_b.

AuthorityEffect: None.
"""

from __future__ import annotations
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from typing import Dict, Tuple

import numpy as np

from omega_engine.crates.quantum_physics.primitives import (
    I2,
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    is_density_matrix,
    marginals,
    mutual_information,
    operator_norm,
    partial_trace_a,
    partial_trace_b,
    pure_state,
    purity,
    trace_norm,
)


def commutator(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return A @ B - B @ A


@dataclass(config=ConfigDict(arbitrary_types_allowed=True), frozen=True)
class BipartiteEdge:
    r"""A declared bipartite edge carrier H_a \otimes H_b.

    Carries the product-of-marginals retraction \Pi_e(\sigma) = Tr_b\sigma \otimes Tr_a\sigma.
    """

    hamiltonian: np.ndarray
    rho0: np.ndarray
    da: int = 2
    db: int = 2

    def derivatives(self) -> Tuple[np.ndarray, np.ndarray]:
        rdot = -1j * commutator(self.hamiltonian, self.rho0)
        rddot = -1j * commutator(self.hamiltonian, rdot)
        return rdot, rddot

    def marginals(self) -> Tuple[np.ndarray, np.ndarray]:
        return (
            partial_trace_b(self.rho0, self.da, self.db),
            partial_trace_a(self.rho0, self.da, self.db),
        )

    def P_e(self, z: np.ndarray) -> np.ndarray:
        rho_a, rho_b = self.marginals()
        return np.kron(partial_trace_b(z, self.da, self.db), rho_b) + np.kron(
            rho_a, partial_trace_a(z, self.da, self.db)
        )

    def Q_e(self, z: np.ndarray) -> np.ndarray:
        return z - self.P_e(z)

    def nu_e(self) -> float:
        rdot, _ = self.derivatives()
        return trace_norm(self.Q_e(rdot))

    def cross_term(self) -> np.ndarray:
        rdot, _ = self.derivatives()
        return 2 * np.kron(
            partial_trace_b(rdot, self.da, self.db),
            partial_trace_a(rdot, self.da, self.db),
        )

    def f_second_derivative(self) -> np.ndarray:
        _, rddot = self.derivatives()
        return self.Q_e(rddot) - self.cross_term()

    def a_e_as_defined(self) -> float:
        _, rddot = self.derivatives()
        return 0.5 * trace_norm(self.Q_e(rddot))

    def a_e_true(self) -> float:
        return 0.5 * trace_norm(self.f_second_derivative())

    def exact_defect(self, t: float) -> float:
        from scipy.linalg import expm

        u = expm(-1j * self.hamiltonian * t)
        rho_t = u @ self.rho0 @ u.conj().T
        ra = partial_trace_b(rho_t, self.da, self.db)
        rb = partial_trace_a(rho_t, self.da, self.db)
        return trace_norm(rho_t - np.kron(ra, rb))

    def second_order_report(self) -> Dict[str, float]:
        a_def, a_true = self.a_e_as_defined(), self.a_e_true()
        return {
            "nu_e": self.nu_e(),
            "a_e_as_defined": a_def,
            "a_e_true": a_true,
            "omitted_cross_term_norm": trace_norm(self.cross_term()),
            "discrepancy": abs(a_def - a_true),
        }

    def bar_a_e_sampled(self, t: float, n_samples: int = 20) -> float:
        from scipy.linalg import expm

        max_val = 0.0
        for s in np.linspace(0.0, max(t, 1e-12), n_samples):
            u = expm(-1j * self.hamiltonian * s)
            rho_s = u @ self.rho0 @ u.conj().T
            rdot_s = -1j * commutator(self.hamiltonian, rho_s)
            rddot_s = -1j * commutator(self.hamiltonian, rdot_s)

            rho_a = partial_trace_b(rho_s, self.da, self.db)
            rho_b = partial_trace_a(rho_s, self.da, self.db)

            p_e_rddot = np.kron(
                partial_trace_b(rddot_s, self.da, self.db), rho_b
            ) + np.kron(rho_a, partial_trace_a(rddot_s, self.da, self.db))
            q_e_rddot = rddot_s - p_e_rddot

            cross_s = 2.0 * np.kron(
                partial_trace_b(rdot_s, self.da, self.db),
                partial_trace_a(rdot_s, self.da, self.db),
            )
            val = 0.5 * trace_norm(q_e_rddot - cross_s)
            if val > max_val:
                max_val = val
        return max_val

    def bar_a_e_upper_bound(self) -> float:
        h_op = float(np.max(np.linalg.svd(self.hamiltonian, compute_uv=False)))
        return 10.0 * h_op * h_op

    def bar_a_e_interval(self, t: float, n_samples: int = 20) -> Tuple[float, float]:
        return self.bar_a_e_sampled(t, n_samples), self.bar_a_e_upper_bound()




