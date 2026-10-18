"""Exact real-field splitting degrees through polynomial degree five.

AuthorityEffect: None. Degree-five input is factored over its actual E.
Irreducible quintics use localized fixed algebras. Degrees are over E;
all-real carrier transport and multiplicative dependence are separate.
Polynomial coefficients use descending exact rational coordinate pairs.
"""

from __future__ import annotations

from fractions import Fraction as Q
import json
import sys
from typing import Any

from . import field_factors as factors
from . import splitting_deg as splitting
from . import field_squares as real
from . import quintic_split as quintic


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


def _fields(value: Any, expected: set[str], label: str) -> None:
    if type(value) is not dict or set(value) != expected:
        raise ValueError(f"compositum_degree: exact {label} field census required")


def _json_types(value: Any) -> None:
    """Reject implicit coercions throughout supplied native JSON certificates."""
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise ValueError("compositum_degree: JSON object keys must be strings")
        for item in value.values():
            _json_types(item)
    elif type(value) is list:
        for item in value:
            _json_types(item)
    elif value is not None and type(value) not in (str, int, bool):
        raise ValueError("compositum_degree: exact native JSON types required")


def _integer_list(value: Any, expected: list[int], label: str) -> None:
    if type(value) is not list or any(type(item) is not int for item in value):
        raise ValueError(f"compositum_degree: exact integer {label} required")
    if value != expected:
        raise ValueError(f"compositum_degree: {label} differs from factorization")


def _input(conductor: int, coefficients: Any) -> tuple[int, Polynomial]:
    radicand, values = factors._domain(conductor, coefficients)
    if len(values) > 6:
        raise ValueError("compositum_degree: polynomial degree must be at most five")
    return radicand, values


def _nonlinear_factors(certificate: dict[str, Any]) -> tuple[list[int], list[int]]:
    """Read only an already arithmetically validated factorization."""
    rows = certificate["factors"]
    indices = sorted((i for i, row in enumerate(rows) if len(row["polynomial"]) > 2),
                     key=lambda i: (len(rows[i]["polynomial"]) - 1, i))
    pattern = [len(rows[i]["polynomial"]) - 1 for i in indices]
    if tuple(pattern) not in {(), (2,), (3,), (4,), (5,), (2, 2), (2, 3)}:
        raise ValueError("compositum_degree: inconsistent degree-at-most-five factor pattern")
    return indices, pattern


def _quadratic_discriminant(polynomial: Polynomial, radicand: int) -> Coordinates:
    if len(polynomial) != 3 or polynomial[0] != ONE:
        raise ValueError("compositum_degree: monic quadratic factor required")
    _, linear, constant = polynomial
    return factors._add(factors._mul(linear, linear, radicand),
                        (-4 * constant[0], -4 * constant[1]))


def _make_leaf(conductor: int, radicand: int, index: int,
               polynomial: Polynomial) -> dict[str, Any]:
    degree = len(polynomial) - 1
    if degree == 2:
        discriminant = _quadratic_discriminant(polynomial, radicand)
        certificate = {
            "kind": "IRREDUCIBLE_QUADRATIC",
            "discriminant": real._wire(discriminant),
            "discriminant_square": real.square_certificate(conductor, discriminant),
        }
        extension_degree = 2
    elif degree == 5:
        certificate = quintic.quintic_splitting_degree(conductor, polynomial)
        extension_degree = certificate["degree_over_real_field"]
    else:
        certificate = splitting.irreducible_splitting_degree(conductor, polynomial)
        extension_degree = certificate["degree_over_real_field"]
    return {"factor_index": index, "polynomial_degree": degree,
            "degree_over_real_field": extension_degree, "certificate": certificate}


def _validate_leaf(conductor: int, radicand: int, index: int,
                   polynomial: Polynomial, row: Any) -> Leaf:
    _fields(row, LEAF_FIELDS, "factor certificate")
    for key in ("factor_index", "polynomial_degree", "degree_over_real_field"):
        if type(row[key]) is not int:
            raise ValueError(f"compositum_degree: exact integer leaf metadata required: {key}")
    degree = len(polynomial) - 1
    if row["factor_index"] != index or row["polynomial_degree"] != degree:
        raise ValueError("compositum_degree: leaf index or polynomial-degree binding differs")
    certificate = row["certificate"]
    if degree == 2:
        _fields(certificate, {"kind", "discriminant", "discriminant_square"}, "quadratic certificate")
        if type(certificate["kind"]) is not str or certificate["kind"] != "IRREDUCIBLE_QUADRATIC":
            raise ValueError("compositum_degree: irreducible quadratic kind required")
        discriminant = _quadratic_discriminant(polynomial, radicand)
        if discriminant == ZERO:
            raise ValueError("compositum_degree: irreducible quadratic has zero discriminant")
        if real._parse_coordinates(conductor, certificate["discriminant"]) != discriminant:
            raise ValueError("compositum_degree: quadratic discriminant binding differs")
        real.validate_square_certificate(conductor, discriminant, certificate["discriminant_square"])
        if certificate["discriminant_square"]["is_square"]:
            raise ValueError("compositum_degree: quadratic discriminant must be nonsquare in E")
        extension_degree, group = 2, "C2"
    elif degree in (3, 4):
        splitting.validate_splitting_degree(conductor, polynomial, certificate)
        discriminant = real._parse_coordinates(conductor, certificate["discriminant"])
        extension_degree, group = certificate["degree_over_real_field"], certificate["galois_group"]
    elif degree == 5:
        quintic.validate_quintic_degree(conductor, polynomial, certificate)
        discriminant = real._parse_coordinates(conductor, certificate["discriminant"])
        extension_degree, group = certificate["degree_over_real_field"], certificate["galois_group"]
    else:
        raise ValueError("compositum_degree: supported nonlinear leaf required")
    if row["degree_over_real_field"] != extension_degree:
        raise ValueError("compositum_degree: leaf splitting degree differs from arithmetic certificate")
    return extension_degree, discriminant, group


