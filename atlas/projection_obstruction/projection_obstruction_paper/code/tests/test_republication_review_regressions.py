"""Reviewer Regression Test Suite for Republication Review Findings (C01–C23).

AuthorityEffect: None.

Directly asserts that republication review findings (C01–C23) are
remediated and that recurrence is prevented.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any
import numpy as np
import pytest

from calibration_quotient import (
    CalibrationQuotient,
    CalibrationQuotientCertificate,
    NuisanceModel,
    _to_fraction,
)
from exact_graph_state_separation import (
    CARDANO_CUBIC_ROOT_R,
    RATIONAL_ISOLATING_INTERVAL,
    certify_universal_product_lower_bound,
    generate_minimax_certificate,
    observational_distance,
    verify_rational_isolating_interval,
    verify_state_validity,
)
from exactsym import Matrix
from observable_duhamel import (
    Interval,
    evaluate_observable_duhamel_bound,
)
from observation_tradeoffs import (
    benchmark_against_tran_multipartite,
    connected_onset_bound_constant,
    evaluate_difference_set_conditioning,
)
from open_system_jets import (
    OpenSystemInputError,
    compute_local_incident_strengths,
    evaluate_open_system_defect_jet,
    lindblad_action,
    propagate_parameter_uncertainties,
)
from verify_certificate import verify_document


# ===========================================================================
# C01: Legacy Lindblad helper returns a false lower bound
# ===========================================================================
def test_C01_legacy_open_system_lower_bound_is_not_above_exact_defect() -> None:
    """C01: evaluate_open_system_defect_jet must not return a bound strictly above actual defect.

    Reproduction model: H=0, rho0=|00><00|, L=|11><00|, gamma=1.
    nu=4, g_v=0, G_v=1, Lambda_* = 2.
    Exact solution: D(t) = 4 exp(-t)(1 - exp(-t)).
    """
    nu = 4.0
    g_v = 0.0
    G_v = 1.0

    times = [0.01, 0.05, 0.1, 0.15, 0.2]
    for t in times:
        exact_defect = 4.0 * math.exp(-t) * (1.0 - math.exp(-t))
        bound = evaluate_open_system_defect_jet(nu, g_v, G_v, t)
        assert bound <= exact_defect, (
            f"Returned lower bound {bound} exceeds exact defect {exact_defect} at t={t}"
        )

    # At t=0.1: exact defect is 0.34442665983191106.
    # Proved formula with Lambda_* = 2 returns 0.16 <= 0.34442665983191106.
    bound_01 = evaluate_open_system_defect_jet(nu, g_v, G_v, 0.1)
    assert math.isclose(bound_01, 0.16, abs_tol=1e-12)
    assert bound_01 < 0.34442665983191106


# ===========================================================================
# C02: Core certificate witnesses are not mathematically rechecked
# ===========================================================================
def test_C02_core_verifier_rejects_missing_or_unrealisable_witness(monkeypatch: pytest.MonkeyPatch) -> None:
    """C02: Core verifier must reject empty witnesses and negative/unrealisable norms."""
    import pathlib

    # Minimal mock data mimicking a mechanization run
    from verify_certificate import REQUIRED_CLAIMS

    dummy_results: list[dict[str, Any]] = []
    for cid in sorted(REQUIRED_CLAIMS):
        dummy_results.append({
            "claim_ids": [cid],
            "title": f"Claim {cid}",
            "evidence_kind": "not_executable" if cid in ("H8", "H9") else "exact_finite",
            "verdict": "refused" if cid in ("H8", "H9") else "pass",
            "statement_scope": "finite scope",
            "algorithm": "exact verification",
            "witness": {"dummy": "1"},
            "limitations": [],
            "authority_effect": "None",
        })

    mock_doc = {
        "schema_version": "po000.mechanization_run.v4",
        "paper_id": "PO-000",
        "authority_effect": "None",
        "paper_version": "6.9.18",
        "python_package_version": "6.9.6",
        "results": dummy_results,
        "unresolved_claim_ids": ["E3-general", "E4-general", "P4-7"],
        "execution_completed": True,
        "executable_checks_passed": True,
        "refusals_present": True,
        "open_obligations_present": True,
        "claim_disposition_complete": True,
        "promotion_eligible": False,
        "source_hashes": {},
        "publication_hashes": {},
        "finite_certificates": {},
    }

    # Test 1: all-empty witnesses must produce errors
    empty_doc = dict(mock_doc)
    empty_doc["results"] = [
        dict(r, witness={}) if r["verdict"] == "pass" else r
        for r in dummy_results
    ]
    errs_empty = verify_document(empty_doc, pathlib.Path("."))
    assert any("witness must be a nonempty object" in e for e in errs_empty)

    # Test 2: B2 witness with raw_I = -999 and defect=Matrix([[2]]) must produce error
    bad_b2_doc = dict(mock_doc)
    bad_b2_results = []
    for r in dummy_results:
        if "B2" in r["claim_ids"]:
            bad_b2_results.append(dict(r, witness={"raw_I": "-999", "defect": "Matrix([[2]])", "bound": "2"}))
        else:
            bad_b2_results.append(r)
    bad_b2_doc["results"] = bad_b2_results
    errs_bad_b2 = verify_document(bad_b2_doc, pathlib.Path("."))
    assert any("raw_I must be non-negative" in e or "cannot be negative" in e or "does not match bound" in e for e in errs_bad_b2)


# ===========================================================================
# C03: Minimax certificate remains verified after exact interval failure
# ===========================================================================
def test_C03_minimax_status_depends_on_exact_interval_check(monkeypatch: pytest.MonkeyPatch) -> None:
    """C03: Minimax certificate status must fail when rational isolating interval fails."""
    # Nominal case: passes
    cert_nominal = generate_minimax_certificate()
    assert cert_nominal.status == "verified"
    assert cert_nominal.universal_lower_bound_proved is True

    # Mutate isolating interval to invalid endpoints
    import exact_graph_state_separation as egss
    monkeypatch.setattr(egss, "RATIONAL_ISOLATING_INTERVAL", (Fraction(0), Fraction(1, 10)))

    proof = egss.certify_universal_product_lower_bound()
    assert proof["is_interval_verified"] is False
    assert proof["status"] == "fail"

    cert_mutated = egss.generate_minimax_certificate()
    assert cert_mutated.status == "failed"
    assert cert_mutated.universal_lower_bound_proved is False


# ===========================================================================
# C04: Comparative benchmark is not model-bound and can underbound the defect
# ===========================================================================
def test_C04_benchmark_onset_bound_encloses_declared_two_qubit_example() -> None:
    """C04: Two-qubit ZZ interaction with initial |++> must receive onset order 1 and enclose actual defect."""
    # For H = Z x Z with initial |++>, actual defect at t=0.001 is D(t) ~ 0.002001998664
    t = 0.001
    exact_defect = math.sin(2 * t) + 0.5 * (math.sin(2 * t) ** 2)

    res = benchmark_against_tran_multipartite(
        lattice={"num_qubits": 2, "j_zz": 1.0, "state": "plus"},
        time_horizon=t,
        num_time_points=10,
    )

    # 1. Onset order must be 1 for adjacent 2-qubit pair
    assert res["steiner_onset_order"] == 1

    # 2. Bound must enclose actual defect (not underbound it as 0.000032)
    po000_bound = res["po000_onset_bound"]
    assert po000_bound >= exact_defect, (
        f"PO-000 onset bound {po000_bound} underbounds actual defect {exact_defect}"
    )

    # 3. Commutator cancellation must evaluate to False on asymmetric/state-mismatched input
    assert res["exact_commutator_cancels"] is False


# ===========================================================================
# C05: Lindblad input paths silently drop jumps or admit negative rates
# ===========================================================================
def test_C05_generator_rejects_missing_jump_rate() -> None:
    """C05: Generator must reject mismatched jump operators and jump rates."""
    rho = np.eye(2, dtype=np.complex128) / 2.0
    h = np.zeros((2, 2), dtype=np.complex128)
    l_op = np.array([[0, 1], [0, 0]], dtype=np.complex128)

    with pytest.raises(OpenSystemInputError, match="Length mismatch"):
        lindblad_action(rho, h, jump_ops=[l_op], jump_rates=[])


def test_C05_generator_rejects_negative_tuple_rate() -> None:
    """C05: Incident strength computation must reject negative tuple rates."""
    l_op = np.array([[0, 1], [0, 0]], dtype=np.complex128)
    with pytest.raises(OpenSystemInputError, match="Jump rate must be"):
        compute_local_incident_strengths(
            hamiltonian_terms=[],
            jump_operators=[((0,), -1.0, l_op)],
            vertex=0,
        )


# ===========================================================================
# C06: A lower-bound value is presented as a two-sided defect interval
# ===========================================================================
def test_C06_zero_uncertainty_does_not_make_lower_bound_an_actual_defect_interval() -> None:
    """C06: Zero parameter uncertainty on a lower bound must not collapse to a singleton excluding actual defect."""
    # From C01, corrected lower bound is 0.16 and actual defect is 0.34442665983191106
    base_lower_bound = 0.16
    exact_defect = 0.34442665983191106

    interval = propagate_parameter_uncertainties(
        delta_J=0.0,
        delta_gamma=0.0,
        delta_M=0.0,
        base_bound=base_lower_bound,
    )

    assert interval.lower <= base_lower_bound
    assert interval.upper > base_lower_bound, "Zero uncertainty must not collapse lower bound to singleton"
    assert interval.contains(exact_defect), (
        f"Defect interval [{interval.lower}, {interval.upper}] must contain actual defect {exact_defect}"
    )


# ===========================================================================
# C07: Invalid carriers and incomplete reports return valid or zero results
# ===========================================================================
def test_C07_density_validator_rejects_nan() -> None:
    """C07: Density matrix validator must reject NaN entries."""
    nan_mat = np.array([[np.nan, 0.0], [0.0, 1.0]], dtype=np.complex128)
    valid, msg = verify_state_validity(nan_mat)
    assert valid is False
    assert "non-finite" in msg.lower() or "nan" in msg.lower()


def test_C07_observation_distance_rejects_missing_coordinates() -> None:
    """C07: Observation distance must reject empty coordinate lists."""
    empty_dict = {"K": [], "X": [], "Z": []}
    with pytest.raises(ValueError, match="cannot be empty"):
        observational_distance(empty_dict, empty_dict)


def test_C07_observation_distance_rejects_nan() -> None:
    """C07: Observation distance must reject NaN coordinates."""
    dict1 = {"K": [np.nan], "X": [0.0], "Z": [0.0]}
    dict2 = {"K": [0.0], "X": [0.0], "Z": [0.0]}
    with pytest.raises(ValueError, match="finite"):
        observational_distance(dict1, dict2)


def test_C07_difference_state_validator_enforces_trace_norm_cap() -> None:
    """C07: Difference state conditioning must enforce ||Delta||_1 <= 2.0 cap."""
    # 2 * Z has trace norm 4.0, which violates the physical difference state cap of 2.0
    two_z = np.array([[2.0, 0.0], [0.0, -2.0]], dtype=np.complex128)
    obs = [np.eye(2, dtype=np.complex128)]
    res = evaluate_difference_set_conditioning(difference_state=two_z, observables=obs)
    assert res["trace_norm"] == 4.0
    assert res["is_valid_difference_state"] is False


# ===========================================================================
# C08: Calibration checker leaves report fields unverified
# ===========================================================================
def test_C08_calibration_checker_recomputes_mean() -> None:
    """C08: Calibration checker must verify that mean_circulation matches the cochain."""
    cert = CalibrationQuotient(3).certificate([1, 2, 3])
    assert cert.verify() is True

    # Mutate mean_circulation to 999
    bad_mean_cert = CalibrationQuotientCertificate(
        n_sites=cert.n_sites,
        cochain=cert.cochain,
        mean_circulation=Fraction(999),
        quotient_norm=cert.quotient_norm,
        optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual,
        dual_witness=cert.dual_witness,
        primal_value=cert.primal_value,
        dual_value=cert.dual_value,
        duality_gap=cert.duality_gap,
        is_separated=cert.is_separated,
        evidence_scope=cert.evidence_scope,
        authority_effect=cert.authority_effect,
    )
    assert bad_mean_cert.verify() is False


def test_C08_calibration_checker_enforces_authority_metadata() -> None:
    """C08: Calibration checker must reject non-None authority metadata."""
    cert = CalibrationQuotient(3).certificate([1, 2, 3])
    bad_auth_cert = CalibrationQuotientCertificate(
        n_sites=cert.n_sites,
        cochain=cert.cochain,
        mean_circulation=cert.mean_circulation,
        quotient_norm=cert.quotient_norm,
        optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual,
        dual_witness=cert.dual_witness,
        primal_value=cert.primal_value,
        dual_value=cert.dual_value,
        duality_gap=cert.duality_gap,
        is_separated=cert.is_separated,
        evidence_scope=cert.evidence_scope,
        authority_effect="Granted",
    )
    assert bad_auth_cert.verify() is False


# ===========================================================================
# C09: Exact matrix indices can silently alias another entry
# ===========================================================================
def test_C09_exact_matrix_setter_rejects_out_of_range_coordinate() -> None:
    """C09: Matrix.__setitem__ must reject out-of-range coordinates."""
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(IndexError, match="out of range"):
        m[0, 2] = 99
    # Ensure entry (1, 0) was NOT modified
    assert m[1, 0] == 3


def test_C09_exact_matrix_extract_rejects_out_of_range_coordinate() -> None:
    """C09: Matrix.extract must reject nonexistent row or column coordinates."""
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(IndexError, match="out of range"):
        m.extract([0], [2])


# ===========================================================================
# C10: Used NumPy API exceeds the advertised dependency minimum
# ===========================================================================
def test_C10_numpy_api_matches_advertised_dependency_minimum(monkeypatch: pytest.MonkeyPatch) -> None:
    """C10: Duhamel sampling must succeed even when np.trapezoid is absent (as in NumPy 1.x)."""
    # Delete or hide np.trapezoid to emulate NumPy 1.x
    import numpy as np_mod
    if hasattr(np_mod, "trapezoid"):
        monkeypatch.delattr(np_mod, "trapezoid")

    # The function must smoothly fall back to np.trapz without raising AttributeError
    res = evaluate_observable_duhamel_bound(
        observable=[0],
        defects_by_edge={(0, 1): 0.5},
        time_horizon=0.1,
    )
    assert res.upper > 0.0
    assert math.isfinite(res.upper)


# ===========================================================================
# C11: Exact calibration coercion silently changes a NumPy float
# ===========================================================================
def test_C11_exact_calibration_rejects_numpy_binary_float() -> None:
    """C11: _to_fraction must reject numpy.float32 and numpy.float64 instead of coercing str."""
    f32_val = np.float32(0.1)
    f64_val = np.float64(0.1)

    with pytest.raises(TypeError, match="Float values not permitted"):
        _to_fraction(f32_val)

    with pytest.raises(TypeError, match="Float values not permitted"):
        _to_fraction(f64_val)

    # Valid exact rationals must still succeed
    assert _to_fraction(Fraction(1, 10)) == Fraction(1, 10)
    assert _to_fraction(5) == Fraction(5, 1)
    assert _to_fraction("1/10") == Fraction(1, 10)


# ===========================================================================
# C12: Observer certificates accept stale models and inconsistent numerical fields
# ===========================================================================
def test_C12_observer_certificates_recheck_models_and_inequalities() -> None:
    """C12: Observer certificates must verify primitive model data and reject stale or unadmitted values."""
    import dataclasses
    from sympy import Matrix as SpMatrix
    from observer_carriers import (
        JointInjectivityCertificate,
        LocalObserverCarrier,
        ObserverFamily,
        ObserverTallies,
        PassivityCertificate,
        PassivityRow,
        three_patch_certificate,
    )

    cert = three_patch_certificate(scale=1)
    assert cert.verify() is True

    # 1. Replacing family with identity observer maps must fail verification
    identity_observers = tuple(
        LocalObserverCarrier(
            obs.observer_id,
            {edge_id: [[1, 0, 0], [0, 1, 0], [0, 0, 1]] for edge_id in obs.maps},
        )
        for obs in cert.family.observers
    )
    stale_family = ObserverFamily(cert.family.edge_dimensions, identity_observers)
    stale_cert = dataclasses.replace(cert, family=stale_family)
    assert stale_cert.verify() is False

    # 2. Passivity must reject invalid inequality 100 <= 1
    bad_row = PassivityRow(
        observer_id="C1",
        observed_J=100,
        watched_raw_tally=1,
        raw_I=10,
        observed_le_watched=True,
        watched_le_raw=True,
    )
    bad_passivity = PassivityCertificate(rows=(bad_row,), holds=True)
    assert bad_passivity.verify() is False

    # 3. Negative rank in JointInjectivityCertificate must fail
    bad_inj = JointInjectivityCertificate(
        full_edge_coverage=True,
        edgewise_injective={"e1": True},
        edgewise_combined_rank={"e1": -1},
        premises_hold=True,
    )
    assert bad_inj.verify() is False

    # 4. Negative tallies must fail ObserverTallies.verify
    from sympy import Integer
    bad_tallies = ObserverTallies(I=Integer(-6), J={"C1": Integer(-6)}, Lambda=Integer(0))
    assert bad_tallies.verify() is False


# ===========================================================================
# C13: Finite-family admission and internal recheck do not enforce family contract
# ===========================================================================
def test_C13_family_bound_validates_contract_and_cardinalities() -> None:
    """C13: Family admission must reject fractional site/edge counts and verify member bounds non-emptiness."""
    import dataclasses
    from sympy import Rational
    from family_bound import (
        FiniteFamilyMember,
        UniformFamilyPremises,
        certify_uniform_family,
    )

    # 1. Fractional site_count must raise ValueError
    with pytest.raises(ValueError, match="site_count must be a positive integer"):
        FiniteFamilyMember(
            system_id="sys_frac",
            site_count=Rational(3, 2),  # type: ignore[arg-type]
            edge_count=3,
            local_interaction_norm=Rational(1),
            active_edge_rates=[Rational(1)],
        )

    # 2. Create valid certificate and test mutations
    member = FiniteFamilyMember("s1", site_count=2, edge_count=2, local_interaction_norm=1, active_edge_rates=[2, 2])
    premises = UniformFamilyPremises(g_star=1, eta_star=1, nu_star=2, a_star=1)
    cert = certify_uniform_family([member], premises, time=Rational(1, 100))
    assert cert.accepted is True
    assert cert.verify() is True

    # Mutate member_bounds to empty tuple
    empty_members_cert = dataclasses.replace(cert, member_bounds=())
    assert empty_members_cert.verify() is False

    # Mutate local_edge_polynomial to -999
    bad_poly_cert = dataclasses.replace(cert, local_edge_polynomial=Rational(-999))
    assert bad_poly_cert.verify() is False


# ===========================================================================
# C14: Higher-complex admission survives invalidation of d1*d0=0
# ===========================================================================
def test_C14_higher_complex_admission_enforces_differential_nilpotency() -> None:
    """C14: Admitted complex capability must enforce immutable differentials and d1*d0=0 at consumers."""
    import types
    from sympy import Matrix as SpMatrix
    from cochain_presentation import (
        AdmittedComplexV1,
        ObservationMap,
        ObservationPresentation,
    )

    # 1. Non-nilpotent d1*d0 != 0 must fail on admission
    with pytest.raises(ValueError, match="d1 \\* d0 != 0"):
        AdmittedComplexV1(d0=SpMatrix([[1], [0]]), d1=SpMatrix([[1, 0]]))

    # 2. Capability must be frozen/immutable or validated
    d0 = SpMatrix([[1], [0]])
    d1 = SpMatrix([[0, 1]])
    cap = AdmittedComplexV1(d0=d0, d1=d1)

    pres = ObservationPresentation(
        edge_order=["e1"],
        maps={"e1": ObservationMap("e1", SpMatrix([[1, 0], [0, 1]]))},
    )

    # 3. Induce must reject arbitrary object/SimpleNamespace
    with pytest.raises(TypeError, match="must be an AdmittedComplexV1 instance"):
        pres.induce({"e1": SpMatrix([1, 0])}, capability=types.SimpleNamespace(d0=d0, d1=d1))  # type: ignore[arg-type]


# ===========================================================================
# C15: Numerical derivative kill test treats NaNs as nonviolations
# ===========================================================================
def test_C15_numerical_derivative_kill_test_rejects_nans_and_invalids() -> None:
    """C15: SecondDerivativeBoundCertificate must reject NaNs, infinities, and negative norms."""
    from short_time_defect_numerical_certificate import SecondDerivativeBoundCertificate

    cert = SecondDerivativeBoundCertificate(g=1.0)

    # 1. NaN measured norms must raise ValueError
    with pytest.raises(ValueError, match="must be a finite nonnegative real"):
        cert.evaluate_assembly(
            measured_one_site_first_a=float("nan"),
            measured_one_site_first_b=float("nan"),
            measured_one_site_second_a=float("nan"),
            measured_one_site_second_b=float("nan"),
            measured_two_site_second=float("nan"),
        )

    # 2. Negative measured norm must raise ValueError
    with pytest.raises(ValueError, match="must be a finite nonnegative real"):
        cert.evaluate_assembly(1.0, 1.0, 1.0, 1.0, -5.0)

    # 3. NaN atol must raise ValueError
    with pytest.raises(ValueError, match="atol must be a finite nonnegative real"):
        cert.evaluate_assembly(1.0, 1.0, 1.0, 1.0, 1.0, atol=float("nan"))


# ===========================================================================
# C16: Artifact output collisions overwrite the certificate or hashed source
# ===========================================================================
def test_C16_artifact_output_separation_prevents_collisions(tmp_path: Any) -> None:
    """C16: write_artifact_bundle must reject certificate/manifest path aliasing."""
    from pathlib import Path
    from artifact_bundle import write_artifact_bundle

    same_path = tmp_path / "colliding_out.json"

    with pytest.raises(ValueError, match="must be distinct resolved files"):
        write_artifact_bundle(same_path, same_path)


# ===========================================================================
# C17: Positive report-factorization case is reported as factors=False
# ===========================================================================
def test_C17_dual_case_factorization_control() -> None:
    """C17: no_report_decision must report factors=True when fiber does not split valid."""
    from authorization_boundary import no_report_decision

    bools = (False, True)

    # 1. Identity report: valid is constant on fibers (fibers are singletons) -> factors=True
    res_id = no_report_decision(bools, lambda x: x, lambda x: bool(x))
    assert res_id.factors is True

    # 2. Constant valid predicate: factors=True
    res_const = no_report_decision(bools, lambda x: x, lambda x: True)
    assert res_const.factors is True

    # 3. Genuine split fiber: factors=False
    res_split = no_report_decision(bools, lambda x: (), lambda x: bool(x))
    assert res_split.factors is False


# ===========================================================================
# C18: Inline companion describes a different physical model from the one it calculates
# ===========================================================================
def test_C18_inline_companion_xx_model_documentation_binding() -> None:
    """C18: Example 6.1 helper must document the XX Hamiltonian and initial state |00><00|."""
    from inline_code_companion import run_example_61_bell_state_leakage

    eig_sum, formula_val = run_example_61_bell_state_leakage(np.pi / 8)
    assert math.isclose(eig_sum, formula_val, rel_tol=1e-10)

    doc = run_example_61_bell_state_leakage.__doc__ or ""
    assert "X_A X_B" in doc
    assert "|00><00|" in doc


# ===========================================================================
# C20: Axiom report is not a faithful per-declaration dependency receipt
# ===========================================================================
def test_C20_axiom_report_fidelity_and_no_blanket_on_definitional_proofs() -> None:
    """C20: lean4/axiom_report.txt must not assign blanket axioms to definitional theorems."""
    import pathlib
    import re

    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    axiom_report_path = package_root / "lean4" / "axiom_report.txt"
    assert axiom_report_path.exists(), "lean4/axiom_report.txt must exist"

    raw_bytes = axiom_report_path.read_bytes()
    assert b"\r\n" not in raw_bytes, "axiom_report.txt must use LF-only line endings"

    content = raw_bytes.decode("utf-8")

    # Definitional theorems must not be assigned blanket axiom sets
    definitional = [
        "AuthorizationBoundary.extra_recovers_negative",
        "PO000ProjectionFactor.residual_not_coboundary_without_adapter",
    ]
    for thm in definitional:
        assert thm in content, f"Expected {thm} in axiom report"
        pattern = re.compile(rf"'{re.escape(thm)}'\s+depends on axioms:\s*\[([^\]]+)\]")
        match = pattern.search(content)
        if match:
            axioms = [a.strip() for a in match.group(1).split(",") if a.strip()]
            assert not any(ax in ("Classical.choice", "Quot.sound", "propext") for ax in axioms), (
                f"Definitional theorem {thm} cannot depend on non-empty axioms {axioms}"
            )

    # Bare unqualified short names must not be present as targets
    for short_name in ("first_order_k1", "double_factor_k1", "double_factor_k2"):
        assert not re.search(rf"^'{re.escape(short_name)}'\s+depends on axioms:", content, re.MULTILINE), (
            f"Bare unqualified name '{short_name}' must be qualified with PO000.DoubleCommutatorEstimates"
        )


# ===========================================================================
# C21: Positive real-scalar commutator antecedent is uninhabited
# ===========================================================================
def test_C21_real_scalar_commutator_rate_bracket_vanishes_identically() -> None:
    """C21: Commutative Lie bracket [A, B] = AB - BA on Real vanishes identically."""
    import pathlib

    # Check symbolic / algebraic identity over commutative reals:
    # For any A, B in R, bracket(A, B) = A*B - B*A = 0
    # and doubleBracket(H, A) = bracket(bracket(H, A), H) = 0.
    test_reals = [(1.5, 2.3), (-4.0, 7.1), (0.0, 5.5), (1e-6, 1e6)]
    for A, B in test_reals:
        bracket = A * B - B * A
        assert bracket == 0.0
        double_bracket = (A * B - B * A) * A - A * (A * B - B * A)
        assert double_bracket == 0.0

    # Verify source file is labeled as LEAN_TOY / zero-commutator control
    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    rate_file = package_root / "lean4" / "po000_l003_double_commutator_rate.lean"
    assert rate_file.exists()
    rate_content = rate_file.read_text(encoding="utf-8")
    assert "zero-commutator" in rate_content.lower() or "toy" in rate_content.lower()


# ===========================================================================
# C22: Advertised structured commutator bounds are only coefficient nonnegativity
# ===========================================================================
def test_C22_double_commutator_bounds_scoped_to_factor_nonnegativity_arithmetic() -> None:
    """C22: DoubleCommutatorBounds asserts factor nonnegativity rather than operator bounds."""
    import pathlib

    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    estimates_file = package_root / "lean4" / "po000_l003_double_commutator_estimates.lean"
    assert estimates_file.exists()
    content = estimates_file.read_text(encoding="utf-8")

    # Verify that the structure only asserts factor * A_norm >= 0
    assert "firstOrderFactor k g * A_norm ≥ 0" in content
    assert "doubleCommutatorFactor k g * A_norm ≥ 0" in content

    # Verify that the module scope explicitly classifies it as factor arithmetic/nonnegativity
    assert "nonnegativity" in content.lower() or "arithmetic" in content.lower()


# ===========================================================================
# C23: Parked fixed-acceleration all-scales bound contradicts positive acceleration
# ===========================================================================
def test_C23_extrinsic_acceleration_scale_bound_contradiction_witness() -> None:
    """C23: For any a_e > 0, the rational witness g = a_e / (48(a_e + 1)) refutes a_e <= 24g^2."""
    import pathlib
    from fractions import Fraction

    # Check rational witness across multiple positive acceleration scales
    test_a_values = [
        Fraction(1, 1),
        Fraction(1, 10),
        Fraction(10, 1),
        Fraction(1, 1000),
        Fraction(48, 1),
    ]
    for a in test_a_values:
        g = a / (48 * (a + 1))
        assert g > 0, "g must be strictly positive"
        bound = 24 * (g ** 2)
        diff = a - bound
        assert diff > 0, f"Expected a > 24g^2 for a={a}, got diff={diff}"
        # Exact algebraic formula: diff = a * (96*a^2 + 191*a + 96) / (96*(a+1)^2)
        expected_diff = (a * (96 * (a ** 2) + 191 * a + 96)) / (96 * ((a + 1) ** 2))
        assert diff == expected_diff

    # Verify source file is quarantined and parked
    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    parked_file = package_root / "lean4" / "po000_beyond_paper_advancements.lean"
    assert parked_file.exists()
    parked_content = parked_file.read_text(encoding="utf-8")
    assert "parked" in parked_content.lower()
    assert "quarantine" in parked_content.lower()


# ===========================================================================
# AC2 / R1–R10 Regressions: Manuscript Anchors, Bibliography, and Specifications
# ===========================================================================

def test_republic_review_local_proof_anchors_resolve_in_manuscript() -> None:
    """AC2(a) / R5: Every local proof_anchor in claim ledgers must resolve in projection_obstruction.md."""
    import json
    import re
    import pathlib

    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    manuscript_path = package_root / "projection_obstruction.md"
    assert manuscript_path.is_file(), f"Manuscript missing: {manuscript_path}"
    manuscript_text = manuscript_path.read_text(encoding="utf-8")
    norm_text = re.sub(r"\s+", " ", manuscript_text)

    deps_path = package_root / "docs" / "claim_dependencies.json"
    assert deps_path.is_file(), f"claim_dependencies.json missing: {deps_path}"
    deps = json.loads(deps_path.read_text(encoding="utf-8"))

    unresolved: list[str] = []
    checked = 0
    for claim in deps.get("claims", []):
        cid = claim.get("id", "UNKNOWN")
        proof_file = claim.get("proof_file", "")
        anchor = claim.get("proof_anchor", "")
        disposition = claim.get("disposition", "local")

        if disposition in ("omitted", "imported_sibling", "archived_code"):
            continue
        if proof_file and proof_file != "projection_obstruction.md":
            continue
        if not anchor:
            continue

        checked += 1
        cleaned = anchor.strip()
        if cleaned.startswith("**") and cleaned.endswith("**"):
            cleaned = cleaned[2:-2].strip()
        cleaned = cleaned.rstrip(".:")

        if anchor not in manuscript_text and cleaned not in manuscript_text and cleaned not in norm_text:
            unresolved.append(f"Claim {cid}: {anchor!r}")

    assert unresolved == [], (
        f"{len(unresolved)} local proof anchors failed to resolve in projection_obstruction.md:\n"
        + "\n".join(f"  - {u}" for u in unresolved)
    )
    assert checked > 0, "No local claims checked"


def test_republic_review_every_bibliography_item_is_cited_in_body() -> None:
    """AC2(b) / R10: Every [n] in References must be cited in body text (zero orphan entries)."""
    import re
    import pathlib

    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    manuscript_path = package_root / "projection_obstruction.md"
    assert manuscript_path.is_file()
    content = manuscript_path.read_text(encoding="utf-8")

    ref_match = re.search(r"\n## References\s*\n", content)
    assert ref_match is not None, "Missing '## References' section"

    body_text = content[:ref_match.start()]
    references_text = content[ref_match.end():]

    ref_pattern = re.compile(r"^\s*(\d+)\.\s+(.+)$", re.MULTILINE)
    references = {int(m.group(1)): m.group(2).strip() for m in ref_pattern.finditer(references_text)}
    assert references, "No numbered references found"

    cleaned_body = re.sub(r"```[\s\S]*?```", "", body_text)
    cleaned_body = re.sub(r"`[^`\n]+`", "", cleaned_body)
    cleaned_body = re.sub(r"\$\$[\s\S]*?\$\$", "", cleaned_body)
    cleaned_body = re.sub(r"\$[^\$\n]+\$", "", cleaned_body)

    citation_brackets = re.findall(r"\[([0-9\s,\-\–]+)\](?!\()", cleaned_body)
    cited_in_body: set[int] = set()
    for bracket in citation_brackets:
        for part in bracket.split(","):
            part = part.strip()
            range_match = re.match(r"^(\d+)\s*(?:--|-|–)\s*(\d+)$", part)
            if range_match:
                for n in range(int(range_match.group(1)), int(range_match.group(2)) + 1):
                    cited_in_body.add(n)
            elif part.isdigit():
                cited_in_body.add(int(part))

    orphans = [num for num in sorted(references.keys()) if num not in cited_in_body]
    assert orphans == [], (
        f"Found {len(orphans)} orphan bibliography entries in References not cited in body: {orphans}"
    )

    missing = [num for num in sorted(cited_in_body) if num not in references]
    assert missing == [], f"Found citations in body missing from References: {missing}"


def test_republic_review_reference_36_historical_url_pin() -> None:
    """R4: Reference [36] (renumbered to [26]) URL pin must point to a valid revision without 404."""
    import re
    import pathlib

    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    content = (package_root / "projection_obstruction.md").read_text(encoding="utf-8")

    ref36_match = re.search(r"^\s*(?:26|36)\.\s+([^\n]+)", content, re.MULTILINE)
    assert ref36_match is not None, "Reference [36]/[26] not found"
    ref36 = ref36_match.group(1)

    valid = ("4a4fd192f" in ref36 and "crates_rs/omega_wdp/docs" in ref36) or (
        "4bdf074" in ref36 and "documentation/rust_crates/omega_wdp/docs" in ref36
    )
    assert valid, f"Reference [36]/[26] URL pin is invalid:\n{ref36}"


def test_republic_review_duhamel_variational_priors_cited() -> None:
    """R10: Martinazzo–Burghardt and Zoufal–Sutter–Woerner must be cited."""
    import pathlib

    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    content = (package_root / "projection_obstruction.md").read_text(encoding="utf-8").lower()
    assert "martinazzo" in content, "Martinazzo–Burghardt not cited in manuscript"
    assert "zoufal" in content, "Zoufal–Sutter–Woerner not cited in manuscript"


def test_republic_review_r1_po033_scope_attribution() -> None:
    """R1: PO-033 scope attribution must declare HEURISTIC_UNCERTIFIED without quadrature overclaim."""
    import pathlib

    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    content = (package_root / "projection_obstruction.md").read_text(encoding="utf-8")
    lower = content.lower()

    assert "heuristic_uncertified" in content, "Missing HEURISTIC_UNCERTIFIED classification for PO-033"
    assert "verified adaptive dynamics" not in lower, "Contains forbidden overclaim 'verified adaptive dynamics'"
    assert "quadrature certification" not in lower, "Contains forbidden overclaim 'quadrature certification'"


def test_republic_review_r2_authoritative_reference_table_and_cut_material() -> None:
    """R2: No nonexistent PO-004/005 claims and cut material is pinned to historical revisions."""
    import re
    import pathlib

    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    content = (package_root / "projection_obstruction.md").read_text(encoding="utf-8")

    assert not re.search(r"\bPO-004\b", content), "Found nonexistent PO-004 reference"
    assert not re.search(r"\bPO-005\b", content), "Found nonexistent PO-005 reference"
    assert "90e6231546" in content or "d44f760555" in content, "Missing historical commit pin for cut material"


def test_republic_review_r10_scaffolding_and_formatting() -> None:
    """R10: Legacy house scaffolding terms and LaTeX malformations removed."""
    import pathlib

    package_root = pathlib.Path(__file__).resolve().parent.parent.parent
    content = (package_root / "projection_obstruction.md").read_text(encoding="utf-8")

    for term in ["Sovereign Mathematical Scope", "Relative Path in Estate", "Modular Delegation"]:
        assert term not in content, f"Legacy scaffolding term '{term}' still present in manuscript"
    assert " ^3$" not in content and "under a ^3$" not in content, "Malformed LaTeX '^3$' present in manuscript"



