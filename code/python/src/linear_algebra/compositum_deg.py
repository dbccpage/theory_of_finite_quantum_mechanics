"""Exact splitting degrees over E by Galois intersection of small factors.

Origin: code/rust/src/linear_algebra/compositum_deg.rs, which states the exact
small-factor Galois intersections over E, not an unconditional K-degree, and
names the quadratic-quadratic and quadratic-cubic intersection rules.
Claim: urn:omega:fqm:linear-algebra:compositum-degree:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_compositum_deg.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 10; AST Sonar cognitive complexity max 12; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 10.
Scope Fence: the degree is the product of the leaf degrees divided by the
intersection degree. Python schema v2 also accepts one irreducible quintic
leaf. The Rust schema is v1 and leaves irreducible quintics unsupported.
This file does not claim an unconditional degree over K, carrier transport,
multiplicative dependence, or the Rust overflow error, and it does not admit
floats or Q(i).
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from typing import Any, Mapping

from . import field_factors as factors
from . import field_squares as real
from . import quintic_split as quintic
from . import splitting_deg as splitting
from .scalars import GaussianRational


Coordinates = tuple[Q, Q]
Polynomial = list[Coordinates]
Leaf = tuple[int, Coordinates, str]
ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))
SCHEMA = "real_field_compositum_degree_v2"
ALGORITHM = "EXACT_FACTOR_SPLITTING_DEGREES_AND_GALOIS_INTERSECTION"
SCOPE = "E_SPLITTING_DEGREE_AT_MOST_FIVE_NO_CARRIER_TRANSPORT_OR_DEPENDENCE"
RESULT_FIELDS = {
    "schema", "authority_effect", "conductor", "real_generator_radicand",
    "coefficient_field", "coefficients", "factorization", "nonlinear_factor_indices",
    "degree_pattern", "factor_certificates", "intersection_certificate",
    "degree_over_real_field", "algorithm", "scope",
}
LEAF_FIELDS = {"factor_index", "polynomial_degree", "degree_over_real_field", "certificate"}
INTERSECTION_FIELDS = {
    "factor_indices", "rule", "left_discriminant", "right_discriminant",
    "squareclass_certificate", "intersection_degree",
}
_REQUEST_FIELDS = {"operation", "conductor", "coefficients"}


class CompositumError(ValueError):
    """One violated compositum invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CompositumError:
    return CompositumError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_conductor(value: object) -> int:
    _refuse_float(value, "conductor")
    if type(value) is bool:
        raise _fail("boolean refused where a conductor was required", role="conductor")
    if type(value) is int:
        return value
    raise _fail("compositum_degree: exact integer conductor required", received=type(value).__name__)


def _refuse_coordinate(value: object, role: str) -> None:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational coordinate was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail(
            "Gaussian rational refused; compositum degrees in this module are over a real field",
            role=role,
        )


def _scan_coefficient(value: object, role: str) -> None:
    _refuse_coordinate(value, role)
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _refuse_coordinate(item, f"{role}[{index}]")


def _scan_coefficients(coefficients: object) -> None:
    _refuse_coordinate(coefficients, "coefficients")
    if isinstance(coefficients, (list, tuple)):
        for index, item in enumerate(coefficients):
            _scan_coefficient(item, f"coefficient[{index}]")


def _fields(value: object, expected: set[str], label: str) -> dict[str, Any]:
    if type(value) is dict and set(value) == expected:
        return value
    raise _fail("compositum_degree: exact field census required", label=label)


def _json_types(value: object) -> None:
    """Reject implicit coercions throughout supplied native JSON certificates."""
    if type(value) is dict:
        _json_object(value)
        return
    if type(value) is list:
        _json_list(value)
        return
    if value is not None and type(value) not in (str, int, bool):
        raise _fail("compositum_degree: exact native JSON types required", received=type(value).__name__)


def _json_object(value: dict[object, object]) -> None:
    if any(type(key) is not str for key in value):
        raise _fail("compositum_degree: JSON object keys must be strings")
    for item in value.values():
        _json_types(item)


def _json_list(value: list[object]) -> None:
    for item in value:
        _json_types(item)


def _integer_list(value: object, expected: list[int], label: str) -> None:
    if type(value) is not list or any(type(item) is not int for item in value):
        raise _fail("compositum_degree: exact integer list required", label=label)
    if value != expected:
        raise _fail("compositum_degree: integer list differs from factorization", label=label)


