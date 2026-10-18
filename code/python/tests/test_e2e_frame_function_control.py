"""Exact tests for the QM-210 finite map: Born pairing on finite frame sets.

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/frame_function.py
Claim: frame_function_control certificate locked by exact checks in this file
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases import frame_function_control as ffc


@pytest.fixture(scope="module")
def control() -> dict:
    return ffc.evaluate_frame_function_control()


def test_unit_cabello_frame_set_shape(control: dict) -> None:
    fs = control["frame_set"]
    assert fs["dimension"] == 4 and fs["basis_count"] == 9 and fs["ray_count"] == 18
    assert fs["all_bases_orthogonal"]
    assert fs["every_ray_in_exactly_two_bases"]


def test_frame_identity_holds_for_trace_one_forms(control: dict) -> None:
    assert control["frame_identity"] == {
        "maximally_mixed": True,
        "pure_state": True,
        "generic_trace_one": True,
    }


def test_linear_gleason_nullity_is_zero_on_every_prefix(control: dict) -> None:
    by_prefix = control["gleason_nullity_by_prefix"]
    expected = {
        3: (10, 3, 7, 7, 8),
        6: (15, 6, 9, 9, 10),
        9: (18, 9, 9, 9, 10),
    }
    for k, (rays, rank, affine, quantum, span) in expected.items():
        g = by_prefix[k]
        assert g["ray_count"] == rays
        assert g["constraint_rank_q"] == rank
        assert g["frame_function_affine_dimension"] == affine
        assert g["quantum_affine_dimension"] == quantum
        assert g["quantum_linear_span_dimension"] == span
        assert g["nullity"] == 0 and g["finite_gleason_holds"]


def test_parity_obstruction_and_colorability_prefix(control: dict) -> None:
    par = control["parity_obstruction"]
    assert par["basis_count"] == 9 and par["f2_rank"] == 8
    assert par["f2_system_consistent"] is False
    assert par["two_valued_function_by_search"] is False
    col = control["colorability"]
    assert col["first_uncolorable_prefix"] == 9
    assert [p["two_valued_exists"] for p in col["profile"]] == [True] * 8 + [False]


def test_eight_bases_still_admit_a_two_valued_frame_function() -> None:
    bases = ffc.CABELLO_BASES[:8]
    f = ffc.two_valued_frame_function(bases)
    assert f is not None
    rays = ffc.rays_of(bases)
    assert all(sum(f[ffc.ray_index(rays, v)] for v in b) == 1 for b in bases)
    assert ffc.parity_obstruction(bases)["f2_system_consistent"] is True


def test_positivity_gap_witness_on_both_frame_sets(control: dict) -> None:
    for gap in (control["positivity_gap"], control["peres_24"]["positivity_gap"]):
        assert gap["trace_one"] and gap["frame_identity_holds"]
        assert gap["nonnegative_on_every_ray"]
        assert gap["positive_semidefinite"] is False
        assert gap["negative_direction"] == [2, 1, 0, 0]
        assert gap["value_on_negative_direction"] == "-1/2"
        assert gap["witness_is_a_gap"]
    pure = [[Fraction(1) if i == j == 0 else Fraction(0) for j in range(4)] for i in range(4)]
    assert ffc.principal_minors_nonnegative(pure)
    assert ffc.quadratic_form(pure, (2, 1, 0, 0)) == 4


def test_peres_24_ray_set(control: dict) -> None:
    peres = control["peres_24"]
    assert peres["frame_set"]["basis_count"] == 24 and peres["frame_set"]["ray_count"] == 24
    assert peres["frame_set"]["ray_multiplicities"] == [4] * 24
    assert peres["frame_set"]["every_ray_in_exactly_two_bases"] is False
    g = peres["gleason_nullity"]
    assert (g["constraint_rank_q"], g["frame_function_affine_dimension"], g["nullity"]) == (
        15,
        9,
        0,
    )
    par = peres["parity_obstruction"]
    assert par["f2_rank"] == 14 and par["f2_system_consistent"] is False
    assert par["two_valued_function_by_search"] is False


def test_negative_tampered_basis_is_detected() -> None:
    tampered = list(ffc.CABELLO_BASES)
    tampered[0] = ((0, 0, 0, 1), (0, 0, 1, 1), (1, 1, 0, 0), (1, -1, 0, 0))
    assert ffc.frame_set_checks(tampered)["all_bases_orthogonal"] is False
    with pytest.raises(ffc.FrameControlRefusal):
        ffc.ray_index(ffc.rays_of(ffc.CABELLO_BASES), (1, 2, 3, 4))


def test_ledger_has_three_layers(control: dict) -> None:
    ledger = control["residual_import_ledger"]
    assert [row["layer"] for row in ledger] == ["finite invariant", "completion", "residual import"]
    assert [row["status"] for row in ledger] == ["COMPUTED", "IMPORTED", "IMPORTED"]
    assert "nullity zero" in ledger[0]["statement"]
    assert "Positivity" in ledger[2]["statement"]


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'frame_function.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'frame_function_control' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.frame_function', 'finite_qm.use_cases.frame_function', 'src.qm.campaigns.frame_function_control', 'finite_qm.use_cases.frame_function_control')
_USE_SHIM = True
_MUTANTS = (('two_valued_frame_function:203', '            return True', '            return False'),)
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
