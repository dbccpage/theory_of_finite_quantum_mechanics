"""
Floating-point fusion-matrix and route-label diagnostics.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)

Computes selected trigonometric SU(2)_k-inspired scalar data, 2x2 F/R
matrices, and the declared commutator B1 B2 B1^-1 B2^-1, with B1=R^2
and B2=F B1 F^-1. All-zero flux flags select a 1x1 identity; other
flux values do not independently determine a geometric loop configuration.

This is not a mechanization of (3+1)D BF theory, a Wilson/'t Hooft network,
a Wang-Levin invariant, a full modular category or a general sign obstruction.
Existing public names and TerminalRoute labels identify this diagnostic API.
No validated floating-point error enclosure or physical interpretation follows.

The doubled matrix is M tensor M^dagger. Its trace identity motivates the
numerical abs(trace(M))**2 calculation; diagnostic Phi_1=0 and average_sign_gin=1
are conventions, not a physical ensemble average, exact certificate or proof
of sign-problem repair, particularly when the trace vanishes.
"""

from __future__ import annotations

import cmath
from dataclasses import dataclass, field
import math
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

code_dir = Path(__file__).resolve().parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from bqnf_sign_evaluator import TerminalRoute


@dataclass(frozen=True)
class SU2LevelKCategory:
    """Selected floating-point SU(2)_k-inspired formulas for level k >= 2."""
    k: int

    def __post_init__(self) -> None:
        if self.k < 2:
            raise ValueError(f"Level k={self.k} must be >= 2 for non-abelian BF theory.")

    @property
    def num_objects(self) -> int:
        """Spins 0, 1/2, ..., k/2 (represented as 2j in 0..k)."""
        return self.k + 1

    def quantum_dimension(self, two_j: int) -> float:
        """Computes d_j = sin((2j+1)pi / (k+2)) / sin(pi / (k+2))."""
        if not (0 <= two_j <= self.k):
            raise ValueError(f"2j={two_j} out of range [0, {self.k}]")
        num = math.sin((two_j + 1) * math.pi / (self.k + 2))
        den = math.sin(math.pi / (self.k + 2))
        return num / den

    @property
    def total_quantum_dimension(self) -> float:
        """D = sqrt(sum_j d_j^2)."""
        return math.sqrt(sum(self.quantum_dimension(two_j)**2 for two_j in range(self.k + 1)))

    def conformal_weight(self, two_j: int) -> float:
        """h_j = j(j+1)/(k+2) = (two_j/2)(two_j/2 + 1)/(k+2)."""
        j = two_j / 2.0
        return j * (j + 1.0) / (self.k + 2)

    def topological_twist(self, two_j: int) -> complex:
        """theta_j = exp(2pi i h_j)."""
        h = self.conformal_weight(two_j)
        return cmath.exp(2.0j * math.pi * h)

    def f_matrix_fundamental(self) -> np.ndarray:
        """
        Computes the 2x2 F-matrix for fundamental representations j = 1/2:
        (1/2 (x) 1/2) (x) 1/2 -> 1/2, with intermediate channels j_12 in {0, 1}
        and j_23 in {0, 1}.
        F = [[1/d_{1/2}, sqrt(d_1)/d_{1/2}], [sqrt(d_1)/d_{1/2}, -1/d_{1/2}]].
        """
        d_half = self.quantum_dimension(1)
        d_one = self.quantum_dimension(2)
        inv_d = 1.0 / d_half
        s_d = math.sqrt(d_one) / d_half
        return np.array([
            [inv_d, s_d],
            [s_d, -inv_d]
        ], dtype=complex)

    def r_matrix_fundamental(self) -> np.ndarray:
        """
        Computes the diagonal 2x2 R-matrix for swapping two j=1/2 flux lines:
        R_{1/2, 1/2}^0 and R_{1/2, 1/2}^1.
        """
        h_half = self.conformal_weight(1)
        h_zero = self.conformal_weight(0)
        h_one = self.conformal_weight(2)

        r0 = -cmath.exp(-2.0j * math.pi * h_half)
        r1 = cmath.exp(1.0j * math.pi * (h_one - 2.0 * h_half))

        return np.diag([r0, r1])


@dataclass(frozen=True)
class WangLevin3LoopAuditReceipt:
    """Measured numerical matrix diagnostics and conventional route labels."""
    model_id: str
    k_level: int
    loop_fluxes: Tuple[float, float, float]
    fusion_space_dim: int
    is_non_abelian: bool
    trace_holonomy: complex
    cochain_curvature_gamma2: float
    involution_pairing_phi1: float
    average_sign_gin: float
    is_quantum_double_projected: bool
    terminal_route: TerminalRoute
    authority: str = "None"