def _input(conductor: int, coefficients: object) -> tuple[int, Polynomial]:
    radicand, values = factors._domain(conductor, coefficients)
    if len(values) > 6:
        raise _fail("compositum_degree: polynomial degree must be at most five", length=len(values))
    return radicand, values


def _nonlinear_factors(certificate: dict[str, Any]) -> tuple[list[int], list[int]]:
    """Read only an already arithmetically validated factorization."""
    rows = certificate["factors"]
    indices = sorted(
        (i for i, row in enumerate(rows) if len(row["polynomial"]) > 2),
        key=lambda i: (len(rows[i]["polynomial"]) - 1, i),
    )
    pattern = [len(rows[i]["polynomial"]) - 1 for i in indices]
    if tuple(pattern) not in {(), (2,), (3,), (4,), (5,), (2, 2), (2, 3)}:
        raise _fail("compositum_degree: inconsistent degree-at-most-five factor pattern")
    return indices, pattern


def _quadratic_discriminant(polynomial: Polynomial, radicand: int) -> Coordinates:
    if len(polynomial) != 3 or polynomial[0] != ONE:
        raise _fail("compositum_degree: monic quadratic factor required")
    _, linear, constant = polynomial
    return factors._add(factors._mul(linear, linear, radicand), (-4 * constant[0], -4 * constant[1]))


def _require_degree(value: object, role: str) -> int:
    if type(value) is not int:
        raise _fail("compositum_degree: exact integer leaf metadata required", role=role)
    return value


def _quadratic_certificate(conductor: int, radicand: int, polynomial: Polynomial) -> dict[str, Any]:
    discriminant = _quadratic_discriminant(polynomial, radicand)
    return {
        "kind": "IRREDUCIBLE_QUADRATIC",
        "discriminant": real._wire(discriminant),
        "discriminant_square": real.square_certificate(conductor, discriminant),
    }


def _make_leaf(conductor: int, radicand: int, index: int, polynomial: Polynomial) -> dict[str, Any]:
    degree = len(polynomial) - 1
    if degree == 2:
        certificate: dict[str, Any] = _quadratic_certificate(conductor, radicand, polynomial)
        extension_degree = 2
    elif degree == 5:
        certificate = quintic.quintic_splitting_degree(conductor, polynomial)
        extension_degree = _require_degree(certificate["degree_over_real_field"], "degree_over_real_field")
    else:
        certificate = splitting.irreducible_splitting_degree(conductor, polynomial)
        extension_degree = _require_degree(certificate["degree_over_real_field"], "degree_over_real_field")
    return {
        "factor_index": index,
        "polynomial_degree": degree,
        "degree_over_real_field": extension_degree,
        "certificate": certificate,
    }


def _require_leaf_ints(row: dict[str, Any]) -> None:
    for key in ("factor_index", "polynomial_degree", "degree_over_real_field"):
        if type(row[key]) is not int:
            raise _fail("compositum_degree: exact integer leaf metadata required", role=key)


def _require_quadratic_kind(certificate: dict[str, Any]) -> None:
    _fields(certificate, {"kind", "discriminant", "discriminant_square"}, "quadratic certificate")
    if type(certificate["kind"]) is not str or certificate["kind"] != "IRREDUCIBLE_QUADRATIC":
        raise _fail("compositum_degree: irreducible quadratic kind required")


def _quadratic_binding(
    conductor: int,
    radicand: int,
    polynomial: Polynomial,
    certificate: dict[str, Any],
) -> Coordinates:
    discriminant = _quadratic_discriminant(polynomial, radicand)
    if discriminant == ZERO:
        raise _fail("compositum_degree: irreducible quadratic has zero discriminant")
    if real._parse_coordinates(conductor, certificate["discriminant"]) != discriminant:
        raise _fail("compositum_degree: quadratic discriminant binding differs")
    real.validate_square_certificate(conductor, discriminant, certificate["discriminant_square"])
    if certificate["discriminant_square"]["is_square"]:
        raise _fail("compositum_degree: quadratic discriminant must be nonsquare in E")
    return discriminant


