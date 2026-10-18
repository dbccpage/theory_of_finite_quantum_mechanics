"""Exact eigenvalue-to-factor binding over the declared real coefficient field.

Origin: code/rust/src/linear_algebra/spectral_factors.rs, which states exact
matrix/root/irreducible-factor binding over the real coefficient field, with
no numerical splitting degree, multiplicative dependence, or new admission.
Claim: urn:omega:fqm:linear-algebra:spectral-factor-binding:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_spectral_factors.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 8; AST Sonar cognitive complexity max 6; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 8.
Scope Fence: This file binds admitted roots to E-irreducible factors. It does
not claim a splitting degree, multiplicative dependence, or a new density
admission, and it does not admit floats.
"""

from __future__ import annotations

import copy
import json
import sys
from fractions import Fraction as Q
from typing import Any, Mapping, cast

from . import cyclo_density as field
from . import entropy_dichotomy as kernel
from . import field_factors as factors
from . import field_squares as real
from . import poly_roots as roots


SCHEMA = "spectral_factor_binding_v1"
SCOPE = "EXACT_EIGENVALUE_FACTORS_AND_REAL_CARRIER_TRANSPORT_NO_DEGREE_OR_DEPENDENCE"
RESULT_FIELDS = {
    "schema", "authority_effect", "scope", "input", "carrier_conductor", "embedding",
    "coefficient_field", "real_generator_radicand", "characteristic_polynomial",
    "factorization", "root_certificate", "root_assignments", "factor_root_counts",
    "carrier_transport",
}
ASSIGNMENT_FIELDS = {"root_index", "factor_index", "multiplicity"}
TRANSPORT_FIELDS = {
    "rule", "carrier_degree_over_real_field", "all_roots_real", "root_field", "degree_identity",
}
CyclotomicPolynomial = list[field.Cyclotomic]