def _intersection_rule(pattern: list[int], right_group: str,
                       same_squareclass: bool | None) -> tuple[str, int]:
    if pattern == [2, 3] and right_group == "C3":
        if same_squareclass is not None:
            raise ValueError("compositum_degree: coprime C3 branch has no squareclass evidence")
        return "QUADRATIC_CYCLIC_CUBIC_COPRIME", 1
    if type(same_squareclass) is not bool:
        raise ValueError("compositum_degree: verified Boolean squareclass decision required")
    if pattern == [2, 2]:
        return (("QUADRATIC_QUADRATIC_SAME_FIELD", 2) if same_squareclass
                else ("QUADRATIC_QUADRATIC_DISJOINT", 1))
    if pattern == [2, 3] and right_group == "S3":
        return (("QUADRATIC_SYMMETRIC_CUBIC_CONTAINED", 2) if same_squareclass
                else ("QUADRATIC_SYMMETRIC_CUBIC_DISJOINT", 1))
    raise ValueError("compositum_degree: inconsistent nonlinear intersection pattern")


def _make_intersection(conductor: int, indices: list[int], pattern: list[int],
                       leaves: list[Leaf]) -> dict[str, Any] | None:
    if len(leaves) < 2:
        return None
    left, right = leaves[0][1], leaves[1][1]
    coprime = pattern == [2, 3] and leaves[1][2] == "C3"
    certificate = None if coprime else real.squareclass_certificate(conductor, left, right)
    same = None if certificate is None else certificate["same_squareclass"]
    rule, intersection_degree = _intersection_rule(pattern, leaves[1][2], same)
    return {"factor_indices": indices[:], "rule": rule,
            "left_discriminant": real._wire(left), "right_discriminant": real._wire(right),
            "squareclass_certificate": certificate, "intersection_degree": intersection_degree}


def _validate_intersection(conductor: int, indices: list[int], pattern: list[int],
                           leaves: list[Leaf], certificate: Any) -> int:
    if len(leaves) < 2:
        if certificate is not None:
            raise ValueError("compositum_degree: fewer than two nonlinear factors require null intersection")
        return 1
    _fields(certificate, INTERSECTION_FIELDS, "intersection certificate")
    _integer_list(certificate["factor_indices"], indices, "intersection factor indices")
    if type(certificate["rule"]) is not str or type(certificate["intersection_degree"]) is not int:
        raise ValueError("compositum_degree: exact intersection metadata types required")
    left, right = leaves[0][1], leaves[1][1]
    if (real._parse_coordinates(conductor, certificate["left_discriminant"]) != left
            or real._parse_coordinates(conductor, certificate["right_discriminant"]) != right):
        raise ValueError("compositum_degree: ordered discriminant binding differs")
    squareclass = certificate["squareclass_certificate"]
    if pattern == [2, 3] and leaves[1][2] == "C3":
        if squareclass is not None:
            raise ValueError("compositum_degree: coprime C3 branch requires null squareclass certificate")
        same = None
    else:
        real.validate_squareclass_certificate(conductor, left, right, squareclass)
        same = squareclass["same_squareclass"]
    rule, intersection_degree = _intersection_rule(pattern, leaves[1][2], same)
    if certificate["rule"] != rule or certificate["intersection_degree"] != intersection_degree:
        raise ValueError("compositum_degree: intersection rule or degree differs from arithmetic evidence")
    return intersection_degree


def _combined_degree(leaves: list[Leaf], intersection_degree: int) -> int:
    product = 1
    for degree, _, _ in leaves:
        product *= degree
    if intersection_degree < 1 or product % intersection_degree:
        raise ValueError("compositum_degree: splitting degrees do not divide by intersection exactly")
    return product // intersection_degree


