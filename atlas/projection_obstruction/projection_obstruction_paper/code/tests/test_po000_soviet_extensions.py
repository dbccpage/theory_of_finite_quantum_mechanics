"""Soviet coverage for PO-000 modules beyond the original deep-coverage file."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))


# --- 13. FFI & Measurement Call Soviet Inspection ---

def test_ffi_measurement_call_error_branches(monkeypatch):
    """Test every refusal and validation branch of ffi.measurement_call."""
    import ffi

    # An installed adapter never opts a standalone replay into native execution.
    monkeypatch.delenv("PO000_NATIVE_INTEGRATION", raising=False)
    with pytest.raises(ffi.NativeMeasurementUnavailable, match="NATIVE_INTEGRATION_NOT_REQUESTED"):
        ffi.measurement_call("test_action", {})

    # Branch 1: native integration requested but adapter unavailable
    monkeypatch.setenv("PO000_NATIVE_INTEGRATION", "1")
    # The retired owner cannot stand in for the current canonical adapter.
    _missing_module = object()
    _previous_retired_adapter = sys.modules.get(
        "omega_engine_operating_system.python.adapters.rust_host.ffi", _missing_module
    )
    _previous_host_adapter = _missing_module
    _host_adapter_saved = False
    _previous_rop_result = _missing_module
    _rop_result_saved = False
    try:
        sys.modules["omega_engine_operating_system.python.adapters.rust_host.ffi"] = None
        _previous_host_adapter = sys.modules.get(
            "omega_engine_operating_system.adapters.rust_host.ffi", _missing_module
        )
        _host_adapter_saved = True
        sys.modules["omega_engine_operating_system.adapters.rust_host.ffi"] = None
        with pytest.raises(ffi.NativeMeasurementUnavailable, match="NATIVE_ADAPTER_UNAVAILABLE"):
            ffi.measurement_call("test_action", {})

        # Mock ROP Err and Ok for testing the return branches
        class MockError:
            def __init__(self, code: str):
                self.code = code

        class MockErr:
            def __init__(self, error: MockError):
                self.error = error

        class MockHost:
            def __init__(self, resp):
                self._resp = resp

            def invoke_runtime(self, action, payload):
                return self._resp

        # Branch 2: response is an Err
        class FakeModuleErr:
            def RustSymbolGameHost(self):
                return MockHost(MockErr(MockError("RUST_DEFECT_ERR")))

        class FakeRopModule:
            Err = MockErr

        sys.modules["omega_engine_operating_system.adapters.rust_host.ffi"] = FakeModuleErr()
        _previous_rop_result = sys.modules.get(
            "omega_engine_operations.domain.rop.result", _missing_module
        )
        _rop_result_saved = True
        sys.modules["omega_engine_operations.domain.rop.result"] = FakeRopModule()

        with pytest.raises(ffi.NativeMeasurementUnavailable, match="RUST_DEFECT_ERR"):
            ffi.measurement_call("action", {})

        # Branch 3: outcome['success'] is not True
        class MockOk:
            def __init__(self, val):
                self.value = val

        class FakeModuleUnsuccessful:
            def RustSymbolGameHost(self):
                return MockHost(MockOk({"success": False, "error": "MEAS_FAILED"}))

        sys.modules["omega_engine_operating_system.adapters.rust_host.ffi"] = (
            FakeModuleUnsuccessful()
        )
        with pytest.raises(ffi.NativeMeasurementUnavailable, match="MEAS_FAILED"):
            ffi.measurement_call("action", {})

        # Branch 4: result is not a dict
        class FakeModuleNonDictResult:
            def RustSymbolGameHost(self):
                return MockHost(MockOk({"success": True, "result": "not_a_dict"}))

        sys.modules["omega_engine_operating_system.adapters.rust_host.ffi"] = (
            FakeModuleNonDictResult()
        )
        with pytest.raises(ValueError, match="invalid measurement outcome"):
            ffi.measurement_call("action", {})

        # Branch 5: result has invalid authority_effect
        class FakeModuleWrongAuthority:
            def RustSymbolGameHost(self):
                return MockHost(
                    MockOk({"success": True, "result": {"authority_effect": "BINDING"}})
                )

        sys.modules["omega_engine_operating_system.adapters.rust_host.ffi"] = (
            FakeModuleWrongAuthority()
        )
        with pytest.raises(ValueError, match="invalid measurement outcome or authority ceiling"):
            ffi.measurement_call("action", {})

        # Branch 6: valid outcome
        expected_result = {"authority_effect": "None", "measured_distance": 0.42}

        class FakeModuleSuccess:
            def RustSymbolGameHost(self):
                return MockHost(MockOk({"success": True, "result": expected_result}))

        sys.modules["omega_engine_operating_system.adapters.rust_host.ffi"] = FakeModuleSuccess()
        res = ffi.measurement_call("action", {})
        assert res == expected_result
    finally:
        if _rop_result_saved:
            if _previous_rop_result is _missing_module:
                sys.modules.pop("omega_engine_operations.domain.rop.result", None)
            else:
                sys.modules["omega_engine_operations.domain.rop.result"] = _previous_rop_result
        if _host_adapter_saved:
            if _previous_host_adapter is _missing_module:
                sys.modules.pop("omega_engine_operating_system.adapters.rust_host.ffi", None)
            else:
                sys.modules["omega_engine_operating_system.adapters.rust_host.ffi"] = (
                    _previous_host_adapter
                )
        if _previous_retired_adapter is _missing_module:
            sys.modules.pop("omega_engine_operating_system.python.adapters.rust_host.ffi", None)
        else:
            sys.modules["omega_engine_operating_system.python.adapters.rust_host.ffi"] = (
                _previous_retired_adapter
            )


# --- 14. Finite Certificates & Verify Finite Records Soviet Inspection ---

def test_finite_certificates_and_verify_records_soviet_coverage(monkeypatch):
    """Exercise all error branches in finite_certificates and verify_finite_certificates."""
    import finite_certificates
    import verify_finite_certificates
    from finite_inputs import measurement_requests

    # Branch 1: build_finite_certificates with request mismatch raises ValueError
    requests = measurement_requests()
    tampered_cert = {"request": {"different": True}}
    monkeypatch.setattr("finite_certificates.measurement_call", lambda act, req: tampered_cert)
    with pytest.raises(ValueError, match="native certificate is not bound"):
        finite_certificates.build_finite_certificates()

    # Branch 2: build_finite_certificates with verified native cert
    monkeypatch.setattr("finite_certificates.measurement_call", lambda act, req: {"request": req})
    certs = finite_certificates.build_finite_certificates()
    assert certs[next(iter(requests.keys()))]["status"] == "verified"

    # Branch 3: verify_finite_records inventory check
    assert verify_finite_certificates.verify_finite_records("not_dict") == ["finite certificate inventory mismatch"]
    assert verify_finite_certificates.verify_finite_records({"wrong": 1}) == ["finite certificate inventory mismatch"]

    # Build valid base inventory
    base_inv = {
        name: {"status": "refused", "reason": "REFUSED_OK"}
        for name in ["separable_correlated", "three_factor", "ising_five_cycle", "commuting_boundary", "rotating_polynomial"]
    }
    assert verify_finite_certificates.verify_finite_records(base_inv) == []

    # Record not a dict
    bad_inv1 = dict(base_inv)
    bad_inv1["separable_correlated"] = "not_a_dict"
    assert any("invalid record" in err for err in verify_finite_certificates.verify_finite_records(bad_inv1))

    # Invalid refused record (missing reason or extra keys)
    bad_inv2 = dict(base_inv)
    bad_inv2["separable_correlated"] = {"status": "refused"}
    assert any("invalid capability refusal" in err for err in verify_finite_certificates.verify_finite_records(bad_inv2))

    bad_inv2b = dict(base_inv)
    bad_inv2b["separable_correlated"] = {"status": "refused", "reason": 123}
    assert any("invalid capability refusal" in err for err in verify_finite_certificates.verify_finite_records(bad_inv2b))

    # Invalid status
    bad_inv3 = dict(base_inv)
    bad_inv3["separable_correlated"] = {"status": "pending"}
    assert any("invalid finite evidence status" in err for err in verify_finite_certificates.verify_finite_records(bad_inv3))

    # Verified measurement record with request mismatch
    bad_inv4 = dict(base_inv)
    bad_inv4["separable_correlated"] = {
        "status": "verified",
        "certificate": {"request": {"mismatch": True}, "input_digest": "abc"}
    }
    monkeypatch.setattr("verify_finite_certificates.measurement_call", lambda act, payload: {"accepted": True, "input_digest": "abc"})
    errs4 = verify_finite_certificates.verify_finite_records(bad_inv4)
    assert any("measurement request differs" in err for err in errs4)

    # Verified measurement record with rejected replay
    req = requests["separable_correlated"]
    bad_inv5 = dict(base_inv)
    bad_inv5["separable_correlated"] = {
        "status": "verified",
        "certificate": {"request": req, "input_digest": "digest_a"}
    }
    monkeypatch.setattr("verify_finite_certificates.measurement_call", lambda act, payload: {"accepted": False, "input_digest": "digest_a"})
    errs5 = verify_finite_certificates.verify_finite_records(bad_inv5)
    assert any("native mathematical replay rejected" in err for err in errs5)


# --- 15. Calibration Quotient Soviet Deep Coverage ---

def test_calibration_quotient_soviet_deep_coverage():
    """Exercise all input validations, tamper detection, and error paths in calibration_quotient.py."""
    from fractions import Fraction

    import calibration_quotient

    # _to_fraction guards
    with pytest.raises(TypeError, match="Boolean"):
        calibration_quotient._to_fraction(True)
    with pytest.raises(TypeError, match="Boolean"):
        calibration_quotient._to_fraction(False)
    with pytest.raises(TypeError, match="Float"):
        calibration_quotient._to_fraction(1.5)
    with pytest.raises(TypeError, match="Cannot convert"):
        calibration_quotient._to_fraction(object())

    class RatioObj:
        def __init__(self, p, q):
            self.p = p
            self.q = q
    assert calibration_quotient._to_fraction(RatioObj(3, 7)) == Fraction(3, 7)

    # OperationalMeasurementSet length checks
    meas = calibration_quotient.OperationalMeasurementSet(3)
    with pytest.raises(ValueError, match="mu_K length"):
        meas.construct_cochain_from_moments([1, 2], [1, 2, 3], [1, 2, 3])
    with pytest.raises(ValueError, match="mu_X length"):
        meas.construct_cochain_from_moments([1, 2, 3], [1, 2], [1, 2, 3])
    with pytest.raises(ValueError, match="mu_Z length"):
        meas.construct_cochain_from_moments([1, 2, 3], [1, 2, 3], [1, 2])

    # NuisanceModel guards
    with pytest.raises(ValueError, match="at least 3 sites"):
        calibration_quotient.NuisanceModel(2)

    nm = calibration_quotient.NuisanceModel(3)
    with pytest.raises(ValueError, match="Potential length"):
        nm.coboundary([1, 2])
    with pytest.raises(ValueError, match="Vector length"):
        nm.is_exact_coboundary([1, 2])
    with pytest.raises(ValueError, match="nominal_cochain length"):
        nm.apply_detector_gain_drift([1, 2], [1, 2, 3])
    with pytest.raises(ValueError, match="local_gains length"):
        nm.apply_detector_gain_drift([1, 2, 3], [1, 2])
    with pytest.raises(ValueError, match="nominal_cochain length"):
        nm.apply_multiplicative_gain_drift([1, 2], 2)

    # CalibrationQuotient initialization and bounds
    with pytest.raises(ValueError, match="at least 3 sites"):
        calibration_quotient.CalibrationQuotient(2)

    cq = calibration_quotient.CalibrationQuotient(3)
    with pytest.raises(ValueError, match="Cochain length"):
        cq.mean_circulation([1, 2])
    with pytest.raises(ValueError, match="Cochain length"):
        cq.optimal_repair_potential([1, 2])

    # dual_witness branches: ell > 0, ell < 0, ell == 0
    assert cq.dual_witness([1, 1, 1]) == (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3))
    assert cq.dual_witness([-1, -1, -1]) == (Fraction(-1, 3), Fraction(-1, 3), Fraction(-1, 3))
    assert cq.dual_witness([1, -1, 0]) == (Fraction(0), Fraction(0), Fraction(0))

    # cohomological_projection
    proj_class, proj_cob = cq.cohomological_projection([Fraction(2), Fraction(0), Fraction(1)])
    assert proj_class == Fraction(1)
    assert sum(proj_cob) == Fraction(0)

    # verify_coarse_graining_invariance errors
    with pytest.raises(ValueError, match="must equal n_sites"):
        cq.verify_coarse_graining_invariance([1, 2, 3], [1, 1])
    with pytest.raises(ValueError, match="strictly positive"):
        cq.verify_coarse_graining_invariance([1, 2, 3], [0, 3])

    # verify_multiplicative_gain_budget
    budget_res = cq.verify_multiplicative_gain_budget([Fraction(1), Fraction(2), Fraction(3)], gain=2)
    assert budget_res["status"] == "pass"

    # CalibrationQuotientCertificate comprehensive tamper detection
    cert = cq.certificate([Fraction(1), Fraction(2), Fraction(3)])
    assert cert.verify() is True

    # Tamper 1: cochain len
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=(Fraction(1), Fraction(2)), optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual, dual_witness=cert.dual_witness, primal_value=cert.primal_value,
        dual_value=cert.dual_value, duality_gap=cert.duality_gap, quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 2: potential len
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=(Fraction(0),),
        optimal_residual=cert.optimal_residual, dual_witness=cert.dual_witness, primal_value=cert.primal_value,
        dual_value=cert.dual_value, duality_gap=cert.duality_gap, quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 3: residual len
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=(Fraction(0),), dual_witness=cert.dual_witness, primal_value=cert.primal_value,
        dual_value=cert.dual_value, duality_gap=cert.duality_gap, quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 4: dual witness len
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual, dual_witness=(Fraction(0),), primal_value=cert.primal_value,
        dual_value=cert.dual_value, duality_gap=cert.duality_gap, quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 5: residual values mismatch
    bad_res = tuple(r + Fraction(1) for r in cert.optimal_residual)
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=bad_res, dual_witness=cert.dual_witness, primal_value=cert.primal_value,
        dual_value=cert.dual_value, duality_gap=cert.duality_gap, quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 6: primal value mismatch
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual, dual_witness=cert.dual_witness, primal_value=Fraction(999),
        dual_value=cert.dual_value, duality_gap=cert.duality_gap, quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 7: non-constant dual witness
    bad_dual = (Fraction(1, 3), Fraction(0), Fraction(1, 3))
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual, dual_witness=bad_dual, primal_value=cert.primal_value,
        dual_value=cert.dual_value, duality_gap=cert.duality_gap, quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 8: dual witness exceeding 1/n
    big_dual = (Fraction(2, 3), Fraction(2, 3), Fraction(2, 3))
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual, dual_witness=big_dual, primal_value=cert.primal_value,
        dual_value=cert.dual_value, duality_gap=cert.duality_gap, quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 9: dual value mismatch
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual, dual_witness=cert.dual_witness, primal_value=cert.primal_value,
        dual_value=Fraction(999), duality_gap=cert.duality_gap, quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 10: non-zero duality gap
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual, dual_witness=cert.dual_witness, primal_value=cert.primal_value,
        dual_value=cert.dual_value, duality_gap=Fraction(1), quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 11: primal != dual
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual, dual_witness=cert.dual_witness, primal_value=Fraction(2),
        dual_value=Fraction(1), duality_gap=Fraction(0), quotient_norm=Fraction(2),
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 12: quotient_norm != primal
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual, dual_witness=cert.dual_witness, primal_value=cert.primal_value,
        dual_value=cert.dual_value, duality_gap=cert.duality_gap, quotient_norm=Fraction(999),
        mean_circulation=cert.mean_circulation, is_separated=cert.is_separated
    ).verify()

    # Tamper 13: is_separated mismatch
    assert not calibration_quotient.CalibrationQuotientCertificate(
        n_sites=3, cochain=cert.cochain, optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual, dual_witness=cert.dual_witness, primal_value=cert.primal_value,
        dual_value=cert.dual_value, duality_gap=cert.duality_gap, quotient_norm=cert.quotient_norm,
        mean_circulation=cert.mean_circulation, is_separated=False
    ).verify()

    # evaluate_nuisance_invariance input errors
    with pytest.raises(ValueError, match="at least 3 sites"):
        calibration_quotient.evaluate_nuisance_invariance([1, 2], [0, 0])
    with pytest.raises(ValueError, match="does not match"):
        calibration_quotient.evaluate_nuisance_invariance([1, 2, 3], [0, 0])


# --- 16. Short-Time Jets Soviet Deep Coverage ---

def test_short_time_jets_soviet_deep_coverage():
    """Exercise all input error paths and exact examples in short_time_jets.py."""
    import short_time_jets
    import sympy as sp

    h2 = sp.eye(2)
    r2 = sp.eye(2)
    r3 = sp.eye(3)

    # state_jets errors
    with pytest.raises(ValueError, match="nonnegative order"):
        short_time_jets.state_jets(h2, r2, order=-1)
    with pytest.raises(ValueError, match="matching square matrices"):
        short_time_jets.state_jets(h2, r3, order=1)

    # defect_jets errors
    with pytest.raises(ValueError, match="ordered pair of distinct sites"):
        short_time_jets.defect_jets(sp.eye(4), sp.eye(4), (2, 2), edge=(1, 0), order=1)
    with pytest.raises(ValueError, match="ordered pair of distinct sites"):
        short_time_jets.defect_jets(sp.eye(4), sp.eye(4), (2, 2), edge=(0, 0), order=1)
    with pytest.raises(ValueError, match="ordered pair of distinct sites"):
        short_time_jets.defect_jets(sp.eye(8), sp.eye(8), (2, 2, 2), edge=(0, 1, 2), order=1)

    # remainder_bound & derivative_factor errors
    with pytest.raises(ValueError, match="nonnegative Taylor order"):
        short_time_jets.remainder_bound(order=-1, g=1, t=1)
    with pytest.raises(ValueError, match="nonnegative derivative order"):
        short_time_jets.derivative_factor(order=-1)

    # exact_examples execution
    examples = short_time_jets.exact_examples()
    assert "ising_zero_first" in examples
    assert "quadratic_example_second" in examples


# --- 17. Derivation Replays Soviet Deep Coverage ---

def test_derivation_replays_soviet_deep_coverage():
    """Exercise input validations and exact summary in derivation_replays.py."""
    import derivation_replays
    import sympy as sp

    # _exact_scalar errors
    with pytest.raises(TypeError, match="exact scalar required"):
        derivation_replays._exact_scalar(3.14)
    with pytest.raises(ValueError, match="finite exact scalar"):
        derivation_replays._exact_scalar(sp.nan)

    # _dimensions errors
    with pytest.raises(ValueError, match="nonempty positive integer"):
        derivation_replays._dimensions(())
    with pytest.raises(ValueError, match="nonempty positive integer"):
        derivation_replays._dimensions((2, -1))

    # hermitian_trace_norm errors
    non_hermitian = sp.Matrix([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="Hermitian matrix required"):
        derivation_replays.hermitian_trace_norm(non_hermitian)

    # mixed_certificate errors
    with pytest.raises(TypeError, match="exact rational factors"):
        derivation_replays.mixed_certificate(sp.Rational(1, 2), "not_rational")
    with pytest.raises(ValueError, match="full-rank rational factors"):
        derivation_replays.mixed_certificate(sp.Rational(0, 1), sp.Rational(1, 2))

    # support_component errors
    rho4 = sp.eye(4) / 4
    with pytest.raises(ValueError, match="ordered support required"):
        derivation_replays.support_component(rho4, (2, 2), support=(1, 0))
    with pytest.raises(ValueError, match="ordered support required"):
        derivation_replays.support_component(rho4, (2, 2), support=(2,))

    # single site support_component (remaining == ())
    rho2 = sp.eye(2) / 2
    res_single = derivation_replays.support_component(rho2, (2,), support=(0,))
    assert res_single.rows == 2

    # cumulant_constants error
    with pytest.raises(ValueError, match="positive support size"):
        derivation_replays.cumulant_constants(0)

    # exact_summary execution
    summary = derivation_replays.exact_summary()
    assert summary["scope"].startswith("Exact finite examples")
    assert summary["cycle_purity"] is True


# --- 18. Evidence Soviet Deep Coverage ---

def test_evidence_soviet_deep_coverage(tmp_path):
    """Exercise data model validations and claim universe loading in evidence.py."""
    import evidence
    from evidence import ClaimEvidence, MechanizationRun

    # load_required_claim_ids errors
    with pytest.raises(FileNotFoundError, match="claim ledger is required"):
        evidence.load_required_claim_ids(tmp_path / "nonexistent.yaml")

    empty_ledger = tmp_path / "empty.yaml"
    empty_ledger.write_text("# empty comment only\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no claim rows parsed"):
        evidence.load_required_claim_ids(empty_ledger)

    # ClaimEvidence validations
    with pytest.raises(ValueError, match="claim_ids must be a nonempty"):
        ClaimEvidence(claim_ids=(), title="T", evidence_kind="exact_finite", verdict="pass", statement_scope="s", algorithm="a", witness={})
    with pytest.raises(ValueError, match="authority_effect must be the literal string None"):
        ClaimEvidence(claim_ids=("V1",), title="T", evidence_kind="exact_finite", verdict="pass", statement_scope="s", algorithm="a", witness={}, authority_effect="INVALID")
    with pytest.raises(ValueError, match="witness must be a dict"):
        ClaimEvidence(claim_ids=("V1",), title="T", evidence_kind="exact_finite", verdict="pass", statement_scope="s", algorithm="a", witness="not_a_dict")

    # MechanizationRun validations
    valid_ev = ClaimEvidence(
        claim_ids=("V1-TEST",), title="T", evidence_kind="exact_finite", verdict="pass", statement_scope="s", algorithm="a", witness={}
    )
    with pytest.raises(ValueError, match="unexpected schema_version"):
        MechanizationRun(
            paper_version="6.9.15", python_package_version="6.9.5", results=(valid_ev,),
            unresolved_claim_ids=(), execution_completed=True, executable_checks_passed=True,
            open_obligations_present=False, refusals_present=False, claim_disposition_complete=False,
            promotion_eligible=False, schema_version="wrong_schema"
        )
    with pytest.raises(ValueError, match="unexpected paper_id"):
        MechanizationRun(
            paper_version="6.9.15", python_package_version="6.9.5", results=(valid_ev,),
            unresolved_claim_ids=(), execution_completed=True, executable_checks_passed=True,
            open_obligations_present=False, refusals_present=False, claim_disposition_complete=False,
            promotion_eligible=False, paper_id="WRONG_ID"
        )
    with pytest.raises(ValueError, match="promotion_eligible must be false"):
        MechanizationRun(
            paper_version="6.9.15", python_package_version="6.9.5", results=(valid_ev,),
            unresolved_claim_ids=(), execution_completed=True, executable_checks_passed=True,
            open_obligations_present=False, refusals_present=False, claim_disposition_complete=False,
            promotion_eligible=True
        )
    with pytest.raises(ValueError, match="authority_effect must be the literal string None"):
        MechanizationRun(
            paper_version="6.9.15", python_package_version="6.9.5", results=(valid_ev,),
            unresolved_claim_ids=(), execution_completed=True, executable_checks_passed=True,
            open_obligations_present=False, refusals_present=False, claim_disposition_complete=False,
            promotion_eligible=False, authority_effect="INVALID"
        )
    with pytest.raises(ValueError, match="execution_completed must be true"):
        MechanizationRun(
            paper_version="6.9.15", python_package_version="6.9.5", results=(valid_ev,),
            unresolved_claim_ids=(), execution_completed=False, executable_checks_passed=True,
            open_obligations_present=False, refusals_present=False, claim_disposition_complete=False,
            promotion_eligible=False
        )


# --- 19. Cochain Presentation Soviet Deep Coverage ---

def test_cochain_presentation_soviet_deep_coverage():
    """Exercise complex composition, presentation validation, and repair problems."""
    import cochain_presentation
    from exactsym import Matrix

    # AdmittedComplexV1 dimension and d1 * d0 checks
    d0_bad = Matrix([[1], [2]])  # 2x1
    d1_bad_dim = Matrix([[1, 2, 3]])  # 1x3
    with pytest.raises(ValueError, match="dimensions do not compose"):
        cochain_presentation.AdmittedComplexV1(d0=d0_bad, d1=d1_bad_dim)

    d1_bad_comp = Matrix([[1, 1]])  # 1x2, d1 * d0 = 3 != 0
    with pytest.raises(ValueError, match="complex composition failed"):
        cochain_presentation.AdmittedComplexV1(d0=d0_bad, d1=d1_bad_comp)

    # ObservationPresentation domain checks
    with pytest.raises(ValueError, match="at least one edge"):
        cochain_presentation.ObservationPresentation(edge_order=[], maps={})
    om = cochain_presentation.ObservationMap("e1", Matrix([[1]]))
    with pytest.raises(ValueError, match="duplicates"):
        cochain_presentation.ObservationPresentation(edge_order=["e1", "e1"], maps={"e1": om})
    with pytest.raises(ValueError, match="domain mismatch"):
        om2 = cochain_presentation.ObservationMap("e2", Matrix([[1]]))
        cochain_presentation.ObservationPresentation(edge_order=["e1"], maps={"e1": om, "e2": om2})
    with pytest.raises(ValueError, match="keys must match their edge_id"):
        om_wrong = cochain_presentation.ObservationMap("e_different", Matrix([[1]]))
        cochain_presentation.ObservationPresentation(edge_order=["e1"], maps={"e1": om_wrong})

    # induce_field extra edge check
    pres = cochain_presentation.ObservationPresentation(edge_order=["e1"], maps={"e1": om})
    with pytest.raises(cochain_presentation.MissingObservationMapError, match="without declared maps"):
        pres.induce_field({"e1": Matrix([[1]]), "extra": Matrix([[2]])})

    # LinearRepairProblem
    m_repair = Matrix([[1, 0], [0, 1], [1, 1]])
    cochain = Matrix([[2], [3], [5]])  # exact coboundary
    prob = cochain_presentation.LinearRepairProblem(m_repair)
    cert_exact = prob.exactness_certificate(cochain)
    assert cert_exact.verify() is True
    assert cert_exact.is_exact_coboundary is True

    # Obstructed cochain
    cochain_obs = Matrix([[2], [3], [0]])
    cert_obs = prob.exactness_certificate(cochain_obs)
    assert cert_obs.verify() is True
    assert cert_obs.is_exact_coboundary is False


# --- 20. Observation Tradeoffs & Entanglement Deep Coverage ---

def test_observation_tradeoffs_and_entanglement_deep_coverage():
    """Exercise edge cases in observation_tradeoffs and entanglement_production."""
    import entanglement_production
    import numpy as np
    import observation_tradeoffs

    # Entanglement production edge cases
    zero_state = np.zeros((2, 2), dtype=np.complex128)
    assert entanglement_production.renyi_entropy(zero_state, alpha=2.0) == 0.0

    rho_diag = np.diag([0.7, 0.3]).astype(np.complex128)
    assert entanglement_production.renyi_entropy(rho_diag, alpha=0.5) > 0.0
    assert entanglement_production.von_neumann_entropy(rho_diag) > 0.0

    with pytest.raises(ValueError, match="keep must be 'a' or 'b'"):
        entanglement_production.partial_trace_bipartite(np.eye(4, dtype=np.complex128), 2, 2, keep="invalid")

    with pytest.raises(ValueError, match="rho must be 4x4"):
        entanglement_production.two_qubit_concurrence(np.eye(2, dtype=np.complex128))

    # Observation tradeoffs edge cases
    with pytest.raises(ValueError, match="disconnected"):
        observation_tradeoffs.steiner_tree_onset_order(
            edges=[(0, 1), (2, 3)], support=[0, 3]
        )

    # DifferenceSetStateFamily validations
    with pytest.raises(ValueError, match="num_qubits must be an integer"):
        observation_tradeoffs.DifferenceSetStateFamily(num_qubits=0)
    with pytest.raises(ValueError, match="num_qubits must be an integer"):
        observation_tradeoffs.DifferenceSetStateFamily(num_qubits=True)
    with pytest.raises(ValueError, match="unknown family_type"):
        observation_tradeoffs.DifferenceSetStateFamily(num_qubits=2, family_type="invalid")

    fam = observation_tradeoffs.DifferenceSetStateFamily(num_qubits=2)
    with pytest.raises(ValueError, match="support must be nonempty"):
        fam.generate_state_pair(support=[])
    with pytest.raises(ValueError, match="invalid support site index"):
        fam.generate_state_pair(support=[99])

    with pytest.raises(ValueError, match="order must be >= 1"):
        fam.compute_krylov_observability_matrix(np.eye(4), np.eye(4), order=0)
    with pytest.raises(ValueError, match="matrix shapes must match"):
        fam.compute_krylov_observability_matrix(np.eye(2), np.eye(4), order=1)

    zero_mat = np.zeros((4, 4), dtype=np.complex128)
    cond = fam.compute_krylov_conditioning(zero_mat, zero_mat, order=1)
    assert cond == float("inf")

    state = observation_tradeoffs._bloch_state(1.5, 0.0, 0.0)
    assert abs(np.trace(state) - 1.0) < 1e-12


# --- 21. Tangent Cone & Eval Auth Factor Deep Coverage ---

def test_tangent_cone_and_eval_auth_factor_deep_coverage():
    """Exercise eval_auth_factor TypeError branches and TangentCone geometry."""
    import eval_auth_factor
    import falsification_sandbox
    import feasible_tangent_cone
    import numpy as np

    # eval_auth_factor TypeErrors
    with pytest.raises(TypeError, match="Expected Pair instance"):
        eval_auth_factor.p_prod("not_a_pair")
    with pytest.raises(TypeError, match="Expected Pair instance"):
        eval_auth_factor.valid_hidden("not_a_pair")
    with pytest.raises(TypeError, match="Expected Pair instance"):
        eval_auth_factor.eval_hidden("not_a_pair")

    # falsification_sandbox assert_all_breaks_trip failure
    failed_item = falsification_sandbox.FalsificationResult(
        name="synthetic_break", broken_hypothesis="synthetic_break", expected_failure=True, residual=0.0, detail="did not trip"
    )
    with pytest.raises(RuntimeError, match="synthetic_break"):
        falsification_sandbox.assert_all_breaks_trip([failed_item])

    # TangentCone dimension mismatch on distance
    cone = feasible_tangent_cone.AmbientFeasibleTangentCone(np.eye(2, dtype=np.complex128) / 2)
    with pytest.raises(feasible_tangent_cone.BoundaryGeometryError, match="dimension"):
        cone.distance(np.zeros((3, 3), dtype=np.complex128))

    rank1 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128)
    cone_rank1 = feasible_tangent_cone.AmbientFeasibleTangentCone(rank1)
    infeasible_dir = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
    assert cone_rank1.is_feasible(infeasible_dir) is False

    full_rank = np.eye(2, dtype=np.complex128) / 2
    cone_full = feasible_tangent_cone.AmbientFeasibleTangentCone(full_rank)
    assert cone_full.distance(infeasible_dir) == 0.0


# --- 22. Additional Edge Branches for 95%+ Target ---

def test_additional_edge_branches_for_target_coverage():
    """Exercise remaining uncovered branches in cochain_presentation, covering_edge, family_bound, and evidence."""
    import cochain_presentation
    import covering_edge
    import family_bound
    from exactsym import Matrix, Rational

    # 1. cochain_presentation: induce with capability
    om = cochain_presentation.ObservationMap("e1", Matrix([[1]]))
    pres = cochain_presentation.ObservationPresentation(edge_order=["e1"], maps={"e1": om})
    d0 = Matrix([[1]])
    d1 = Matrix([[0]])
    cap = cochain_presentation.AdmittedComplexV1(d0=d0, d1=d1)
    admitted = pres.induce({"e1": Matrix([[2]])}, capability=cap)
    assert admitted.field.as_vector()[0, 0] == Rational(2)

    # Capability dimension mismatch
    d0_bad = Matrix([[1], [0]])
    d1_bad = Matrix([[0, 0]])
    cap_bad = cochain_presentation.AdmittedComplexV1(d0=d0_bad, d1=d1_bad)
    with pytest.raises(ValueError, match="stacked observed field dimension"):
        pres.induce({"e1": Matrix([[2]])}, capability=cap_bad)

    # LinearRepairProblem shape mismatch
    prob = cochain_presentation.LinearRepairProblem(Matrix([[1]]))
    with pytest.raises(ValueError, match="cochain has shape"):
        prob.exactness_certificate(Matrix([[1, 2]]))
    with pytest.raises(ValueError, match="cochain has shape"):
        prob.quotient_l1_distance(Matrix([[1, 2]]))

    # ExactnessCertificate verify() returning False when separating vector is None
    cert_false = cochain_presentation.ExactnessCertificate(
        is_exact_coboundary=False,
        cochain=Matrix([[1]]),
        repair_map=Matrix([[1]]),
        witness=None,
        separating_left_kernel_vector=None,
        separating_pairing=None,
    )
    assert cert_false.verify() is False

    # 2. covering_edge: non-contractive edge, section domain/shape mismatch, is_descended
    with pytest.raises(ValueError, match="not l1-contractive"):
        covering_edge.CoveringEdgeDiagram(
            fiber_dimensions={"v0": 1, "v1": 1},
            edges=(
                covering_edge.CoveringEdge(
                    edge_id="e_bad",
                    lower="v0",
                    upper="v1",
                    restriction=Matrix([[2]]),
                ),
            ),
        )

    carrier = covering_edge.CoveringEdgeDiagram(
        fiber_dimensions={"v0": 1, "v1": 1},
        edges=(
            covering_edge.CoveringEdge(
                edge_id="e1",
                lower="v0",
                upper="v1",
                restriction=Matrix([[1]]),
            ),
        ),
    )
    with pytest.raises(ValueError, match="section domain mismatch"):
        carrier.normalize_section({"v0": [1]})
    with pytest.raises(ValueError, match="section value at 'v0' has shape"):
        carrier.normalize_section({"v0": Matrix([[1, 2]]), "v1": [1]})

    assert carrier.is_descended({"v0": [1], "v1": [1]}) is True
    assert carrier.is_descended({"v0": [1], "v1": [2]}) is False

    # 3. family_bound: t <= 0, no active edges, edge site density failed, verify False branches
    premises = family_bound.UniformFamilyPremises(
        g_star=Rational(1),
        nu_star=Rational(1),
        eta_star=Rational(1, 2),
        a_star=Rational(1, 2),
    )
    member_valid = family_bound.FiniteFamilyMember(
        system_id="sys1",
        site_count=4,
        edge_count=4,
        local_interaction_norm=Rational(1),
        active_edge_rates=(Rational(1), Rational(1)),
    )
    cert_t0 = family_bound.certify_uniform_family((member_valid,), premises, time=Rational(0))
    assert cert_t0.accepted is False

    member_no_edges = family_bound.FiniteFamilyMember(
        system_id="sys2",
        site_count=4,
        edge_count=4,
        local_interaction_norm=Rational(1),
        active_edge_rates=(),
    )
    cert_no_edges = family_bound.certify_uniform_family((member_no_edges,), premises, time=Rational(1, 100))
    assert cert_no_edges.accepted is False

    member_low_site_dens = family_bound.FiniteFamilyMember(
        system_id="sys3",
        site_count=10,
        edge_count=2,
        local_interaction_norm=Rational(1),
        active_edge_rates=(Rational(1), Rational(1)),
    )
    cert_low_dens = family_bound.certify_uniform_family((member_low_site_dens,), premises, time=Rational(1, 100))
    assert cert_low_dens.accepted is False

    # UniformFamilyBoundCertificate verify branches
    cert_inconsistent = family_bound.UniformFamilyBoundCertificate(
        accepted=True,
        time=Rational(1, 100),
        uniform_window_upper=Rational(1),
        local_edge_polynomial=Rational(1),
        edge_density_floor=Rational(1),
        site_density_floor=Rational(1),
        half_slope_site_floor=Rational(1),
        member_bounds=(),
        refusals=(family_bound.PremiseRefusal("fake", "fake"),),
    )
    assert cert_inconsistent.verify() is False

    # 4. evidence: duplicate claim IDs, inconsistent flags, run.passes
    from evidence import ClaimEvidence, MechanizationRun
    ev1 = ClaimEvidence(
        claim_ids=("V1",), title="T1", evidence_kind="exact_finite", verdict="pass", statement_scope="s", algorithm="a", witness={}
    )
    ev2 = ClaimEvidence(
        claim_ids=("V1",), title="T2", evidence_kind="exact_finite", verdict="pass", statement_scope="s", algorithm="a", witness={}
    )
    with pytest.raises(ValueError, match="duplicate claims"):
        MechanizationRun(
            paper_version="6.9.15", python_package_version="6.9.5", results=(ev1, ev2),
            unresolved_claim_ids=(), execution_completed=True, executable_checks_passed=True,
            open_obligations_present=False, refusals_present=False, claim_disposition_complete=False,
            promotion_eligible=False
        )

    # Inconsistent executable_checks_passed
    with pytest.raises(ValueError, match="executable_checks_passed is inconsistent"):
        MechanizationRun(
            paper_version="6.9.15", python_package_version="6.9.5", results=(ev1,),
            unresolved_claim_ids=(), execution_completed=True, executable_checks_passed=False,
            open_obligations_present=False, refusals_present=False, claim_disposition_complete=False,
            promotion_eligible=False
        )

    # Inconsistent refusals_present
    with pytest.raises(ValueError, match="refusals_present is inconsistent"):
        MechanizationRun(
            paper_version="6.9.15", python_package_version="6.9.5", results=(ev1,),
            unresolved_claim_ids=(), execution_completed=True, executable_checks_passed=True,
            open_obligations_present=False, refusals_present=True, claim_disposition_complete=False,
            promotion_eligible=False
        )

    # Inconsistent open_obligations_present
    with pytest.raises(ValueError, match="open_obligations_present is inconsistent"):
        MechanizationRun(
            paper_version="6.9.15", python_package_version="6.9.5", results=(ev1,),
            unresolved_claim_ids=(), execution_completed=True, executable_checks_passed=True,
            open_obligations_present=True, refusals_present=False, claim_disposition_complete=False,
            promotion_eligible=False
        )

    run = MechanizationRun(
        paper_version="6.9.15", python_package_version="6.9.5", results=(ev1,),
        unresolved_claim_ids=(), execution_completed=True, executable_checks_passed=True,
        open_obligations_present=False, refusals_present=False, claim_disposition_complete=False,
        promotion_eligible=False
    )
    assert run.passes is True