def _quadratic_leaf(
    conductor: int,
    radicand: int,
    polynomial: Polynomial,
    certificate: dict[str, Any],
) -> Leaf:
    _require_quadratic_kind(certificate)
    discriminant = _quadratic_binding(conductor, radicand, polynomial, certificate)
    extension_degree, group = 2, "C2"
    return extension_degree, discriminant, group


def _higher_leaf(conductor: int, degree: int, polynomial: Polynomial, certificate: dict[str, Any]) -> Leaf:
    if degree in (3, 4):
        splitting.validate_splitting_degree(conductor, polynomial, certificate)
    elif degree == 5:
        quintic.validate_quintic_degree(conductor, polynomial, certificate)
    else:
        raise _fail("compositum_degree: supported nonlinear leaf required", degree=degree)
    extension_degree = _require_degree(certificate["degree_over_real_field"], "degree_over_real_field")
    discriminant = real._parse_coordinates(conductor, certificate["discriminant"])
    return extension_degree, discriminant, str(certificate["galois_group"])


def _validate_leaf(
    conductor: int,
    radicand: int,
    index: int,
    polynomial: Polynomial,
    row: object,
) -> Leaf:
    record = _fields(row, LEAF_FIELDS, "factor certificate")
    _require_leaf_ints(record)
    degree = len(polynomial) - 1
    if record["factor_index"] != index or record["polynomial_degree"] != degree:
        raise _fail("compositum_degree: leaf index or polynomial-degree binding differs")
    certificate = record["certificate"]
    if degree == 2:
        leaf = _quadratic_leaf(conductor, radicand, polynomial, certificate)
    else:
        leaf = _higher_leaf(conductor, degree, polynomial, certificate)
    if record["degree_over_real_field"] != leaf[0]:
        raise _fail("compositum_degree: leaf splitting degree differs from arithmetic certificate")
    return leaf


def _intersection_rule(pattern: list[int], right_group: str, same_squareclass: bool | None) -> tuple[str, int]:
    if pattern == [2, 3] and right_group == "C3":
        if same_squareclass is not None:
            raise _fail("compositum_degree: coprime C3 branch has no squareclass evidence")
        return "QUADRATIC_CYCLIC_CUBIC_COPRIME", 1
    if type(same_squareclass) is not bool:
        raise _fail("compositum_degree: verified Boolean squareclass decision required")
    if pattern == [2, 2]:
        return (("QUADRATIC_QUADRATIC_SAME_FIELD", 2) if same_squareclass
                else ("QUADRATIC_QUADRATIC_DISJOINT", 1))
    if pattern == [2, 3] and right_group == "S3":
        return (("QUADRATIC_SYMMETRIC_CUBIC_CONTAINED", 2) if same_squareclass
                else ("QUADRATIC_SYMMETRIC_CUBIC_DISJOINT", 1))
    raise _fail("compositum_degree: inconsistent nonlinear intersection pattern")


def _make_intersection(
    conductor: int,
    indices: list[int],
    pattern: list[int],
    leaves: list[Leaf],
) -> dict[str, Any] | None:
    if len(leaves) < 2:
        return None
    left, right = leaves[0][1], leaves[1][1]
    coprime = pattern == [2, 3] and leaves[1][2] == "C3"
    certificate = None if coprime else real.squareclass_certificate(conductor, left, right)
    same = None if certificate is None else certificate["same_squareclass"]
    rule, intersection_degree = _intersection_rule(pattern, leaves[1][2], same)
    return {
        "factor_indices": indices[:],
        "rule": rule,
        "left_discriminant": real._wire(left),
        "right_discriminant": real._wire(right),
        "squareclass_certificate": certificate,
        "intersection_degree": intersection_degree,
    }


def _require_intersection_metadata(certificate: dict[str, Any]) -> None:
    if type(certificate["rule"]) is not str or type(certificate["intersection_degree"]) is not int:
        raise _fail("compositum_degree: exact intersection metadata types required")


def _discriminants_match(conductor: int, certificate: dict[str, Any], left: Coordinates, right: Coordinates) -> bool:
    if real._parse_coordinates(conductor, certificate["left_discriminant"]) != left:
        return False
    return real._parse_coordinates(conductor, certificate["right_discriminant"]) == right


