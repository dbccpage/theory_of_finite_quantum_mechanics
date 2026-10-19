"""E2E tests for QM-224 (Hydrogen Dirac-Coulomb fine structure & 1-loop QED Lamb shift)
and QM-225 (Helium variational / Hylleraas ground state, 1s2s ortho/para exchange
splitting, and closed-shell Roothaan-Hartree-Fock contraction for Z=2..10 over Q).

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/atomic_dirac.py
Claim: RationalIntervalQ certificate locked by exact checks in this file
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from finite_qm.use_cases.atomic_dirac_lamb_hartree_fock_control import (
    RationalIntervalQ,
    build_qm224_dirac_lamb_certificate,
    build_qm225_helium_rhf_certificate,
    dirac_coulomb_alpha4_coeff,
    evaluate_helium_1s2s_ortho_para_splitting,
    evaluate_helium_hylleraas_secular_over_q,
    evaluate_helium_variational_polynomial,
    run_closed_shell_rhf_scf,
)


def test_unit_qm224_dirac_coulomb_fine_structure_and_j_half_degeneracy() -> None:
    cert = build_qm224_dirac_lamb_certificate()
    assert cert.passed is True
    assert cert.control_id == "QM-224"

    assert cert.c4_1s_half == Fraction(1, 8)
    assert cert.c4_2s_half == Fraction(5, 128)
    assert cert.c4_2p_half == Fraction(5, 128)
    assert cert.c4_2p_three_half == Fraction(1, 128)

    assert cert.c4_2s_rel_kinetic + cert.c4_2s_darwin == Fraction(5, 128)
    assert cert.c4_2p_rel_kinetic + cert.c4_2p_half_spin_orbit == Fraction(5, 128)
    assert cert.c4_2p_rel_kinetic + cert.c4_2p_three_half_spin_orbit == Fraction(1, 128)
    assert cert.dirac_j_half_degeneracy_exact is True

    assert cert.fine_structure_2p_coeff_mc2 == Fraction(1, 32)
    assert cert.fine_structure_2p_coeff_rydberg == Fraction(1, 16)
    assert RationalIntervalQ(Fraction(1_094_928, 100), Fraction(1_094_929, 100)).contains(
        cert.fine_structure_2p_leading_mhz_interval
    )
    assert cert.fine_structure_2p_qed_mhz_interval.contains(Fraction(1_096_905, 100))


def test_qm224_one_loop_qed_lamb_shift_lifts_degeneracy_and_encloses_lundeen_pipkin() -> None:
    cert = build_qm224_dirac_lamb_certificate()
    assert cert.lamb_uehling_vp_coeff_4pi == Fraction(-4, 15)
    assert cert.lamb_uehling_vp_coeff_6pi == Fraction(-1, 5)
    assert cert.lamb_self_energy_plus_vp_coeff == Fraction(19, 30)
    assert cert.lamb_magnetic_moment_2s_minus_2p_coeff == Fraction(1, 8)
    assert cert.lamb_total_contact_coeff == Fraction(91, 120)

    assert cert.bethe_log_diff_interval == RationalIntervalQ(
        Fraction(2_841_786, 1_000_000), Fraction(2_841_787, 1_000_000)
    )
    assert RationalIntervalQ(Fraction(105_219, 100), Fraction(105_220, 100)).contains(
        cert.lamb_1loop_mhz_interval
    )
    assert RationalIntervalQ(Fraction(105_770, 100), Fraction(105_795, 100)).contains(
        cert.lamb_full_mhz_interval
    )
    assert cert.lundeen_pipkin_benchmark_mhz == Fraction(211_569, 200)
    assert cert.lundeen_pipkin_enclosed is True

    assert dirac_coulomb_alpha4_coeff(3, 1) == Fraction(1, 72)
    assert dirac_coulomb_alpha4_coeff(3, 3) == Fraction(1, 216)
    assert dirac_coulomb_alpha4_coeff(3, 5) == Fraction(1, 648)


def test_qm225_helium_variational_kellner_minimum_and_hylleraas_secular_bounds() -> None:
    cert = build_qm225_helium_rhf_certificate()
    assert cert.passed is True
    assert cert.control_id == "QM-225"

    assert cert.helium_bare_z2.z_eff == Fraction(2, 1)
    assert cert.helium_bare_z2.kinetic_eh == Fraction(4, 1)
    assert cert.helium_bare_z2.nuclear_attraction_eh == Fraction(-8, 1)
    assert cert.helium_bare_z2.electron_repulsion_eh == Fraction(5, 4)
    assert cert.helium_bare_z2.total_energy_eh == Fraction(-11, 4)

    assert cert.helium_kellner_opt.z_eff == Fraction(27, 16)
    assert cert.helium_kellner_opt.total_energy_eh == Fraction(-729, 256)
    assert cert.helium_kellner_opt.virial_residual_2t_plus_v == Fraction(0)
    assert cert.helium_kellner_opt.square_completion_excess_eh == Fraction(0)

    for z_test in (Fraction(1, 1), Fraction(3, 2), Fraction(7, 4), Fraction(2, 1)):
        ev = evaluate_helium_variational_polynomial(z_test)
        assert ev.total_energy_eh - Fraction(-729, 256) == (z_test - Fraction(27, 16)) ** 2

    hyll = evaluate_helium_hylleraas_secular_over_q()
    assert hyll.scale_zeta == Fraction(29, 16)
    assert hyll.overlap_s_4x4[0][0] == Fraction(1, 1)
    assert hyll.kinetic_m_4x4[0][0] == Fraction(1, 1)
    assert hyll.potential_l_4x4[0][0] == Fraction(27, 8)
    assert hyll.target_enclosure_eh.contains(hyll.rayleigh_energy_3term_eh)
    assert hyll.target_enclosure_eh.contains(hyll.rayleigh_energy_4term_eh)
    assert hyll.rayleigh_energy_4term_eh < hyll.rayleigh_energy_3term_eh < Fraction(-729, 256)
    rel_err_4term = abs(
        (hyll.rayleigh_energy_4term_eh - hyll.pekeris_benchmark_eh) / hyll.pekeris_benchmark_eh
    )
    assert rel_err_4term < Fraction(5, 10_000)


def test_qm225_helium_1s2s_ortho_para_exchange_and_closed_shell_rhf_contraction() -> None:
    ortho_para = evaluate_helium_1s2s_ortho_para_splitting(2)
    assert ortho_para.unperturbed_1s2s_eh == Fraction(-5, 2)
    assert ortho_para.direct_coulomb_j1s2s_eh == Fraction(34, 81)
    assert ortho_para.exchange_integral_k1s2s_eh == Fraction(32, 729)
    assert ortho_para.triplet_ortho_3s1_eh == Fraction(-3097, 1458)
    assert ortho_para.singlet_para_1s0_eh == Fraction(-2969, 1458)
    assert ortho_para.para_minus_ortho_splitting_eh == Fraction(64, 729)
    assert ortho_para.triplet_strictly_below_singlet is True

    cert = build_qm225_helium_rhf_certificate()
    for atom in (cert.rhf_he_z2, cert.rhf_be_z4, cert.rhf_ne_z10):
        assert atom.strictly_contractive_all_steps is True
        for k in range(1, len(atom.step_l1_distances)):
            assert (
                atom.step_l1_distances[k]
                == atom.contraction_lambda * atom.step_l1_distances[k - 1]
            )

    assert cert.rhf_be_z4.first_ionization_potential_eh == Fraction(169, 500)
    assert cert.rhf_he_z2.first_ionization_potential_eh == Fraction(217, 256)
    assert cert.rhf_ne_z10.first_ionization_potential_eh == Fraction(13_689, 16_000)
    assert cert.noble_gas_ionization_increases_he_to_ne is True
    assert cert.noble_gas_peaks_above_open_shell_be is True

    he_custom = run_closed_shell_rhf_scf(
        "He", 2, (Fraction(2),), (Fraction(5, 16),), Fraction(1, 3), 5
    )
    assert he_custom.fixed_point_z_eff == (Fraction(27, 16),)
    assert he_custom.strictly_contractive_all_steps is True


def test_qm224_qm225_lean_and_manuscript_cross_layer_constant_parity() -> None:
    paper_root = Path(__file__).resolve().parents[3]
    lean_file = paper_root / "lean4" / "FiniteQM.lean"
    if not lean_file.exists():
        lean_file = paper_root / "lean" / "FiniteQM.lean"
    if not lean_file.exists():
        lean_file = paper_root / "research" / "lean4" / "FiniteQM.lean"
    lean_text = lean_file.read_text(encoding="utf-8")

    ms_file = paper_root / "papers" / "core" / "finite_quantum_mechanics.md"
    if not ms_file.exists():
        ms_file = paper_root / "finite_quantum_mechanics.md"
    manuscript_text = ms_file.read_text(encoding="utf-8")

    assert "let zeta : Rat := 29 / 16" in lean_text
    assert "e_hylleraas_4term = -119193915 / 41066752" in lean_text
    assert "let i1_be_2s : Rat := 169 / 500" in lean_text
    assert "let i1_he_1s : Rat := 217 / 256" in lean_text
    assert "let i1_ne_2p : Rat := 13689 / 16000" in lean_text
    assert r"\zeta = 29/16" in manuscript_text
    assert r"\ln k_0(2S) - \ln k_0(2P) \in [2.841786, 2.841787]" in manuscript_text
    assert r"I_1(\mathrm{Be}) = 169/500\,E_h < I_1(\mathrm{He}) = 217/256\,E_h < I_1(\mathrm{Ne}) = 13689/16000\,E_h" in manuscript_text


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'atomic_dirac.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'RationalIntervalQ' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.atomic_dirac', 'finite_qm.use_cases.atomic_dirac', 'src.qm.campaigns.atomic_dirac_lamb_hartree_fock_control', 'finite_qm.use_cases.atomic_dirac_lamb_hartree_fock_control')
_USE_SHIM = True
_MUTANTS = (('dirac_coulomb_alpha4_coeff:31', '    return Fraction(1, 2 * (n**4)) * (Fraction(n, k) - Fraction(3, 4))', '    return Fraction(1, 2 * (n**4)) * (Fraction(n, k) - Fraction(5, 4))'),)
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
