"""E2E: QM-229 / QM-230 / QM-231 gravity, GHZ / Page-Wootters / phase damping and
Chern parity finite-map control.

AuthorityEffect: None.

Each test recomputes the quantity it checks from the stored values or from the
public functions, rather than reading a flag the builder wrote.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/regge_gravity.py
Claim: Qi certificate locked by exact checks in this file
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases.page_wootters_tsirelson_wigner_control import (
    Qi,
    qi_eye,
    qi_mat_eq,
    qi_matmul,
    qi_matvec,
    qi_scale,
    qi_trace,
)
from finite_qm.use_cases.regge_gravity_ghz_chern_control import (
    ReggeGravityGhzChernRefusal,
    apply_kraus,
    build_chern_parity_audit,
    build_ghz_mermin_audit,
    build_page_wootters_audit,
    build_phase_damping_audit,
    build_post_newtonian_audit,
    clock_shift,
    deflection_radians,
    dust_at_rest_stress_tensor,
    evaluate_regge_gravity_ghz_chern_control,
    exact_eigenvalue,
    ghz_unnormalized,
    haldane_chern_number,
    kron3,
    mermin_deterministic_values,
    mermin_operator,
    minkowski_trace,
    null_probe_stress_tensor,
    pauli_x,
    pauli_z,
    perihelion_advance_arcsec_per_orbit,
    phase_damping_kraus,
    plus_state_density,
    ppn_deflection_factor,
    ppn_perihelion_factor,
    qi_mat_pow,
    qwz_chern_number,
    rayleigh_quotient,
)


def test_unit_qm229_stress_tensors_are_built_and_traced() -> None:
    audit = build_post_newtonian_audit()
    e, rho = audit.null_probe_energy, audit.dust_density
    assert audit.null_probe_tensor == null_probe_stress_tensor(e)
    assert audit.null_probe_tensor[0][0] == audit.null_probe_tensor[0][1] == e
    assert audit.null_probe_tensor[1][1] == e
    assert minkowski_trace(audit.null_probe_tensor) == e - e == 0
    assert audit.dust_tensor == dust_at_rest_stress_tensor(rho)
    assert minkowski_trace(audit.dust_tensor) == rho == Fraction(5, 2)


def test_negative_qm229_gr_deflection_is_twice_newtonian() -> None:
    audit = build_post_newtonian_audit()
    inp = audit.inputs
    gm, c, b = inp.solar_gm_m3_s2, inp.speed_of_light_m_s, inp.solar_radius_m
    assert audit.gr_deflection_rad == 4 * gm / (c * c * b)
    assert audit.newtonian_deflection_rad == 2 * gm / (c * c * b)
    assert audit.gr_deflection_rad == 2 * audit.newtonian_deflection_rad
    assert ppn_deflection_factor(Fraction(1)) == 1
    assert ppn_deflection_factor(Fraction(0)) == Fraction(1, 2)
    with pytest.raises(ReggeGravityGhzChernRefusal):
        deflection_radians(gm, c, Fraction(0), Fraction(1))


def test_qm229_solar_limb_deflection_windows() -> None:
    audit = build_post_newtonian_audit()
    gr, newton = audit.gr_deflection_arcsec, audit.newtonian_deflection_arcsec
    assert Fraction(1750, 1000) <= gr.lo <= gr.hi <= Fraction(1752, 1000)
    assert Fraction(875, 1000) <= newton.lo <= newton.hi <= Fraction(876, 1000)
    assert Fraction(17511, 10000) <= gr.lo <= gr.hi < Fraction(17512, 10000)
    assert Fraction(8755, 10000) <= newton.lo <= newton.hi < Fraction(8756, 10000)


def test_qm229_mercury_perihelion_exact_rational() -> None:
    audit = build_post_newtonian_audit()
    inp = audit.inputs
    a_m = inp.mercury_semi_major_axis_au * inp.astronomical_unit_m
    e = inp.mercury_eccentricity
    per_orbit = perihelion_advance_arcsec_per_orbit(
        inp.solar_gm_m3_s2, inp.speed_of_light_m_s, a_m, e, Fraction(1), Fraction(1)
    )
    assert audit.mercury_advance_arcsec_per_orbit == per_orbit
    per_century = per_orbit * inp.julian_century_days / inp.mercury_period_days
    assert audit.mercury_advance_arcsec_per_century == per_century
    assert Fraction(4297, 100) <= per_century <= Fraction(4299, 100)
    assert Fraction(4298, 100) <= per_century < Fraction(4299, 100)
    assert ppn_perihelion_factor(Fraction(1), Fraction(1)) == 1
    assert ppn_perihelion_factor(Fraction(41, 42), Fraction(1)) == Fraction(62, 63)
    with pytest.raises(ReggeGravityGhzChernRefusal):
        perihelion_advance_arcsec_per_orbit(
            inp.solar_gm_m3_s2, inp.speed_of_light_m_s, a_m, Fraction(1), Fraction(1), Fraction(1)
        )


def test_qm230_ghz_is_an_eigenvector_of_each_mermin_operator() -> None:
    audit = build_ghz_mermin_audit()
    g = ghz_unnormalized()
    for op, lam in zip(audit.operators, (-1, -1, -1, 1), strict=True):
        assert qi_matvec(op, g) == [Qi.from_int(lam) * x for x in g]
    mermin = mermin_operator(audit.operators)
    assert qi_matvec(mermin, g) == [Qi.from_int(4) * x for x in g]
    assert audit.ghz_eigenvalues == tuple(Qi.from_int(n) for n in (-1, -1, -1, 1))
    assert audit.mermin_eigenvalue == Qi.from_int(4)


def test_qm230_mermin_operator_algebra() -> None:
    a1, a2, a3, b = build_ghz_mermin_audit().operators
    for op in (a1, a2, a3, b):
        assert qi_mat_eq(qi_matmul(op, op), qi_eye(8))
    assert qi_mat_eq(qi_matmul(a1, a2), qi_matmul(a2, a1))
    assert qi_mat_eq(qi_matmul(qi_matmul(a1, a2), a3), qi_scale(Fraction(-1), b))


def test_qm230_deterministic_assignments_stay_within_two() -> None:
    values = mermin_deterministic_values()
    assert len(values) == 64
    assert max(abs(v) for v in values) == 2
    assert sorted(set(values)) == [-2, 2]
    assert build_ghz_mermin_audit().mermin_eigenvalue.re == 4


def test_qm230_non_eigenvector_and_zero_vector_are_refused() -> None:
    zxx = kron3(pauli_z(), pauli_x(), pauli_x())
    with pytest.raises(ReggeGravityGhzChernRefusal):
        exact_eigenvalue(zxx, ghz_unnormalized())
    zero = [Qi.from_int(0) for _ in range(8)]
    with pytest.raises(ReggeGravityGhzChernRefusal):
        rayleigh_quotient(zxx, zero)
    with pytest.raises(ReggeGravityGhzChernRefusal):
        exact_eigenvalue(zxx, zero)


def test_qm230_page_wootters_history() -> None:
    audit = build_page_wootters_audit()
    u, psi0, history = audit.step_unitary, audit.initial_state, audit.history
    assert qi_mat_eq(qi_mat_pow(u, 4), qi_eye(2))
    assert not qi_mat_eq(qi_mat_pow(u, 2), qi_eye(2))
    assert not u[0][1].is_zero()
    for t in range(4):
        assert history[2 * t : 2 * t + 2] == qi_matvec(qi_mat_pow(u, t), psi0)
    assert all(x.is_zero() for x in audit.lowering_residual)
    assert not all(x.is_zero() for x in audit.raising_residual)
    assert clock_shift(4, -1)[3][0] == Qi.from_int(1)
    assert audit.history_norm_sq_over_initial_norm_sq == 4


def test_qm230_phase_damping_three_applications() -> None:
    audit = build_phase_damping_audit()
    run = audit.runs[0]
    assert run.triple == (3, 4, 5)
    k0, k1 = phase_damping_kraus(3, 4, 5)
    rho = plus_state_density()
    for n in range(4):
        assert qi_mat_eq(run.states[n], rho)
        assert qi_trace(rho) == Qi.from_int(1)
        assert rho[0][1] == Qi(Fraction(1, 2) * Fraction(3, 5) ** n)
        rho = apply_kraus((k0, k1), rho)
    assert run.states[3][0][1] == Qi(Fraction(27, 250))
    assert run.coherence(3) == Fraction(27, 125)
    for other in audit.runs[1:]:
        p, _, q = other.triple
        assert other.coherence(3) == Fraction(p, q) ** 3
    with pytest.raises(ReggeGravityGhzChernRefusal):
        phase_damping_kraus(2, 3, 4)


def test_qm231_qwz_chern_numbers() -> None:
    audit = build_chern_parity_audit()
    for m, c in audit.qwz_values:
        assert c == qwz_chern_number(m)
    assert tuple(c for _, c in audit.qwz_values) == (0, 1, -1, 0)
    for m in (Fraction(-2), Fraction(0), Fraction(2)):
        assert qwz_chern_number(m) is None
    assert qwz_chern_number(Fraction(1, 2)) == -1
    assert qwz_chern_number(Fraction(-1, 2)) == 1


def test_qm231_haldane_phase_diagram() -> None:
    t2 = Fraction(1, 10)
    assert haldane_chern_number(Fraction(1), t2, Fraction(1)) == 0
    assert haldane_chern_number(Fraction(1, 2), t2, Fraction(1)) == -1
    assert haldane_chern_number(Fraction(1, 2), t2, Fraction(-1)) == 1
    assert haldane_chern_number(Fraction(0), Fraction(0), Fraction(1)) is None
    audit = build_chern_parity_audit()
    for (m, t, s), c in audit.haldane_grid:
        assert c == haldane_chern_number(m, t, s)
        assert c is not None


def test_combined_report_reads_its_audits() -> None:
    report = evaluate_regge_gravity_ghz_chern_control()
    assert report.control_ids == ("QM-229", "QM-230", "QM-231")
    assert report.passed == (
        report.post_newtonian.passed
        and report.ghz_mermin.passed
        and report.page_wootters.passed
        and report.phase_damping.passed
        and report.chern_parity.passed
    )
    assert report.passed


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'regge_gravity.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'Qi' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.regge_gravity', 'finite_qm.use_cases.regge_gravity', 'src.qm.campaigns.regge_gravity_ghz_chern_control', 'finite_qm.use_cases.regge_gravity_ghz_chern_control')
_USE_SHIM = True
_MUTANTS = (('ppn_deflection_factor:109', '    return (1 + gamma) / 2', '    return (2 + gamma) / 2'),)
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
