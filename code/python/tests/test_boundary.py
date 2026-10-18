"""Unit, negative, integration, end-to-end, and mutation tests for the triangle boundary.

Origin: code/python/src/homology/boundary.py
Claim: urn:omega:fqm:homology:triangle-boundary-square:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""





from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from src.homology.boundary import (
    BoundaryOperator,
    require_boundary_square,
    triangle_boundaries,
    triangle_boundary_defect,
)
from src.homology.errors import DimensionMismatchError, NonZeroCompositionError, require_composition_zero
from src.linear_algebra import ExactMatrix

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "boundary.py"
_ZERO = (Fraction(0), Fraction(0), Fraction(0))
_CYCLE = (Fraction(1), Fraction(-1), Fraction(1))
_COLUMN = (Fraction(-1), Fraction(1), Fraction(0))


def test_triangle_boundary_square_is_zero() -> None:
    edge, face = triangle_boundaries()
    assert triangle_boundary_defect() == Fraction(0)
    assert tuple(face.col(0)) == _CYCLE
    assert BoundaryOperator(edge).apply((1, -1, 1)) == _ZERO
    assert BoundaryOperator(edge).apply((1, 0, 0)) == _COLUMN


def test_negative_boundary_failures() -> None:
    edge, _face = triangle_boundaries()
    operator = BoundaryOperator(edge)

    with pytest.raises(DimensionMismatchError, match="float refused") as floated:
        operator.apply((_probe("1.0"), 0, 0))
    assert floated.value.parameters["role"] == "chain[0]"

    with pytest.raises(DimensionMismatchError, match="boolean refused") as boolean:
        operator.apply(cast(tuple[object, ...], (True, 0, 0)))
    assert boolean.value.parameters["role"] == "chain[0]"

    with pytest.raises(DimensionMismatchError, match="must be a sequence") as raw:
        operator.apply("123")
    assert raw.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="does not match") as length:
        operator.apply((1, 0))
    assert length.value.parameters["length"] == 2

    with pytest.raises(DimensionMismatchError, match="exact matrix") as bare:
        BoundaryOperator(cast(object, (1, 0, 0)))
    assert bare.value.parameters["received"] == "tuple"

    bad_face = ExactMatrix.from_rows([[Fraction(1)], [Fraction(1)], [Fraction(1)]])
    with pytest.raises(NonZeroCompositionError, match="not zero") as opened:
        require_boundary_square(edge, bad_face)
    assert opened.value.parameters["defect"] == "4"

    with pytest.raises(DimensionMismatchError, match="do not compose") as swapped:
        require_boundary_square(bad_face, edge)
    assert swapped.value.parameters["left"] == 1


def test_integration_with_composition_certificate() -> None:
    edge, face = triangle_boundaries()
    edge_rows = [edge.row(index) for index in range(edge.rows)]
    face_rows = [face.row(index) for index in range(face.rows)]
    assert require_composition_zero(edge_rows, face_rows) == triangle_boundary_defect()
    assert triangle_boundary_defect() == Fraction(0)


def test_end_to_end_public_contract() -> None:
    edge, face = triangle_boundaries()
    assert require_boundary_square(edge, face) == Fraction(0)
    image = BoundaryOperator(edge).apply(tuple(face.col(0)))
    assert image == _ZERO


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "CellGrammar.lean").read_text(encoding="utf-8")
    assert "boundarySquare" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:triangle-boundary-square:v1" in source
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
    ("face orientation flipped", "_FACE_MIDDLE = Fraction(-1)", "_FACE_MIDDLE = Fraction(1)"),
    ("composition check inverted", "if left.cols != right.rows:", "if left.cols == right.rows:"),
    ("string accepted as a chain", "isinstance(values, (str, bytes)) or ", ""),
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
    defect_of = namespace["triangle_boundary_defect"]
    boundaries = namespace["triangle_boundaries"]
    operator = namespace["BoundaryOperator"]
    if not _all_hold((callable(defect_of), callable(boundaries), isinstance(operator, type),)):
        return False
    try:
        defect = defect_of()
        edge, face = boundaries()
        image = operator(edge).apply((1, -1, 1))
        column = operator(edge).apply((1, 0, 0))
        cycle = tuple(face.col(0))
    except error:
        return False
    if defect != 0 or image != _ZERO or column != _COLUMN:
        return False
    return cycle == _CYCLE


def _bad_values_refused(namespace: dict[str, object]) -> bool:
    mismatch = namespace["DimensionMismatchError"]
    nonzero = namespace["NonZeroCompositionError"]
    operator_type = namespace["BoundaryOperator"]
    boundaries = namespace["triangle_boundaries"]
    require = namespace["require_boundary_square"]
    matrix_type = namespace["ExactMatrix"]
    if not _all_hold((isinstance(mismatch, type), isinstance(nonzero, type), isinstance(operator_type, type),)):
        return False
    factory = getattr(matrix_type, "from_rows", None)
    if not _all_hold((isinstance(matrix_type, type), callable(factory), callable(boundaries), callable(require),)):
        return False
    edge, _face = boundaries()
    operator = operator_type(edge)
    bad_face = factory([[Fraction(1)], [Fraction(1)], [Fraction(1)]])
    expected = (
        (mismatch, lambda: operator.apply((_probe("1.0"), 0, 0)), "float refused at the public boundary"),
        (mismatch, lambda: operator.apply((True, 0, 0)), "boolean refused where a rational was required"),
        (mismatch, lambda: operator.apply("123"), "boundary chain must be a sequence"),
        (mismatch, lambda: operator.apply((1, 0)), "boundary chain length does not match the operator"),
        (nonzero, lambda: require(edge, bad_face), "triangle boundary square is not zero"),
        (mismatch, lambda: require(bad_face, edge), "boundary factors do not compose"),
    )
    for error, probe, invariant in expected:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["DimensionMismatchError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_boundary_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_boundary_{index}"
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
