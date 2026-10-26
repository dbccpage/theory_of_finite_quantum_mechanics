"""Exact finite reverse-triangle transfer certificates for PO-000 §5.6.

The caller supplies two points and their projected images.  The certificate
first checks the pairwise Lipschitz premise and only then exposes the transfer
inequality.  A failed premise is a refusal, even when the final numerical
inequality happens to hold accidentally.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from exactsym import Basic, Matrix, MatrixBase, Rational, simplify

from exact import ExactInput, as_rational, exact_column, exact_equal, l1_norm


def _exact_vector(
    value: Sequence[ExactInput] | MatrixBase,
    *,
    label: str,
) -> Matrix:
    if isinstance(value, MatrixBase):
        vector = Matrix(
            value.rows,
            value.cols,
            [
                as_rational(value[row, col])
                for row in range(value.rows)
                for col in range(value.cols)
            ],
        )
    else:
        vector = exact_column(value)
    if vector.cols != 1:
        raise ValueError(f"{label} must be a column vector")
    return vector



@dataclass(frozen=True)
class ReverseTriangleCertificate:
    """Exact result for one compared pair and one declared Lipschitz constant."""

    accepted: bool
    lipschitz_constant: Rational
    source_distance: Basic
    projection_distance: Basic
    rho_defect: Basic
    sigma_defect: Basic
    defect_difference: Basic
    transfer_lower_bound: Basic
    pairwise_lipschitz_premise: bool
    reverse_triangle_holds: bool
    defect_difference_bound_holds: bool | None
    transfer_holds: bool | None
    refusal: str | None
    evidence_scope: str = "exact finite reverse-triangle instance"
    universal_theorem_status: str = "not claimed"
    density_matrix_specialization_status: str = "not claimed"
    authority_effect: str = "None"

    def verify(self) -> bool:
        reverse_triangle = bool(self.rho_defect >= self.sigma_defect - self.defect_difference)
        if reverse_triangle != self.reverse_triangle_holds:
            return False
        if not self.accepted:
            return (
                not self.pairwise_lipschitz_premise
                and self.refusal is not None
                and self.defect_difference_bound_holds is None
                and self.transfer_holds is None
            )
        expected_difference_bound = bool(
            self.defect_difference <= (1 + self.lipschitz_constant) * self.source_distance
        )
        expected_transfer = bool(self.rho_defect >= self.transfer_lower_bound)
        return (
            self.pairwise_lipschitz_premise
            and self.refusal is None
            and self.defect_difference_bound_holds == expected_difference_bound
            and self.transfer_holds == expected_transfer
            and expected_difference_bound
            and expected_transfer
        )


def reverse_triangle_certificate(
    rho: Sequence[ExactInput] | MatrixBase,
    sigma: Sequence[ExactInput] | MatrixBase,
    projected_rho: Sequence[ExactInput] | MatrixBase,
    projected_sigma: Sequence[ExactInput] | MatrixBase,
    lipschitz_constant: ExactInput,
) -> ReverseTriangleCertificate:
    """Check the pairwise premise and exact transfer inequality.

    With ``C_P(x) = ||x-P(x)||_1`` and a checked pairwise bound
    ``||P(rho)-P(sigma)||_1 <= L ||rho-sigma||_1``, this verifies

    ``C_P(rho) >= C_P(sigma) - (1+L)||rho-sigma||_1``.
    """

    left = _exact_vector(rho, label="rho")
    right = _exact_vector(sigma, label="sigma")
    projected_left = _exact_vector(projected_rho, label="projected_rho")
    projected_right = _exact_vector(projected_sigma, label="projected_sigma")
    shapes = {left.shape, right.shape, projected_left.shape, projected_right.shape}
    if len(shapes) != 1:
        raise ValueError(f"all four vectors must have the same shape, got {sorted(shapes)}")

    lipschitz = as_rational(lipschitz_constant)
    if lipschitz < 0:
        raise ValueError("lipschitz_constant must be nonnegative")

    source_distance = simplify(l1_norm(left - right))
    projection_distance = simplify(l1_norm(projected_left - projected_right))
    left_residual = left - projected_left
    right_residual = right - projected_right
    rho_defect = simplify(l1_norm(left_residual))
    sigma_defect = simplify(l1_norm(right_residual))
    defect_difference = simplify(l1_norm(left_residual - right_residual))
    transfer_lower_bound = simplify(sigma_defect - (1 + lipschitz) * source_distance)
    premise = bool(projection_distance <= lipschitz * source_distance)
    reverse_triangle = bool(rho_defect >= sigma_defect - defect_difference)

    if not premise:
        certificate = ReverseTriangleCertificate(
            accepted=False,
            lipschitz_constant=lipschitz,
            source_distance=source_distance,
            projection_distance=projection_distance,
            rho_defect=rho_defect,
            sigma_defect=sigma_defect,
            defect_difference=defect_difference,
            transfer_lower_bound=transfer_lower_bound,
            pairwise_lipschitz_premise=False,
            reverse_triangle_holds=reverse_triangle,
            defect_difference_bound_holds=None,
            transfer_holds=None,
            refusal="pairwise_lipschitz_premise_failed",
        )
    else:
        difference_bound = bool(defect_difference <= (1 + lipschitz) * source_distance)
        transfer = bool(rho_defect >= transfer_lower_bound)
        certificate = ReverseTriangleCertificate(
            accepted=True,
            lipschitz_constant=lipschitz,
            source_distance=source_distance,
            projection_distance=projection_distance,
            rho_defect=rho_defect,
            sigma_defect=sigma_defect,
            defect_difference=defect_difference,
            transfer_lower_bound=transfer_lower_bound,
            pairwise_lipschitz_premise=True,
            reverse_triangle_holds=reverse_triangle,
            defect_difference_bound_holds=difference_bound,
            transfer_holds=transfer,
            refusal=None,
        )

    if not certificate.verify():
        raise ArithmeticError("reverse-triangle certificate failed internal exact recheck")
    return certificate


def linear_projection_transfer_certificate(
    rho: Sequence[ExactInput] | MatrixBase,
    sigma: Sequence[ExactInput] | MatrixBase,
    projection: MatrixBase,
    lipschitz_constant: ExactInput,
) -> ReverseTriangleCertificate:
    """Convenience wrapper for an explicitly supplied exact linear map."""

    left = _exact_vector(rho, label="rho")
    right = _exact_vector(sigma, label="sigma")
    matrix = Matrix(
        projection.rows,
        projection.cols,
        [
            as_rational(projection[row, col])
            for row in range(projection.rows)
            for col in range(projection.cols)
        ],
    )
    if matrix.shape != (left.rows, left.rows):
        raise ValueError(f"projection has shape {matrix.shape}, expected {(left.rows, left.rows)}")
    if right.shape != left.shape:
        raise ValueError("rho and sigma must have the same shape")
    if not exact_equal(matrix * matrix, matrix):
        raise ValueError("projection matrix P is not idempotent (P^2 != P)")
    return reverse_triangle_certificate(
        left,
        right,
        matrix * left,
        matrix * right,
        lipschitz_constant,
    )

