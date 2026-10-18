//! Cross-module refusal of a float, a planted flag, and a tampered artifact.
//!
//! The floating-diagnostic arm is checked on the shipped request function and,
//! separately, on the source of that function. The seal recomputes
//! `EnclosedTriple::certify` and does not take the hostile inputs as a pass bit.
//!
//! AuthorityEffect: None
//! Firewall Line: NOT MUB(6)=3, NOT MUB(6)<=3; stated region only; mints no authority

use omega_kernel::interval::Interval;
use omega_mub::omega_native::census::mub6_claim_gate::seal_vbox_certificate;
use omega_mub::omega_native::exact::mub6_cover::EnclosedTriple;
use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_mub::omega_native::exact::mub6_interval_cover::VectorBox;
use omega_mub::runtime_adapter::{
    evaluate_mub6_request, Mub6RuntimeAdapterError, Mub6RuntimeEvidenceV1, Mub6RuntimeRequestV1,
};
use omega_number_theory::rational::ri;

fn wide_box() -> VectorBox {
    std::array::from_fn(|_| Interval::new(ri(0), ri(1)))
}

#[test]
fn floating_diagnostic_is_refused_before_exact_replay() {
    let error = evaluate_mub6_request(Mub6RuntimeRequestV1 {
        evidence: Mub6RuntimeEvidenceV1::FloatingDiagnostic { objective: 1.0e9 },
    })
    .expect_err("a float must not enter exact replay");
    assert!(matches!(
        error,
        Mub6RuntimeAdapterError::FloatingEvidenceRefused
    ));

    let source = include_str!("../../omega_mub/src/runtime_adapter.rs");
    let start = source
        .find("pub fn evaluate_mub6_request")
        .expect("shipped entry point");
    let rest = &source[start..];
    let function_end = rest[1..]
        .find("\npub fn")
        .map(|index| index + 1)
        .unwrap_or(rest.len());
    let function = &rest[..function_end];
    let arm_at = function
        .find("FloatingDiagnostic")
        .expect("floating arm");
    let arm = &function[arm_at..];
    assert!(
        !arm.contains("evaluate_exact_case"),
        "the floating arm must return before exact replay:\n{arm}"
    );
    assert!(arm.contains("FloatingEvidenceRefused"));
}

#[test]
fn a_float_decision_cannot_become_the_multi_module_pass_bit() {
    let exact = EnclosedTriple::standard();
    let vbox = wide_box();
    let artifact = r#"{"global_solution":true,"solved":true,"verified_certificate":true,"note":"MUB(6)=3"}"#;
    let hostile = seal_vbox_certificate(&exact, &vbox, artifact, 1.0e9, true);
    let quiet = seal_vbox_certificate(&exact, &vbox, "{}", -1.0e9, false);
    assert_eq!(hostile, quiet);
    assert_eq!(hostile.firewall, FIREWALL);
    assert_eq!(hostile.authority_effect, AUTHORITY_EFFECT);
    assert!(!hostile.mub6_equals_3);
    assert!(!hostile.mub6_at_most_3);
    assert!(!hostile.global_solution);
    assert_eq!(hostile.verified_certificate, exact.certify(&vbox).is_some());
    assert_eq!(
        hostile.stated_region_certificate,
        hostile.verified_certificate
    );
}
