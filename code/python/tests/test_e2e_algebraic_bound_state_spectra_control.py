"""End-to-end tests for QM-217 algebraic bound-state spectra (su(2) Kravchuk & so(4) Hydrogen).
Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/bound_spectra.py
Claim: check_kravchuk_orthogonality_and_difference_eq certificate locked by exact checks in this file
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases.algebraic_bound_state_spectra_control import (
    check_kravchuk_orthogonality_and_difference_eq,
    dirac_fine_structure_coeff,
    evaluate_algebraic_bound_state_spectra_control,
    q_comm,
    q_is_zero,
    sl2_oscillator_generators,
    so4_hydrogen_shell_operators,
)


def test_negative_part_a_su2_kravchuk_harmonic_oscillator_and_uncertainty_saturation() -> None:
    """Verify sl(2, Q) ladder algebra, G-metric adjointness, and Robertson-Schrodinger saturation."""
    report = evaluate_algebraic_bound_state_spectra_control()
    assert report.kravchuk_sl2_commutators_exact
    assert report.kravchuk_casimir_matches_j_j_plus_1
    assert report.kravchuk_metric_adjoint_exact
    assert report.kravchuk_equidistant_ladder_commutators_exact
    assert report.kravchuk_ground_variance_q2 == Fraction(1, 4)
    assert report.kravchuk_ground_variance_p2 == Fraction(1, 4)
    assert report.kravchuk_ground_uncertainty_product == Fraction(1, 16)
    assert report.kravchuk_ground_saturates_robertson_schrodinger
    assert report.kravchuk_polynomial_orthogonality_exact
    assert report.kravchuk_difference_eigenvalue_exact

    with pytest.raises(ValueError):
        sl2_oscillator_generators(0)


def test_unit_part_a_kravchuk_polynomial_orthogonality_and_difference_equation() -> None:
    """Verify discrete Kravchuk binomial orthogonality and 3-term difference eigenvalue identity."""
    for n_max in (1, 2, 3, 4, 5):
        ortho_ok, diff_ok = check_kravchuk_orthogonality_and_difference_eq(n_max)
        assert ortho_ok
        assert diff_ok


def test_part_b_so4_pauli_runge_lenz_hydrogen_spectrum_and_orthogonality() -> None:
    """Verify L . K = 0, C_2(so(4)) = (n^2 - 1) I, E_n = -1/n^2, and orbital L^2 traces."""
    report = evaluate_algebraic_bound_state_spectra_control()
    assert report.hydrogen_chiral_factors_commute
    assert report.hydrogen_so4_lie_brackets_exact
    assert report.hydrogen_pauli_orthogonality_l_dot_k_zero
    assert report.hydrogen_asymmetric_control_l_dot_k_nonzero
    assert report.hydrogen_casimir_matches_n_squared_minus_1
    assert report.hydrogen_balmer_rydberg_energies == (
        Fraction(-1, 1),
        Fraction(-1, 4),
        Fraction(-1, 9),
        Fraction(-1, 16),
    )
    assert report.hydrogen_lyman_alpha_dimensionless_jump == Fraction(3, 4)
    assert report.hydrogen_balmer_alpha_dimensionless_jump == Fraction(5, 36)
    assert report.hydrogen_orbital_l2_traces == (
        Fraction(0, 1),
        Fraction(6, 1),
        Fraction(36, 1),
        Fraction(120, 1),
    )
    assert report.hydrogen_orbital_l2_traces_match_clebsch_gordan

    with pytest.raises(ValueError):
        so4_hydrogen_shell_operators(0)


def test_part_c_n2_degeneracy_projectors_and_runge_lenz_symmetry_breaking() -> None:
    """Verify Pi_{2S} and Pi_{2P} projectors, Dirac fine-structure degeneracy, and [Pi_{2S}, K_z] != 0."""
    report = evaluate_algebraic_bound_state_spectra_control()
    assert report.n2_projectors_idempotent_orthogonal_complete
    assert report.n2_2s_rank == Fraction(1, 1)
    assert report.n2_2p_rank == Fraction(3, 1)
    assert report.n2_pi_2s_commutes_with_so3_l
    assert report.n2_pi_2s_breaks_runge_lenz_k
    assert report.dirac_fs_2s_half_coeff == Fraction(-5, 128)
    assert report.dirac_fs_2p_half_coeff == Fraction(-5, 128)
    assert report.dirac_fs_2p_three_halves_coeff == Fraction(-1, 128)
    assert report.dirac_fs_2s_2p_half_degenerate
    assert report.dirac_fs_fine_structure_splitting_coeff == Fraction(1, 32)

    with pytest.raises(ValueError):
        dirac_fine_structure_coeff(2, 2)


def test_part_c_12_decimal_lyman_alpha_and_lamb_contact_enclosures() -> None:
    """Verify 12-decimal RationalInterval enclosures for Lyman-alpha THz and 2S-2P contact MHz."""
    report = evaluate_algebraic_bound_state_spectra_control()
    assert report.lyman_alpha_gross_thz_12_digits_agree
    assert report.lyman_alpha_gross_thz_interval.width < Fraction(1, 10**13)
    assert report.lyman_alpha_gross_thz_decimal_12 == "2467.381467264629"

    assert report.lamb_contact_2s_2p_mhz_12_digits_agree
    assert report.lamb_contact_2s_2p_mhz_interval.width < Fraction(1, 10**13)
    assert report.lamb_contact_2s_2p_mhz_decimal_12 == "617.179215588248"


def test_part_c_so4_runge_lenz_commutes_with_unperturbed_casimir() -> None:
    """Verify [C_2(so(4)), K_z] = 0 on H_2 while [Pi_{2S}, K_z] != 0."""
    ops_n2 = so4_hydrogen_shell_operators(2)
    assert q_is_zero(q_comm(ops_n2["C2_so4"], ops_n2["Kz"]))


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'bound_spectra.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'check_kravchuk_orthogonality_and_difference_eq' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.bound_spectra', 'finite_qm.use_cases.bound_spectra', 'src.qm.campaigns.algebraic_bound_state_spectra_control', 'finite_qm.use_cases.algebraic_bound_state_spectra_control')
_USE_SHIM = True
_MUTANTS = (('q_is_zero:124', '    return all(entry == 0 for row in a for entry in row)', '    return all(entry == 1 for row in a for entry in row)'),)
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
