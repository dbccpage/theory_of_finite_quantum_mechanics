"""Unit, negative, integration, end-to-end, and mutation tests for the quadratic jet."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.second_jet import (
    ExactMatrix,
    JetError,
    _require_zero_defect,
    certify_taylor,
    quadratic_value,
    second_jet,
    taylor_defect,
)
from src.linear_algebra.scalars import GaussianRational

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "second_jet.py"


def test_jet_matches_the_hand_expansion() -> None:
    assert quadratic_value(1, 2) == 11
    value, gradient, hessian = second_jet(1, 2)
    assert value == 11
    assert gradient == (Fraction(12), Fraction(4))
    assert hessian == ExactMatrix.from_rows([[Fraction(2), Fraction(3)], [Fraction(3), Fraction(1)]])
    assert taylor_defect(1, 2, 1, 1) == 0
    assert certify_taylor(Fraction(1, 2), Fraction(-2), Fraction(3), Fraction(1, 3)) == 0
    assert type(value) is Fraction


def test_negative_boundary_failures() -> None:
    with pytest.raises(JetError, match="float refused") as floated:
        quadratic_value(1.5, 0)
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "x"
    assert type(floated.value) is JetError

    with pytest.raises(JetError, match="boolean refused") as boolean:
        quadratic_value(True, 0)
    assert boolean.value.invariant == "boolean refused where a rational coordinate was required"

    with pytest.raises(JetError, match="Gaussian rational refused") as gaussian:
        quadratic_value(GaussianRational(0, 1), 0)
    assert gaussian.value.parameters["role"] == "x"

    with pytest.raises(JetError, match="not an exact rational") as text:
        quadratic_value("1", 0)
    assert text.value.parameters["received"] == "str"

    with pytest.raises(JetError, match="float refused") as step:
        taylor_defect(0, 0, 0.5, 0)
    assert step.value.parameters["role"] == "step_x"

    with pytest.raises(JetError, match="Taylor defect") as defect:
        _require_zero_defect(Fraction(1))
    assert defect.value.parameters["defect"] == "1"


def test_integration_symmetric_difference_matches_the_gradient() -> None:
    root = Path(__file__).resolve().parents[3]
    note = (
        root
        / "papers"
        / "derivations"
        / "mub6"
        / "artifacts"
        / "knowledge"
        / "observation_quartic_overlap_secant_failure.md"
    ).read_text(encoding="utf-8")
    assert "holds strictly for systems of quadratic polynomials" in note
    assert "non-vanishing second-order Taylor remainder" in note
    assert quadratic_value(2, 2) == 24
    assert quadratic_value(0, 2) == 0
    partial_x = (quadratic_value(2, 2) - quadratic_value(0, 2)) / 2
    partial_y = (quadratic_value(1, 3) - quadratic_value(1, 1)) / 2
    value, gradient, hessian = second_jet(1, 2)
    assert value == 11
    assert partial_x == gradient[0]
    assert partial_y == gradient[1]
    assert partial_x == 12
    assert partial_y == 4
    step = ExactMatrix.from_rows([[Fraction(1)], [Fraction(1)]])
    form = (step.transpose() * hessian * step).get(0, 0)
    assert form == 9
    assert taylor_defect(1, 2, 1, 1) == 0


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.second_jet
    assert package.certify_taylor(1, 2, 1, 1) == 0
    assert package.quadratic_value(0, 0) == 0
    value, gradient, _hessian = package.second_jet(0, 0)
    assert value == 0
    assert gradient == (Fraction(4), Fraction(-1))
    tampered = 0.25
    with pytest.raises(JetError, match="float refused"):
        package.certify_taylor(tampered, 0, 0, 0)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    note = (
        root
        / "papers"
        / "derivations"
        / "mub6"
        / "artifacts"
        / "knowledge"
        / "observation_quartic_overlap_secant_failure.md"
    )
    assert note.is_file()
    assert "holds strictly for systems of quadratic polynomials" in note.read_text(encoding="utf-8")
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:second-jet:v1" in source
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
        'if type(value) is bool:\n        return Fraction(1)\n    if False:\n        raise _fail("boolean refused where a rational coordinate was required", role=role)',
    ),
    (
        "Gaussian coordinate admitted",
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; the second jet in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; the second jet in this module is over Q", role=role)',
    ),
    (
        "cross term coefficient changed",
        "3 * xx * yy",
        "4 * xx * yy",
    ),
    (
        "Hessian cross entry cleared",
        "[Fraction(2), Fraction(3)],\n            [Fraction(3), Fraction(1)],",
        "[Fraction(2), Fraction(0)],\n            [Fraction(3), Fraction(1)],",
    ),
    (
        "gradient constant flipped",
        "2 * x + 3 * y + 4",
        "2 * x + 3 * y - 4",
    ),
    (
        "quadratic half dropped",
        "quad_form / 2",
        "quad_form",
    ),
    (
        "linear y sign flipped",
        "4 * xx - yy",
        "4 * xx + yy",
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
    value_at = namespace["quadratic_value"]
    jet = namespace["second_jet"]
    certify = namespace["certify_taylor"]
    matrix = namespace["ExactMatrix"]
    if not callable(value_at) or not callable(jet) or not callable(certify) or not isinstance(matrix, type):
        return False
    try:
        value = value_at(1, 2)
        jet_value, gradient, hessian = jet(1, 2)
        defect = certify(1, 2, 1, 1)
    except error:
        return False
    if not isinstance(hessian, matrix):
        return False
    return bool(
        value == 11
        and jet_value == 11
        and gradient == (Fraction(12), Fraction(4))
        and hessian.get(0, 0) == 2
        and hessian.get(0, 1) == 3
        and hessian.get(1, 0) == 3
        and defect == 0
    )


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    value_at = namespace["quadratic_value"]
    gaussian = namespace["GaussianRational"]
    if not callable(value_at) or not callable(gaussian):
        return False
    probes = (
        (lambda: value_at(1.5, 0), "float refused at the public boundary"),
        (lambda: value_at(True, 0), "boolean refused where a rational coordinate was required"),
        (lambda: value_at(gaussian(0, 1), 0), "Gaussian rational refused; the second jet in this module is over Q"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["JetError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_second_jet_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_second_jet_{index}"
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
