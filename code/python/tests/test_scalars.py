"""Unit, negative, integration, end-to-end, and mutation tests for Q(i)."""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from src.linear_algebra.matrix import ExactMatrix
from src.linear_algebra.scalars import (
    GaussianRational,
    ScalarDivisionByZero,
    ScalarError,
    q,
)

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "scalars.py"


def test_ring_law_and_norm() -> None:
    value = GaussianRational(1, 1) * GaussianRational(1, 1)
    assert value == GaussianRational(0, 2)
    assert GaussianRational(3, 4).norm_sq() == Fraction(25)
    assert GaussianRational(3, 4).conjugate() == GaussianRational(3, -4)
    assert GaussianRational(1, 0) == 1
    assert GaussianRational(1, 0) != True
    assert q(1, 2) == Fraction(1, 2)


def test_negative_boundary_failures() -> None:
    with pytest.raises(ScalarError, match="float refused") as floated:
        GaussianRational(1.0, 0)
    assert floated.value.parameters["role"] == "real"
    assert type(floated.value) is ScalarError

    with pytest.raises(ScalarError, match="boolean refused") as boolean:
        GaussianRational(1, True)
    assert boolean.value.parameters["role"] == "imag"

    with pytest.raises(ScalarError, match="not an exact rational") as text:
        q("1", 2)
    assert text.value.parameters["received"] == "str"

    with pytest.raises(ScalarDivisionByZero, match="rational denominator") as denom:
        q(1, 0)
    assert isinstance(denom.value, ZeroDivisionError)
    assert denom.value.parameters["numerator"] == "1"

    with pytest.raises(ScalarDivisionByZero, match="rational field") as rational:
        GaussianRational(1, 2) / 0
    assert rational.value.parameters["divisor"] == "0"

    with pytest.raises(ScalarDivisionByZero, match="Gaussian rational field") as zero:
        GaussianRational(1, 1) / GaussianRational.zero()
    assert zero.value.parameters["norm_sq"] == "0"

    with pytest.raises(ScalarError, match="float refused") as added:
        GaussianRational(1, 0) + 0.5
    assert added.value.parameters["role"] == "addend"


def test_integration_with_matrix_neighbor() -> None:
    """The neighboring exact matrix builds its Gaussian identity from this field."""
    identity = ExactMatrix.identity(1, is_gaussian=True)
    assert identity.get(0, 0) == GaussianRational.one()
    assert (GaussianRational(3, 4) / GaussianRational(3, 4)) == GaussianRational.one()


def test_end_to_end_public_contract() -> None:
    value = q(3, 5) + q(4, 5) * GaussianRational.i()
    assert value.norm_sq() == 1
    assert value.sha256() == hashlib_of(value)
    with pytest.raises(ScalarError, match="float refused") as caught:
        GaussianRational.i() * 1.5
    assert caught.value.parameters["role"] == "factor"


def hashlib_of(value: GaussianRational) -> str:
    import hashlib

    return hashlib.sha256(value.canonical_bytes()).hexdigest()


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "DerivationDagQMClosure.lean").read_text(encoding="utf-8")
    assert "theorem ds_qm062_u1_selector_layers_and_ring_iso" in lean
    assert "a1 a2 - b1 b2" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:scalar:gaussian-rational-field:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return Fraction(value)\n    if False:",
    ),
    (
        "boolean admitted as an integer",
        "if isinstance(value, bool):",
        "if isinstance(value, bool):\n        return Fraction(int(value))\n    if False:",
    ),
    (
        "product imag sign flipped",
        "self.real * other.real - self.imag * other.imag",
        "self.real * other.real + self.imag * other.imag",
    ),
    ("conjugate sign dropped", "return GaussianRational(self.real, -self.imag)", "return GaussianRational(self.real, self.imag)"),
    ("gaussian zero divisor accepted", "if denom == 0:", "if denom < 0:"),
    ("addition imag subtracted", "self.imag + partner.imag", "self.imag - partner.imag"),
    ("norm difference", "self.real * self.real + self.imag * self.imag", "self.real * self.real - self.imag * self.imag"),
    ("zero rational denominator accepted", "if denominator_value == 0:", "if denominator_value != 0:"),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
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
    gaussian = namespace["GaussianRational"]
    ratio = namespace["q"]
    if not isinstance(gaussian, type) or not callable(ratio):
        return False
    try:
        square = gaussian(1, 1) * gaussian(1, 1)
        added = gaussian(1, 1) + gaussian(1, 1)
        norm = gaussian(3, 4).norm_sq()
        conjugate = gaussian(3, 4).conjugate()
        half = ratio(1, 2)
    except error:
        return False
    if square != gaussian(0, 2) or added != gaussian(2, 2):
        return False
    if norm != Fraction(25):
        return False
    if conjugate != gaussian(3, -4):
        return False
    if half != Fraction(1, 2):
        return False
    return True


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    gaussian = namespace["GaussianRational"]
    ratio = namespace["q"]
    if not isinstance(gaussian, type) or not callable(ratio):
        return False
    expected = (
        (lambda: gaussian(1.0, 0), "float refused at the public boundary"),
        (lambda: gaussian(True, 0), "boolean refused where a rational was required"),
        (lambda: gaussian(1, 1) / gaussian(0, 0), "division by zero in the Gaussian rational field"),
        (lambda: ratio(1, 0), "rational denominator is zero"),
    )
    for probe, invariant in expected:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["ScalarError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_scalar_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_scalar_{index}"
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
