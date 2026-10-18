"""Unit, negative, integration, end-to-end, and mutation tests for the Z gap.

Origin: code/python/src/qm/campaigns/separating_preds.py
Claim: urn:omega:fqm:qm:separating-z-gap:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""



from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from src.qm.campaigns.separating_preds import SeparationError, expectation_gap, z_expectation

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "campaigns" / "separating_preds.py"
_Q = Fraction
_COMP = (_Q(1), _Q(0))
_TILT = (_Q(3, 5), _Q(4, 5))
_GAP = _Q(32, 25)


def _raises(probe: Any, invariant: str) -> SeparationError:
    with pytest.raises(SeparationError) as caught:
        probe()
    assert caught.value.invariant == invariant
    assert all(type(item).__name__ != "float" for item in caught.value.parameters.values())
    return caught.value


def test_frozen_states_are_separated_by_z() -> None:
    assert z_expectation(_COMP) == 1
    assert z_expectation(_TILT) == _Q(-7, 25)
    assert expectation_gap() == _GAP
    assert expectation_gap(_COMP, _TILT) == _GAP
    assert type(expectation_gap()) is Fraction


def test_negative_states_record_every_invariant() -> None:
    floated = _raises(lambda: expectation_gap((_probe("0.5"), _Q(0)), _TILT), "float refused at the public boundary")
    assert floated.parameters == {"role": "computational_up", "received": "float"}
    boolean = _raises(
        lambda: expectation_gap((True, _Q(0)), _TILT),
        "boolean refused where an exact rational was required",
    )
    assert boolean.parameters == {"role": "computational_up"}
    _raises(lambda: expectation_gap(("1", _Q(0)), _TILT), "amplitude coordinate is not an exact rational")
    _raises(lambda: expectation_gap((_Q(1),), _TILT), "state is not an amplitude pair")
    _raises(lambda: expectation_gap("up", _TILT), "state is not an amplitude pair")
    off = _raises(lambda: expectation_gap((_Q(1), _Q(1)), _TILT), "a state is not normalized")
    assert off.parameters["role"] == "computational"
    assert off.parameters["norm"] == "2"
    same = _raises(lambda: expectation_gap(_COMP, _COMP), "Z does not separate the two states")
    assert same.parameters == {"gap": "0"}
    tilted = _raises(lambda: z_expectation((_probe("0.5"), _Q(0))), "float refused at the public boundary")
    assert tilted.parameters["role"] == "amplitude_up"


def test_integration_matches_pauli_z_definition() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "GroupParameter.lean").read_text(encoding="utf-8")
    assert "def pauliZ" in source
    assert "| 0, 0 => 1" in source
    assert "| 1, 1 => -1" in source
    assert "theorem pauli_z_trace_zero" in source
    assert z_expectation(_COMP) == 1
    assert z_expectation(_TILT) == _Q(3, 5) * _Q(3, 5) - _Q(4, 5) * _Q(4, 5)
    assert expectation_gap() == _GAP


def test_end_to_end_public_contract() -> None:
    assert expectation_gap() == _GAP
    with pytest.raises(SeparationError, match="float refused"):
        expectation_gap(_COMP, (_Q(3, 5), _probe("0.5")))


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "lean4" / "GroupParameter.lean"
    assert origin.is_file()
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:qm:separating-z-gap:v1" in source
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
        "unit circle inverted",
        "if norm != 1:",
        "if norm == 1:",
    ),
    (
        "expectation sign flipped",
        "return up * up - down * down",
        "return up * up + down * down",
    ),
    (
        "tilt sine collapsed",
        "Fraction(4, 5)",
        "Fraction(3, 5)",
    ),
    (
        "separation test inverted",
        "if gap == 0:",
        "if gap != 0:",
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
        explicit = function(_COMP, _TILT)
    except Exception:
        return False
    return _all_hold((frozen == _GAP, explicit == _GAP,))


def _boundary_holds(function: object, error: type[BaseException]) -> bool:
    if not callable(function):
        return False
    probes = (
        (lambda: function((_probe("0.5"), _Q(0)), _TILT), "float refused at the public boundary"),
        (lambda: function((True, _Q(0)), _TILT), "boolean refused where an exact rational was required"),
        (lambda: function(("x", _Q(0)), _TILT), "amplitude coordinate is not an exact rational"),
        (lambda: function((_Q(1),), _TILT), "state is not an amplitude pair"),
        (lambda: function((_Q(1), _Q(1)), _TILT), "a state is not normalized"),
        (lambda: function(_COMP, _COMP), "Z does not separate the two states"),
    )
    return all(_invariant(error, probe) == invariant for probe, invariant in probes)


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["SeparationError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    function = namespace["expectation_gap"]
    if not _certificates_hold(function):
        return False
    return _boundary_holds(function, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_separating_preds_baseline")
        assert _oracle(_load_source(source, loaded[-1])) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_separating_preds_{index}"
            loaded.append(module_name)
            try:
                survived = _oracle(_load_source(source.replace(old, new, 1), module_name))
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
