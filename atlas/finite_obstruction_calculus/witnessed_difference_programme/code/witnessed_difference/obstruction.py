"""Exact degree-1 obstruction windows, quotient norms, and dual certificates.

Quotient proposals are solved in native Rust and evaluated by omega_functional.
A quotient certificate carries a primal potential and a dual circulation; its
value and verification both come from that canonical evaluator.  A diagnostic class is a finite classification of
one declared window; it is not a routing terminal, a repair action, a
stabilization receipt, or authority.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Hashable, Iterable, Mapping, Sequence

from .cochains import Edge, FiniteComplex, Vertex, _edge_value, _validate_cochain
from .exact import as_fraction, l1
from .outcomes import Accepted, AuthorityEffect, Outcome, RefusalCode, Refused
from .native_functionals import (
    CertificateMismatchError,
    FunctionalEvaluationError,
    NativeProtocolError,
    NativeTimeoutError,
    NativeUnavailableError,
    closure,
    decode,
    encode,
    evaluate,
)

Matrix = tuple[tuple[Fraction, ...], ...]
DEFAULT_PIVOT_BUDGET = 10_000
ROUTING_TERMINALS = frozenset(
    {
        "BudgetUnknown",
        "CheckPassed",
        "ExactRepair",
        "NoRule",
        "OpenObstruction",
        "Refusal",
        "Refused",
        "Repair",
        "RequiresLift",
        "StabilizedSurvivor",
    }
)


def evaluation_preorder(
    vertices: Sequence[Hashable],
    relation: Iterable[tuple[Hashable, Hashable]],
) -> Outcome[frozenset[tuple[Hashable, Hashable]]]:
    """Return the reflexive-transitive closure of a declared finite comparison."""

    carrier = tuple(vertices)
    if len(set(carrier)) != len(carrier):
        return Refused(RefusalCode.INVALID_INPUT, "the evaluation carrier must list each state once")
    successors: dict[Hashable, set[Hashable]] = {vertex: set() for vertex in carrier}
    for pair in relation:
        if type(pair) is not tuple or len(pair) != 2:
            return Refused(RefusalCode.INVALID_INPUT, "a comparison relation contains ordered pairs")
        if pair[0] not in successors or pair[1] not in successors:
            return Refused(RefusalCode.OUTSIDE_CARRIER, f"comparison {pair!r} leaves the declared carrier")
        successors[pair[0]].add(pair[1])
    closure: set[tuple[Hashable, Hashable]] = set()
    for start in carrier:
        reached = {start}
        queue: deque[Hashable] = deque([start])
        while queue:
            for target in successors[queue.popleft()]:
                if target not in reached:
                    reached.add(target)
                    queue.append(target)
        closure.update((start, target) for target in reached)
    return Accepted(frozenset(closure))


def d0_matrix(complex_: FiniteComplex) -> Matrix:
    """Rows are edges, columns are vertices: (d0 f)(u, v) = f(v) - f(u)."""

    position = {vertex: index for index, vertex in enumerate(complex_.vertices)}
    rows = []
    for tail, head in complex_.edges:
        row = [Fraction(0)] * len(complex_.vertices)
        row[position[head]] += 1
        row[position[tail]] -= 1
        rows.append(tuple(row))
    return tuple(rows)


def d1_matrix(complex_: FiniteComplex) -> Matrix:
    """Rows are faces, columns are edges: face (a, b, c) has boundary ab + bc - ac."""

    position = {edge: index for index, edge in enumerate(complex_.edges)}
    rows = []
    for a, b, c in complex_.faces:
        row = [Fraction(0)] * len(complex_.edges)
        for (tail, head), sign in (((a, b), 1), ((b, c), 1), ((a, c), -1)):
            if (tail, head) in position:
                row[position[(tail, head)]] += sign
            else:
                row[position[(head, tail)]] -= sign
        rows.append(tuple(row))
    return tuple(rows)


def matrix_product(left: Matrix, right: Matrix, columns: int) -> Matrix:
    """Exact product of a p x q and a q x ``columns`` matrix."""

    return tuple(
        tuple(
            sum((entry * right[k][j] for k, entry in enumerate(row)), start=Fraction(0))
            for j in range(columns)
        )
        for row in left
    )


@dataclass(frozen=True)
class DegreeOneWindow:
    """A degree-1 window C0 -> C1 -> C2 with its d1 o d0 = 0 certificate."""

    complex_: FiniteComplex
    d0: Matrix
    d1: Matrix
    composite: Matrix


def degree_one_window(complex_: FiniteComplex) -> Outcome[DegreeOneWindow]:
    if not isinstance(complex_, FiniteComplex):
        return Refused(RefusalCode.INVALID_INPUT, "a degree-1 window needs a finite complex")
    first, second = d0_matrix(complex_), d1_matrix(complex_)
    composite = matrix_product(second, first, len(complex_.vertices))
    if any(entry != 0 for row in composite for entry in row):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "d1 o d0 is not zero on this window")
    return Accepted(DegreeOneWindow(complex_, first, second, composite))


def _exact(value: object) -> Fraction | None:
    try:
        return as_fraction(value)  # type: ignore[arg-type]
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def _exact_vector(values: object) -> tuple[Fraction, ...] | None:
    if isinstance(values, (str, bytes, Mapping)) or not isinstance(values, Sequence):
        return None
    converted = tuple(_exact(value) for value in values)
    if any(value is None for value in converted):
        return None
    return converted  # type: ignore[return-value]


def _exact_matrix(rows: object, columns: int | None) -> Matrix | None:
    if isinstance(rows, (str, bytes, Mapping)) or not isinstance(rows, Sequence):
        return None
    converted = tuple(_exact_vector(row) for row in rows)
    if any(row is None for row in converted):
        return None
    widths = {len(row) for row in converted}  # type: ignore[arg-type]
    if columns is not None:
        widths.add(columns)
    if len(widths) > 1:
        return None
    return converted  # type: ignore[return-value]


@dataclass(frozen=True)
class LinearProgramSolution:
    """x >= 0 with Ax = b, and y with A^T y <= c and b.y = c.x = value."""

    primal: tuple[Fraction, ...]
    dual: tuple[Fraction, ...]
    value: Fraction
    pivots: int


def verify_standard_lp(costs, matrix, rhs, solution: LinearProgramSolution) -> bool:
    """Independent exact primal/dual replay against the actual LP inputs."""
    c, b = _exact_vector(costs), _exact_vector(rhs)
    a = _exact_matrix(matrix, None if c is None else len(c))
    if c is None or b is None or a is None or len(a) != len(b):
        return False
    if not isinstance(solution, LinearProgramSolution):
        return False
    x, y = solution.primal, solution.dual
    if (not _is_vector(x) or not _is_vector(y) or type(solution.value) is not Fraction
            or len(x) != len(c) or len(y) != len(b) or any(v < 0 for v in x)):
        return False
    def dot(u, v):
        return sum((p * q for p, q in zip(u, v)), start=Fraction(0))

    return (all(dot(row, x) == value for row, value in zip(a, b))
            and all(sum((row[j] * v for row, v in zip(a, y)), start=Fraction(0)) <= c[j]
                    for j in range(len(c)))
            and dot(c, x) == dot(b, y) == solution.value)


def _pivot(tableau: list[list[Fraction]], row: int, column: int) -> None:
    scale = tableau[row][column]
    tableau[row] = [entry / scale for entry in tableau[row]]
    for index, other in enumerate(tableau):
        factor = other[column]
        if index != row and factor != 0:
            tableau[index] = [a - factor * b for a, b in zip(other, tableau[row])]


def _simplex(tableau: list[list[Fraction]], basis: list[int], eligible: int, budget: int) -> tuple[str, int]:
    """Bland's rule: least-index entering column, least-index basic variable on ratio ties."""

    rhs = len(tableau[0]) - 1
    pivots = 0
    while True:
        entering = next((j for j in range(eligible) if tableau[0][j] < 0), None)
        if entering is None:
            return "optimal", pivots
        ratios = [
            (tableau[i][rhs] / tableau[i][entering], basis[i - 1], i)
            for i in range(1, len(tableau))
            if tableau[i][entering] > 0
        ]
        if not ratios:
            return "unbounded", pivots
        if pivots >= budget:
            return "budget", pivots
        leaving = min(ratios)[2]
        _pivot(tableau, leaving, entering)
        basis[leaving - 1] = entering
        pivots += 1


