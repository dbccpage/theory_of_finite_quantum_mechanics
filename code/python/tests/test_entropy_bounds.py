"""Unit, negative, integration, end-to-end, and mutation tests for the Cauchy collision bound."""

from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

import pytest

from src.bin.entropy_cli import collision_probability as cli_collision
from src.qm.entropy_bounds import (
    EntropyBoundError,
    cauchy_defect,
    certified_collision,
    collision_probability,
    main,
)

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "entropy_bounds.py"
_FIXTURE = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))


def test_fixture_collision_and_defect() -> None:
    assert collision_probability(_FIXTURE) == Fraction(7, 18)
    assert cauchy_defect(_FIXTURE) == Fraction(1, 6)
    assert collision_probability((1, 0, 0)) == Fraction(1)
    assert cauchy_defect((1, 0, 0)) == Fraction(2)
    assert collision_probability((Fraction(1, 3), Fraction(1, 3), Fraction(1, 3))) == Fraction(1, 3)
    assert cauchy_defect((Fraction(1, 3), Fraction(1, 3), Fraction(1, 3))) == Fraction(0)
    assert certified_collision() == Fraction(7, 18)
    assert type(collision_probability((1, 0, 0))) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(EntropyBoundError, match="float refused") as floated:
        collision_probability((1.0, 0, 0))
    assert floated.value.invariant == "float refused at the collision boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is EntropyBoundError

    with pytest.raises(EntropyBoundError, match="boolean refused") as boolean:
        collision_probability((True, 0, 0))
    assert boolean.value.invariant == "boolean refused where a rational weight was required"

    with pytest.raises(EntropyBoundError, match="negative") as negative:
        cauchy_defect((Fraction(-1, 2), Fraction(3, 2), 0))
    assert negative.value.parameters["received"] == "-1/2"

    with pytest.raises(EntropyBoundError, match="not an exact rational") as text:
        collision_probability(("1", 0, 0))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(EntropyBoundError, match="not a tuple") as listed:
        collision_probability([1, 0, 0])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(EntropyBoundError, match="not a triple") as short:
        collision_probability((1, 0))
    assert short.value.parameters["length"] == 2

    with pytest.raises(EntropyBoundError, match="not a triple") as empty:
        collision_probability(())
    assert empty.value.parameters["length"] == 0

    with pytest.raises(EntropyBoundError, match="not a triple") as long:
        cauchy_defect((1, 0, 0, 0))
    assert long.value.parameters["length"] == 4

    with pytest.raises(EntropyBoundError, match="do not sum to one") as mass:
        collision_probability((2, 0, 0))
    assert mass.value.parameters["total"] == "2"

    with pytest.raises(EntropyBoundError, match="not a tuple"):
        collision_probability("100")


def test_integration_matches_integer_cauchy_identity() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "DerivationDagQMClosure.lean").read_text(encoding="utf-8")
    assert "theorem signed_sqrt_density_lift_cauchy_schwarz" in source
    assert "def sqDiffSum3" in source
    w0, w1, w2 = 2, 3, 5
    pairwise = (w0 - w1) * (w0 - w1) + (w1 - w2) * (w1 - w2) + (w2 - w0) * (w2 - w0)
    squares = w0 * w0 + w1 * w1 + w2 * w2
    mass = w0 + w1 + w2
    assert pairwise == 3 * squares - mass * mass
    assert pairwise == 14
    normalized = (Fraction(w0, mass), Fraction(w1, mass), Fraction(w2, mass))
    assert collision_probability(normalized) == cli_collision(normalized)
    assert cauchy_defect(normalized) == Fraction(pairwise, mass * mass)


def test_end_to_end_cli_prints_seven_eighteenths() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "7/18"
    assert certified_collision() == Fraction(7, 18)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "DerivationDagQMClosure.lean").read_text(encoding="utf-8")
    assert "theorem signed_sqrt_density_lift_cauchy_schwarz" in source
    assert "def sqDiffSum3" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:entropy:cauchy-collision-bound:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float weight admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return Fraction(0)\n    if False:",
    ),
    (
        "boolean weight admitted",
        "if type(value) is bool:",
        "if type(value) is bool:\n        return Fraction(1)\n    if False:",
    ),
    ("negative weight admitted", "if weight < 0:", "if weight < -1:"),
    ("mass check inverted", "if total != 1:", "if total == 1:"),
    ("triple length admitted", "len(weights) != _WIDTH", "len(weights) != -1"),
    ("tuple check inverted", "not isinstance(weights, tuple)", "isinstance(weights, tuple)"),
    ("square replaced by the weight", "return weight * weight", "return weight"),
    ("pairwise square replaced by the gap", "return gap * gap", "return gap"),
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
    collision = namespace["collision_probability"]
    defect = namespace["cauchy_defect"]
    certified = namespace["certified_collision"]
    if not callable(collision) or not callable(defect) or not callable(certified):
        return False
    try:
        measured = collision(_FIXTURE)
        pure = collision((1, 0, 0))
        fair = collision((Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)))
        gap = defect(_FIXTURE)
        pure_gap = defect((1, 0, 0))
        signed = certified()
    except error:
        return False
    actual = (measured, pure, fair, gap, pure_gap, signed)
    expected = (Fraction(7, 18), Fraction(1), Fraction(1, 3), Fraction(1, 6), Fraction(2), Fraction(7, 18))
    return bool(actual == expected and Fraction(3) * measured - Fraction(1) == gap)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    collision = namespace["collision_probability"]
    defect = namespace["cauchy_defect"]
    if not callable(collision) or not callable(defect):
        return False
    probes = (
        (lambda: collision((1.0, 0, 0)), "float refused at the collision boundary"),
        (lambda: collision((True, 0, 0)), "boolean refused where a rational weight was required"),
        (lambda: collision((-1, 2, 0)), "collision weight is negative"),
        (lambda: collision((1, 0, 0, 0)), "collision weights are not a triple"),
        (lambda: collision((2, 0, 0)), "collision weights do not sum to one"),
        (lambda: collision([1, 0, 0]), "collision weights are not a tuple"),
        (lambda: collision(("1", 0, 0)), "collision weight is not an exact rational"),
        (lambda: defect((1, 0)), "collision weights are not a triple"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["EntropyBoundError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_entropy_bounds_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_entropy_bounds_{index}"
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
