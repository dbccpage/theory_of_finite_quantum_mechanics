"""Unit, negative, integration, end-to-end, and mutation tests for rational involutions.

Origin: code/python/src/linear_algebra/involution.py
Claim: urn:omega:fqm:involution:householder-and-conjugation:v1
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

from src.linear_algebra.involution import (
    InvolutionError,
    certify_conjugation,
    certify_householder,
    conjugation_square,
    householder,
    require_involution,
)
from src.linear_algebra.matrix import ExactMatrix
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "involution.py"


def test_householder_squares_to_identity() -> None:
    certificate = certify_householder([0, 1])
    assert certificate.norm_sq == Fraction(1)
    assert certificate.matrix == ExactMatrix.from_rows(
        [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(-1)]]
    )
    assert householder([3, 4]) * householder([3, 4]) == ExactMatrix.identity(2)


def test_conjugation_restores_value() -> None:
    certificate = certify_conjugation(3, 4)
    assert certificate.conjugate == GaussianRational(3, -4)
    assert certificate.twice == certificate.value
    assert conjugation_square(3, 4) == GaussianRational(3, 4)


def test_negative_boundary_failures() -> None:
    with pytest.raises(InvolutionError, match="float refused") as floated:
        householder([_probe("1.0"), 0])
    assert floated.value.parameters["role"] == "vector[0]"

    with pytest.raises(InvolutionError, match="boolean refused") as boolean:
        householder([True])
    assert boolean.value.invariant == "boolean refused where a rational was required"

    with pytest.raises(InvolutionError, match="outside the Householder") as gaussian:
        householder([GaussianRational(3, 4)])
    assert gaussian.value.invariant == "Q(i) is outside the Householder carrier"

    with pytest.raises(InvolutionError, match="not an exact rational") as text:
        householder(["1"])
    assert text.value.parameters["received"] == "str"

    with pytest.raises(InvolutionError, match="nonempty sequence") as empty:
        householder([])
    assert empty.value.parameters["received"] == "list"

    with pytest.raises(InvolutionError, match="must be nonzero") as zero:
        householder([0, 0])
    assert zero.value.parameters["norm_sq"] == "0"

    with pytest.raises(InvolutionError, match="must be square") as shape:
        require_involution(ExactMatrix(1, 2, [Fraction(1), Fraction(0)]))
    assert shape.value.parameters["cols"] == 2

    with pytest.raises(InvolutionError, match="not an involution") as shear:
        require_involution(ExactMatrix.from_rows([[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]]))
    assert shear.value.parameters["rows"] == 2

    with pytest.raises(InvolutionError, match="float refused") as conj:
        conjugation_square(_probe("1.0"), 0)
    assert conj.value.parameters["role"] == "real"


def test_integration_with_matrix_neighbor() -> None:
    """diag(1, -1) from the neighboring matrix module is the Householder of (0, 1)."""
    selector = ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(-1)]])
    assert householder([0, 1]) == selector
    assert selector * selector == ExactMatrix.identity(2)
    assert conjugation_square(Fraction(1, 2), Fraction(-3, 2)).imag == Fraction(-3, 2)


def test_end_to_end_public_contract() -> None:
    reflected = householder([Fraction(1), Fraction(0)])
    assert reflected * reflected == ExactMatrix.identity(2)
    with pytest.raises(InvolutionError, match="float refused") as caught:
        conjugation_square(0, _probe("1.5"))
    assert caught.value.parameters["role"] == "imag"


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "DerivationDagQMClosure.lean").read_text(encoding="utf-8")
    assert "theorem ds_qm062_u1_selector_layers_and_ring_iso" in lean
    assert "Mat2Int.mul S S = I2" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:involution:householder-and-conjugation:v1" in source
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
        "gaussian real part admitted",
        "if isinstance(value, GaussianRational):",
        "if isinstance(value, GaussianRational):\n        return value.real\n    if False:",
    ),
    ("zero vector accepted", "if norm_sq == 0:", "if norm_sq < 0:"),
    ("reflection scale changed", "Fraction(2) * coords[row]", "Fraction(3) * coords[row]"),
    ("involution check inverted", "if matrix * matrix != identity:", "if matrix * matrix == identity:"),
    ("empty vector accepted", "or len(values) == 0:", "or len(values) < 0:"),
    ("conjugation skipped", "once = value.conjugate()", "once = value"),
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
    certify = namespace["certify_householder"]
    conjure = namespace["certify_conjugation"]
    if not _all_hold((callable(certify), callable(conjure),)):
        return False
    try:
        certificate = certify([0, 1])
        conjugation = conjure(3, 4)
    except error:
        return False
    matrix = getattr(certificate, "matrix", None)
    if not isinstance(matrix, ExactMatrix):
        return False
    selector = ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(-1)]])
    if matrix != selector or matrix * matrix != ExactMatrix.identity(2):
        return False
    conjugate = getattr(conjugation, "conjugate", None)
    if not isinstance(conjugate, GaussianRational) or conjugate.imag != Fraction(-4):
        return False
    return getattr(conjugation, "twice", None) == getattr(conjugation, "value", None)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    reflect = namespace["householder"]
    conjure = namespace["conjugation_square"]
    if not _all_hold((callable(reflect), callable(conjure),)):
        return False
    gaussian = namespace["GaussianRational"]
    if not isinstance(gaussian, type):
        return False
    expected = (
        (lambda: reflect([_probe("1.0"), 0]), "float refused at the public boundary"),
        (lambda: reflect([True]), "boolean refused where a rational was required"),
        (lambda: reflect([gaussian(3, 4)]), "Q(i) is outside the Householder carrier"),
        (lambda: reflect([0, 0]), "Householder vector must be nonzero"),
        (lambda: reflect([]), "Householder vector must be a nonempty sequence"),
        (lambda: conjure(_probe("1.0"), 0), "float refused at the public boundary"),
    )
    for probe, invariant in expected:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["InvolutionError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_involution_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_involution_{index}"
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
