"""End-to-end verification tests for the Four-Wall Finite Reconstruction & Positivity
Boundary Theorem and the 5-Stage Operadic Ecology (pilot_051..055) of Finite QM.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/four_wall_operad.py
Claim: evaluate_four_wall_reconstruction_and_operad_control certificate locked by exact checks in this file
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

from finite_qm.use_cases.four_wall_reconstruction_and_operad_control import (
    evaluate_four_wall_reconstruction_and_operad_control,
    evaluate_wall1_busch_ic_povm_vs_polyhedral_cone,
    evaluate_wall2_galois_sos_total_positivity,
    evaluate_wall3_cocycle_and_choi_separation,
    evaluate_wall4_cayley_and_entropy_enclosure,
)


def test_wall1_busch_ic_povm_and_polyhedral_cone_separation() -> None:
    audit = evaluate_wall1_busch_ic_povm_vs_polyhedral_cone()
    assert audit.trace_sum_equals_two
    assert audit.bloch_sum_vanishes
    assert audit.all_effects_psd
    assert audit.reconstruction_determinant == Fraction(9, 1000)
    assert audit.reconstruction_invertible
    assert audit.polyhedral_cabello_peres_minor == Fraction(-1, 16)
    assert audit.polyhedral_cone_strictly_larger_than_psd
    assert audit.reconstructed_pythagorean_state_trace == Fraction(1, 1)
    assert audit.reconstructed_pythagorean_state_det == Fraction(108, 625)
    assert audit.cholesky_sos_verified


def test_wall2_galois_conjugate_negativity_vs_sos_total_positivity() -> None:
    audit = evaluate_wall2_galois_sos_total_positivity()
    assert audit.twist_trace_rational == Fraction(1, 1)
    assert audit.twist_trace_sqrt5 == Fraction(0, 1)
    assert audit.twist_det_rational == Fraction(-1, 8)
    assert audit.twist_det_sqrt5 == Fraction(1, 8)
    assert audit.twist_det_field_norm == Fraction(-1, 16)
    assert audit.twist_fails_conjugate_embedding
    assert audit.sos_trace_rational == Fraction(1, 1)
    assert audit.sos_trace_sqrt5 == Fraction(0, 1)
    assert audit.sos_det_rational == Fraction(1, 9)
    assert audit.sos_det_sqrt5 == Fraction(0, 1)
    assert audit.sos_det_field_norm == Fraction(1, 81)
    assert audit.sos_factor_identity_holds
    assert audit.sos_psd_in_all_galois_embeddings


def test_wall3_char2_cocycle_and_choi_transpose_separation() -> None:
    audit = evaluate_wall3_cocycle_and_choi_separation()
    assert audit.inv2_mod3 == 1
    assert audit.two_mod2 == 0
    assert audit.odd_prime_half_invertible
    assert audit.char2_half_obstructed
    assert audit.mermin_peres_cocycle_ratio == -1
    assert audit.choi_transpose_singlet_expectation == Fraction(-1, 2)
    assert audit.choi_identity_singlet_expectation == Fraction(0, 1)
    assert audit.choi_identity_bell_expectation == Fraction(1, 1)
    assert audit.choi_separates_positive_witness_from_cptp


def test_wall4_cayley_unitarity_and_entropy_interval_enclosure() -> None:
    audit = evaluate_wall4_cayley_and_entropy_enclosure()
    assert audit.cayley_single_unitarity_defect == Fraction(0, 1)
    assert audit.strang_cayley_split_unitarity_defect == Fraction(0, 1)
    assert audit.taylor_first_order_norm_sq == Fraction(5, 4)
    assert audit.taylor_violates_unitarity
    assert audit.renyi_p2 == Fraction(337, 625)
    assert audit.renyi_p3 == Fraction(193, 625)
    assert audit.renyi_p4 == Fraction(72097, 390625)
    assert audit.interval_width_below_1e_12


def test_five_stage_operad_ecology_complete() -> None:
    report = evaluate_four_wall_reconstruction_and_operad_control()
    assert report.all_four_walls_and_five_stages_verified
    assert len(report.operad_stages) == 5
    pilot_ids = [s.pilot_id for s in report.operad_stages]
    assert pilot_ids == ["pilot_051", "pilot_052", "pilot_053", "pilot_054", "pilot_055"]
    operad_symbols = [s.operad_symbol for s in report.operad_stages]
    assert operad_symbols == ["B_Polar", "O_Gal", "O_{H^2}", "O_Strat", "Op_FQM"]
    for stage in report.operad_stages:
        assert stage.verified
        assert stage.antibody_id.startswith("AB_FQM_05")
        assert stage.rule_id.startswith("RULE_FQM_05")
        assert stage.anti_rule_id.startswith("ANTIRULE_FQM_05")
        assert stage.anti_pattern_id.startswith("AP_MATH_02")
        assert stage.helpful_pattern_id.startswith("HP_MATH_02")
        assert stage.agent_id.startswith("AGENT_FQM_05")
        assert stage.anti_agent_id.startswith("ANTIAGENT_FQM_05")


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'four_wall_operad.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'evaluate_four_wall_reconstruction_and_operad_control' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.four_wall_operad', 'finite_qm.use_cases.four_wall_operad', 'src.qm.campaigns.four_wall_reconstruction_and_operad_control', 'finite_qm.use_cases.four_wall_reconstruction_and_operad_control')
_USE_SHIM = True
_MUTANTS = (('evaluate_wall1_busch_ic_povm_vs_polyhedral_cone:161', '        (Fraction(3, 5), Fraction(0, 1), Fraction(4, 5)),', '        (Fraction(4, 5), Fraction(0, 1), Fraction(4, 5)),'),)
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
