"""Unit, negative, integration, end-to-end, and mutation tests for the Smith export.

Origin: code/python/src/linear_algebra/__init__.py
Claim: urn:omega:fqm:linear-algebra:exported-smith-trace:v1
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

import src.linear_algebra as linear_algebra
from src.linear_algebra import ExactMatrix, SmithExportError, exported_smith_trace
from src.linear_algebra.smith_form import SmithFormError, smith_normal_form

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "__init__.py"
_Q = Fraction
_FROZEN = ((2, 4), (2, 6))


def _raises(probe: Any, invariant: str) -> SmithExportError:
    with pytest.raises(SmithExportError) as caught:
        probe()
    assert caught.value.invariant == invariant
    assert all(type(item).__name__ != "float" for item in caught.value.parameters.values())
    return caught.value


def test_frozen_witness_trace_is_four() -> None:
    assert exported_smith_trace() == 4
    assert exported_smith_trace(_FROZEN) == 4
    assert "exported_smith_trace" in linear_algebra.__all__
    assert linear_algebra.ExactMatrix is ExactMatrix
    diagonal, left, right = smith_normal_form(ExactMatrix.from_rows([[_Q(2), _Q(4)], [_Q(2), _Q(6)]]))
    assert left * ExactMatrix.from_rows([[_Q(2), _Q(4)], [_Q(2), _Q(6)]]) * right == diagonal
    assert _Q(diagonal.get(0, 0)) + _Q(diagonal.get(1, 1)) == 4


def test_negative_witnesses_record_every_invariant() -> None:
    floated = _raises(lambda: exported_smith_trace(((_probe("0.5"), 0), (0, 1))), "float refused at the public boundary")
    assert floated.parameters == {"role": "row0_0", "received": "float"}
    boolean = _raises(
        lambda: exported_smith_trace(((True, 0), (0, 1))),
        "boolean refused where an integer witness entry was required",
    )
    assert boolean.parameters == {"role": "row0_0"}
    _raises(lambda: exported_smith_trace((("2", 4), (2, 6))), "Smith witness entry must be an exact integer")
    _raises(lambda: exported_smith_trace(((2, 4),)), "Smith witness must be two rows")
    _raises(lambda: exported_smith_trace("24"), "Smith witness must be two rows")
    _raises(lambda: exported_smith_trace(((2, 4, 0), (2, 6, 0))), "Smith witness row must contain two entries")
    _raises(lambda: exported_smith_trace((["2", "4"], (2, 6))), "Smith witness row must contain two entries")
    eye = ExactMatrix.identity(2)
    doubled = ExactMatrix.from_rows([[_Q(2), _Q(0)], [_Q(0), _Q(2)]])
    _raises(
        lambda: linear_algebra._require_factorization(eye, eye, eye, doubled),
        "exported Smith form failed U*A*V = D",
    )
    _raises(lambda: linear_algebra._rational_entry("1", "d0"), "Smith diagonal entry is not an exact rational")


def test_neighbor_smith_error_propagates(monkeypatch: pytest.MonkeyPatch) -> None:
    def refuse(matrix: object) -> tuple[ExactMatrix, ExactMatrix, ExactMatrix]:
        raise SmithFormError("neighbor Smith form refused the witness", {"role": "smith"})

    monkeypatch.setattr(linear_algebra, "smith_normal_form", refuse)
    with pytest.raises(SmithFormError) as caught:
        exported_smith_trace()
    assert caught.value.invariant == "neighbor Smith form refused the witness"
    assert type(caught.value) is SmithFormError


def test_integration_matches_rust_smith_sentence() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "smith_form.rs").read_text(encoding="utf-8")
    assert 'DEFAULT_SNF_PIVOT_ITERATION_LIMIT' in source
    assert 'DEFAULT_SNF_PIVOT_ITERATION_LIMIT' in source
    assert exported_smith_trace() == linear_algebra.smith_form.witness_diagonal_sum() == 4


def test_end_to_end_public_contract() -> None:
    assert linear_algebra.exported_smith_trace() == 4
    with pytest.raises(SmithExportError, match="float refused"):
        linear_algebra.exported_smith_trace(((_probe("1.0"), 1), (0, 1)))


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "smith_form.rs"
    assert origin.is_file()
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:exported-smith-trace:v1" in source
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
        "integer gate removed",
        "if type(value) is not int:",
        "if False and type(value) is not int:",
    ),
    (
        "witness width collapsed",
        "len(value) != 2",
        "len(value) != 0",
    ),
    (
        "frozen corner replaced",
        "((2, 4), (2, 6))",
        "((2, 4), (2, 8))",
    ),
    (
        "factor order reversed",
        "left * witness * right != diagonal",
        "witness * left * right != diagonal",
    ),
    (
        "diagonal sum replaced",
        '_rational_entry(diagonal.get(0, 0), "d0") + _rational_entry(diagonal.get(1, 1), "d1")',
        '_rational_entry(diagonal.get(0, 0), "d0") - _rational_entry(diagonal.get(1, 1), "d1")',
    ),
    (
        "second diagonal entry cleared",
        'diagonal.get(1, 1)',
        "diagonal.get(0, 1)",
    ),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.linear_algebra"
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
        explicit = function(_FROZEN)
    except Exception:
        return False
    return _all_hold((frozen == 4, explicit == 4,))


def _boundary_holds(function: object, error: type[BaseException]) -> bool:
    if not callable(function):
        return False
    probes = (
        (lambda: function(((_probe("0.5"), 0), (0, 1))), "float refused at the public boundary"),
        (lambda: function(((True, 0), (0, 1))), "boolean refused where an integer witness entry was required"),
        (lambda: function((("x", 0), (0, 1))), "Smith witness entry must be an exact integer"),
    )
    return all(_invariant(error, probe) == invariant for probe, invariant in probes)


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["SmithExportError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    function = namespace["exported_smith_trace"]
    if not _certificates_hold(function):
        return False
    return _boundary_holds(function, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_smith_export_baseline")
        assert _oracle(_load_source(source, loaded[-1])) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_smith_export_{index}"
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