_SIMPLEX_REFUSALS = {
    "unbounded": Refused(RefusalCode.UNBOUNDED, "the linear programme is unbounded below"),
    "budget": Refused(RefusalCode.BUDGET_EXHAUSTED, "the declared pivot budget was exhausted"),
}


def solve_standard_lp(
    costs: Sequence[int | str | Fraction],
    matrix: Sequence[Sequence[int | str | Fraction]],
    rhs: Sequence[int | str | Fraction],
    *,
    max_pivots: int = DEFAULT_PIVOT_BUDGET,
) -> Outcome[LinearProgramSolution]:
    """Minimize c.x subject to Ax = b and x >= 0 by exact two-phase simplex."""

    c = _exact_vector(costs)
    b = _exact_vector(rhs)
    a = _exact_matrix(matrix, None if c is None else len(c))
    if c is None or b is None or a is None or len(a) != len(b):
        return Refused(RefusalCode.INVALID_INPUT, "the programme needs exact data of matching shape")
    if type(max_pivots) is not int or max_pivots < 0:
        return Refused(RefusalCode.INVALID_INPUT, "the pivot budget must be a non-negative integer")
    m, n = len(a), len(c)
    signs = [Fraction(-1) if value < 0 else Fraction(1) for value in b]
    tableau = [[Fraction(0)] * (n + m + 1) for _ in range(m + 1)]
    for i in range(m):
        tableau[i + 1][:n] = [signs[i] * entry for entry in a[i]]
        tableau[i + 1][n + i] = Fraction(1)
        tableau[i + 1][n + m] = signs[i] * b[i]
    for j in range(n):
        tableau[0][j] = -sum((tableau[i + 1][j] for i in range(m)), start=Fraction(0))
    tableau[0][n + m] = -sum((tableau[i + 1][n + m] for i in range(m)), start=Fraction(0))
    basis = [n + i for i in range(m)]
    status, used = _simplex(tableau, basis, n, max_pivots)
    if status != "optimal":
        return _SIMPLEX_REFUSALS[status]
    if tableau[0][n + m] != 0:
        return Refused(RefusalCode.INFEASIBLE, f"phase one leaves artificial mass {-tableau[0][n + m]}")
    for i in range(1, m + 1):
        column = next((j for j in range(n) if basis[i - 1] >= n and tableau[i][j] != 0), None)
        if column is not None:
            if used >= max_pivots:
                return _SIMPLEX_REFUSALS["budget"]
            used += 1
            _pivot(tableau, i, column)
            basis[i - 1] = column
    kept = [i for i in range(1, m + 1) if basis[i - 1] < n]
    phase_two = [list(c) + [Fraction(0)] * (m + 1)] + [tableau[i][:] for i in kept]
    basis_two = [basis[i - 1] for i in kept]
    for row, variable in enumerate(basis_two, start=1):
        cost = phase_two[0][variable]
        phase_two[0] = [x - cost * y for x, y in zip(phase_two[0], phase_two[row])]
    status, more = _simplex(phase_two, basis_two, n, max_pivots - used)
    if status != "optimal":
        return _SIMPLEX_REFUSALS[status]
    primal = [Fraction(0)] * n
    for row, variable in enumerate(basis_two, start=1):
        primal[variable] = phase_two[row][n + m]
    dual = tuple(-signs[i] * phase_two[0][n + i] for i in range(m))
    solution = LinearProgramSolution(tuple(primal), dual, -phase_two[0][n + m], used + more)
    if not verify_standard_lp(c, a, b, solution):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "independent primal/dual replay failed")
    return Accepted(solution)


