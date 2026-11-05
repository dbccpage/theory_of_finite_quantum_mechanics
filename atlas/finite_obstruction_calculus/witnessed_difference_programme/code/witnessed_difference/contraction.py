"""Chain contractions over Q: validation, retraction defect, normalization, perturbation.

Convention.  A contraction of a finite cochain complex (C, d) onto (D, d_D)
consists of chain maps i: D -> C and r: C -> D with r i = 1_D and a map h of
degree -1 with 1_C - i r = d h + h d.  It is normalized when h i = 0, r h = 0,
and h h = 0; its retraction defect is epsilon = 1 - i r.

The retraction defect is a cocycle of the degree-zero window of the
endomorphism complex (d epsilon = epsilon d), so its class is ``ExactClass`` or
``ClosedResidual`` and never ``ActiveClosureFailure``; it is exact precisely
when ker r is acyclic.  The perturbation lemma is an imported standard result,
sign-corrected for this convention: with A = (1 + delta h)^-1 delta, the maps
d_D + r A i, i - h A i, r - r A h, h - h A h are computed exactly and the
result is re-validated; the formula is never trusted.  These are exact finite
instances, not a general proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from .exact import l1
from .exact_linear import (
    ExactField,
    Matrix,
    add,
    coerce_matrix,
    identity,
    inverse,
    is_zero,
    matmul,
    rank,
    solve,
    subtract,
)
from .obstruction import (
    DEFAULT_PIVOT_BUDGET,
    DiagnosticClass,
    MatrixQuotientCertificate,
    classify_signature,
    matrix_quotient_l1,
)
from .outcomes import Accepted, Outcome, RefusalCode, Refused

FIELD = ExactField.RATIONAL


def _labels(dims: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(degree for degree, size in enumerate(dims) for _ in range(size))


def _indices(dims: tuple[int, ...], degree: int) -> tuple[int, ...]:
    return tuple(index for index, label in enumerate(_labels(dims)) if label == degree)


def _homogeneous(matrix: Matrix, source: tuple[int, ...], target: tuple[int, ...], degree: int) -> bool:
    rows, columns = _labels(target), _labels(source)
    return all(
        entry == 0 or rows[x] == columns[y] + degree for x, row in enumerate(matrix) for y, entry in enumerate(row)
    )


def _mul(left: Matrix, right: Matrix, columns: int) -> Matrix:
    return matmul(left, right, columns, FIELD)


@dataclass(frozen=True)
class GradedComplex:
    """dims[k] = dim C^k for k = 0, ..., top; the basis is ordered by degree."""

    dims: tuple[int, ...]
    differential: Matrix

    @property
    def size(self) -> int:
        return sum(self.dims)


def make_total_complex(dims: tuple[int, ...], differential: object) -> Outcome[GradedComplex]:
    """Admit a total differential of degree +1 with d d = 0."""

    if type(dims) is not tuple or not dims or any(type(size) is not int or size < 0 for size in dims):
        return Refused(RefusalCode.INVALID_INPUT, "dims must be a nonempty tuple of non-negative integers")
    size = sum(dims)
    admitted = coerce_matrix(differential, (size, size), FIELD)
    if isinstance(admitted, Refused):
        return admitted
    d = admitted.value
    if not _homogeneous(d, dims, dims, 1):
        return Refused(RefusalCode.INVALID_INPUT, "the differential is not homogeneous of degree +1")
    if not is_zero(_mul(d, d, size), FIELD):
        return Refused(RefusalCode.NOT_A_DIFFERENTIAL, "d d is not zero")
    return Accepted(GradedComplex(dims, d))


def assemble_map(
    source_dims: tuple[int, ...],
    target_dims: tuple[int, ...],
    degree: int,
    blocks: Sequence[object],
) -> Outcome[Matrix]:
    """Assemble block k: source degree k -> target degree k + degree into one total matrix."""

    if type(degree) is not int or not isinstance(blocks, (tuple, list)) or len(blocks) != len(source_dims):
        return Refused(RefusalCode.INVALID_INPUT, "declare an integer degree and one block per source degree")
    source_offsets = [sum(source_dims[:k]) for k in range(len(source_dims))]
    target_offsets = [sum(target_dims[:k]) for k in range(len(target_dims))]
    total = [[Fraction(0)] * sum(source_dims) for _ in range(sum(target_dims))]
    for k, block in enumerate(blocks):
        landing = k + degree
        height = target_dims[landing] if 0 <= landing < len(target_dims) else 0
        admitted = coerce_matrix(block, (height, source_dims[k]), FIELD)
        if isinstance(admitted, Refused):
            return admitted
        for a, row in enumerate(admitted.value):
            for b, entry in enumerate(row):
                total[target_offsets[landing] + a][source_offsets[k] + b] = entry
    return Accepted(tuple(tuple(row) for row in total))


def make_complex(dims: tuple[int, ...], blocks: Sequence[object]) -> Outcome[GradedComplex]:
    """Admit a complex from per-degree blocks d^k: C^k -> C^(k+1), k = 0, ..., top - 1."""

    if type(dims) is not tuple or not isinstance(blocks, (tuple, list)) or len(blocks) != len(dims) - 1:
        return Refused(RefusalCode.INVALID_INPUT, "declare one differential block per degree below the top")
    assembled = assemble_map(dims, dims, 1, tuple(blocks) + ((),))
    if isinstance(assembled, Refused):
        return assembled
    return make_total_complex(dims, assembled.value)


def _readmit_complex(value: object) -> Outcome[GradedComplex]:
    if not isinstance(value, GradedComplex):
        return Refused(RefusalCode.INVALID_INPUT, "a graded complex is required")
    return make_total_complex(value.dims, value.differential)


def homology_dimensions(complex_: GradedComplex) -> Outcome[tuple[int, ...]]:
    """dim H^k = dim C^k - rank d^k - rank d^(k-1) over Q."""

    admitted = _readmit_complex(complex_)
    if isinstance(admitted, Refused):
        return admitted
    dims, d = admitted.value.dims, admitted.value.differential

    def block_rank(k: int) -> int:
        rows, columns = _indices(dims, k + 1), _indices(dims, k)
        return rank(tuple(tuple(d[x][y] for y in columns) for x in rows), len(columns), FIELD)

    return Accepted(tuple(dims[k] - block_rank(k) - block_rank(k - 1) for k in range(len(dims))))


@dataclass(frozen=True)
class Retract:
    big: GradedComplex
    small: GradedComplex
    inclusion: Matrix
    retraction: Matrix


def _retract(big: object, small: object, inclusion: object, retraction: object) -> Outcome[Retract]:
    c, e = _readmit_complex(big), _readmit_complex(small)
    for outcome in (c, e):
        if isinstance(outcome, Refused):
            return outcome
    c_complex, d_complex = c.value, e.value  # type: ignore[union-attr]
    if len(c_complex.dims) != len(d_complex.dims):
        return Refused(RefusalCode.INVALID_INPUT, "declare C and D on the same degree range (pad with zero dims)")
    n, m = c_complex.size, d_complex.size
    i = coerce_matrix(inclusion, (n, m), FIELD)
    r = coerce_matrix(retraction, (m, n), FIELD)
    for outcome in (i, r):
        if isinstance(outcome, Refused):
            return outcome
    i_map, r_map = i.value, r.value  # type: ignore[union-attr]
    if not (
        _homogeneous(i_map, d_complex.dims, c_complex.dims, 0) and _homogeneous(r_map, c_complex.dims, d_complex.dims, 0)
    ):
        return Refused(RefusalCode.INVALID_INPUT, "i and r must preserve degree")
    dc, dd = c_complex.differential, d_complex.differential
    if _mul(dc, i_map, m) != _mul(i_map, dd, m) or _mul(dd, r_map, n) != _mul(r_map, dc, n):
        return Refused(RefusalCode.NOT_CHAIN_MAP, "i or r does not commute with the differentials")
    if _mul(r_map, i_map, m) != identity(m, FIELD):
        return Refused(RefusalCode.NOT_A_RETRACTION, "r i is not the identity of D")
    return Accepted(Retract(c_complex, d_complex, i_map, r_map))


@dataclass(frozen=True)
class Contraction:
    big: GradedComplex
    small: GradedComplex
    inclusion: Matrix
    retraction: Matrix
    homotopy: Matrix


def validate_contraction(
    big: GradedComplex,
    small: GradedComplex,
    inclusion: object,
    retraction: object,
    homotopy: object,
) -> Outcome[Contraction]:
    """Chain maps i and r, r i = 1, h of degree -1, and 1 - i r = d h + h d, all exactly."""

    retract = _retract(big, small, inclusion, retraction)
    if isinstance(retract, Refused):
        return retract
    data = retract.value
    n = data.big.size
    admitted = coerce_matrix(homotopy, (n, n), FIELD)
    if isinstance(admitted, Refused):
        return admitted
    h, d = admitted.value, data.big.differential
    if not _homogeneous(h, data.big.dims, data.big.dims, -1):
        return Refused(RefusalCode.INVALID_INPUT, "the homotopy is not homogeneous of degree -1")
    if subtract(identity(n, FIELD), _mul(data.inclusion, data.retraction, n)) != add(_mul(d, h, n), _mul(h, d, n)):
        return Refused(RefusalCode.HOMOTOPY_MISMATCH, "1 - i r is not d h + h d")
    return Accepted(Contraction(data.big, data.small, data.inclusion, data.retraction, h))


def _readmit(contraction: object) -> Outcome[Contraction]:
    if not isinstance(contraction, Contraction):
        return Refused(RefusalCode.INVALID_INPUT, "a contraction is required")
    return validate_contraction(
        contraction.big, contraction.small, contraction.inclusion, contraction.retraction, contraction.homotopy
    )


@dataclass(frozen=True)
class NormalizationReport:
    hi_zero: bool
    rh_zero: bool
    hh_zero: bool

    @property
    def normalized(self) -> bool:
        return self.hi_zero and self.rh_zero and self.hh_zero


def is_normalized(contraction: Contraction) -> Outcome[NormalizationReport]:
    """Report h i = 0, r h = 0, and h h = 0 for a re-validated contraction."""

    checked = _readmit(contraction)
    if isinstance(checked, Refused):
        return checked
    c = checked.value
    n, m = c.big.size, c.small.size
    return Accepted(
        NormalizationReport(
            is_zero(_mul(c.homotopy, c.inclusion, m), FIELD),
            is_zero(_mul(c.retraction, c.homotopy, n), FIELD),
            is_zero(_mul(c.homotopy, c.homotopy, n), FIELD),
        )
    )


def normalize_homotopy(contraction: Contraction) -> Outcome[Contraction]:
    """h' = pi h pi with pi = 1 - i r, then h'' = h' d h'; the result is re-validated."""

    checked = _readmit(contraction)
    if isinstance(checked, Refused):
        return checked
    c = checked.value
    n = c.big.size
    projector = subtract(identity(n, FIELD), _mul(c.inclusion, c.retraction, n))
    first = _mul(_mul(projector, c.homotopy, n), projector, n)
    second = _mul(_mul(first, c.big.differential, n), first, n)
    return validate_contraction(c.big, c.small, c.inclusion, c.retraction, second)


