"""Exact tests for the QM-208 finite map: quadratic readout, Sorkin selection, interference.

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/quadratic_readout.py
Claim: quadratic_readout_control certificate locked by exact checks in this file
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases import holonomy_bridge_control as hbc
from finite_qm.use_cases import quadratic_readout_control as qrc

N = 12


@pytest.fixture(scope="module")
def control() -> dict:
    return qrc.evaluate_quadratic_readout_control(conductor=N)


def test_phase_blind_monomials_are_exactly_the_diagonal(control: dict) -> None:
    census = control["monomial_census"]
    assert census["monomials_examined"] == 14
    assert [tuple(m) for m in census["phase_blind"]] == [(1, 1), (2, 2)]
    assert census["blind_are_exactly_diagonal"]
    assert len(census["phase_sensitive"]) == 12


def test_sorkin_i3_selects_beta_zero_on_the_grid(control: dict) -> None:
    sel = control["sorkin_selection"]
    assert sel["selection_is_exactly_beta_zero"]
    assert len(sel["rows"]) == 16
    assert all(Fraction(str(b)) == 0 for _, b in sel["selected"])
    assert len(sel["selected"]) == 4
    assert control["quartic_i3_on_unit_triple_is_36"]
    assert str(control["quartic_i3_on_unit_triple"]) == "36"
    assert control["quadratic_i3_on_unit_triple_is_zero"]


def test_quartic_term_breaks_sorkin_on_the_unit_triple() -> None:
    one = hbc.root_of_unity(N, 0)
    rows = qrc.sorkin_selection(N, [(Fraction(1), Fraction(1))], [[one, one, one]])["rows"]
    assert rows[0]["i3_zero_on_all_triples"] is False
    assert str(rows[0]["i3_values"][0]) == "36"
    quadratic = qrc.sorkin_selection(N, [(Fraction(1), Fraction(0))], [[one, one, one]])["rows"]
    assert quadratic[0]["i3_zero_on_all_triples"] is True


def test_two_report_interference_is_born_weight_times_holonomy(control: dict) -> None:
    two = control["two_report_interference"]
    assert str(two["i2"]) == "1"
    assert two["holonomy_exponent"] == 10
    assert two["i2_equals_born_weight_times_two_re_holonomy"]
    assert two["i2_gauge_invariant"]
    assert two["holonomy_factorizes_through_cycle_invariants"]
    assert control["three_report_interference"]["quadratic_i3_zero"]


def test_quadratic_interferes_where_l1_is_additive(control: dict) -> None:
    inter = control["interference"]
    assert inter["quadratic_has_some_interference"]
    assert inter["l1_additive_on_all_pairs"]
    assert [str(r["i2_quadratic"]) for r in inter["rows"]][:3] == ["2", "-2", "0"]
    assert all(str(r["i2_l1"]) == "0" for r in inter["rows"])
    assert all(r["i2_equals_two_re_cross_term"] for r in inter["rows"])


def test_amplitudes_live_in_finite_extensions(control: dict) -> None:
    ext = control["amplitude_extensions"]
    assert ext["sqrt3_squared_is_3"]
    assert ext["weight_3_over_4_has_amplitude_in_q_zeta12"]
    assert ext["every_extension_is_finite"]
    assert [r["extension"] for r in ext["rows"]] == ["Q", "Q", "Q(sqrt(2))", "Q(sqrt(3/4))", "Q"]
    assert qrc.rational_square_root(Fraction(9, 16)) == Fraction(3, 4)
    assert qrc.rational_square_root(Fraction(2)) is None
    assert qrc.rational_square_root(Fraction(0)) == Fraction(0)


def test_ledger_has_three_layers(control: dict) -> None:
    ledger = control["residual_import_ledger"]
    assert [row["layer"] for row in ledger] == ["finite invariant", "completion", "residual import"]
    assert [row["status"] for row in ledger] == ["COMPUTED", "none needed", "IMPORTED"]
    assert "add-then-square" in ledger[2]["statement"]


def test_negative_refusals() -> None:
    with pytest.raises(qrc.ReadoutControlRefusal):
        qrc.monomial_readout(0, 0, N)
    with pytest.raises(qrc.ReadoutControlRefusal):
        qrc.phase_blind_monomial_census(N, N)
    with pytest.raises(qrc.ReadoutControlRefusal):
        qrc.evaluate_quadratic_readout_control(conductor=10)


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'quadratic_readout.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'quadratic_readout_control' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.quadratic_readout', 'finite_qm.use_cases.quadratic_readout', 'src.qm.campaigns.quadratic_readout_control', 'finite_qm.use_cases.quadratic_readout_control')
_USE_SHIM = True
_MUTANTS = (('monomial_readout:42', '    if a < 0 or b < 0 or a + b == 0:', '    if a < 1 or b < 0 or a + b == 0:'),)
_CHILD = '\nimport importlib\nimport importlib.util\nimport json\nimport sys\nimport tempfile\nfrom pathlib import Path\n\npayload = json.loads(sys.stdin.read())\nfor root in payload["roots"]:\n    if root not in sys.path:\n        sys.path.insert(0, root)\nif payload["shim"]:\n    import tests.conftest\nprimary = payload["modules"][0]\nreal = importlib.import_module(primary)\nspec = importlib.util.spec_from_loader(primary, loader=None)\nmodule = importlib.util.module_from_spec(spec)\nmodule.__package__ = real.__package__\nmodule.__file__ = payload["origin"]\nif hasattr(real, "__path__"):\n    module.__path__ = list(real.__path__)\nfor name in payload["modules"]:\n    sys.modules[name] = module\n    parent, _, child = name.rpartition(".")\n    if parent in sys.modules:\n        setattr(sys.modules[parent], child, module)\nexec(compile(payload["source"], payload["origin"], "exec"), module.__dict__)\ntest_spec = importlib.util.spec_from_file_location("certificate_probe", payload["test"])\ntest_mod = importlib.util.module_from_spec(test_spec)\ntest_spec.loader.exec_module(test_mod)\n\n\ndef _unwrap(fn):\n    wrapped = getattr(fn, "__wrapped__", None)\n    if callable(wrapped):\n        return wrapped\n    holder = getattr(fn, "__pytest_wrapped__", None)\n    obj = getattr(holder, "obj", None)\n    if callable(obj):\n        return obj\n    return fn\n\n\ndef _fixture(name):\n    if name == "tmp_path":\n        return Path(tempfile.mkdtemp())\n    fix = getattr(test_mod, name, None)\n    if not callable(fix):\n        return None\n    target = _unwrap(fix)\n    code = getattr(target, "__code__", None)\n    if code is None or code.co_argcount != 0:\n        return None\n    return target()\n\n\nran = 0\ntry:\n    for name in dir(test_mod):\n        if not name.startswith("test_"):\n            continue\n        if "mutation" in name:\n            continue\n        if name == "test_integration_origin_locks_the_source_module":\n            continue\n        fn = getattr(test_mod, name)\n        code = getattr(fn, "__code__", None)\n        if code is None:\n            continue\n        values = []\n        ready = True\n        for arg in code.co_varnames[: code.co_argcount]:\n            value = _fixture(arg)\n            if value is None:\n                ready = False\n                break\n            values.append(value)\n        if ready is False:\n            continue\n        fn(*values)\n        ran += 1\n    if ran == 0:\n        print("FAIL none")\n    else:\n        print("PASS " + str(ran))\nexcept Exception as exc:\n    print("FAIL " + type(exc).__name__)\n'

def _suite_passes(source: str) -> bool:
    payload = json.dumps({
        "modules": list(_ALIAS_NAMES),
        "source": source,
        "origin": str(_MODULE_PATH),
        "test": str(__import__("pathlib").Path(__file__).resolve()),
        "shim": _USE_SHIM,
        "roots": [str(__import__("pathlib").Path(__file__).resolve().parents[1]), str(__import__("pathlib").Path(__file__).resolve().parents[1] / "src")],
    })
    completed = subprocess.run(
        [sys.executable, "-c", _CHILD],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )
    lines = completed.stdout.strip().splitlines()
    status = lines[-1] if lines else ""
    return status.startswith("PASS")

def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    if _suite_passes(source) is False:
        raise AssertionError("baseline suite failed")
    killed = 0
    for name, old, new in _MUTANTS:
        if source.count(old) != 1:
            raise AssertionError(name)
        if _suite_passes(source.replace(old, new, 1)) is not False:
            raise AssertionError(name)
        killed += 1
    if killed != len(_MUTANTS):
        raise AssertionError(str(killed))
    record = f"Mutation-Kills: {killed} non-equivalent"
    if record not in __import__('pathlib').Path(__file__).read_text(encoding="utf-8"):
        raise AssertionError(record)
