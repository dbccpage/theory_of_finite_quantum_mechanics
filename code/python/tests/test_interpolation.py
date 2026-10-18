"""Unit, negative, integration, end-to-end, and mutation tests for Newton–Neville interpolation."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.interpolation import (
    ExactMatrix,
    InterpolationError,
    _solve_vandermonde,
    certify_interpolant,
    divided_differences,
    interpolation_node_defect,
    neville_eval,
    newton_eval,
    vandermonde_solution,
)
from src.linear_algebra.scalars import GaussianRational

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "interpolation.py"

_NODES = [Fraction(0), Fraction(1), Fraction(2)]
_VALUES = [Fraction(0), Fraction(1), Fraction(4)]


def test_square_polynomial_has_the_hand_coefficients() -> None:
    assert divided_differences(_NODES, _VALUES) == [Fraction(0), Fraction(1), Fraction(1)]
    assert newton_eval(_NODES, [Fraction(0), Fraction(1), Fraction(1)], Fraction(1, 2)) == Fraction(1, 4)
    assert neville_eval(_NODES, _VALUES, Fraction(1, 2)) == Fraction(1, 4)
    assert interpolation_node_defect(_NODES, _VALUES) == 0
    column = vandermonde_solution(_NODES, _VALUES)
    assert column == ExactMatrix.from_rows([[Fraction(0)], [Fraction(0)], [Fraction(1)]])
    assert certify_interpolant([Fraction(5)], [Fraction(9)]) == (Fraction(9),)
    assert type(divided_differences(_NODES, _VALUES)[1]) is Fraction


def test_negative_boundary_failures() -> None:
    with pytest.raises(InterpolationError, match="float refused") as floated:
        divided_differences([1.5], [Fraction(0)])
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "abscissa[0]"
    assert type(floated.value) is InterpolationError

    with pytest.raises(InterpolationError, match="boolean refused") as boolean:
        divided_differences([True], [Fraction(0)])
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(InterpolationError, match="Gaussian rational refused") as gaussian:
        divided_differences([GaussianRational(0, 1)], [Fraction(0)])
    assert gaussian.value.parameters["role"] == "abscissa[0]"

    with pytest.raises(InterpolationError, match="not an exact rational") as text:
        divided_differences(["1"], [Fraction(0)])
    assert text.value.parameters["received"] == "str"

    with pytest.raises(InterpolationError, match="does not match the ordinates") as counted:
        divided_differences([Fraction(0), Fraction(1)], [Fraction(0)])
    assert counted.value.parameters["left"] == 2
    assert counted.value.parameters["right"] == 1

    with pytest.raises(InterpolationError, match="at least one node") as empty:
        divided_differences([], [])
    assert empty.value.parameters["count"] == 0

    with pytest.raises(InterpolationError, match="must be distinct") as repeated:
        divided_differences([Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)])
    assert repeated.value.parameters["order"] == 1

    with pytest.raises(InterpolationError, match="coefficient count") as coeffs:
        newton_eval(_NODES, [Fraction(0)], Fraction(0))
    assert coeffs.value.parameters["right"] == 1

    with pytest.raises(InterpolationError, match="float refused") as coeff_float:
        newton_eval([Fraction(0)], [1.5], Fraction(0))
    assert coeff_float.value.parameters["role"] == "coeff[0]"

    with pytest.raises(InterpolationError, match="singular") as singular:
        _solve_vandermonde(
            [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)]],
            [Fraction(0), Fraction(0)],
        )
    assert singular.value.parameters["nodes"] == 2


def test_integration_matches_the_cited_neville_recurrence() -> None:
    root = Path(__file__).resolve().parents[3]
    rust = (root / "code" / "rust" / "src" / "linear_algebra" / "interpolation.rs").read_text(encoding="utf-8")
    assert "For distinct nodes, the recurrence evaluates the unique interpolating" in rust
    assert "Neither calculation supplies a function remainder" in rust
    coeffs = divided_differences(_NODES, _VALUES)
    column = vandermonde_solution(_NODES, _VALUES)
    probe = Fraction(1, 2)
    monomial = Fraction(column.get(0, 0)) + Fraction(column.get(1, 0)) * probe + Fraction(column.get(2, 0)) * probe * probe
    assert coeffs == [Fraction(0), Fraction(1), Fraction(1)]
    assert monomial == Fraction(1, 4)
    assert newton_eval(_NODES, coeffs, probe) == monomial
    assert neville_eval(_NODES, _VALUES, probe) == monomial
    assert interpolation_node_defect(_NODES, _VALUES) == 0


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.interpolation
    assert package.certify_interpolant(_NODES, _VALUES) == (Fraction(0), Fraction(1), Fraction(1))
    assert package.neville_eval([Fraction(2)], [Fraction(7)], Fraction(9)) == 7
    assert package.newton_eval([Fraction(2)], [Fraction(7)], Fraction(9)) == 7
    assert package.vandermonde_solution([Fraction(2)], [Fraction(7)]) == ExactMatrix.from_rows([[Fraction(7)]])
    with pytest.raises(InterpolationError, match="float refused"):
        package.certify_interpolant([0.25], [Fraction(1)])


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    rust = root / "code" / "rust" / "src" / "linear_algebra" / "interpolation.rs"
    assert rust.is_file()
    text = rust.read_text(encoding="utf-8")
    assert "unique interpolating" in text
    assert "function remainder" in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:newton-neville:v1" in source
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
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; interpolation in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; interpolation in this module is over Q", role=role)',
    ),
    (
        "distinct-node check inverted",
        'if span == 0:\n            raise _fail("abscissae must be distinct", index=index, order=order)',
        'if span != 0:\n            raise _fail("abscissae must be distinct", index=index, order=order)',
    ),
    (
        "divided difference reversed",
        "(table[index + 1] - table[index]) / span",
        "(table[index] - table[index + 1]) / span",
    ),
    (
        "Neville step sign flipped",
        "((abscissa - left) * column[index + 1] - (abscissa - right) * column[index]) / span",
        "((abscissa - left) * column[index + 1] + (abscissa - right) * column[index]) / span",
    ),
    (
        "Newton-Neville check inverted",
        "if newton != neville:",
        "if newton == neville:",
    ),
    (
        "Vandermonde power incremented",
        "power *= node",
        "power += node",
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
    certify = namespace["certify_interpolant"]
    column_of = namespace["vandermonde_solution"]
    neville = namespace["neville_eval"]
    matrix = namespace["ExactMatrix"]
    if not callable(certify) or not callable(column_of) or not callable(neville) or not isinstance(matrix, type):
        return False
    try:
        coeffs = certify(_NODES, _VALUES)
        column = column_of(_NODES, _VALUES)
        off_node = neville(_NODES, _VALUES, Fraction(1, 2))
        constant = certify([Fraction(5)], [Fraction(9)])
    except error:
        return False
    if not isinstance(column, matrix):
        return False
    return bool(
        coeffs == (Fraction(0), Fraction(1), Fraction(1))
        and off_node == Fraction(1, 4)
        and constant == (Fraction(9),)
        and list(column.data) == [Fraction(0), Fraction(0), Fraction(1)]
    )


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    differences = namespace["divided_differences"]
    gaussian = namespace["GaussianRational"]
    if not callable(differences) or not callable(gaussian):
        return False
    probes = (
        (lambda: differences([1.5], [Fraction(0)]), "float refused at the public boundary"),
        (lambda: differences([True], [Fraction(0)]), "boolean refused where a rational entry was required"),
        (
            lambda: differences([gaussian(0, 1)], [Fraction(0)]),
            "Gaussian rational refused; interpolation in this module is over Q",
        ),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["InterpolationError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_interpolation_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_interpolation_{index}"
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
