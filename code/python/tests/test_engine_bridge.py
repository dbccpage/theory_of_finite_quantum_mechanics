"""Unit, negative, integration, end-to-end, and mutation tests for the Z bridge."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from src.qm.campaigns.engine_bridge import BridgeError, pythagorean_expectation, z_expectation


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "campaigns" / "engine_bridge.py"
_Q = Fraction
_STATE = (_Q(3, 5), _Q(4, 5))
_VALUE = _Q(-7, 25)


def _raises(probe: Any, invariant: str) -> BridgeError:
    with pytest.raises(BridgeError) as caught:
        probe()
    assert caught.value.invariant == invariant
    assert all(type(item) is not float for item in caught.value.parameters.values())
    return caught.value


def test_pythagorean_expectation_is_the_population_difference() -> None:
    assert z_expectation() == _VALUE
    assert z_expectation(_STATE) == _Q(9, 25) - _Q(16, 25)
    assert pythagorean_expectation() == _VALUE
    assert pythagorean_expectation(_STATE) == _VALUE
    assert type(pythagorean_expectation()) is Fraction


def test_negative_bridge_records_every_invariant() -> None:
    floated = _raises(lambda: pythagorean_expectation((0.5, _Q(0))), "float refused at the public boundary")
    assert floated.parameters == {"role": "amplitude_up", "received": "float"}
    boolean = _raises(
        lambda: z_expectation((True, _Q(0))),
        "boolean refused where an exact rational was required",
    )
    assert boolean.parameters == {"role": "amplitude_up"}
    _raises(lambda: z_expectation(("3/5", _Q(4, 5))), "amplitude coordinate is not an exact rational")
    _raises(lambda: z_expectation((_Q(1),)), "the bridge expects a qubit amplitude")
    off = _raises(lambda: z_expectation((_Q(1), _Q(1))), "amplitude norm is not 1")
    assert off.parameters["norm"] == "2"
    other = _raises(lambda: pythagorean_expectation((_Q(1), _Q(0))), "expectation disagrees with the population difference")
    assert other.parameters["value"] == "1"
    assert other.parameters["population"] == "-7/25"


def test_integration_matches_pauli_z_definition() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "GroupParameter.lean").read_text(encoding="utf-8")
    assert "/-- Pauli Z generator matrix: diag(1, -1). -/" in source
    assert "def pauliZ" in source
    assert z_expectation(_STATE) == _VALUE
    assert pythagorean_expectation() == _VALUE


def test_end_to_end_public_contract() -> None:
    assert pythagorean_expectation() == _VALUE
    with pytest.raises(BridgeError, match="float refused"):
        pythagorean_expectation((_Q(3, 5), 0.5))


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "lean4" / "GroupParameter.lean"
    assert origin.is_file()
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:qm:pythagorean-z-expectation:v1" in source
    assert "Scope Fence:" in source
    assert "Gate 5 measurement:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        "if isinstance(value, float):\n        return",
    ),
    (
        "boolean admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    (
        "rational gate removed",
        "if type(value) is not int:",
        "if False and type(value) is not int:",
    ),
    (
        "pair width collapsed",
        "len(value) != 2",
        "len(value) != 0",
    ),
    (
        "norm gate inverted",
        "if norm != 1:",
        "if norm == 1:",
    ),
    (
        "expectation sign flipped",
        "return up * up - down * down",
        "return up * up + down * down",
    ),
    (
        "population sine collapsed",
        "Fraction(16, 25)",
        "Fraction(9, 25)",
    ),
    (
        "population comparison inverted",
        "if value != _POPULATION:",
        "if value == _POPULATION:",
    ),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
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


def _certificates_hold(function: object) -> bool:
    if not callable(function):
        return False
    try:
        frozen = function()
        explicit = function(_STATE)
    except Exception:
        return False
    return frozen == _VALUE and explicit == _VALUE


def _boundary_holds(function: object, error: type[BaseException]) -> bool:
    if not callable(function):
        return False
    probes = (
        (lambda: function((0.5, _Q(0))), "float refused at the public boundary"),
        (lambda: function((True, _Q(0))), "boolean refused where an exact rational was required"),
        (lambda: function(("x", _Q(0))), "amplitude coordinate is not an exact rational"),
        (lambda: function((_Q(1),)), "the bridge expects a qubit amplitude"),
        (lambda: function((_Q(1), _Q(1))), "amplitude norm is not 1"),
        (lambda: function((_Q(1), _Q(0))), "expectation disagrees with the population difference"),
    )
    return all(_invariant(error, probe) == invariant for probe, invariant in probes)


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["BridgeError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    function = namespace["pythagorean_expectation"]
    if not _certificates_hold(function):
        return False
    return _boundary_holds(function, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_engine_bridge_baseline")
        assert _oracle(_load_source(source, loaded[-1])) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_engine_bridge_{index}"
            loaded.append(module_name)
            try:
                survived = _oracle(_load_source(source.replace(old, new, 1), module_name))
            except Exception:
                survived = False
            assert survived is False, name
            killed += 1
        assert killed == len(_MUTANTS)
        assert f"Mutation-Kills: {killed} non-equivalent" in source
    finally:
        for module_name in loaded:
            sys.modules.pop(module_name, None)
