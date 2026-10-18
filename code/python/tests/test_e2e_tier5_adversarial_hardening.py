"""Unit, integration, and negative tests for exact Born purity.

Origin: code/python/src/qm/campaigns/born_normalization.py
Claim: the rational weights 1/4 and 3/4 have exact purity 5/8.
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

import ast
from fractions import Fraction
from pathlib import Path

import pytest

from finite_qm.api import claims, is_native_available, list_suites, run_suite
from src.qm.campaigns.born_normalization import exact_born_purity
from src.qm.campaigns.stabilizer_codes import (
    build_steane_seven_qubit_code,
    build_three_qubit_bitflip_code,
)


def test_unit_exact_born_purity() -> None:
    purity = exact_born_purity((Fraction(1, 4), Fraction(3, 4)))
    assert purity == Fraction(5, 8)
    assert type(purity) is Fraction


def test_negative_born_purity_refuses_bad_mass() -> None:
    with pytest.raises(ValueError, match="non-negative") as negative:
        exact_born_purity((Fraction(-1), Fraction(2)))
    assert type(negative.value) is ValueError
    with pytest.raises(ValueError, match="positive sum") as empty:
        exact_born_purity((Fraction(0), Fraction(0)))
    assert type(empty.value) is ValueError


def test_integration_syndromes_and_claims() -> None:
    report = build_three_qubit_bitflip_code()
    assert report["syndromes"]["X0"] == (-1, 1)
    steane = build_steane_seven_qubit_code()
    assert steane["unique_error_syndromes_count"] == 21
    ledger = claims("qm122")
    assert ledger["schema_version"] == 1
    assert ledger["authority_effect"] == "None"
    assert len(ledger["claims"]) == 66
    assert is_native_available() is False
    suites = list_suites()
    assert len(suites) == 12


def test_negative_claims_and_suite() -> None:
    with pytest.raises(ValueError, match="UNKNOWN_PAPER:unknown_paper") as unknown:
        claims("unknown_paper")
    assert type(unknown.value) is ValueError
    with pytest.raises(RuntimeError, match="Native acceleration engine") as native:
        run_suite("c750")
    assert type(native.value) is RuntimeError


def _domain_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "src" / "qm" / "domain"


def _import_parts(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, ast.Import):
        return tuple(alias.name.split(".")[0] for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        if node.module is None:
            return ()
        return tuple(node.module.split("."))
    return ()


def _file_avoids_outer(path: Path, forbidden: frozenset[str]) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        for part in _import_parts(node):
            if part in forbidden:
                return False
    return True


def test_integration_domain_modules_avoid_outer_layers() -> None:
    domain_dir = _domain_dir()
    py_files = list(domain_dir.glob("*.py"))
    assert len(py_files) >= 5
    forbidden = frozenset({"use_cases", "infrastructure", "cli", "api", "entrypoints"})
    for py_file in py_files:
        assert _file_avoids_outer(py_file, forbidden) is True


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'born_normalization.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'exact_born_purity' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.born_normalization',)
_USE_SHIM = True
_MUTANTS = (('exact_born_purity:25', '    if any(value < 0 for value in values):', '    if any(value < 1 for value in values):'),)
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
