"""Chosen-real-embedding algebraic root identities. AuthorityEffect: None.

No splitting degree, minimal polynomial, or logarithm basis is inferred from
an isolator. All identity checks use the original exact typed matrix.
"""

from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from . import cyclo_density as field
from . import entropy_dichotomy as kernel


REPRESENTATION = "ORDERED_REAL_POLYNOMIAL_ROOTS_V1"
SCOPE = "EXACT_ROOT_IDENTITIES_NO_SPLITTING_DEGREE_OR_DEPENDENCE"


def _polynomials(case: dict[str, Any]) -> tuple[list[Any], list[tuple[list[Any], int]], list[Any]]:
    matrix = field.validated_matrix(case)
    n = case["conductor"]
    polynomial = [value if isinstance(value, field.Cyclotomic) else field.Cyclotomic.rational(n, value)
                  for value in kernel.charpoly(matrix)]
    if any(value != value.conjugate() for value in polynomial):
        raise ValueError("root_identity: characteristic coefficient is not self-conjugate")
    factors = kernel.squarefree_factors(polynomial)
    radical = [field.Cyclotomic.rational(n, 1)]
    for factor, _ in factors:
        radical = kernel.poly_product(radical, factor)
    return polynomial, factors, radical


def _wire(polynomial: list[Any], conductor: int) -> list[dict[str, list[str]]]:
    return [(value if isinstance(value, field.Cyclotomic)
             else field.Cyclotomic.rational(conductor, value)).wire() for value in polynomial]


def _multiplicity(lower: Q, upper: Q, factors: list[tuple[list[Any], int]]) -> int:
    matches = []
    for factor, multiplicity in factors:
        count = (int(kernel._poly_eval(factor, lower) == 0) if lower == upper
                 else kernel._open_root_count(kernel.sturm_sequence(factor), lower, upper))
        if count not in (0, 1):
            raise ValueError("root_identity: factor has more than one root in an identity")
        if count:
            matches.append(multiplicity)
    if len(matches) != 1:
        raise ValueError("root_identity: root must belong to exactly one squarefree factor")
    return matches[0]


def exact_spectrum(case: dict[str, Any], *, _test_subdivision_limit: int | None = None) -> dict[str, Any]:
    """Return exact polynomial-root identities, with separate degree obligations.

    The optional lower test limit exists only to prove resource refusal and
    cannot increase the unchanged production ceiling.
    """
    polynomial, factors, radical = _polynomials(case)
    limit = kernel.STURM_SUBDIVISION_RESOURCE_LIMIT
    if _test_subdivision_limit is not None:
        if type(_test_subdivision_limit) is not int or not 0 <= _test_subdivision_limit <= limit:
            raise ValueError("root_identity: test subdivision limit must only lower the production ceiling")
        limit = _test_subdivision_limit
    budget = kernel._Budget(limit, "IMPLEMENTATION_RESOURCE_LIMIT: sturm_subdivisions")
    intervals = kernel.sturm_spectrum_intervals(radical, 0, budget)
    n = case["conductor"]
    defining = _wire(radical, n)
    roots = [{"kind": "EXACT_RATIONAL_ROOT" if a == b else "EXACT_REAL_ALGEBRAIC_ROOT",
              "defining_polynomial": defining, "lower": kernel.rat(a), "upper": kernel.rat(b),
              "endpoint_convention": "SINGLETON" if a == b else "OPEN",
              "distinct_root_count": 1, "multiplicity": _multiplicity(a, b, factors)}
             for a, b, _ in intervals]
    return {"representation": REPRESENTATION, "carrier_conductor": n,
            "embedding": field.embedding(n), "characteristic_polynomial": _wire(polynomial, n),
            "squarefree_factors": [{"polynomial": _wire(factor, n), "multiplicity": multiplicity}
                                   for factor, multiplicity in factors],
            "squarefree_radical": defining, "spectrum": roots,
            "resource": {"kind": "IMPLEMENTATION_RESOURCE_LIMIT", "sturm_subdivisions": budget.limit - budget.remaining,
                         "sturm_subdivision_limit": kernel.STURM_SUBDIVISION_RESOURCE_LIMIT},
            "scope": SCOPE}


