"""Unit, negative, integration, end-to-end, and mutation tests for triangle holonomy."""

from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

import pytest

from src.qm.causal_prices import additive_holonomy
from src.qm.obstruction_calc import ObstructionError, certified_obstruction, face_obstruction, main

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "obstruction_calc.py"
_FIXTURE = (Fraction(0), Fraction(1, 2), Fraction(3, 5))
_PRICES = (Fraction(1), Fraction(2, 3), Fraction(4, 5))


def test_triangle_holonomy_is_zero() -> None:
    assert face_obstruction() == Fraction(0)
    assert face_obstruction(_FIXTURE) == Fraction(0)
    assert face_obstruction((1, 2, 3)) == Fraction(0)
    assert face_obstruction((Fraction(-1), 4, Fraction(1, 2))) == Fraction(0)
    assert face_obstruction(_PRICES) == Fraction(0)
    assert certified_obstruction() == Fraction(0)
    assert type(face_obstruction((1, 2, 3))) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(ObstructionError, match="float refused") as floated:
        face_obstruction((1.0, 2, 3))
    assert floated.value.invariant == "float refused at the vertex boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is ObstructionError

    with pytest.raises(ObstructionError, match="boolean refused") as boolean:
        face_obstruction((True, 2, 3))
    assert boolean.value.invariant == "boolean refused where a rational vertex was required"

    with pytest.raises(ObstructionError, match="not an exact rational") as text:
        face_obstruction(("0", 1, 2))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(ObstructionError, match="not three") as short:
        face_obstruction((0, 1))
    assert short.value.parameters["length"] == 2

    with pytest.raises(ObstructionError, match="not three") as long:
        face_obstruction((0, 1, 2, 3))
    assert long.value.parameters["length"] == 4

    with pytest.raises(ObstructionError, match="not a tuple") as listed:
        face_obstruction([0, 1, 2])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(ObstructionError, match="not a tuple"):
        face_obstruction("012")


def test_integration_matches_closed_price_holonomy() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "CoboundaryHolonomy.lean").read_text(encoding="utf-8")
    assert "theorem coboundary_triangle_holonomy_zero" in source
    assert "def coboundary" in source
    face = face_obstruction(_PRICES)
    holonomy = additive_holonomy(_PRICES)
    assert face == Fraction(0)
    assert holonomy == Fraction(0)
    assert face == holonomy
    assert face_obstruction(_FIXTURE) == Fraction(0)


def test_end_to_end_cli_prints_zero() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "0"
    assert certified_obstruction() == Fraction(0)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "CoboundaryHolonomy.lean").read_text(encoding="utf-8")
    assert "theorem coboundary_triangle_holonomy_zero" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:obstruction:triangle-coboundary:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float vertex admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
    ),
    (
        "boolean vertex admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    ("tuple check inverted", "not isinstance(vertices, tuple)", "isinstance(vertices, tuple)"),
    ("three-vertex check dropped", "len(vertices) != 3", "len(vertices) != -1"),
    ("edge keeps only the endpoint", "return end - start", "return end"),
    ("signed middle term flipped", "return left - middle + right", "return left + middle + right"),
    ("readings check inverted", "if cycle != signed:", "if cycle == signed:"),
    ("certified zero check inverted", "if value != _ZERO:", "if value == _ZERO:"),
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
    face = namespace["face_obstruction"]
    certified = namespace["certified_obstruction"]
    if not callable(face) or not callable(certified):
        return False
    try:
        values = (
            face(),
            face(_FIXTURE),
            face((1, 2, 3)),
            face((Fraction(-1), 4, Fraction(1, 2))),
            face(_PRICES),
            certified(),
        )
    except error:
        return False
    zeros = (Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    return values == zeros


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    face = namespace["face_obstruction"]
    if not callable(face):
        return False
    probes = (
        (lambda: face((1.0, 2, 3)), "float refused at the vertex boundary"),
        (lambda: face((True, 2, 3)), "boolean refused where a rational vertex was required"),
        (lambda: face(("0", 1, 2)), "triangle vertex is not an exact rational"),
        (lambda: face((0, 1)), "triangle vertices are not three"),
        (lambda: face((0, 1, 2, 3)), "triangle vertices are not three"),
        (lambda: face([0, 1, 2]), "triangle vertices are not a tuple"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["ObstructionError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_obstruction_calc_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_obstruction_calc_{index}"
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
