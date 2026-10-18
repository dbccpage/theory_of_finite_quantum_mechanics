// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

//! Integration test of the core suite of the native package: every check of
//! `run_finite_qm_verification_suite` holds on the declared finite instances
//! (maximal MUBs and exact tomography in d = 3 and 4, the discrete Wigner
//! function in d = 5 with its magic-state negativity, and the commutator trace
//! obstruction). The algebra behind each check is tested in
//! `omega_quantum_physics`.

use omega_number_theory::rational::rq;

use finite_qm_native::run_finite_qm_verification_suite;

#[test]
fn test_integration_full_suite_report() {
    let report = run_finite_qm_verification_suite();
    assert!(report.d3_mub_exhaustive);
    assert!(report.d3_tomography_ground_state_verified);
    assert!(report.d3_tomography_magic_state_verified);
    assert!(report.d3_tomography_mixed_state_verified);
    assert!(report.d4_mub_exhaustive);
    assert!(report.d4_tomography_bell_state_verified);
    assert!(report.clifton_kent_all_1024_non_psd_certified);
    assert!(report.d5_wigner_algebra_verified);
    assert!(report.d5_magic_state_negativity_witnessed);
    assert_eq!(report.d5_magic_point_value, rq(-1, 5));
    assert!(report.commutator_trace_obstruction_verified);
}
