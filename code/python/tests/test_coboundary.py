"""Unit, negative, integration, end-to-end, and mutation tests for the triangle coboundary."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from src.homology.boundary import triangle_boundaries
from src.homology.coboundary import (
    CoboundaryOperator,
    require_coboundary_square,
    triangle_coboundaries,
    triangle_coboundary_defect,
)
from src.homology.cochain import coboundary_square, coboundary_values
from src.homology.errors import DimensionMismatchError, NonZeroCompositionError, require_composition_zero
from src.linear_algebra import ExactMatrix

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "coboundary.py"
_COLUMN = (Fraction(-1), Fraction(-1), Fraction(0))
_SQUARE = (Fraction(0),)


def test_triangle_coboundary_square_is_zero() -> None:
    edge, _face = triangle_boundaries()
    delta0, delta1 = triangle_coboundaries()
    assert triangle_coboundary_defect() == Fraction(0)
    assert (delta1.rows, delta1.cols) == (1, 3)
    assert tuple(delta0.data) == tuple(edge.transpose().data)
    assert CoboundaryOperator(edge).apply((1, 0, 0)) == _COLUMN


def test_negative_coboundary_failures() -> None:
    edge, _face = triangle_boundaries()
    _delta0, delta1 = triangle_coboundaries()
    operator = CoboundaryOperator(edge)

    with pytest.raises(DimensionMismatchError, match="float refused") as floated:
        operator.apply((1.0, 0, 0))
    assert floated.value.parameters["role"] == "cochain[0]"

    with pytest.raises(DimensionMismatchError, match="boolean refused") as boolean:
        operator.apply(cast(tuple[object, ...], (True, 0, 0)))
    assert boolean.value.parameters["role"] == "cochain[0]"

    with pytest.raises(DimensionMismatchError, match="must be a sequence") as raw:
        operator.apply("123")
    assert raw.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="does not match") as length:
        operator.apply((1, 0))
    assert length.value.parameters["length"] == 2

    with pytest.raises(DimensionMismatchError, match="exact matrix") as bare:
        CoboundaryOperator(cast(object, (1, 0, 0)))
    assert bare.value.parameters["received"] == "tuple"

    opened_row = ExactMatrix.from_rows([[Fraction(1), Fraction(0), Fraction(0)]])
    with pytest.raises(NonZeroCompositionError, match="not zero") as opened:
        require_coboundary_square(opened_row, _delta0_from(edge))
    assert opened.value.parameters["defect"] == "2"

    with pytest.raises(DimensionMismatchError, match="do not compose") as swapped:
        require_coboundary_square(edge, delta1)
    assert swapped.value.parameters["left"] == 3


def _delta0_from(edge: ExactMatrix) -> ExactMatrix:
    return CoboundaryOperator(edge).matrix


def test_integration_with_composition_certificate() -> None:
    delta0, delta1 = triangle_coboundaries()
    left_rows = [delta1.row(index) for index in range(delta1.rows)]
    right_rows = [delta0.row(index) for index in range(delta0.rows)]
    assert require_composition_zero(left_rows, right_rows) == triangle_coboundary_defect()
    assert coboundary_square((1, 0, 0)) == [Fraction(0)]
    assert coboundary_values((1, 0, 0)) == [Fraction(-1), Fraction(-1), Fraction(0)]


def test_end_to_end_public_contract() -> None:
    edge, face = triangle_boundaries()
    delta0, delta1 = triangle_coboundaries()
    assert require_coboundary_square(delta1, delta0) == Fraction(0)
    image = CoboundaryOperator(edge).apply((1, 0, 0))
    assert CoboundaryOperator(face).apply(image) == _SQUARE


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "FiniteCochain.lean").read_text(encoding="utf-8")
    assert "theorem d1_d0_zero" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:triangle-coboundary-square:v1" in source
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
    ("length check inverted", "if len(parsed) != matrix.cols:", "if len(parsed) == matrix.cols:"),
    ("square check inverted", "if defect != 0:", "if defect == 0:"),
    ("transpose dropped", ".transpose()", ""),
    ("composition check inverted", "if left.cols != right.rows:", "if left.cols == right.rows:"),
    ("string accepted as a cochain", "isinstance(values, (str, bytes)) or ", ""),
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
    defect_of = namespace["triangle_coboundary_defect"]
    coboundaries = namespace["triangle_coboundaries"]
    boundaries = namespace["triangle_boundaries"]
    operator = namespace["CoboundaryOperator"]
    if not callable(defect_of) or not callable(coboundaries) or not callable(boundaries):
        return False
    if not isinstance(operator, type):
        return False
    try:
        defect = defect_of()
        _delta0, delta1 = coboundaries()
        edge, _face = boundaries()
        column = operator(edge).apply((1, 0, 0))
    except error:
        return False
    if defect != 0 or delta1.rows != 1 or delta1.cols != 3:
        return False
    matches = column == _COLUMN
    if matches is True:
        return True
    return False


def _bad_values_refused(namespace: dict[str, object]) -> bool:
    mismatch = namespace["DimensionMismatchError"]
    nonzero = namespace["NonZeroCompositionError"]
    operator_type = namespace["CoboundaryOperator"]
    coboundaries = namespace["triangle_coboundaries"]
    require = namespace["require_coboundary_square"]
    matrix_type = namespace["ExactMatrix"]
    if not isinstance(mismatch, type) or not isinstance(nonzero, type) or not isinstance(operator_type, type):
        return False
    factory = getattr(matrix_type, "from_rows", None)
    if not isinstance(matrix_type, type) or not callable(factory) or not callable(coboundaries) or not callable(require):
        return False
    delta0, delta1 = coboundaries()
    operator = operator_type(delta0)
    opened_row = factory([[Fraction(1), Fraction(0), Fraction(0)]])
    expected = (
        (mismatch, lambda: operator.apply((1.0, 0, 0)), "float refused at the public boundary"),
        (mismatch, lambda: operator.apply((True, 0, 0)), "boolean refused where a rational was required"),
        (mismatch, lambda: operator.apply("123"), "coboundary cochain must be a sequence"),
        (mismatch, lambda: operator.apply((1, 0)), "coboundary cochain length does not match the operator"),
        (nonzero, lambda: require(opened_row, delta0), "triangle coboundary square is not zero"),
        (mismatch, lambda: require(delta0, delta1), "coboundary factors do not compose"),
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
        loaded.append("mutant_coboundary_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_coboundary_{index}"
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
