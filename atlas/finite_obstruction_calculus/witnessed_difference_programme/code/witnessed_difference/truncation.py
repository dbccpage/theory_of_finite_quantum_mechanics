"""Weighted sums of forms and truncation leakage over Q and Q(i).

For maps A_a out of Q(i)^n and Hermitian weights W_a, H = sum_a A_a* W_a A_a.
With positive-definite weights, H is Hermitian positive semidefinite and
H psi = 0 exactly when every A_a psi = 0; a merely semidefinite weight can
break the equivalence, and an indefinite weight is refused.  For an orthogonal
projector P, P A* A P = (PAP)*(PAP) + L_P with L_P = ((1-P)AP)*((1-P)AP)
positive semidefinite; L_P = 0 exactly when ran P is A-invariant; and a reduced
zero psi = P psi with PAP psi = 0 is genuine (A psi = 0) exactly when
<psi, L_P psi> = 0.  Every positivity statement carries an exact congruence
certificate.  The leakage classifies no vector and interprets nothing
physically.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from .exact_linear import (
    CongruenceCertificate,
    ExactField,
    Matrix,
    Vector,
    add,
    adjoint,
    apply,
    coerce_matrix,
    coerce_vector,
    constant,
    diagonalize_hermitian,
    identity,
    inner,
    is_zero,
    kernel_basis,
    matmul,
    subtract,
    zero_matrix,
)
from .outcomes import Accepted, Outcome, RefusalCode, Refused

FIELD = ExactField.GAUSSIAN


@dataclass(frozen=True)
class WeightedFormOperator:
    dimension: int
    maps: tuple[Matrix, ...]
    weights: tuple[Matrix, ...]
    operator: Matrix
    weight_certificates: tuple[CongruenceCertificate, ...]
    operator_certificate: CongruenceCertificate

    @property
    def weights_positive_definite(self) -> bool:
        return all(certificate.positive_definite for certificate in self.weight_certificates)


def _form_operator(dimension: int, maps: tuple[Matrix, ...], weights: tuple[Matrix, ...]) -> Matrix:
    total = zero_matrix(dimension, dimension, FIELD)
    for a, w in zip(maps, weights):
        pulled = matmul(adjoint(a, dimension), matmul(w, a, dimension, FIELD), dimension, FIELD)
        total = add(total, pulled)
    return total


def weighted_form_operator(maps: Sequence[object], weights: Sequence[object], dimension: int) -> Outcome[WeightedFormOperator]:
    """H = sum_a A_a* W_a A_a for exact A_a: Q(i)^dimension -> Q(i)^m_a and Hermitian PSD W_a."""

    if type(dimension) is not int or dimension < 0:
        return Refused(RefusalCode.INVALID_INPUT, "the domain dimension must be a non-negative integer")
    if not isinstance(maps, (tuple, list)) or not isinstance(weights, (tuple, list)) or len(maps) != len(weights):
        return Refused(RefusalCode.INVALID_INPUT, "declare exactly one weight per map")
    admitted_maps, admitted_weights, certificates = [], [], []
    for index, (rows, weight_rows) in enumerate(zip(maps, weights)):
        a = coerce_matrix(rows, (None, dimension), FIELD)
        if isinstance(a, Refused):
            return a
        size = len(a.value)
        w = coerce_matrix(weight_rows, (size, size), FIELD)
        if isinstance(w, Refused):
            return w
        if adjoint(w.value, size) != w.value:
            return Refused(RefusalCode.NOT_HERMITIAN, f"weight {index} is not Hermitian")
        certificate = diagonalize_hermitian(w.value, FIELD)
        if not certificate.positive_semidefinite:
            return Refused(
                RefusalCode.NOT_POSITIVE_SEMIDEFINITE,
                f"weight {index} has negative energy on {certificate.negative_vector()!r}",
            )
        admitted_maps.append(a.value)
        admitted_weights.append(w.value)
        certificates.append(certificate)
    operator = _form_operator(dimension, tuple(admitted_maps), tuple(admitted_weights))
    return Accepted(
        WeightedFormOperator(
            dimension,
            tuple(admitted_maps),
            tuple(admitted_weights),
            operator,
            tuple(certificates),
            diagonalize_hermitian(operator, FIELD),
        )
    )


@dataclass(frozen=True)
class KernelComparison:
    operator_kernel: tuple[Vector, ...]
    component_kernel: tuple[Vector, ...]
    matches: bool
    weights_positive_definite: bool
    separating_vector: Vector | None


def kernel_matches_components(form: WeightedFormOperator) -> Outcome[KernelComparison]:
    """Compare ker H with the common kernel of the A_a; a mismatch carries a separating vector."""

    if not isinstance(form, WeightedFormOperator):
        return Refused(RefusalCode.INVALID_INPUT, "a weighted form operator is required")
    rebuilt = weighted_form_operator(form.maps, form.weights, form.dimension)
    if isinstance(rebuilt, Refused):
        return rebuilt
    if rebuilt.value.operator != form.operator:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the stored operator is not sum_a A_a* W_a A_a")
    size = form.dimension
    stacked = tuple(row for a in rebuilt.value.maps for row in a)
    operator_kernel = kernel_basis(form.operator, size, FIELD)
    component_kernel = kernel_basis(stacked, size, FIELD)
    zero = constant(FIELD, 0)
    separating = next(
        (vector for vector in operator_kernel if any(value != zero for value in apply(stacked, vector, FIELD))),
        None,
    )
    return Accepted(
        KernelComparison(
            operator_kernel,
            component_kernel,
            len(operator_kernel) == len(component_kernel),
            rebuilt.value.weights_positive_definite,
            separating,
        )
    )


def validate_projector(rows: object, dimension: int) -> Outcome[Matrix]:
    """Admit P only when P* = P and P P = P exactly."""

    admitted = coerce_matrix(rows, (dimension, dimension), FIELD)
    if isinstance(admitted, Refused):
        return admitted
    projector = admitted.value
    if adjoint(projector, dimension) != projector:
        return Refused(RefusalCode.NOT_ORTHOGONAL_PROJECTOR, "P is not self-adjoint")
    if matmul(projector, projector, dimension, FIELD) != projector:
        return Refused(RefusalCode.NOT_ORTHOGONAL_PROJECTOR, "P is not idempotent")
    return Accepted(projector)


@dataclass(frozen=True)
class TruncationLeakage:
    operator: Matrix
    projector: Matrix
    compression: Matrix
    compressed_energy: Matrix
    leakage: Matrix
    identity_holds: bool
    leakage_certificate: CongruenceCertificate
    leakage_free: bool
    range_invariant: bool


def _operator_and_projector(operator: object, projector: object) -> Outcome[tuple[Matrix, Matrix]]:
    rows = coerce_matrix(operator, (None, None), FIELD)
    if isinstance(rows, Refused):
        return rows
    size = len(rows.value)
    if any(len(row) != size for row in rows.value):
        return Refused(RefusalCode.INVALID_INPUT, "the operator must be square")
    p = validate_projector(projector, size)
    if isinstance(p, Refused):
        return p
    return Accepted((rows.value, p.value))


def _leak(a: Matrix, p: Matrix) -> tuple[Matrix, Matrix]:
    """(PAP, (1-P)AP)."""

    size = len(a)
    ap = matmul(a, p, size, FIELD)
    return matmul(p, ap, size, FIELD), matmul(subtract(identity(size, FIELD), p), ap, size, FIELD)


def truncation_leakage(operator: object, projector: object) -> Outcome[TruncationLeakage]:
    """Check P A* A P = (PAP)*(PAP) + L_P exactly and certify L_P positive semidefinite."""

    admitted = _operator_and_projector(operator, projector)
    if isinstance(admitted, Refused):
        return admitted
    a, p = admitted.value
    size = len(a)
    compression, leaked = _leak(a, p)
    energy = matmul(matmul(p, adjoint(a, size), size, FIELD), matmul(a, p, size, FIELD), size, FIELD)
    leakage = matmul(adjoint(leaked, size), leaked, size, FIELD)
    squared = matmul(adjoint(compression, size), compression, size, FIELD)
    return Accepted(
        TruncationLeakage(
            a,
            p,
            compression,
            energy,
            leakage,
            energy == add(squared, leakage),
            diagonalize_hermitian(leakage, FIELD),
            is_zero(leakage, FIELD),
            is_zero(leaked, FIELD),
        )
    )


@dataclass(frozen=True)
class ReducedZero:
    vector: Vector
    image: Vector
    leakage_energy: Fraction
    genuine: bool
    image_is_zero: bool
    leakage_free: bool


def reduced_zero_is_genuine(operator: object, projector: object, psi: object) -> Outcome[ReducedZero]:
    """For psi = P psi != 0 with PAP psi = 0, decide A psi = 0 by <psi, L_P psi> = 0."""

    admitted = _operator_and_projector(operator, projector)
    if isinstance(admitted, Refused):
        return admitted
    a, p = admitted.value
    vector = coerce_vector(psi, len(a), FIELD)
    if isinstance(vector, Refused):
        return vector
    psi_vector = vector.value
    zero = constant(FIELD, 0)
    if all(value == zero for value in psi_vector):
        return Refused(RefusalCode.INVALID_INPUT, "the zero vector is not a reduced zero")
    if apply(p, psi_vector, FIELD) != psi_vector:
        return Refused(RefusalCode.OUTSIDE_CARRIER, "psi does not lie in the range of P")
    compression, leaked = _leak(a, p)
    if any(value != zero for value in apply(compression, psi_vector, FIELD)):
        return Refused(RefusalCode.NOT_A_REDUCED_ZERO, "PAP psi is not zero")
    leakage = matmul(adjoint(leaked, len(a)), leaked, len(a), FIELD)
    energy = inner(psi_vector, apply(leakage, psi_vector, FIELD), FIELD).real
    image = apply(a, psi_vector, FIELD)
    return Accepted(
        ReducedZero(
            psi_vector,
            image,
            energy,
            energy == 0,
            all(value == zero for value in image),
            is_zero(leakage, FIELD),
        )
    )


def promote_truncation_zero(evidence: ReducedZero | TruncationLeakage, target: str) -> Refused:
    """A reduced zero or leakage record is finite linear algebra, never a physical zero-mode."""

    if not isinstance(evidence, (ReducedZero, TruncationLeakage)):
        return Refused(RefusalCode.INVALID_INPUT, "only truncation evidence can be examined for promotion")
    return Refused(
        RefusalCode.SCOPE_VIOLATION,
        f"{type(evidence).__name__} does not classify vectors and carries no Hamiltonian, energy, "
        f"zero-mode, probability-leak, or superspace interpretation: {target!r}",
    )


# Executable finite evidence; AuthorityEffect: None.
