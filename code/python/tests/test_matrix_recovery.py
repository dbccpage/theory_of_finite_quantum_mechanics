"""Unit, negative, integration, end-to-end, and mutation tests for column recovery."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from src.linear_algebra.elimination import witness_upper_entry
from src.qm.campaigns.matrix_recovery import RecoveryError, recover, recovery_defect


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "campaigns" / "matrix_recovery.py"
_Q = Fraction
_COLUMNS = ((_Q(1), _Q(3)), (_Q(2), _Q(4)))
_MATRIX = ((_Q(1), _Q(2)), (_Q(3), _Q(4)))


def _raises(probe: Any, invariant: str) -> RecoveryError:
    with pytest.raises(RecoveryError) as caught:
        probe()
    assert caught.value.invariant == invariant
    assert all(type(item) is not float for item in caught.value.parameters.values())
    return caught.value


def test_witness_columns_rebuild_the_matrix() -> None:
    assert recover(_COLUMNS) == _MATRIX
    assert recovery_defect() == 0
    assert recovery_defect(_COLUMNS) == 0
    assert type(recovery_defect()) is Fraction
    assert witness_upper_entry() == _Q(2, 3)


def test_negative_recovery_records_every_invariant() -> None:
    floated = _raises(lambda: recovery_defect(((0.5, _Q(3)), _COLUMNS[1])), "float refused at the public boundary")
    assert floated.parameters["role"] == "column0_0"
    assert floated.parameters["received"] == "float"
    boolean = _raises(
        lambda: recover(((True, _Q(3)), _COLUMNS[1])),
        "boolean refused where an exact rational was required",
    )
    assert boolean.parameters["role"] == "column0_0"
    _raises(lambda: recover((("1", _Q(3)), _COLUMNS[1])), "matrix entry is not an exact rational")
    _raises(lambda: recover("columns"), "columns are not a nonempty tuple")
    short = _raises(lambda: recover(((_Q(1),), _COLUMNS[1])), "basis images do not match the dimension")
    assert short.parameters["height"] == 2
    other = _raises(
        lambda: recovery_defect(((_Q(1), _Q(0)), (_Q(0), _Q(1)))),
        "recovery defect is not zero",
    )
    assert other.parameters["defect"] == "8"
    wide = _raises(lambda: recovery_defect(((_Q(1),),)), "recovery witness is 2 by 2")
    assert wide.parameters["rows"] == 1


def test_integration_matches_elimination_witness() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "python" / "src" / "linear_algebra" / "elimination.py").read_text(encoding="utf-8")
    assert "def witness_upper_entry" in source
    assert "[[1, 2], [3, 4]]" in source
    assert witness_upper_entry() == _Q(2, 3)
    assert recover(_COLUMNS) == _MATRIX
    assert recovery_defect() == 0


def test_end_to_end_public_contract() -> None:
    assert recovery_defect() == 0
    with pytest.raises(RecoveryError, match="float refused"):
        recovery_defect(((_Q(1), _Q(3)), (_Q(2), 0.5)))


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "python" / "src" / "linear_algebra" / "elimination.py"
    assert origin.is_file()
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:qm:matrix-column-recovery:v1" in source
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
        "empty columns admitted",
        "len(value) == 0",
        "len(value) == -1",
    ),
    (
        "height gate removed",
        "if len(value) != height:",
        "if False and len(value) != height:",
    ),
    (
        "column axis transposed",
        "return tuple(tuple(parsed[column][row] for column in range(width)) for row in range(width))",
        "return parsed",
    ),
    (
        "defect added instead of subtracted",
        "defect += abs(rebuilt[row][column] - _WITNESS[row][column])",
        "defect += abs(rebuilt[row][column] + _WITNESS[row][column])",
    ),
    (
        "defect gate inverted",
        "if defect != 0:",
        "if defect == 0:",
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


def _certificates_hold(recover_fn: object, defect_fn: object) -> bool:
    if not callable(recover_fn) or not callable(defect_fn):
        return False
    try:
        rebuilt = recover_fn(_COLUMNS)
        frozen = defect_fn()
        explicit = defect_fn(_COLUMNS)
    except Exception:
        return False
    return rebuilt == _MATRIX and frozen == 0 and explicit == 0


def _boundary_holds(recover_fn: object, defect_fn: object, error: type[BaseException]) -> bool:
    if not callable(recover_fn) or not callable(defect_fn):
        return False
    probes = (
        (lambda: defect_fn(((0.5, _Q(3)), _COLUMNS[1])), "float refused at the public boundary"),
        (lambda: recover_fn(((True, _Q(3)), _COLUMNS[1])), "boolean refused where an exact rational was required"),
        (lambda: recover_fn((("x", _Q(3)), _COLUMNS[1])), "matrix entry is not an exact rational"),
        (lambda: recover_fn(()), "columns are not a nonempty tuple"),
        (lambda: recover_fn(((_Q(1),), _COLUMNS[1])), "basis images do not match the dimension"),
        (lambda: defect_fn(((_Q(1), _Q(0)), (_Q(0), _Q(1)))), "recovery defect is not zero"),
    )
    return all(_invariant(error, probe) == invariant for probe, invariant in probes)


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["RecoveryError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _certificates_hold(namespace["recover"], namespace["recovery_defect"]):
        return False
    return _boundary_holds(namespace["recover"], namespace["recovery_defect"], error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_matrix_recovery_baseline")
        assert _oracle(_load_source(source, loaded[-1])) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_matrix_recovery_{index}"
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
