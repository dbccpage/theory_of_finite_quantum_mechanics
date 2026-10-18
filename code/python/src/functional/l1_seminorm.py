"""Exact weighted L1 quotient seminorm evaluator.
Under the Zero-Float Law, all boundary entries, weights, and certificates
are exact fractions.Fraction instances.
"""

from __future__ import annotations
from fractions import Fraction
from dataclasses import dataclass
from typing import List, Sequence, Tuple, Optional


@dataclass(frozen=True)
class ExactPhi1Certificate:
    """Primal-dual certificate for quotient L1 seminorm."""
    omega: List[Fraction]
    d0: List[List[Fraction]]
    weights: List[Fraction]
    alpha: List[Fraction]
    primal_residual: List[Fraction]
    dual_witness: List[Fraction]
    reported_value: Fraction


@dataclass(frozen=True)
class VerifiedExactPhi1:
    certificate: ExactPhi1Certificate

    @property
    def value(self) -> Fraction:
        return self.certificate.reported_value

    @property
    def d0(self) -> List[List[Fraction]]:
        return self.certificate.d0

    @property
    def weights(self) -> List[Fraction]:
        return self.certificate.weights


class L1Seminorm:
    """Exact weighted L1 quotient seminorm on Q^n / im(B)."""

    def __init__(self, boundary: Sequence[Sequence[Fraction | int | Tuple[int, int]]], weights: Sequence[Fraction | int | Tuple[int, int]]) -> None:
        p_weights: List[Fraction] = []
        for i, w in enumerate(weights):
            fw = Fraction(w[0], w[1]) if isinstance(w, tuple) else Fraction(w)
            if fw <= 0:
                raise ValueError(f"Weight at index {i} must be strictly positive, got {fw}")
            p_weights.append(fw)

        n_rows = len(p_weights)
        p_boundary: List[List[Fraction]] = []
        n_cols = len(boundary[0]) if len(boundary) > 0 and len(boundary[0]) > 0 else 0

        for r_idx, row in enumerate(boundary):
            if len(row) != n_cols:
                raise ValueError("Boundary matrix must be rectangular")
            p_row = [Fraction(x[0], x[1]) if isinstance(x, tuple) else Fraction(x) for x in row]
            p_boundary.append(p_row)

        if len(p_boundary) != n_rows and len(p_boundary) > 0:
            raise ValueError(f"Boundary rows {len(p_boundary)} must match weights length {n_rows}")

        self._boundary = p_boundary
        self._weights = p_weights

    @property
    def boundary(self) -> List[List[Fraction]]:
        return [list(r) for r in self._boundary]

    @property
    def weights(self) -> List[Fraction]:
        return list(self._weights)

    def verify_certificate(self, cert: ExactPhi1Certificate) -> VerifiedExactPhi1:
        n = len(self._weights)
        m = len(self._boundary[0]) if self._boundary and self._boundary[0] else 0

        if len(cert.omega) != n:
            raise ValueError(f"Omega length {len(cert.omega)} != {n}")
        if len(cert.weights) != n or cert.weights != self._weights:
            raise ValueError("Weight binding mismatch")
        if cert.d0 != self._boundary:
            raise ValueError("Boundary binding mismatch")
        if len(cert.alpha) != m:
            raise ValueError(f"Alpha length {len(cert.alpha)} != {m}")
        if len(cert.primal_residual) != n:
            raise ValueError(f"Primal residual length {len(cert.primal_residual)} != {n}")
        if len(cert.dual_witness) != n:
            raise ValueError(f"Dual witness length {len(cert.dual_witness)} != {n}")

        # 1. Primal feasibility: r = omega - B * alpha
        for i in range(n):
            b_alpha_i = sum(self._boundary[i][j] * cert.alpha[j] for j in range(m)) if m > 0 else Fraction(0)
            expected_r_i = cert.omega[i] - b_alpha_i
            if cert.primal_residual[i] != expected_r_i:
                raise ValueError(f"Primal residual mismatch at coordinate {i}")

        # 2. Dual feasibility: B^T * z = 0
        for j in range(m):
            b_t_z_j = sum(self._boundary[i][j] * cert.dual_witness[i] for i in range(n))
            if b_t_z_j != Fraction(0):
                raise ValueError(f"Dual witness not orthogonal to column {j} of B: sum = {b_t_z_j}")

        # 3. Dual box constraints: |z_i| <= w_i
        for i in range(n):
            if abs(cert.dual_witness[i]) > self._weights[i]:
                raise ValueError(f"Dual witness bound violated at {i}: |{cert.dual_witness[i]}| > {self._weights[i]}")

        # 4. Primal cost: sum_i w_i * |r_i|
        primal_cost = sum(self._weights[i] * abs(cert.primal_residual[i]) for i in range(n))

        # 5. Dual objective: z^T * omega = z^T * r
        dual_val = sum(cert.dual_witness[i] * cert.omega[i] for i in range(n))

        # 6. Duality gap closure
        if primal_cost != dual_val:
            raise ValueError(f"Duality gap not closed: primal {primal_cost} != dual {dual_val}")

        if cert.reported_value != primal_cost:
            raise ValueError(f"Reported value {cert.reported_value} != certified {primal_cost}")

        return VerifiedExactPhi1(cert)
