"""Unit, negative, integration, end-to-end, and mutation tests for the triangle cycle."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from src.homology.boundary import triangle_boundaries
from src.homology.chain import Chain, face_column, face_cycle_boundary, require_closed_edge_cycle, vertex_boundary
from src.homology.errors import DimensionMismatchError, require_composition_zero

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "chain.py"


def test_face_cycle_is_closed() -> None:
    assert face_column() == (Fraction(1), Fraction(-1), Fraction(1))
    assert face_cycle_boundary() == (Fraction(0), Fraction(0), Fraction(0))
    assert vertex_boundary((1, -1, 1)) == (Fraction(0), Fraction(0), Fraction(0))
    assert Chain(1, (Fraction(1), Fraction(-1), Fraction(1))).total() == Fraction(1)


def test_negative_boundary_failures() -> None:
    with pytest.raises(DimensionMismatchError, match="float refused") as floated:
        vertex_boundary((1.0, 0, 0))
    assert floated.value.parameters["role"] == "edge[0]"

    with pytest.raises(DimensionMismatchError, match="boolean refused") as boolean:
        vertex_boundary(cast(tuple[object, ...], (True, 0, 0)))
    assert boolean.value.parameters["role"] == "edge[0]"

    with pytest.raises(DimensionMismatchError, match="not an exact rational") as text:
        vertex_boundary(("1", 0, 0))
    assert text.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="must be a sequence") as raw:
        vertex_boundary("123")
    assert raw.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="length 3") as length:
        vertex_boundary((1, 0))
    assert length.value.parameters["length"] == 2

    with pytest.raises(DimensionMismatchError, match="not closed") as opened:
        require_closed_edge_cycle((1, 0, 0))
    assert opened.value.parameters["index"] == 0

    with pytest.raises(DimensionMismatchError, match="nonnegative int") as dim:
        Chain(cast(int, True), ())
    assert dim.value.parameters["received"] == "bool"

    with pytest.raises(DimensionMismatchError, match="nonnegative int") as negative:
        Chain(-1, ())
    assert negative.value.parameters["received"] == "int"


def test_integration_with_boundary_neighbor() -> None:
    """∂1 ∂2 of the neighboring triangle matrices is the same zero witnessed here."""
    edge, face = triangle_boundaries()
    edge_rows = [edge.row(index) for index in range(edge.rows)]
    face_rows = [face.row(index) for index in range(face.rows)]
    assert require_composition_zero(edge_rows, face_rows) == Fraction(0)
    assert face_cycle_boundary() == (Fraction(0), Fraction(0), Fraction(0))


def test_end_to_end_public_contract() -> None:
    assert require_closed_edge_cycle(face_column()) == (Fraction(0), Fraction(0), Fraction(0))
    with pytest.raises(DimensionMismatchError, match="float refused") as caught:
        Chain(0, cast(tuple[Fraction, ...], (0.5,)))
    assert caught.value.parameters["role"] == "coeff[0]"


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "FiniteCochain.lean").read_text(encoding="utf-8")
    assert "theorem d1_d0_zero" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:triangle-cycle-boundary:v1" in source
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
    ("length check inverted", "if len(parsed) != edge.cols:", "if len(parsed) == edge.cols:"),
    ("closure check inverted", "if entry != 0:", "if entry == 0:"),
    ("cycle orientation flipped", "Fraction(-1)", "Fraction(1)"),
    ("coefficient total subtracted", "total += coeff", "total -= coeff"),
    ("negative dimension accepted", "or dim < 0:", "or dim < -1:"),
    ("string accepted as coefficients", "isinstance(values, (str, bytes)) or ", ""),
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
    boundary = namespace["face_cycle_boundary"]
    column = namespace["face_column"]
    chain = namespace["Chain"]
    if not callable(boundary) or not callable(column) or not isinstance(chain, type):
        return False
    try:
        image = boundary()
        cycle = column()
        total = chain(1, (Fraction(1), Fraction(1))).total()
    except error:
        return False
    if image != (Fraction(0), Fraction(0), Fraction(0)):
        return False
    if cycle != (Fraction(1), Fraction(-1), Fraction(1)):
        return False
    matches = total == Fraction(2)
    if matches is True:
        return True
    return False


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    boundary = namespace["vertex_boundary"]
    closed = namespace["require_closed_edge_cycle"]
    chain = namespace["Chain"]
    if not callable(boundary) or not callable(closed) or not isinstance(chain, type):
        return False
    expected = (
        (lambda: boundary((1.0, 0, 0)), "float refused at the public boundary"),
        (lambda: boundary((True, 0, 0)), "boolean refused where a rational was required"),
        (lambda: boundary("123"), "coefficients must be a sequence"),
        (lambda: closed((1, 0, 0)), "edge cycle is not closed"),
        (lambda: chain(-1, ()), "chain dimension must be a nonnegative int"),
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
        loaded.append("mutant_chain_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_chain_{index}"
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