@dataclass(frozen=True)
class MatrixQuotientCertificate:
    """min over f of sum_i w_i |delta_i - (D f)_i| with a primal and a dual witness."""

    matrix: Matrix
    columns: int
    delta: tuple[Fraction, ...]
    weights: tuple[Fraction, ...]
    potential: tuple[Fraction, ...]
    residual: tuple[Fraction, ...]
    value: Fraction
    dual: tuple[Fraction, ...]


def _apply(matrix: Matrix, vector: Sequence[Fraction]) -> tuple[Fraction, ...]:
    return tuple(sum((a * b for a, b in zip(row, vector)), start=Fraction(0)) for row in matrix)


def _transpose_apply(matrix: Matrix, vector: Sequence[Fraction], columns: int) -> tuple[Fraction, ...]:
    return tuple(
        sum((row[j] * value for row, value in zip(matrix, vector)), start=Fraction(0))
        for j in range(columns)
    )


def _is_vector(value: object) -> bool:
    return type(value) is tuple and all(type(item) is Fraction for item in value)


def _exact_fields(value: object, vectors: tuple[object, ...], matrix: object = ()) -> bool:
    """Certificates are checked intact: flat tuples of Fractions, never coerced."""

    return (
        type(value) is Fraction
        and all(_is_vector(vector) for vector in vectors)
        and type(matrix) is tuple
        and all(_is_vector(row) for row in matrix)  # type: ignore[union-attr]
    )


