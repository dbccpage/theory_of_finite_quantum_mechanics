"""Unit, negative, integration, end-to-end, and mutation tests for the phase fiber.

Origin: code/python/src/qm/campaigns/phase_fiber.py
Claim: urn:omega:fqm:qm:phase-fiber-unit-product:v1
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

from src.linear_algebra.scalars import GaussianRational
from src.qm.campaigns.phase_fiber import PhaseFiberError, unit_product
from src.qm.campaigns import phase_fiber

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "phase_fiber.py"
_Q = Fraction
_FIRST = (_Q(3, 5), _Q(4, 5))
_SECOND = (_Q(5, 13), _Q(12, 13))


def _raises(probe: Any, invariant: str) -> PhaseFiberError:
    with pytest.raises(PhaseFiberError) as caught:
        probe()
    assert caught.value.invariant == invariant
    assert all(type(item).__name__ != "float" for item in caught.value.parameters.values())
    return caught.value


def test_frozen_phases_multiply_to_a_unit() -> None:
    assert unit_product() == 1
    assert unit_product(_FIRST, _SECOND) == 1
    product = GaussianRational(*_FIRST) * GaussianRational(*_SECOND)
    assert product.real == _Q(-33, 65)
    assert product.imag == _Q(56, 65)
    assert product.norm_sq() == 1


def test_negative_phases_record_every_invariant() -> None:
    floated = _raises(lambda: unit_product((_probe("0.5"), _Q(0)), _SECOND), "float refused at the public boundary")
    assert floated.parameters == {"role": "first_real", "received": "float"}
    boolean = _raises(
        lambda: unit_product((True, _Q(0)), _SECOND),
        "boolean refused where an exact rational was required",
    )
    assert boolean.parameters == {"role": "first_real"}
    _raises(lambda: unit_product(("3/5", _Q(4, 5)), _SECOND), "phase coordinate is not an exact rational")
    _raises(lambda: unit_product((_Q(3, 5),), _SECOND), "phase representative is not a coordinate pair")
    _raises(lambda: unit_product("3/5", _SECOND), "phase representative is not a coordinate pair")
    off_circle = _raises(
        lambda: unit_product((_Q(1), _Q(1)), _SECOND),
        "phase representative is not on the unit circle",
    )
    assert off_circle.parameters["role"] == "first"
    assert off_circle.parameters["norm"] == "2"
    second = _raises(
        lambda: unit_product(_FIRST, (_Q(1), _Q(0), _Q(0))),
        "phase representative is not a coordinate pair",
    )
    assert second.parameters["role"] == "second"
    _raises(
        lambda: phase_fiber._require_unit(GaussianRational(1, 1), "product"),
        "phase representative is not on the unit circle",
    )


def test_integration_matches_rust_connection_sentence() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "wdp" / "connection.rs").read_text(encoding="utf-8")
    assert 'test_frustrated_holonomy_is_gauge_invariant' in source
    assert "phase(qr(5, 13), qr(12, 13))" in source
    assert GaussianRational(*_FIRST).norm_sq() == 1
    assert GaussianRational(*_SECOND).norm_sq() == 1
    assert unit_product() == 1


def test_end_to_end_public_contract() -> None:
    assert phase_fiber.unit_product() == 1
    with pytest.raises(PhaseFiberError, match="float refused"):
        phase_fiber.unit_product((_Q(3, 5), _probe("0.5")), _SECOND)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "wdp" / "connection.rs"
    assert origin.is_file()
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:qm:phase-fiber-unit-product:v1" in source
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
        "first sine collapsed",
        "Fraction(4, 5)",
        "Fraction(3, 5)",
    ),
    (
        "second sine collapsed",
        "Fraction(12, 13)",
        "Fraction(5, 13)",
    ),
    (
        "product replaced by sum",
        "product = left * right",
        "product = left + right",
    ),
    (
        "unit circle inverted",
        "if norm != 1:",
        "if norm == 1:",
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


def _certificates_hold(function: object) -> bool:
    if not callable(function):
        return False
    try:
        frozen = function()
        explicit = function(_FIRST, _SECOND)
    except Exception:
        return False
    return _all_hold((frozen == 1, explicit == 1,))


def _boundary_holds(function: object, error: type[BaseException]) -> bool:
    if not callable(function):
        return False
    probes = (
        (lambda: function((_probe("0.5"), _Q(0)), _SECOND), "float refused at the public boundary"),
        (lambda: function((True, _Q(0)), _SECOND), "boolean refused where an exact rational was required"),
        (lambda: function(("x", _Q(0)), _SECOND), "phase coordinate is not an exact rational"),
        (lambda: function((_Q(1),), _SECOND), "phase representative is not a coordinate pair"),
    )
    return all(_invariant(error, probe) == invariant for probe, invariant in probes)


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["PhaseFiberError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    function = namespace["unit_product"]
    if not _certificates_hold(function):
        return False
    return _boundary_holds(function, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_phase_fiber_baseline")
        assert _oracle(_load_source(source, loaded[-1])) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_phase_fiber_{index}"
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
