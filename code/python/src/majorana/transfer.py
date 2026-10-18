"""Native exact finite reverse-triangle transfer certificates for PO-000 §5.6.

SymPy values retain the paper's presentation. All premise decisions, norms,
transfer arithmetic, and certificate replay delegate to omega_functional.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from native_exact_input import ExactInput, as_rational, exact_vector, matrix_wire
from sympy import Basic, Matrix, Rational
from sympy.matrices.matrixbase import MatrixBase

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    NativeMathReply,
    call_native,
)

_SCALARS = (
    "lipschitz_constant",
    "source_distance",
    "projection_distance",
    "rho_defect",
    "sigma_defect",
    "defect_difference",
    "transfer_lower_bound",
)
_FLAGS = ("accepted", "pairwise_lipschitz_premise", "reverse_triangle_holds")
_OPTIONAL_FLAGS = ("defect_difference_bound_holds", "transfer_holds")


@dataclass
class ReverseTriangleCertificate:
    """Finite result retaining the original request and complete native outcome."""

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
    _native_request: dict[str, Any] | None = field(
        default=None, init=False, repr=False, compare=False
    )
    _native_reply: NativeMathReply | None = field(
        default=None, init=False, repr=False, compare=False
    )

    @property
    def native_outcome(self) -> Any:
        return None if self._native_reply is None else self._native_reply.outcome

    def _wire(self) -> dict:
        if any(not isinstance(getattr(self, name), bool) for name in _FLAGS):
            raise TypeError("certificate flags must be booleans")
        if any(
            getattr(self, name) is not None and not isinstance(getattr(self, name), bool)
            for name in _OPTIONAL_FLAGS
        ):
            raise TypeError("certificate conclusion flags must be boolean or None")
        return {
            **{name: str(as_rational(getattr(self, name))) for name in _SCALARS},
            **{name: getattr(self, name) for name in (*_FLAGS, *_OPTIONAL_FLAGS)},
            "refusal": self.refusal,
        }

    def verify(self) -> bool:
        """Replay the original supplied pair; fabricated report-only objects fail."""
        if self._native_request is None:
            return False
        if (
            self.evidence_scope,
            self.universal_theorem_status,
            self.density_matrix_specialization_status,
            self.authority_effect,
        ) != ("exact finite reverse-triangle instance", "not claimed", "not claimed", "None"):
            return False
        try:
            actual = self._wire()
        except (TypeError, ValueError):
            return False
        expected = call_native("functional_projection_transfer", self._native_request)
        return actual == {name: expected[name] for name in actual}


def _certificate(request: dict, reply: NativeMathReply) -> ReverseTriangleCertificate:
    result = ReverseTriangleCertificate(
        **{name: as_rational(reply[name]) for name in _SCALARS},
        **{name: reply[name] for name in (*_FLAGS, *_OPTIONAL_FLAGS)},
        refusal=reply["refusal"],
    )
    result._native_request = request
    result._native_reply = reply
    return result


def reverse_triangle_certificate(
    rho: Sequence[ExactInput] | MatrixBase,
    sigma: Sequence[ExactInput] | MatrixBase,
    projected_rho: Sequence[ExactInput] | MatrixBase,
    projected_sigma: Sequence[ExactInput] | MatrixBase,
    lipschitz_constant: ExactInput,
) -> ReverseTriangleCertificate:
    """Delegate the complete finite pairwise premise and transfer calculation."""
    vectors = [
        exact_vector(value, label=name)
        for name, value in (
            ("rho", rho),
            ("sigma", sigma),
            ("projected_rho", projected_rho),
            ("projected_sigma", projected_sigma),
        )
    ]
    if len({value.shape for value in vectors}) != 1:
        raise ValueError("all four vectors must have the same shape")
    request = {
        **{
            name: [str(item) for item in value]
            for name, value in zip(
                ("rho", "sigma", "projected_rho", "projected_sigma"), vectors, strict=True
            )
        },
        "lipschitz_constant": str(as_rational(lipschitz_constant)),
    }
    reply = call_native("functional_projection_transfer", request)
    return _certificate(request, reply)


def linear_projection_transfer_certificate(
    rho: Sequence[ExactInput] | MatrixBase,
    sigma: Sequence[ExactInput] | MatrixBase,
    projection: MatrixBase,
    lipschitz_constant: ExactInput,
) -> ReverseTriangleCertificate:
    """Validate idempotence and apply the declared projection in native Rust."""
    left = exact_vector(rho, label="rho")
    right = exact_vector(sigma, label="sigma")
    matrix = matrix_wire(projection)
    if projection.shape != (left.rows, left.rows):
        raise ValueError(
            f"projection has shape {projection.shape}, expected {(left.rows, left.rows)}"
        )
    if right.shape != left.shape:
        raise ValueError("rho and sigma must have the same shape")
    idempotence = call_native(
        "math_rational_matrix", {"operation": "is_idempotent", "matrix": matrix}
    )
    if idempotence["is_idempotent"] is not True:
        raise ValueError("projection matrix P is not idempotent (P^2 != P)")
    images = [
        call_native(
            "math_rational_matrix",
            {"operation": "apply", "matrix": matrix, "vector": [str(item) for item in state]},
        )["vector"]
        for state in (left, right)
    ]
    return reverse_triangle_certificate(
        left,
        right,
        Matrix(left.rows, 1, images[0]),
        Matrix(right.rows, 1, images[1]),
        lipschitz_constant,
    )