def verify_matrix_certificate(cert: MatrixQuotientCertificate) -> Outcome[MatrixQuotientCertificate]:
    """Recompute residual, primal value, dual feasibility, and the duality equation."""

    if not isinstance(cert, MatrixQuotientCertificate) or type(cert.columns) is not int:
        return Refused(RefusalCode.INVALID_INPUT, "not a matrix quotient certificate")
    vectors = (cert.delta, cert.weights, cert.potential, cert.residual, cert.dual)
    if not _exact_fields(cert.value, vectors, cert.matrix):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "certificate entries must be exact Fractions")
    rows = len(cert.matrix)
    if (
        any(len(row) != cert.columns for row in cert.matrix)
        or len(cert.potential) != cert.columns
        or {len(cert.delta), len(cert.weights), len(cert.residual), len(cert.dual)} != {rows}
    ):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "certificate shapes do not match")
    if any(weight <= 0 for weight in cert.weights):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "weights must be positive")
    try:
        result = evaluate({
            "operation": "verify_phi1", "columns": cert.columns,
            "matrix": [[encode(x) for x in row] for row in cert.matrix],
            "delta": [encode(x) for x in cert.delta],
            "weights": [encode(x) for x in cert.weights],
            "potential": [encode(x) for x in cert.potential],
            "residual": [encode(x) for x in cert.residual],
            "dual": [encode(x) for x in cert.dual], "value": encode(cert.value),
        })
        if decode(result.get("value")) != cert.value:
            return Refused(RefusalCode.CERTIFICATE_MISMATCH, "native verification changed the claimed value")
    except NativeUnavailableError as error:
        return Refused(RefusalCode.NO_RULE, str(error))
    except NativeTimeoutError as error:
        return Refused(RefusalCode.BUDGET_EXHAUSTED, str(error))
    except NativeProtocolError as error:
        return Refused(RefusalCode.GRAMMAR_VIOLATION, str(error))
    except (CertificateMismatchError, FunctionalEvaluationError) as error:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, str(error))
    return Accepted(cert)


def matrix_quotient_l1(
    matrix: Sequence[Sequence[int | str | Fraction]],
    delta: Sequence[int | str | Fraction],
    weights: Sequence[int | str | Fraction] | None = None,
    *,
    columns: int | None = None,
    max_pivots: int = DEFAULT_PIVOT_BUDGET,
) -> Outcome[MatrixQuotientCertificate]:
    """Exact weighted l1 distance from ``delta`` to the column space of ``matrix``."""

    if columns is not None and (type(columns) is not int or columns < 0):
        return Refused(RefusalCode.INVALID_INPUT, "the declared column count must be a non-negative integer")
    d = _exact_matrix(matrix, columns)
    target = _exact_vector(delta)
    if d is None or target is None or len(d) != len(target):
        return Refused(RefusalCode.INVALID_INPUT, "quotient data must be exact and shape-consistent")
    width = len(d[0]) if d else (columns or 0)
    w = (Fraction(1),) * len(d) if weights is None else _exact_vector(weights)
    if w is None or len(w) != len(d) or any(value <= 0 for value in w):
        return Refused(RefusalCode.INVALID_INPUT, "weights must be exact, positive, and one per row")
    if type(max_pivots) is not int or max_pivots < 0:
        return Refused(RefusalCode.INVALID_INPUT, "pivot budget must be a nonnegative integer")
    try:
        result = evaluate({
            "operation": "solve_phi1", "columns": width, "max_pivots": max_pivots,
            "matrix": [[encode(x) for x in row] for row in d],
            "delta": [encode(x) for x in target], "weights": [encode(x) for x in w],
        })
        vectors = []
        for name, size in (("potential", width), ("residual", len(d)), ("dual", len(d))):
            raw = result.get(name)
            if type(raw) is not list or len(raw) != size:
                raise FunctionalEvaluationError("native certificate shape mismatch")
            vectors.append(tuple(decode(x) for x in raw))
        potential, residual, dual = vectors
        cert = MatrixQuotientCertificate(d, width, target, w, potential, residual,
                                         decode(result.get("value")), dual)
    except FunctionalEvaluationError as error:
        code = RefusalCode.BUDGET_EXHAUSTED if "budget" in str(error) else RefusalCode.NO_RULE
        return Refused(code, str(error))
    return verify_matrix_certificate(cert)


