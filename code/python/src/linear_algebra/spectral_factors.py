"""Exact eigenvalue-to-E-factor binding. AuthorityEffect: None.

The real-carrier base-change identity has checked spectral premises here;
no unknown numerical splitting degree or logarithm dependence is computed.
Original density admission and the existing root-isolation budget are retained.
"""

from __future__ import annotations

import copy
from fractions import Fraction as Q
import json
import sys
from typing import Any

from . import cyclo_density as field
from . import entropy_dichotomy as kernel
from . import poly_roots as roots
from . import field_factors as factors
from . import field_squares as real


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


def _fields(value: Any, expected: set[str], label: str) -> None:
    if type(value) is not dict or set(value) != expected:
        raise ValueError(f"spectral_binding: exact {label} field census required")


def _json_types(value: Any) -> None:
    """Require scalar Unicode and exact JSON types, without coercion."""
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise ValueError("spectral_binding: JSON object keys must be strings")
        for key, item in value.items():
            _json_types(key)
            _json_types(item)
    elif type(value) is list:
        for item in value:
            _json_types(item)
    elif type(value) is str:
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise ValueError("spectral_binding: non-scalar Unicode text is not admitted")
    elif value is not None and type(value) not in (int, bool):
        raise ValueError("spectral_binding: exact native JSON types required")


