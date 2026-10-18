"""Unit, negative, integration, end-to-end, and mutation tests for compositum degrees."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.compositum_deg import (
    CompositumError,
    compositum_splitting_degree,
    dispatch,
    validate_compositum_degree,
    witness_same_field_degree,
)
from src.linear_algebra.scalars import GaussianRational

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "compositum_deg.py"
_Q = Fraction
_LINEAR = [(_Q(1), _Q(0)), (_Q(-1), _Q(0))]
_QUAD_2 = [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(-2), _Q(0))]
_DISJOINT = [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(-5), _Q(0)), (_Q(0), _Q(0)), (_Q(6), _Q(0))]
_SAME = [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(-10), _Q(0)), (_Q(0), _Q(0)), (_Q(16), _Q(0))]
_DEGREE_SIX = [(_Q(1), _Q(0))] + [(_Q(0), _Q(0))] * 5 + [(_Q(-1), _Q(0))]


def _intersection(certificate: dict[str, object]) -> dict[str, object]:
    row = certificate["intersection_certificate"]
    assert isinstance(row, dict)
    return row


def test_compositum_degrees_match_hand_values() -> None:
    assert witness_same_field_degree() == 2
    assert type(witness_same_field_degree()) is int

    linear = compositum_splitting_degree(1, _LINEAR)
    assert linear["degree_over_real_field"] == 1
    assert linear["degree_pattern"] == []
    assert linear["intersection_certificate"] is None
    assert linear["schema"] == "real_field_compositum_degree_v2"
    assert linear["authority_effect"] == "None"
    assert linear["coefficient_field"] == "Q"
    validate_compositum_degree(1, _LINEAR, linear)

    quadratic = compositum_splitting_degree(1, _QUAD_2)
    assert quadratic["degree_over_real_field"] == 2
    assert quadratic["degree_pattern"] == [2]
    assert quadratic["intersection_certificate"] is None
    validate_compositum_degree(1, _QUAD_2, quadratic)

    same = compositum_splitting_degree(1, _SAME)
    same_row = _intersection(same)
    squareclass = same_row["squareclass_certificate"]
    assert isinstance(squareclass, dict)
    assert same["degree_over_real_field"] == 2
    assert same["degree_pattern"] == [2, 2]
    assert same_row["rule"] == "QUADRATIC_QUADRATIC_SAME_FIELD"
    assert same_row["intersection_degree"] == 2
    assert squareclass["same_squareclass"] is True
    validate_compositum_degree(1, _SAME, same)

    disjoint = compositum_splitting_degree(1, _DISJOINT)
    disjoint_row = _intersection(disjoint)
    assert disjoint["degree_over_real_field"] == 4
    assert disjoint["degree_pattern"] == [2, 2]
    assert disjoint_row["rule"] == "QUADRATIC_QUADRATIC_DISJOINT"
    assert disjoint_row["intersection_degree"] == 1
    validate_compositum_degree(1, _DISJOINT, disjoint)


def test_negative_boundary_failures() -> None:
    with pytest.raises(CompositumError, match="float refused") as floated:
        compositum_splitting_degree(1, [(_Q(1), _Q(0)), (1.5, _Q(0))])
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "coefficient[1][0]"
    assert floated.value.parameters["received"] == "float"

    with pytest.raises(CompositumError, match="boolean refused") as boolean_coordinate:
        compositum_splitting_degree(1, [(True, _Q(0)), (_Q(-1), _Q(0))])
    assert boolean_coordinate.value.invariant == "boolean refused where a rational coordinate was required"
    assert boolean_coordinate.value.parameters["role"] == "coefficient[0][0]"

    with pytest.raises(CompositumError, match="Gaussian") as gaussian:
        compositum_splitting_degree(1, [(GaussianRational(0, 1), _Q(0)), (_Q(-1), _Q(0))])
    assert gaussian.value.invariant == (
        "Gaussian rational refused; compositum degrees in this module are over a real field"
    )

    with pytest.raises(CompositumError, match="boolean refused") as boolean_conductor:
        compositum_splitting_degree(True, _LINEAR)
    assert boolean_conductor.value.invariant == "boolean refused where a conductor was required"
    assert boolean_conductor.value.parameters["role"] == "conductor"

    with pytest.raises(CompositumError, match="at most five") as wide:
        compositum_splitting_degree(1, _DEGREE_SIX)
    assert wide.value.invariant == "compositum_degree: polynomial degree must be at most five"
    assert wide.value.parameters["length"] == 7

    tampered = dict(compositum_splitting_degree(1, _SAME))
    tampered["degree_over_real_field"] = 4
    with pytest.raises(CompositumError, match="final splitting degree differs") as changed:
        validate_compositum_degree(1, _SAME, tampered)
    assert changed.value.invariant == (
        "compositum_degree: final splitting degree differs from checked Galois intersection"
    )

    with pytest.raises(CompositumError, match="field census") as census:
        dispatch("compositum_splitting_degree")
    assert census.value.invariant == "compositum_degree: exact field census required"

    with pytest.raises(CompositumError, match="operation required") as operation:
        dispatch({"operation": "degree", "conductor": 1, "coefficients": []})
    assert operation.value.invariant == "compositum_degree: compositum_splitting_degree operation required"


def test_integration_matches_rust_intersection_sentence() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "compositum_deg.rs").read_text(encoding="utf-8")
    assert "Exact small-factor Galois intersections over E, not an unconditional K-degree." in source
    assert "QUADRATIC_QUADRATIC_SAME_FIELD" in source
    assert "QUADRATIC_QUADRATIC_DISJOINT" in source
    certificate = compositum_splitting_degree(1, _SAME)
    validate_compositum_degree(1, _SAME, certificate)
    assert _intersection(certificate)["rule"] == "QUADRATIC_QUADRATIC_SAME_FIELD"


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.compositum_deg
    witness = package.witness_same_field_degree()
    certificate = package.compositum_splitting_degree(1, _SAME)
    assert witness == certificate["degree_over_real_field"] == 2
    published = package.dispatch(
        {
            "operation": "compositum_splitting_degree",
            "conductor": 1,
            "coefficients": [["1/1", "0/1"], ["0/1", "0/1"], ["-2/1", "0/1"]],
        }
    )
    assert published["degree_over_real_field"] == 2
    assert published["authority_effect"] == "None"
    with pytest.raises(CompositumError, match="float refused"):
        package.compositum_splitting_degree(1.0, _LINEAR)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "compositum_deg.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert "not an unconditional K-degree" in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:compositum-degree:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if isinstance(value, float):\n        return\n    if False:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
    ),
    (
        "boolean conductor admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a conductor was required", role="conductor")',
        'if False and type(value) is bool:\n        raise _fail("boolean refused where a conductor was required", role="conductor")',
    ),
    (
        "boolean coordinate admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a rational coordinate was required", role=role)',
        'if type(value) is bool:\n        return\n    if False:\n        raise _fail("boolean refused where a rational coordinate was required", role=role)',
    ),
    (
        "intersection quotient replaced by product",
        "return product // intersection_degree",
        "return product * intersection_degree",
    ),
    (
        "same-field intersection degree dropped",
        '("QUADRATIC_QUADRATIC_SAME_FIELD", 2)',
        '("QUADRATIC_QUADRATIC_SAME_FIELD", 1)',
    ),
    (
        "disjoint intersection degree raised",
        '("QUADRATIC_QUADRATIC_DISJOINT", 1)',
        '("QUADRATIC_QUADRATIC_DISJOINT", 2)',
    ),
    (
        "quadratic extension degree dropped",
        'extension_degree, group = 2, "C2"',
        'extension_degree, group = 1, "C2"',
    ),
    (
        "same-field squareclass test inverted",
        '("QUADRATIC_QUADRATIC_SAME_FIELD", 2) if same_squareclass',
        '("QUADRATIC_QUADRATIC_SAME_FIELD", 2) if not same_squareclass',
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


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    witness = namespace["witness_same_field_degree"]
    degree = namespace["compositum_splitting_degree"]
    if not callable(witness) or not callable(degree):
        return False
    try:
        published = witness()
        same = degree(1, _SAME)
        disjoint = degree(1, _DISJOINT)
        quadratic = degree(1, _QUAD_2)
        linear = degree(1, _LINEAR)
    except error:
        return False
    if not isinstance(same, dict) or not isinstance(disjoint, dict):
        return False
    if not isinstance(quadratic, dict) or not isinstance(linear, dict):
        return False
    same_row = same.get("intersection_certificate")
    disjoint_row = disjoint.get("intersection_certificate")
    if not isinstance(same_row, dict) or not isinstance(disjoint_row, dict):
        return False
    squareclass = same_row.get("squareclass_certificate")
    if not isinstance(squareclass, dict):
        return False
    return bool(
        published == 2
        and type(published) is int
        and same.get("degree_over_real_field") == 2
        and same.get("coefficient_field") == "Q"
        and same.get("authority_effect") == "None"
        and same_row.get("rule") == "QUADRATIC_QUADRATIC_SAME_FIELD"
        and same_row.get("intersection_degree") == 2
        and squareclass.get("same_squareclass") is True
        and disjoint.get("degree_over_real_field") == 4
        and disjoint_row.get("rule") == "QUADRATIC_QUADRATIC_DISJOINT"
        and quadratic.get("degree_over_real_field") == 2
        and quadratic.get("degree_pattern") == [2]
        and quadratic.get("intersection_certificate") is None
        and linear.get("degree_over_real_field") == 1
        and linear.get("degree_pattern") == []
    )


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    degree = namespace["compositum_splitting_degree"]
    gaussian = namespace["GaussianRational"]
    if not callable(degree) or not callable(gaussian):
        return False
    probes = (
        (lambda: degree(1, [(_Q(1), _Q(0)), (1.5, _Q(0))]), "float refused at the public boundary"),
        (lambda: degree(True, _LINEAR), "boolean refused where a conductor was required"),
        (
            lambda: degree(1, [(True, _Q(0)), (_Q(-1), _Q(0))]),
            "boolean refused where a rational coordinate was required",
        ),
        (
            lambda: degree(1, [(gaussian(0, 1), _Q(0)), (_Q(-1), _Q(0))]),
            "Gaussian rational refused; compositum degrees in this module are over a real field",
        ),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["CompositumError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_compositum_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_compositum_{index}"
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
    finally:
        for module_name in loaded:
            sys.modules.pop(module_name, None)
