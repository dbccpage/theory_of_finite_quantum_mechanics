"""Unit, integration, end-to-end, negative, and mutation checks for the QM-122 dual.

Origin: papers/foundations/finite_ledger.md claim QM-122-C38.
Claim: urn:omega:fqm:qm122:python-dual-falsification:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/foundations/_code/qm_122/tests/test_qm122_dual.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 10; AST Sonar cognitive complexity max 6; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: A killed mutant certifies this dual harness. It does not prove Gleason or recover M_n(C).
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import cast

import pytest

_PKG = Path(__file__).resolve().parents[1] / 'src'
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from qm122_lib import exported_reversible_report_count
from qm122_lib.qm122_dual import (
    Qm122DualError,
    bool_reversibles,
    collapse,
    delta,
    dump_right,
    gmul,
    identity_dilations,
    mix,
    one_plus_i_not_unit,
    psi1,
    psi2,
    qm122_dual_receipt,
    tensor,
    toggle,
    total_weight,
)

_DUAL = _PKG / "qm122_lib" / "qm122_dual.py"
_INIT = _PKG / "qm122_lib" / "__init__.py"
_LOADED: list[str] = []

_DUAL_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("collapse", "collapsed = " + "False", "collapsed = True"),
    ("toggle", "return not " + "report", "return report"),
    ("product", "return (ar * br - ai * bi, ar * bi + ai * br)", "return (1, 0)"),
    ("mix", "vf[0] - vt[0]", "vf[0] + vt[0]"),
    ("dump", "return left[report] * (right[False] + right[True])", "return left[report] * right[ancilla]"),
    ("double", "2 * receipt.weight_psi1", "3 * receipt.weight_psi1"),
    ("float", "isinstance(value, " + "float)", "isinstance(value, complex)"),
    ("census", "receipt.reversible_reports, 2", "receipt.reversible_reports, 3"),
)

_INIT_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("export type", "type(count) is not " + "int", "type(count) is not bool"),
    ("export width", "count != " + "2", "count != 3"),
    ("export return", "return count", "return count + 1"),
)

_HARNESS_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("hand mix", "mixed != 2 * " + "weight", "mixed != 3 * weight"),
    ("hand float", "type(value) is " + "float", "type(value) is complex"),
    ("hand bool", "type(value) is " + "bool", "type(value) is int"),
    ("hand gmul", "real * other_real - imag * " + "other_imag", "0"),
)


class Qm122HarnessError(ValueError):
    """One violated dual-harness invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: dict[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> Qm122HarnessError:
    return Qm122HarnessError(invariant, parameters)


def _hand_int(value: object, role: str) -> int:
    if type(value) is float:
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer weight was required", role=role)
    if type(value) is int:
        return value
    raise _fail("value is not an exact integer", role=role, received=type(value).__name__)


def _hand_gmul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    real, imag = left
    other_real, other_imag = right
    return (real * other_real - imag * other_imag, real * other_imag + imag * other_real)


def independent_psi_mix_total(witness: tuple[tuple[int, int], tuple[int, int]]) -> int:
    """Hand total of |a+b|^2 + |a-b|^2 for one exhibited Gaussian pair."""
    left, right = witness
    mixed_false = _hand_gmul((1, 0), (_hand_int(left[0] + right[0], "sum.re"), _hand_int(left[1] + right[1], "sum.im")))
    mixed_true_real = left[0] - right[0]
    mixed_true_imag = left[1] - right[1]
    weight = left[0] * left[0] + left[1] * left[1] + right[0] * right[0] + right[1] * right[1]
    mixed = (
        mixed_false[0] * mixed_false[0]
        + mixed_false[1] * mixed_false[1]
        + mixed_true_real * mixed_true_real
        + mixed_true_imag * mixed_true_imag
    )
    if mixed != 2 * weight:
        raise _fail("hand mix total did not double", mixed=mixed, weight=weight)
    return mixed


def test_unit_report_census() -> None:
    assert collapse(False) is False
    assert collapse(True) is False
    assert toggle(False) is True
    assert toggle(True) is False
    assert len(bool_reversibles()) == 2
    assert len(identity_dilations()) == 4
    assert one_plus_i_not_unit() is True


def test_unit_gauss_witnesses_match_hand_total() -> None:
    assert total_weight(psi1()) == 2
    assert total_weight(psi2()) == 2
    assert total_weight(mix(psi1())) == independent_psi_mix_total(((1, 0), (1, 0)))
    assert total_weight(mix(psi2())) == independent_psi_mix_total(((1, 0), (-1, 0)))
    assert gmul((1, 1), (1, 0)) == (1, 1)
    assert delta(False) == {False: 1, True: 0}


def test_integration_dump_tensor_and_package_export() -> None:
    weights_u = {False: 1, True: 0}
    weights_v = {False: 0, True: 1}
    assert dump_right(weights_u, weights_v, (False, False)) != tensor(weights_u, weights_v, (False, False))
    assert exported_reversible_report_count() == len(bool_reversibles())


def test_e2e_named_receipt() -> None:
    receipt = qm122_dual_receipt()
    assert receipt.reversible_reports == 2
    assert receipt.identity_dilations == 4
    assert receipt.collapse_dilations == 4
    assert receipt.one_plus_i_blocked is True
    assert receipt.dump_disagrees is True
    assert receipt.no_half_step is True
    assert receipt.mix_psi1 == 4
    assert receipt.mix_psi2 == 4
    assert exported_reversible_report_count() == 2


def test_negative_boundary_refusals() -> None:
    with pytest.raises(Qm122DualError, match="float refused") as floated:
        gmul((1.5, 0), (1, 0))
    assert floated.value.parameters["role"] == "left.re"
    with pytest.raises(Qm122DualError, match="boolean refused"):
        gmul((True, 0), (1, 0))
    with pytest.raises(Qm122DualError, match="report is not a boolean"):
        collapse(1)
    with pytest.raises(Qm122DualError, match="not a report boolean"):
        dump_right({0: 1, 1: 0}, {False: 1, True: 0}, (False, False))
    with pytest.raises(Qm122HarnessError, match="float refused"):
        _hand_int(1.5, "probe")
    with pytest.raises(Qm122HarnessError, match="boolean refused"):
        _hand_int(True, "probe")


def _load_source(source: str, name: str) -> ModuleType:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise _fail("source spec was not created", module=name)
    module = ModuleType(name)
    module.__spec__ = spec
    module.__file__ = name + ".py"
    if name.startswith("qinit"):
        module.__package__ = "qm122_lib"
    sys.modules[name] = module
    _LOADED.append(name)
    exec(compile(source, name + ".py", "exec"), module.__dict__)
    return module


def _callable(namespace: dict[str, object], name: str) -> Callable[..., object] | None:
    value = namespace.get(name)
    if not callable(value):
        return None
    return cast(Callable[..., object], value)


def _error_type(error: object) -> type[BaseException] | None:
    if isinstance(error, type) and issubclass(error, BaseException):
        return error
    return None


def _raised_invariant(error: object, probe: Callable[[], object]) -> str:
    kind = _error_type(error)
    if kind is None:
        return ""
    try:
        probe()
    except kind as caught:
        invariant = getattr(caught, "invariant", "")
        if isinstance(invariant, str):
            return invariant
    return ""


def _dual_surface(namespace: dict[str, object]) -> bool:
    collapse_fn = _callable(namespace, "collapse")
    dump_fn = _callable(namespace, "dump_right")
    tensor_fn = _callable(namespace, "tensor")
    if collapse_fn is None or dump_fn is None or tensor_fn is None:
        return False
    if collapse_fn(False) is not False or collapse_fn(True) is not False:
        return False
    weights_u = {False: 1, True: 0}
    weights_v = {False: 0, True: 1}
    dumped = dump_fn(weights_u, weights_v, (False, False))
    multiplied = tensor_fn(weights_u, weights_v, (False, False))
    return dumped != multiplied


def _dual_receipt_ok(namespace: dict[str, object]) -> bool:
    receipt_fn = _callable(namespace, "qm122_dual_receipt")
    if receipt_fn is None:
        return False
    receipt = receipt_fn()
    if getattr(receipt, "reversible_reports") != 2:
        return False
    if getattr(receipt, "mix_psi1") != 4:
        return False
    if getattr(receipt, "collapse_dilations") != 4:
        return False
    return getattr(receipt, "no_half_step") is True


def _dual_float_refused(namespace: dict[str, object]) -> bool:
    gmul_fn = _callable(namespace, "gmul")
    if gmul_fn is None:
        return False
    invariant = _raised_invariant(namespace.get("Qm122DualError"), lambda: gmul_fn((1.5, 0), (1, 0)))
    return invariant == "float refused at the public boundary"


def _dual_oracle(namespace: dict[str, object]) -> bool:
    if not _dual_surface(namespace):
        return False
    if not _dual_receipt_ok(namespace):
        return False
    return _dual_float_refused(namespace)


def _init_oracle(namespace: dict[str, object]) -> bool:
    exported = _callable(namespace, "exported_reversible_report_count")
    if exported is None:
        return False
    return exported() == 2


def _harness_oracle(namespace: dict[str, object]) -> bool:
    pairing = _callable(namespace, "independent_psi_mix_total")
    hand = _callable(namespace, "_hand_int")
    if pairing is None or hand is None:
        return False
    if pairing(((1, 0), (1, 0))) != 4:
        return False
    error = namespace.get("Qm122HarnessError")
    floated = _raised_invariant(error, lambda: hand(1.5, "probe"))
    if floated != "float refused at the public boundary":
        return False
    boolean = _raised_invariant(error, lambda: hand(True, "probe"))
    return boolean == "boolean refused where an integer weight was required"


def _survived(source: str, name: str, oracle: Callable[[dict[str, object]], bool]) -> bool:
    try:
        loaded = _load_source(source, name)
        return oracle(loaded.__dict__)
    except Exception:
        return False


def _kill(source: str, mutants: tuple[tuple[str, str, str], ...], oracle: Callable[[dict[str, object]], bool], label: str) -> int:
    killed = 0
    for index, (name, old, new) in enumerate(mutants):
        count = source.count(old)
        if count != 1:
            raise _fail("mutant site was not unique", mutant=name, count=count, label=label)
        if _survived(source.replace(old, new, 1), f"{label}_{index}", oracle):
            raise _fail("mutant survived", mutant=name, label=label)
        killed += 1
    return killed


def test_mutation_suite_kills_dual_export_and_harness() -> None:
    dual = _DUAL.read_text(encoding="utf-8")
    init_source = _INIT.read_text(encoding="utf-8")
    harness = Path(__file__).read_text(encoding="utf-8")
    assert _dual_oracle(_load_source(dual, "qm122_dual_baseline").__dict__) is True
    dual_kills = _kill(dual, _DUAL_MUTANTS, _dual_oracle, "dual")
    init_kills = _kill(init_source, _INIT_MUTANTS, _init_oracle, "qinit")
    harness_kills = _kill(harness, _HARNESS_MUTANTS, _harness_oracle, "qharness")
    assert dual_kills == 8
    assert init_kills == 3
    assert harness_kills == 4
    assert "Mutation-Kills: 8 non-equivalent" in dual
    assert "Mutation-Kills: 3 non-equivalent" in init_source
    assert "Mutation-Kills: 4 non-equivalent" in harness


def teardown_module() -> None:
    for name in _LOADED:
        sys.modules.pop(name, None)