@dataclass(frozen=True)
class RetractionDefect:
    """epsilon = 1 - i r, its closure data, and its class in the degree-zero endomorphism window."""

    defect: Matrix
    idempotent: bool
    commutes_with_differential: bool
    closure_mass: Fraction
    kernel_cohomology: tuple[int, ...]
    homotopy: Matrix | None
    class_certificate: MatrixQuotientCertificate
    diagnostic_class: DiagnosticClass

    @property
    def kernel_acyclic(self) -> bool:
        return not any(self.kernel_cohomology)

    @property
    def nullhomotopic(self) -> bool:
        return self.homotopy is not None


def _endomorphism_window(complex_: GradedComplex) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...], Matrix]:
    """Unknown entries of a degree -1 map h, degree-0 equations, and the matrix of h -> d h + h d."""

    labels, d = _labels(complex_.dims), complex_.differential
    size = len(labels)
    unknowns = tuple((a, b) for a in range(size) for b in range(size) if labels[a] == labels[b] - 1)
    equations = tuple((x, y) for x in range(size) for y in range(size) if labels[x] == labels[y])
    zero = Fraction(0)
    rows = tuple(
        tuple((d[x][a] if b == y else zero) + (d[b][y] if a == x else zero) for a, b in unknowns)
        for x, y in equations
    )
    return unknowns, equations, rows