def _squareclass_decision(
    conductor: int,
    pattern: list[int],
    leaves: list[Leaf],
    squareclass: object,
    left: Coordinates,
    right: Coordinates,
) -> bool | None:
    if pattern == [2, 3] and leaves[1][2] == "C3":
        if squareclass is not None:
            raise _fail("compositum_degree: coprime C3 branch requires null squareclass certificate")
        return None
    real.validate_squareclass_certificate(conductor, left, right, squareclass)
    if not isinstance(squareclass, dict):
        raise _fail("compositum_degree: verified Boolean squareclass decision required")
    decision = squareclass["same_squareclass"]
    if isinstance(decision, bool):
        return decision
    raise _fail("compositum_degree: verified Boolean squareclass decision required")


def _validate_intersection(
    conductor: int,
    indices: list[int],
    pattern: list[int],
    leaves: list[Leaf],
    certificate: object,
) -> int:
    if len(leaves) < 2:
        if certificate is not None:
            raise _fail("compositum_degree: fewer than two nonlinear factors require null intersection")
        return 1
    record = _fields(certificate, INTERSECTION_FIELDS, "intersection certificate")
    _integer_list(record["factor_indices"], indices, "intersection factor indices")
    _require_intersection_metadata(record)
    left, right = leaves[0][1], leaves[1][1]
    if not _discriminants_match(conductor, record, left, right):
        raise _fail("compositum_degree: ordered discriminant binding differs")
    same = _squareclass_decision(conductor, pattern, leaves, record["squareclass_certificate"], left, right)
    rule, intersection_degree = _intersection_rule(pattern, leaves[1][2], same)
    if record["rule"] != rule or record["intersection_degree"] != intersection_degree:
        raise _fail("compositum_degree: intersection rule or degree differs from arithmetic evidence")
    return intersection_degree


def _combined_degree(leaves: list[Leaf], intersection_degree: int) -> int:
    product = 1
    for degree, _, _ in leaves:
        product *= degree
    if intersection_degree < 1 or product % intersection_degree:
        raise _fail("compositum_degree: splitting degrees do not divide by intersection exactly")
    return product // intersection_degree


def _assembled_degree(
    conductor: int,
    radicand: int,
    values: Polynomial,
    factorization: dict[str, Any],
) -> dict[str, Any]:
    indices, pattern = _nonlinear_factors(factorization)
    rows: list[dict[str, Any]] = []
    leaves: list[Leaf] = []
    for index in indices:
        polynomial = factors._parse_polynomial(conductor, factorization["factors"][index]["polynomial"])
        row = _make_leaf(conductor, radicand, index, polynomial)
        _json_types(row)
        leaves.append(_validate_leaf(conductor, radicand, index, polynomial, row))
        rows.append(row)
    intersection = _make_intersection(conductor, indices, pattern, leaves)
    _json_types(intersection)
    intersection_degree = _validate_intersection(conductor, indices, pattern, leaves, intersection)
    return {
        "schema": SCHEMA,
        "authority_effect": "None",
        "conductor": conductor,
        "real_generator_radicand": radicand,
        "coefficient_field": factors._field(radicand),
        "coefficients": factors._wire(values),
        "factorization": factorization,
        "nonlinear_factor_indices": indices,
        "degree_pattern": pattern,
        "factor_certificates": rows,
        "intersection_certificate": intersection,
        "degree_over_real_field": _combined_degree(leaves, intersection_degree),
        "algorithm": ALGORITHM,
        "scope": SCOPE,
    }


def compositum_splitting_degree(conductor: object, coefficients: object) -> dict[str, Any]:
    """Compute the supported splitting degree over E, retaining original content."""
    number = _require_conductor(conductor)
    _scan_coefficients(coefficients)
    radicand, values = _input(number, coefficients)
    factorization = factors.factor_polynomial(number, values)
    _json_types(factorization)
    factors.validate_factorization(number, values, factorization)
    return _assembled_degree(number, radicand, values, factorization)


def _require_result_text(result: dict[str, Any], key: str) -> None:
    if type(result[key]) is not str:
        raise _fail("compositum_degree: string metadata required", role=key)


def _require_result_types(result: dict[str, Any]) -> None:
    for key in ("schema", "authority_effect", "coefficient_field", "algorithm", "scope"):
        _require_result_text(result, key)
    for key in ("conductor", "real_generator_radicand", "degree_over_real_field"):
        if type(result[key]) is not int:
            raise _fail("compositum_degree: exact integer metadata required", role=key)


