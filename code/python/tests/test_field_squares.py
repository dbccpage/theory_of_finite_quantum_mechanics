"""Unit, negative, integration, end-to-end, and mutation tests for real squares."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.field_squares import (
    FieldSquareError,
    _orient_root,
    dispatch,
    square_certificate,
    squareclass_certificate,
    validate_square_certificate,
    validate_squareclass_certificate,
    witness_positive_root,
)
from src.linear_algebra.scalars import GaussianRational

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "field_squares.py"


def test_square_certificates_match_hand_values() -> None:
    assert witness_positive_root() == Fraction(2)
    assert type(witness_positive_root()) is Fraction
    four = square_certificate(1, (4, 0))
    assert four["is_square"] is True
    assert four["root"] == ["2/1", "0/1"]
    assert four["obstruction"] is None
    assert four["real_generator_radicand"] == 0
    validate_square_certificate(1, (4, 0), four)
    two = square_certificate(1, (2, 0))
    assert two["is_square"] is False
    assert two["root"] is None
    assert two["obstruction"] == "RATIONAL_NONSQUARE"
    validate_square_certificate(1, (2, 0), two)
    fraction = square_certificate(1, (Fraction(9, 4), 0))
    assert fraction["root"] == ["3/2", "0/1"]
    mixed = square_certificate(5, (6, 2))
    assert mixed["root"] == ["1/1", "1/1"]
    assert mixed["real_generator_radicand"] == 5
    validate_square_certificate(5, (6, 2), mixed)
    oriented = square_certificate(5, (6, -2))
    assert oriented["root"] == ["-1/1", "1/1"]
    assert square_certificate(5, (5, 0))["root"] == ["0/1", "1/1"]
    assert square_certificate(8, (2, 0))["root"] == ["0/1", "1/1"]
    assert square_certificate(8, (2, 0))["real_generator_radicand"] == 2
    assert square_certificate(5, (1, 1))["obstruction"] == "NORM_NOT_RATIONAL_SQUARE"
    same = squareclass_certificate(1, (8, 0), (2, 0))
    assert same["same_squareclass"] is True
    assert same["quotient"] == ["4/1", "0/1"]
    validate_squareclass_certificate(1, (8, 0), (2, 0), same)
    different = squareclass_certificate(1, (2, 0), (3, 0))
    assert different["same_squareclass"] is False
    assert different["quotient"] == ["2/3", "0/1"]
    request = dispatch({"operation": "square", "conductor": 1, "coefficients": ["4/1", "0/1"]})
    assert request["root"] == ["2/1", "0/1"]
    ratio = dispatch(
        {
            "operation": "squareclass",
            "conductor": 1,
            "left": ["8/1", "0/1"],
            "right": ["2/1", "0/1"],
        }
    )
    assert ratio["same_squareclass"] is True


def test_negative_boundary_failures() -> None:
    with pytest.raises(FieldSquareError, match="float refused") as floated:
        square_certificate(1, (1.5, 0))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "coordinate[0]"

    with pytest.raises(FieldSquareError, match="boolean refused") as boolean_coordinate:
        square_certificate(1, (True, 0))
    assert boolean_coordinate.value.invariant == "boolean refused where a rational coordinate was required"

    with pytest.raises(FieldSquareError, match="Gaussian") as gaussian:
        square_certificate(1, (GaussianRational(0, 1), 0))
    assert gaussian.value.parameters["role"] == "coordinate[0]"

    with pytest.raises(FieldSquareError, match="boolean refused") as boolean_conductor:
        square_certificate(True, (4, 0))
    assert boolean_conductor.value.invariant == "boolean refused where a conductor was required"

    with pytest.raises(FieldSquareError, match="unsupported") as conductor:
        square_certificate(7, (1, 0))
    assert conductor.value.parameters["received"] == "int"

    with pytest.raises(FieldSquareError, match="zero radical") as radical:
        square_certificate(1, (1, 1))
    assert radical.value.parameters["conductor"] == 1

    with pytest.raises(FieldSquareError, match="exact rational coordinates") as text:
        square_certificate(1, ("1", 0))
    assert text.value.invariant == "real_field: exact rational coordinates required"
    assert text.value.parameters["received"] == "str"

    with pytest.raises(FieldSquareError, match="reduced") as unreduced:
        dispatch({"operation": "square", "conductor": 1, "coefficients": ["2/4", "0/1"]})
    assert unreduced.value.invariant == "real_field: rational string must be reduced"

    with pytest.raises(FieldSquareError, match="reconstruction failed") as rebuilt:
        _orient_root((Fraction(1), Fraction(0)), (Fraction(4), Fraction(0)), 0)
    assert rebuilt.value.invariant == "square_certificate: root reconstruction failed"

    bad_root = dict(square_certificate(1, (4, 0)))
    bad_root["root"] = ["1/1", "0/1"]
    with pytest.raises(FieldSquareError, match="does not square") as supplied:
        validate_square_certificate(1, (4, 0), bad_root)
    assert supplied.value.invariant == "square_certificate: supplied root does not square to the input"

    negative = dict(square_certificate(1, (4, 0)))
    negative["root"] = ["-2/1", "0/1"]
    with pytest.raises(FieldSquareError, match="negative embedding") as signed:
        validate_square_certificate(1, (4, 0), negative)
    assert signed.value.invariant == "square_certificate: supplied root has negative embedding sign"

    carried = dict(square_certificate(1, (4, 0)))
    carried["obstruction"] = "RATIONAL_NONSQUARE"
    with pytest.raises(FieldSquareError, match="cannot carry") as obstruction:
        validate_square_certificate(1, (4, 0), carried)
    assert obstruction.value.invariant == "square_certificate: a root cannot carry a nonsquare obstruction"

    nonsquare = dict(square_certificate(1, (2, 0)))
    nonsquare["root"] = ["1/1", "0/1"]
    with pytest.raises(FieldSquareError, match="has a root") as rooted:
        validate_square_certificate(1, (2, 0), nonsquare)
    assert rooted.value.invariant == "square_certificate: nonsquare certificate has a root"

    wrong_reason = dict(square_certificate(1, (2, 0)))
    wrong_reason["obstruction"] = "NORM_NOT_RATIONAL_SQUARE"
    with pytest.raises(FieldSquareError, match="obstruction differs") as reason:
        validate_square_certificate(1, (2, 0), wrong_reason)
    assert reason.value.invariant == "square_certificate: nonsquare obstruction differs"

    with pytest.raises(FieldSquareError, match="field census") as census:
        validate_square_certificate(1, (4, 0), {})
    assert census.value.invariant == "square_certificate: exact field census required"

    unbound = dict(square_certificate(1, (4, 0)))
    unbound["conductor"] = 5
    with pytest.raises(FieldSquareError, match="field binding") as binding:
        validate_square_certificate(1, (4, 0), unbound)
    assert binding.value.invariant == "square_certificate: original input or field binding differs"

    verdict = dict(square_certificate(1, (4, 0)))
    verdict["is_square"] = "yes"
    with pytest.raises(FieldSquareError, match="Boolean square verdict") as flag:
        validate_square_certificate(1, (4, 0), verdict)
    assert flag.value.invariant == "square_certificate: Boolean square verdict required"

    with pytest.raises(FieldSquareError, match="nonzero") as zero:
        squareclass_certificate(1, (0, 0), (1, 0))
    assert zero.value.invariant == "squareclass: both arguments must be nonzero"

    tampered = dict(squareclass_certificate(1, (8, 0), (2, 0)))
    tampered["quotient"] = ["1/1", "0/1"]
    with pytest.raises(FieldSquareError, match="does not reconstruct") as quotient:
        validate_squareclass_certificate(1, (8, 0), (2, 0), tampered)
    assert quotient.value.invariant == "squareclass: quotient does not reconstruct the original arguments"

    flipped = dict(squareclass_certificate(1, (8, 0), (2, 0)))
    flipped["same_squareclass"] = False
    with pytest.raises(FieldSquareError, match="verdict differs") as verdict_gap:
        validate_squareclass_certificate(1, (8, 0), (2, 0), flipped)
    assert verdict_gap.value.invariant == "squareclass: quotient square verdict differs"

    with pytest.raises(FieldSquareError, match="request object") as foreign:
        dispatch("square")
    assert foreign.value.parameters["received"] == "str"

    with pytest.raises(FieldSquareError, match="known operation") as operation:
        dispatch({"operation": "degree"})
    assert operation.value.invariant == "real_field: exact request fields and known operation required"


def test_integration_matches_rust_square_sentence() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "field_squares.rs").read_text(encoding="utf-8")
    assert "Exact square and squareclass certificates in Q, Q(sqrt(2)), Q(sqrt(5))." in source
    assert "RATIONAL_NONSQUARE" in source
    certificate = square_certificate(5, (6, 2))
    validate_square_certificate(5, (6, 2), certificate)
    assert certificate["root"] == ["1/1", "1/1"]


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.field_squares
    assert package.witness_positive_root() == Fraction(2)
    certificate = package.square_certificate(4, (9, 0))
    assert certificate["root"] == ["3/1", "0/1"]
    assert package.squareclass_certificate(1, (8, 0), (2, 0))["same_squareclass"] is True
    with pytest.raises(FieldSquareError, match="float refused"):
        package.square_certificate(1, (0.25, 0))


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "field_squares.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert "Q(sqrt(2))" in text
    assert "Q(sqrt(5))" in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:real-square-certificate:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if isinstance(value, float):\n        return\n    if False:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
    ),
    (
        "boolean coordinate admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a rational coordinate was required", role=role)',
        'if type(value) is bool:\n        return Q(1)\n    if False:\n        raise _fail("boolean refused where a rational coordinate was required", role=role)',
    ),
    (
        "boolean conductor admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a conductor was required", role="conductor")',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a conductor was required", role="conductor")',
    ),
    (
        "rational square test inverted",
        "numerator * numerator != value.numerator",
        "numerator * numerator == value.numerator",
    ),
    (
        "field multiplication sign inverted",
        "return a * c + d * b * e, a * e + b * c",
        "return a * c - d * b * e, a * e + b * c",
    ),
    (
        "root orientation inverted",
        "if _sign(root, d) < 0:\n        return -root[0], -root[1]",
        "if _sign(root, d) > 0:\n        return -root[0], -root[1]",
    ),
    (
        "square verdict inverted",
        '"is_square": published is not None,',
        '"is_square": published is None,',
    ),
    (
        "half-trace denominator dropped",
        "return x, b / (2 * x)",
        "return x, b / x",
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
    witness = namespace["witness_positive_root"]
    square = namespace["square_certificate"]
    squareclass = namespace["squareclass_certificate"]
    if not callable(witness) or not callable(square) or not callable(squareclass):
        return False
    try:
        root = witness()
        four = square(1, (4, 0))
        mixed = square(5, (6, 2))
        oriented = square(5, (6, -2))
        same = squareclass(1, (8, 0), (2, 0))
    except error:
        return False
    if not isinstance(four, dict) or not isinstance(mixed, dict) or not isinstance(oriented, dict):
        return False
    if not isinstance(same, dict):
        return False
    return bool(
        root == Fraction(2)
        and type(root) is Fraction
        and four.get("is_square") is True
        and four.get("root") == ["2/1", "0/1"]
        and mixed.get("root") == ["1/1", "1/1"]
        and oriented.get("root") == ["-1/1", "1/1"]
        and same.get("same_squareclass") is True
        and same.get("quotient") == ["4/1", "0/1"]
    )


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    square = namespace["square_certificate"]
    gaussian = namespace["GaussianRational"]
    if not callable(square) or not callable(gaussian):
        return False
    probes = (
        (lambda: square(1, (1.5, 0)), "float refused at the public boundary"),
        (lambda: square(1, (True, 0)), "boolean refused where a rational coordinate was required"),
        (
            lambda: square(1, (gaussian(0, 1), 0)),
            "Gaussian rational refused; square certificates in this module are over a real field",
        ),
        (lambda: square(True, (4, 0)), "boolean refused where a conductor was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["FieldSquareError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_square_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_square_{index}"
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