def compositum_splitting_degree(conductor: int, coefficients: Any) -> dict[str, Any]:
    """Compute the supported splitting degree over E, retaining original content."""
    radicand, values = _input(conductor, coefficients)
    factorization = factors.factor_polynomial(conductor, values)
    _json_types(factorization)
    factors.validate_factorization(conductor, values, factorization)
    indices, pattern = _nonlinear_factors(factorization)
    rows, leaves = [], []
    for index in indices:
        polynomial = factors._parse_polynomial(conductor, factorization["factors"][index]["polynomial"])
        row = _make_leaf(conductor, radicand, index, polynomial)
        _json_types(row)
        leaves.append(_validate_leaf(conductor, radicand, index, polynomial, row))
        rows.append(row)
    intersection = _make_intersection(conductor, indices, pattern, leaves)
    _json_types(intersection)
    intersection_degree = _validate_intersection(conductor, indices, pattern, leaves, intersection)
    return {"schema": SCHEMA, "authority_effect": "None", "conductor": conductor,
            "real_generator_radicand": radicand, "coefficient_field": factors._field(radicand),
            "coefficients": factors._wire(values), "factorization": factorization,
            "nonlinear_factor_indices": indices, "degree_pattern": pattern,
            "factor_certificates": rows, "intersection_certificate": intersection,
            "degree_over_real_field": _combined_degree(leaves, intersection_degree),
            "algorithm": ALGORITHM, "scope": SCOPE}


def _validate_compositum_degree(conductor: int, coefficients: Any, result: Any) -> None:
    radicand, values = _input(conductor, coefficients)
    _fields(result, RESULT_FIELDS, "result")
    _json_types(result)
    for key in ("schema", "authority_effect", "coefficient_field", "algorithm", "scope"):
        if type(result[key]) is not str:
            raise ValueError(f"compositum_degree: string metadata required: {key}")
    for key in ("conductor", "real_generator_radicand", "degree_over_real_field"):
        if type(result[key]) is not int:
            raise ValueError(f"compositum_degree: exact integer metadata required: {key}")
    expected = {"schema": SCHEMA, "authority_effect": "None", "conductor": conductor,
                "real_generator_radicand": radicand, "coefficient_field": factors._field(radicand),
                "algorithm": ALGORITHM, "scope": SCOPE}
    if any(result[key] != value for key, value in expected.items()):
        raise ValueError("compositum_degree: metadata or real-field binding differs")
    if factors._parse_polynomial(conductor, result["coefficients"]) != values:
        raise ValueError("compositum_degree: original polynomial binding differs")
    factors.validate_factorization(conductor, values, result["factorization"])
    indices, pattern = _nonlinear_factors(result["factorization"])
    _integer_list(result["nonlinear_factor_indices"], indices, "nonlinear factor indices")
    _integer_list(result["degree_pattern"], pattern, "nonlinear degree pattern")
    rows = result["factor_certificates"]
    if type(rows) is not list or len(rows) != len(indices):
        raise ValueError("compositum_degree: full nonlinear factor certificate census required")
    leaves = []
    for index, row in zip(indices, rows):
        polynomial = factors._parse_polynomial(conductor, result["factorization"]["factors"][index]["polynomial"])
        leaves.append(_validate_leaf(conductor, radicand, index, polynomial, row))
    intersection_degree = _validate_intersection(conductor, indices, pattern, leaves,
                                                  result["intersection_certificate"])
    if result["degree_over_real_field"] != _combined_degree(leaves, intersection_degree):
        raise ValueError("compositum_degree: final splitting degree differs from checked Galois intersection")


def validate_compositum_degree(conductor: int, coefficients: Any, certificate: Any) -> None:
    """Validate supplied input-bound arithmetic proofs, not producer JSON equality."""
    try:
        _validate_compositum_degree(conductor, coefficients, certificate)
    except (KeyError, IndexError, TypeError, AttributeError, ZeroDivisionError) as error:
        raise ValueError("compositum_degree: malformed nested certificate or input") from error


def dispatch(request: Any) -> dict[str, Any]:
    _fields(request, {"operation", "conductor", "coefficients"}, "request")
    _json_types(request)
    if type(request["operation"]) is not str or request["operation"] != "compositum_splitting_degree":
        raise ValueError("compositum_degree: compositum_splitting_degree operation required")
    conductor = request["conductor"]
    coefficients = factors._parse_polynomial(conductor, request["coefficients"])
    return compositum_splitting_degree(conductor, coefficients)


def _reject_inexact(token: str) -> None:
    raise ValueError(f"compositum_degree: inexact JSON number forbidden: {token}")


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise ValueError("compositum_degree: stdin request only; no CLI arguments permitted")
        request = json.loads(sys.stdin.buffer.read(), parse_int=real._integer_from_text,
                             parse_float=_reject_inexact, parse_constant=_reject_inexact)
        result = dispatch(request)
        output = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                            allow_nan=False) + "\n"
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write(output.encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
