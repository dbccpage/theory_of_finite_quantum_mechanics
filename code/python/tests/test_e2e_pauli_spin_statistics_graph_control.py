"""E2E tests for QM-223 Pauli exclusion and topological spin-statistics on finite graphs.

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/pauli_spin_stat.py
Claim: analyze_conf2_graph certificate locked by exact checks in this file
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

from finite_qm.use_cases.pauli_spin_statistics_graph_control import (
    analyze_conf2_graph,
    build_pauli_spin_statistics_certificate,
    orbital_slater_or_permanent,
    verify_two_mode_jordan_wigner_car,
)


def test_unit_qm223_certificate_passes_all_finite_spin_statistics_checks() -> None:
    cert = build_pauli_spin_statistics_certificate()
    assert cert.passed is True
    assert cert.control_id == "QM-223"
    assert cert.conf2_p3.conf2_betti_1 == 0
    assert cert.conf2_p3.conf2_z2_torsion_rank == 0
    assert cert.conf2_y_star is not None
    assert cert.conf2_y_star.conf2_betti_1 == 1
    assert cert.conf2_y_star.conf2_squares == 0
    assert cert.conf2_y_star.conf2_z2_torsion_rank == 0
    assert cert.conf2_y_star.has_y_junction_exchange_cycle is False
    assert cert.conf2_c4.conf2_betti_1 == 3
    assert cert.conf2_c4.conf2_squares == 2
    assert cert.conf2_c4.conf2_2complex_betti_1_q == 1
    assert cert.conf2_c4.has_y_junction_exchange_cycle is False
    assert cert.conf2_k4 is not None
    assert cert.conf2_k4.conf2_betti_1 == 7
    assert cert.conf2_k4.conf2_squares == 3
    assert cert.conf2_k4.conf2_2complex_betti_1_q == 4
    assert cert.conf2_k4.conf2_z2_torsion_rank == 0
    assert cert.conf2_k4.has_y_junction_exchange_cycle is False
    assert cert.conf2_k5.conf2_betti_1 == 21
    assert cert.conf2_k5.conf2_squares == 15
    assert cert.conf2_k5.conf2_2complex_betti_1_q == 6
    assert cert.conf2_k5.conf2_2complex_betti_1_f2 == 7
    assert cert.conf2_k5.conf2_z2_torsion_rank == 1
    assert cert.conf2_k5.has_y_junction_exchange_cycle is True
    assert cert.pauli_same_orbital_slater == Fraction(0)
    assert cert.swap_ratio_fermion == Fraction(-1)
    assert cert.swap_ratio_boson == Fraction(1)
    assert cert.fermi_hole_coincidence_probability == Fraction(0)
    assert cert.hbt_boson_bunching_ratio == Fraction(2)
    assert cert.shell_orbital_degeneracies_1_to_4 == (1, 4, 9, 16)
    assert cert.shell_capacities_1_to_4 == (2, 8, 18, 32)
    assert cert.noble_gas_atomic_numbers == (2, 10, 18, 36, 54, 86, 118)


def test_qm223_three_particle_slater_antisymmetry_and_duplicate_orbital_exclusion() -> None:
    r1 = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)]
    r2 = [Fraction(2, 5), Fraction(3, 5), Fraction(1, 5)]
    r3 = [Fraction(3, 7), Fraction(2, 7), Fraction(4, 7)]

    assert orbital_slater_or_permanent([r1, r1, r2], alternating=True) == Fraction(0)

    det_123 = orbital_slater_or_permanent([r1, r2, r3], alternating=True)
    det_213 = orbital_slater_or_permanent([r2, r1, r3], alternating=True)
    assert det_213 == -det_123
    assert det_123 != Fraction(0)

    perm_123 = orbital_slater_or_permanent([r1, r2, r3], alternating=False)
    perm_213 = orbital_slater_or_permanent([r2, r1, r3], alternating=False)
    assert perm_213 == perm_123


def test_qm223_jordan_wigner_car_nilpotency_and_fock_trace() -> None:
    nilpotent, car_exact, tr_sum = verify_two_mode_jordan_wigner_car()
    assert nilpotent is True
    assert car_exact is True
    assert tr_sum == Fraction(4)


def test_qm223_planar_theta_vs_nonplanar_k33_2complex_torsion() -> None:
    theta4 = analyze_conf2_graph("Theta_4", 4, [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])
    assert theta4.conf2_vertices == 6
    assert theta4.conf2_edges == 10
    assert theta4.conf2_betti_1 == 5
    assert theta4.conf2_squares == 2
    assert theta4.conf2_2complex_betti_1_q == 3
    assert theta4.conf2_z2_torsion_rank == 0
    assert theta4.has_y_junction_exchange_cycle is False
    assert theta4.admissible_1d_exchange_characters == ("BRAID_U1_CYCLOTOMIC_PHASE",)

    k33_edges = [(u, v) for u in range(3) for v in range(3, 6)]
    k33 = analyze_conf2_graph("K_3_3", 6, k33_edges)
    assert k33.conf2_z2_torsion_rank == 1
    assert k33.has_y_junction_exchange_cycle is True
    assert k33.admissible_1d_exchange_characters == ("+1_BOSON", "-1_FERMION")


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'pauli_spin_stat.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'analyze_conf2_graph' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.pauli_spin_stat', 'finite_qm.use_cases.pauli_spin_stat', 'src.qm.campaigns.pauli_spin_statistics_graph_control', 'finite_qm.use_cases.pauli_spin_statistics_graph_control')
_USE_SHIM = True
_MUTANTS = (('verify_two_mode_jordan_wigner_car:282', '        return [[m[r][c] for r in range(4)] for c in range(4)]', '        return [[m[r][c] for r in range(5)] for c in range(4)]'),)
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
