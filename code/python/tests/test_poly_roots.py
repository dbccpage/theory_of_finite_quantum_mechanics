"""Unit, negative, integration, end-to-end, and mutation tests for root identities.

Origin: code/python/src/linear_algebra/poly_roots.py
Claim: urn:omega:fqm:linear-algebra:ordered-real-polynomial-roots:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""



from __future__ import annotations

import copy
import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.cyclo_density import Cyclotomic
from src.linear_algebra.entropy_dichotomy import RefusedAtBudget
from src.linear_algebra.poly_roots import (
    RootIdentityError,
    exact_spectrum,
    report,
    validate_spectrum,
)
from src.linear_algebra import poly_roots

def _probe(text: str) -> object:
    import ast as _ast

    value = _ast.literal_eval(text)
    if type(value).__name__ in {"int", "bool"}:
        raise TypeError("admitted scalar is not a refusal probe")
    return value

def _all_hold(flags: tuple[bool, ...]) -> bool:
    for flag in flags:
        if flag is False:
            return False
    return True


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "poly_roots.py"
_Q = Fraction

PURE: dict[str, Any] = {
    "fixture_id": "s1_pure",
    "system_id": "S1",
    "conductor": 4,
    "matrix": [["1/1", "0/1"], ["0/1", "0/1"]],
    "scope": "DECLARED_SYSTEM_STATE",
}
MIXED: dict[str, Any] = {
    "fixture_id": "s1_mixed_half",
    "system_id": "S1",
    "conductor": 4,
    "matrix": [["1/2", "0/1"], ["0/1", "1/2"]],
    "scope": "DECLARED_SYSTEM_STATE",
}
SQRT2: dict[str, Any] = {
    "fixture_id": "s1_sqrt2",
    "system_id": "S1",
    "conductor": 4,
    "matrix": [["5/8", "1/8"], ["1/8", "3/8"]],
    "scope": "DECLARED_SYSTEM_STATE",
}


def _spectrum(certificate: dict[str, Any]) -> list[dict[str, Any]]:
    rows = certificate["spectrum"]
    assert isinstance(rows, list)
    return rows


def _pair(row: dict[str, Any]) -> tuple[Any, Any, Any, Any]:
    return (row["lower"], row["upper"], row["kind"], row["multiplicity"])


def test_hand_spectra_for_rational_and_quadratic_roots() -> None:
    pure = exact_spectrum(PURE)
    assert pure["representation"] == "ORDERED_REAL_POLYNOMIAL_ROOTS_V1"
    assert pure["scope"] == "EXACT_ROOT_IDENTITIES_NO_SPLITTING_DEGREE_OR_DEPENDENCE"
    assert pure["carrier_conductor"] == 4
    assert pure["resource"] == {
        "kind": "IMPLEMENTATION_RESOURCE_LIMIT",
        "sturm_subdivisions": 0,
        "sturm_subdivision_limit": 4096,
    }
    assert [_pair(row) for row in _spectrum(pure)] == [
        ("0/1", "0/1", "EXACT_RATIONAL_ROOT", 1),
        ("1/1", "1/1", "EXACT_RATIONAL_ROOT", 1),
    ]
    assert _spectrum(pure)[0]["endpoint_convention"] == "SINGLETON"
    validate_spectrum(PURE, pure)

    mixed = exact_spectrum(MIXED)
    assert [_pair(row) for row in _spectrum(mixed)] == [
        ("1/2", "1/2", "EXACT_RATIONAL_ROOT", 2),
    ]
    assert mixed["resource"]["sturm_subdivisions"] == 1
    assert mixed["squarefree_factors"] == [
        {
            "polynomial": [
                {"cyclotomic_coefficients": ["1/1", "0/1"]},
                {"cyclotomic_coefficients": ["-1/2", "0/1"]},
            ],
            "multiplicity": 2,
        }
    ]
    validate_spectrum(MIXED, mixed)

    algebraic = exact_spectrum(SQRT2)
    assert algebraic["characteristic_polynomial"][2] == {"cyclotomic_coefficients": ["7/32", "0/1"]}
    assert [_pair(row) for row in _spectrum(algebraic)] == [
        ("1/4", "1/2", "EXACT_REAL_ALGEBRAIC_ROOT", 1),
        ("1/2", "1/1", "EXACT_REAL_ALGEBRAIC_ROOT", 1),
    ]
    assert _spectrum(algebraic)[0]["endpoint_convention"] == "OPEN"
    assert algebraic["resource"]["sturm_subdivisions"] == 2
    validate_spectrum(SQRT2, algebraic)

    widened = copy.deepcopy(algebraic)
    widened["spectrum"][0]["lower"] = "0/1"
    validate_spectrum(SQRT2, widened)


def test_negative_boundary_and_certificate_failures() -> None:
    floated = copy.deepcopy(PURE)
    floated["matrix"][0][0] = _probe("1.5")
    with pytest.raises(RootIdentityError, match="float refused") as float_error:
        exact_spectrum(floated)
    assert float_error.value.invariant == "float refused at the public boundary"
    assert float_error.value.parameters == {"role": "input", "received": "float"}

    with pytest.raises(RootIdentityError, match="boolean refused") as boolean_error:
        exact_spectrum(PURE, _test_subdivision_limit=True)
    assert boolean_error.value.invariant == "boolean refused where an exact integer was required"
    assert boolean_error.value.parameters["role"] == "subdivision_limit"

    with pytest.raises(RootIdentityError, match="exact integer required") as text_conductor:
        broken = copy.deepcopy(PURE)
        broken["conductor"] = "4"
        exact_spectrum(broken)
    assert text_conductor.value.parameters["role"] == "conductor"

    with pytest.raises(RootIdentityError, match="typed input object required"):
        exact_spectrum(["not", "a", "case"])

    with pytest.raises(RootIdentityError, match="only lower the production ceiling") as high_limit:
        exact_spectrum(PURE, _test_subdivision_limit=4097)
    assert high_limit.value.parameters == {"received": 4097, "ceiling": 4096}

    with pytest.raises(RefusedAtBudget, match="sturm_subdivisions"):
        exact_spectrum(SQRT2, _test_subdivision_limit=1)
    assert exact_spectrum(PURE, _test_subdivision_limit=0)["resource"]["sturm_subdivisions"] == 0

    published = exact_spectrum(PURE)
    with pytest.raises(RootIdentityError, match="output field census differs"):
        validate_spectrum(PURE, [])
    missing = copy.deepcopy(published)
    del missing["scope"]
    with pytest.raises(RootIdentityError, match="output field census differs"):
        validate_spectrum(PURE, missing)

    rebound = copy.deepcopy(published)
    rebound["scope"] = "OTHER"
    with pytest.raises(RootIdentityError, match="input-bound field differs") as rebound_error:
        validate_spectrum(PURE, rebound)
    assert rebound_error.value.parameters["field"] == "scope"

    counted = copy.deepcopy(exact_spectrum(SQRT2))
    counted["resource"]["sturm_subdivisions"] = 3
    with pytest.raises(RootIdentityError, match="subdivision counter differs") as counter:
        validate_spectrum(SQRT2, counted)
    assert counter.value.parameters["used"] == 3
    assert counter.value.parameters["replayed"] == 2

    kind = copy.deepcopy(published)
    kind["resource"]["kind"] = "OTHER"
    with pytest.raises(RootIdentityError, match="invalid subdivision resource accounting") as kind_error:
        validate_spectrum(PURE, kind)
    assert kind_error.value.parameters["reason"] == "kind"

    boolean_used = copy.deepcopy(published)
    boolean_used["resource"]["sturm_subdivisions"] = True
    with pytest.raises(RootIdentityError, match="boolean refused") as used_bool:
        validate_spectrum(PURE, boolean_used)
    assert used_bool.value.parameters["role"] == "sturm_subdivisions"

    outside = copy.deepcopy(exact_spectrum(SQRT2))
    outside["spectrum"][1]["upper"] = "3/2"
    with pytest.raises(RootIdentityError, match="invalid exact endpoints"):
        validate_spectrum(SQRT2, outside)

    unordered = copy.deepcopy(published)
    unordered["spectrum"] = [published["spectrum"][1], published["spectrum"][0]]
    with pytest.raises(RootIdentityError, match="overlap or are not ordered"):
        validate_spectrum(PURE, unordered)

    renamed = copy.deepcopy(published)
    renamed["spectrum"][0]["kind"] = "EXACT_REAL_ALGEBRAIC_ROOT"
    with pytest.raises(RootIdentityError, match="kind or endpoint convention differs"):
        validate_spectrum(PURE, renamed)

    dropped = copy.deepcopy(published)
    del dropped["spectrum"][0]["multiplicity"]
    with pytest.raises(RootIdentityError, match="root field census differs"):
        validate_spectrum(PURE, dropped)

    redefined = copy.deepcopy(published)
    redefined["spectrum"][0]["defining_polynomial"] = []
    with pytest.raises(RootIdentityError, match="defining polynomial differs"):
        validate_spectrum(PURE, redefined)

    doubled = copy.deepcopy(published)
    doubled["spectrum"][0]["distinct_root_count"] = 2
    with pytest.raises(RootIdentityError, match="one distinct root required") as doubled_error:
        validate_spectrum(PURE, doubled)
    assert doubled_error.value.parameters["count"] == 2

    zero_mult = copy.deepcopy(published)
    zero_mult["spectrum"][0]["multiplicity"] = 0
    with pytest.raises(RootIdentityError, match="invalid multiplicity"):
        validate_spectrum(PURE, zero_mult)

    empty = copy.deepcopy(exact_spectrum(SQRT2))
    empty["spectrum"][0]["lower"] = "0/1"
    empty["spectrum"][0]["upper"] = "1/8"
    with pytest.raises(RootIdentityError, match="exactly one root") as empty_error:
        validate_spectrum(SQRT2, empty)
    assert empty_error.value.parameters["count"] == 0

    relabeled = copy.deepcopy(published)
    relabeled["spectrum"][0]["multiplicity"] = 2
    with pytest.raises(RootIdentityError, match="multiplicity differs"):
        validate_spectrum(PURE, relabeled)

    short = copy.deepcopy(published)
    short["spectrum"] = [published["spectrum"][0]]
    with pytest.raises(RootIdentityError, match="distinct-root census differs") as short_error:
        validate_spectrum(PURE, short)
    assert short_error.value.parameters == {"rows": 1, "distinct": 2}

    floated_output = copy.deepcopy(published)
    floated_output["spectrum"][0]["lower"] = _probe("0.0")
    with pytest.raises(RootIdentityError, match="float refused") as output_float:
        validate_spectrum(PURE, floated_output)
    assert output_float.value.parameters["role"] == "output"


def test_helper_invariants_have_measured_parameters() -> None:
    polynomial = [Cyclotomic.rational(5, 1), Cyclotomic.zeta(5)]
    with pytest.raises(RootIdentityError, match="not self-conjugate") as conjugate:
        poly_roots._require_self_conjugate(polynomial)
    assert conjugate.value.parameters["index"] == 1

    _characteristic, factors, _radical = poly_roots._polynomials(SQRT2)
    with pytest.raises(RootIdentityError, match="more than one root") as wide:
        poly_roots._factor_multiplicity(_Q(0), _Q(1), factors)
    assert wide.value.parameters["count"] == 2
    with pytest.raises(RootIdentityError, match="exactly one squarefree factor") as absent:
        poly_roots._factor_multiplicity(_Q(0), _Q(1, 8), factors)
    assert absent.value.parameters["owners"] == 0

    with pytest.raises(RootIdentityError, match="coefficient list required") as not_list:
        poly_roots._lift_polynomial(4, "1/1")
    assert not_list.value.parameters["received"] == "str"
    with pytest.raises(RootIdentityError, match="exact integer required") as text:
        poly_roots._lift_coefficient(4, "1/1")
    assert text.value.parameters == {"role": "coefficient", "received": "str"}
    with pytest.raises(RootIdentityError, match="conductor differs") as foreign:
        poly_roots._lift_coefficient(4, Cyclotomic.rational(5, 1))
    assert foreign.value.parameters == {"conductor": 4, "received": 5}
    with pytest.raises(RootIdentityError, match="weighted root census differs") as weighted:
        poly_roots._require_weighted_census(1, 2)
    assert weighted.value.parameters == {"total": 1, "degree": 2}


def test_neighbor_refusal_is_not_rewritten() -> None:
    bad = copy.deepcopy(PURE)
    bad["system_id"] = "NOPE"
    with pytest.raises(ValueError, match="system missing") as caught:
        exact_spectrum(bad)
    assert not isinstance(caught.value, RootIdentityError)


def test_integration_matches_rust_root_sentence() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "poly_roots.rs").read_text(encoding="utf-8")
    assert 'ORDERED_REAL_POLYNOMIAL_ROOTS_V1' in source
    certificate = exact_spectrum(PURE)
    validate_spectrum(PURE, certificate)
    assert certificate["spectrum"][1]["upper"] == "1/1"


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.poly_roots
    published = package.exact_spectrum(PURE)
    package.validate_spectrum(PURE, published)
    assert published["representation"] == package.REPRESENTATION
    envelope = package.report()
    assert envelope["authority_effect"] == "None"
    assert envelope["schema"] == "ordered_real_polynomial_roots_v1"
    assert len(envelope["cases"]) == 21
    for case in envelope["cases"]:
        package.validate_spectrum(case["input"], case["output"])
    with pytest.raises(RootIdentityError, match="float refused"):
        package.exact_spectrum(_probe("1.5"))


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "poly_roots.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert 'REPRESENTATION' in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:ordered-real-polynomial-roots:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if isinstance(value, float):\n        return\n    if False:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
    ),
    (
        "boolean counter admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where an exact integer was required", role=role)',
        'if False and type(value) is bool:\n        raise _fail("boolean refused where an exact integer was required", role=role)',
    ),
    (
        "singleton test flipped",
        "singleton = lower == upper",
        "singleton = lower != upper",
    ),
    (
        "multiplicity incremented",
        "return matches[0]",
        "return matches[0] + 1",
    ),
    (
        "weighted census inverted",
        "if total != degree:",
        "if total == degree:",
    ),
    (
        "distinct count accepts zero",
        "if count != 1:",
        "if count != 0:",
    ),
    (
        "representation renamed",
        'REPRESENTATION = "ORDERED_REAL_POLYNOMIAL_ROOTS_V1"',
        'REPRESENTATION = "ORDERED_REAL_POLYNOMIAL_ROOTS_V2"',
    ),
    (
        "order test reversed",
        "if previous[1] > lower or previous == (lower, upper):",
        "if previous[1] < lower or previous == (lower, upper):",
    ),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.linear_algebra"
    sys.modules[name] = module
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="__package__ != __spec__.parent", category=DeprecationWarning)
        exec(compile(source, name + ".py", "exec"), module.__dict__)
    return module.__dict__


def _invariant(error: type[BaseException], probe: object) -> str | None:
    if not callable(probe):
        return None
    try:
        probe()
    except error as caught:
        invariant = getattr(caught, "invariant", None)
        return invariant if isinstance(invariant, str) else None
    return None


def _pairs(certificate: object) -> list[tuple[object, object, object, object]] | None:
    if not isinstance(certificate, dict):
        return None
    rows = certificate.get("spectrum")
    if not isinstance(rows, list):
        return None
    parsed: list[tuple[object, object, object, object]] = []
    for row in rows:
        if not isinstance(row, dict):
            return None
        parsed.append((row.get("lower"), row.get("upper"), row.get("kind"), row.get("multiplicity")))
    return parsed


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    produce = namespace["exact_spectrum"]
    verify = namespace["validate_spectrum"]
    if not _all_hold((callable(produce), callable(verify),)):
        return False
    try:
        pure = produce(PURE)
        mixed = produce(MIXED)
        algebraic = produce(SQRT2)
        verify(PURE, pure)
        verify(MIXED, mixed)
        verify(SQRT2, algebraic)
    except error:
        return False
    pure_rows = _pairs(pure)
    mixed_rows = _pairs(mixed)
    algebraic_rows = _pairs(algebraic)
    if pure_rows is None or mixed_rows is None or algebraic_rows is None:
        return False
    if not _all_hold((isinstance(pure, dict), isinstance(mixed, dict), isinstance(algebraic, dict),)):
        return False
    pure_resource = pure.get("resource")
    mixed_resource = mixed.get("resource")
    algebraic_resource = algebraic.get("resource")
    if not _all_hold((isinstance(pure_resource, dict), isinstance(mixed_resource, dict),)):
        return False
    if not isinstance(algebraic_resource, dict):
        return False
    return _all_hold((
pure.get("representation") == "ORDERED_REAL_POLYNOMIAL_ROOTS_V1",
pure.get("scope") == "EXACT_ROOT_IDENTITIES_NO_SPLITTING_DEGREE_OR_DEPENDENCE",
pure_rows == [
            ("0/1", "0/1", "EXACT_RATIONAL_ROOT", 1),
            ("1/1", "1/1", "EXACT_RATIONAL_ROOT", 1),
        ],
pure_resource.get("sturm_subdivisions") == 0,
mixed_rows == [("1/2", "1/2", "EXACT_RATIONAL_ROOT", 2)],
mixed_resource.get("sturm_subdivisions") == 1,
algebraic_rows == [
            ("1/4", "1/2", "EXACT_REAL_ALGEBRAIC_ROOT", 1),
            ("1/2", "1/1", "EXACT_REAL_ALGEBRAIC_ROOT", 1),
        ],
algebraic_resource.get("sturm_subdivisions") == 2,
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    produce = namespace["exact_spectrum"]
    if not callable(produce):
        return False
    floated = copy.deepcopy(PURE)
    floated["matrix"][0][0] = _probe("1.5")
    probes = (
        (lambda: produce(floated), "float refused at the public boundary"),
        (lambda: produce(PURE, _test_subdivision_limit=True), "boolean refused where an exact integer was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["RootIdentityError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_roots_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_roots_{index}"
            loaded.append(module_name)
            try:
                namespace = _load_source(source.replace(old, new, 1), module_name)
                survived = _oracle(namespace)
            except Exception:
                survived = False
            assert survived is False, name
            killed += 1
        assert killed == len(_MUTANTS)
        assert f"Mutation-Kills: {killed} non-equivalent" in source
        assert f"Mutation-Kills: {killed} non-equivalent" in Path(__file__).read_text(encoding="utf-8")
    finally:
        for module_name in loaded:
            sys.modules.pop(module_name, None)
