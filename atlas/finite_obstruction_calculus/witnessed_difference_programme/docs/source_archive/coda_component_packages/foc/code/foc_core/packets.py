"""Data structures, enums, certificates, and packets for CODA-FOC.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e).
Self-contained: Zero external monorepo dependencies.
Constraint: Zero floating-point operations in exact algebraic decision paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from sympy import Abs, ImmutableMatrix, Matrix, Rational, simplify
from sympy.matrices.matrixbase import MatrixBase

from .exact_arithmetic import (
    _as_exact_rational,
    _check_no_floats,
    _digest_exact,
    _exact_matrix,
    _exact_vector,
    exact_equal,
    exact_matrix_from_matrix,
)


class Diagnostic(str, Enum):
    EXACT_REPAIR = "ExactRepair"
    COHERENT_RESIDUAL = "CoherentResidual"
    NONCLOSED_DEFECT = "NonclosedDefect"


class TerminalRoute(str, Enum):
    EXACT_REPAIR = "ExactRepair"
    STABILIZED_SURVIVOR = "StabilizedSurvivor"
    OPEN_OBSTRUCTION = "OpenObstruction"


class RepairDisposition(str, Enum):
    NO_ADMISSIBLE_REPAIR = "NoAdmissibleRepair"
    REPAIR_AVAILABLE = "RepairAvailable"
    REFUSED = "Refused"


@dataclass(frozen=True, slots=True)
class QuotientCertificate:
    value: Rational
    repair: Matrix
    residual: Matrix
    annihilator: Matrix
    duality_gap: Rational
    input_digest: str
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        _check_no_floats(self.value, "QuotientCertificate.value")
        _check_no_floats(self.duality_gap, "QuotientCertificate.duality_gap")
        object.__setattr__(self, "value", _as_exact_rational(self.value))
        object.__setattr__(self, "duality_gap", _as_exact_rational(self.duality_gap))
        for name in ("repair", "residual", "annihilator"):
            mat = getattr(self, name)
            _check_no_floats(mat, f"QuotientCertificate.{name}")
            if not isinstance(mat, MatrixBase):
                raise TypeError(f"{name} must be a matrix, got {type(mat).__name__}")
            object.__setattr__(self, name, ImmutableMatrix(exact_matrix_from_matrix(mat)))

    def verify(
        self,
        repair_map: Any | None = None,
        cochain: Any | None = None,
        weights: Any | None = None,
    ) -> bool:
        """Verify certificate consistency and optional adherence to declared problem data."""
        _check_no_floats(self.value, "QuotientCertificate.value")
        _check_no_floats(self.duality_gap, "QuotientCertificate.duality_gap")
        _check_no_floats(self.repair, "QuotientCertificate.repair")
        _check_no_floats(self.residual, "QuotientCertificate.residual")
        _check_no_floats(self.annihilator, "QuotientCertificate.annihilator")
        if self.authority_effect != "None":
            return False
        if self.duality_gap != 0:
            return False
        if self.value < 0:
            return False
        if self.residual.shape[1] != 1 or self.annihilator.shape[1] != 1 or self.repair.shape[1] != 1:
            return False
        m = self.residual.rows
        if self.annihilator.rows != m:
            return False

        if repair_map is not None and cochain is not None and weights is not None:
            mat = _exact_matrix(repair_map)
            x = _exact_vector(cochain)
            w = _exact_vector(weights)
            if mat.rows != m or mat.cols != self.repair.rows:
                return False
            if x.shape != (m, 1) or w.shape != (m, 1):
                return False
            if self.input_digest != _digest_exact("quotient", mat, x, w):
                return False
            if not exact_equal(self.residual, x + mat * self.repair):
                return False
            weighted_norm = sum(w[i, 0] * Abs(self.residual[i, 0]) for i in range(m))
            if simplify(weighted_norm - self.value) != 0:
                return False
            if mat.cols > 0 and not exact_equal(mat.T * self.annihilator, Matrix.zeros(mat.cols, 1)):
                return False
            if any(bool(Abs(self.annihilator[i, 0]) > w[i, 0]) for i in range(m)):
                return False
            dual_pairing = (self.annihilator.T * x)[0, 0] if m > 0 else Rational(0)
            if simplify(self.value - dual_pairing) != 0:
                return False
        return True


@dataclass(frozen=True, slots=True)
class FiniteObstructionPacket:
    d0: Matrix
    d1: Matrix
    a2: Matrix
    w1: Matrix
    w2: Matrix

    def __post_init__(self) -> None:
        # A frozen dataclass alone does not freeze mutable SymPy matrices.
        for name in ("d0", "d1", "a2", "w1", "w2"):
            object.__setattr__(self, name, ImmutableMatrix(_exact_matrix(getattr(self, name))))

    @classmethod
    def create(
        cls,
        d0: Any,
        d1: Any,
        a2: Any,
        w1: Any,
        w2: Any,
        *,
        tolerance: Any = None,
    ) -> "FiniteObstructionPacket":
        if tolerance is not None and isinstance(tolerance, float):
            raise TypeError("Floating-point tolerance is prohibited on the exact rail")
        m_d0 = _exact_matrix(d0)
        m_d1 = _exact_matrix(d1)
        m_a2 = _exact_matrix(a2)
        v_w1 = _exact_vector(w1)
        v_w2 = _exact_vector(w2)
        packet = cls(m_d0, m_d1, m_a2, v_w1, v_w2)
        packet.validate(tolerance=tolerance)
        return packet

    def validate(self, *, tolerance: Any = None) -> None:
        if tolerance is not None and isinstance(tolerance, float):
            raise TypeError("Floating-point tolerance is prohibited on the exact rail")
        n1 = self.d0.rows
        n2 = self.d1.rows
        d1_domain = self.d1.cols
        if d1_domain != n1 or self.a2.rows != n2:
            raise ValueError("map dimensions do not compose")
        if self.w1.shape != (n1, 1) or self.w2.shape != (n2, 1):
            raise ValueError("weight dimensions do not match carriers")
        if any(w <= 0 for w in self.w1) or any(w <= 0 for w in self.w2):
            raise ValueError("observer weights must be strictly positive")
        composition = self.d1 * self.d0
        if not exact_equal(composition, Matrix.zeros(self.d1.rows, self.d0.cols)):
            raise ValueError("cochain condition d1*d0=0 failed")


@dataclass(frozen=True, slots=True)
class ObstructionResult:
    phi1: QuotientCertificate
    gamma2: QuotientCertificate
    diagnostic: Diagnostic
    input_digest: str
    observer_digest: str
    authority_effect: str = "None"
