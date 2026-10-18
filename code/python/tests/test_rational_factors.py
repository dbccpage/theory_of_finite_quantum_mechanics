"""Unit, negative, integration, end-to-end, and mutation tests for rational factorization."""

from __future__ import annotations

import copy
import importlib.util
import io
import json
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.field_factors import factor_polynomial as factor_real
from src.linear_algebra.rational_factors import (
    RationalFactorError,
    dispatch,
    factor_polynomial,
    validate_factorization,
)
from src.linear_algebra import rational_factors


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "rational_factors.py"
_Q = Fraction


def _wires(certificate: dict[str, Any]) -> list[tuple[Any, Any]]:
    rows = certificate["factors"]
    assert isinstance(rows, list)
    return [(row["polynomial"], row["multiplicity"]) for row in rows]


def _raises(probe: Any, invariant: str) -> RationalFactorError:
    with pytest.raises(RationalFactorError) as caught:
        probe()
    assert caught.value.invariant == invariant
    assert all(type(item) is not float for item in caught.value.parameters.values())
    return caught.value


def test_hand_factorizations_match_exact_certificates() -> None:
    linear = factor_polynomial([1, -1])
    assert linear["schema"] == "rational_polynomial_factorization_v1"
    assert linear["authority_effect"] == "None"
    assert linear["coefficient_field"] == "Q"
    assert linear["content"] == "1/1"
    assert _wires(linear) == [(["1/1", "-1/1"], 1)]
    validate_factorization((1, -1), linear)

    split = factor_polynomial([1, 0, -1])
    assert _wires(split) == [(["1/1", "-1/1"], 1), (["1/1", "1/1"], 1)]
    validate_factorization([1, 0, -1], split)

    square = factor_polynomial([1, -2, 1])
    assert _wires(square) == [(["1/1", "-1/1"], 2)]
    validate_factorization([1, -2, 1], square)

    content = factor_polynomial([2, -2])
    assert content["content"] == "2/1"
    assert _wires(content) == [(["1/1", "-1/1"], 1)]
    validate_factorization([2, -2], content)

    assert _wires(factor_polynomial([1, 0, 1])) == [(["1/1", "0/1", "1/1"], 1)]
    cubic = factor_polynomial([1, 1, -1, -1])
    assert _wires(cubic) == [(["1/1", "-1/1"], 1), (["1/1", "1/1"], 2)]
    validate_factorization([1, 1, -1, -1], cubic)
    fourth = factor_polynomial([1, 0, 0, 0, -1])
    assert _wires(fourth) == [
        (["1/1", "-1/1"], 1),
        (["1/1", "0/1", "1/1"], 1),
        (["1/1", "1/1"], 1),
    ]
    validate_factorization([1, 0, 0, 0, -1], fourth)

    half = factor_polynomial([_Q(1, 2), _Q(-1, 2)])
    assert half["content"] == "1/2"
    assert _wires(half) == [(["1/1", "-1/1"], 1)]
    negative = factor_polynomial([-2, 2])
    assert negative["content"] == "-2/1"
    assert _wires(negative) == [(["1/1", "-1/1"], 1)]
    constant = factor_polynomial([5])
    assert constant["factors"] == []
    assert constant["content"] == "5/1"
    validate_factorization([5], constant)
    ascending = rational_factors._factor_squarefree([_Q(-1), _Q(0), _Q(1)])
    assert ascending == [[_Q(1), _Q(1)], [_Q(-1), _Q(1)]]


