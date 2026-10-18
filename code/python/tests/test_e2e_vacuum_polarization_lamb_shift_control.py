"""End-to-end tests for QM-216 1-loop QED vacuum polarization, running alpha, and Lamb shift.
Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/vacuum_polarization.py
Claim: check_transverse_projector_identities certificate locked by exact checks in this file
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases.vacuum_polarization_lamb_shift_control import (
    check_transverse_projector_identities,
    evaluate_vacuum_polarization_lamb_shift_control,
    fermion_bubble_numerator_analytic,
    fermion_bubble_numerator_clifford_trace,
    feynman_parameter_moment_beta_closed,
    feynman_parameter_moment_polynomial,
    transverse_projector,
)


def test_negative_part_a_transverse_ward_projector_and_null_guard() -> None:
    """Verify q_mu P_T^{mu nu}(q) = 0, P_T^2 = P_T, tr(P_T) = 3, and null-momentum refusal."""
    q_timelike = [Fraction(5, 1), Fraction(1, 1), Fraction(2, 1), Fraction(1, 1)]
    q_spacelike = [Fraction(2, 1), Fraction(3, 1), Fraction(1, 1), Fraction(1, 1)]
    for q_vec in (q_timelike, q_spacelike):
        ward_ok, idemp_ok, tr_val = check_transverse_projector_identities(q_vec)
        assert ward_ok
        assert idemp_ok
        assert tr_val == Fraction(3, 1)

    q_null = [Fraction(5, 1), Fraction(3, 1), Fraction(4, 1), Fraction(0, 1)]
    with pytest.raises(ZeroDivisionError):
        transverse_projector(q_null)


def test_unit_part_a_clifford_bubble_numerator_trace_matches_analytic() -> None:
    """Verify 4x4 Clifford trace tr[gamma^mu(k_slash+q_slash+m)gamma^nu(k_slash+m)] over Q(i)."""
    k = [Fraction(5, 1), Fraction(-1, 1), Fraction(2, 1), Fraction(3, 1)]
    q = [Fraction(2, 1), Fraction(3, 1), Fraction(1, 1), Fraction(1, 1)]
    mass = Fraction(2, 1)
    num_cliff = fermion_bubble_numerator_clifford_trace(k, q, mass)
    num_anal = fermion_bubble_numerator_analytic(k, q, mass)
    assert num_cliff == num_anal

    assert num_cliff != fermion_bubble_numerator_analytic(k, q, Fraction(3, 1))


def test_part_a_symanzik_bubble_simplex_and_bphz_on_shell_subtraction() -> None:
    """Verify U_{G_bub}(x, 1-x) = 1, F_{G_bub} = m^2 - x(1-x)q^2, and BPHZ UV cutoff cancellation."""
    report = evaluate_vacuum_polarization_lamb_shift_control()
    assert report.transverse_ward_identity_exact
    assert report.transverse_projector_idempotent_exact
    assert report.transverse_projector_trace_equals_three == Fraction(3, 1)
    assert report.clifford_bubble_trace_matches_analytic
    assert report.symanzik_bubble_simplex_u_equals_one
    assert report.symanzik_bubble_simplex_f_matches_feynman_denom
    assert report.bphz_uv_cutoff_cancels_at_all_scales
    assert report.bphz_on_shell_pi_r_at_zero_is_zero


def test_part_b_feynman_parameter_moments_and_uehling_series() -> None:
    """Verify exact polynomial integration matches Beta((n+1)!^2/(2n+3)!) and Uehling 1/15 slope."""
    expected_moments = [
        Fraction(1, 30),
        Fraction(1, 140),
        Fraction(1, 630),
        Fraction(1, 2772),
    ]
    for n, exp_m in enumerate(expected_moments, start=1):
        assert feynman_parameter_moment_polynomial(n) == exp_m
        assert feynman_parameter_moment_beta_closed(n) == exp_m

    report = evaluate_vacuum_polarization_lamb_shift_control()
    assert report.moments_match_beta_closed_form
    assert report.uehling_leading_slope_coeff == Fraction(1, 15)
    assert report.second_moment_series_coeff == Fraction(1, 140)
    assert report.third_moment_series_coeff == Fraction(1, 945)


def test_part_b_spacelike_vacuum_polarization_and_running_alpha_enclosure() -> None:
    """Verify 12-decimal enclosure of Pi_R(-9m^2/4) and running alpha_eff^{-1}(-9m^2/4)."""
    report = evaluate_vacuum_polarization_lamb_shift_control()
    assert report.spacelike_velocity_v == Fraction(5, 3)
    assert report.spacelike_q2_over_m2 == Fraction(-9, 4)
    assert report.pi_r_spacelike_interval.hi < 0
    assert report.pi_r_spacelike_12_digits_agree
    assert report.pi_r_spacelike_decimal_12 == "-0.000284802666"
    assert report.alpha_eff_inv_spacelike_12_digits_agree
    assert report.alpha_eff_inv_spacelike_decimal_12 == "136.996970947974"
    assert report.alpha_eff_exceeds_bare_alpha


def test_part_c_uehling_potential_and_hydrogen_lamb_shift_enclosure() -> None:
    """Verify 5/6 + 1/8 - 1/5 = 91/120 contact sum and 12-decimal -27.128756729153 MHz Uehling shift."""
    report = evaluate_vacuum_polarization_lamb_shift_control()
    assert report.lamb_contact_se_term == Fraction(5, 6)
    assert report.lamb_contact_g2_magnetic_term == Fraction(1, 8)
    assert report.lamb_contact_uehling_vp_term == Fraction(-1, 5)
    assert report.lamb_contact_total_rational == Fraction(91, 120)
    assert report.lamb_contact_se_term + report.lamb_contact_uehling_vp_term == Fraction(19, 30)
    assert report.uehling_2s_dimensionless_coeff == Fraction(-1, 30)
    assert report.uehling_2s_dimensionless_interval.hi < 0
    assert report.uehling_2s_mhz_12_digits_agree
    assert report.uehling_2s_mhz_decimal_12 == "-27.128756729153"


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'vacuum_polarization.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'check_transverse_projector_identities' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.vacuum_polarization', 'finite_qm.use_cases.vacuum_polarization', 'src.qm.campaigns.vacuum_polarization_lamb_shift_control', 'finite_qm.use_cases.vacuum_polarization_lamb_shift_control')
_USE_SHIM = True
_MUTANTS = (('check_transverse_projector_identities:96', '    for nu in range(4):', '    for nu in range(5):'),)
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