class WangLevin3LoopBraidingModel:
    """
    Declared finite fusion-matrix diagnostic with retained historical API names.
    No geometric loop/surface network or Wang-Levin invariant is constructed.
    """
    def __init__(
        self,
        k_level: int = 2,
        loop_fluxes: Tuple[float, float, float] = (0.5, 0.5, 0.5),
        temperature: float = 1.0,
        energy_gap_orient: float = 0.0,
    ) -> None:
        self.category = SU2LevelKCategory(k=k_level)
        self.loop_fluxes = loop_fluxes
        self.temperature = max(1e-4, temperature)
        self.energy_gap_orient = max(0.0, energy_gap_orient)

    @property
    def is_abelian(self) -> bool:
        """True if all loop fluxes are trivial spin-0."""
        return all(f == 0.0 for f in self.loop_fluxes)

    def compute_3loop_holonomy_matrix(self) -> np.ndarray:
        """
        Return the supplied 2x2 fusion-matrix commutator, or a 1x1 identity.
        B1 = R^2, B2 = F @ B1 @ F^{-1}; M = B1 @ B2 @ B1^{-1} @ B2^{-1}.
        The name is not evidence for a geometric three-loop invariant.
        """
        if self.is_abelian:
            return np.array([[1.0 + 0.0j]], dtype=complex)

        F = self.category.f_matrix_fundamental()
        R = self.category.r_matrix_fundamental()

        B1 = R @ R
        F_inv = np.linalg.inv(F)
        B2 = F @ B1 @ F_inv

        B1_inv = np.linalg.inv(B1)
        B2_inv = np.linalg.inv(B2)
        M_WL = B1 @ B2 @ B1_inv @ B2_inv
        return M_WL


    def compute_quantum_double_projection(self, M_WL: np.ndarray) -> np.ndarray:
        """
        Form a Kronecker matrix, not a categorical or physical repair:
        M_QD = M_WL (x) M_WL^dagger.
        Tr(M_QD) = |Tr(M_WL)|^2 >= 0 real and nonnegative in exact arithmetic.
        """
        return np.kron(M_WL, M_WL.conj().T)


class NonAbelianBfEngine:
    """
    Numerical trace statistics and conventional diagnostic routing only.
    """
    @classmethod
    def audit_nonabelian_3loop_braiding(
        cls,
        model: WangLevin3LoopBraidingModel,
        use_quantum_double: bool = False,
    ) -> WangLevin3LoopAuditReceipt:
        """Return numerical trace diagnostics; route labels do not certify physics."""
        M = model.compute_3loop_holonomy_matrix()
        dim_v = M.shape[0]

        if use_quantum_double:
            # tr(M tensor M*) = |tr(M)|^2. Evaluating the identity avoids
            # cancellation that can give a tiny negative Kronecker trace.
            # This is still floating-point diagnostics, not an exact proof.
            tr_val = abs(np.trace(M)) ** 2
            norm_factor = dim_v**2
            norm_tr = tr_val / norm_factor
            gamma_2 = 0.0
            phi_1 = 0.0
            avg_sign = 1.0
            route = TerminalRoute.EXACT_REPAIR
        else:
            M_eff = M
            tr_val = np.trace(M_eff)
            norm_tr = tr_val / dim_v

            gamma_2 = abs(cmath.phase(norm_tr))

            if model.is_abelian:
                phi_1 = 0.0
                avg_sign = 1.0
                route = TerminalRoute.EXACT_REPAIR
            else:
                if model.energy_gap_orient > 1e-4:
                    phi_1 = float(1.0 - math.exp(-model.energy_gap_orient / model.temperature))
                    avg_sign = float(math.exp(-model.energy_gap_orient / model.temperature) * max(0.0, norm_tr.real))
                    route = TerminalRoute.REFUSED
                else:
                    re_part = float(norm_tr.real)
                    im_part = float(norm_tr.imag)
                    phi_1 = float(max(0.0, 1.0 - re_part) + abs(im_part))
                    avg_sign = float(max(0.0, min(1.0, re_part)))
                    route = TerminalRoute.OPEN_SIGN_OBSTRUCTION

        return WangLevin3LoopAuditReceipt(
            model_id=f"SU2_k{model.category.k}_3loop_braiding",
            k_level=model.category.k,
            loop_fluxes=model.loop_fluxes,
            fusion_space_dim=dim_v,
            is_non_abelian=not model.is_abelian,
            trace_holonomy=complex(tr_val),
            cochain_curvature_gamma2=float(gamma_2),
            involution_pairing_phi1=float(phi_1),
            average_sign_gin=float(avg_sign),
            is_quantum_double_projected=use_quantum_double,
            terminal_route=route,
            authority="None",
        )
