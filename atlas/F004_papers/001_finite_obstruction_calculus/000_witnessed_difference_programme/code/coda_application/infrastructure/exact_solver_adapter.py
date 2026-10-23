# -*- coding: utf-8 -*-
"""
Exact solver adapter for CODA infrastructure.
Provides exact rational L1 quotient calculations and dual witnesses.

Delegates to the single domain solver (``coda_application.domain.l1_quotient``): Layer 1, the
``solve_exact_l1_repair`` use case and this adapter return the same certified value.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Optional, Tuple

from sympy import Matrix, Rational

from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator
from coda_application.domain.intake import exact, matrix_rows
from coda_application.domain.l1_quotient import solve_l1_quotient
from coda_application.domain.value_objects import DualWitness, ExactRational


class ExactSolverAdapter:
    """Exact rational solver implementing the CODA L1 quotient distance and dual witnesses."""

    @staticmethod
    def compute_quotient_distance(
        boundary_matrix: Matrix,
        cochain: Matrix,
    ) -> Tuple[ExactRational, Optional[DualWitness], Matrix]:
        """
        Solves: Phi_1([cochain]) = min_f ||cochain - boundary_matrix * f||_1.
        Returns: (quotient_distance, dual_witness or None when the distance is 0, residual).
        """
        rows, (m, k) = matrix_rows(boundary_matrix, "boundary_matrix")
        if cochain.cols != 1 or cochain.rows != m:
            raise ValueError(f"cochain shape {cochain.shape} does not match the boundary's {m} rows")
        cert = solve_l1_quotient(rows, k, [exact(cochain[i, 0], f"cochain[{i}]") for i in range(m)], evaluator=NativeFunctionalEvaluator())
        distance = ExactRational(cert.distance.numerator, cert.distance.denominator)
        witness = DualWitness.from_fractions(cert.witness, cert.distance) if cert.distance > 0 else None
        residual = Matrix([Rational(r.numerator, r.denominator) for r in cert.residual]) if m else Matrix.zeros(0, 1)
        return distance, witness, residual
