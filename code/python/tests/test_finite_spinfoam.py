"""Unit, negative, integration, end-to-end, and mutation tests for the tetrahedron Euler count."""

from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from src.combinatorics.finite_combinatorics import binomial_exact
from src.qm.finite_spinfoam import SpinfoamError, certified_euler, main, tetrahedron_euler

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "finite_spinfoam.py"


def test_labeled_tetrahedron_has_characteristic_two() -> None:
    assert tetrahedron_euler((0, 1, 2, 3)) == 2
    assert tetrahedron_euler((-1, 0, 1, 2)) == 2
    assert tetrahedron_euler((3, 1, 0, 2)) == 2
    assert certified_euler() == 2
    assert type(tetrahedron_euler((0, 1, 2, 3))) is int


def test_negative_type_failures() -> None:
    with pytest.raises(SpinfoamError, match="float refused") as floated:
        tetrahedron_euler((1.0, 2, 3, 4))
    assert floated.value.invariant == "float refused at the vertex boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is SpinfoamError

    with pytest.raises(SpinfoamError, match="boolean refused") as boolean:
        tetrahedron_euler((True, 2, 3, 4))
    assert boolean.value.invariant == "boolean refused where an integer vertex was required"

    with pytest.raises(SpinfoamError, match="not an exact integer") as text:
        tetrahedron_euler(("0", 1, 2, 3))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(SpinfoamError, match="not four") as short:
        tetrahedron_euler((0, 1, 2))
    assert short.value.parameters["length"] == 3

    with pytest.raises(SpinfoamError, match="not four") as long:
        tetrahedron_euler((0, 1, 2, 3, 4))
    assert long.value.parameters["length"] == 5

    with pytest.raises(SpinfoamError, match="duplicated") as duplicate:
        tetrahedron_euler((0, 0, 1, 2))
    assert duplicate.value.parameters["vertex"] == 0

    with pytest.raises(SpinfoamError, match="not a tuple") as listed:
        tetrahedron_euler([0, 1, 2, 3])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(SpinfoamError, match="not a tuple"):
        tetrahedron_euler("0123")


def test_integration_matches_binomial_counts() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "H029Simplicial3complexCayleyEvolution.lean").read_text(encoding="utf-8")
    assert "theorem tetrahedron_euler_characteristic" in source
    edges = binomial_exact(4, 2)
    faces = binomial_exact(4, 3)
    assert edges == 6
    assert faces == 4
    assert 4 - edges + faces == 2
    assert tetrahedron_euler((0, 1, 2, 3)) == 4 - edges + faces
    assert certified_euler() == 2


def test_end_to_end_cli_prints_two() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "2"
    assert certified_euler() == 2


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "H029Simplicial3complexCayleyEvolution.lean").read_text(encoding="utf-8")
    assert "theorem tetrahedron_euler_characteristic" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:spinfoam:tetrahedron-euler:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float vertex admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return 0\n    if False:",
    ),
    (
        "boolean vertex admitted",
        "if type(value) is bool:",
        "if type(value) is bool:\n        return 1\n    if False:",
    ),
    ("tuple check inverted", "not isinstance(vertices, tuple)", "isinstance(vertices, tuple)"),
    ("four-vertex check dropped", "len(vertices) != _WIDTH", "len(vertices) != -1"),
    ("duplicate check dropped", "if vertex in seen:", "if vertex != vertex:"),
    ("edges counted as singletons", "combinations(vertices, 2)", "combinations(vertices, 1)"),
    (
        "characteristic sign flipped",
        "vertex_count - edge_count + face_count",
        "vertex_count - edge_count - face_count",
    ),
    ("edge count check shifted", "edge_count != 6", "edge_count != 7"),
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
    euler = namespace["tetrahedron_euler"]
    certified = namespace["certified_euler"]
    if not callable(euler) or not callable(certified):
        return False
    try:
        standard = euler((0, 1, 2, 3))
        shifted = euler((-1, 0, 1, 2))
        ordered = euler((3, 1, 0, 2))
        checked = certified()
    except error:
        return False
    return (standard, shifted, ordered, checked) == (2, 2, 2, 2)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    euler = namespace["tetrahedron_euler"]
    if not callable(euler):
        return False
    probes = (
        (lambda: euler((1.0, 2, 3, 4)), "float refused at the vertex boundary"),
        (lambda: euler((True, 2, 3, 4)), "boolean refused where an integer vertex was required"),
        (lambda: euler(("0", 1, 2, 3)), "tetrahedron vertex is not an exact integer"),
        (lambda: euler((0, 1, 2)), "tetrahedron vertices are not four"),
        (lambda: euler((0, 1, 2, 3, 4)), "tetrahedron vertices are not four"),
        (lambda: euler((0, 0, 1, 2)), "tetrahedron vertex is duplicated"),
        (lambda: euler([0, 1, 2, 3]), "tetrahedron vertices are not a tuple"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["SpinfoamError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_finite_spinfoam_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_finite_spinfoam_{index}"
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
