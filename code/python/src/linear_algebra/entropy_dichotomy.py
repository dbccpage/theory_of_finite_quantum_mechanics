"""Exact rational purity and interval certificate for admitted densities.

Origin: lean4/EntropyDichotomy.lean theorem entropy_dichotomy_general_dimension.
The Python certificate recomputes rational purity and dyadic enclosures. It
does not discharge the Lean proof.
Claim: urn:omega:fqm:entropy:rational-purity-interval-certificate:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/linear_algebra/test_entropy_dichotomy.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 10; AST Sonar cognitive complexity max 9; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 10.
Scope Fence: Verdicts that name Baker input A1 are conditional on that cited
input. This file does not prove transcendence, does not admit a float, and
does not claim a physical entropy theorem beyond the exact rational certificate.
Explicit splitting output requires rational roots and at most one quadratic pair.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from functools import reduce
from math import gcd, lcm
from pathlib import Path
from typing import Any, Mapping

_DATA_DIR = Path(__file__).resolve().parent.parent / "qm" / "data"


class EntropyKernelError(ValueError):
    """One violated entropy-kernel invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        super().__init__(invariant)


class RationalTextError(EntropyKernelError):
    """A rational token is not a reduced a/b string."""


class RefusedAtBudget(EntropyKernelError):
    """No mathematical negative follows from this computational refusal."""


class UnsupportedExactScope(EntropyKernelError):
    """The general theorem remains separate from this implemented domain."""


def _ve(invariant: str, **parameters: object) -> EntropyKernelError:
    return EntropyKernelError(invariant, parameters)


def _text(invariant: str, **parameters: object) -> RationalTextError:
    return RationalTextError(invariant, parameters)


def _delta(left: int, right: int) -> Q:
    if left == right:
        return Q(1)
    return Q(0)


class _Budget:
    def __init__(self, limit: int, reason: str):
        self.limit = limit
        self.remaining = limit
        self.reason = reason

    def spend(self) -> None:
        if self.remaining == 0:
            raise RefusedAtBudget(f"{self.reason}; used={self.limit}, limit={self.limit}")
        self.remaining -= 1


MAX_D = 5
MAX_INPUT = 4096
MAX_CANDIDATES = 100000
MAX_COEFFICIENT = 64
MAX_K = 32
MAX_TERMS = 4096
MAX_FIXTURES = 64
RATIONAL_ROOT_RESOURCE_LIMIT = 100000
STURM_SUBDIVISION_RESOURCE_LIMIT = 4096
CLASS = {"S1": (2, 4), "S2": (3, 3), "S3": (2, 8), "S4": (4, 8),
         "S5": (5, 5), "S6": (4, 1), "S7": (3, 1), "S8": (4, 4)}
PHI = {1: 1, 3: 2, 4: 2, 5: 4, 8: 4}
INPUT_KEYS = {"fixture_id", "system_id", "conductor", "matrix", "scope"}
INTERFACE = _DATA_DIR / "rational_quadratic_fixtures.json"


def rat(q: Q | int) -> str:
    if isinstance(q, float) or type(q) is bool:
        raise _ve("float or boolean refused where a rational was required", received=type(q).__name__)
    parsed = Q(q)
    return f"{parsed.numerator}/{parsed.denominator}"


def _reject_float_list(value: list[Any], path: str) -> None:
    for index, item in enumerate(value):
        reject_floats(item, f"{path}[{index}]")


def reject_floats(value: Any, path: str = "object") -> None:
    if isinstance(value, float):
        raise _ve(f"float leakage at {path}", path=path, received="float")
    if isinstance(value, dict):
        for key, item in value.items():
            reject_floats(item, f"{path}.{key}")
        return
    if isinstance(value, list):
        _reject_float_list(value, path)


