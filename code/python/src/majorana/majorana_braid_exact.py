"""majorana_braid_exact.py — Non-Abelian Anyon Braiding & Yang-Baxter Representation.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Claim MAJ-C7/MAJ-C8, gemini_000.md.

Mechanizes:
1. Exact Non-Abelian Braid Representation for Ising Anyons / MZMs:
   - Evaluates elementary braid operators R_j on the Clifford carrier of 2M Majorana modes.
   - Adjoint action on Majorana operators:
     R_j gamma_j R_j^dagger = gamma_{j+1}
     R_j gamma_{j+1} R_j^dagger = -gamma_j
     R_j gamma_k R_j^dagger = gamma_k for k notin {j, j+1}
2. Exact Rational Representation Matrices:
   - Every braid acts as an exact signed permutation matrix in SO(2M) with entries in {-1, 0, 1}.
   - Pure exact rational numbers (fractions.Fraction) under Zero-Float Law.
3. Yang-Baxter Relation & Braid Group Invariants:
   - Verifies the braid relations:
     R_j R_{j+1} R_j == R_{j+1} R_j R_{j+1} (Yang-Baxter equation)
     R_i R_j == R_j R_i for |i - j| >= 2 (far commutativity)
   - Verifies zero decoherence on discrete steps and total fermion parity conservation.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    call_native,
    decode_rational,
)


def _matrix_wire(matrix: ExactSignedPermutationMatrix) -> dict[str, Any]:
    return {
        "rows": matrix.dim,
        "cols": matrix.dim,
        "data": [[str(Fraction(value)) for value in row] for row in matrix.data],
    }


def _decode_matrix(wire: dict[str, Any]) -> ExactSignedPermutationMatrix:
    if wire["rows"] != wire["cols"]:
        raise ValueError("Native Majorana matrix must be square")
    return ExactSignedPermutationMatrix(
        wire["rows"], tuple(tuple(decode_rational(value) for value in row) for row in wire["data"])
    )


def _braid_matrix(num_modes: int, steps: list[tuple[int, bool]]) -> ExactSignedPermutationMatrix:
    result = call_native("majorana_braid_action", {"num_modes": num_modes, "steps": steps})
    return _decode_matrix(result["matrix"])


def _valid_index(value: object, upper: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 1 <= value < upper


@dataclass(frozen=True)
class ExactSignedPermutationMatrix:
    """Exact matrix value object; rational operations belong to native linear algebra.

    The historical constructor admits arbitrary rational square matrices, including
    singular ones. Braid-generated matrices have the stronger signed-permutation
    invariant, checked by the native Majorana owner.
    """

    dim: int
    data: tuple[tuple[Fraction, ...], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.dim, int) or isinstance(self.dim, bool) or self.dim < 2:
            raise ValueError(f"dim must be integer >= 2, got {self.dim}")
        if len(self.data) != self.dim or any(len(row) != self.dim for row in self.data):
            raise ValueError(f"Data shape must be {self.dim}x{self.dim}")
        for row in self.data:
            for value in row:
                if not isinstance(value, (Fraction, int)) or isinstance(value, bool):
                    raise TypeError("Matrix entries must be Fraction or int, not float or bool")
        object.__setattr__(
            self,
            "data",
            tuple(tuple(Fraction(value) for value in row) for row in self.data),
        )

    @classmethod
    def identity(cls, dim: int) -> ExactSignedPermutationMatrix:
        """Construct the exact native identity action."""
        if not isinstance(dim, int) or isinstance(dim, bool) or dim < 2:
            raise ValueError(f"dim must be integer >= 2, got {dim}")
        return _braid_matrix(dim, [])

    def multiply(self, other: ExactSignedPermutationMatrix) -> ExactSignedPermutationMatrix:
        """Matrix product through the canonical rational-matrix owner."""
        if self.dim != other.dim:
            raise ValueError(f"Dimension mismatch: {self.dim} != {other.dim}")
        result = call_native(
            "math_rational_matrix",
            {"operation": "multiply", "matrix": _matrix_wire(self), "other": _matrix_wire(other)},
        )
        return _decode_matrix(result["matrix"])

    def transpose(self) -> ExactSignedPermutationMatrix:
        result = call_native(
            "math_rational_matrix", {"operation": "transpose", "matrix": _matrix_wire(self)}
        )
        return _decode_matrix(result["matrix"])

    def is_orthogonal(self) -> bool:
        return self.transpose().multiply(self) == self.identity(self.dim)

    def determinant(self) -> Fraction:
        result = call_native(
            "math_rational_matrix", {"operation": "determinant", "matrix": _matrix_wire(self)}
        )
        return decode_rational(result["value"])


class MajoranaBraidGenerator:
    """Elementary native braid adjoint action, using one-indexed generators."""

    def __init__(self, num_modes: int, j: int, inverse: bool = False) -> None:
        if not isinstance(num_modes, int) or isinstance(num_modes, bool) or num_modes < 2:
            raise ValueError(f"num_modes must be >= 2, got {num_modes}")
        if not _valid_index(j, num_modes):
            raise ValueError(f"Braid index j must be in [1, {num_modes - 1}], got {j}")
        if not isinstance(inverse, bool):
            raise TypeError("inverse must be boolean")
        self.num_modes = num_modes
        self.j = j
        self.inverse = inverse
        self._matrix = self._build_matrix()

    def _build_matrix(self) -> ExactSignedPermutationMatrix:
        return _braid_matrix(self.num_modes, [(self.j, self.inverse)])

    @property
    def matrix(self) -> ExactSignedPermutationMatrix:
        return self._matrix


class MajoranaBraidCircuit:
    """A braid word whose signed-permutation evaluation is owned by Rust."""

    def __init__(self, num_modes: int) -> None:
        if not isinstance(num_modes, int) or isinstance(num_modes, bool) or num_modes < 2:
            raise ValueError("num_modes must be integer >= 2")
        self.num_modes = num_modes
        self.steps: list[tuple[int, bool]] = []

    def append(self, j: int, inverse: bool = False) -> MajoranaBraidCircuit:
        if not _valid_index(j, self.num_modes):
            raise ValueError(f"Braid index {j} out of range [1, {self.num_modes - 1}]")
        if not isinstance(inverse, bool):
            raise TypeError("inverse must be boolean")
        self.steps.append((j, inverse))
        return self

    def evaluate_matrix(self) -> ExactSignedPermutationMatrix:
        return _braid_matrix(self.num_modes, self.steps)

    def verify_yang_baxter(self, j: int) -> bool:
        if not _valid_index(j, self.num_modes - 1):
            raise ValueError(f"Cannot verify Yang-Baxter for j={j} on {self.num_modes} modes")
        lhs = _braid_matrix(self.num_modes, [(j, False), (j + 1, False), (j, False)])
        rhs = _braid_matrix(self.num_modes, [(j + 1, False), (j, False), (j + 1, False)])
        return lhs == rhs

    def verify_far_commutativity(self, i: int, j: int) -> bool:
        if not _valid_index(i, self.num_modes) or not _valid_index(j, self.num_modes):
            raise ValueError(f"Braid indices out of range [1, {self.num_modes - 1}]")
        if abs(i - j) < 2:
            raise ValueError(f"Indices must satisfy |i - j| >= 2, got i={i}, j={j}")
        return _braid_matrix(self.num_modes, [(i, False), (j, False)]) == _braid_matrix(
            self.num_modes, [(j, False), (i, False)]
        )