def _json_text(value: Any) -> str:
    _json_types(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def _from_real(conductor: int, coordinates: tuple[Q, Q]) -> field.Cyclotomic:
    """Embed derived E coordinates directly, never through bounded input parsing."""
    radicand, (a, b) = real._domain(conductor, coordinates)
    if conductor == 1:
        coefficients = (a,)
    elif conductor in (3, 4):
        coefficients = (a, Q(0))
    elif conductor == 8:
        coefficients = (a, b, Q(0), -b)
    else:  # The domain gate leaves only conductor five.
        coefficients = (a - b, Q(0), -2 * b, -2 * b)
    value = field.Cyclotomic(conductor, coefficients)
    if value.real_coordinates() != (a, b, radicand):
        raise ValueError("spectral_binding: inverse real-coordinate map failed")
    return value


def _context(case: Any) -> tuple[int, int, list[tuple[Q, Q]], int]:
    _json_types(case)
    matrix = field.validated_matrix(case)
    conductor = case["conductor"]
    radicand = real.RADICANDS[conductor]
    coefficients = []
    for value in kernel.charpoly(matrix):
        if not isinstance(value, field.Cyclotomic):
            value = field.Cyclotomic.rational(conductor, value)
        if value != value.conjugate():
            raise ValueError("spectral_binding: characteristic coefficient is not self-conjugate")
        a, b, actual_radicand = value.real_coordinates()
        if actual_radicand != radicand or _from_real(conductor, (a, b)) != value:
            raise ValueError("spectral_binding: characteristic coefficient round-trip failed")
        coefficients.append((a, b))
    return conductor, radicand, coefficients, len(matrix)


def _validate_nested(case: Any, conductor: int, polynomial: list[tuple[Q, Q]],
                     factorization: Any, root_certificate: Any) -> None:
    try:
        factors.validate_factorization(conductor, polynomial, factorization)
        roots.validate_spectrum(case, root_certificate)
    except (KeyError, IndexError, TypeError, AttributeError, ZeroDivisionError) as error:
        # Malformed supplied data must not leak decoder/container exceptions.
        # Existing ValueError subclasses, including genuine resource refusals,
        # pass through unchanged.
        raise ValueError("spectral_binding: malformed nested arithmetic certificate") from error


def _census(conductor: int, factorization: dict[str, Any], root_certificate: dict[str, Any],
            dimension: int) -> tuple[list[dict[str, int]], list[int]]:
    """Count ownership only after both full nested certificates were checked."""
    factor_rows = factorization["factors"]
    polynomials = [[_from_real(conductor, coordinate)
                    for coordinate in factors._parse_polynomial(conductor, row["polynomial"])]
                   for row in factor_rows]
    sequences = [kernel.sturm_sequence(polynomial) for polynomial in polynomials]
    counts, assignments = [0] * len(polynomials), []
    for root_index, row in enumerate(root_certificate["spectrum"]):
        lower, upper = kernel.parse_rat(row["lower"]), kernel.parse_rat(row["upper"])
        owners = []
        for factor_index, (polynomial, sequence) in enumerate(zip(polynomials, sequences)):
            count = (int(kernel._poly_eval(polynomial, lower) == 0) if lower == upper
                     else kernel._open_root_count(sequence, lower, upper))
            if count not in (0, 1):
                raise ValueError("spectral_binding: factor root count is not zero or one")
            if count:
                owners.append(factor_index)
        if len(owners) != 1:
            raise ValueError("spectral_binding: each root requires exactly one irreducible factor owner")
        factor_index = owners[0]
        multiplicity = factor_rows[factor_index]["multiplicity"]
        if row["multiplicity"] != multiplicity:
            raise ValueError("spectral_binding: root multiplicity differs from its irreducible factor")
        counts[factor_index] += 1
        assignments.append({"root_index": root_index, "factor_index": factor_index,
                            "multiplicity": multiplicity})
    if counts != [len(polynomial) - 1 for polynomial in polynomials]:
        raise ValueError("spectral_binding: distinct roots do not exhaust every irreducible factor")
    if sum(count * row["multiplicity"] for count, row in zip(counts, factor_rows)) != dimension:
        raise ValueError("spectral_binding: weighted factor root census differs from matrix dimension")
    return assignments, counts


def _transport(conductor: int) -> dict[str, Any]:
    return {"rule": "REAL_SPECTRAL_FIELD_BASE_CHANGE_V1",
            "carrier_degree_over_real_field": 1 if conductor == 1 else 2,
            "all_roots_real": True, "root_field": "E_ALL_CHARACTERISTIC_ROOTS",
            "degree_identity": "[K(all_roots):K]=[E(all_roots):E]"}


def bind_spectral_factors(case: Any) -> dict[str, Any]:
    """Bind every distinct eigenvalue to its E-irreducible factor and exponent."""
    conductor, radicand, polynomial, dimension = _context(case)
    factorization = factors.factor_polynomial(conductor, polynomial)
    root_certificate = roots.exact_spectrum(case)
    _validate_nested(case, conductor, polynomial, factorization, root_certificate)
    assignments, counts = _census(conductor, factorization, root_certificate, dimension)
    return {"schema": SCHEMA, "authority_effect": "None", "scope": SCOPE,
            "input": copy.deepcopy(case), "carrier_conductor": conductor,
            "embedding": field.embedding(conductor), "coefficient_field": factors._field(radicand),
            "real_generator_radicand": radicand, "characteristic_polynomial": factors._wire(polynomial),
            "factorization": factorization, "root_certificate": root_certificate,
            "root_assignments": assignments, "factor_root_counts": counts,
            "carrier_transport": _transport(conductor)}


def validate_spectral_factor_binding(case: Any, certificate: Any) -> None:
    """Reconstruct and recount supplied evidence, not whole-producer JSON equality."""
    conductor, radicand, polynomial, dimension = _context(case)
    _fields(certificate, RESULT_FIELDS, "result")
    _json_types(certificate)
    expected = {"schema": SCHEMA, "authority_effect": "None", "scope": SCOPE,
                "carrier_conductor": conductor, "real_generator_radicand": radicand,
                "coefficient_field": factors._field(radicand)}
    for key, value in expected.items():
        if type(certificate[key]) is not type(value) or certificate[key] != value:
            raise ValueError(f"spectral_binding: metadata or coefficient-field binding differs: {key}")
    if _json_text(certificate["input"]) != _json_text(case):
        raise ValueError("spectral_binding: original typed input binding differs")
    if _json_text(certificate["embedding"]) != _json_text(field.embedding(conductor)):
        raise ValueError("spectral_binding: frozen embedding binding differs")
    if factors._parse_polynomial(conductor, certificate["characteristic_polynomial"]) != polynomial:
        raise ValueError("spectral_binding: characteristic polynomial binding differs")
    _validate_nested(case, conductor, polynomial, certificate["factorization"], certificate["root_certificate"])
    expected_assignments, expected_counts = _census(
        conductor, certificate["factorization"], certificate["root_certificate"], dimension)
    assignments, counts = certificate["root_assignments"], certificate["factor_root_counts"]
    if type(assignments) is not list or len(assignments) != len(expected_assignments):
        raise ValueError("spectral_binding: root assignment census differs")
    for actual, expected_row in zip(assignments, expected_assignments):
        _fields(actual, ASSIGNMENT_FIELDS, "root assignment")
        if any(type(actual[key]) is not int for key in ASSIGNMENT_FIELDS):
            raise ValueError("spectral_binding: root indices and multiplicity require exact integers")
        if actual != expected_row:
            raise ValueError("spectral_binding: root factor assignment or multiplicity differs")
    if type(counts) is not list or any(type(value) is not int for value in counts):
        raise ValueError("spectral_binding: factor root counts require exact integers")
    if counts != expected_counts:
        raise ValueError("spectral_binding: factor distinct-root census differs")
    transport = certificate["carrier_transport"]
    _fields(transport, TRANSPORT_FIELDS, "carrier transport")
    # Only after input, factorization, containment and full root census checks
    # is the real-field base-change premise admitted. No degree value follows.
    for key, value in _transport(conductor).items():
        if type(transport[key]) is not type(value) or transport[key] != value:
            raise ValueError(f"spectral_binding: carrier transport premise differs: {key}")


def dispatch(request: Any) -> dict[str, Any]:
    _fields(request, {"operation", "input"}, "request")
    if type(request["operation"]) is not str or request["operation"] != "bind_spectral_factors":
        raise ValueError("spectral_binding: bind_spectral_factors operation required")
    return bind_spectral_factors(request["input"])


def _reject_inexact(token: str) -> None:
    raise ValueError(f"spectral_binding: inexact JSON number forbidden: {token}")


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise ValueError("spectral_binding: stdin request only; no CLI arguments permitted")
        request = json.loads(sys.stdin.buffer.read(), parse_int=real._integer_from_text,
                             parse_float=_reject_inexact, parse_constant=_reject_inexact)
        result = dispatch(request)
        output = _json_text(result) + "\n"
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write(output.encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
