# -*- coding: utf-8 -*-
"""
coda_a_core.py: Standalone Exact Rational Linear Algebra and Finite Cochain Classification for CODA-A.

Governing Claims:
1. Definition A-D1: residual(C, x) = x - C x.
2. Definition A-D2: is_projection(C) <=> C² = C.
3. Theorem A-T1: residual(C, x) == 0 <=> C x == x.
4. Theorem A-T2: is_projection(C) => C(residual(C, x)) == 0.
5. Theorem A-T3: is_projection(C) => residual(C, residual(C, x)) == residual(C, x).
6. Theorem A-T4: is_projection(C) => (x in im(C) <=> C x == x).
7. Theorem A-T5: maps_commute(T, C, D) => T(residual(C, x)) == residual(D, T x).
8. Theorem A-T6: is_projection(C) => (x - y in im(C) <=> residual(C, x) == residual(C, y)).
9. Theorem A-T7: universal factorization on quotient V/R.
10. Scope fence A-S1: residual data are not decision or provenance data.
11. Finite discrete classifier for 5-case residual taxonomy (GTLA-01).
12. Strict zero floats invariant: exact rational arithmetic (SymPy Rational / Integer).
    Floats, numpy.floating, sympy.Float, and booleans passed as scalars strictly raise TypeError.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Any, Dict, Optional

from cochain_presentation import (
    LinearRepairProblem,
    QuotientDistanceCertificate,
)
from sympy import Float, Integer, Matrix, Rational
from sympy.matrices.matrixbase import MatrixBase

# ---------------------------------------------------------------------------
# Strict Exact Rational Validation
# ---------------------------------------------------------------------------

def _validate_exact_rational(val: Any, name: str) -> Rational:
    """Ensure value is an exact rational or integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    val_dtype = getattr(val, "dtype", None)
    if isinstance(val, (float, Float)) or (
        val_dtype is not None and "float" in str(val_dtype).lower()
    ):
        raise TypeError(f"{name} must be an exact rational or integer, got float (floats strictly forbidden)")
    if isinstance(val, (int, Integer, Fraction, Rational)):
        return Rational(val)
    if isinstance(val, str):
        try:
            return Rational(val)
        except Exception as exc:
            raise TypeError(f"{name} string could not be converted to exact Rational: {exc}") from exc
    raise TypeError(f"{name} must be an exact rational or integer, got {type(val).__name__}")