def _parsed_token(value: str) -> Q:
    try:
        return Q(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise _text("invalid rational input", received=value) from exc


def parse_rat(value: Any, *, bounded: bool = False) -> Q:
    if isinstance(value, float):
        raise _text("float refused at the public boundary", role="rational", received="float")
    if type(value) is bool or not isinstance(value, str):
        raise _text("rational input must be an a/b string", received=type(value).__name__)
    parsed = _parsed_token(value)
    if value != rat(parsed):
        raise _text("rational input must be reduced a/b with positive denominator", received=value)
    if bounded and (abs(parsed.numerator) > MAX_INPUT or parsed.denominator > MAX_INPUT):
        raise RefusedAtBudget("rational_input bound 4096 exhausted")
    return parsed


def prime_factors(value: int, budget: _Budget | None = None) -> dict[int, int]:
    """Trial division with an explicit candidate budget; no failed-search claim."""
    if type(value) is bool or type(value) is not int:
        raise _ve("prime factorization requires an exact integer", received=type(value).__name__)
    value = abs(value)
    if value == 0:
        raise _ve("zero has no prime exponent vector")
    budget = budget or _Budget(MAX_CANDIDATES, "dependence_candidates_max=100000 exhausted in exact factoring")
    factors: dict[int, int] = {}
    candidate = 2
    while candidate * candidate <= value:
        budget.spend()
        while value % candidate == 0:
            factors[candidate] = factors.get(candidate, 0) + 1
            value //= candidate
        candidate = 3 if candidate == 2 else candidate + 2
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def valuations(value: Q) -> dict[int, int]:
    if value <= 0:
        raise _ve("log argument must be strictly positive")
    result = prime_factors(value.numerator)
    for p, exponent in prime_factors(value.denominator).items():
        result[p] = result.get(p, 0) - exponent
    return {p: e for p, e in result.items() if e}


def rational_root(value: Q) -> dict[str, Any]:
    return {"kind": "rational", "value": rat(value)}


def quadratic_root(center: Q, coefficient: Q, radicand: int) -> dict[str, Any]:
    return {"kind": "quadratic", "center": rat(center),
            "coefficient": rat(coefficient), "radicand": radicand}


def sqrt_rational(value: Q) -> tuple[Q, int]:
    """Return nonnegative c and squarefree d with sqrt(value)=c*sqrt(d)."""
    if value < 0:
        raise _ve("negative discriminant")
    if value == 0:
        return Q(0), 1
    square, radical = 1, 1
    for prime, exponent in prime_factors(value.numerator * value.denominator).items():
        square *= prime ** (exponent // 2)
        radical *= prime ** (exponent % 2)
    return Q(square, value.denominator), radical


def multiply(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    n = len(left)
    return [[sum((left[i][k] * right[k][j] for k in range(n)), Q(0))
             for j in range(n)] for i in range(n)]


def charpoly(matrix: list[list[Q]]) -> list[Q]:
    """Faddeev--LeVerrier over Q; all coefficients of det(xI-matrix)."""
    n = len(matrix)
    previous = [[_delta(i, j) for j in range(n)] for i in range(n)]
    coefficients = [Q(1)]
    for degree in range(1, n + 1):
        product = multiply(matrix, previous)
        coefficient = -sum((product[i][i] for i in range(n)), Q(0)) / degree
        coefficients.append(coefficient)
        previous = [[product[i][j] + _delta(i, j) * coefficient for j in range(n)] for i in range(n)]
    return coefficients


def poly_product(left: list[Q], right: list[Q]) -> list[Q]:
    result = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def _poly_trim(poly: list[Q]) -> list[Q]:
    first = next((i for i, value in enumerate(poly) if value), len(poly) - 1)
    return poly[first:]


def _poly_eval(poly: list[Q], value: Q) -> Q:
    result = Q(0)
    for coefficient in poly:
        result = result * value + coefficient
    return result


def _poly_divmod(left: list[Q], right: list[Q]) -> tuple[list[Q], list[Q]]:
    left, right = _poly_trim(left[:]), _poly_trim(right[:])
    if not any(right):
        raise _ve("division by the zero polynomial")
    if len(left) < len(right):
        return [Q(0)], left
    quotient = [Q(0)] * (len(left) - len(right) + 1)
    degree = len(left) - len(right)
    remainder = left[:]
    while any(remainder) and len(remainder) >= len(right):
        offset = degree - (len(remainder) - len(right))
        coefficient = remainder[0] / right[0]
        quotient[offset] = coefficient
        for index, value in enumerate(right):
            remainder[index] -= coefficient * value
        remainder = _poly_trim(remainder)
    return _poly_trim(quotient), remainder


def _poly_exact_div(left: list[Q], right: list[Q]) -> list[Q]:
    quotient, remainder = _poly_divmod(left, right)
    if any(remainder):
        raise _ve("nonzero remainder in exact polynomial division")
    return quotient


def _poly_derivative(poly: list[Q]) -> list[Q]:
    degree = len(poly) - 1
    return [coefficient * (degree - index) for index, coefficient in enumerate(poly[:-1])] or [Q(0)]


def _poly_gcd(left: list[Q], right: list[Q]) -> list[Q]:
    while any(right):
        _, remainder = _poly_divmod(left, right)
        left, right = right, remainder
    return [value / left[0] for value in left]


def _divisors(value: int, budget: _Budget) -> list[int]:
    divisors = [1]
    for prime, exponent in prime_factors(value, budget).items():
        expanded = []
        for divisor in divisors:
            power = 1
            for _ in range(exponent + 1):
                budget.spend()
                expanded.append(divisor * power)
                power *= prime
        divisors = expanded
    return sorted(divisors)


def _integer_content(poly: list[Q]) -> list[int]:
    denominator = lcm(*(value.denominator for value in poly))
    integer = [value.numerator * (denominator // value.denominator) for value in poly]
    content = reduce(gcd, integer)
    return [value // content for value in integer]


def _root_on_denominator(poly: list[Q], budget: _Budget, numerator: int, denominators: list[int]) -> Q | None:
    for denominator in denominators:
        budget.spend()
        if numerator > denominator or gcd(numerator, denominator) != 1:
            continue
        candidate = Q(numerator, denominator)
        if _poly_eval(poly, candidate) == 0:
            return candidate
    return None


def _search_rational_root(poly: list[Q], budget: _Budget, numerators: list[int], denominators: list[int]) -> Q | None:
    for numerator in numerators:
        found = _root_on_denominator(poly, budget, numerator, denominators)
        if found is not None:
            return found
    return None


def _find_rational_root(poly: list[Q], budget: _Budget) -> Q | None:
    """Rational-root theorem on [0,1]. None means every candidate was tested."""
    if poly[-1] == 0:
        return Q(0)
    if _poly_eval(poly, Q(1)) == 0:
        return Q(1)
    integer = _integer_content(poly)
    return _search_rational_root(poly, budget, _divisors(abs(integer[-1]), budget), _divisors(abs(integer[0]), budget))


def _quadratic_square(poly: list[Q]) -> list[Q] | None:
    if len(poly) != 5 or poly[0] != 1:
        return None
    linear = poly[1] / 2
    constant = (poly[2] - linear * linear) / 2
    quadratic = [Q(1), linear, constant]
    return quadratic if poly_product(quadratic, quadratic) == poly else None


def _negative_diagonal(current: list[list[Q]]) -> bool:
    return any(current[i][i] < 0 for i in range(len(current)))


def _zero_pivot_defect(current: list[list[Q]]) -> bool:
    size = len(current)
    for index in range(size):
        if current[index][index] == 0 and any(current[index][column] for column in range(size)):
            return True
    return False


def _refuse_indefinite(current: list[list[Q]]) -> None:
    if _negative_diagonal(current):
        raise _ve("negative eigenvalue: exact Schur complement is not positive semidefinite")
    if _zero_pivot_defect(current):
        raise _ve("negative eigenvalue: zero diagonal has a nonzero off-diagonal entry")


def _schur_complement(current: list[list[Q]], pivot: int) -> list[list[Q]]:
    indices = [index for index in range(len(current)) if index != pivot]
    value = current[pivot][pivot]
    return [
        [current[i][j] - current[i][pivot] * current[pivot][j] / value for j in indices]
        for i in indices
    ]


def validate_psd(matrix: list[list[Q]]) -> None:
    """Exact rational Schur complements, including singular zero-pivot cases."""
    current = [row[:] for row in matrix]
    while current:
        _refuse_indefinite(current)
        pivot = next((i for i in range(len(current)) if current[i][i] > 0), None)
        if pivot is None:
            return
        current = _schur_complement(current, pivot)


def _require_s8_scope(case: dict[str, Any]) -> None:
    if case["scope"] != "S8_DIMENSION_ONLY_PROXY":
        raise _ve("S8 code support unresolved; dimension-only proxy label required")


def _require_declared_scope(case: dict[str, Any]) -> None:
    if case["system_id"] == "S8":
        _require_s8_scope(case)
        return
    if case["scope"] != "DECLARED_SYSTEM_STATE":
        raise _ve("state scope label mismatch")


def _require_diagonal_ladder(matrix: list[list[Q]], n: int) -> None:
    if any(matrix[i][j] for i in range(n) for j in range(n) if i != j):
        raise _ve("frozen ladder states must be diagonal")


def _require_geometric_ratio(matrix: list[list[Q]], n: int) -> None:
    if matrix[0][0] <= 0:
        raise _ve("S6 requires a positive geometric ladder")
    ratio = matrix[1][1] / matrix[0][0]
    if not 0 < ratio < 1:
        raise _ve("S6 requires the declared decreasing geometric ladder")
    if any(matrix[i][i] != matrix[0][0] * ratio**i for i in range(n)):
        raise _ve("S6 requires the declared decreasing geometric ladder")


def _check_system_scope_and_ladder(case: dict[str, Any], matrix: list[list[Q]], n: int) -> None:
    _require_declared_scope(case)
    if case["system_id"] in {"S6", "S7"}:
        _require_diagonal_ladder(matrix, n)
    if case["system_id"] == "S6":
        _require_geometric_ratio(matrix, n)


def _require_case_identity(case: dict[str, Any]) -> None:
    reject_floats(case, "input")
    if set(case) != INPUT_KEYS or not isinstance(case["fixture_id"], str):
        raise _ve("typed input requires exactly the five interface fields")
    if not case["fixture_id"]:
        raise _ve("fixture_id: nonempty string required")
    if case["system_id"] not in CLASS:
        raise _ve("system missing from frozen class")


def _require_conductor(case: dict[str, Any]) -> int:
    dimension, conductor = CLASS[case["system_id"]]
    if type(case["conductor"]) is bool or type(case["conductor"]) is not int or case["conductor"] != conductor:
        raise _ve("frozen conductor mismatch", received=type(case["conductor"]).__name__)
    return dimension


def _parse_square(raw: object, dimension: int) -> list[list[Q]]:
    if not isinstance(raw, list) or len(raw) > MAX_D:
        raise RefusedAtBudget("matrix_dimension_max=5 exhausted")
    if len(raw) != dimension or any(not isinstance(row, list) or len(row) != dimension for row in raw):
        raise _ve("frozen system dimension mismatch")
    return [[parse_rat(entry, bounded=True) for entry in row] for row in raw]


def _require_symmetric_trace(matrix: list[list[Q]], dimension: int) -> None:
    if any(matrix[i][j] != matrix[j][i] for i in range(dimension) for j in range(dimension)):
        raise _ve("input is not real symmetric; complex carrier matrices require another exact implementation")
    if sum((matrix[i][i] for i in range(dimension)), Q(0)) != 1:
        raise _ve("unnormalised spectrum: trace must equal one")


def validated_matrix(case: dict[str, Any]) -> list[list[Q]]:
    _require_case_identity(case)
    dimension = _require_conductor(case)
    matrix = _parse_square(case["matrix"], dimension)
    _require_symmetric_trace(matrix, dimension)
    _check_system_scope_and_ladder(case, matrix, dimension)
    validate_psd(matrix)
    return matrix


def _peel_rational_root(
    remaining: list[Q],
    budget: _Budget,
    roots: list[dict[str, Any]],
    reconstructed: list[Q],
) -> tuple[list[Q], list[Q]]:
    root = _find_rational_root(remaining, budget)
    if root is None:
        degree = len(remaining) - 1
        raise UnsupportedExactScope(
            f"residual characteristic degree {degree}: splitting/dependence beyond one quadratic pair is unsupported; no negative result"
        )
    while len(remaining) > 1 and _poly_eval(remaining, root) == 0:
        remaining = _poly_exact_div(remaining, [Q(1), -root])
        roots.append(rational_root(root))
        reconstructed = poly_product(reconstructed, [Q(1), -root])
    return remaining, reconstructed


def _append_linear(remaining: list[Q], roots: list[dict[str, Any]], reconstructed: list[Q]) -> list[Q]:
    root = -remaining[1] / remaining[0]
    roots.append(rational_root(root))
    return poly_product(reconstructed, [Q(1), -root])


def _append_quadratic_roots(roots: list[dict[str, Any]], center: Q, coefficient: Q, radical: int) -> None:
    if radical == 1:
        roots.extend([rational_root(center - coefficient), rational_root(center + coefficient)])
        return
    roots.extend([quadratic_root(center, -coefficient, radical), quadratic_root(center, coefficient, radical)])


def _append_quadratic(remaining: list[Q], roots: list[dict[str, Any]], reconstructed: list[Q], multiplicity: int) -> list[Q]:
    _ignored, linear, constant = remaining
    coefficient, radical = sqrt_rational(linear * linear - 4 * constant)
    center = -linear / 2
    coefficient = coefficient / 2
    for _ in range(multiplicity):
        reconstructed = poly_product(reconstructed, remaining)
        _append_quadratic_roots(roots, center, coefficient, radical)
    return reconstructed


def _finish_low_degree(
    remaining: list[Q],
    roots: list[dict[str, Any]],
    reconstructed: list[Q],
    multiplicity: int,
) -> list[Q]:
    if len(remaining) == 2:
        return _append_linear(remaining, roots, reconstructed)
    if len(remaining) == 3:
        return _append_quadratic(remaining, roots, reconstructed, multiplicity)
    return reconstructed


def _ordered_roots(roots: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rational = sorted([item for item in roots if item["kind"] == "rational"], key=lambda item: Q(item["value"]))
    quadratic = sorted(
        [item for item in roots if item["kind"] == "quadratic"],
        key=lambda item: (Q(item["center"]), item["radicand"], Q(item["coefficient"])),
    )
    return rational, quadratic


def _require_one_quadratic_pair(quadratic: list[dict[str, Any]]) -> None:
    pairs = {(item["center"], abs(Q(item["coefficient"])), item["radicand"]) for item in quadratic}
    if len(pairs) > 1:
        raise UnsupportedExactScope("multiple quadratic pairs: dependence support refused; no negative independence result")


def _push_spectrum(spectrum: list[dict[str, Any]], root: dict[str, Any]) -> None:
    if spectrum and spectrum[-1]["root"] == root:
        spectrum[-1]["multiplicity"] += 1
        return
    spectrum.append({"root": root, "multiplicity": 1})


def _group_spectrum(roots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rational, quadratic = _ordered_roots(roots)
    _require_one_quadratic_pair(quadratic)
    spectrum: list[dict[str, Any]] = []
    for root in rational + quadratic:
        _push_spectrum(spectrum, root)
    return spectrum


def _peel_high_degree(
    remaining: list[Q],
    budget: _Budget,
    roots: list[dict[str, Any]],
    reconstructed: list[Q],
) -> tuple[list[Q], list[Q], int]:
    multiplicity = 1
    while len(remaining) > 3:
        quadratic = _quadratic_square(remaining)
        if quadratic is not None:
            return quadratic, reconstructed, 2
        remaining, reconstructed = _peel_rational_root(remaining, budget, roots, reconstructed)
    return remaining, reconstructed, multiplicity


def polynomial_spectrum(coefficients: list[Q]) -> tuple[list[dict[str, Any]], list[Q]]:
    """Graph-independent extraction of rational roots and one quadratic pair."""
    roots: list[dict[str, Any]] = []
    reconstructed = [Q(1)]
    if len(coefficients) > MAX_D + 1:
        raise RefusedAtBudget("characteristic_degree_max=5 exhausted")
    budget = _Budget(
        RATIONAL_ROOT_RESOURCE_LIMIT,
        "IMPLEMENTATION_RESOURCE_LIMIT: rational-root search units are trial-factor candidates, generated divisors, and divisor-pair candidates",
    )
    remaining, reconstructed, multiplicity = _peel_high_degree(coefficients[:], budget, roots, reconstructed)
    reconstructed = _finish_low_degree(remaining, roots, reconstructed, multiplicity)
    return _group_spectrum(roots), reconstructed


def _find_basis_pivots(rows: list[list[Q]]) -> list[int]:
    pivots: list[tuple[int, list[Q]]] = []
    indices: list[int] = []
    for index, original in enumerate(rows):
        residual = original[:]
        for pivot, normalized in pivots:
            factor = residual[pivot]
            residual = [a - factor * b for a, b in zip(residual, normalized)]
        pivot = next((i for i, value in enumerate(residual) if value), None)
        if pivot is not None:
            factor = residual[pivot]
            pivots.append((pivot, [x / factor for x in residual]))
            indices.append(index)
    return indices


def _eliminate_tracked(
    residual: list[Q],
    representation: list[Q],
    tracked: list[tuple[int, list[Q], list[Q]]],
    sign: int,
) -> tuple[list[Q], list[Q]]:
    for pivot, normalized, coeffs in tracked:
        factor = residual[pivot]
        residual = [a - factor * b for a, b in zip(residual, normalized)]
        representation = [a + Q(sign) * factor * b for a, b in zip(representation, coeffs)]
    return residual, representation


def _next_nonzero(residual: list[Q]) -> int:
    for index, value in enumerate(residual):
        if value:
            return index
    raise _ve("Q row basis failed reconstruction")


def _scale_tracked(residual: list[Q], representation: list[Q], pivot: int) -> tuple[list[Q], list[Q]]:
    scale = residual[pivot]
    return [entry / scale for entry in residual], [entry / scale for entry in representation]


def _one_tracked_row(
    index: int,
    original: list[Q],
    tracked: list[tuple[int, list[Q], list[Q]]],
    rank: int,
) -> tuple[int, list[Q], list[Q]]:
    residual, representation = _eliminate_tracked(original[:], [_delta(index, column) for column in range(rank)], tracked, -1)
    pivot = _next_nonzero(residual)
    residual, representation = _scale_tracked(residual, representation, pivot)
    return pivot, residual, representation


def _build_tracked_basis(basis: list[list[Q]], rank: int) -> list[tuple[int, list[Q], list[Q]]]:
    tracked: list[tuple[int, list[Q], list[Q]]] = []
    for index, original in enumerate(basis):
        tracked.append(_one_tracked_row(index, original, tracked, rank))
    return tracked


def _bounded_coordinate(representation: list[Q]) -> list[Q]:
    denominator = lcm(*(entry.denominator for entry in representation))
    relation = [denominator] + [-entry.numerator * (denominator // entry.denominator) for entry in representation]
    divisor = reduce(gcd, relation)
    if any(abs(entry // divisor) > MAX_COEFFICIENT for entry in relation):
        raise RefusedAtBudget("dependence_integer_coefficient_abs_max=64 exhausted in exact coordinates")
    return representation


def _one_coordinate(original: list[Q], tracked: list[tuple[int, list[Q], list[Q]]], rank: int) -> list[Q]:
    residual, representation = _eliminate_tracked(original[:], [Q(0)] * rank, tracked, 1)
    if any(residual):
        raise _ve("Q row basis failed reconstruction")
    return _bounded_coordinate(representation)


def _compute_row_coordinates(rows: list[list[Q]], tracked: list[tuple[int, list[Q], list[Q]]], rank: int) -> list[list[Q]]:
    return [_one_coordinate(original, tracked, rank) for original in rows]


def row_basis(rows: list[list[Q]]) -> tuple[list[int], list[list[Q]]]:
    """Greedy exact Q row basis and reconstruction coordinates."""
    indices = _find_basis_pivots(rows)
    basis = [rows[i] for i in indices]
    rank = len(basis)
    tracked = _build_tracked_basis(basis, rank)
    coordinates = _compute_row_coordinates(rows, tracked, rank)
    return indices, coordinates


def _quadratic_pair(arguments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pair = [item for item in arguments if item["kind"] == "quadratic"]
    if pair and len(pair) != 2:
        raise UnsupportedExactScope("quadratic conjugate pair not available")
    return pair


def _norm_of_pair(pair: list[dict[str, Any]]) -> dict[int, int]:
    if not pair:
        return {}
    center, coefficient = Q(pair[0]["center"]), Q(pair[0]["coefficient"])
    norm = center**2 - coefficient**2 * pair[0]["radicand"]
    if norm <= 0:
        raise _ve("quadratic log arguments must be strictly positive")
    return valuations(norm)


def _rational_exponent_row(factors: dict[int, int], primes: list[int], paired: int) -> list[Q]:
    row = [Q(factors.get(prime, 0)) for prime in primes]
    if paired != 0:
        row.append(Q(0))
    return row


def _quadratic_exponent_row(item: dict[str, Any], primes: list[int], norm_factors: dict[int, int]) -> list[Q]:
    sign = 1 if Q(item["coefficient"]) > 0 else -1
    return [Q(norm_factors.get(prime, 0), 2) for prime in primes] + [Q(sign, 2)]


def _exponent_row(item: dict[str, Any], primes: list[int], pair: list[dict[str, Any]], norm_factors: dict[int, int]) -> list[Q]:
    if item["kind"] == "rational":
        paired = 1 if pair else 0
        return _rational_exponent_row(valuations(Q(item["value"])), primes, paired)
    return _quadratic_exponent_row(item, primes, norm_factors)


def _dependence_method(pair: list[dict[str, Any]]) -> str:
    if pair:
        return "PRIME_AND_CONJUGATE_RATIO_Q_ROW_BASIS"
    return "PRIME_EXPONENT_Q_ROW_BASIS"


def _nonzero_arguments(spectrum: list[dict[str, Any]]) -> list[dict[str, Any]]:
    arguments: list[dict[str, Any]] = []
    for entry in spectrum:
        if entry["root"] != rational_root(Q(0)):
            arguments.append(entry["root"])
    return arguments


def _rational_maps(arguments: list[dict[str, Any]]) -> list[dict[int, int]]:
    maps: list[dict[int, int]] = []
    for item in arguments:
        if item["kind"] == "rational":
            maps.append(valuations(Q(item["value"])))
    return maps


def _prime_support(exponent_maps: list[dict[int, int]], norm_factors: dict[int, int]) -> list[int]:
    primes: set[int] = set()
    for factors in exponent_maps + [norm_factors]:
        for prime in factors:
            primes.add(prime)
    return sorted(primes)


def _prime_generators(primes: list[int]) -> list[dict[str, Any]]:
    generators: list[dict[str, Any]] = []
    for prime in primes:
        generators.append({"kind": "prime", "value": prime})
    return generators


def _wire_rows(rows: list[list[Q]]) -> list[list[str]]:
    wired: list[list[str]] = []
    for row in rows:
        wired.append([rat(entry) for entry in row])
    return wired


def _dependence_record(
    pair: list[dict[str, Any]],
    arguments: list[dict[str, Any]],
    generators: list[dict[str, Any]],
    rows: list[list[Q]],
    indices: list[int],
    coordinates: list[list[Q]],
) -> dict[str, Any]:
    return {
        "status": "EXACT",
        "method": _dependence_method(pair),
        "arguments": arguments,
        "generators": generators,
        "exponent_rows": _wire_rows(rows),
        "basis_argument_indices": indices,
        "coordinates": _wire_rows(coordinates),
    }


def dependence(spectrum: list[dict[str, Any]]) -> dict[str, Any]:
    arguments = _nonzero_arguments(spectrum)
    pair = _quadratic_pair(arguments)
    norm_factors = _norm_of_pair(pair)
    primes = _prime_support(_rational_maps(arguments), norm_factors)
    generators = _prime_generators(primes)
    if pair:
        generators.append({"kind": "quadratic_ratio", "numerator": pair[1], "denominator": pair[0]})
    rows = [_exponent_row(item, primes, pair, norm_factors) for item in arguments]
    indices, coordinates = row_basis(rows)
    return _dependence_record(pair, arguments, generators, rows, indices, coordinates)


def splitting_field(spectrum: list[dict[str, Any]], conductor: int) -> dict[str, Any]:
    radicals = {entry["root"]["radicand"] for entry in spectrum if entry["root"]["kind"] == "quadratic"}
    if len(radicals) > 1:
        raise UnsupportedExactScope("multiple squareclasses require another exact splitting-field implementation")
    d = next(iter(radicals)) if radicals else None
    degree = 2 if d else 1
    relative = 1 if d is None or (d, conductor) in {(2, 8), (5, 5)} else 2
    return {"spectrum_splitting_field": f"Q(sqrt({d}))" if d else "Q",
            "spectrum_degree_over_q": degree, "carrier_conductor": conductor,
            "extension_degree_over_carrier": relative,
            "compositum_degree_over_q": PHI[conductor] * relative}


def _verdict_from_validated_purity(purity: str, interval: dict[str, Any] | None = None) -> dict[str, str]:
    """Total on the two admitted purity values and validated optional interface.

    MIXED uses strict positivity of a real entropy summand and Baker A1.
    Arithmetic establishes only purity, never transcendence itself.
    """
    if purity not in {"PURE", "MIXED"}:
        raise _ve("verdict domain requires a previously validated purity witness")
    if interval is not None:
        validate_interval(interval)
    if purity == "PURE":
        return {"verdict": "CARRIED", "reason": "PURE_STATE_ZERO",
                "anchor": "ZERO_LOG_ZERO_CONVENTION_AND_REAL_LOG_ONE", "quantity_type": "CARRIER_ZERO"}
    if interval is None:
        return {"verdict": "REFUSED_TRANSCENDENTAL", "reason": "MIXED_STATE_POSITIVITY_AND_BAKER_REDUCTION",
                "anchor": "A1", "quantity_type": "TRANSCENDENTAL_VALUE"}
    return {"verdict": "EXTERNALLY_INTERFACED", "reason": "MIXED_STATE_WITH_RATIONAL_INTERVAL_INTERFACE",
            "anchor": "A1", "quantity_type": "APPROXIMATION_NOT_MEMBERSHIP"}


def analyze(case: dict[str, Any]) -> dict[str, Any]:
    matrix = validated_matrix(case)
    coefficients = charpoly(matrix)
    spectrum, reconstructed = polynomial_spectrum(coefficients)
    if coefficients != reconstructed:
        raise _ve("spectrum product does not match characteristic polynomial")
    power_sum = sum((matrix[i][j] * matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix))), Q(0))
    purity = "PURE" if power_sum == 1 else "MIXED"
    return {"characteristic_polynomial": [rat(q) for q in coefficients], "spectrum": spectrum,
            "splitting_field": splitting_field(spectrum, case["conductor"]),
            "dependence": dependence(spectrum), "purity": purity,
            "renyi2_power_sum": rat(power_sum), "entropy": _verdict_from_validated_purity(purity)}


def entropy_verdict(case: dict[str, Any], *, approximation_k: int | None = None) -> dict[str, str]:
    """Total three-way verdict on admitted, exactly validated density inputs.

    An external verdict requires actually computing the interval for this input;
    a caller cannot obtain one by supplying an unrelated or invented enclosure.
    """
    import cyclotomic_density
    if cyclotomic_density.has_cyclotomic_entries(case):
        return cyclotomic_density.entropy_verdict(case, approximation_k=approximation_k)
    matrix = validated_matrix(case)
    power_sum = sum((value * value for row in matrix for value in row), Q(0))
    purity = "PURE" if power_sum == 1 else "MIXED"
    interval = None if approximation_k is None else entropy_interval(case, approximation_k)
    return _verdict_from_validated_purity(purity, interval)


def _atanh_series_interval(q: Q, epsilon: Q) -> tuple[Q, Q, int]:
    if not 1 <= q <= 2 or epsilon <= 0:
        raise _ve("series interval requires 1<=q<=2 and positive epsilon")
    z = (q - 1) / (q + 1)
    power, partial = z, Q(0)
    for terms in range(1, MAX_TERMS + 1):
        partial += 2 * power / (2 * terms - 1)
        power *= z * z
        tail = 2 * power / ((2 * terms + 1) * (1 - z * z))
        if tail <= epsilon:
            return partial, partial + tail, terms
    raise RefusedAtBudget("approximation_series_terms_max=4096 exhausted")


def log_interval(q: Q, epsilon: Q) -> tuple[Q, Q, int]:
    """Real ln(q), rational atanh series and rigorously bounded rational tail."""
    if q <= 0:
        raise _ve("log interval requires a strictly positive rational; log(0) is never evaluated")
    if q == 1:
        return Q(0), Q(0), 0
    if q > 1:
        low, high, terms = log_interval(1 / q, epsilon)
        return -high, -low, terms
    shift, scaled = 0, q
    while scaled < 1:
        scaled *= 2
        shift += 1
        if shift > MAX_TERMS:
            raise RefusedAtBudget("approximation reduction exceeded 4096 exact shifts")
    part_epsilon = epsilon / (shift + 1)
    low, high, terms = _atanh_series_interval(scaled, part_epsilon)
    low2, high2, terms2 = _atanh_series_interval(Q(2), part_epsilon)
    return low - shift * high2, min(Q(0), high - shift * low2), max(terms, terms2)


def root_interval(root: dict[str, Any], bits: int) -> tuple[Q, Q]:
    if root["kind"] == "rational":
        q = Q(root["value"])
        return q, q
    d, center, coefficient = root["radicand"], Q(root["center"]), Q(root["coefficient"])
    lo, hi = Q(0), Q(max(1, d))
    for _ in range(MAX_TERMS):
        if abs(coefficient) * (hi - lo) <= Q(1, 2**bits):
            if coefficient >= 0:
                return center + coefficient * lo, center + coefficient * hi
            return center + coefficient * hi, center + coefficient * lo
        mid = (lo + hi) / 2
        if mid * mid <= d:
            lo = mid
        else:
            hi = mid
    raise RefusedAtBudget("root isolating interval exceeded 4096 rational bisections")


def squarefree_factors(poly: list[Q]) -> list[tuple[list[Q], int]]:
    """Yun's characteristic-zero squarefree decomposition over exact Q."""
    poly = [value / poly[0] for value in poly]
    repeated = _poly_gcd(poly, _poly_derivative(poly))
    remaining = _poly_exact_div(poly, repeated)
    multiplicity, factors = 1, []
    while len(remaining) > 1:
        shared = _poly_gcd(remaining, repeated)
        factor = _poly_exact_div(remaining, shared)
        if len(factor) > 1:
            factors.append((factor, multiplicity))
        remaining = shared
        repeated = _poly_exact_div(repeated, shared)
        multiplicity += 1
    rebuilt = [Q(1)]
    for factor, count in factors:
        for _ in range(count):
            rebuilt = poly_product(rebuilt, factor)
    if rebuilt != poly:
        raise _ve("squarefree factor multiplicities failed exact characteristic-polynomial reconstruction")
    return factors


def sturm_sequence(poly: list[Q]) -> list[list[Q]]:
    """Signed negative-remainder sequence; only POSITIVE rescaling is used."""
    sequence = [poly, _poly_derivative(poly)]
    while len(sequence[-1]) > 1:
        _, remainder = _poly_divmod(sequence[-2], sequence[-1])
        if not any(remainder):
            break
        negative = [-value for value in remainder]
        scale = abs(negative[0])
        sequence.append([value / scale for value in negative])
    return sequence


def _variations(sequence: list[list[Q]], value: Q) -> int:
    values = [_poly_eval(poly, value) for poly in sequence]
    signs = [1 if entry > 0 else -1 for entry in values if entry]
    changes = 0
    for left, right in zip(signs, signs[1:]):
        if left != right:
            changes += 1
    return changes


def _upper_hit(sequence: list[list[Q]], upper: Q) -> int:
    if _poly_eval(sequence[0], upper) == 0:
        return 1
    return 0


def _open_root_count(sequence: list[list[Q]], lower: Q, upper: Q) -> int:
    """Distinct roots in the OPEN interval (lower, upper)."""
    return _variations(sequence, lower) - _variations(sequence, upper) - _upper_hit(sequence, upper)


def sturm_spectrum_intervals(coefficients: list[Q], bits: int,
                             budget: _Budget | None = None) -> list[tuple[Q, Q, int]]:
    """All algebraic roots of an admitted density charpoly, with multiplicities.

    This does not identify a splitting field or a logarithm basis. The finite
    root-count certificate covers [0,1], including exact endpoint roots. A
    shared operational subdivision ceiling is distinct from the log-series cap.
    """
    return [(a, b, multiplicity) for a, b, count, multiplicity
            in _sturm_enclosures(coefficients, bits, budget, clusters=False)]


def sturm_spectral_clusters(coefficients: list[Any], bits: int,
                            budget: _Budget | None = None) -> list[tuple[Q, Q, int, int]]:
    """Count roots without separating them: (lower, upper, distinct count, m).

    Here m is the squarefree factor multiplicity. An open bin with r roots
    represents r*m eigenvalues, not one eigenvalue of multiplicity r*m.
    Exact endpoint and midpoint roots are represented separately as singletons.
    """
    return _sturm_enclosures(coefficients, bits, budget, clusters=True)


def _peel_sturm_endpoint(factor: list[Q], endpoint: Q, multiplicity: int, result: list[tuple[Q, Q, int, int]]) -> list[Q]:
    if len(factor) > 1 and _poly_eval(factor, endpoint) == 0:
        result.append((endpoint, endpoint, 1, multiplicity))
        return _poly_exact_div(factor, [Q(1), -endpoint])
    return factor


def _bin_is_terminal(clusters: bool, count: int, lower: Q, upper: Q, tolerance: Q) -> bool:
    if upper - lower > tolerance:
        return False
    if clusters:
        return True
    return count == 1 and lower > 0


def _exact_bit(value: bool) -> int:
    if value:
        return 1
    return 0


def _enqueue_sturm_split(
    pending: list[tuple[Q, Q, int]],
    result: list[tuple[Q, Q, int, int]],
    factor: list[Q],
    sequence: list[list[Q]],
    lower: Q,
    upper: Q,
    count: int,
    multiplicity: int,
    budget: _Budget,
) -> None:
    budget.spend()
    midpoint = (lower + upper) / 2
    exact = _poly_eval(factor, midpoint) == 0
    left = _open_root_count(sequence, lower, midpoint)
    right = _open_root_count(sequence, midpoint, upper)
    if left < 0 or right < 0 or left + right + _exact_bit(exact) != count:
        raise _ve("Sturm subdivision lost or double-counted an eigenvalue")
    if exact:
        result.append((midpoint, midpoint, 1, multiplicity))
    pending.append((midpoint, upper, right))
    pending.append((lower, midpoint, left))


def _consume_sturm_bin(
    pending: list[tuple[Q, Q, int]],
    result: list[tuple[Q, Q, int, int]],
    factor: list[Q],
    sequence: list[list[Q]],
    lower: Q,
    upper: Q,
    count: int,
    multiplicity: int,
    budget: _Budget,
    tolerance: Q,
    clusters: bool,
) -> None:
    if count == 0:
        return
    if _bin_is_terminal(clusters, count, lower, upper, tolerance):
        result.append((lower, upper, count, multiplicity))
        return
    _enqueue_sturm_split(pending, result, factor, sequence, lower, upper, count, multiplicity, budget)


def _enclose_one_factor(
    factor: list[Q],
    multiplicity: int,
    budget: _Budget,
    tolerance: Q,
    clusters: bool,
    result: list[tuple[Q, Q, int, int]],
) -> None:
    for endpoint in (Q(0), Q(1)):
        factor = _peel_sturm_endpoint(factor, endpoint, multiplicity, result)
    if len(factor) == 1:
        return
    sequence = sturm_sequence(factor)
    count = _open_root_count(sequence, Q(0), Q(1))
    if count != len(factor) - 1:
        raise _ve("Sturm root census does not place every density eigenvalue in [0,1]")
    pending = [(Q(0), Q(1), count)]
    while pending:
        lower, upper, count = pending.pop()
        _consume_sturm_bin(pending, result, factor, sequence, lower, upper, count, multiplicity, budget, tolerance, clusters)


def _require_sturm_census(result: list[tuple[Q, Q, int, int]], coefficients: list[Any]) -> None:
    total = sum(count * multiplicity for _lower, _upper, count, multiplicity in result)
    if total != len(coefficients) - 1:
        raise _ve("Sturm multiplicity census differs from the characteristic degree")


def _sturm_enclosures(coefficients: list[Any], bits: int, budget: _Budget | None,
                       *, clusters: bool) -> list[tuple[Q, Q, int, int]]:
    active = budget or _Budget(STURM_SUBDIVISION_RESOURCE_LIMIT, "IMPLEMENTATION_RESOURCE_LIMIT: sturm_subdivisions")
    tolerance = Q(1, 2**bits)
    result: list[tuple[Q, Q, int, int]] = []
    for original, multiplicity in squarefree_factors(coefficients):
        _enclose_one_factor(original[:], multiplicity, active, tolerance, clusters, result)
    _require_sturm_census(result, coefficients)
    return sorted(result)


def entropy_interval(case: dict[str, Any], k: int) -> dict[str, Any]:
    """Return a rational enclosure of S with width <=2^-k, never membership."""
    if type(k) is not int or not 0 <= k <= MAX_K:
        raise RefusedAtBudget("approximation_k_max=32 exhausted or invalid precision")
    import cyclotomic_density
    if cyclotomic_density.has_cyclotomic_entries(case):
        return cyclotomic_density.entropy_interval(case, k)
    matrix = validated_matrix(case)
    coefficients = charpoly(matrix)
    return _entropy_interval_from_characteristic(coefficients, k)


def _require_precision(k: object) -> int:
    if type(k) is bool or type(k) is not int or not 0 <= k <= MAX_K:
        raise RefusedAtBudget("approximation_k_max=32 exhausted or invalid precision")
    return k


def _positive_count(value: object) -> int:
    if type(value) is bool or type(value) is not int or value < 1:
        raise _ve("Sturm cluster count and multiplicity must be positive integers")
    return value


def _dyadic_point(value: Q, bits: int) -> bool:
    return (value * 2**bits).denominator == 1


def _cluster_geometry_bad(lower: Q, upper: Q, count: int, tolerance: Q, bits: int) -> bool:
    if not 0 <= lower <= upper <= 1:
        return True
    if upper - lower > tolerance:
        return True
    if lower == upper and count != 1:
        return True
    if not _dyadic_point(lower, bits) or not _dyadic_point(upper, bits):
        return True
    return False


def _cluster_contribution(
    lower: Q,
    upper: Q,
    count: int,
    multiplicity: int,
    epsilon: Q,
    dimension: int,
    radius: Q,
    tolerance: Q,
    bits: int,
) -> tuple[Q, Q, int]:
    _positive_count(count)
    _positive_count(multiplicity)
    if _cluster_geometry_bad(lower, upper, count, tolerance, bits):
        raise _ve("Sturm cluster geometry or width violates the dyadic contract")
    if lower == upper and lower in {Q(0), Q(1)}:
        return Q(0), Q(0), 0
    midpoint = (lower + upper) / 2
    log_lo, log_hi, used_terms = log_interval(midpoint, epsilon / (8 * dimension))
    error_radius = radius if lower != upper else Q(0)
    weight = count * multiplicity
    low = weight * max(Q(0), -midpoint * log_hi - error_radius)
    high = weight * (-midpoint * log_lo + error_radius)
    return low, high, used_terms


def _sum_clusters(
    enclosures: list[tuple[Q, Q, int, int]],
    epsilon: Q,
    dimension: int,
    radius: Q,
    tolerance: Q,
    bits: int,
) -> tuple[Q, Q, int]:
    lower, upper, terms = Q(0), Q(0), 0
    for left, right, count, multiplicity in enclosures:
        low, high, used = _cluster_contribution(left, right, count, multiplicity, epsilon, dimension, radius, tolerance, bits)
        lower += low
        upper += high
        terms = max(terms, used)
    return lower, upper, terms


def _interval_record(
    k: int,
    lower: Q,
    upper: Q,
    epsilon: Q,
    terms: int,
    bits: int,
    radius: Q,
    dimension: int,
    resource: _Budget,
    enclosures: list[tuple[Q, Q, int, int]],
) -> dict[str, Any]:
    return {
        "authority_effect": "None",
        "quantity_type": "APPROXIMATION_NOT_MEMBERSHIP",
        "metric": "ABSOLUTE_REAL_ERROR",
        "k": k,
        "lower": rat(lower),
        "upper": rat(upper),
        "midpoint": rat((lower + upper) / 2),
        "width": rat(upper - lower),
        "error_bound": rat(epsilon),
        "max_series_terms_used": terms,
        "root_isolation": "EXACT_RATIONAL_STURM_SPECTRAL_CLUSTERS",
        "approximation_algorithm": "DYADIC_STURM_CLUSTERS_WITH_UNIFORM_ENTROPY_MODULUS",
        "spectral_count_convention": "OPEN_BINS_PLUS_EXACT_SINGLETONS",
        "cluster_precision_bits": bits,
        "uniform_entropy_radius": rat(radius),
        "sturm_subdivision_proved_bound": dimension * bits,
        "log_shift_proved_bound": bits + 1,
        "series_terms_proved_bound": 64,
        "sturm_subdivisions_used": resource.limit - resource.remaining,
        "sturm_subdivision_limit": resource.limit,
        "sturm_resource_limit_kind": "IMPLEMENTATION_RESOURCE_LIMIT",
        "input_dimension": dimension,
        "spectral_enclosures": [
            {"lower": rat(left), "upper": rat(right), "distinct_root_count": count, "multiplicity": multiplicity}
            for left, right, count, multiplicity in enclosures
        ],
        "analytic_input": "REAL_LOG_ATANH_TAIL_AND_UNIFORM_ENTROPY_MODULUS",
        "transcendence_anchor": "A1",
    }


def _attach_embedding(result: dict[str, Any], cyclotomic_embedding: dict[str, Any] | None) -> None:
    if cyclotomic_embedding is None:
        return
    import cyclotomic_density
    result["root_isolation"] = cyclotomic_density.ROOT_ISOLATION
    result["embedding"] = cyclotomic_embedding


def _entropy_interval_from_characteristic(coefficients: list[Any], k: int, *,
                                           cyclotomic_embedding: dict[str, Any] | None = None) -> dict[str, Any]:
    """Counted dyadic root clusters with a uniform modulus for -x*ln(x)."""
    precision = _require_precision(k)
    epsilon, dimension = Q(1, 2**precision), len(coefficients) - 1
    bits = precision + 12
    tolerance = Q(1, 2**bits)
    radius = tolerance * (bits + 2)
    resource = _Budget(STURM_SUBDIVISION_RESOURCE_LIMIT, "IMPLEMENTATION_RESOURCE_LIMIT: sturm_subdivisions")
    enclosures = sturm_spectral_clusters(coefficients, bits, resource)
    if sum(count * multiplicity for _a, _b, count, multiplicity in enclosures) != dimension:
        raise _ve("Sturm spectral enclosure multiplicity sum differs from input dimension")
    lower, upper, terms = _sum_clusters(enclosures, epsilon, dimension, radius, tolerance, bits)
    result = _interval_record(precision, lower, upper, epsilon, terms, bits, radius, dimension, resource, enclosures)
    _attach_embedding(result, cyclotomic_embedding)
    validate_interval(result)
    return result


def _require_interval_kind(interval: dict[str, Any]) -> None:
    reject_floats(interval, "entropy_interval")
    if interval.get("quantity_type") != "APPROXIMATION_NOT_MEMBERSHIP":
        raise _ve("interval must be approximation, never carrier membership")
    if interval.get("metric") != "ABSOLUTE_REAL_ERROR":
        raise _ve("interval must be approximation, never carrier membership")


def _require_interval_precision(interval: dict[str, Any]) -> int:
    k = interval.get("k")
    if type(k) is bool or type(k) is not int or not 0 <= k <= MAX_K:
        raise _ve("invalid interval precision")
    return k


def _require_interval_order(lower: Q, upper: Q, midpoint: Q) -> None:
    if lower < 0 or lower > upper or midpoint != (lower + upper) / 2:
        raise _ve("invalid rational entropy enclosure")


def _require_interval_width(interval: dict[str, Any], lower: Q, upper: Q, k: int) -> None:
    if parse_rat(interval["width"]) != upper - lower or upper - lower > Q(1, 2**k):
        raise _ve("entropy interval exceeds declared error obligation")
    if parse_rat(interval["error_bound"]) != Q(1, 2**k):
        raise _ve("entropy error bound does not equal 2^-k")


def _check_interval_bounds(interval: dict[str, Any]) -> int:
    _require_interval_kind(interval)
    k = _require_interval_precision(interval)
    lower, upper, midpoint = (parse_rat(interval[key]) for key in ("lower", "upper", "midpoint"))
    _require_interval_order(lower, upper, midpoint)
    _require_interval_width(interval, lower, upper, k)
    return k


def _require_sturm_kind(interval: dict[str, Any], root_isolation: object) -> None:
    admitted = {"EXACT_RATIONAL_STURM_SPECTRAL_CLUSTERS", "EXACT_CYCLOTOMIC_REAL_STURM_SPECTRAL_CLUSTERS"}
    if root_isolation not in admitted:
        raise _ve("invalid Sturm operational resource accounting")
    if interval.get("sturm_resource_limit_kind") != "IMPLEMENTATION_RESOURCE_LIMIT":
        raise _ve("invalid Sturm operational resource accounting")


def _require_sturm_counts(used: object, limit: object) -> tuple[int, int]:
    if type(used) is bool or type(used) is not int or type(limit) is bool or type(limit) is not int:
        raise _ve("invalid Sturm operational resource accounting")
    if limit != STURM_SUBDIVISION_RESOURCE_LIMIT or not 0 <= used <= limit:
        raise _ve("invalid Sturm operational resource accounting")
    return used, limit


def _require_series_terms(series_terms: object) -> int:
    if type(series_terms) is bool or type(series_terms) is not int or not 0 <= series_terms <= MAX_TERMS:
        raise _ve("invalid frozen series-term accounting")
    return series_terms


def _check_sturm_accounting(interval: dict[str, Any]) -> tuple[int, int]:
    used = interval.get("sturm_subdivisions_used")
    limit = interval.get("sturm_subdivision_limit")
    root_isolation = interval.get("root_isolation")
    if root_isolation == "EXACT_CYCLOTOMIC_REAL_STURM_SPECTRAL_CLUSTERS":
        import cyclotomic_density
        cyclotomic_density.validate_embedding(interval.get("embedding"))
    _require_sturm_kind(interval, root_isolation)
    checked_used, _checked_limit = _require_sturm_counts(used, limit)
    return checked_used, _require_series_terms(interval.get("max_series_terms_used"))


def _require_dimension_list(interval: dict[str, Any]) -> tuple[int, list[Any]]:
    dimension = interval.get("input_dimension")
    enclosures = interval.get("spectral_enclosures")
    if type(dimension) is bool or type(dimension) is not int or not 1 <= dimension <= MAX_D:
        raise _ve("invalid spectral enclosure dimension or list")
    if not isinstance(enclosures, list):
        raise _ve("invalid spectral enclosure dimension or list")
    return dimension, enclosures


def _require_bound_field(interval: dict[str, Any], key: str, expected: int) -> None:
    if type(interval.get(key)) is not int or interval[key] != expected:
        raise _ve("invalid proved cluster approximation bounds or count convention")


def _require_algorithm_bounds(interval: dict[str, Any], dimension: int, k: int, used: int, series_terms: int) -> int:
    bits = k + 12
    if interval.get("approximation_algorithm") != "DYADIC_STURM_CLUSTERS_WITH_UNIFORM_ENTROPY_MODULUS":
        raise _ve("invalid proved cluster approximation bounds or count convention")
    if interval.get("spectral_count_convention") != "OPEN_BINS_PLUS_EXACT_SINGLETONS":
        raise _ve("invalid proved cluster approximation bounds or count convention")
    _require_bound_field(interval, "cluster_precision_bits", bits)
    _require_bound_field(interval, "sturm_subdivision_proved_bound", dimension * bits)
    _require_bound_field(interval, "log_shift_proved_bound", bits + 1)
    _require_bound_field(interval, "series_terms_proved_bound", 64)
    if interval.get("uniform_entropy_radius") != rat(Q(bits + 2, 2**bits)):
        raise _ve("invalid proved cluster approximation bounds or count convention")
    if used > dimension * bits or series_terms > 64:
        raise _ve("invalid proved cluster approximation bounds or count convention")
    return bits


def _enclosure_weight(enclosure: object, bits: int) -> int:
    if not isinstance(enclosure, dict) or set(enclosure) != {"lower", "upper", "distinct_root_count", "multiplicity"}:
        raise _ve("spectral enclosure requires lower, upper, distinct_root_count, and multiplicity")
    count = enclosure["distinct_root_count"]
    multiplicity = enclosure["multiplicity"]
    if type(multiplicity) is bool or type(multiplicity) is not int or multiplicity < 1:
        raise _ve("spectral enclosure multiplicity must be a positive integer")
    if type(count) is bool or type(count) is not int or count < 1:
        raise _ve("spectral enclosure distinct root count must be a positive integer")
    lower, upper = parse_rat(enclosure["lower"]), parse_rat(enclosure["upper"])
    if _cluster_geometry_bad(lower, upper, count, Q(1, 2**bits), bits):
        raise _ve("spectral cluster geometry, width, or singleton root count is invalid")
    return count * multiplicity


def _check_spectral_enclosures(interval: dict[str, Any], k: int, used: int, series_terms: int) -> None:
    dimension, enclosures = _require_dimension_list(interval)
    bits = _require_algorithm_bounds(interval, dimension, k, used, series_terms)
    total = 0
    for enclosure in enclosures:
        total += _enclosure_weight(enclosure, bits)
    if total != dimension:
        raise _ve("spectral enclosure multiplicity sum differs from input dimension")


def validate_interval(interval: dict[str, Any]) -> None:
    """Validate type/width/multiplicity metadata; this is not a root proof.

    The producer's exact Sturm construction establishes the enclosures. Merely
    passing this structural validator cannot establish that invented endpoints
    contain any particular matrix's eigenvalues.
    """
    k = _check_interval_bounds(interval)
    used, series_terms = _check_sturm_accounting(interval)
    _check_spectral_enclosures(interval, k, used, series_terms)


def fixtures(interface: Path | None = None) -> list[dict[str, Any]]:
    envelope = json.loads((interface or INTERFACE).read_text(encoding="utf-8"))
    reject_floats(envelope, "interface")
    return validate_fixture_batch(envelope["fixtures"])


def validate_fixture_batch(values: Any) -> list[dict[str, Any]]:
    if not isinstance(values, list) or not values:
        raise _ve("fixtures: nonempty array required")
    if len(values) > MAX_FIXTURES:
        raise RefusedAtBudget("fixture_cases_max=64 exhausted")
    seen = set()
    for case in values:
        identity = case.get("fixture_id") if isinstance(case, dict) else None
        if not isinstance(identity, str) or not identity:
            raise _ve("fixture_id: nonempty string required")
        if identity in seen:
            raise _ve(f"fixture_id:{identity}: duplicate fixture ID")
        seen.add(identity)
    return values


def report(interface: Path | None = None) -> dict[str, Any]:
    return {"authority_effect": "None", "schema": "c750_b01_exact_v1",
            "cases": [{"input": case, "output": analyze(case)} for case in fixtures(interface)]}


def serialized(value: Any) -> str:
    reject_floats(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"


def validate_case_record(record: dict[str, Any]) -> None:
    reject_floats(record, "case_record")
    if set(record) != {"input", "output"}:
        raise _ve("case record must contain typed input and output")
    expected = analyze(record["input"])
    for field in expected:
        if serialized(record["output"].get(field)) != serialized(expected[field]):
            raise _ve(f"{record['input']['fixture_id']}: injected or invalid {field}")
    if set(record["output"]) != set(expected):
        raise _ve("unexpected output field")


MUTATIONS = ("float_leakage", "zero_log_zero", "unnormalised_spectrum", "splitting_degree_one", "algebraic_entropy_claim")


def _injection_fixture(name: str) -> str:
    if name == "splitting_degree_one":
        return "s1_sqrt2"
    if name == "zero_log_zero":
        return "s1_pure"
    return "s1_mixed_half"


def _apply_injection(name: str, record: dict[str, Any]) -> dict[str, Any]:
    if name == "float_leakage":
        raise _ve("float refused at the public boundary", role="injection", received="float")
    if name == "zero_log_zero":
        record["output"]["entropy"]["quantity_type"] = "UNDEFINED_LOG_ZERO"
        return record
    if name == "unnormalised_spectrum":
        record["input"]["matrix"][0][0] = "3/2"
        return record
    if name == "splitting_degree_one":
        record["output"]["splitting_field"]["spectrum_degree_over_q"] = 1
        return record
    record["output"]["entropy"]["verdict"] = "CARRIED"
    return record


def injected_record(name: str) -> dict[str, Any]:
    if name not in MUTATIONS:
        raise _ve("unknown injection", received=name)
    case = next(item for item in fixtures() if item["fixture_id"] == _injection_fixture(name))
    record = {"input": copy.deepcopy(case), "output": analyze(case)}
    return _apply_injection(name, record)


def _reject_verdict_mix(args: Any, parser: argparse.ArgumentParser) -> None:
    if args.verdict_only and (args.inject or args.intervals is not None):
        parser.error("--verdict-only cannot be combined with --inject or --intervals")


def _reject_cyclotomic_mix(args: Any, parser: argparse.ArgumentParser) -> None:
    if args.cyclotomic_characteristic and (args.verdict_only or args.inject or args.intervals is not None):
        parser.error("--cyclotomic-characteristic cannot be combined with another output mode")


def _reject_spectral_mix(args: Any, parser: argparse.ArgumentParser) -> None:
    mixed = args.cyclotomic_characteristic or args.verdict_only or args.inject or args.intervals is not None
    if args.spectral_roots and mixed:
        parser.error("--spectral-roots cannot be combined with another output mode")


def _run_inject(args: Any) -> int:
    try:
        validate_case_record(injected_record(args.inject))
    except ValueError as exc:
        print(f"INJECTION_REJECTED {args.inject}: {exc}")
        return 1
    print(f"INJECTION_SURVIVED {args.inject}")
    return 2


def _verdict_report(interface: Path | None) -> dict[str, Any]:
    return {
        "authority_effect": "None",
        "schema": "c750_b01_verdict_v1",
        "cases": [{"input": case, "entropy": entropy_verdict(case)} for case in fixtures(interface)],
    }


def _interval_report(interface: Path | None, precision: int) -> dict[str, Any]:
    return {
        "authority_effect": "None",
        "intervals": [
            {"fixture_id": case["fixture_id"], "interval": entropy_interval(case, precision)}
            for case in fixtures(interface)
        ],
    }


def _select_report(args: Any) -> dict[str, Any]:
    if args.spectral_roots:
        import polynomial_roots
        return polynomial_roots.report(args.interface)
    if args.cyclotomic_characteristic:
        import cyclotomic_density
        return cyclotomic_density.characteristic_report(args.interface)
    if args.verdict_only:
        return _verdict_report(args.interface)
    if args.intervals is not None:
        return _interval_report(args.interface, args.intervals)
    return report(args.interface)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inject", choices=MUTATIONS)
    parser.add_argument("--intervals", type=int)
    parser.add_argument("--interface", type=Path)
    parser.add_argument("--verdict-only", action="store_true")
    parser.add_argument("--cyclotomic-characteristic", action="store_true")
    parser.add_argument("--spectral-roots", action="store_true")
    args = parser.parse_args()
    _reject_verdict_mix(args, parser)
    _reject_cyclotomic_mix(args, parser)
    _reject_spectral_mix(args, parser)
    if args.inject:
        return _run_inject(args)
    sys.stdout.buffer.write(serialized(_select_report(args)).encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
