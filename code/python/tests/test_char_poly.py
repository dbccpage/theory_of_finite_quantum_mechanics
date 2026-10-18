"""Unit, negative, integration, end-to-end, and mutation tests for the characteristic polynomial.

Origin: code/python/src/linear_algebra/char_poly.py
Claim: urn:omega:fqm:linear-algebra:characteristic-polynomial:v1
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
from src.linear_algebra.char_poly import (
    CharacteristicError,
    ExactMatrix,
    _require_constant_term,
    _require_zero_defect,
    cayley_hamilton_defect,
    certify_characteristic_polynomial,
    characteristic_coefficients,
    matrix_polynomial,
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "char_poly.py"


def _pair() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(2)],
            [Fraction(3), Fraction(4)],
        ]
    )


def _diagonal() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(2), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(3), Fraction(0)],
            [Fraction(0), Fraction(0), Fraction(4)],
        ]
    )


def test_coefficients_match_the_hand_polynomial() -> None:
    assert characteristic_coefficients(_pair()) == [Fraction(1), Fraction(-5), Fraction(-2)]
    assert characteristic_coefficients(_diagonal()) == [
        Fraction(1),
        Fraction(-9),
        Fraction(26),
        Fraction(-24),
    ]
    assert characteristic_coefficients(ExactMatrix.from_rows([[Fraction(5)]])) == [
        Fraction(1),
        Fraction(-5),
    ]
    assert cayley_hamilton_defect(_pair()) == 0
    assert cayley_hamilton_defect(_diagonal()) == 0
    assert type(characteristic_coefficients(_pair())[1]) is Fraction


def test_negative_boundary_failures() -> None:
    with pytest.raises(CharacteristicError, match="float refused") as floated:
        characteristic_coefficients(ExactMatrix.from_rows([[_probe("1.5")]]))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0]"
    assert type(floated.value) is CharacteristicError

    with pytest.raises(CharacteristicError, match="boolean refused where a rational") as boolean:
        characteristic_coefficients(ExactMatrix.from_rows([[True]]))
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(CharacteristicError, match="Gaussian rational refused") as gaussian:
        characteristic_coefficients(ExactMatrix.from_rows([[GaussianRational(0, 1)]]))
    assert gaussian.value.parameters["role"] == "entry[0]"

    with pytest.raises(CharacteristicError, match="not an exact rational") as text:
        characteristic_coefficients(ExactMatrix.from_rows([["1"]]))
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = True
    with pytest.raises(CharacteristicError, match="boolean refused where a matrix dimension") as dim_bool:
        characteristic_coefficients(shaped)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = _probe("1.0")
    with pytest.raises(CharacteristicError, match="float refused") as dim_float:
        characteristic_coefficients(shaped)
    assert dim_float.value.parameters["role"] == "rows"

    with pytest.raises(CharacteristicError, match="negative") as negative:
        characteristic_coefficients(ExactMatrix(-1, 0, []))
    assert negative.value.parameters["received"] == -1

    named = ExactMatrix.from_rows([[Fraction(1)]])
    named.rows = "1"
    with pytest.raises(CharacteristicError, match="not an integer") as named_error:
        characteristic_coefficients(named)
    assert named_error.value.parameters["received"] == "str"

    with pytest.raises(CharacteristicError, match="not an ExactMatrix") as bare:
        characteristic_coefficients("matrix")
    assert bare.value.parameters["received"] == "str"

    with pytest.raises(CharacteristicError, match="square") as wide:
        characteristic_coefficients(ExactMatrix.from_rows([[Fraction(1), Fraction(2)]]))
    assert wide.value.parameters["cols"] == 2

    mismatched = ExactMatrix.identity(2)
    mismatched.rows = 3
    mismatched.cols = 3
    with pytest.raises(CharacteristicError, match="data length") as length_error:
        characteristic_coefficients(mismatched)
    assert length_error.value.parameters["length"] == 4

    with pytest.raises(CharacteristicError, match="constant term") as constant:
        _require_constant_term(ExactMatrix.from_rows([[Fraction(5)]]), [Fraction(0)])
    assert constant.value.parameters["n"] == 1

    with pytest.raises(CharacteristicError, match="coefficient count") as counted:
        matrix_polynomial(ExactMatrix.from_rows([[Fraction(5)]]), [Fraction(1)])
    assert counted.value.parameters["count"] == 1

    with pytest.raises(CharacteristicError, match="float refused") as coeff_float:
        matrix_polynomial(ExactMatrix.from_rows([[Fraction(5)]]), [_probe("1.5"), Fraction(1)])
    assert coeff_float.value.parameters["role"] == "coeff[0]"

    with pytest.raises(CharacteristicError, match="Cayley-Hamilton defect") as defect:
        _require_zero_defect(Fraction(1), 2)
    assert defect.value.parameters["degree"] == 2


def test_integration_matches_elimination_and_the_cited_degree() -> None:
    root = Path(__file__).resolve().parents[3]
    rust = (root / "code" / "rust" / "src" / "linear_algebra" / "char_poly.rs").read_text(encoding="utf-8")
    note = (root / "evidence" / "dossiers" / "reduction_proof.md").read_text(encoding="utf-8")
    assert 'characteristic_polynomial' in rust
    assert 'characteristic_polynomial' in rust
    assert "The characteristic polynomial" in note
    assert "has degree $d$" in note
    source = _pair()
    coeffs = characteristic_coefficients(source)
    assert coeffs == [Fraction(1), Fraction(-5), Fraction(-2)]
    assert source.determinant() == Fraction(-2)
    assert (-1) ** source.rows * source.determinant() == coeffs[-1]
    shifted = ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(-2)],
            [Fraction(-3), Fraction(-2)],
        ]
    )
    evaluated = Fraction(4) + Fraction(-5) * 2 + Fraction(-2)
    assert evaluated == Fraction(-8)
    assert shifted.determinant() == evaluated
    value = matrix_polynomial(source, coeffs)
    assert value == ExactMatrix.zeros(2, 2)


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.char_poly
    certified = package.certify_characteristic_polynomial(_diagonal())
    assert certified == (Fraction(1), Fraction(-9), Fraction(26), Fraction(-24))
    assert package.cayley_hamilton_defect(ExactMatrix(0, 0, [])) == 0
    assert package.characteristic_coefficients(ExactMatrix(0, 0, [])) == [Fraction(1)]
    scalar = package.certify_characteristic_polynomial(ExactMatrix.from_rows([[Fraction(5)]]))
    assert scalar == (Fraction(1), Fraction(-5))
    tampered = ExactMatrix.identity(1)
    tampered.data[0] = _probe("0.25")
    with pytest.raises(CharacteristicError, match="float refused"):
        package.certify_characteristic_polynomial(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    rust = root / "code" / "rust" / "src" / "linear_algebra" / "char_poly.rs"
    note = root / "evidence" / "dossiers" / "reduction_proof.md"
    assert rust.is_file()
    assert note.is_file()
    assert 'the_minimal_polynomial_annihilates_divides_the_characteristic_polynomial_and_is_minimal' in rust.read_text(encoding="utf-8")
    assert "has degree $d$" in note.read_text(encoding="utf-8")
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:characteristic-polynomial:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if isinstance(value, float):\n        return\n    if False:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
    ),
    (
        "boolean entry admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a rational entry was required", role=role)',
        'if type(value) is bool:\n        return Fraction(1)\n    if False:\n        raise _fail("boolean refused where a rational entry was required", role=role)',
    ),
    (
        "Gaussian entry admitted",
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; characteristic polynomial in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; characteristic polynomial in this module is over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "LeVerrier sign flipped",
        "coeff = -_trace(current) / Fraction(step)",
        "coeff = _trace(current) / Fraction(step)",
    ),
    (
        "constant term check inverted",
        "if coeffs[-1] != expected:",
        "if coeffs[-1] == expected:",
    ),
    (
        "Cayley-Hamilton check inverted",
        "if defect != 0:",
        "if defect == 0:",
    ),
    (
        "polynomial term dropped",
        "total = _add_term(total, power, coeff)",
        "total = power",
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
    certify = namespace["certify_characteristic_polynomial"]
    matrix = namespace["ExactMatrix"]
    if not _all_hold((callable(certify), isinstance(matrix, type),)):
        return False
    try:
        pair = certify(_pair())
        diagonal = certify(_diagonal())
        scalar = certify(matrix.from_rows([[Fraction(5)]]))
        empty = certify(matrix(0, 0, []))
    except error:
        return False
    return _all_hold((
pair == (Fraction(1), Fraction(-5), Fraction(-2)),
diagonal == (Fraction(1), Fraction(-9), Fraction(26), Fraction(-24)),
scalar == (Fraction(1), Fraction(-5)),
empty == (Fraction(1),),
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    certify = namespace["certify_characteristic_polynomial"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(certify), isinstance(matrix, type), callable(gaussian),)):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    shaped = build([[Fraction(1)]])
    shaped.rows = True
    probes = (
        (lambda: certify(build([[_probe("1.5")]])), "float refused at the public boundary"),
        (lambda: certify(build([[True]])), "boolean refused where a rational entry was required"),
        (lambda: certify(build([[gaussian(0, 1)]])), "Gaussian rational refused; characteristic polynomial in this module is over Q"),
        (lambda: certify(shaped), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["CharacteristicError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_char_poly_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_char_poly_{index}"
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