def _validate_exact_int(val: Any, name: str) -> int:
    """Ensure value is an exact non-negative integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an integer, got bool")
    val_dtype = getattr(val, "dtype", None)
    if val_dtype is not None and "float" in str(val_dtype).lower():
        raise TypeError(f"{name} must be an integer, got float")
    if not isinstance(val, (int, Integer)):
        raise TypeError(f"{name} must be an integer, got {type(val).__name__}")
    int_val = int(val)
    if int_val < 0:
        raise ValueError(f"{name} must be non-negative, got {int_val}")
    return int_val


def _matrix_entries_exact(M: MatrixBase, name: str) -> Matrix:
    """Copy a matrix, insisting every entry is an exact rational."""
    m = Matrix(M)
    for i in range(m.rows):
        for j in range(m.cols):
            m[i, j] = _validate_exact_rational(m[i, j], f"{name}[{i},{j}]")
    return m


def _column(vec: MatrixBase, name: str) -> Matrix:
    """Accept a row or column vector and return a column of exact rationals."""
    m = _matrix_entries_exact(Matrix(vec), name)
    if m.cols == 1:
        return m
    if m.rows == 1:
        return m.T
    raise ValueError(f"{name} must be a column vector, got shape {m.shape}")


def _square(C: MatrixBase, n: int, name: str) -> Matrix:
    """Accept a square matrix whose size matches a declared dimension."""
    m = _matrix_entries_exact(Matrix(C), name)
    if m.rows != m.cols:
        raise ValueError(f"{name} must be square, got shape {m.shape}")
    if m.rows != n:
        raise ValueError(f"{name} dimension ({m.rows}) must match vector dimension ({n})")
    return m


# ---------------------------------------------------------------------------
# Elementary Linear Algebra Operations (Theorems A-T1 through A-T7)
# ---------------------------------------------------------------------------

def residual(C: MatrixBase, x: MatrixBase) -> Matrix:
    """
    Definition A-D1: Leftover of a linear correction:
        residual(C, x) = x - C x.
    Always satisfies x = C x + residual(C, x).
    """
    xcol = _column(x, "x")
    Cmat = _square(C, xcol.rows, "C")
    return xcol - Cmat * xcol


def is_projection(C: MatrixBase) -> bool:
    """
    Definition A-D2: True exactly when C is square and C² = C.
    """
    m = _matrix_entries_exact(Matrix(C), "C")
    if m.rows != m.cols:
        raise ValueError(f"C must be square, got shape {m.shape}")
    return bool((m * m - m).is_zero_matrix)


def maps_commute(T: MatrixBase, C: MatrixBase, D: MatrixBase) -> bool:
    """
    True exactly when T C = D T with matching dimensions.
    """
    Tm = _matrix_entries_exact(Matrix(T), "T")
    Cm = _matrix_entries_exact(Matrix(C), "C")
    Dm = _matrix_entries_exact(Matrix(D), "D")
    if Cm.rows != Cm.cols:
        raise ValueError("C must be square")
    if Dm.rows != Dm.cols:
        raise ValueError("D must be square")
    if Tm.cols != Cm.rows:
        raise ValueError("T domain dimension must match C")
    if Tm.rows != Dm.rows:
        raise ValueError("T codomain dimension must match D")
    return bool((Tm * Cm - Dm * Tm).is_zero_matrix)


def difference_in_image(C: MatrixBase, x: MatrixBase, y: MatrixBase) -> bool:
    """
    Theorem A-T6: True exactly when x - y lies in the image of C.
    Decided via exact rational linear system certificate.
    """
    xcol = _column(x, "x")
    ycol = _column(y, "y")
    if xcol.rows != ycol.rows:
        raise ValueError(f"x and y must have the same dimension ({xcol.rows} != {ycol.rows})")
    Cmat = _square(C, xcol.rows, "C")
    cert = LinearRepairProblem(repair_map_d0=Cmat).exactness_certificate(
        cochain=xcol - ycol
    )
    return bool(cert.is_exact_coboundary)


def residual_in_kernel(correction: MatrixBase, vector: MatrixBase) -> Matrix:
    """
    Theorem A-T2: C(residual(C, x)) = 0. Requires C² = C.
    """
    C = _matrix_entries_exact(Matrix(correction), "correction")
    if C.rows != C.cols or not (C * C - C).is_zero_matrix:
        raise ValueError("idempotence hypothesis required (C² = C)")
    return C * residual(C, vector)


def residual_transport(
    source_correction: MatrixBase,
    target_correction: MatrixBase,
    transport: MatrixBase,
    vector: MatrixBase,
) -> Matrix:
    """
    Theorem A-T5: T(residual(C, x)) = residual(D, T x) under T C = D T.
    """
    if not maps_commute(transport, source_correction, target_correction):
        raise ValueError("commuting transport hypothesis required (T C = D T)")
    return Matrix(transport) * residual(source_correction, vector)


def induced_quotient_section(correction: MatrixBase, vector: MatrixBase) -> Matrix:
    """
    Section 4: The induced residual section representative s([x]) = x - C x in ker(C).
    Requires C² = C; maps representative x to its canonical residual representative in ker(C),
    which by Theorem A-T6 is independent of representative up to im(C).
    """
    C = _matrix_entries_exact(Matrix(correction), "correction")
    if C.rows != C.cols or not (C * C - C).is_zero_matrix:
        raise ValueError("idempotence hypothesis required (C² = C)")
    res = residual(C, vector)
    assert (C * res).is_zero_matrix, "residual must lie in ker(C)"
    return res


def quotient_universal_factor(f: MatrixBase, pi: MatrixBase) -> Matrix:
    """
    Theorem A-T7: For linear f : V -> W vanishing on R = ker(pi), find unique g : V/R -> W
    such that g * pi = f.
    Requires pi to be surjective onto the declared quotient space (rank(pi) == pi.rows)
    to guarantee factor uniqueness.
    """
    f_mat = _matrix_entries_exact(Matrix(f), "f")
    pi_mat = _matrix_entries_exact(Matrix(pi), "pi")
    if f_mat.cols != pi_mat.cols:
        raise ValueError("f and pi must share the same domain dimension")
    if pi_mat.rank() != pi_mat.rows:
        raise ValueError(
            f"pi must be surjective onto the quotient space (rank={pi_mat.rank()} != rows={pi_mat.rows}) "
            "to guarantee a unique linear factor"
        )
    # Solve g * pi = f <=> pi.T * g.T = f.T
    try:
        sol, params = pi_mat.T.gauss_jordan_solve(f_mat.T)
    except ValueError as e:
        raise ArithmeticError(f"quotient factorization failed: f does not factor through pi ({e})") from e
    if params.rows > 0 or len(sol.free_symbols) > 0:
        raise ValueError("quotient factor is not unique (free parameters in linear solve)")
    g = sol.T
    if not (g * pi_mat - f_mat).is_zero_matrix:
        raise ArithmeticError("quotient factorization failed: f does not factor through pi")
    return _matrix_entries_exact(g, "g")


# ---------------------------------------------------------------------------
# Discrete Residual Taxonomy & Terminal Records (GTLA-01 through GTLA-03)
# ---------------------------------------------------------------------------

class ResidualTerminalClass(str, Enum):
    CLOSURE_ABSORBED = "ClosureAbsorbed"
    CLOSED_RESIDUAL = "ClosedResidual"  # The Anomalon Terminal
    OPEN_RESIDUAL = "OpenResidual"
    LIFT_REQUIRED = "LiftRequired"
    REFUSED_CLOSURE = "RefusedClosure"


def is_anomalon(terminal_class: ResidualTerminalClass) -> bool:
    """Anomalon is the ClosedResidual class, not the entire taxonomy."""
    return terminal_class == ResidualTerminalClass.CLOSED_RESIDUAL


@dataclass(frozen=True)
class AuthEvidence:
    """Authority terminal evidence produced by finite descent."""

    packet_id: str
    terminalizer_id: str
    replayable: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.packet_id, str):
            raise TypeError("packet_id must be a string")
        if not isinstance(self.terminalizer_id, str):
            raise TypeError("terminalizer_id must be a string")
        if not isinstance(self.replayable, bool) or type(self.replayable) is not bool:
            raise TypeError("replayable must be a bool")


@dataclass(frozen=True)
class ResidualOutcome:
    """
    Residual terminal outcome in T_res + F_res.
    Contains no authority evidence by construction (GTLA-03).
    """

    classification: ResidualTerminalClass
    residual_class_id: str
    defect_vector: Optional[Matrix]
    quotient_distance: Optional[Rational]
    is_closed: bool
    refusal_reason: Optional[str] = None
    is_anomalon_terminal: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.classification, ResidualTerminalClass):
            raise TypeError("classification must be a ResidualTerminalClass")
        if not isinstance(self.residual_class_id, str) or not self.residual_class_id.strip():
            raise TypeError("residual_class_id must be a non-empty string")
        if self.refusal_reason is not None and (
            not isinstance(self.refusal_reason, str) or not self.refusal_reason.strip()
        ):
            raise TypeError("refusal_reason must be a non-empty string when provided")
        if not isinstance(self.is_closed, bool) or type(self.is_closed) is not bool:
            raise TypeError("is_closed must be an exact bool")

        if self.defect_vector is not None:
            vec = _column(self.defect_vector, "defect_vector")
            object.__setattr__(self, "defect_vector", vec)

        # Distance validation
        if self.classification in (
            ResidualTerminalClass.REFUSED_CLOSURE,
            ResidualTerminalClass.LIFT_REQUIRED,
        ):
            # Administrative states: quotient_distance is absent / None
            if self.quotient_distance is not None:
                raise ValueError(
                    f"{self.classification.value} must have quotient_distance=None"
                )
        else:
            # Mathematical states: distance must be non-negative Rational
            if self.quotient_distance is None:
                raise ValueError(
                    f"{self.classification.value} requires an exact quotient_distance, cannot be None"
                )
            qdist = _validate_exact_rational(self.quotient_distance, "quotient_distance")
            if qdist < 0:
                raise ValueError(f"quotient_distance must be non-negative, got {qdist}")
            object.__setattr__(self, "quotient_distance", qdist)

            # Invariant checks for mathematical states:
            if self.classification == ResidualTerminalClass.CLOSURE_ABSORBED:
                if not self.is_closed:
                    raise ValueError("ClosureAbsorbed must satisfy is_closed=True")
                if qdist != 0:
                    raise ValueError("ClosureAbsorbed must have quotient_distance=0")

            elif self.classification == ResidualTerminalClass.CLOSED_RESIDUAL:
                if not self.is_closed:
                    raise ValueError("ClosedResidual must satisfy is_closed=True")
                if qdist == 0:
                    raise ValueError(
                        "ClosedResidual must have positive quotient_distance (distance 0 is ClosureAbsorbed)"
                    )

            elif self.classification == ResidualTerminalClass.OPEN_RESIDUAL:
                if self.is_closed:
                    raise ValueError("OpenResidual must satisfy is_closed=False")
                if qdist == 0:
                    raise ValueError(
                        "OpenResidual cannot have quotient_distance=0 in a valid complex"
                    )

        object.__setattr__(
            self,
            "is_anomalon_terminal",
            is_anomalon(self.classification),
        )


@dataclass(frozen=True)
class Terminal:
    """
    Global terminal coproduct: AuthEvidence (+) ResidualOutcome.
    Constructed disjoint: inl carries AuthEvidence, inr carries ResidualOutcome.
    """

    auth_evidence: Optional[AuthEvidence] = None
    residual_outcome: Optional[ResidualOutcome] = None

    def __post_init__(self) -> None:
        if self.auth_evidence is not None and self.residual_outcome is not None:
            raise ValueError("Terminal cannot co-inhabit both AuthEvidence and ResidualOutcome")
        if self.auth_evidence is None and self.residual_outcome is None:
            raise ValueError("Terminal must carry either AuthEvidence or ResidualOutcome")

    def is_auth(self) -> bool:
        return (
            self.auth_evidence is not None
            and self.residual_outcome is None
            and self.auth_evidence.replayable is True
        )

    def is_residual(self) -> bool:
        return self.residual_outcome is not None and self.auth_evidence is None


def residual_not_auth(residual: ResidualOutcome) -> bool:
    """GTLA-14 / GTLA-03: No residual terminal is an authority terminal."""
    term = Terminal(residual_outcome=residual)
    return not term.is_auth()


@dataclass(frozen=True)
class GtlaObject:
    """
    A GTLA object carrying two independent readings:
    1. residual_closure: Option[ResidualOutcome]
    2. descent_classifier: Terminal
    """

    object_id: str
    residual_closure: Optional[ResidualOutcome]
    descent_classifier: Terminal

    def has_residual(self) -> bool:
        return self.residual_closure is not None

    def obj_auth(self) -> bool:
        return self.descent_classifier.is_auth()


# ---------------------------------------------------------------------------
# Finite Cochain Classifier
# ---------------------------------------------------------------------------

def classify_closure_attempt(
    d0: MatrixBase,
    d1: Optional[MatrixBase],
    defect_cochain: MatrixBase,
    closure_id: str = "closure_attempt",
    pending_lift: bool = False,
    refusal_reason: Optional[str] = None,
) -> ResidualOutcome:
    """
    Classifies a declared closure/repair attempt into the 5-case residual taxonomy (GTLA-01).
    Validates exact rational entries, shapes, and the cochain complex condition d1 * d0 = 0
    before any classification branch.
    """
    if not isinstance(closure_id, str) or not closure_id.strip():
        raise TypeError("closure_id must be a non-empty string")
    if not isinstance(pending_lift, bool) or type(pending_lift) is not bool:
        raise TypeError("pending_lift must be an exact bool")
    if refusal_reason is not None and (
        not isinstance(refusal_reason, str) or not refusal_reason.strip()
    ):
        raise TypeError("refusal_reason must be a non-empty string when provided")

    # 1. Validate exact matrices and dimensions first
    defect_col = _column(defect_cochain, "defect_cochain")
    d0_mat = _matrix_entries_exact(Matrix(d0), "d0")
    if d0_mat.rows != defect_col.rows:
        raise ValueError(f"d0 rows ({d0_mat.rows}) must match defect dimension ({defect_col.rows})")

    d1_mat: Optional[Matrix] = None
    if d1 is not None:
        d1_mat = _matrix_entries_exact(Matrix(d1), "d1")
        if d1_mat.cols != defect_col.rows:
            raise ValueError(f"d1 cols ({d1_mat.cols}) must match defect dimension ({defect_col.rows})")
        # Enforce cochain complex condition: d1 * d0 == 0 when d1 has rows
        if d1_mat.rows > 0:
            if not (d1_mat * d0_mat).is_zero_matrix:
                raise ValueError("d1 * d0 != 0: declared matrices do not form a valid cochain complex")

    # 2. Check explicit administrative refusal (no distance exposed)
    if refusal_reason is not None:
        return ResidualOutcome(
            classification=ResidualTerminalClass.REFUSED_CLOSURE,
            residual_class_id=f"{closure_id}_refused",
            defect_vector=defect_col,
            quotient_distance=None,
            is_closed=False,
            refusal_reason=refusal_reason,
        )

    # 3. Check administrative pending lift (no distance exposed)
    if pending_lift:
        return ResidualOutcome(
            classification=ResidualTerminalClass.LIFT_REQUIRED,
            residual_class_id=f"{closure_id}_lift",
            defect_vector=defect_col,
            quotient_distance=None,
            is_closed=True,
            refusal_reason="Pending lift obstruction issued and held",
        )

    # 4. For all mathematical classifications, solve exact quotient repair: d0 * alpha = defect
    problem = LinearRepairProblem(repair_map_d0=d0_mat)
    cert: QuotientDistanceCertificate = problem.quotient_l1_distance(cochain=defect_col)
    if not cert.verify():
        raise ArithmeticError("solver certificate verification failed")

    dist = Rational(cert.distance)
    if dist < 0:
        raise ArithmeticError(f"negative quotient distance returned by solver: {dist}")

    # 5. Check cocycle condition: d1 * defect == 0 (closedness)
    if d1_mat is not None and d1_mat.rows > 0:
        d1_defect = d1_mat * defect_col
        if not d1_defect.is_zero_matrix:
            return ResidualOutcome(
                classification=ResidualTerminalClass.OPEN_RESIDUAL,
                residual_class_id=f"{closure_id}_open",
                defect_vector=defect_col,
                quotient_distance=dist,
                is_closed=False,
                refusal_reason="d1 * defect != 0: open boundary tear",
            )

    if dist == Rational(0, 1):
        return ResidualOutcome(
            classification=ResidualTerminalClass.CLOSURE_ABSORBED,
            residual_class_id=f"{closure_id}_absorbed",
            defect_vector=defect_col,
            quotient_distance=Rational(0, 1),
            is_closed=True,
            refusal_reason=None,
        )

    # 6. Distance > 0 and cocycle closed: Closed residual survivor -> The Anomalon
    return ResidualOutcome(
        classification=ResidualTerminalClass.CLOSED_RESIDUAL,
        residual_class_id=f"{closure_id}_anomalon",
        defect_vector=defect_col,
        quotient_distance=dist,
        is_closed=True,
        refusal_reason="Survivor: closed non-bounding residual class (H^1 survivor)",
    )


def evaluate_authority_firewall(gtla_obj: GtlaObject) -> Dict[str, Any]:
    """
    Evaluates GTLA-03: Residual terminalization lands in T_res + F_res,
    strictly disjoint from T_auth on this declared finite object reading.
    AuthorityEffect: None unconditionally.
    """
    has_res = gtla_obj.has_residual()
    is_auth = gtla_obj.obj_auth()
    is_pure_residual = gtla_obj.descent_classifier.is_residual()

    return {
        "object_id": gtla_obj.object_id,
        "has_residual": has_res,
        "is_auth": is_auth,
        "is_pure_residual": is_pure_residual,
        "firewall_intact": not (is_pure_residual and is_auth),
        "authority_effect": "None",
    }


def reproduce_worked_example() -> Dict[str, Any]:
    """
    Replays 3 verified cochain classifications:
    1. Specimen 1: Boundary tear with d1 * defect != 0 -> OPEN_RESIDUAL
    2. Specimen 2: Closed non-bounding cycle in 3D complex -> CLOSED_RESIDUAL (Anomalon)
    3. Specimen 3: Pending lift (referral issued and held) -> LIFT_REQUIRED
    """
    # 1. Specimen 1: Open residual (non-cycle boundary tear in 2D)
    d0_toy = Matrix([[1], [2]])
    d1_toy = Matrix([[2, -1]])  # d1 * d0 = [0], valid complex!
    defect_open = Matrix([[1], [0]])  # d1 * defect = 2 != 0 -> OPEN
    res_specimen1 = classify_closure_attempt(
        d0=d0_toy,
        d1=d1_toy,
        defect_cochain=defect_open,
        closure_id="cochain_specimen1_open",
    )

    # 2. Specimen 2: Closed residual (Anomalon: 3D complex with H^1 survivor)
    # d0 : Q^1 -> Q^3, d1 : Q^3 -> Q^1
    # d0 = [[1], [0], [0]], d1 = [[0, 0, 1]]
    # d1 * d0 = [[0]], valid complex!
    # defect = [[0], [1], [0]]
    # d1 * defect = 0 (closed cycle), defect not in im(d0), dist = 1 > 0
    d0_3d = Matrix([[1], [0], [0]])
    d1_3d = Matrix([[0, 0, 1]])
    defect_closed = Matrix([[0], [1], [0]])
    res_specimen2 = classify_closure_attempt(
        d0=d0_3d,
        d1=d1_3d,
        defect_cochain=defect_closed,
        closure_id="cochain_specimen2_anomalon",
    )

    # 3. Specimen 3: Pending lift (LiftRequired issued and held)
    res_specimen3 = classify_closure_attempt(
        d0=d0_toy,
        d1=d1_toy,
        defect_cochain=Matrix([[0], [0]]),
        closure_id="cochain_specimen3_lift",
        pending_lift=True,
    )

    # 4. Pure residual object test
    pure_anomalon_obj = GtlaObject(
        object_id="Anomalon_Witness",
        residual_closure=res_specimen2,
        descent_classifier=Terminal(residual_outcome=res_specimen2),
    )
    firewall_audit = evaluate_authority_firewall(pure_anomalon_obj)

    return {
        "specimen1_class": res_specimen1.classification.value,
        "specimen1_distance": res_specimen1.quotient_distance,
        "specimen2_class": res_specimen2.classification.value,
        "specimen2_is_anomalon": res_specimen2.is_anomalon_terminal,
        "specimen2_distance": res_specimen2.quotient_distance,
        "specimen3_class": res_specimen3.classification.value,
        "specimen3_distance": res_specimen3.quotient_distance,
        "firewall_audit": firewall_audit,
    }
