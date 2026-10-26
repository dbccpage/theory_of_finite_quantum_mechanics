"""Diagnosis, quotient evaluation, and defect certification for CODA-FOC.

Bounded Context: CODA.FOC (Finite Obstruction Calculus)
AuthorityEffect: None.
Constraint: Zero floating-point operations in exact algebraic decision paths.
"""

from __future__ import annotations

from typing import Any

from sympy import Abs, ImmutableMatrix, Matrix, Rational, simplify

from .exact_arithmetic import (
    _digest_exact,
    _exact_matrix,
    _exact_vector,
    exact_equal,
)
from .packets import (
    Diagnostic,
    FiniteObstructionPacket,
    ObstructionResult,
    QuotientCertificate,
)
from .solvers import LinearRepairProblem


def quotient_certificate(
    repair_map: Any,
    vector: Any,
    weights: Any,
    *,
    tolerance: Any = None,
) -> QuotientCertificate:
    """Solve one positive weighted L1 quotient problem and its exact dual via LinearRepairProblem."""
    if tolerance is not None and isinstance(tolerance, float):
        raise TypeError("Floating-point tolerance is prohibited on the exact rail")
    matrix = _exact_matrix(repair_map)
    x = _exact_vector(vector)
    w = _exact_vector(weights)

    if matrix.rows != x.rows or x.rows != w.rows:
        raise ValueError("quotient dimensions do not match")
    if any(val <= 0 for val in w):
        raise ValueError("quotient weights must be strictly positive")

    m = matrix.rows
    n = matrix.cols

    if m == 0:
        val = Rational(0)
        rep = ImmutableMatrix(Matrix.zeros(n, 1))
        res = ImmutableMatrix(Matrix.zeros(0, 1))
        ann = ImmutableMatrix(Matrix.zeros(0, 1))
        gap = Rational(0)
        return QuotientCertificate(
            value=val,
            repair=rep,
            residual=res,
            annihilator=ann,
            duality_gap=gap,
            input_digest=_digest_exact("quotient", matrix, x, w),
        )

    # Diagonal scaling: W = diag(w_1, ..., w_m)
    W = Matrix.diag(*w)
    W_matrix = W * matrix
    W_x = W * x

    import sys
    solver_cls = getattr(
        sys.modules.get("finite_obstruction"), "LinearRepairProblem", LinearRepairProblem
    )
    problem = solver_cls(W_matrix)
    cert = problem.quotient_l1_distance(W_x)

    # In LinearRepairProblem: cert.residual = W_x - W_matrix * cert.repair_witness
    # In FOC: residual = x + matrix * repair_f, so repair_f = -cert.repair_witness
    repair_f = ImmutableMatrix(-cert.repair_witness)

    # The unweighted residual: residual = W^{-1} * cert.residual
    residual = ImmutableMatrix(Matrix([cert.residual[i, 0] / w[i, 0] for i in range(m)]))

    # Dual functional: z = W * cert.dual_witness
    annihilator = ImmutableMatrix(Matrix([cert.dual_witness[i, 0] * w[i, 0] for i in range(m)]))

    exact_value = cert.distance
    dual_pairing = (annihilator.T * x)[0, 0]
    duality_gap = simplify(exact_value - dual_pairing)

    if duality_gap != 0:
        raise RuntimeError(f"exact duality gap nonzero: {duality_gap}")
    if n > 0 and not exact_equal(matrix.T * annihilator, Matrix.zeros(n, 1)):
        raise RuntimeError("annihilator does not vanish on the full repair subspace")
    if any(Abs(annihilator[i, 0]) > w[i, 0] for i in range(m)):
        raise RuntimeError("annihilator exceeds observer capacity")

    return QuotientCertificate(
        value=exact_value,
        repair=repair_f,
        residual=residual,
        annihilator=annihilator,
        duality_gap=duality_gap,
        input_digest=_digest_exact("quotient", matrix, x, w),
    )


def diagnose(
    packet: FiniteObstructionPacket,
    defect: Any,
    *,
    tolerance: Any = None,
) -> ObstructionResult:
    """Diagnose a defect on a finite obstruction packet via exact trichotomy."""
    if tolerance is not None and isinstance(tolerance, float):
        raise TypeError("Floating-point tolerance is prohibited on the exact rail")
    packet.validate(tolerance=tolerance)
    x = _exact_vector(defect)
    if x.rows != packet.d0.rows:
        raise ValueError("defect does not inhabit C1")
    phi1 = quotient_certificate(packet.d0, x, packet.w1, tolerance=tolerance)
    d1_x = packet.d1 * x
    gamma2 = quotient_certificate(packet.a2, d1_x, packet.w2, tolerance=tolerance)
    if phi1.value == 0:
        diagnostic = Diagnostic.EXACT_REPAIR
    elif gamma2.value == 0:
        diagnostic = Diagnostic.COHERENT_RESIDUAL
    else:
        diagnostic = Diagnostic.NONCLOSED_DEFECT
    return ObstructionResult(
        phi1=phi1,
        gamma2=gamma2,
        diagnostic=diagnostic,
        input_digest=_digest_exact(
            "obstruction-packet",
            packet.d0,
            packet.d1,
            packet.a2,
            packet.w1,
            packet.w2,
            x,
        ),
        observer_digest=_digest_exact("observer", packet.w1, packet.w2),
    )


def is_full_subspace_annihilator(
    repair_map: Any,
    functional: Any,
    *,
    tolerance: Any = None,
) -> bool:
    """Test whether a functional vanishes on the entire image of the repair map."""
    if tolerance is not None and isinstance(tolerance, float):
        raise TypeError("Floating-point tolerance is prohibited on the exact rail")
    matrix = _exact_matrix(repair_map)
    z = _exact_vector(functional)
    if matrix.rows != z.rows:
        raise ValueError("annihilator dimensions do not match")
    return exact_equal(matrix.T * z, Matrix.zeros(matrix.cols, 1))


def direct_sum(
    left: FiniteObstructionPacket, right: FiniteObstructionPacket
) -> FiniteObstructionPacket:
    """Form the direct sum of two finite obstruction packets."""
    return FiniteObstructionPacket.create(
        Matrix.diag(left.d0, right.d0),
        Matrix.diag(left.d1, right.d1),
        Matrix.diag(left.a2, right.a2),
        Matrix.vstack(left.w1, right.w1),
        Matrix.vstack(left.w2, right.w2),
    )


__all__ = [
    "diagnose",
    "direct_sum",
    "is_full_subspace_annihilator",
    "quotient_certificate",
]
