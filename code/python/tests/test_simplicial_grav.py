"""Unit, negative, integration, end-to-end, and mutation tests for boundary area.

Origin: code/python/src/qm/simplicial_grav.py
Claim: urn:omega:fqm:grav:boundary-area-even:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""



from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

import pytest

from src.homology.ids import SimplexId
from src.qm.simplicial_grav import SimplicialGravityError, boundary_face_area, main, polygon_area

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "simplicial_grav.py"


def test_boundary_area_is_even_and_gluing_reduces_it() -> None:
    assert boundary_face_area() == 12
    assert boundary_face_area(3, 1) == 10
    assert boundary_face_area(1, 0) == 4
    assert boundary_face_area(4, 2) == 12
    assert polygon_area() == Fraction(12)
    assert type(boundary_face_area()) is int
    assert boundary_face_area(3, 1) != polygon_area()


def test_negative_type_failures() -> None:
    with pytest.raises(SimplicialGravityError, match="float refused") as floated:
        boundary_face_area(_probe("1.0"), 0)
    assert floated.value.invariant == "float refused at the count boundary"
    assert floated.value.parameters["role"] == "simplices"
    assert type(floated.value) is SimplicialGravityError

    with pytest.raises(SimplicialGravityError, match="boolean refused") as boolean:
        boundary_face_area(True, 0)
    assert boolean.value.invariant == "boolean refused where a natural count was required"

    with pytest.raises(SimplicialGravityError, match="not an integer") as text:
        boundary_face_area("3", 0)
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(SimplicialGravityError, match="count is negative") as simplices:
        boundary_face_area(-1, 0)
    assert simplices.value.parameters["role"] == "simplices"
    assert simplices.value.parameters["value"] == -1

    with pytest.raises(SimplicialGravityError, match="count is negative") as interior:
        boundary_face_area(3, -2)
    assert interior.value.parameters["role"] == "interior"

    with pytest.raises(SimplicialGravityError, match="float refused") as mixed:
        boundary_face_area(3, _probe("1.5"))
    assert mixed.value.parameters["role"] == "interior"


def test_integration_matches_simplex_vertex_count() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "SimplicialAreaLawPageCurve.lean").read_text(encoding="utf-8")
    assert "theorem boundary_area_even" in source
    assert "theorem gluing_reduces_boundary" in source
    face = SimplexId(2, (0, 1, 2))
    count = len(face.vertices)
    assert count == 3
    assert boundary_face_area(count, 0) == 4 * count
    assert boundary_face_area(count, 1) == 4 * count - 2
    assert polygon_area() == Fraction(12)


def test_end_to_end_cli_prints_twelve() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = main()
    assert code == 0
    assert stdout.getvalue() == "12\n"


def test_origin_resolves_in_repo() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "Origin: lean4/SimplicialAreaLawPageCurve.lean theorem boundary_area_even" in source
    assert "Claim: urn:omega:fqm:grav:boundary-area-even:v1" in source
    assert "AuthorityEffect: None" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float count admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
    ),
    (
        "boolean count admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    (
        "integer check inverted",
        "if type(value) is not int:",
        "if type(value) is int:",
    ),
    ("negative check weakened", "if value < 0:", "if value < -1:"),
    (
        "interior coefficient dropped",
        "4 * simplex_count - 2 * interior_faces",
        "4 * simplex_count - interior_faces",
    ),
    ("even check inverted", "if area % 2 != 0:", "if area % 2 == 0:"),
    (
        "gluing comparison flipped",
        "area >= 4 * simplex_count",
        "area < 4 * simplex_count",
    ),
    (
        "shoelace constant shifted",
        "if whole != Fraction(12):",
        "if whole != Fraction(11):",
    ),
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
    area = namespace["boundary_face_area"]
    shoelace = namespace["polygon_area"]
    if not _all_hold((callable(area), callable(shoelace),)):
        return False
    try:
        values = (area(), area(3, 1), area(1, 0), area(4, 2), shoelace())
    except error:
        return False
    return values == (12, 10, 4, 12, Fraction(12))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    area = namespace["boundary_face_area"]
    if not callable(area):
        return False
    probes = (
        (lambda: area(_probe("1.0"), 0), "float refused at the count boundary"),
        (lambda: area(True, 0), "boolean refused where a natural count was required"),
        (lambda: area("3", 0), "count is not an integer"),
        (lambda: area(-1, 0), "count is negative"),
        (lambda: area(3, -2), "count is negative"),
        (lambda: area(3, _probe("1.5")), "float refused at the count boundary"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["SimplicialGravityError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_simplicial_grav_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_simplicial_grav_{index}"
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