def _result_binding(conductor: int, radicand: int) -> dict[str, object]:
    return {
        "schema": SCHEMA,
        "authority_effect": "None",
        "conductor": conductor,
        "real_generator_radicand": radicand,
        "coefficient_field": factors._field(radicand),
        "algorithm": ALGORITHM,
        "scope": SCOPE,
    }


def _require_result_binding(result: dict[str, Any], conductor: int, radicand: int, values: Polynomial) -> None:
    expected = _result_binding(conductor, radicand)
    if any(result[key] != value for key, value in expected.items()):
        raise _fail("compositum_degree: metadata or real-field binding differs")
    if factors._parse_polynomial(conductor, result["coefficients"]) != values:
        raise _fail("compositum_degree: original polynomial binding differs")


def _validated_leaves(
    conductor: int,
    radicand: int,
    result: dict[str, Any],
    indices: list[int],
) -> list[Leaf]:
    rows = result["factor_certificates"]
    if type(rows) is not list or len(rows) != len(indices):
        raise _fail("compositum_degree: full nonlinear factor certificate census required")
    leaves: list[Leaf] = []
    for index, row in zip(indices, rows):
        polynomial = factors._parse_polynomial(conductor, result["factorization"]["factors"][index]["polynomial"])
        leaves.append(_validate_leaf(conductor, radicand, index, polynomial, row))
    return leaves


def _validate_compositum_degree(conductor: int, coefficients: object, result: object) -> None:
    radicand, values = _input(conductor, coefficients)
    record = _fields(result, RESULT_FIELDS, "result")
    _json_types(record)
    _require_result_types(record)
    _require_result_binding(record, conductor, radicand, values)
    factors.validate_factorization(conductor, values, record["factorization"])
    indices, pattern = _nonlinear_factors(record["factorization"])
    _integer_list(record["nonlinear_factor_indices"], indices, "nonlinear factor indices")
    _integer_list(record["degree_pattern"], pattern, "nonlinear degree pattern")
    leaves = _validated_leaves(conductor, radicand, record, indices)
    intersection_degree = _validate_intersection(
        conductor, indices, pattern, leaves, record["intersection_certificate"]
    )
    if record["degree_over_real_field"] != _combined_degree(leaves, intersection_degree):
        raise _fail("compositum_degree: final splitting degree differs from checked Galois intersection")


def validate_compositum_degree(conductor: object, coefficients: object, certificate: object) -> None:
    """Validate supplied input-bound arithmetic proofs, not producer JSON equality."""
    number = _require_conductor(conductor)
    _scan_coefficients(coefficients)
    try:
        _validate_compositum_degree(number, coefficients, certificate)
    except (KeyError, IndexError, TypeError, AttributeError, ZeroDivisionError) as error:
        raise _fail("compositum_degree: malformed nested certificate or input") from error


def dispatch(request: object) -> dict[str, Any]:
    record = _fields(request, _REQUEST_FIELDS, "request")
    number = _require_conductor(record["conductor"])
    _json_types(record)
    if type(record["operation"]) is not str or record["operation"] != "compositum_splitting_degree":
        raise _fail("compositum_degree: compositum_splitting_degree operation required")
    coefficients = factors._parse_polynomial(number, record["coefficients"])
    return compositum_splitting_degree(number, coefficients)


def _reject_inexact(token: str) -> None:
    raise _fail("compositum_degree: inexact JSON number forbidden", token=token)


def _read_request() -> object:
    if len(sys.argv) != 1:
        raise _fail("compositum_degree: stdin request only; no CLI arguments permitted")
    return json.loads(
        sys.stdin.buffer.read(),
        parse_int=real._integer_from_text,
        parse_float=_reject_inexact,
        parse_constant=_reject_inexact,
    )


def main() -> int:
    try:
        result = dispatch(_read_request())
        output = json.dumps(
            result,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ) + "\n"
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write(output.encode("ascii"))
    return 0


def witness_same_field_degree() -> int:
    """Splitting degree of (x^2-2)(x^2-8) over Q, which is 2."""
    coefficients = [(Q(1), Q(0)), (Q(0), Q(0)), (Q(-10), Q(0)), (Q(0), Q(0)), (Q(16), Q(0))]
    degree = compositum_splitting_degree(1, coefficients)["degree_over_real_field"]
    return _require_degree(degree, "witness")


if __name__ == "__main__":
    raise SystemExit(main())
