"""Exported Smith trace of the frozen witness [[2, 4], [2, 6]].

Origin: code/rust/src/linear_algebra/smith_form.rs, which certifies
U * A * V = D by pivot-selection elimination over Z.
Claim: urn:omega:fqm:linear-algebra:exported-smith-trace:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_smith_export.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 2; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 4.
Scope Fence: This file re-exports the package surface and checks that one
frozen 2 by 2 integer witness. An explicit witness must be that same shape
of exact integers. This file does not recompute Smith form and does not
admit floats, booleans, or a non-integer entry.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from .scalars import GaussianRational, Q, q
from .matrix import ExactMatrix, MatrixError
from .smith_form import smith_normal_form
from .image_kernel import image_basis, kernel_basis

from . import bareiss_det
from . import basic_matrix
from . import char_poly
from . import commutant
from . import complex_tensor
from . import compositum_deg
from . import congruence
from . import cyclo_density
from . import elimination
from . import entropy_dichotomy
from . import field_factors
from . import field_squares
from . import image_kernel
from . import interpolation
from . import involution
from . import laws
from . import matrix
from . import ordered
from . import poly_roots
from . import pseudoinverse
from . import quintic_split
from . import rational_factors
from . import scalars
from . import second_jet
from . import smith_form
from . import spectral_factors
from . import splitting_deg
from . import tensor_proj
from . import test_support

__all__ = [
    "GaussianRational", "Q", "q", "ExactMatrix", "MatrixError", "smith_normal_form", "image_basis", "kernel_basis",
    "bareiss_det",
    "basic_matrix",
    "char_poly",
    "commutant",
    "complex_tensor",
    "compositum_deg",
    "congruence",
    "cyclo_density",
    "elimination",
    "entropy_dichotomy",
    "field_factors",
    "field_squares",
    "image_kernel",
    "interpolation",
    "involution",
    "laws",
    "matrix",
    "ordered",
    "poly_roots",
    "pseudoinverse",
    "quintic_split",
    "rational_factors",
    "scalars",
    "second_jet",
    "smith_form",
    "spectral_factors",
    "splitting_deg",
    "tensor_proj",
    "test_support",
    "exported_smith_trace",
]

_FROZEN: tuple[tuple[int, int], tuple[int, int]] = ((2, 4), (2, 6))


class SmithExportError(ValueError):
    """One violated exported-Smith invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SmithExportError:
    return SmithExportError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _reject_bool(value: object, role: str) -> None:
    if type(value) is bool:
        raise _fail("boolean refused where an integer witness entry was required", role=role)


def _exact_int(value: object, role: str) -> int:
    _refuse_float(value, role)
    _reject_bool(value, role)
    if type(value) is not int:
        raise _fail("Smith witness entry must be an exact integer", role=role, received=type(value).__name__)
    return value


def _pair(row: object, role: str) -> tuple[int, int]:
    if isinstance(row, (str, bytes)) or not isinstance(row, tuple) or len(row) != 2:
        raise _fail("Smith witness row must contain two entries", role=role, received=type(row).__name__)
    return (_exact_int(row[0], role + "_0"), _exact_int(row[1], role + "_1"))


def _require_witness(value: object) -> tuple[tuple[int, int], tuple[int, int]]:
    if isinstance(value, (str, bytes)) or not isinstance(value, tuple) or len(value) != 2:
        raise _fail("Smith witness must be two rows", received=type(value).__name__)
    return (_pair(value[0], "row0"), _pair(value[1], "row1"))


def _rational_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    _reject_bool(value, role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("Smith diagonal entry is not an exact rational", role=role, received=type(value).__name__)


def _require_factorization(
    left: ExactMatrix,
    witness: ExactMatrix,
    right: ExactMatrix,
    diagonal: ExactMatrix,
) -> None:
    if left * witness * right != diagonal:
        raise _fail("exported Smith form failed U*A*V = D")


def _trace_of(rows: tuple[tuple[int, int], tuple[int, int]]) -> Fraction:
    witness = ExactMatrix.from_rows(
        [
            [Fraction(rows[0][0]), Fraction(rows[0][1])],
            [Fraction(rows[1][0]), Fraction(rows[1][1])],
        ]
    )
    diagonal, left, right = smith_normal_form(witness)
    _require_factorization(left, witness, right, diagonal)
    return _rational_entry(diagonal.get(0, 0), "d0") + _rational_entry(diagonal.get(1, 1), "d1")


def exported_smith_trace(witness: object = None) -> Fraction:
    """Trace of the Smith diagonal. The default witness is [[2, 4], [2, 6]]."""
    rows = _FROZEN if witness is None else witness
    return _trace_of(_require_witness(rows))
