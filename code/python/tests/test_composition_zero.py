"""Unit, negative, integration, end-to-end, and mutation tests for composition zero."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

from src.homology.boundary import triangle_boundary_defect
from src.homology.errors import (
    DimensionMismatchError,
    HomologyError,
    NonZeroCompositionError,
    require_composition_zero,
    triangle_composition_defect,
)

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "errors.py"

_EDGE = (
    (Fraction(-1), Fraction(-1), Fraction(0)),
    (Fraction(1), Fraction(0), Fraction(-1)),
    (Fraction(0), Fraction(1), Fraction(1)),
)
_FACE = ((Fraction(1),), (Fraction(-1),), (Fraction(1),))


def test_triangle_product_is_zero() -> None:
    assert triangle_composition_defect() == Fraction(0)
    assert require_composition_zero(_EDGE, _FACE) == Fraction(0)


def test_negative_value_failures() -> None:
    with pytest.raises(HomologyError, match="float refused") as caught:
        require_composition_zero([[1.0]], [[1]])
    assert type(caught.value) is HomologyError
    assert caught.value.parameters["role"] == "left[0][0]"

    with pytest.raises(HomologyError, match="boolean refused") as caught:
        require_composition_zero([[True]], [[1]])
    assert caught.value.invariant == "boolean refused where a rational was required"

    with pytest.raises(HomologyError, match="not an exact rational") as caught:
        require_composition_zero([["1"]], [[1]])
    assert caught.value.parameters["received"] == "str"


def test_negative_shape_and_defect_failures() -> None:
    with pytest.raises(DimensionMismatchError, match="nonempty") as empty:
        require_composition_zero([], [[1]])
    assert empty.value.parameters["role"] == "left"

    with pytest.raises(DimensionMismatchError, match="not a vector") as blank:
        require_composition_zero([[]], [[1]])
    assert blank.value.parameters["row"] == 0

    with pytest.raises(DimensionMismatchError, match="jagged") as jagged:
        require_composition_zero([[1, 0], [1]], [[1], [0]])
    assert jagged.value.parameters["expected"] == 2

    with pytest.raises(DimensionMismatchError, match="cannot compose widths") as widths:
        require_composition_zero([[1, 0]], [[1]])
    assert widths.value.parameters["left_columns"] == 2
    assert widths.value.parameters["right_rows"] == 1

    with pytest.raises(NonZeroCompositionError, match="defect is not zero") as defect:
        require_composition_zero([[1], [-1]], [[1, 0]])
    assert defect.value.parameters["defect"] == "2"


def test_integration_with_boundary_neighbor() -> None:
    """The neighbor's matrix defect and this certificate agree on the triangle."""
    assert triangle_composition_defect() == triangle_boundary_defect()
    assert triangle_boundary_defect() == Fraction(0)


def test_end_to_end_public_contract() -> None:
    assert require_composition_zero([[1, -1], [0, 0]], [[1], [1]]) == Fraction(0)
    with pytest.raises(HomologyError, match="float refused") as caught:
        require_composition_zero([[1]], [[0.5]])
    assert caught.value.parameters["role"] == "right[0][0]"


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "FiniteCochain.lean").read_text(encoding="utf-8")
    assert "theorem d1_d0_zero" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:cochain:composition-zero-certificate:v1" in source
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
    ("absolute defect dropped", "defect += abs(_dot_column(row, right, column))", "defect += _dot_column(row, right, column)"),
    ("right factor dropped", "total += entry * right[index][column]", "total += entry"),
    ("width check inverted", "if right_rows != left_columns:", "if right_rows == left_columns:"),
    ("empty matrix accepted", "or len(values) == 0:", "or len(values) < 0:"),
    ("jagged check inverted", "if width is not None and len(parsed) != width:", "if width is not None and len(parsed) == width:"),
    ("zero defect rejected", "if defect != 0:", "if defect == 0:"),
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


def _raises(error: type[BaseException], probe: object) -> bool:
    if not callable(probe):
        return False
    try:
        probe()
    except error:
        return True
    return False


def _callables_ready(namespace: dict[str, object]) -> bool:
    return callable(namespace["require_composition_zero"]) and callable(namespace["triangle_composition_defect"])


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    require = namespace["require_composition_zero"]
    triangle = namespace["triangle_composition_defect"]
    if not callable(require) or not callable(triangle):
        return False
    try:
        if triangle() != Fraction(0):
            return False
        if require([[1, -1], [0, 0]], [[1], [1]]) != Fraction(0):
            return False
    except error:
        return False
    return True


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    require = namespace["require_composition_zero"]
    if not callable(require):
        return False
    probes = (
        lambda: require([[1.0]], [[0]]),
        lambda: require([[True]], [[0]]),
        lambda: require([], [[1]]),
        lambda: require([[1, 0], [0]], [[0], [0]]),
        lambda: require([[1, 0]], [[1]]),
        lambda: require([[1], [-1]], [[1, 0]]),
    )
    for probe in probes:
        if not _raises(error, probe):
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["HomologyError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _callables_ready(namespace):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_compose_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_compose_{index}"
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
