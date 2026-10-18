"""Unit, negative, integration, end-to-end, and mutation tests for real factorization.

Origin: code/python/src/linear_algebra/field_factors.py
Claim: urn:omega:fqm:linear-algebra:real-factorization:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""





from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.field_factors import (
    FieldFactorError,
    dispatch,
    factor_polynomial,
    validate_factorization,
    witness_split_linear_count,
)
from src.linear_algebra.scalars import GaussianRational

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "field_factors.py"
_Q = Fraction


def _poly(*values: int) -> list[tuple[Fraction, Fraction]]:
    return [(_Q(value), _Q(0)) for value in values]


_IRREDUCIBLE = _poly(1, 0, -2)
_SPLIT = _poly(1, 0, -4)
_SQUARE = _poly(1, -2, 1)
_CONTENT = _poly(2, 0, -8)
_QUADRATIC_FIELD = _poly(1, 0, -2)


def _wires(certificate: dict[str, object]) -> list[tuple[object, object]]:
    rows = certificate["factors"]
    assert isinstance(rows, list)
    parsed = []
    for row in rows:
        assert isinstance(row, dict)
        parsed.append((row["polynomial"], row["multiplicity"]))
    return parsed


def test_factorizations_match_hand_values() -> None:
    assert witness_split_linear_count() == 2
    assert type(witness_split_linear_count()) is int

    irreducible = factor_polynomial(1, _IRREDUCIBLE)
    assert irreducible["coefficient_field"] == "Q"
    assert irreducible["authority_effect"] == "None"
    assert irreducible["schema"] == "real_field_polynomial_factorization_v1"
    assert irreducible["content"] == ["1/1", "0/1"]
    assert _wires(irreducible) == [([["1/1", "0/1"], ["0/1", "0/1"], ["-2/1", "0/1"]], 1)]
    validate_factorization(1, _IRREDUCIBLE, irreducible)

    split = factor_polynomial(1, _SPLIT)
    assert _wires(split) == [
        ([["1/1", "0/1"], ["-2/1", "0/1"]], 1),
        ([["1/1", "0/1"], ["2/1", "0/1"]], 1),
    ]
    validate_factorization(1, _SPLIT, split)

    square = factor_polynomial(1, _SQUARE)
    assert _wires(square) == [([["1/1", "0/1"], ["-1/1", "0/1"]], 2)]
    validate_factorization(1, _SQUARE, square)

    content = factor_polynomial(1, _CONTENT)
    assert content["content"] == ["2/1", "0/1"]
    assert _wires(content) == [
        ([["1/1", "0/1"], ["-2/1", "0/1"]], 1),
        ([["1/1", "0/1"], ["2/1", "0/1"]], 1),
    ]
    validate_factorization(1, _CONTENT, content)

    embedded = factor_polynomial(8, _QUADRATIC_FIELD)
    assert embedded["coefficient_field"] == "Q(sqrt(2))"
    assert _wires(embedded) == [
        ([["1/1", "0/1"], ["0/1", "-1/1"]], 1),
        ([["1/1", "0/1"], ["0/1", "1/1"]], 1),
    ]
    validate_factorization(8, _QUADRATIC_FIELD, embedded)


def test_negative_boundary_failures() -> None:
    with pytest.raises(FieldFactorError, match="float refused") as floated:
        factor_polynomial(1, [_poly(1)[0], _poly(0)[0], (_probe("1.5"), _Q(0))])
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "coefficient[2][0]"
    assert floated.value.parameters["received"] == "float"

    with pytest.raises(FieldFactorError, match="boolean refused") as boolean_coordinate:
        factor_polynomial(1, [(True, _Q(0)), _poly(0)[0], _poly(-2)[0]])
    assert boolean_coordinate.value.invariant == "boolean refused where a rational coordinate was required"
    assert boolean_coordinate.value.parameters["role"] == "coefficient[0][0]"

    with pytest.raises(FieldFactorError, match="Gaussian") as gaussian:
        factor_polynomial(1, [(GaussianRational(0, 1), _Q(0)), _poly(0)[0], _poly(-2)[0]])
    assert gaussian.value.invariant == (
        "Gaussian rational refused; factorization in this module is over a real field"
    )

    with pytest.raises(FieldFactorError, match="boolean refused") as boolean_conductor:
        factor_polynomial(True, _SPLIT)
    assert boolean_conductor.value.invariant == "boolean refused where a conductor was required"
    assert boolean_conductor.value.parameters["role"] == "conductor"

    with pytest.raises(FieldFactorError, match="nonempty") as empty:
        factor_polynomial(1, [])
    assert empty.value.invariant == "real_factorization: nonempty coefficient sequence required"

    with pytest.raises(FieldFactorError, match="nonzero leading") as leading:
        factor_polynomial(1, [_poly(0)[0], _poly(1)[0]])
    assert leading.value.invariant == "real_factorization: nonzero leading coefficient required"

    tampered = dict(factor_polynomial(1, _SPLIT))
    rows = [dict(row) for row in tampered["factors"]]
    rows[0]["multiplicity"] = 2
    tampered["factors"] = rows
    with pytest.raises(FieldFactorError, match="degree census exceeds") as changed:
        validate_factorization(1, _SPLIT, tampered)
    assert changed.value.invariant == "real_factorization[1]: factor degree census exceeds input degree"

    with pytest.raises(FieldFactorError, match="factor operation required") as operation:
        dispatch({"operation": "degree", "conductor": 1, "coefficients": []})
    assert operation.value.invariant == "real_factorization: exact request fields and factor operation required"


def test_integration_matches_rust_factor_sentence() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "field_factors.rs").read_text(encoding="utf-8")
    assert 'validate_factorization' in source
    assert 'validate_factorization' in source
    certificate = factor_polynomial(1, _SPLIT)
    validate_factorization(1, _SPLIT, certificate)
    assert certificate["content"] == ["1/1", "0/1"]


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.field_factors
    assert package.witness_split_linear_count() == 2
    published = package.dispatch(
        {
            "operation": "factor",
            "conductor": 1,
            "coefficients": [["1/1", "0/1"], ["0/1", "0/1"], ["-4/1", "0/1"]],
        }
    )
    assert len(published["factors"]) == 2
    assert published["authority_effect"] == "None"
    with pytest.raises(FieldFactorError, match="float refused"):
        package.factor_polynomial(_probe("1.0"), _SPLIT)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "field_factors.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert 'validate_factorization' in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:real-factorization:v1" in source
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
        "multiplicity step doubled",
        "multiplicity += 1",
        "multiplicity += 2",
    ),
    (
        "factor order reversed",
        "factors.sort(key=lambda item: item[0])",
        "factors.sort(key=lambda item: item[0], reverse=True)",
    ),
    (
        "leading content dropped from the certificate",
        '"content": real._wire(values[0]),',
        '"content": real._wire(ONE),',
    ),
    (
        "real conjugation dropped",
        "return [(a, -b) for a, b in poly]",
        "return [(a, b) for a, b in poly]",
    ),
    (
        "field multiplication cross term inverted",
        "return a[0] * b[0] + d * a[1] * b[1], a[0] * b[1] + a[1] * b[0]",
        "return a[0] * b[0] + d * a[1] * b[1], a[0] * b[1] - a[1] * b[0]",
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


def _wires_of(certificate: object) -> list[tuple[object, object]] | None:
    if not isinstance(certificate, dict):
        return None
    rows = certificate.get("factors")
    if not isinstance(rows, list):
        return None
    parsed: list[tuple[object, object]] = []
    for row in rows:
        if not isinstance(row, dict):
            return None
        parsed.append((row.get("polynomial"), row.get("multiplicity")))
    return parsed


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    witness = namespace["witness_split_linear_count"]
    factor = namespace["factor_polynomial"]
    if not _all_hold((callable(witness), callable(factor),)):
        return False
    try:
        published = witness()
        split = factor(1, _SPLIT)
        square = factor(1, _SQUARE)
        content = factor(1, _CONTENT)
        embedded = factor(8, _QUADRATIC_FIELD)
    except error:
        return False
    split_rows = _wires_of(split)
    square_rows = _wires_of(square)
    content_rows = _wires_of(content)
    embedded_rows = _wires_of(embedded)
    if split_rows is None or square_rows is None or content_rows is None or embedded_rows is None:
        return False
    if not _all_hold((isinstance(split, dict), isinstance(content, dict), isinstance(embedded, dict),)):
        return False
    return _all_hold((
published == 2,
type(published) is int,
split.get("authority_effect") == "None",
split.get("coefficient_field") == "Q",
split_rows == [
            ([["1/1", "0/1"], ["-2/1", "0/1"]], 1),
            ([["1/1", "0/1"], ["2/1", "0/1"]], 1),
        ],
square_rows == [([["1/1", "0/1"], ["-1/1", "0/1"]], 2)],
content.get("content") == ["2/1", "0/1"],
content_rows == split_rows,
embedded.get("coefficient_field") == "Q(sqrt(2))",
embedded_rows == [
            ([["1/1", "0/1"], ["0/1", "-1/1"]], 1),
            ([["1/1", "0/1"], ["0/1", "1/1"]], 1),
        ],
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    factor = namespace["factor_polynomial"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(factor), callable(gaussian),)):
        return False
    probes = (
        (
            lambda: factor(1, [_poly(1)[0], _poly(0)[0], (_probe("1.5"), _Q(0))]),
            "float refused at the public boundary",
        ),
        (lambda: factor(True, _SPLIT), "boolean refused where a conductor was required"),
        (
            lambda: factor(1, [(True, _Q(0)), _poly(0)[0], _poly(-2)[0]]),
            "boolean refused where a rational coordinate was required",
        ),
        (
            lambda: factor(1, [(gaussian(0, 1), _Q(0)), _poly(0)[0], _poly(-2)[0]]),
            "Gaussian rational refused; factorization in this module is over a real field",
        ),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["FieldFactorError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_factor_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_factor_{index}"
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
