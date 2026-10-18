"""Exact finite C750 T561--564 kernel. AuthorityEffect: None.

The entropy verdict is conditional on cited Baker input A1 and real-log facts.
It is not an arithmetic test for transcendence. Exact PSD validation and rational
Sturm entropy enclosures cover encoded rational symmetric matrices up to d=5.
Explicit splitting/dependence output additionally requires a characteristic
polynomial with rational roots and at most one distinct quadratic pair. The
cyclotomic density path additionally implements the five launch scalar fields
for purity verdicts and intervals, not splitting/dependence. Bounds are unchanged.
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
from typing import Any

_DATA_DIR = Path(__file__).resolve().parent.parent / "qm" / "data"


class RefusedAtBudget(ValueError):
    """No mathematical negative follows from this computational refusal."""


class UnsupportedExactScope(ValueError):
    """The general theorem remains separate from this implemented domain."""


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
# Operational ceilings for newly implemented algorithms; these do not rename
# the launch's dependence-search or approximation-series bounds.
RATIONAL_ROOT_RESOURCE_LIMIT = 100000
STURM_SUBDIVISION_RESOURCE_LIMIT = 4096
CLASS = {"S1": (2, 4), "S2": (3, 3), "S3": (2, 8), "S4": (4, 8),
         "S5": (5, 5), "S6": (4, 1), "S7": (3, 1), "S8": (4, 4)}
PHI = {1: 1, 3: 2, 4: 2, 5: 4, 8: 4}
INPUT_KEYS = {"fixture_id", "system_id", "conductor", "matrix", "scope"}
INTERFACE = _DATA_DIR / "rational_quadratic_fixtures.json"


def rat(q: Q | int) -> str:
    q = Q(q)
    return f"{q.numerator}/{q.denominator}"


def reject_floats(value: Any, path: str = "object") -> None:
    if isinstance(value, float):
        raise ValueError(f"float leakage at {path}")
    if isinstance(value, dict):
        for key, item in value.items():
            reject_floats(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_floats(item, f"{path}[{index}]")


def parse_rat(value: Any, *, bounded: bool = False) -> Q:
    if not isinstance(value, str):
        raise ValueError("rational input must be an a/b string")
    try:
        q = Q(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational input") from exc
    if value != rat(q):
        raise ValueError("rational input must be reduced a/b with positive denominator")
    if bounded and (abs(q.numerator) > MAX_INPUT or q.denominator > MAX_INPUT):
        raise RefusedAtBudget("rational_input bound 4096 exhausted")
    return q


def prime_factors(value: int, budget: _Budget | None = None) -> dict[int, int]:
    """Trial division with an explicit candidate budget; no failed-search claim."""
    value = abs(value)
    if value == 0:
        raise ValueError("zero has no prime exponent vector")
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
        raise ValueError("log argument must be strictly positive")
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
        raise ValueError("negative discriminant")
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
    previous = [[Q(i == j) for j in range(n)] for i in range(n)]
    coefficients = [Q(1)]
    for degree in range(1, n + 1):
        product = multiply(matrix, previous)
        coefficient = -sum((product[i][i] for i in range(n)), Q(0)) / degree
        coefficients.append(coefficient)
        previous = [[product[i][j] + (coefficient if i == j else 0)
                     for j in range(n)] for i in range(n)]
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
        raise ValueError("division by the zero polynomial")
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
        raise ValueError("nonzero remainder in exact polynomial division")
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


def _find_rational_root(poly: list[Q], budget: _Budget) -> Q | None:
    """Rational-root theorem on [0,1], justified by prior exact density checks.

    None means every rational-root candidate in that interval was tested. A
    factorization or enumeration budget failure raises separately.
    """
    if poly[-1] == 0:
        return Q(0)
    if _poly_eval(poly, Q(1)) == 0:
        return Q(1)
    denominator = lcm(*(value.denominator for value in poly))
    integer = [value.numerator * (denominator // value.denominator) for value in poly]
    content = reduce(gcd, integer)
    integer = [value // content for value in integer]
    numerators = _divisors(abs(integer[-1]), budget)
    denominators = _divisors(abs(integer[0]), budget)
    for numerator in numerators:
        for denominator in denominators:
            budget.spend()
            if numerator <= denominator and gcd(numerator, denominator) == 1:
                candidate = Q(numerator, denominator)
                if _poly_eval(poly, candidate) == 0:
                    return candidate
    return None


def _quadratic_square(poly: list[Q]) -> list[Q] | None:
    if len(poly) != 5 or poly[0] != 1:
        return None
    linear = poly[1] / 2
    constant = (poly[2] - linear * linear) / 2
    quadratic = [Q(1), linear, constant]
    return quadratic if poly_product(quadratic, quadratic) == poly else None


def validate_psd(matrix: list[list[Q]]) -> None:
    """Exact rational Schur complements, including singular zero-pivot cases.

    A positive pivot gives a congruence to pivot direct-sum Schur complement.
    A zero diagonal with a nonzero incident entry has a negative 2x2 principal
    minor. Each successful step eliminates a row/column; no search is involved.
    """
    current = [row[:] for row in matrix]
    while current:
        if any(current[i][i] < 0 for i in range(len(current))):
            raise ValueError("negative eigenvalue: exact Schur complement is not positive semidefinite")
        for i in range(len(current)):
            if current[i][i] == 0 and any(current[i][j] for j in range(len(current))):
                raise ValueError("negative eigenvalue: zero diagonal has a nonzero off-diagonal entry")
        pivot = next((i for i in range(len(current)) if current[i][i] > 0), None)
        if pivot is None:
            return
        indices = [i for i in range(len(current)) if i != pivot]
        value = current[pivot][pivot]
        current = [[current[i][j] - current[i][pivot] * current[pivot][j] / value
                    for j in indices] for i in indices]


def validated_matrix(case: dict[str, Any]) -> list[list[Q]]:
    reject_floats(case, "input")
    if set(case) != INPUT_KEYS or not isinstance(case["fixture_id"], str):
        raise ValueError("typed input requires exactly the five interface fields")
    if not case["fixture_id"]:
        raise ValueError("fixture_id: nonempty string required")
    if case["system_id"] not in CLASS:
        raise ValueError("system missing from frozen class")
    n, conductor = CLASS[case["system_id"]]
    if type(case["conductor"]) is not int or case["conductor"] != conductor:
        raise ValueError("frozen conductor mismatch")
    raw = case["matrix"]
    if not isinstance(raw, list) or len(raw) > MAX_D:
        raise RefusedAtBudget("matrix_dimension_max=5 exhausted")
    if len(raw) != n or any(not isinstance(row, list) or len(row) != n for row in raw):
        raise ValueError("frozen system dimension mismatch")
    matrix = [[parse_rat(x, bounded=True) for x in row] for row in raw]
    if any(matrix[i][j] != matrix[j][i] for i in range(n) for j in range(n)):
        raise ValueError("input is not real symmetric; complex carrier matrices require another exact implementation")
    if sum((matrix[i][i] for i in range(n)), Q(0)) != 1:
        raise ValueError("unnormalised spectrum: trace must equal one")
    if case["system_id"] == "S8":
        if case["scope"] != "S8_DIMENSION_ONLY_PROXY":
            raise ValueError("S8 code support unresolved; dimension-only proxy label required")
    elif case["scope"] != "DECLARED_SYSTEM_STATE":
        raise ValueError("state scope label mismatch")
    if case["system_id"] in {"S6", "S7"}:
        if any(matrix[i][j] for i in range(n) for j in range(n) if i != j):
            raise ValueError("frozen ladder states must be diagonal")
    if case["system_id"] == "S6":
        if matrix[0][0] <= 0:
            raise ValueError("S6 requires a positive geometric ladder")
        ratio = matrix[1][1] / matrix[0][0]
        if not 0 < ratio < 1 or any(matrix[i][i] != matrix[0][0] * ratio**i for i in range(n)):
            raise ValueError("S6 requires the declared decreasing geometric ladder")
    validate_psd(matrix)
    return matrix


def polynomial_spectrum(coefficients: list[Q]) -> tuple[list[dict[str, Any]], list[Q]]:
    """Graph-independent extraction of rational roots and one quadratic pair.

    Repeated quadratic factors are supported. Other residual factors retain an
    explicit unsupported-splitting/dependence outcome, not a mathematical claim.
    """
    roots: list[dict[str, Any]] = []
    reconstructed = [Q(1)]
    remaining = coefficients[:]
    if len(coefficients) > MAX_D + 1:
        raise RefusedAtBudget("characteristic_degree_max=5 exhausted")
    budget = _Budget(RATIONAL_ROOT_RESOURCE_LIMIT,
                    "IMPLEMENTATION_RESOURCE_LIMIT: rational-root search units are trial-factor candidates, generated divisors, and divisor-pair candidates")
    multiplicity = 1
    while len(remaining) > 3:
        quadratic = _quadratic_square(remaining)
        if quadratic is not None:
            remaining, multiplicity = quadratic, 2
            break
        root = _find_rational_root(remaining, budget)
        if root is None:
            raise UnsupportedExactScope(f"residual characteristic degree {len(remaining)-1}: splitting/dependence beyond one quadratic pair is unsupported; no negative result")
        while len(remaining) > 1 and _poly_eval(remaining, root) == 0:
            remaining = _poly_exact_div(remaining, [Q(1), -root])
            roots.append(rational_root(root))
            reconstructed = poly_product(reconstructed, [Q(1), -root])
    if len(remaining) == 2:
        root = -remaining[1] / remaining[0]
        roots.append(rational_root(root))
        reconstructed = poly_product(reconstructed, [Q(1), -root])
    elif len(remaining) == 3:
        _, linear, constant = remaining
        coefficient, d = sqrt_rational(linear * linear - 4 * constant)
        center, coefficient = -linear / 2, coefficient / 2
        for _ in range(multiplicity):
            reconstructed = poly_product(reconstructed, remaining)
            if d == 1:
                roots.extend([rational_root(center - coefficient), rational_root(center + coefficient)])
            else:
                roots.extend([quadratic_root(center, -coefficient, d), quadratic_root(center, coefficient, d)])
    rational = sorted([r for r in roots if r["kind"] == "rational"], key=lambda r: Q(r["value"]))
    quadratic = sorted([r for r in roots if r["kind"] == "quadratic"],
                       key=lambda r: (Q(r["center"]), r["radicand"], Q(r["coefficient"])))
    quadratic_pairs = {(r["center"], abs(Q(r["coefficient"])), r["radicand"]) for r in quadratic}
    if len(quadratic_pairs) > 1:
        raise UnsupportedExactScope("multiple quadratic pairs: dependence support refused; no negative independence result")
    spectrum: list[dict[str, Any]] = []
    for root in rational + quadratic:
        if spectrum and spectrum[-1]["root"] == root:
            spectrum[-1]["multiplicity"] += 1
        else:
            spectrum.append({"root": root, "multiplicity": 1})
    return spectrum, reconstructed


def row_basis(rows: list[list[Q]]) -> tuple[list[int], list[list[Q]]]:
    """Greedy exact Q row basis and reconstruction coordinates."""
    pivots: list[tuple[int, list[Q], list[Q]]] = []
    indices: list[int] = []
    for index, original in enumerate(rows):
        residual = original[:]
        for pivot, normalized, _ in pivots:
            factor = residual[pivot]
            residual = [a - factor * b for a, b in zip(residual, normalized)]
        pivot = next((i for i, value in enumerate(residual) if value), None)
        if pivot is not None:
            factor = residual[pivot]
            pivots.append((pivot, [x / factor for x in residual], []))
            indices.append(index)
    basis = [rows[i] for i in indices]
    # Reduce a basis copy while tracking each row as a combination of originals.
    tracked: list[tuple[int, list[Q], list[Q]]] = []
    rank = len(basis)
    for i, original in enumerate(basis):
        residual = original[:]
        representation = [Q(i == j) for j in range(rank)]
        for pivot, normalized, coeffs in tracked:
            factor = residual[pivot]
            residual = [a - factor * b for a, b in zip(residual, normalized)]
            representation = [a - factor * b for a, b in zip(representation, coeffs)]
        pivot = next(j for j, value in enumerate(residual) if value)
        scale = residual[pivot]
        tracked.append((pivot, [x / scale for x in residual], [x / scale for x in representation]))
    coordinates = []
    for original in rows:
        residual, representation = original[:], [Q(0)] * rank
        for pivot, normalized, coeffs in tracked:
            factor = residual[pivot]
            residual = [a - factor * b for a, b in zip(residual, normalized)]
            representation = [a + factor * b for a, b in zip(representation, coeffs)]
        if any(residual):
            raise AssertionError("Q row basis failed reconstruction")
        denominator = lcm(*(x.denominator for x in representation))
        relation = [denominator] + [-x.numerator * (denominator // x.denominator) for x in representation]
        divisor = reduce(gcd, relation)
        if any(abs(x // divisor) > MAX_COEFFICIENT for x in relation):
            raise RefusedAtBudget("dependence_integer_coefficient_abs_max=64 exhausted in exact coordinates")
        coordinates.append(representation)
    return indices, coordinates


def dependence(spectrum: list[dict[str, Any]]) -> dict[str, Any]:
    arguments = [entry["root"] for entry in spectrum
                 if entry["root"] != rational_root(Q(0))]
    pair = [q for q in arguments if q["kind"] == "quadratic"]
    exponent_maps = [valuations(Q(q["value"])) for q in arguments if q["kind"] == "rational"]
    norm_factors: dict[int, int] = {}
    if pair:
        if len(pair) != 2:
            raise UnsupportedExactScope("quadratic conjugate pair not available")
        center, coefficient = Q(pair[0]["center"]), Q(pair[0]["coefficient"])
        norm = center**2 - coefficient**2 * pair[0]["radicand"]
        if norm <= 0:
            raise ValueError("quadratic log arguments must be strictly positive")
        norm_factors = valuations(norm)
    primes = sorted({p for factors in exponent_maps + [norm_factors] for p in factors})
    generators: list[dict[str, Any]] = [{"kind": "prime", "value": p} for p in primes]
    if pair:
        generators.append({"kind": "quadratic_ratio", "numerator": pair[1], "denominator": pair[0]})
    rows: list[list[Q]] = []
    for q in arguments:
        if q["kind"] == "rational":
            factors = valuations(Q(q["value"]))
            rows.append([Q(factors.get(p, 0)) for p in primes] + ([Q(0)] if pair else []))
        else:
            sign = 1 if Q(q["coefficient"]) > 0 else -1
            rows.append([Q(norm_factors.get(p, 0), 2) for p in primes] + [Q(sign, 2)])
    indices, coordinates = row_basis(rows)
    return {"status": "EXACT", "method": "PRIME_AND_CONJUGATE_RATIO_Q_ROW_BASIS" if pair else "PRIME_EXPONENT_Q_ROW_BASIS",
            "arguments": arguments, "generators": generators,
            "exponent_rows": [[rat(q) for q in row] for row in rows],
            "basis_argument_indices": indices, "coordinates": [[rat(q) for q in row] for row in coordinates]}


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
        raise ValueError("verdict domain requires a previously validated purity witness")
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
        raise ValueError("spectrum product does not match characteristic polynomial")
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
        raise ValueError("series interval requires 1<=q<=2 and positive epsilon")
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
        raise ValueError("log interval requires a strictly positive rational; log(0) is never evaluated")
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
    # The known sign ln(q)<=0 prevents a loose upper endpoint from making the
    # entropy lower bound negative near q=1. This uses the same real-log input.
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
        raise ValueError("squarefree factor multiplicities failed exact characteristic-polynomial reconstruction")
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
    return sum(left != right for left, right in zip(signs, signs[1:]))


def _open_root_count(sequence: list[list[Q]], lower: Q, upper: Q) -> int:
    """Distinct roots in the OPEN interval (lower, upper).

    Ignoring zero signs makes V(lower)-V(upper) count (lower,upper]; subtract
    an upper-endpoint root explicitly. Midpoint roots are then recorded once.
    """
    return (_variations(sequence, lower) - _variations(sequence, upper)
            - int(_poly_eval(sequence[0], upper) == 0))


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


def _sturm_enclosures(coefficients: list[Any], bits: int, budget: _Budget | None,
                       *, clusters: bool) -> list[tuple[Q, Q, int, int]]:
    budget = budget or _Budget(STURM_SUBDIVISION_RESOURCE_LIMIT,
                              "IMPLEMENTATION_RESOURCE_LIMIT: sturm_subdivisions")
    tolerance = Q(1, 2**bits)
    result: list[tuple[Q, Q, int, int]] = []
    for original, multiplicity in squarefree_factors(coefficients):
        factor = original[:]
        for endpoint in [Q(0), Q(1)]:
            if len(factor) > 1 and _poly_eval(factor, endpoint) == 0:
                result.append((endpoint, endpoint, 1, multiplicity))
                factor = _poly_exact_div(factor, [Q(1), -endpoint])
        if len(factor) == 1:
            continue
        sequence = sturm_sequence(factor)
        count = _open_root_count(sequence, Q(0), Q(1))
        if count != len(factor) - 1:
            raise ValueError("Sturm root census does not place every density eigenvalue in [0,1]")
        pending = [(Q(0), Q(1), count)]
        while pending:
            lower, upper, count = pending.pop()
            if not count:
                continue
            if upper - lower <= tolerance and (clusters or (count == 1 and lower > 0)):
                result.append((lower, upper, count, multiplicity))
                continue
            budget.spend()
            midpoint = (lower + upper) / 2
            exact = _poly_eval(factor, midpoint) == 0
            left = _open_root_count(sequence, lower, midpoint)
            right = _open_root_count(sequence, midpoint, upper)
            if left < 0 or right < 0 or left + right + int(exact) != count:
                raise ValueError("Sturm subdivision lost or double-counted an eigenvalue")
            if exact:
                result.append((midpoint, midpoint, 1, multiplicity))
            pending.extend([(midpoint, upper, right), (lower, midpoint, left)])
    if sum(count * multiplicity for _, _, count, multiplicity in result) != len(coefficients) - 1:
        raise ValueError("Sturm multiplicity census differs from the characteristic degree")
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


def _entropy_interval_from_characteristic(coefficients: list[Any], k: int, *,
                                           cyclotomic_embedding: dict[str, Any] | None = None) -> dict[str, Any]:
    """Counted dyadic root clusters with a uniform modulus for -x*ln(x).

    Called after density admission. No root-separation or positive-eigenvalue
    lower bound is required. See entropy_cluster_bounds.md for the uniform
    d*(k+12)<=220 subdivision and 64-series-term success bounds.
    """
    if type(k) is not int or not 0 <= k <= MAX_K:
        raise RefusedAtBudget("approximation_k_max=32 exhausted or invalid precision")
    epsilon, dimension = Q(1, 2**k), len(coefficients) - 1
    bits = k + 12
    tolerance = Q(1, 2**bits)
    radius = tolerance * (bits + 2)
    resource = _Budget(STURM_SUBDIVISION_RESOURCE_LIMIT,
                       "IMPLEMENTATION_RESOURCE_LIMIT: sturm_subdivisions")
    enclosures = sturm_spectral_clusters(coefficients, bits, resource)
    lower, upper, terms = Q(0), Q(0), 0
    if sum(count * multiplicity for _, _, count, multiplicity in enclosures) != dimension:
        raise ValueError("Sturm spectral enclosure multiplicity sum differs from input dimension")
    for a, b, count, multiplicity in enclosures:
        if any(type(value) is not int or value < 1 for value in (count, multiplicity)):
            raise ValueError("Sturm cluster count and multiplicity must be positive integers")
        if (not 0 <= a <= b <= 1 or b - a > tolerance or (a == b and count != 1)
                or (a * 2**bits).denominator != 1 or (b * 2**bits).denominator != 1):
            raise ValueError("Sturm cluster geometry or width violates the dyadic contract")
        if a == b and a in {Q(0), Q(1)}:
            continue
        midpoint = (a + b) / 2
        log_lo, log_hi, used_terms = log_interval(midpoint, epsilon / (8 * dimension))
        error_radius = radius if a != b else Q(0)
        lower += count * multiplicity * max(Q(0), -midpoint * log_hi - error_radius)
        upper += count * multiplicity * (-midpoint * log_lo + error_radius)
        terms = max(terms, used_terms)
    result = {"authority_effect": "None", "quantity_type": "APPROXIMATION_NOT_MEMBERSHIP",
              "metric": "ABSOLUTE_REAL_ERROR", "k": k, "lower": rat(lower), "upper": rat(upper),
              "midpoint": rat((lower + upper) / 2), "width": rat(upper - lower),
              "error_bound": rat(epsilon), "max_series_terms_used": terms,
              "root_isolation": "EXACT_RATIONAL_STURM_SPECTRAL_CLUSTERS",
              "approximation_algorithm": "DYADIC_STURM_CLUSTERS_WITH_UNIFORM_ENTROPY_MODULUS",
              "spectral_count_convention": "OPEN_BINS_PLUS_EXACT_SINGLETONS",
              "cluster_precision_bits": bits, "uniform_entropy_radius": rat(radius),
              "sturm_subdivision_proved_bound": dimension * bits,
              "log_shift_proved_bound": bits + 1, "series_terms_proved_bound": 64,
              "sturm_subdivisions_used": resource.limit - resource.remaining,
              "sturm_subdivision_limit": resource.limit,
              "sturm_resource_limit_kind": "IMPLEMENTATION_RESOURCE_LIMIT",
              "input_dimension": dimension,
              "spectral_enclosures": [{"lower": rat(a), "upper": rat(b),
                                       "distinct_root_count": count, "multiplicity": multiplicity}
                                      for a, b, count, multiplicity in enclosures],
              "analytic_input": "REAL_LOG_ATANH_TAIL_AND_UNIFORM_ENTROPY_MODULUS",
              "transcendence_anchor": "A1"}
    if cyclotomic_embedding is not None:
        import cyclotomic_density
        result["root_isolation"] = cyclotomic_density.ROOT_ISOLATION
        result["embedding"] = cyclotomic_embedding
    validate_interval(result)
    return result


def validate_interval(interval: dict[str, Any]) -> None:
    """Validate type/width/multiplicity metadata; this is not a root proof.

    The producer's exact Sturm construction establishes the enclosures. Merely
    passing this structural validator cannot establish that invented endpoints
    contain any particular matrix's eigenvalues.
    """
    reject_floats(interval, "entropy_interval")
    if interval.get("quantity_type") != "APPROXIMATION_NOT_MEMBERSHIP" or interval.get("metric") != "ABSOLUTE_REAL_ERROR":
        raise ValueError("interval must be approximation, never carrier membership")
    k = interval.get("k")
    if type(k) is not int or not 0 <= k <= MAX_K:
        raise ValueError("invalid interval precision")
    lo, hi, midpoint = (parse_rat(interval[key]) for key in ("lower", "upper", "midpoint"))
    if lo < 0 or lo > hi or midpoint != (lo + hi) / 2:
        raise ValueError("invalid rational entropy enclosure")
    if parse_rat(interval["width"]) != hi - lo or hi - lo > Q(1, 2**k):
        raise ValueError("entropy interval exceeds declared error obligation")
    if parse_rat(interval["error_bound"]) != Q(1, 2**k):
        raise ValueError("entropy error bound does not equal 2^-k")
    used, limit = interval.get("sturm_subdivisions_used"), interval.get("sturm_subdivision_limit")
    root_isolation = interval.get("root_isolation")
    if root_isolation == "EXACT_CYCLOTOMIC_REAL_STURM_SPECTRAL_CLUSTERS":
        import cyclotomic_density
        cyclotomic_density.validate_embedding(interval.get("embedding"))
    if (root_isolation not in {"EXACT_RATIONAL_STURM_SPECTRAL_CLUSTERS",
                               "EXACT_CYCLOTOMIC_REAL_STURM_SPECTRAL_CLUSTERS"}
            or interval.get("sturm_resource_limit_kind") != "IMPLEMENTATION_RESOURCE_LIMIT"
            or type(used) is not int or type(limit) is not int
            or limit != STURM_SUBDIVISION_RESOURCE_LIMIT or not 0 <= used <= limit):
        raise ValueError("invalid Sturm operational resource accounting")
    series_terms = interval.get("max_series_terms_used")
    if type(series_terms) is not int or not 0 <= series_terms <= MAX_TERMS:
        raise ValueError("invalid frozen series-term accounting")
    dimension, enclosures = interval.get("input_dimension"), interval.get("spectral_enclosures")
    if type(dimension) is not int or not 1 <= dimension <= MAX_D or not isinstance(enclosures, list):
        raise ValueError("invalid spectral enclosure dimension or list")
    bits = k + 12
    expected_bounds = {"cluster_precision_bits": bits,
                       "sturm_subdivision_proved_bound": dimension * bits,
                       "log_shift_proved_bound": bits + 1, "series_terms_proved_bound": 64}
    if (interval.get("approximation_algorithm") != "DYADIC_STURM_CLUSTERS_WITH_UNIFORM_ENTROPY_MODULUS"
            or interval.get("spectral_count_convention") != "OPEN_BINS_PLUS_EXACT_SINGLETONS"
            or any(type(interval.get(key)) is not int or interval[key] != value
                   for key, value in expected_bounds.items())
            or interval.get("uniform_entropy_radius") != rat(Q(bits + 2, 2**bits))
            or used > dimension * bits or series_terms > 64):
        raise ValueError("invalid proved cluster approximation bounds or count convention")
    total = 0
    for enclosure in enclosures:
        if set(enclosure) != {"lower", "upper", "distinct_root_count", "multiplicity"}:
            raise ValueError("spectral enclosure requires lower, upper, distinct_root_count, and multiplicity")
        count, multiplicity = enclosure["distinct_root_count"], enclosure["multiplicity"]
        if type(multiplicity) is not int or multiplicity < 1:
            raise ValueError("spectral enclosure multiplicity must be a positive integer")
        if type(count) is not int or count < 1:
            raise ValueError("spectral enclosure distinct root count must be a positive integer")
        a, b = parse_rat(enclosure["lower"]), parse_rat(enclosure["upper"])
        if (not 0 <= a <= b <= 1 or b - a > Q(1, 2**bits) or (a == b and count != 1)
                or (a * 2**bits).denominator != 1 or (b * 2**bits).denominator != 1):
            raise ValueError("spectral cluster geometry, width, or singleton root count is invalid")
        total += count * multiplicity
    if total != dimension:
        raise ValueError("spectral enclosure multiplicity sum differs from input dimension")


def fixtures(interface: Path | None = None) -> list[dict[str, Any]]:
    envelope = json.loads((interface or INTERFACE).read_text(encoding="utf-8"))
    reject_floats(envelope, "interface")
    return validate_fixture_batch(envelope["fixtures"])


def validate_fixture_batch(values: Any) -> list[dict[str, Any]]:
    if not isinstance(values, list) or not values:
        raise ValueError("fixtures: nonempty array required")
    if len(values) > MAX_FIXTURES:
        raise RefusedAtBudget("fixture_cases_max=64 exhausted")
    seen = set()
    for case in values:
        identity = case.get("fixture_id") if isinstance(case, dict) else None
        if not isinstance(identity, str) or not identity:
            raise ValueError("fixture_id: nonempty string required")
        if identity in seen:
            raise ValueError(f"fixture_id:{identity}: duplicate fixture ID")
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
        raise ValueError("case record must contain typed input and output")
    expected = analyze(record["input"])
    for field in expected:
        # Python structural equality conflates True with 1 and False with 0.
        # JSON serialization preserves primitive types recursively, including
        # integers nested inside spectrum entries and dependence coordinate data.
        if serialized(record["output"].get(field)) != serialized(expected[field]):
            raise ValueError(f"{record['input']['fixture_id']}: injected or invalid {field}")
    if set(record["output"]) != set(expected):
        raise ValueError("unexpected output field")


MUTATIONS = ("float_leakage", "zero_log_zero", "unnormalised_spectrum", "splitting_degree_one", "algebraic_entropy_claim")


def injected_record(name: str) -> dict[str, Any]:
    if name not in MUTATIONS:
        raise ValueError("unknown injection")
    fixture_id = "s1_sqrt2" if name == "splitting_degree_one" else "s1_pure" if name == "zero_log_zero" else "s1_mixed_half"
    case = next(case for case in fixtures() if case["fixture_id"] == fixture_id)
    record = {"input": copy.deepcopy(case), "output": analyze(case)}
    if name == "float_leakage":
        record["output"]["entropy"]["injected_float"] = float("0")
    elif name == "zero_log_zero":
        record["output"]["entropy"]["quantity_type"] = "UNDEFINED_LOG_ZERO"
    elif name == "unnormalised_spectrum":
        record["input"]["matrix"][0][0] = "3/2"
    elif name == "splitting_degree_one":
        record["output"]["splitting_field"]["spectrum_degree_over_q"] = 1
    elif name == "algebraic_entropy_claim":
        record["output"]["entropy"]["verdict"] = "CARRIED"
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inject", choices=MUTATIONS)
    parser.add_argument("--intervals", type=int)
    parser.add_argument("--interface", type=Path)
    parser.add_argument("--verdict-only", action="store_true")
    parser.add_argument("--cyclotomic-characteristic", action="store_true")
    parser.add_argument("--spectral-roots", action="store_true")
    args = parser.parse_args()
    if args.verdict_only and (args.inject or args.intervals is not None):
        parser.error("--verdict-only cannot be combined with --inject or --intervals")
    if args.cyclotomic_characteristic and (args.verdict_only or args.inject or args.intervals is not None):
        parser.error("--cyclotomic-characteristic cannot be combined with another output mode")
    if args.spectral_roots and (args.cyclotomic_characteristic or args.verdict_only or args.inject or args.intervals is not None):
        parser.error("--spectral-roots cannot be combined with another output mode")
    if args.inject:
        try:
            validate_case_record(injected_record(args.inject))
        except ValueError as exc:
            print(f"INJECTION_REJECTED {args.inject}: {exc}")
            return 1
        print(f"INJECTION_SURVIVED {args.inject}")
        return 2
    if args.spectral_roots:
        import polynomial_roots
        value = polynomial_roots.report(args.interface)
    elif args.cyclotomic_characteristic:
        import cyclotomic_density
        value = cyclotomic_density.characteristic_report(args.interface)
    elif args.verdict_only:
        value = {"authority_effect": "None", "schema": "c750_b01_verdict_v1", "cases": [
            {"input": case, "entropy": entropy_verdict(case)} for case in fixtures(args.interface)]}
    elif args.intervals is not None:
        value = {"authority_effect": "None", "intervals": [
            {"fixture_id": case["fixture_id"], "interval": entropy_interval(case, args.intervals)} for case in fixtures(args.interface)]}
    else:
        value = report(args.interface)
    sys.stdout.buffer.write(serialized(value).encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
