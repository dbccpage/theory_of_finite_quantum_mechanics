"""Unit, negative, integration, end-to-end, and mutation tests for simplex identifiers."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from pathlib import Path
from typing import cast

import pytest

from src.homology.boundary import triangle_boundaries
from src.homology.errors import DimensionMismatchError
from src.homology.ids import ComplexId, SimplexId, triangle_simplex_ids

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "ids.py"


def test_triangle_census_matches_dim_plus_one() -> None:
    identified = triangle_simplex_ids()
    assert len(identified) == 7
    assert identified[0] == SimplexId(0, (0,))
    assert identified[3] == SimplexId(1, (0, 1))
    assert identified[6] == SimplexId(2, (0, 1, 2))
    assert ComplexId("triangle").name == "triangle"


def test_negative_boundary_failures() -> None:
    with pytest.raises(DimensionMismatchError, match="float refused") as floated:
        SimplexId(0, cast(tuple[int, ...], (1.0,)))
    assert floated.value.parameters["index"] == 0

    with pytest.raises(DimensionMismatchError, match="nonnegative int") as boolean:
        SimplexId(cast(int, True), (0, 1))
    assert boolean.value.parameters["received"] == "bool"

    with pytest.raises(DimensionMismatchError, match="must be ints") as vertex:
        SimplexId(0, cast(tuple[int, ...], (True,)))
    assert vertex.value.parameters["received"] == "bool"

    with pytest.raises(DimensionMismatchError, match="dim \\+ 1") as counted:
        SimplexId(1, (0,))
    assert counted.value.parameters["length"] == 1
    assert counted.value.parameters["dim"] == 1

    with pytest.raises(DimensionMismatchError, match="not distinct") as repeated:
        SimplexId(1, (0, 0))
    assert "0, 0" in str(repeated.value.parameters["vertices"])

    with pytest.raises(DimensionMismatchError, match="must be a tuple") as listed:
        SimplexId(0, cast(tuple[int, ...], [0]))
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(DimensionMismatchError, match="nonempty name") as named:
        ComplexId("")
    assert named.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="nonnegative int") as negative:
        SimplexId(-1, ())
    assert negative.value.parameters["received"] == "int"


def test_integration_with_boundary_neighbor() -> None:
    """The triangle face has 3 vertices, matching the 3 edges of the boundary matrix."""
    _edge, face = triangle_boundaries()
    face_id = SimplexId(2, (0, 1, 2))
    assert len(face_id.vertices) == face.rows
    assert len(triangle_simplex_ids()) == 7


def test_end_to_end_public_contract() -> None:
    four_simplex = SimplexId(4, (0, 1, 2, 3, 4))
    assert len(four_simplex.vertices) == four_simplex.dim + 1
    with pytest.raises(DimensionMismatchError, match="dim \\+ 1") as caught:
        SimplexId(4, (0, 1, 2, 3))
    assert caught.value.parameters["length"] == 4


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "H024FourSimplexSpinfoamS4.lean").read_text(encoding="utf-8")
    assert "A 4-simplex has 5 vertices" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:simplex-vertex-count:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float vertex admitted",
        "if isinstance(vertex, float):",
        "if isinstance(vertex, float):\n        return int(vertex)\n    if False:",
    ),
    ("boolean dimension admitted", "isinstance(dim, bool) or ", ""),
    ("vertex count off by one", "len(vertices) != dim + 1", "len(vertices) != dim"),
    ("duplicate vertices accepted", "if len(set(parsed)) != len(parsed):", "if len(set(parsed)) == len(parsed):"),
    ("negative dimension accepted", "or dim < 0:", "or dim < -1:"),
    ("boolean vertex admitted", "isinstance(vertex, bool) or ", ""),
    ("triangle census inverted", "if len(identified) != 7:", "if len(identified) == 7:"),
    ("empty complex name accepted", "or not self.name:", "or False:"),
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
    simplex = namespace["SimplexId"]
    census = namespace["triangle_simplex_ids"]
    named = namespace["ComplexId"]
    if not isinstance(simplex, type) or not callable(census) or not isinstance(named, type):
        return False
    try:
        edge = simplex(1, (0, 1))
        identified = census()
        complex_id = named("triangle")
    except error:
        return False
    if getattr(edge, "dim", None) != 1:
        return False
    if len(identified) != 7:
        return False
    return getattr(complex_id, "name", None) == "triangle"


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    simplex = namespace["SimplexId"]
    named = namespace["ComplexId"]
    if not isinstance(simplex, type) or not isinstance(named, type):
        return False
    expected = (
        (lambda: simplex(0, (1.0,)), "float refused at the public boundary"),
        (lambda: simplex(True, (0, 1)), "simplex dimension must be a nonnegative int"),
        (lambda: simplex(0, (True,)), "simplex vertices must be ints"),
        (lambda: simplex(1, (0, 0)), "simplex vertices are not distinct"),
        (lambda: simplex(-1, ()), "simplex dimension must be a nonnegative int"),
        (lambda: named(""), "complex id requires a nonempty name"),
    )
    for probe, invariant in expected:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["DimensionMismatchError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_simplex_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_simplex_{index}"
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
