"""Unit, negative, integration, end-to-end, and mutation tests for simplicial boundaries."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

from src.homology.boundary import triangle_boundaries
from src.homology.errors import DimensionMismatchError, require_composition_zero
from src.homology.simplicial import (
    Simplex,
    SimplicialComplex,
    boundary_square_defect,
    filled_triangle,
    triangle_boundary_square,
)

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "simplicial.py"


def test_filled_triangle_boundaries_match_orientation() -> None:
    complex_ = filled_triangle()
    assert complex_.dimension() == 2
    assert len(complex_.of_dimension(1)) == 3
    assert Simplex.create([2, 0, 1]).vertices == (0, 1, 2)
    assert Simplex.create([0]).faces() == ()
    face = complex_.boundary_matrix(2)
    assert list(face.data) == [Fraction(1), Fraction(-1), Fraction(1)]
    assert triangle_boundary_square() == Fraction(0)


def test_negative_simplicial_failures() -> None:
    with pytest.raises(DimensionMismatchError, match="float refused") as float_error:
        Simplex.create([1.0])
    assert float_error.value.parameters["role"] == "vertex[0]"

    with pytest.raises(DimensionMismatchError, match="boolean refused where a vertex") as bool_error:
        Simplex.create([True])
    assert bool_error.value.parameters["index"] == 0

    with pytest.raises(DimensionMismatchError, match="not distinct") as duplicate:
        Simplex.create([1, 1])
    assert "1" in str(duplicate.value.parameters["vertices"])

    with pytest.raises(DimensionMismatchError, match="must be a sequence") as text:
        Simplex.create("01")
    assert text.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="at least one vertex"):
        Simplex.create([])

    vertices = tuple(Simplex.create([index]) for index in range(3))
    broken = SimplicialComplex(vertices + (Simplex.create([0, 1, 2]),))
    with pytest.raises(DimensionMismatchError, match="face is missing") as missing:
        broken.boundary_matrix(2)
    assert missing.value.parameters["face"] == "(1, 2)"

    with pytest.raises(DimensionMismatchError, match="at least 2") as low_dim:
        boundary_square_defect(filled_triangle(), 1)
    assert low_dim.value.parameters["received"] == 1

    with pytest.raises(DimensionMismatchError, match="float refused") as float_dim:
        boundary_square_defect(filled_triangle(), 2.0)
    assert float_dim.value.parameters["role"] == "dim"

    with pytest.raises(DimensionMismatchError, match="expects a simplicial complex") as bare:
        boundary_square_defect("triangle", 2)
    assert bare.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="must be simplices") as entry:
        SimplicialComplex((Simplex.create([0]), "edge"))  # type: ignore[arg-type]
    assert entry.value.parameters["index"] == 1


def test_integration_with_triangle_boundaries() -> None:
    edge, face = triangle_boundaries()
    complex_ = filled_triangle()
    boundary1 = complex_.boundary_matrix(1)
    boundary2 = complex_.boundary_matrix(2)
    assert list(boundary1.data) == list(edge.data)
    assert list(boundary2.data) == list(face.data)
    rows1 = [boundary1.row(index) for index in range(boundary1.rows)]
    rows2 = [boundary2.row(index) for index in range(boundary2.rows)]
    assert require_composition_zero(rows1, rows2) == Fraction(0)
    assert boundary_square_defect(complex_, 2) == Fraction(0)


def test_end_to_end_public_contract() -> None:
    assert triangle_boundary_square() == Fraction(0)
    simplex = Simplex.create([1, 0])
    assert simplex.dim == 1
    assert simplex.faces()[0].vertices == (1,)
    assert simplex.faces()[1].vertices == (0,)
    with pytest.raises(DimensionMismatchError, match="float refused"):
        filled_triangle().boundary_matrix(1.5)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "CellGrammar.lean").read_text(encoding="utf-8")
    assert "boundarySquare" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:simplicial-boundary-square:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return\n    if False:",
    ),
    (
        "boolean vertex admitted",
        "if isinstance(vertex, bool):",
        "if isinstance(vertex, bool):\n        return int(vertex)\n    if False:",
    ),
    (
        "duplicate vertices accepted",
        "if len(set(parsed)) != len(parsed):",
        "if len(set(parsed)) < 0:",
    ),
    ("vertex sort removed", "ordered = tuple(sorted(parsed))", "ordered = parsed"),
    ("missing face ignored", "if slot is None:", "if False and slot is None:"),
    ("square dimension lowered", "if dim < minimum:", "if dim < minimum - 1:"),
    ("orientation parity swapped", "if omit % 2 == 0:", "if omit % 2 == 1:"),
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
    triangle = namespace["filled_triangle"]
    square = namespace["triangle_boundary_square"]
    defect = namespace["boundary_square_defect"]
    simplex = namespace["Simplex"]
    create = getattr(simplex, "create", None)
    if not callable(triangle) or not callable(square) or not callable(defect) or not callable(create):
        return False
    try:
        complex_ = triangle()
        measured = square()
        face = complex_.boundary_matrix(2)
        edge = create([1, 0])
    except error:
        return False
    if measured != 0 or defect(complex_, 2) != 0:
        return False
    if list(face.data) != [Fraction(1), Fraction(-1), Fraction(1)]:
        return False
    if edge.vertices != (0, 1) or edge.dim != 1:
        return False
    return True


def _bad_values_refused(namespace: dict[str, object]) -> bool:
    mismatch = namespace["DimensionMismatchError"]
    simplex = namespace["Simplex"]
    complex_type = namespace["SimplicialComplex"]
    triangle = namespace["filled_triangle"]
    defect = namespace["boundary_square_defect"]
    create = getattr(simplex, "create", None)
    if not isinstance(mismatch, type) or not isinstance(complex_type, type):
        return False
    if not callable(create) or not callable(triangle) or not callable(defect):
        return False
    vertices = tuple(create([index]) for index in range(3))
    broken = complex_type(vertices + (create([0, 1, 2]),))
    filled = triangle()
    expected = (
        (mismatch, lambda: create([1.0]), "float refused at the public boundary"),
        (mismatch, lambda: create([True]), "boolean refused where a vertex was required"),
        (mismatch, lambda: create([1, 1]), "simplex vertices are not distinct"),
        (mismatch, lambda: broken.boundary_matrix(2), "face is missing from the complex"),
        (mismatch, lambda: defect(filled, 1), "a boundary square needs dimension at least 2"),
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
        loaded.append("mutant_simplicial_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_simplicial_{index}"
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
