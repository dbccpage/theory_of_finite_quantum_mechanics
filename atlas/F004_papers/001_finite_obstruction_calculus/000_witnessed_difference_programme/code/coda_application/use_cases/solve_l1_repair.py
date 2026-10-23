# -*- coding: utf-8 -*-
"""
L1 repair and dual witness certification use case.
Solves exact rational quotient distance Phi_1([x]) = min_f ||x - D f||_1 and validates dual witness.

Supplies the native functional evaluator through the domain interface.
The native solver proposes a repair; omega_functional checks its primal and
dual certificate. The returned residual is x - D f for that checked repair.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Optional, Tuple

from sympy import Matrix, Rational

from coda_application.domain.l1_quotient import FunctionalEvaluator
from coda_application.domain.intake import exact, matrix_rows
from coda_application.domain.l1_quotient import solve_l1_quotient
from coda_application.domain.value_objects import DualWitness, ExactRational


def solve_exact_l1_repair(
    d: Matrix,
    cochain: Matrix,
    *, evaluator: FunctionalEvaluator,
) -> Tuple[ExactRational, Optional[DualWitness], Matrix]:
    """
    Computes the exact L1 quotient distance and its dual witness y* in ker(d^T).
    Returns (distance, dual_witness or None when the distance is 0, residual_vector).
    """
    rows, (m, k) = matrix_rows(d, "d")
    if cochain.cols != 1 or cochain.rows != m:
        raise ValueError(f"cochain shape {cochain.shape} does not match boundary with {m} rows")
    x = [exact(cochain[i, 0], f"cochain[{i}]") for i in range(m)]
    cert = solve_l1_quotient(rows, k, x, evaluator=evaluator)
    distance = ExactRational(cert.distance.numerator, cert.distance.denominator)
    witness = DualWitness.from_fractions(cert.witness, cert.distance) if cert.distance > 0 else None
    residual = Matrix([Rational(r.numerator, r.denominator) for r in cert.residual]) if m else Matrix.zeros(0, 1)
    return distance, witness, residual