def validate_spectrum(case: dict[str, Any], output: Any) -> None:
    """Recount supplied roots, independently of producer interval choices.

    This checks root containment against the input, unlike an approximation
    metadata check. It does not verify irreducibility or a splitting degree.
    """
    kernel.reject_floats(output, "root_identity")
    expected_keys = {"representation", "carrier_conductor", "embedding", "characteristic_polynomial",
                     "squarefree_factors", "squarefree_radical", "spectrum", "resource", "scope"}
    if not isinstance(output, dict) or set(output) != expected_keys:
        raise ValueError("root_identity: output field census differs")
    polynomial, factors, radical = _polynomials(case)
    n = case["conductor"]
    expected = {"representation": REPRESENTATION, "carrier_conductor": n,
                "embedding": field.embedding(n), "characteristic_polynomial": _wire(polynomial, n),
                "squarefree_factors": [{"polynomial": _wire(factor, n), "multiplicity": multiplicity}
                                       for factor, multiplicity in factors],
                "squarefree_radical": _wire(radical, n), "scope": SCOPE}
    for key, value in expected.items():
        if kernel.serialized(output[key]) != kernel.serialized(value):
            raise ValueError(f"root_identity: input-bound {key} differs")
    resource = output["resource"]
    if (not isinstance(resource, dict)
            or set(resource) != {"kind", "sturm_subdivisions", "sturm_subdivision_limit"}
            or resource["kind"] != "IMPLEMENTATION_RESOURCE_LIMIT"
            or type(resource["sturm_subdivisions"]) is not int
            or type(resource["sturm_subdivision_limit"]) is not int
            or resource["sturm_subdivision_limit"] != kernel.STURM_SUBDIVISION_RESOURCE_LIMIT
            or not 0 <= resource["sturm_subdivisions"] <= resource["sturm_subdivision_limit"]):
        raise ValueError("root_identity: invalid subdivision resource accounting")
    # Counter provenance is a deterministic traversal replay, not the root
    # containment argument below. Supplied isolators may differ from ours.
    replay_budget = kernel._Budget(kernel.STURM_SUBDIVISION_RESOURCE_LIMIT,
                                   "IMPLEMENTATION_RESOURCE_LIMIT: sturm_subdivisions")
    kernel.sturm_spectrum_intervals(radical, 0, replay_budget)
    if resource["sturm_subdivisions"] != replay_budget.limit - replay_budget.remaining:
        raise ValueError("root_identity: subdivision counter differs from deterministic traversal")
    roots = output["spectrum"]
    if not isinstance(roots, list) or len(roots) != len(radical) - 1:
        raise ValueError("root_identity: distinct-root census differs from radical degree")
    sequence = kernel.sturm_sequence(radical)
    previous: tuple[Q, Q] | None = None
    total = 0
    row_keys = {"kind", "defining_polynomial", "lower", "upper", "endpoint_convention",
                "distinct_root_count", "multiplicity"}
    for index, row in enumerate(roots):
        label = f"root_identity[{index}]"
        if not isinstance(row, dict) or set(row) != row_keys:
            raise ValueError(f"{label}: root field census differs")
        if kernel.serialized(row["defining_polynomial"]) != kernel.serialized(expected["squarefree_radical"]):
            raise ValueError(f"{label}: defining polynomial differs from squarefree radical")
        if type(row["distinct_root_count"]) is not int or row["distinct_root_count"] != 1:
            raise ValueError(f"{label}: one distinct root required")
        if type(row["multiplicity"]) is not int or not 1 <= row["multiplicity"] <= len(polynomial) - 1:
            raise ValueError(f"{label}: invalid multiplicity")
        lower, upper = kernel.parse_rat(row["lower"]), kernel.parse_rat(row["upper"])
        if kernel.rat(lower) != row["lower"] or kernel.rat(upper) != row["upper"] or not 0 <= lower <= upper <= 1:
            raise ValueError(f"{label}: invalid exact endpoints")
        if previous is not None and (previous[1] > lower or previous == (lower, upper)):
            raise ValueError(f"{label}: identities overlap or are not ordered")
        singleton = lower == upper
        if (row["kind"] != ("EXACT_RATIONAL_ROOT" if singleton else "EXACT_REAL_ALGEBRAIC_ROOT")
                or row["endpoint_convention"] != ("SINGLETON" if singleton else "OPEN")):
            raise ValueError(f"{label}: kind or endpoint convention differs")
        count = (int(kernel._poly_eval(radical, lower) == 0) if singleton
                 else kernel._open_root_count(sequence, lower, upper))
        if count != 1:
            raise ValueError(f"{label}: supplied identity does not contain exactly one root")
        if _multiplicity(lower, upper, factors) != row["multiplicity"]:
            raise ValueError(f"{label}: multiplicity differs from exact squarefree factor")
        total += row["multiplicity"]
        previous = lower, upper
    if total != len(polynomial) - 1:
        raise ValueError("root_identity: weighted root census differs from input dimension")


def report(interface: Path | None = None) -> dict[str, Any]:
    return {"authority_effect": "None", "schema": "ordered_real_polynomial_roots_v1",
            "cases": [{"input": case, "output": exact_spectrum(case)} for case in kernel.fixtures(interface)]}
