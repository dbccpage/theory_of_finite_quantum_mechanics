"""Unit, negative, integration, end-to-end, and mutation tests for the boost eigenpair residual."""

from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

import pytest

from src.qm.finite_witness import FiniteWitnessError, eigenpair_residual, main, pair_residual

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "finite_witness.py"
_NEIGHBOR = Path(__file__).resolve().parents[1] / "src" / "qm" / "campaigns" / "spectral_claims.py"
_MATRIX = ((5, 3), (3, 5))


def test_boost_numerator_eigenpairs_have_zero_residual() -> None:
    assert pair_residual(_MATRIX, (1, 1), 8) == Fraction(0)
    assert pair_residual(_MATRIX, (1, -1), 2) == Fraction(0)
    assert pair_residual(_MATRIX, (1, -1), 0) == Fraction(4)
    assert pair_residual(_MATRIX, (1, 0), 0) == Fraction(8)
    assert eigenpair_residual() == Fraction(0)
    assert type(pair_residual(_MATRIX, (1, 1), 8)) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(FiniteWitnessError, match="float refused") as floated:
        pair_residual(_MATRIX, (1.0, 1), 8)
    assert floated.value.invariant == "float refused at the eigenpair boundary"
    assert floated.value.parameters["role"] == "vector"
    assert type(floated.value) is FiniteWitnessError

    with pytest.raises(FiniteWitnessError, match="boolean refused") as boolean:
        pair_residual(_MATRIX, (True, 1), 8)
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(FiniteWitnessError, match="float refused") as scale:
        pair_residual(_MATRIX, (1, 1), 8.0)
    assert scale.value.parameters["role"] == "eigenvalue"

    with pytest.raises(FiniteWitnessError, match="not an exact rational") as text:
        pair_residual(_MATRIX, ("1", 1), 8)
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(FiniteWitnessError, match="wrong length") as short:
        pair_residual(_MATRIX, (1,), 8)
    assert short.value.parameters["role"] == "vector"
    assert short.value.parameters["length"] == 1

    with pytest.raises(FiniteWitnessError, match="wrong length") as row:
        pair_residual(((5,), (3, 5)), (1, 1), 8)
    assert row.value.parameters["role"] == "row"

    with pytest.raises(FiniteWitnessError, match="not a tuple") as listed:
        pair_residual([(5, 3), (3, 5)], (1, 1), 8)
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(FiniteWitnessError, match="not a tuple"):
        pair_residual("53", (1, 1), 8)


def _characteristic_value() -> object:
    spec = importlib.util.spec_from_file_location("spectral_claims_neighbor", _NEIGHBOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the characteristic neighbor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.characteristic_value


def test_integration_matches_characteristic_roots() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "LorentzBoost.lean").read_text(encoding="utf-8")
    assert "theorem boost_eigenvalue_1" in source
    assert "theorem boost_eigenvalue_2" in source
    assert "theorem boost_hyperbolic_identity" in source
    assert 5 * 5 - 3 * 3 == 16
    characteristic = _characteristic_value()
    assert callable(characteristic)
    assert characteristic(_MATRIX, Fraction(8)) == 0
    assert characteristic(_MATRIX, Fraction(2)) == 0
    assert pair_residual(_MATRIX, (1, 1), 8) == 0


def test_end_to_end_cli_prints_zero() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "0"
    assert eigenpair_residual() == Fraction(0)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "LorentzBoost.lean").read_text(encoding="utf-8")
    assert "theorem boost_eigenvalue_1" in source
    assert "theorem boost_eigenvalue_2" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:witness:boost-eigenpair-residual:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float entry admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return Fraction(0)\n    if False:",
    ),
    (
        "boolean entry admitted",
        "if type(value) is bool:",
        "if type(value) is bool:\n        return Fraction(1)\n    if False:",
    ),
    ("length check dropped", "len(values) != length", "len(values) != -1"),
    ("tuple check inverted", "not isinstance(value, tuple)", "isinstance(value, tuple)"),
    ("second image term dropped", "row[1] * vector[1]", "Fraction(0)"),
    ("eigenvalue scale dropped", "return eigenvalue * component", "return component"),
    ("absolute value dropped", "if value < 0:", "if value != value:"),
    ("zero residual check inverted", "if total != 0:", "if total == 0:"),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.qm"
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
    residual = namespace["pair_residual"]
    certified = namespace["eigenpair_residual"]
    if not callable(residual) or not callable(certified):
        return False
    try:
        left = residual(_MATRIX, (1, 1), 8)
        right = residual(_MATRIX, (1, -1), 2)
        shifted = residual(_MATRIX, (1, -1), 0)
        axis = residual(_MATRIX, (1, 0), 0)
        total = certified()
    except error:
        return False
    actual = (left, right, shifted, axis, total)
    expected = (Fraction(0), Fraction(0), Fraction(4), Fraction(8), Fraction(0))
    return actual == expected


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    residual = namespace["pair_residual"]
    if not callable(residual):
        return False
    probes = (
        (lambda: residual(_MATRIX, (1.0, 1), 8), "float refused at the eigenpair boundary"),
        (lambda: residual(_MATRIX, (True, 1), 8), "boolean refused where a rational entry was required"),
        (lambda: residual(_MATRIX, ("1", 1), 8), "eigenpair entry is not an exact rational"),
        (lambda: residual(_MATRIX, (1,), 8), "eigenpair value has the wrong length"),
        (lambda: residual([(5, 3), (3, 5)], (1, 1), 8), "eigenpair value is not a tuple"),
        (lambda: residual(_MATRIX, (1, 1), 8.0), "float refused at the eigenpair boundary"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["FiniteWitnessError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_finite_witness_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_finite_witness_{index}"
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