def retraction_defect(
    big: GradedComplex,
    small: GradedComplex,
    inclusion: object,
    retraction: object,
    *,
    max_pivots: int = DEFAULT_PIVOT_BUDGET,
) -> Outcome[RetractionDefect]:
    """For chain maps with r i = 1: idempotence, closure, kernel cohomology, and the exact class of epsilon.

    The class value is Phi = min_h ||epsilon - (d h + h d)||_1 over the degree-zero window of the
    endomorphism complex, with a verified primal-dual certificate; the closure mass is
    ||d epsilon - epsilon d||_1.
    """

    retract = _retract(big, small, inclusion, retraction)
    if isinstance(retract, Refused):
        return retract
    data = retract.value
    n, d = data.big.size, data.big.differential
    projection = _mul(data.inclusion, data.retraction, n)
    epsilon = subtract(identity(n, FIELD), projection)
    closure = subtract(_mul(d, epsilon, n), _mul(epsilon, d, n))
    image = _mul(d, epsilon, n)
    dims = data.big.dims

    def column_rank(matrix: Matrix, degree: int) -> int:
        columns = _indices(dims, degree)
        return rank(tuple(tuple(row[y] for y in columns) for row in matrix), len(columns), FIELD)

    cohomology = tuple(
        column_rank(epsilon, k) - column_rank(image, k) - column_rank(image, k - 1) for k in range(len(dims))
    )
    unknowns, equations, window = _endomorphism_window(data.big)
    target = tuple(epsilon[x][y] for x, y in equations)
    solution = solve(window, target, len(unknowns), FIELD)
    homotopy = None
    if solution is not None:
        entries = dict(zip(unknowns, solution))
        homotopy = tuple(tuple(entries.get((a, b), Fraction(0)) for b in range(n)) for a in range(n))
    certified = matrix_quotient_l1(window, target, columns=len(unknowns), max_pivots=max_pivots)
    if isinstance(certified, Refused):
        return certified
    closure_mass = l1(entry for row in closure for entry in row)
    return Accepted(
        RetractionDefect(
            epsilon,
            _mul(projection, projection, n) == projection,
            is_zero(closure, FIELD),
            closure_mass,
            cohomology,
            homotopy,
            certified.value,
            classify_signature(certified.value.value, closure_mass),
        )
    )