@dataclass(frozen=True)
class QuotientCertificate:
    """Graph certificate aligned with ``complex_.vertices`` and ``complex_.edges``."""

    complex_: FiniteComplex
    cochain: tuple[Fraction, ...]
    weights: tuple[Fraction, ...]
    potential: tuple[Fraction, ...]
    residual: tuple[Fraction, ...]
    value: Fraction
    dual: tuple[Fraction, ...]


def _cochain_vector(complex_: FiniteComplex, cochain: Mapping[Edge, object]) -> Outcome[tuple[Fraction, ...]]:
    try:
        _validate_cochain(complex_, cochain)
        return Accepted(tuple(_edge_value(cochain, *edge) for edge in complex_.edges))  # type: ignore[arg-type]
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"invalid edge cochain: {error}")


def edge_weights(
    complex_: FiniteComplex,
    weights: Mapping[Edge, int | str | Fraction] | None,
) -> Outcome[tuple[Fraction, ...]]:
    """Positive exact edge weights aligned with ``complex_.edges``; default 1."""

    if weights is None:
        return Accepted((Fraction(1),) * len(complex_.edges))
    try:
        _validate_cochain(complex_, weights)
        values = tuple(
            as_fraction(weights[(u, v)] if (u, v) in weights else weights[(v, u)])
            for u, v in complex_.edges
        )
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"invalid edge weights: {error}")
    if any(value <= 0 for value in values):
        return Refused(RefusalCode.INVALID_INPUT, "edge weights must be positive")
    return Accepted(values)


def d0_adjoint(complex_: FiniteComplex, edge_values: Mapping[Edge, int | str | Fraction]) -> dict[Vertex, Fraction]:
    """(d0* x)(v) = sum of x on edges into v minus sum of x on edges out of v."""

    _validate_cochain(complex_, edge_values)
    divergence = {vertex: Fraction(0) for vertex in complex_.vertices}
    for tail, head in complex_.edges:
        value = _edge_value(edge_values, tail, head)
        divergence[head] += value
        divergence[tail] -= value
    return divergence


def d1_operator_norm_1to1(complex_: FiniteComplex) -> Fraction:
    """max over edges of the sum over faces of |d1 coefficient|; zero without faces."""

    return max((l1(column) for column in zip(*d1_matrix(complex_))), default=Fraction(0))


def verify_quotient_certificate(cert: QuotientCertificate) -> Outcome[QuotientCertificate]:
    """Independently recompute the graph residual, value, dual bounds, and divergence."""

    if not isinstance(cert, QuotientCertificate) or not isinstance(cert.complex_, FiniteComplex):
        return Refused(RefusalCode.INVALID_INPUT, "not a graph quotient certificate")
    complex_ = cert.complex_
    vectors = (cert.cochain, cert.weights, cert.potential, cert.residual, cert.dual)
    if not _exact_fields(cert.value, vectors):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "certificate entries must be exact Fractions")
    edges = len(complex_.edges)
    if len(cert.potential) != len(complex_.vertices) or {
        len(cert.cochain), len(cert.weights), len(cert.residual), len(cert.dual)
    } != {edges}:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "certificate is not aligned with the complex")
    if any(weight <= 0 for weight in cert.weights):
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "weights must be positive")
    checked = verify_matrix_certificate(MatrixQuotientCertificate(
        d0_matrix(complex_), len(complex_.vertices), cert.cochain, cert.weights,
        cert.potential, cert.residual, cert.value, cert.dual,
    ))
    if isinstance(checked, Refused):
        return checked
    return Accepted(cert)


