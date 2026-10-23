# -*- coding: utf-8 -*-
"""
coda_or_core.py: Enriched Comparison Envelope & Defect Classifier for CODA-OR.

Governing Claims (Omniversal Re-Presentation, v1.0 Pre-Print):
1. OR-D1 & OR-T1–T3: Overlap compatibility and pair gluing.
2. OR-D2 & OR-T4: Four-case square defect classification & exact repair closure:
   - StrictCommute (delta_square == 0)
   - WeakCommuteCertified (quotient distance Phi_1([delta]) == 0 via exact repair d0 alpha = delta)
   - H1DiagramTear (Phi_1([delta]) > 0, d1 delta == 0, closed diagram tear)
   - OpenDiagramObstruction (Phi_1([delta]) > 0, d1 delta != 0, open defect)
3. OR-D3 & OR-T5–T6: Standing of comparison object & non-creation firewall:
   - Sieve target and arrow targets must strictly bind to comparison object id.
   - Empty support sieve forces hard refusal R_empty_support.
   - Envelope membership does not confer authority: X in Omega_O not=> Auth(X).
4. OR-D4 & OR-T7–T8: Limit candidate standing & weak 2-terminal non-assumption:
   - Limit standing requires all valid legs and declared local terminalizer.
   - Global omniversal object is not assumed.
5. Exact Cochain Quotient Solver: LinearRepairProblem from local cochain_presentation.
6. Zero Floats Invariant: strictly exact rational arithmetic (sympy.Rational / fractions.Fraction).
   Floats, booleans, and sympy symbols passed in scalar positions strictly raise TypeError.
7. Defensive Immutability: EnrichedEnvironment and DiagramDefectResult store immutable
   exact matrices (sympy.ImmutableMatrix) to prevent mutable alias corruption.

AuthorityEffect: None unconditionally.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Any, List, Optional, Sequence, Tuple, Union

from cochain_presentation import (
    LinearRepairProblem,
    QuotientDistanceCertificate,
)
from sympy import ImmutableMatrix, Integer, Matrix, Rational
from sympy.matrices.matrixbase import MatrixBase

# Exact rational residual constants
RESIDUAL_EMPTY_SUPPORT = Rational(1, 1)
RESIDUAL_NO_TERMINALIZER = Rational(1, 2)
RESIDUAL_UNSTABILIZED = Rational(3, 4)
RESIDUAL_CLOSED_TEAR = Rational(1, 4)
RESIDUAL_SUCCESS = Rational(0, 1)

# Refusal codes
R_EMPTY_SUPPORT = "R_empty_support"
R_NO_TERMINALIZER = "R_no_terminalizer"
R_UNSUPPORTED_COMPONENT = "R_unsupported_component"
R_SILENT_MUTATION = "R_silent_mutation"
R_OPEN_OBSTRUCTION = "R_open_obstruction"


def _validate_declared_string(val: Any, name: str) -> str:
    """Ensure value is a declared non-empty string, rejecting booleans, empty strings, and non-strings."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be a declared non-empty string, got bool")
    if not isinstance(val, str):
        raise TypeError(f"{name} must be a string, got {type(val).__name__}")
    s = val.strip()
    if not s:
        raise ValueError(f"{name} must be a non-empty string")
    return s


def _validate_exact_rational(val: Any, name: str) -> Rational:
    """Ensure value is an exact rational or integer, rejecting floats, booleans, and sympy symbols."""
    if isinstance(val, bool) or getattr(val, "is_Boolean", False):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    val_dtype = getattr(val, "dtype", None)
    if isinstance(val, float) or (val_dtype is not None and "float" in str(val_dtype)):
        raise TypeError(f"{name} must be an exact rational or integer, got float (floats strictly forbidden)")
    if hasattr(val, "is_Float") and val.is_Float:
        raise TypeError(f"{name} must be an exact rational or integer, got SymPy Float (floats strictly forbidden)")
    if isinstance(val, (int, Integer, Fraction, Rational)):
        return Rational(val)
    if isinstance(val, str):
        s = val.strip()
        if not s:
            raise ValueError(f"{name} string cannot be empty")
        try:
            return Rational(s)
        except Exception as exc:
            raise TypeError(f"{name} string could not be converted to exact Rational: {exc}") from exc
    if hasattr(val, "free_symbols") and len(val.free_symbols) > 0:
        raise TypeError(f"{name} must be an exact rational or integer, got symbolic expression with free symbols: {val}")
    if hasattr(val, "is_rational") and val.is_rational:
        return Rational(val)
    raise TypeError(f"{name} must be an exact rational or integer, got {type(val).__name__}")