def perturb(contraction: Contraction, perturbation: object) -> Outcome[Contraction]:
    """Sign-corrected perturbation lemma with re-validation of every produced map.

    A = (1 + delta h)^-1 delta, d_D' = d_D + r A i, i' = i - h A i,
    r' = r - r A h, h' = h - h A h, on the perturbed complex (C, d + delta).
    The lemma assumes a normalized contraction and yields one; both ends are checked.
    """

    report = is_normalized(contraction)
    if isinstance(report, Refused):
        return report
    if not report.value.normalized:
        return Refused(
            RefusalCode.SCOPE_VIOLATION,
            "the perturbation lemma is stated for normalized contractions; normalize the homotopy first",
        )
    c = _readmit(contraction).value  # type: ignore[union-attr]
    n, m = c.big.size, c.small.size
    admitted = coerce_matrix(perturbation, (n, n), FIELD)
    if isinstance(admitted, Refused):
        return admitted
    delta = admitted.value
    if not _homogeneous(delta, c.big.dims, c.big.dims, 1):
        return Refused(RefusalCode.INVALID_INPUT, "the perturbation is not homogeneous of degree +1")
    big = make_total_complex(c.big.dims, add(c.big.differential, delta))
    if isinstance(big, Refused):
        return big
    twisted = inverse(add(identity(n, FIELD), _mul(delta, c.homotopy, n)), FIELD)
    if twisted is None:
        return Refused(RefusalCode.NOT_INVERTIBLE, "1 + delta h is singular; the perturbation is not small")
    a = _mul(twisted, delta, n)
    ai, ah = _mul(a, c.inclusion, m), _mul(a, c.homotopy, n)
    small = make_total_complex(c.small.dims, add(c.small.differential, _mul(c.retraction, ai, m)))
    inclusion = subtract(c.inclusion, _mul(c.homotopy, ai, m))
    retraction = subtract(c.retraction, _mul(c.retraction, ah, n))
    homotopy = subtract(c.homotopy, _mul(c.homotopy, ah, n))
    revalidated = small if isinstance(small, Refused) else validate_contraction(
        big.value, small.value, inclusion, retraction, homotopy
    )
    if isinstance(revalidated, Refused):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, f"the perturbed data fail re-validation: {revalidated.detail}")
    report = is_normalized(revalidated.value)
    if isinstance(report, Refused) or not report.value.normalized:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the perturbed contraction is not normalized")
    return revalidated


# Executable finite evidence; AuthorityEffect: None.