class SpectralBindingError(ValueError):
    """One violated spectral-binding invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SpectralBindingError:
    return SpectralBindingError(invariant, parameters)


def _json_string(value: str, role: str) -> None:
    for character in value:
        if 0xD800 <= ord(character) <= 0xDFFF:
            raise _fail("spectral_binding: non-scalar Unicode text is not admitted", role=role)


def _json_object(value: dict[Any, Any], role: str) -> None:
    if any(type(key) is not str for key in value):
        raise _fail("spectral_binding: JSON object keys must be strings", role=role)
    for key, item in value.items():
        _json_types(key, role)
        _json_types(item, role)


def _json_list(value: list[Any], role: str) -> None:
    for item in value:
        _json_types(item, role)


def _json_types(value: object, role: str) -> None:
    """Require scalar Unicode and exact JSON types, without coercion."""
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is dict:
        _json_object(value, role)
        return
    if type(value) is list:
        _json_list(value, role)
        return
    if type(value) is str:
        _json_string(value, role)
        return
    if value is None or type(value) is int or type(value) is bool:
        return
    raise _fail(
        "spectral_binding: exact native JSON types required",
        role=role,
        received=type(value).__name__,
    )


def _json_text(value: object) -> str:
    _json_types(value, "json")
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def _exact_counter(value: object, role: str) -> int:
    _json_types(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where an exact integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("spectral_binding: exact integer required", role=role, received=type(value).__name__)


def _require_fields(value: object, expected: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise _fail(f"spectral_binding: exact {label} field census required", reason="type")
    checked = cast(dict[str, Any], value)
    if set(checked) != expected:
        raise _fail(f"spectral_binding: exact {label} field census required", reason="fields")
    return checked


def _from_real(conductor: int, coordinates: tuple[Q, Q]) -> field.Cyclotomic:
    """Embed derived E coordinates directly, never through bounded input parsing."""
    radicand, pair = real._domain(conductor, coordinates)
    a, b = pair
    coefficients: tuple[Q, ...]
    if conductor == 1:
        coefficients = (a,)
    elif conductor in (3, 4):
        coefficients = (a, Q(0))
    elif conductor == 8:
        coefficients = (a, b, Q(0), -b)
    else:
        coefficients = (a - b, Q(0), -2 * b, -2 * b)
    value = field.Cyclotomic(conductor, coefficients)
    if value.real_coordinates() != (a, b, radicand):
        raise _fail("spectral_binding: inverse real-coordinate map failed", conductor=conductor)
    return value


def _charpoly(matrix: list[list[field.Cyclotomic]]) -> list[object]:
    # The entropy kernel annotates this routine over Q. The carrier is cyclotomic.
    return cast(list[object], kernel.charpoly(cast(list[list[Q]], matrix)))


def _as_cyclotomic(conductor: int, value: object) -> field.Cyclotomic:
    if isinstance(value, field.Cyclotomic):
        return value
    if type(value) is int or isinstance(value, Q):
        return field.Cyclotomic.rational(conductor, value)
    raise _fail(
        "spectral_binding: characteristic coefficient is not an exact cyclotomic",
        received=type(value).__name__,
    )


def _coefficient(conductor: int, radicand: int, value: object) -> tuple[Q, Q]:
    element = _as_cyclotomic(conductor, value)
    if element != element.conjugate():
        raise _fail("spectral_binding: characteristic coefficient is not self-conjugate")
    real_a, real_b, actual_radicand = element.real_coordinates()
    if actual_radicand != radicand or _from_real(conductor, (real_a, real_b)) != element:
        raise _fail("spectral_binding: characteristic coefficient round-trip failed")
    return real_a, real_b


def _as_case(case: object) -> dict[str, Any]:
    _json_types(case, "input")
    if type(case) is not dict:
        raise _fail("spectral_binding: typed input object required", received=type(case).__name__)
    return cast(dict[str, Any], case)


def _context(case: object) -> tuple[int, int, list[tuple[Q, Q]], int]:
    checked = _as_case(case)
    matrix = field.validated_matrix(checked)
    conductor = _exact_counter(checked["conductor"], "conductor")
    radicand = real.RADICANDS[conductor]
    coefficients = [_coefficient(conductor, radicand, value) for value in _charpoly(matrix)]
    return conductor, radicand, coefficients, len(matrix)


def _validate_nested(
    case: object,
    conductor: int,
    polynomial: list[tuple[Q, Q]],
    factorization: object,
    root_certificate: object,
) -> None:
    try:
        factors.validate_factorization(conductor, polynomial, factorization)
        roots.validate_spectrum(case, root_certificate)
    except (KeyError, IndexError, TypeError, AttributeError, ZeroDivisionError) as error:
        # Malformed supplied data must not leak decoder/container exceptions.
        # Existing ValueError subclasses, including genuine resource refusals,
        # pass through unchanged.
        raise _fail("spectral_binding: malformed nested arithmetic certificate") from error


def _embed_factors(conductor: int, rows: list[dict[str, Any]]) -> list[CyclotomicPolynomial]:
    embedded: list[CyclotomicPolynomial] = []
    for row in rows:
        coordinates = factors._parse_polynomial(conductor, row["polynomial"])
        embedded.append([_from_real(conductor, coordinate) for coordinate in coordinates])
    return embedded


def _sequences(polynomials: list[CyclotomicPolynomial]) -> list[list[list[Q]]]:
    return [kernel.sturm_sequence(cast(list[Q], polynomial)) for polynomial in polynomials]


def _eval_zero(polynomial: CyclotomicPolynomial, value: Q) -> bool:
    return kernel._poly_eval(cast(list[Q], polynomial), value) == 0


def _root_count(
    polynomial: CyclotomicPolynomial,
    sequence: list[list[Q]],
    lower: Q,
    upper: Q,
) -> int:
    if lower == upper:
        return int(_eval_zero(polynomial, lower))
    return kernel._open_root_count(sequence, lower, upper)


def _owner_indexes(
    lower: Q,
    upper: Q,
    polynomials: list[CyclotomicPolynomial],
    sequences: list[list[list[Q]]],
) -> list[int]:
    owners: list[int] = []
    for factor_index, polynomial in enumerate(polynomials):
        count = _root_count(polynomial, sequences[factor_index], lower, upper)
        if count not in (0, 1):
            raise _fail("spectral_binding: factor root count is not zero or one", count=count)
        if count:
            owners.append(factor_index)
    return owners


def _one_owner(owners: list[int]) -> int:
    if len(owners) != 1:
        raise _fail(
            "spectral_binding: each root requires exactly one irreducible factor owner",
            owners=len(owners),
        )
    return owners[0]


def _require_factor_multiplicity(row: dict[str, Any], multiplicity: object) -> None:
    if row["multiplicity"] != multiplicity:
        raise _fail("spectral_binding: root multiplicity differs from its irreducible factor")


def _factor_row_list(factorization: dict[str, Any]) -> list[dict[str, Any]]:
    rows = factorization["factors"]
    if type(rows) is not list:
        raise _fail("spectral_binding: exact factor list required", received=type(rows).__name__)
    return cast(list[dict[str, Any]], rows)


def _assign_root(
    root_index: int,
    row: dict[str, Any],
    factor_rows: list[dict[str, Any]],
    polynomials: list[CyclotomicPolynomial],
    sequences: list[list[list[Q]]],
    counts: list[int],
) -> dict[str, int]:
    lower, upper = kernel.parse_rat(row["lower"]), kernel.parse_rat(row["upper"])
    factor_index = _one_owner(_owner_indexes(lower, upper, polynomials, sequences))
    multiplicity = factor_rows[factor_index]["multiplicity"]
    _require_factor_multiplicity(row, multiplicity)
    counts[factor_index] += 1
    return {"root_index": root_index, "factor_index": factor_index, "multiplicity": multiplicity}


def _require_exhaustion(counts: list[int], polynomials: list[CyclotomicPolynomial]) -> None:
    expected = [len(polynomial) - 1 for polynomial in polynomials]
    if counts != expected:
        raise _fail(
            "spectral_binding: distinct roots do not exhaust every irreducible factor",
            counts=counts,
            expected=expected,
        )


def _require_weighted(counts: list[int], rows: list[dict[str, Any]], dimension: int) -> None:
    total = 0
    for count, row in zip(counts, rows):
        total += count * row["multiplicity"]
    if total != dimension:
        raise _fail(
            "spectral_binding: weighted factor root census differs from matrix dimension",
            total=total,
            dimension=dimension,
        )


def _census(
    conductor: int,
    factorization: dict[str, Any],
    root_certificate: dict[str, Any],
    dimension: int,
) -> tuple[list[dict[str, int]], list[int]]:
    """Count ownership only after both full nested certificates were checked."""
    factor_rows = _factor_row_list(factorization)
    polynomials = _embed_factors(conductor, factor_rows)
    sequences = _sequences(polynomials)
    counts = [0] * len(polynomials)
    assignments = [
        _assign_root(root_index, row, factor_rows, polynomials, sequences, counts)
        for root_index, row in enumerate(root_certificate["spectrum"])
    ]
    _require_exhaustion(counts, polynomials)
    _require_weighted(counts, factor_rows, dimension)
    return assignments, counts


def _transport(conductor: int) -> dict[str, Any]:
    degree = 1 if conductor == 1 else 2
    return {
        "rule": "REAL_SPECTRAL_FIELD_BASE_CHANGE_V1",
        "carrier_degree_over_real_field": degree,
        "all_roots_real": True,
        "root_field": "E_ALL_CHARACTERISTIC_ROOTS",
        "degree_identity": "[K(all_roots):K]=[E(all_roots):E]",
    }


def bind_spectral_factors(case: object) -> dict[str, Any]:
    """Bind every distinct eigenvalue to its E-irreducible factor and exponent."""
    conductor, radicand, polynomial, dimension = _context(case)
    factorization = factors.factor_polynomial(conductor, polynomial)
    root_certificate = roots.exact_spectrum(case)
    _validate_nested(case, conductor, polynomial, factorization, root_certificate)
    assignments, counts = _census(conductor, factorization, root_certificate, dimension)
    return {
        "schema": SCHEMA,
        "authority_effect": "None",
        "scope": SCOPE,
        "input": copy.deepcopy(case),
        "carrier_conductor": conductor,
        "embedding": field.embedding(conductor),
        "coefficient_field": factors._field(radicand),
        "real_generator_radicand": radicand,
        "characteristic_polynomial": factors._wire(polynomial),
        "factorization": factorization,
        "root_certificate": root_certificate,
        "root_assignments": assignments,
        "factor_root_counts": counts,
        "carrier_transport": _transport(conductor),
    }


def _require_metadata(certificate: dict[str, Any], conductor: int, radicand: int) -> None:
    expected: dict[str, object] = {
        "schema": SCHEMA,
        "authority_effect": "None",
        "scope": SCOPE,
        "carrier_conductor": conductor,
        "real_generator_radicand": radicand,
        "coefficient_field": factors._field(radicand),
    }
    for key, value in expected.items():
        if type(certificate[key]) is not type(value) or certificate[key] != value:
            raise _fail("spectral_binding: metadata or coefficient-field binding differs", field=key)


def _require_input_binding(
    certificate: dict[str, Any],
    case: object,
    conductor: int,
    polynomial: list[tuple[Q, Q]],
) -> None:
    if _json_text(certificate["input"]) != _json_text(case):
        raise _fail("spectral_binding: original typed input binding differs")
    if _json_text(certificate["embedding"]) != _json_text(field.embedding(conductor)):
        raise _fail("spectral_binding: frozen embedding binding differs")
    parsed = factors._parse_polynomial(conductor, certificate["characteristic_polynomial"])
    if parsed != polynomial:
        raise _fail("spectral_binding: characteristic polynomial binding differs")


def _require_one_assignment(actual: object, expected_row: dict[str, int]) -> None:
    checked = _require_fields(actual, ASSIGNMENT_FIELDS, "root assignment")
    for key in ASSIGNMENT_FIELDS:
        _exact_counter(checked[key], key)
    if checked != expected_row:
        raise _fail("spectral_binding: root factor assignment or multiplicity differs")


def _require_assignments(actual: object, expected: list[dict[str, int]]) -> None:
    if type(actual) is not list or len(actual) != len(expected):
        rows = len(actual) if type(actual) is list else None
        raise _fail("spectral_binding: root assignment census differs", rows=rows, expected=len(expected))
    for row, expected_row in zip(actual, expected):
        _require_one_assignment(row, expected_row)


def _require_counts(actual: object, expected: list[int]) -> None:
    if type(actual) is not list:
        raise _fail("spectral_binding: factor root counts require exact integers", reason="type")
    for value in actual:
        _exact_counter(value, "factor_root_count")
    if list(actual) != expected:
        raise _fail("spectral_binding: factor distinct-root census differs")


def _require_transport(actual: object, conductor: int) -> None:
    checked = _require_fields(actual, TRANSPORT_FIELDS, "carrier transport")
    # Only after input, factorization, containment and full root census checks
    # is the real-field base-change premise admitted. No degree value follows.
    for key, value in _transport(conductor).items():
        if type(checked[key]) is not type(value) or checked[key] != value:
            raise _fail("spectral_binding: carrier transport premise differs", field=key)


def validate_spectral_factor_binding(case: object, certificate: object) -> None:
    """Reconstruct and recount supplied evidence, not whole-producer JSON equality."""
    conductor, radicand, polynomial, dimension = _context(case)
    _json_types(certificate, "certificate")
    checked = _require_fields(certificate, RESULT_FIELDS, "result")
    _require_metadata(checked, conductor, radicand)
    _require_input_binding(checked, case, conductor, polynomial)
    _validate_nested(case, conductor, polynomial, checked["factorization"], checked["root_certificate"])
    expected_assignments, expected_counts = _census(
        conductor, checked["factorization"], checked["root_certificate"], dimension
    )
    _require_assignments(checked["root_assignments"], expected_assignments)
    _require_counts(checked["factor_root_counts"], expected_counts)
    _require_transport(checked["carrier_transport"], conductor)


def dispatch(request: object) -> dict[str, Any]:
    _json_types(request, "request")
    checked = _require_fields(request, {"operation", "input"}, "request")
    operation = checked["operation"]
    if type(operation) is not str or operation != "bind_spectral_factors":
        raise _fail(
            "spectral_binding: bind_spectral_factors operation required",
            received=type(operation).__name__,
        )
    return bind_spectral_factors(checked["input"])


def _reject_inexact(token: str) -> None:
    raise _fail("spectral_binding: inexact JSON number forbidden", token=token)


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise _fail("spectral_binding: stdin request only; no CLI arguments permitted")
        request = json.loads(
            sys.stdin.buffer.read(),
            parse_int=real._integer_from_text,
            parse_float=_reject_inexact,
            parse_constant=_reject_inexact,
        )
        result = dispatch(request)
        output = _json_text(result) + "\n"
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write(output.encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