def _validate_exact_int(val: Any, name: str) -> int:
    """Ensure value is an exact non-negative integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an integer, got bool")
    val_dtype = getattr(val, "dtype", None)
    if not isinstance(val, (int, Integer)) or (val_dtype is not None and "float" in str(val_dtype)):
        raise TypeError(f"{name} must be an integer, got {type(val).__name__}")
    int_val = int(val)
    if int_val < 0:
        raise ValueError(f"{name} must be non-negative, got {int_val}")
    return int_val


class SquareStatus(str, Enum):
    """Four-case defect classification for comparison squares (OR-D2 / OR-T4)."""

    STRICT_COMMUTE = "StrictCommute"
    WEAK_COMMUTE_CERTIFIED = "WeakCommuteCertified"
    H1_DIAGRAM_TEAR = "H^1DiagramTear"
    OPEN_DIAGRAM_OBSTRUCTION = "OpenDiagramObstruction"


@dataclass(frozen=True)
class EnrichedEnvironment:
    """
    Declared enriched comparison environment E = (M, ||.||_1, d0, d1).
    Complex property: d1 * d0 = 0.
    Entries of d0 and d1 must be exact rationals.
    Stores immutable matrices to prevent post-construction mutation.
    """

    dim_c0: int
    dim_c1: int
    dim_c2: int
    d0: MatrixBase  # dim_c1 x dim_c0
    d1: MatrixBase  # dim_c2 x dim_c1
    name: str = "StandardEnrichedEnvironment"

    def __post_init__(self) -> None:
        _validate_exact_int(self.dim_c0, "dim_c0")
        _validate_exact_int(self.dim_c1, "dim_c1")
        _validate_exact_int(self.dim_c2, "dim_c2")

        if not isinstance(self.d0, MatrixBase) or not isinstance(self.d1, MatrixBase):
            raise TypeError("d0 and d1 must be sympy.Matrix instances")

        if self.d0.rows != self.dim_c1 or self.d0.cols != self.dim_c0:
            raise ValueError(f"d0 dimensions {self.d0.shape} must match ({self.dim_c1}, {self.dim_c0})")
        if self.d1.rows != self.dim_c2 or self.d1.cols != self.dim_c1:
            raise ValueError(f"d1 dimensions {self.d1.shape} must match ({self.dim_c2}, {self.dim_c1})")

        # Validate all entries of d0 and d1 as exact rationals
        d0_exact = Matrix(
            self.dim_c1,
            self.dim_c0,
            [
                _validate_exact_rational(self.d0[r, c], f"d0[{r},{c}]")
                for r in range(self.dim_c1)
                for c in range(self.dim_c0)
            ],
        )
        d1_exact = Matrix(
            self.dim_c2,
            self.dim_c1,
            [
                _validate_exact_rational(self.d1[r, c], f"d1[{r},{c}]")
                for r in range(self.dim_c2)
                for c in range(self.dim_c1)
            ],
        )

        # Complex condition: d1 * d0 == 0
        comp = d1_exact * d0_exact
        if not comp.is_zero_matrix:
            raise ValueError("Complex condition violated: d1 * d0 != 0")

        # Store immutable snapshots
        object.__setattr__(self, "d0", ImmutableMatrix(d0_exact))
        object.__setattr__(self, "d1", ImmutableMatrix(d1_exact))


@dataclass(frozen=True)
class DiagramDefectResult:
    """Result of classifying a diagram square defect under an enriched environment."""

    status: SquareStatus
    raw_defect: ImmutableMatrix
    quotient_distance: Rational
    boundary_image: ImmutableMatrix
    repair_2cell: Optional[ImmutableMatrix]
    is_closed: bool
    is_exact: bool


def classify_diagram_square(
    raw_defect: Union[MatrixBase, Sequence[Any]],
    env: EnrichedEnvironment,
) -> DiagramDefectResult:
    """
    Classify a comparison square defect delta_square into the 4 OR-D2 cases
    using exact cochain quotient presentation (LinearRepairProblem).
    """
    if isinstance(raw_defect, MatrixBase):
        matrix_defect = raw_defect
        if matrix_defect.cols != 1:
            if matrix_defect.rows == 1:
                matrix_defect = matrix_defect.T
            else:
                raise ValueError("raw_defect must be a column vector")
        elements = [
            _validate_exact_rational(matrix_defect[i, 0], f"raw_defect[{i}]")
            for i in range(matrix_defect.rows)
        ]
        vec = Matrix(elements)
    else:
        elements = [
            _validate_exact_rational(x, f"raw_defect_elem[{i}]")
            for i, x in enumerate(raw_defect)
        ]
        vec = Matrix(elements)

    if vec.rows != env.dim_c1:
        raise ValueError(f"raw_defect dimension {vec.rows} must match C^1 dimension {env.dim_c1}")

    vec_imm = ImmutableMatrix(vec)

    # Case 1: Strict commute (delta_square == 0 on the nose)
    if vec_imm.is_zero_matrix:
        zero_c2 = ImmutableMatrix(Matrix.zeros(env.dim_c2, 1))
        zero_c0 = ImmutableMatrix(Matrix.zeros(env.dim_c0, 1)) if env.dim_c0 > 0 else None
        return DiagramDefectResult(
            status=SquareStatus.STRICT_COMMUTE,
            raw_defect=vec_imm,
            quotient_distance=Rational(0, 1),
            boundary_image=zero_c2,
            repair_2cell=zero_c0,
            is_closed=True,
            is_exact=True,
        )

    # Compute d1 * delta
    d1_delta = env.d1 * vec_imm
    if d1_delta.is_zero_matrix is None:
        raise ValueError("Indeterminate closure test: d1 * delta cannot be determined to be zero or nonzero")
    is_closed = bool(d1_delta.is_zero_matrix is True)
    d1_delta_imm = ImmutableMatrix(d1_delta)

    # Solve quotient distance Phi_square([delta]) = inf_alpha ||delta - d0 alpha||_1
    if env.dim_c0 == 0:
        quotient_dist = sum(abs(Rational(vec_imm[i, 0])) for i in range(vec_imm.rows))
        repair_alpha_imm = None
        is_exact = False
    else:
        problem = LinearRepairProblem(repair_map_d0=env.d0)
        cert: QuotientDistanceCertificate = problem.quotient_l1_distance(cochain=vec_imm)
        quotient_dist = Rational(cert.distance)
        repair_alpha_imm = ImmutableMatrix(cert.repair_witness)
        is_exact = bool(quotient_dist == Rational(0, 1))

    if is_exact:
        return DiagramDefectResult(
            status=SquareStatus.WEAK_COMMUTE_CERTIFIED,
            raw_defect=vec_imm,
            quotient_distance=quotient_dist,
            boundary_image=d1_delta_imm,
            repair_2cell=repair_alpha_imm,
            is_closed=is_closed,
            is_exact=True,
        )
    elif is_closed:
        return DiagramDefectResult(
            status=SquareStatus.H1_DIAGRAM_TEAR,
            raw_defect=vec_imm,
            quotient_distance=quotient_dist,
            boundary_image=d1_delta_imm,
            repair_2cell=repair_alpha_imm,
            is_closed=True,
            is_exact=False,
        )
    else:
        return DiagramDefectResult(
            status=SquareStatus.OPEN_DIAGRAM_OBSTRUCTION,
            raw_defect=vec_imm,
            quotient_distance=quotient_dist,
            boundary_image=d1_delta_imm,
            repair_2cell=repair_alpha_imm,
            is_closed=False,
            is_exact=False,
        )


@dataclass(frozen=True)
class SupportArrow:
    """A certified arrow u: A -> X into comparison object X."""

    source_regime_id: str
    target_object_id: str
    source_has_authority: bool
    certificate_id: Optional[str] = None

    def __post_init__(self) -> None:
        _validate_declared_string(self.source_regime_id, "source_regime_id")
        _validate_declared_string(self.target_object_id, "target_object_id")
        if type(self.source_has_authority) is not bool:
            raise TypeError(f"source_has_authority must be an exact bool, got {type(self.source_has_authority).__name__}")
        if self.certificate_id is not None:
            _validate_declared_string(self.certificate_id, "certificate_id")

    def is_auth_supporting_for(self, target_id: str) -> bool:
        """Check if arrow validly supports the specified target."""
        return (
            self.target_object_id == target_id
            and self.source_has_authority is True
            and self.certificate_id is not None
        )


@dataclass(frozen=True)
class SupportSieve:
    """
    Authority-support sieve Supp_Auth(X) = {u: A -> X | A in Reg_chi, Auth(A), chi_u down}.
    Enforces target binding: every arrow must target target_object_id.
    """

    target_object_id: str
    arrows: Tuple[SupportArrow, ...] = ()

    def __post_init__(self) -> None:
        _validate_declared_string(self.target_object_id, "target_object_id")
        arrow_tuple = tuple(self.arrows)
        for i, arrow in enumerate(arrow_tuple):
            if not isinstance(arrow, SupportArrow):
                raise TypeError(f"arrows[{i}] must be a SupportArrow instance, got {type(arrow).__name__}")
            if arrow.target_object_id != self.target_object_id:
                raise ValueError(
                    f"Arrow target '{arrow.target_object_id}' does not match sieve target '{self.target_object_id}'"
                )
        object.__setattr__(self, "arrows", arrow_tuple)

    def is_empty(self) -> bool:
        """Sieve is empty if no incoming arrow is auth-supporting for this target."""
        return not any(
            arrow.is_auth_supporting_for(self.target_object_id)
            for arrow in self.arrows
        )

    def authorized_sources(self) -> List[str]:
        return [
            arrow.source_regime_id
            for arrow in self.arrows
            if arrow.is_auth_supporting_for(self.target_object_id)
        ]


@dataclass(frozen=True)
class ComparisonObject:
    """An object X in the comparison envelope Omega_O := Comp_W(Reg_chi)."""

    object_id: str
    weight_class: str
    support_sieve: SupportSieve
    descent_d: Optional[str] = None
    verifier_v: Optional[str] = None
    terminalizer_tau: Optional[str] = None

    def __post_init__(self) -> None:
        _validate_declared_string(self.object_id, "object_id")
        _validate_declared_string(self.weight_class, "weight_class")
        if not isinstance(self.support_sieve, SupportSieve):
            raise TypeError(f"support_sieve must be a SupportSieve, got {type(self.support_sieve).__name__}")
        if self.support_sieve.target_object_id != self.object_id:
            raise ValueError(
                f"support_sieve target '{self.support_sieve.target_object_id}' does not match object_id '{self.object_id}'"
            )
        if self.descent_d is not None:
            _validate_declared_string(self.descent_d, "descent_d")
        if self.verifier_v is not None:
            _validate_declared_string(self.verifier_v, "verifier_v")
        if self.terminalizer_tau is not None:
            _validate_declared_string(self.terminalizer_tau, "terminalizer_tau")


@dataclass(frozen=True)
class ComparisonAuthorityResult:
    """
    Authority verdict for an object in the comparison envelope.
    Enforces OR-T6 Non-Creation: Auth is NOT granted by envelope membership.
    AuthorityEffect: None unconditionally.
    """

    inhabited: bool
    refusal_code: Optional[str]
    residual_mass: Rational
    terminal_state: Optional[str]
    authority_effect: str = "None"


def evaluate_comparison_authority(
    obj: ComparisonObject,
    require_all_sources: bool = True,
) -> ComparisonAuthorityResult:
    """
    Evaluates authority for a comparison object X in Omega_O.
    OR-D3 / OR-T5: Empty support sieve forces hard refusal R_empty_support.
    OR-T6: Envelope membership does not imply authority.
    OR-T7: Missing terminalizer / invalid legs block authority.
    """
    if not isinstance(obj, ComparisonObject):
        raise TypeError(f"obj must be a ComparisonObject, got {type(obj).__name__}")

    # Defensive target binding check
    if obj.support_sieve.target_object_id != obj.object_id:
        raise ValueError(
            f"Target mismatch: sieve targets '{obj.support_sieve.target_object_id}' but object is '{obj.object_id}'"
        )

    # 1. Check support sieve
    if obj.support_sieve.is_empty():
        return ComparisonAuthorityResult(
            inhabited=False,
            refusal_code=R_EMPTY_SUPPORT,
            residual_mass=RESIDUAL_EMPTY_SUPPORT,
            terminal_state=f"refusal_empty_support_{obj.object_id}",
        )

    # 2. Check local terminalization and descent triplet (D, V, tau)
    if not (obj.descent_d and obj.verifier_v and obj.terminalizer_tau):
        return ComparisonAuthorityResult(
            inhabited=False,
            refusal_code=R_NO_TERMINALIZER,
            residual_mass=RESIDUAL_NO_TERMINALIZER,
            terminal_state=f"refusal_no_terminalizer_{obj.object_id}",
        )

    # 3. Component descent verification
    auth_sources = obj.support_sieve.authorized_sources()
    if require_all_sources and len(auth_sources) < len(obj.support_sieve.arrows):
        return ComparisonAuthorityResult(
            inhabited=False,
            refusal_code=R_UNSUPPORTED_COMPONENT,
            residual_mass=RESIDUAL_UNSTABILIZED,
            terminal_state=f"refusal_unsupported_component_{obj.object_id}",
        )

    return ComparisonAuthorityResult(
        inhabited=True,
        refusal_code=None,
        residual_mass=RESIDUAL_SUCCESS,
        terminal_state=f"term_certified_comparison_{obj.object_id}_{obj.terminalizer_tau}",
    )


class SilentMutationRefusal(Exception):
    """Raised when protected skeleton elements mutate without a declared loss ledger."""
    pass


@dataclass(frozen=True)
class ProtectedSkeleton:
    """Protected skeleton Skel_A. Any unledgered mutation raises SilentMutationRefusal."""

    skeleton_id: str
    elements: Tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_declared_string(self.skeleton_id, "skeleton_id")
        elem_tuple = tuple(self.elements)
        for i, el in enumerate(elem_tuple):
            _validate_declared_string(el, f"elements[{i}]")
        object.__setattr__(self, "elements", elem_tuple)

    def mutate(
        self,
        new_elements: Sequence[str],
        loss_ledger: Optional[str] = None,
    ) -> Tuple[ProtectedSkeleton, Optional[str]]:
        new_tuple = tuple(new_elements)
        for i, el in enumerate(new_tuple):
            _validate_declared_string(el, f"new_elements[{i}]")
        if new_tuple != self.elements:
            if not loss_ledger or not isinstance(loss_ledger, str) or not loss_ledger.strip() or isinstance(loss_ledger, bool):
                raise SilentMutationRefusal(
                    f"Skeleton {self.skeleton_id} mutated without declared non-empty LossLedger"
                )
            return ProtectedSkeleton(self.skeleton_id, new_tuple), loss_ledger.strip()
        return self, None


def reproduce_section_6a_worked_example() -> List[DiagramDefectResult]:
    """
    Reproduces the exact four rows of the Section 6A Worked Example table from coda_or.md.
    Environment: E = (M=Q, ||.||_1, d0, d1) with C^0 = C^1 = C^2 = Q.
    Square 1: StrictCommute (raw = 0)
    Square 2: WeakCommuteCertified (raw = 3, d0(t) = t, d1 = 0, dist = 0)
    Square 3: H^1DiagramTear (raw = 3, d0 = 0, d1 = 0, dist = 3, closed)
    Square 4: OpenDiagramObstruction (raw = 3, d0 = 0, d1 = id, dist = 3, d1 delta = 3 != 0)
    """
    # Square 1: Strict commute (dim_c0=1, dim_c1=1, dim_c2=1, d0=0, d1=0, raw=0)
    env1 = EnrichedEnvironment(
        dim_c0=1,
        dim_c1=1,
        dim_c2=1,
        d0=Matrix([[0]]),
        d1=Matrix([[0]]),
        name="Square1_Strict",
    )
    res1 = classify_diagram_square(Matrix([[0]]), env1)

    # Square 2: Exact repair (d0(t) = t, d1 = 0, raw = 3)
    env2 = EnrichedEnvironment(
        dim_c0=1,
        dim_c1=1,
        dim_c2=1,
        d0=Matrix([[1]]),
        d1=Matrix([[0]]),
        name="Square2_WeakCommuteCertified",
    )
    res2 = classify_diagram_square(Matrix([[3]]), env2)

    # Square 3: Closed residual / H^1 tear (d0 = 0, d1 = 0, raw = 3)
    env3 = EnrichedEnvironment(
        dim_c0=1,
        dim_c1=1,
        dim_c2=1,
        d0=Matrix([[0]]),
        d1=Matrix([[0]]),
        name="Square3_H1DiagramTear",
    )
    res3 = classify_diagram_square(Matrix([[3]]), env3)

    # Square 4: Open diagram obstruction (d0 = 0, d1 = id, raw = 3)
    env4 = EnrichedEnvironment(
        dim_c0=1,
        dim_c1=1,
        dim_c2=1,
        d0=Matrix([[0]]),
        d1=Matrix([[1]]),
        name="Square4_OpenDiagramObstruction",
    )
    res4 = classify_diagram_square(Matrix([[3]]), env4)

    return [res1, res2, res3, res4]
