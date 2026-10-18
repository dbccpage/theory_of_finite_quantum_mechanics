"""Exact ordered real polynomial root identities.

Origin: code/rust/src/linear_algebra/poly_roots.rs, which states exact ordered
root identities, not minimal polynomials or splitting degrees.
Claim: urn:omega:fqm:linear-algebra:ordered-real-polynomial-roots:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_poly_roots.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 6; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: This file does not claim a splitting degree, a minimal polynomial,
or multiplicative dependence. It does not admit floats or a complex carrier.
"""

from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Mapping, cast

from . import cyclo_density as field
from . import entropy_dichotomy as kernel


# Entropy-kernel polynomial routines are annotated over Q but evaluate field
# operations. Returned coefficients are lifted back onto this cyclotomic carrier.
REPRESENTATION = "ORDERED_REAL_POLYNOMIAL_ROOTS_V1"
SCOPE = "EXACT_ROOT_IDENTITIES_NO_SPLITTING_DEGREE_OR_DEPENDENCE"
Polynomial = list[field.Cyclotomic]
Factorization = list[tuple[Polynomial, int]]
Wire = list[dict[str, list[str]]]
_OUTPUT_FIELDS = {
    "representation",
    "carrier_conductor",
    "embedding",
    "characteristic_polynomial",
    "squarefree_factors",
    "squarefree_radical",
    "spectrum",
    "resource",
    "scope",
}
_ROOT_FIELDS = {
    "kind",
    "defining_polynomial",
    "lower",
    "upper",
    "endpoint_convention",
    "distinct_root_count",
    "multiplicity",
}
_RESOURCE_FIELDS = {"kind", "sturm_subdivisions", "sturm_subdivision_limit"}


