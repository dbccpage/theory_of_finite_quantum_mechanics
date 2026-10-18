"""End-to-end tests for QM-215 Dirac/Kulish-Faddeev dressed matter and Ward-Takahashi Z_1 = Z_2.
Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/ward_takahashi.py
Claim: Qi certificate locked by exact checks in this file
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

from finite_qm.use_cases.dirac_ward_takahashi_control import (
    Qi,
    check_clifford_anticommutation,
    dirac_propagator,
    dirac_propagator_inverse,
    evaluate_dirac_ward_takahashi_control,
    feynman_slash,
    mat4_identity,
    mat4_mul,
    mat4_sub,
    one_loop_self_energy_integrand,
    one_loop_self_energy_minus_derivative,
    one_loop_vertex_integrand,
)


def test_unit_part_a_clifford_algebra_and_tree_level_ward_takahashi() -> None:
    """Verify 4x4 Clifford anticommutation over Q(i) and tree-level Ward-Takahashi identity."""
    assert check_clifford_anticommutation()
    p = [Fraction(5, 1), Fraction(1, 1), Fraction(2, 1), Fraction(-1, 1)]
    q = [Fraction(2, 1), Fraction(-1, 1), Fraction(1, 1), Fraction(3, 1)]
    pq = [p[mu] + q[mu] for mu in range(4)]
    mass = Fraction(2, 1)

    sf_p = dirac_propagator(p, mass)
    sf_p_inv = dirac_propagator_inverse(p, mass)
    sf_pq = dirac_propagator(pq, mass)
    sf_pq_inv = dirac_propagator_inverse(pq, mass)
    q_slash = feynman_slash(q)

    assert mat4_mul(sf_p, sf_p_inv) == mat4_identity()
    assert mat4_mul(sf_pq, sf_pq_inv) == mat4_identity()
    assert mat4_sub(sf_pq_inv, sf_p_inv) == q_slash
    assert mat4_mul(sf_pq, mat4_mul(q_slash, sf_p)) == mat4_sub(sf_p, sf_pq)


def test_part_a_dfm_spanning_tree_dressed_fermion_gauge_invariance() -> None:
    """Verify bare correlator gauge dependence vs. DFM dressed correlator gauge invariance."""
    report = evaluate_dirac_ward_takahashi_control()
    assert report.bare_correlator_gauge_dependent
    assert report.dfm_dressed_correlator_gauge_invariant_all_trees
    assert report.dfm_tree_change_shifts_by_cycle_holonomy


def test_part_b_one_loop_ward_takahashi_integrand_identity() -> None:
    """Verify q_mu I_Lambda^mu(p+q, p; k) == I_Sigma(p, k) - I_Sigma(p+q, k) in M_4(Q(i))."""
    report = evaluate_dirac_ward_takahashi_control()
    assert report.one_loop_ward_takahashi_integrand_exact


def test_part_b_differential_ward_identity_and_z1_equals_z2() -> None:
    """Verify I_Lambda^mu(p, p; k) == -d I_Sigma(p, k)/d p_mu at q=0 and Z_1 / Z_2 == 1."""
    p = [Fraction(5, 1), Fraction(1, 1), Fraction(2, 1), Fraction(-1, 1)]
    k = [Fraction(3, 1), Fraction(-2, 1), Fraction(1, 2), Fraction(1, 1)]
    mass = Fraction(2, 1)
    photon_mass_sq = Fraction(1, 3)

    for mu in range(4):
        lam_mu = one_loop_vertex_integrand(p, p, k, mu, mass, photon_mass_sq)
        minus_dsigma_mu = one_loop_self_energy_minus_derivative(p, k, mu, mass, photon_mass_sq)
        assert lam_mu == minus_dsigma_mu

    p_perturbed = [Fraction(6, 1), Fraction(1, 1), Fraction(2, 1), Fraction(-1, 1)]
    lam_pert = one_loop_vertex_integrand(p_perturbed, p, k, 0, mass, photon_mass_sq)
    assert lam_pert != one_loop_self_energy_minus_derivative(p, k, 0, mass, photon_mass_sq)

    report = evaluate_dirac_ward_takahashi_control()
    assert report.one_loop_differential_ward_identity_at_q_zero_exact
    assert report.bphz_vertex_and_self_energy_uv_counterterms_equal
    assert report.z1_over_z2_ratio_exact_one == Fraction(1, 1)


def test_part_c_kulish_faddeev_ir_cancellation_and_enclosure() -> None:
    """Verify IR regulator cancellation and 12-decimal enclosure of S_KF = exp(E_KF)."""
    report = evaluate_dirac_ward_takahashi_control()
    assert report.kf_ir_scale_cancels_across_all_cutoffs
    assert report.kf_ir_laurent_pole_cancels_identically
    assert report.kf_cusp_velocity == Fraction(3, 5)
    assert report.kf_energy_resolution_ratio == Fraction(1, 2)
    assert report.kf_exponent_interval.hi < 0
    assert report.kf_attenuation_12_digits_agree
    assert report.kf_attenuation_interval.width < Fraction(1, 10**14)
    assert report.kf_attenuation_decimal_12 == "0.997892261461"


def test_gaussian_rational_qi_field_invariants() -> None:
    """Verify exact multiplicative inverse and norm on Gaussian rationals Q(i)."""
    z = Qi(Fraction(3, 5), Fraction(4, 5))
    assert z.norm_sq() == Fraction(1, 1)
    assert z * z.inv() == Qi.one()
    assert z.inv() == z.conj()
    p = [Fraction(5, 1), Fraction(1, 1), Fraction(2, 1), Fraction(-1, 1)]
    k = [Fraction(3, 1), Fraction(-2, 1), Fraction(1, 2), Fraction(1, 1)]
    sig = one_loop_self_energy_integrand(p, k, Fraction(2, 1), Fraction(1, 3))
    assert sig != mat4_identity()


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'ward_takahashi.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'Qi' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.ward_takahashi', 'finite_qm.use_cases.ward_takahashi', 'src.qm.campaigns.dirac_ward_takahashi_control', 'finite_qm.use_cases.dirac_ward_takahashi_control')
_USE_SHIM = True
_MUTANTS = (('mat4_sub:127', '    return [[left[r][c] - right[r][c] for c in range(4)] for r in range(4)]', '    return [[left[r][c] - right[r][c] for c in range(5)] for r in range(4)]'),)
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
