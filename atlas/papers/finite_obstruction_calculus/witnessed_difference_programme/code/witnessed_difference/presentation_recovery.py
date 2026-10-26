"""Injectivity of a linear presentation on a declared subspace, and exact recovery bounds.

A presentation q: Q^N -> Q^M is injective on a declared subspace Y = span(V)
exactly when Y meets ker q only in 0; that needs M >= dim Y, and with fewer
report coordinates exact elimination exhibits a nonzero y in Y with q(y) = 0.
Every such kernel witness is re-verified before it is reported.  A Euclidean
recovery constant is certified exactly: ||q y||^2 >= t ||y||^2 on Y holds when
H - t G is positive semidefinite (H = (qV)^T (qV), G = V^T V), which an exact
congruence certificate decides; no floating-point eigenvector is trusted.  The
noisy bound ||y|| <= c (||q(y) + eta|| + epsilon) with c^2 = 1/t is checked
exactly by squaring.  Injectivity on Y detects nothing outside Y and selects,
prices, or authorizes no sensor suite.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import Sequence

from .exact import as_fraction
from .exact_linear import (
    CongruenceCertificate,
    ExactField,
    Matrix,
    Vector,
    adjoint,
    apply,
    coerce_matrix,
    coerce_vector,
    diagonalize_hermitian,
    inner,
    kernel_basis,
    matmul,
    rank,
    scale,
    subtract,
    verify_congruence,
)
from .outcomes import Accepted, Outcome, RefusalCode, Refused

FIELD = ExactField.RATIONAL
SUITE_BUDGET = 12


@dataclass(frozen=True)
class DeclaredPresentation:
    presentation: Matrix
    basis: Matrix
    ambient: int

    @property
    def dimension(self) -> int:
        return len(self.basis)

    @property
    def compressed(self) -> Matrix:
        """q V as an M x dim Y matrix."""

        return matmul(self.presentation, adjoint(self.basis, self.ambient), self.dimension, FIELD)


def declare_presentation(q_rows: object, basis: object) -> Outcome[DeclaredPresentation]:
    """Admit an exact q (M x N) and linearly independent basis vectors of Y in Q^N."""

    vectors = coerce_matrix(basis, (None, None), FIELD)
    if isinstance(vectors, Refused):
        return vectors
    if not vectors.value:
        return Refused(RefusalCode.INVALID_INPUT, "declare a nonzero subspace Y by at least one basis vector")
    ambient = len(vectors.value[0])
    if rank(vectors.value, ambient, FIELD) != len(vectors.value):
        return Refused(RefusalCode.INVALID_INPUT, "the declared basis vectors of Y are linearly dependent")
    rows = coerce_matrix(q_rows, (None, ambient), FIELD)
    if isinstance(rows, Refused):
        return rows
    return Accepted(DeclaredPresentation(rows.value, vectors.value, ambient))


def _in_subspace(declared: DeclaredPresentation, vector: Vector) -> bool:
    return rank(declared.basis + (vector,), declared.ambient, FIELD) == declared.dimension


def _format(vector: Vector) -> str:
    return "(" + ", ".join(str(value) for value in vector) + ")"


def verify_kernel_witness(q_rows: object, basis: object, witness: object) -> Outcome[Vector]:
    """Check that the witness is nonzero, lies in Y, and has q(y) = 0."""

    declared = declare_presentation(q_rows, basis)
    if isinstance(declared, Refused):
        return declared
    vector = coerce_vector(witness, declared.value.ambient, FIELD)
    if isinstance(vector, Refused):
        return vector
    y = vector.value
    if all(value == 0 for value in y):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the zero vector witnesses nothing")
    if not _in_subspace(declared.value, y):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the witness lies outside the declared subspace")
    if any(value != 0 for value in apply(declared.value.presentation, y, FIELD)):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the witness is not in the kernel of q")
    return Accepted(y)


def _kernel_candidate(declared: DeclaredPresentation) -> Vector | None:
    coefficients = kernel_basis(declared.compressed, declared.dimension, FIELD)
    if not coefficients:
        return None
    return apply(adjoint(declared.basis, declared.ambient), coefficients[0], FIELD)


def kernel_witness(q_rows: object, basis: object) -> Outcome[Vector]:
    """A verified nonzero y in Y with q(y) = 0; refused when q is injective on Y."""

    declared = declare_presentation(q_rows, basis)
    if isinstance(declared, Refused):
        return declared
    candidate = _kernel_candidate(declared.value)
    if candidate is None:
        return Refused(RefusalCode.NO_WITNESS, "q is injective on Y; Y meets ker q only in 0")
    return verify_kernel_witness(q_rows, basis, candidate)


@dataclass(frozen=True)
class InjectivityRecord:
    presentation: DeclaredPresentation
    report_coordinates: int
    dimension: int
    rank: int


def injective_on_subspace(q_rows: object, basis: object) -> Outcome[InjectivityRecord]:
    """Accept rank data when rank(qV) = dim Y; otherwise refuse with a verified kernel witness."""

    declared = declare_presentation(q_rows, basis)
    if isinstance(declared, Refused):
        return declared
    witness = kernel_witness(q_rows, basis)
    if isinstance(witness, Accepted):
        coordinates, dimension = len(declared.value.presentation), declared.value.dimension
        return Refused(
            RefusalCode.NOT_INJECTIVE,
            f"q is not injective on Y: y = {_format(witness.value)} is nonzero with q(y) = 0 "
            f"({coordinates} report coordinates for dim Y = {dimension})",
        )
    return Accepted(
        InjectivityRecord(
            declared.value, len(declared.value.presentation), declared.value.dimension, declared.value.dimension
        )
    )


@dataclass(frozen=True)
class RecoveryCertificate:
    """||q y||^2 >= threshold * ||y||^2 on Y, so ||y|| <= c ||q y|| with c^2 = 1/threshold."""

    presentation: DeclaredPresentation
    threshold: Fraction
    report_gram: Matrix
    subspace_gram: Matrix
    congruence: CongruenceCertificate

    @property
    def constant_squared(self) -> Fraction:
        return 1 / self.threshold


def _grams(declared: DeclaredPresentation, threshold: Fraction) -> tuple[Matrix, Matrix, Matrix]:
    compressed, k = declared.compressed, declared.dimension
    report = matmul(adjoint(compressed, k), compressed, k, FIELD)
    subspace = matmul(declared.basis, adjoint(declared.basis, declared.ambient), k, FIELD)
    return report, subspace, subtract(report, scale(subspace, threshold))


def _threshold(value: object) -> Fraction | None:
    try:
        threshold = as_fraction(value)  # type: ignore[arg-type]
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    return threshold if threshold > 0 else None


def euclidean_recovery_certificate(q_rows: object, basis: object, threshold: object) -> Outcome[RecoveryCertificate]:
    """Certify ||q y||_2^2 >= t ||y||_2^2 on Y exactly by H - t G being positive semidefinite."""

    declared = declare_presentation(q_rows, basis)
    if isinstance(declared, Refused):
        return declared
    t = _threshold(threshold)
    if t is None:
        return Refused(RefusalCode.INVALID_INPUT, "the recovery threshold must be an exact positive rational")
    report, subspace, difference = _grams(declared.value, t)
    certificate = diagonalize_hermitian(difference, FIELD)
    if not certificate.positive_semidefinite:
        coefficients = certificate.negative_vector()
        y = apply(adjoint(declared.value.basis, declared.value.ambient), coefficients, FIELD)  # type: ignore[arg-type]
        reported = apply(declared.value.presentation, y, FIELD)
        return Refused(
            RefusalCode.NOT_POSITIVE_SEMIDEFINITE,
            f"t = {t} is not certified: y = {_format(y)} has ||q y||^2 = {inner(reported, reported, FIELD)} "
            f"< t ||y||^2 = {t * inner(y, y, FIELD)}",
        )
    return Accepted(RecoveryCertificate(declared.value, t, report, subspace, certificate))


def verify_recovery_certificate(certificate: RecoveryCertificate) -> Outcome[RecoveryCertificate]:
    """Recompute both Gram matrices, the congruence, and its positivity."""

    if not isinstance(certificate, RecoveryCertificate) or not isinstance(
        certificate.presentation, DeclaredPresentation
    ):
        return Refused(RefusalCode.INVALID_INPUT, "not a recovery certificate")
    declared = declare_presentation(certificate.presentation.presentation, certificate.presentation.basis)
    if isinstance(declared, Refused):
        return declared
    if declared.value != certificate.presentation:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the stored presentation differs from its re-admitted form")
    t = _threshold(certificate.threshold)
    if t is None or type(certificate.threshold) is not Fraction:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the threshold is not an exact positive Fraction")
    report, subspace, difference = _grams(declared.value, t)
    if (report, subspace) != (certificate.report_gram, certificate.subspace_gram):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the stored Gram matrices differ from V^T q^T q V and V^T V")
    congruence = verify_congruence(certificate.congruence)
    if isinstance(congruence, Refused):
        return congruence
    if congruence.value.matrix != difference or not congruence.value.positive_semidefinite:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the congruence does not certify H - t G >= 0")
    return Accepted(certificate)


@dataclass(frozen=True)
class NoisyRecoveryRecord:
    vector: Vector
    report: Vector
    epsilon: Fraction
    noise_norm_squared: Fraction
    vector_norm_squared: Fraction
    report_norm_squared: Fraction
    constant_squared: Fraction
    bound_holds: bool


def noisy_recovery_bound(
    certificate: RecoveryCertificate,
    vector: object,
    report: object,
    epsilon: object,
) -> Outcome[NoisyRecoveryRecord]:
    """Check ||y|| <= c (||r|| + epsilon) exactly for r = q(y) + eta with ||eta|| <= epsilon."""

    verified = verify_recovery_certificate(certificate)
    if isinstance(verified, Refused):
        return verified
    declared = certificate.presentation
    y = coerce_vector(vector, declared.ambient, FIELD)
    r = coerce_vector(report, len(declared.presentation), FIELD)
    for outcome in (y, r):
        if isinstance(outcome, Refused):
            return outcome
    y_vector, r_vector = y.value, r.value  # type: ignore[union-attr]
    if not _in_subspace(declared, y_vector):
        return Refused(RefusalCode.OUTSIDE_CARRIER, "the recovered vector lies outside the declared subspace")
    try:
        bound = as_fraction(epsilon)  # type: ignore[arg-type]
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"the noise bound must be exact: {error}")
    noise = tuple(a - b for a, b in zip(r_vector, apply(declared.presentation, y_vector, FIELD)))
    noise_squared = inner(noise, noise, FIELD)
    if bound < 0 or noise_squared > bound * bound:
        return Refused(RefusalCode.OUT_OF_RANGE, f"||eta||^2 = {noise_squared} exceeds the declared epsilon^2")
    y_squared, r_squared = inner(y_vector, y_vector, FIELD), inner(r_vector, r_vector, FIELD)
    slack = certificate.threshold * y_squared - r_squared - bound * bound
    holds = slack <= 0 or 4 * bound * bound * r_squared >= slack * slack
    return Accepted(
        NoisyRecoveryRecord(
            y_vector, r_vector, bound, noise_squared, y_squared, r_squared, certificate.constant_squared, holds
        )
    )


@dataclass(frozen=True)
class SuiteCostRecord:
    """Exhaustive check of the scalar-probe cost bound on one declared probe family."""

    dimension: int
    cheapest_sound_cost: Fraction
    cheapest_sound_suite: tuple[int, ...]
    lower_bound: Fraction
    sound_suites: int
    bound_holds: bool


def suite_cost_lower_bound(probes: Sequence[object], costs: Sequence[object], basis: object) -> Outcome[SuiteCostRecord]:
    """With one scalar row per probe and positive costs, every sound suite costs at least
    the sum of the dim Y cheapest probe costs; checked over every subset of the family."""

    if not isinstance(probes, (tuple, list)) or not isinstance(costs, (tuple, list)) or len(probes) != len(costs):
        return Refused(RefusalCode.INVALID_INPUT, "declare exactly one cost per probe")
    if len(probes) > SUITE_BUDGET:
        return Refused(RefusalCode.BUDGET_EXHAUSTED, f"the subset census is budgeted to {SUITE_BUDGET} probes")
    rows = []
    for probe in probes:
        admitted = coerce_matrix(probe, (None, None), FIELD)
        if isinstance(admitted, Refused):
            return admitted
        if len(admitted.value) != 1:
            return Refused(
                RefusalCode.SCOPE_VIOLATION, "the cost bound is stated for probes contributing one scalar row each"
            )
        rows.append(admitted.value[0])
    prices = [_threshold(cost) for cost in costs]
    if any(price is None for price in prices):
        return Refused(RefusalCode.INVALID_INPUT, "probe costs must be exact positive rationals")
    declared = declare_presentation(tuple(rows), basis)
    if isinstance(declared, Refused):
        return declared
    k = declared.value.dimension
    sound = []
    for size in range(k, len(rows) + 1):
        for suite in combinations(range(len(rows)), size):
            chosen = declare_presentation(tuple(rows[index] for index in suite), basis).value  # type: ignore[union-attr]
            if _kernel_candidate(chosen) is None:
                sound.append((sum((prices[index] for index in suite), start=Fraction(0)), suite))  # type: ignore[misc]
    if not sound:
        return Refused(RefusalCode.INFEASIBLE, "no subset of the declared probes is injective on Y")
    cheapest, suite = min(sound)
    lower = sum(sorted(prices)[:k], start=Fraction(0))  # type: ignore[type-var]
    return Accepted(SuiteCostRecord(k, cheapest, suite, lower, len(sound), cheapest >= lower))


@dataclass(frozen=True)
class DetectionRecord:
    vector: Vector
    report: Vector
    detected: bool


def detection_scope(record: InjectivityRecord, vector: object) -> Outcome[DetectionRecord]:
    """Inside Y a nonzero input has a nonzero report; outside Y nothing is certified."""

    if not isinstance(record, InjectivityRecord) or not isinstance(record.presentation, DeclaredPresentation):
        return Refused(RefusalCode.INVALID_INPUT, "an injectivity record is required")
    declared = record.presentation
    rechecked = injective_on_subspace(declared.presentation, declared.basis)
    if isinstance(rechecked, Refused):
        return rechecked
    if rechecked.value != record:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the stored injectivity record differs from its recomputation")
    admitted = coerce_vector(vector, declared.ambient, FIELD)
    if isinstance(admitted, Refused):
        return admitted
    report = apply(declared.presentation, admitted.value, FIELD)
    silent = all(value == 0 for value in report)
    if not _in_subspace(declared, admitted.value):
        return Refused(
            RefusalCode.SCOPE_VIOLATION,
            f"{_format(admitted.value)} lies outside Y; injectivity on Y certifies no detection outside Y"
            + (" (the presentation reports zero)" if silent else ""),
        )
    return Accepted(DetectionRecord(admitted.value, report, not silent))


PRESENTATION_EVIDENCE = (InjectivityRecord, RecoveryCertificate, NoisyRecoveryRecord, SuiteCostRecord, DetectionRecord)


def promote_presentation_evidence(evidence: object, target: str) -> Refused:
    """Presentation evidence never certifies unmodeled detection or selects, prices, or authorizes a suite."""

    if not isinstance(evidence, PRESENTATION_EVIDENCE):
        return Refused(RefusalCode.INVALID_INPUT, "only presentation evidence can be examined for promotion")
    return Refused(
        RefusalCode.SCOPE_VIOLATION,
        f"{type(evidence).__name__} is finite linear-algebra evidence on a declared subspace; it does not detect "
        f"unmodeled or adversarial inputs and does not select, price, or authorize a sensor suite: {target!r}",
    )


# Executable finite evidence; AuthorityEffect: None.