class RootIdentityError(ValueError):
    """One violated root-identity invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> RootIdentityError:
    return RootIdentityError(invariant, parameters)


def _refuse_elements(values: list[Any] | tuple[Any, ...], role: str) -> None:
    for item in values:
        _refuse_floats(item, role)


def _refuse_floats(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, dict):
        for key, item in value.items():
            _refuse_floats(key, role)
            _refuse_floats(item, role)
        return
    if isinstance(value, list):
        _refuse_elements(value, role)
        return
    if isinstance(value, tuple):
        _refuse_elements(value, role)


def _exact_counter(value: object, role: str) -> int:
    _refuse_floats(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where an exact integer was required", role=role)
    if type(value) is int:
        return value
    raise _fail("root_identity: exact integer required", role=role, received=type(value).__name__)


def _as_case(case: object) -> dict[str, Any]:
    _refuse_floats(case, "input")
    if type(case) is not dict:
        raise _fail("root_identity: typed input object required", received=type(case).__name__)
    return cast(dict[str, Any], case)


def _require_same_conductor(conductor: int, value: field.Cyclotomic) -> None:
    if value.conductor != conductor:
        raise _fail(
            "root_identity: cyclotomic conductor differs from the declared carrier",
            conductor=conductor,
            received=value.conductor,
        )


def _lift_coefficient(conductor: int, value: object) -> field.Cyclotomic:
    if isinstance(value, field.Cyclotomic):
        _require_same_conductor(conductor, value)
        return value
    _refuse_floats(value, "coefficient")
    if isinstance(value, Q):
        return field.Cyclotomic.rational(conductor, value)
    return field.Cyclotomic.rational(conductor, _exact_counter(value, "coefficient"))


def _lift_polynomial(conductor: int, values: object) -> Polynomial:
    if not isinstance(values, list):
        raise _fail(
            "root_identity: polynomial coefficient list required",
            received=type(values).__name__,
        )
    return [_lift_coefficient(conductor, value) for value in values]


def _charpoly(matrix: list[list[field.Cyclotomic]], conductor: int) -> Polynomial:
    raw = kernel.charpoly(cast(list[list[Q]], matrix))
    return _lift_polynomial(conductor, raw)


def _squarefree(polynomial: Polynomial) -> Factorization:
    conductor = polynomial[0].conductor
    raw = kernel.squarefree_factors(cast(list[Q], polynomial))
    factors: Factorization = []
    for factor, multiplicity in raw:
        lifted = _lift_polynomial(conductor, factor)
        factors.append((lifted, _exact_counter(multiplicity, "factor_multiplicity")))
    return factors


def _product(left: Polynomial, right: Polynomial, conductor: int) -> Polynomial:
    raw = kernel.poly_product(cast(list[Q], left), cast(list[Q], right))
    return _lift_polynomial(conductor, raw)


def _radical(conductor: int, factors: Factorization) -> Polynomial:
    radical = [field.Cyclotomic.rational(conductor, 1)]
    for factor, _multiplicity in factors:
        radical = _product(radical, factor, conductor)
    return radical


def _sturm(polynomial: Polynomial) -> list[Polynomial]:
    conductor = polynomial[0].conductor
    raw = kernel.sturm_sequence(cast(list[Q], polynomial))
    return [_lift_polynomial(conductor, row) for row in raw]


def _open_count(sequence: list[Polynomial], lower: Q, upper: Q) -> int:
    bridged = [cast(list[Q], row) for row in sequence]
    return kernel._open_root_count(bridged, lower, upper)


def _intervals(radical: Polynomial, budget: kernel._Budget) -> list[tuple[Q, Q, int]]:
    return kernel.sturm_spectrum_intervals(cast(list[Q], radical), 0, budget)


def _is_zero_at(polynomial: Polynomial, value: Q) -> bool:
    evaluated = kernel._poly_eval(cast(list[Q], polynomial), value)
    lifted = _lift_coefficient(polynomial[0].conductor, evaluated)
    zero = field.Cyclotomic.rational(polynomial[0].conductor, 0)
    return lifted == zero


def _contained_count(factor: Polynomial, lower: Q, upper: Q) -> int:
    if lower == upper:
        return int(_is_zero_at(factor, lower))
    return _open_count(_sturm(factor), lower, upper)


def _require_self_conjugate(polynomial: Polynomial) -> None:
    for index, value in enumerate(polynomial):
        if value != value.conjugate():
            raise _fail(
                "root_identity: characteristic coefficient is not self-conjugate",
                index=index,
            )


def _polynomials(case: dict[str, Any]) -> tuple[Polynomial, Factorization, Polynomial]:
    conductor = _exact_counter(case["conductor"], "conductor")
    matrix = field.validated_matrix(case)
    polynomial = _charpoly(matrix, conductor)
    _require_self_conjugate(polynomial)
    factors = _squarefree(polynomial)
    return polynomial, factors, _radical(conductor, factors)


def _wire(polynomial: Polynomial, conductor: int) -> Wire:
    return [_lift_coefficient(conductor, value).wire() for value in polynomial]


def _subdivision_limit(override: int | None) -> int:
    ceiling = kernel.STURM_SUBDIVISION_RESOURCE_LIMIT
    if override is None:
        return ceiling
    limit = _exact_counter(override, "subdivision_limit")
    if limit < 0 or limit > ceiling:
        raise _fail(
            "root_identity: test subdivision limit must only lower the production ceiling",
            received=limit,
            ceiling=ceiling,
        )
    return limit


def _factor_multiplicity(lower: Q, upper: Q, factors: Factorization) -> int:
    matches: list[int] = []
    for factor, multiplicity in factors:
        count = _contained_count(factor, lower, upper)
        if count not in (0, 1):
            raise _fail("root_identity: factor has more than one root in an identity", count=count)
        if count:
            matches.append(multiplicity)
    if len(matches) != 1:
        raise _fail(
            "root_identity: root must belong to exactly one squarefree factor",
            owners=len(matches),
        )
    return matches[0]


def _root_record(lower: Q, upper: Q, defining: Wire, factors: Factorization) -> dict[str, Any]:
    singleton = lower == upper
    kind = "EXACT_RATIONAL_ROOT" if singleton else "EXACT_REAL_ALGEBRAIC_ROOT"
    convention = "SINGLETON" if singleton else "OPEN"
    return {
        "kind": kind,
        "defining_polynomial": defining,
        "lower": kernel.rat(lower),
        "upper": kernel.rat(upper),
        "endpoint_convention": convention,
        "distinct_root_count": 1,
        "multiplicity": _factor_multiplicity(lower, upper, factors),
    }


def _certificate(
    conductor: int,
    polynomial: Polynomial,
    factors: Factorization,
    defining: Wire,
    spectrum: list[dict[str, Any]],
    budget: kernel._Budget,
) -> dict[str, Any]:
    rows = [
        {"polynomial": _wire(factor, conductor), "multiplicity": multiplicity}
        for factor, multiplicity in factors
    ]
    return {
        "representation": REPRESENTATION,
        "carrier_conductor": conductor,
        "embedding": field.embedding(conductor),
        "characteristic_polynomial": _wire(polynomial, conductor),
        "squarefree_factors": rows,
        "squarefree_radical": defining,
        "spectrum": spectrum,
        "resource": {
            "kind": "IMPLEMENTATION_RESOURCE_LIMIT",
            "sturm_subdivisions": budget.limit - budget.remaining,
            "sturm_subdivision_limit": kernel.STURM_SUBDIVISION_RESOURCE_LIMIT,
        },
        "scope": SCOPE,
    }


def exact_spectrum(case: object, *, _test_subdivision_limit: int | None = None) -> dict[str, Any]:
    """Return exact polynomial-root identities, with separate degree obligations.

    The optional lower test limit exists only to prove resource refusal and
    cannot increase the unchanged production ceiling.
    """
    checked = _as_case(case)
    polynomial, factors, radical = _polynomials(checked)
    limit = _subdivision_limit(_test_subdivision_limit)
    budget = kernel._Budget(limit, "IMPLEMENTATION_RESOURCE_LIMIT: sturm_subdivisions")
    intervals = _intervals(radical, budget)
    conductor = _exact_counter(checked["conductor"], "conductor")
    defining = _wire(radical, conductor)
    spectrum = [
        _root_record(lower, upper, defining, factors) for lower, upper, _ignored in intervals
    ]
    return _certificate(conductor, polynomial, factors, defining, spectrum, budget)


def _bound_fields(
    case: dict[str, Any], output: dict[str, Any]
) -> tuple[Wire, Polynomial, Factorization, Polynomial]:
    if set(output) != _OUTPUT_FIELDS:
        raise _fail("root_identity: output field census differs")
    polynomial, factors, radical = _polynomials(case)
    conductor = _exact_counter(case["conductor"], "conductor")
    radical_wire = _wire(radical, conductor)
    expected: dict[str, object] = {
        "representation": REPRESENTATION,
        "carrier_conductor": conductor,
        "embedding": field.embedding(conductor),
        "characteristic_polynomial": _wire(polynomial, conductor),
        "squarefree_factors": [
            {"polynomial": _wire(factor, conductor), "multiplicity": multiplicity}
            for factor, multiplicity in factors
        ],
        "squarefree_radical": radical_wire,
        "scope": SCOPE,
    }
    for key, value in expected.items():
        if kernel.serialized(output[key]) != kernel.serialized(value):
            raise _fail("root_identity: input-bound field differs", field=key)
    return radical_wire, polynomial, factors, radical


def _require_resource(resource: object) -> dict[str, Any]:
    if not isinstance(resource, dict):
        raise _fail("root_identity: invalid subdivision resource accounting", reason="type")
    if set(resource) != _RESOURCE_FIELDS:
        raise _fail("root_identity: invalid subdivision resource accounting", reason="fields")
    return resource


def _resource_counters(resource: dict[str, Any]) -> tuple[int, int]:
    if resource["kind"] != "IMPLEMENTATION_RESOURCE_LIMIT":
        raise _fail("root_identity: invalid subdivision resource accounting", reason="kind")
    used = _exact_counter(resource["sturm_subdivisions"], "sturm_subdivisions")
    limit = _exact_counter(resource["sturm_subdivision_limit"], "sturm_subdivision_limit")
    ceiling = kernel.STURM_SUBDIVISION_RESOURCE_LIMIT
    if limit != ceiling or used < 0 or used > limit:
        raise _fail(
            "root_identity: invalid subdivision resource accounting",
            used=used,
            limit=limit,
            ceiling=ceiling,
        )
    return used, ceiling


def _validate_resource(output: dict[str, Any], radical: Polynomial) -> None:
    used, ceiling = _resource_counters(_require_resource(output["resource"]))
    replay = kernel._Budget(ceiling, "IMPLEMENTATION_RESOURCE_LIMIT: sturm_subdivisions")
    _intervals(radical, replay)
    spent = replay.limit - replay.remaining
    if used != spent:
        raise _fail(
            "root_identity: subdivision counter differs from deterministic traversal",
            used=used,
            replayed=spent,
        )


def _require_root_fields(label: str, row: object) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise _fail("root_identity: root field census differs", label=label)
    if set(row) != _ROOT_FIELDS:
        raise _fail("root_identity: root field census differs", label=label)
    return row


def _endpoint(label: str, value: object, role: str) -> Q:
    _refuse_floats(value, role)
    try:
        return kernel.parse_rat(value)
    except ValueError as error:
        raise _fail("root_identity: invalid exact endpoints", label=label, role=role) from error


def _endpoints(label: str, row: dict[str, Any]) -> tuple[Q, Q]:
    lower = _endpoint(label, row["lower"], "lower")
    upper = _endpoint(label, row["upper"], "upper")
    if lower < 0 or upper > 1 or lower > upper:
        raise _fail(
            "root_identity: invalid exact endpoints",
            label=label,
            lower=kernel.rat(lower),
            upper=kernel.rat(upper),
        )
    return lower, upper


def _require_order(label: str, previous: tuple[Q, Q] | None, lower: Q, upper: Q) -> None:
    if previous is None:
        return
    if previous[1] > lower or previous == (lower, upper):
        raise _fail("root_identity: identities overlap or are not ordered", label=label)


def _require_kind(label: str, row: dict[str, Any], singleton: bool) -> None:
    expected_kind = "EXACT_RATIONAL_ROOT" if singleton else "EXACT_REAL_ALGEBRAIC_ROOT"
    expected_convention = "SINGLETON" if singleton else "OPEN"
    if row["kind"] != expected_kind or row["endpoint_convention"] != expected_convention:
        raise _fail("root_identity: kind or endpoint convention differs", label=label)


def _require_distinct_count(label: str, row: dict[str, Any]) -> None:
    count = _exact_counter(row["distinct_root_count"], "distinct_root_count")
    if count != 1:
        raise _fail("root_identity: one distinct root required", label=label, count=count)


def _require_row_multiplicity(label: str, row: dict[str, Any], degree: int) -> int:
    multiplicity = _exact_counter(row["multiplicity"], "multiplicity")
    if multiplicity < 1 or multiplicity > degree:
        raise _fail(
            "root_identity: invalid multiplicity",
            label=label,
            multiplicity=multiplicity,
            degree=degree,
        )
    return multiplicity


def _radical_count(radical: Polynomial, sequence: list[Polynomial], lower: Q, upper: Q) -> int:
    if lower == upper:
        return int(_is_zero_at(radical, lower))
    return _open_count(sequence, lower, upper)


def _require_weighted_census(total: int, degree: int) -> None:
    if total != degree:
        raise _fail(
            "root_identity: weighted root census differs from input dimension",
            total=total,
            degree=degree,
        )


def _validate_root(
    index: int,
    row: object,
    radical_wire: Wire,
    radical: Polynomial,
    sequence: list[Polynomial],
    degree: int,
    factors: Factorization,
    previous: tuple[Q, Q] | None,
) -> tuple[tuple[Q, Q], int]:
    label = f"root_identity[{index}]"
    checked = _require_root_fields(label, row)
    lower, upper = _endpoints(label, checked)
    _require_order(label, previous, lower, upper)
    _require_kind(label, checked, lower == upper)
    if kernel.serialized(checked["defining_polynomial"]) != kernel.serialized(radical_wire):
        raise _fail("root_identity: defining polynomial differs from squarefree radical", label=label)
    _require_distinct_count(label, checked)
    multiplicity = _require_row_multiplicity(label, checked, degree)
    contained = _radical_count(radical, sequence, lower, upper)
    if contained != 1:
        raise _fail(
            "root_identity: supplied identity does not contain exactly one root",
            label=label,
            count=contained,
        )
    if _factor_multiplicity(lower, upper, factors) != multiplicity:
        raise _fail("root_identity: multiplicity differs from exact squarefree factor", label=label)
    return (lower, upper), multiplicity


def _validate_roots(
    output: dict[str, Any],
    radical_wire: Wire,
    polynomial: Polynomial,
    factors: Factorization,
    radical: Polynomial,
) -> None:
    roots = output["spectrum"]
    distinct = len(radical) - 1
    if not isinstance(roots, list):
        raise _fail("root_identity: distinct-root census differs from radical degree", distinct=distinct)
    if len(roots) != distinct:
        raise _fail(
            "root_identity: distinct-root census differs from radical degree",
            rows=len(roots),
            distinct=distinct,
        )
    sequence = _sturm(radical)
    previous: tuple[Q, Q] | None = None
    total = 0
    degree = len(polynomial) - 1
    for index, row in enumerate(roots):
        previous, multiplicity = _validate_root(
            index, row, radical_wire, radical, sequence, degree, factors, previous
        )
        total += multiplicity
    _require_weighted_census(total, degree)


def validate_spectrum(case: object, output: object) -> None:
    """Recount supplied roots, independently of producer interval choices.

    This checks root containment against the input. It does not verify
    irreducibility or a splitting degree.
    """
    checked = _as_case(case)
    _refuse_floats(output, "output")
    if type(output) is not dict:
        raise _fail("root_identity: output field census differs")
    parsed = cast(dict[str, Any], output)
    radical_wire, polynomial, factors, radical = _bound_fields(checked, parsed)
    _validate_resource(parsed, radical)
    _validate_roots(parsed, radical_wire, polynomial, factors, radical)


def report(interface: Path | None = None) -> dict[str, Any]:
    cases = [
        {"input": case, "output": exact_spectrum(case)} for case in kernel.fixtures(interface)
    ]
    return {
        "authority_effect": "None",
        "schema": "ordered_real_polynomial_roots_v1",
        "cases": cases,
    }