def test_negative_paths_record_every_invariant() -> None:
    refused = _raises(lambda: factor_polynomial([1.5, -1]), "float refused at the public boundary")
    assert refused.parameters == {"role": "coefficient", "received": "float"}
    boolean = _raises(lambda: factor_polynomial([True, -1]), "boolean refused where an exact rational was required")
    assert boolean.parameters["role"] == "coefficient"
    empty = _raises(lambda: factor_polynomial([]), "factorization: nonempty coefficient sequence required")
    assert empty.parameters["received"] == "empty"
    missing = _raises(lambda: factor_polynomial(None), "factorization: nonempty coefficient sequence required")
    assert missing.parameters["received"] == "NoneType"
    _raises(lambda: factor_polynomial(["1", "1/1"]), "factorization: exact rational coefficients required")
    _raises(lambda: factor_polynomial([0, 1]), "factorization: nonzero leading coefficient required")
    _raises(lambda: rational_factors._parse("1"), "factorization: canonical rational string required")
    _raises(lambda: rational_factors._parse("2/4"), "factorization: rational string must be reduced")
    _raises(lambda: rational_factors._parse(1.5), "float refused at the public boundary")
    _raises(lambda: rational_factors._parse_polynomial("1/1"), "factorization: coefficient array required")
    _raises(lambda: rational_factors._qdivmod([_Q(1)], []), "factorization: polynomial division by zero")
    _raises(
        lambda: rational_factors._exact_div([_Q(1)], [_Q(1), _Q(1)]),
        "factorization: nonzero exact-division remainder",
    )
    _raises(lambda: rational_factors._mod_divmod([1], [], 5), "factorization: modular polynomial division by zero")
    _raises(lambda: rational_factors._mod_inverse([1, 1], [1, 1], 5), "factorization: Hensel factors are not coprime")
    _raises(lambda: rational_factors._require_exact_split([1]), "factorization: Berlekamp split has a remainder")
    _raises(lambda: rational_factors._census_failure(1, 2), "factorization: Berlekamp factor census differs from nullity")
    _raises(
        lambda: rational_factors._lifting_digit([1], 3),
        "factorization: Hensel product does not match input modulo current modulus",
    )
    _raises(
        lambda: rational_factors._require_lifted_product([1], [0]),
        "factorization: lifted product does not match input",
    )
    _raises(
        lambda: rational_factors._integer_root_ceiling(-1, 1),
        "factor_bound: nonnegative integer and positive integer exponent required",
    )
    _raises(lambda: rational_factors._root_radius([1]), "factor_bound: nonconstant monic integer polynomial required")
    _raises(
        lambda: rational_factors._integer_quotient([_Q(1, 2)]),
        "factorization: monic integer divisor gave noninteger quotient",
    )

    split = factor_polynomial([1, 0, -1])
    _raises(lambda: validate_factorization([1, 0, -1], []), "factorization: exact output field census required")
    metadata = copy.deepcopy(split)
    metadata["algorithm"] = "APPROXIMATE"
    _raises(
        lambda: validate_factorization([1, 0, -1], metadata),
        "factorization: schema or arithmetic-domain binding differs",
    )
    rebound = copy.deepcopy(split)
    rebound["coefficients"] = ["1/1", "0/1", "1/1"]
    _raises(
        lambda: validate_factorization([1, 0, -1], rebound),
        "factorization: original polynomial binding differs",
    )
    content = copy.deepcopy(split)
    content["content"] = "2/1"
    _raises(
        lambda: validate_factorization([1, 0, -1], content),
        "factorization: content differs from original leading coefficient",
    )
    rows = copy.deepcopy(split)
    rows["factors"] = None
    _raises(lambda: validate_factorization([1, 0, -1], rows), "factorization: factor array required")
    fields = copy.deepcopy(split)
    fields["factors"] = [{"polynomial": ["1/1", "-1/1"]}]
    _raises(lambda: validate_factorization([1, 0, -1], fields), "factorization: exact factor fields required")
    skewed = copy.deepcopy(split)
    skewed["factors"] = [{"polynomial": ["2/1", "-2/1"], "multiplicity": 1}]
    _raises(
        lambda: validate_factorization([1, 0, -1], skewed),
        "factorization: nonconstant monic factor required",
    )
    counted = copy.deepcopy(split)
    counted["factors"][0]["multiplicity"] = True
    boolean_count = _raises(
        lambda: validate_factorization([1, 0, -1], counted),
        "boolean refused where an exact integer was required",
    )
    assert boolean_count.parameters["role"] == "multiplicity"
    floated = copy.deepcopy(split)
    floated["factors"][0]["multiplicity"] = 1.5
    floated_count = _raises(
        lambda: validate_factorization([1, 0, -1], floated),
        "float refused at the public boundary",
    )
    assert floated_count.parameters["role"] == "multiplicity"
    zero = copy.deepcopy(split)
    zero["factors"][0]["multiplicity"] = 0
    _raises(
        lambda: validate_factorization([1, 0, -1], zero),
        "factorization: bounded positive integer multiplicity required",
    )
    ordered = copy.deepcopy(split)
    ordered["factors"] = list(reversed(ordered["factors"]))
    _raises(
        lambda: validate_factorization([1, 0, -1], ordered),
        "factorization: factors must be distinct and numerically ordered",
    )
    heavy = copy.deepcopy(split)
    heavy["factors"] = [{"polynomial": ["1/1", "0/1", "1/1"], "multiplicity": 2}]
    _raises(
        lambda: validate_factorization([1, 0, -1], heavy),
        "factorization: factor degree census exceeds input degree",
    )
    reducible = copy.deepcopy(split)
    reducible["factors"] = [{"polynomial": ["1/1", "0/1", "-1/1"], "multiplicity": 1}]
    _raises(
        lambda: validate_factorization([1, 0, -1], reducible),
        "factorization: supplied factor is reducible over Q",
    )
    swapped = factor_polynomial([1, 0, 1])
    swapped["factors"] = [
        {"polynomial": ["1/1", "-1/1"], "multiplicity": 1},
        {"polynomial": ["1/1", "1/1"], "multiplicity": 1},
    ]
    _raises(
        lambda: validate_factorization([1, 0, 1], swapped),
        "factorization: exact factor product does not reconstruct original polynomial",
    )
    _raises(lambda: dispatch({}), "factorization: exact request fields and factor operation required")
    _raises(lambda: rational_factors._reject_inexact("1.5"), "factorization: inexact JSON number forbidden")