def exact_quotient_l1(
    complex_: FiniteComplex,
    cochain: Mapping[Edge, int | str | Fraction],
    weights: Mapping[Edge, int | str | Fraction] | None = None,
    *,
    max_pivots: int = DEFAULT_PIVOT_BUDGET,
) -> Outcome[QuotientCertificate]:
    """Phi_1([h]) = min_f ||h - d0 f||_{1,w} with an independently verified certificate."""

    if not isinstance(complex_, FiniteComplex):
        return Refused(RefusalCode.INVALID_INPUT, "the quotient norm needs a finite complex")
    vector = _cochain_vector(complex_, cochain)
    if isinstance(vector, Refused):
        return vector
    w = edge_weights(complex_, weights)
    if isinstance(w, Refused):
        return w
    solved = matrix_quotient_l1(
        d0_matrix(complex_), vector.value, w.value, columns=len(complex_.vertices), max_pivots=max_pivots
    )
    if isinstance(solved, Refused):
        return solved
    found = solved.value
    return verify_quotient_certificate(
        QuotientCertificate(
            complex_, found.delta, found.weights, found.potential, found.residual, found.value, found.dual
        )
    )


class DiagnosticClass(str, Enum):
    EXACT_CLASS = "exact_class"
    CLOSED_RESIDUAL = "closed_residual"
    ACTIVE_CLOSURE_FAILURE = "active_closure_failure"


def classify_signature(phi: Fraction, gamma: Fraction) -> DiagnosticClass:
    """Exactly one class: Gamma > 0, else Phi > 0, else exact."""

    if gamma > 0:
        return DiagnosticClass.ACTIVE_CLOSURE_FAILURE
    if phi > 0:
        return DiagnosticClass.CLOSED_RESIDUAL
    return DiagnosticClass.EXACT_CLASS


@dataclass(frozen=True)
class ObstructionSignature:
    phi1: Fraction
    gamma2: Fraction
    closure_ratio: Fraction | None
    d1_opnorm: Fraction
    diagnostic_class: DiagnosticClass
    certificate: QuotientCertificate
    authority_effect: AuthorityEffect = AuthorityEffect.NONE

    def __post_init__(self) -> None:
        if self.authority_effect is not AuthorityEffect.NONE:
            raise ValueError("a diagnostic signature cannot carry an authority effect")


def obstruction_signature(
    complex_: FiniteComplex,
    cochain: Mapping[Edge, int | str | Fraction],
    *,
    closure_declared: bool,
    weights: Mapping[Edge, int | str | Fraction] | None = None,
) -> Outcome[ObstructionSignature]:
    """(Phi_1, Gamma_2, R_cl) with a verified certificate on a declared window."""

    if closure_declared is not True:
        return Refused(RefusalCode.NO_RULE, "closure data are undeclared; the class is not classified")
    certified = exact_quotient_l1(complex_, cochain, weights)
    if isinstance(certified, Refused):
        return certified
    cert = certified.value
    try:
        gamma = closure(d0_matrix(complex_), len(complex_.vertices),
                        d1_matrix(complex_), cert.cochain)
    except FunctionalEvaluationError as error:
        return Refused(RefusalCode.NO_RULE, str(error))
    norm = d1_operator_norm_1to1(complex_)
    floor = min(cert.weights, default=Fraction(1))
    if gamma * floor > norm * cert.value:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "Gamma_2 exceeds ||d1||_{1->1} Phi_1 / min(w)")
    ratio = None if cert.value == 0 else gamma / cert.value
    return Accepted(
        ObstructionSignature(cert.value, gamma, ratio, norm, classify_signature(cert.value, gamma), cert)
    )


DIAGNOSTIC_EVIDENCE = (ObstructionSignature, QuotientCertificate, MatrixQuotientCertificate)


def promote_diagnostic(
    signature: ObstructionSignature | QuotientCertificate | MatrixQuotientCertificate,
    target: str,
) -> Refused:
    """A class, signature, or certificate never becomes a terminal, repair, receipt, or authority."""

    if not isinstance(signature, DIAGNOSTIC_EVIDENCE):
        return Refused(RefusalCode.INVALID_INPUT, "only diagnostic evidence can be examined for promotion")
    routing = isinstance(target, str) and target in ROUTING_TERMINALS
    kind = "routing terminal" if routing else "repair, receipt, authority, standing, or undeclared target"
    return Refused(
        RefusalCode.SCOPE_VIOLATION,
        f"{type(signature).__name__} is diagnostic evidence, not a {kind}: {target!r}",
    )


# Executable finite evidence; AuthorityEffect: None.
