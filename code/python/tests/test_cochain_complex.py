"""Unit, negative, integration, end-to-end, and mutation tests for cochain complexes."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from src.homology.coboundary import require_coboundary_square, triangle_coboundaries
from src.homology.cochain_complex import CochainComplex, triangle_cochain_complex
from src.homology.errors import DimensionMismatchError, NonZeroCompositionError
from src.linear_algebra import ExactMatrix

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "cochain_complex.py"


def test_triangle_complex_is_nilpotent() -> None:
    delta0, delta1 = triangle_coboundaries()
    complex_ = triangle_cochain_complex()
    assert len(complex_.coboundaries) == 2
    assert list(complex_.coboundaries[0].data) == list(delta0.data)
    assert list(complex_.coboundaries[1].data) == list(delta1.data)
    assert len(CochainComplex((delta0,)).coboundaries) == 1


def test_negative_complex_failures() -> None:
    delta0, _delta1 = triangle_coboundaries()
    floated = ExactMatrix.from_rows([[1.0]])
    with pytest.raises(DimensionMismatchError, match="float refused") as float_error:
        CochainComplex((floated,))
    assert float_error.value.parameters["role"] == "matrix[0][0]"

    boolean = ExactMatrix.from_rows([[True]])
    with pytest.raises(DimensionMismatchError, match="boolean refused") as bool_error:
        CochainComplex((boolean,))
    assert bool_error.value.parameters["role"] == "matrix[0][0]"

    with pytest.raises(DimensionMismatchError, match="nonempty sequence") as raw:
        CochainComplex("ab")
    assert raw.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="nonempty sequence") as empty:
        CochainComplex(())
    assert empty.value.parameters["received"] == "tuple"

    with pytest.raises(DimensionMismatchError, match="exact matrices") as bare:
        CochainComplex((cast(object, (1, 0)),))
    assert bare.value.parameters["received"] == "tuple"

    opened_face = ExactMatrix.from_rows([[Fraction(1), Fraction(1), Fraction(1)]])
    with pytest.raises(NonZeroCompositionError, match="do not compose to zero") as opened:
        CochainComplex((delta0, opened_face))
    assert opened.value.parameters["defect"] == "4"

    thin = ExactMatrix.from_rows([[Fraction(1), Fraction(0)]])
    with pytest.raises(DimensionMismatchError, match="do not compose") as swapped:
        CochainComplex((delta0, thin))
    assert swapped.value.parameters["left"] == 2
    assert swapped.value.parameters["right"] == 3


def test_integration_with_coboundary_square() -> None:
    delta0, delta1 = triangle_coboundaries()
    assert require_coboundary_square(delta1, delta0) == Fraction(0)
    assert len(triangle_cochain_complex().coboundaries) == 2


def test_end_to_end_public_contract() -> None:
    complex_ = triangle_cochain_complex()
    rebuilt = CochainComplex(complex_.coboundaries)
    assert rebuilt.coboundaries[1].row(0) == [Fraction(1), Fraction(-1), Fraction(1)]
    with pytest.raises(DimensionMismatchError, match="float refused"):
        CochainComplex((ExactMatrix.from_rows([[0.5]]),))


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "ContextualityObstruction.lean").read_text(encoding="utf-8")
    assert "differential_squares_to_zero" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:cochain-complex-square:v1" in source
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
    ("square check inverted", "if defect != 0:", "if defect == 0:"),
    ("composition check inverted", "if later.cols != earlier.rows:", "if later.cols == earlier.rows:"),
    ("string accepted as a complex", "isinstance(coboundaries, (str, bytes)) or ", ""),
    ("empty complex accepted", "or len(coboundaries) == 0", "or len(coboundaries) < 0"),
    ("last consecutive pair skipped", "range(len(matrices) - 1)", "range(len(matrices) - 2)"),
    (
        "defect shifted by one",
        'defect += abs(_rational(entry, f"product[{index}]"))',
        'defect += abs(_rational(entry, f"product[{index}]")) + 1',
    ),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.homology"
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
    complex_type = namespace["CochainComplex"]
    triangle = namespace["triangle_cochain_complex"]
    coboundaries = namespace["triangle_coboundaries"]
    if not isinstance(complex_type, type) or not callable(triangle) or not callable(coboundaries):
        return False
    try:
        delta0, _delta1 = coboundaries()
        built = triangle()
        single = complex_type((delta0,))
    except error:
        return False
    if len(built.coboundaries) != 2 or len(single.coboundaries) != 1:
        return False
    return True


def _bad_values_refused(namespace: dict[str, object]) -> bool:
    mismatch = namespace["DimensionMismatchError"]
    nonzero = namespace["NonZeroCompositionError"]
    complex_type = namespace["CochainComplex"]
    coboundaries = namespace["triangle_coboundaries"]
    matrix_type = namespace["ExactMatrix"]
    if not isinstance(mismatch, type) or not isinstance(nonzero, type) or not isinstance(complex_type, type):
        return False
    factory = getattr(matrix_type, "from_rows", None)
    if not isinstance(matrix_type, type) or not callable(factory) or not callable(coboundaries):
        return False
    delta0, _delta1 = coboundaries()
    opened_face = factory([[Fraction(1), Fraction(1), Fraction(1)]])
    thin = factory([[Fraction(1), Fraction(0)]])
    floated = factory([[1.0]])
    boolean = factory([[True]])
    expected = (
        (mismatch, lambda: complex_type((floated,)), "float refused at the public boundary"),
        (mismatch, lambda: complex_type((boolean,)), "boolean refused where a rational was required"),
        (mismatch, lambda: complex_type("ab"), "cochain complex requires a nonempty sequence"),
        (mismatch, lambda: complex_type(()), "cochain complex requires a nonempty sequence"),
        (nonzero, lambda: complex_type((delta0, opened_face)), "consecutive coboundaries do not compose to zero"),
        (mismatch, lambda: complex_type((delta0, thin)), "coboundary factors do not compose"),
    )
    for error, probe, invariant in expected:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["DimensionMismatchError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_cochain_complex_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_cochain_complex_{index}"
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