def test_integration_matches_rust_and_real_field() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "rational_factors.rs").read_text(encoding="utf-8")
    assert "Exact rational factorization, not a splitting-field or dependence certificate." in source
    assert "AuthorityEffect: None." in source
    assert "rational_polynomial_factorization_v1" in source
    assert "EXACT_BERLEKAMP_HENSEL_RECOMBINATION" in source
    embedded = factor_real(1, [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(-1), _Q(0))])
    assert _wires(embedded) == [
        ([["1/1", "0/1"], ["-1/1", "0/1"]], 1),
        ([["1/1", "0/1"], ["1/1", "0/1"]], 1),
    ]
    quadratic = factor_real(8, [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(-2), _Q(0))])
    assert quadratic["coefficient_field"] == "Q(sqrt(2))"
    assert quadratic["authority_effect"] == "None"
    assert _wires(quadratic) == [
        ([["1/1", "0/1"], ["0/1", "-1/1"]], 1),
        ([["1/1", "0/1"], ["0/1", "1/1"]], 1),
    ]


def test_end_to_end_public_contract(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    package = linear_algebra.rational_factors
    request = {"operation": "factor", "coefficients": ["1/1", "0/1", "-1/1"]}
    published = package.dispatch(request)
    package.validate_factorization([1, 0, -1], published)
    assert published["schema"] == "rational_polynomial_factorization_v1"
    assert published["authority_effect"] == "None"
    assert _wires(published) == [(["1/1", "-1/1"], 1), (["1/1", "1/1"], 1)]

    monkeypatch.setattr(sys, "argv", ["rational_factors.py", "--extra"])
    assert package.main() == 2
    assert "stdin request only" in capsys.readouterr().err

    monkeypatch.setattr(sys, "argv", ["rational_factors.py"])
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(json.dumps(request).encode("ascii")), encoding="ascii"))
    assert package.main() == 0
    stdout = capsys.readouterr().out
    assert json.loads(stdout)["authority_effect"] == "None"
    assert stdout == json.dumps(json.loads(stdout), sort_keys=True, separators=(",", ":")) + "\n"

    floated = b'{"operation":"factor","coefficients":[1.5]}'
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(floated), encoding="ascii"))
    assert package.main() == 2
    assert "inexact JSON number forbidden" in capsys.readouterr().err


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "rational_factors.rs"
    assert origin.is_file()
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:rational-polynomial-factorization:v1" in source
    assert "Scope Fence:" in source
    assert "Gate 5 measurement:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if isinstance(value, float):\n        return Q(value)',
    ),
    (
        "boolean multiplicity admitted",
        'if type(count) is bool:\n        raise _fail("boolean refused where an exact integer was required", role="multiplicity")',
        'if False and type(count) is bool:\n        raise _fail("boolean refused where an exact integer was required", role="multiplicity")',
    ),
    (
        "schema renamed",
        'SCHEMA = "rational_polynomial_factorization_v1"',
        'SCHEMA = "rational_polynomial_factorization_v2"',
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
        "leading content replaced",
        '"content": _fraction_text(values[0]),',
        '"content": _fraction_text(Q(1)),',
    ),
    (
        "half-degree recombination dropped",
        "if degree > n // 2:",
        "if degree >= 0:",
    ),
    (
        "authority ceiling raised",
        '"schema": SCHEMA,\n        "authority_effect": "None",\n        "coefficient_field": "Q",',
        '"schema": SCHEMA,\n        "authority_effect": "Some",\n        "coefficient_field": "Q",',
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
    factor = namespace["factor_polynomial"]
    verify = namespace["validate_factorization"]
    if not callable(factor) or not callable(verify):
        return False
    try:
        split = factor([1, 0, -1])
        square = factor([1, -2, 1])
        content = factor([2, -2])
        verify([1, 0, -1], split)
        verify([1, -2, 1], square)
        verify([2, -2], content)
    except error:
        return False
    if not isinstance(split, dict) or not isinstance(square, dict) or not isinstance(content, dict):
        return False
    split_rows = _wires(split)
    square_rows = _wires(square)
    content_rows = _wires(content)
    return bool(
        split.get("schema") == "rational_polynomial_factorization_v1"
        and split.get("authority_effect") == "None"
        and split.get("coefficient_field") == "Q"
        and split.get("content") == "1/1"
        and split_rows == [(["1/1", "-1/1"], 1), (["1/1", "1/1"], 1)]
        and square_rows == [(["1/1", "-1/1"], 2)]
        and content.get("content") == "2/1"
        and content_rows == [(["1/1", "-1/1"], 1)]
    )


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    factor = namespace["factor_polynomial"]
    verify = namespace["validate_factorization"]
    if not callable(factor) or not callable(verify):
        return False
    try:
        published = factor([1, 0, -1])
    except error:
        return False
    if not isinstance(published, dict):
        return False
    boolean = copy.deepcopy(published)
    rows = boolean.get("factors")
    if not isinstance(rows, list) or not rows or not isinstance(rows[0], dict):
        return False
    rows[0]["multiplicity"] = True
    probes = (
        (lambda: factor([1.5, -1.5]), "float refused at the public boundary"),
        (lambda: verify([1, 0, -1], boolean), "boolean refused where an exact integer was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["RationalFactorError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_rational_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_rational_{index}"
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
