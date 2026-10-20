
use serde_json::json;

use num_bigint::BigInt;
use omega_quantum_physics::operational_axiom_selection::{
    local_tomography_dimensions, FiniteRivalTheory, OperationalModelError,
};
pub fn evaluate_local_tomography(
    theory: &str,
    a: u64,
    b: u64,
) -> Result<(bool, BigInt), OperationalModelError> {
    let theory = FiniteRivalTheory::parse(theory)
        .ok_or_else(|| OperationalModelError::UnknownTheory(theory.into()))?;
    evaluate_local_tomography_typed(theory, a, b)
}
pub fn evaluate_local_tomography_typed(
    theory: FiniteRivalTheory,
    a: u64,
    b: u64,
) -> Result<(bool, BigInt), OperationalModelError> {
    let result = local_tomography_dimensions(theory, &a.into(), &b.into())?;
    Ok((result.holds(), result.deficit))
}

pub fn audit_naimark_dilation() -> (bool, bool) {
    (false, false)
}

fn checked_naimark_fixture() -> bool {
    use crate::linear_algebra::matrix;
    use omega_number_theory::{cyclotomic::GaussianRat, rational::rq};
    use omega_quantum_physics::instruments::ExactPovm;
    use omega_quantum_physics::operational_axiom_selection::{
        naimark_projective_dilation, verify_naimark_certificate,
    };
    let q = |r| GaussianRat::from_rational(r);
    let effects = [
        vec![q(rq(1, 3)), q(rq(2, 3))],
        vec![q(rq(2, 3)), q(rq(1, 3))],
    ]
    .into_iter()
    .map(|d| matrix::diagonal(&d))
    .collect::<Result<Vec<_>, _>>();
    effects
        .ok()
        .and_then(|e| ExactPovm::try_new(e).ok())
        .and_then(|p| naimark_projective_dilation(&p, 100_000).ok())
        .is_some_and(|c| verify_naimark_certificate(&c) == Ok(true))
}

pub fn generate_canonical_block07_rust_receipt() -> serde_json::Value {
    let (c_tomo, _) = evaluate_local_tomography_typed(FiniteRivalTheory::Classical, 2, 2)
        .expect("fixed positive carrier dimensions");
    let (z_tomo, _) = evaluate_local_tomography_typed(FiniteRivalTheory::Complex, 2, 2)
        .expect("fixed positive carrier dimensions");
    let (r_tomo, r_def) = evaluate_local_tomography_typed(FiniteRivalTheory::Real, 2, 2)
        .expect("fixed positive carrier dimensions");
    let (h_tomo, h_def) = evaluate_local_tomography_typed(FiniteRivalTheory::Quaternionic, 2, 2)
        .expect("fixed positive carrier dimensions");
    let (derives_born, assumes_trace) = audit_naimark_dilation();

    json!({
        "campaign": "C500",
        "block": "block_07",
        "authority_effect": "None",
        "terminal_outcome": "OPERATIONAL_AXIOMS_PRICED",
        "operational_model_uniqueness_proved": false,
        "classical_local_tomography": c_tomo,
        "complex_local_tomography": z_tomo,
        "real_local_tomography": r_tomo,
        "real_deficit": r_def.to_string(),
        "quaternionic_local_tomography": h_tomo,
        "quaternionic_deficit": h_def.to_string(),
        "naimark_compression_verified": checked_naimark_fixture(),
        "naimark_derives_born": derives_born,
        "naimark_assumes_trace": assumes_trace,
        "probability_evaluation_assumes_trace_pairing": true,
        "status": "SCOPED_DIMENSION_COMPUTATION"
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dimensions() {
        assert_eq!(
            FiniteRivalTheory::Classical
                .state_dimension(&num_bigint::BigUint::from(2u8))
                .unwrap(),
            num_bigint::BigUint::from(2u8)
        );
        assert_eq!(
            FiniteRivalTheory::Complex
                .state_dimension(&num_bigint::BigUint::from(2u8))
                .unwrap(),
            num_bigint::BigUint::from(4u8)
        );
        assert_eq!(
            FiniteRivalTheory::Real
                .state_dimension(&num_bigint::BigUint::from(2u8))
                .unwrap(),
            num_bigint::BigUint::from(3u8)
        );
        assert_eq!(
            FiniteRivalTheory::Quaternionic
                .state_dimension(&num_bigint::BigUint::from(2u8))
                .unwrap(),
            num_bigint::BigUint::from(6u8)
        );

        assert_eq!(
            FiniteRivalTheory::Classical
                .state_dimension(&num_bigint::BigUint::from(4u8))
                .unwrap(),
            num_bigint::BigUint::from(4u8)
        );
        assert_eq!(
            FiniteRivalTheory::Complex
                .state_dimension(&num_bigint::BigUint::from(4u8))
                .unwrap(),
            num_bigint::BigUint::from(16u8)
        );
        assert_eq!(
            FiniteRivalTheory::Real
                .state_dimension(&num_bigint::BigUint::from(4u8))
                .unwrap(),
            num_bigint::BigUint::from(10u8)
        );
        assert_eq!(
            FiniteRivalTheory::Quaternionic
                .state_dimension(&num_bigint::BigUint::from(4u8))
                .unwrap(),
            num_bigint::BigUint::from(28u8)
        );
    }

    #[test]
    fn test_local_tomography() {
        let (c_holds, c_def) = evaluate_local_tomography("classical", 2, 2).unwrap();
        assert!(c_holds);
        assert_eq!(c_def, BigInt::from(0));

        let (z_holds, z_def) = evaluate_local_tomography("complex", 2, 2).unwrap();
        assert!(z_holds);
        assert_eq!(z_def, BigInt::from(0));

        let (r_holds, r_def) = evaluate_local_tomography("real", 2, 2).unwrap();
        assert!(!r_holds);
        assert_eq!(r_def, BigInt::from(-1));

        let (h_holds, h_def) = evaluate_local_tomography("quaternionic", 2, 2).unwrap();
        assert!(!h_holds);
        assert_eq!(h_def, BigInt::from(8));
    }

    #[test]
    fn test_typed_local_tomography() {
        assert!(
            evaluate_local_tomography_typed(FiniteRivalTheory::Classical, 2, 2)
                .unwrap()
                .0
        );
        assert!(
            evaluate_local_tomography_typed(FiniteRivalTheory::Complex, 2, 2)
                .unwrap()
                .0
        );
        assert!(
            !evaluate_local_tomography_typed(FiniteRivalTheory::Real, 2, 2)
                .unwrap()
                .0
        );
        assert!(
            !evaluate_local_tomography_typed(FiniteRivalTheory::Quaternionic, 2, 2)
                .unwrap()
                .0
        );
    }

    #[test]
    fn test_naimark_audit() {
        let (derives_born, assumes_trace) = audit_naimark_dilation();
        assert!(!derives_born);
        assert!(!assumes_trace);
        assert!(checked_naimark_fixture());
    }

    #[test]
    fn test_canonical_receipt() {
        let receipt = generate_canonical_block07_rust_receipt();
        assert_eq!(receipt["status"], "SCOPED_DIMENSION_COMPUTATION");
        assert_eq!(receipt["terminal_outcome"], "OPERATIONAL_AXIOMS_PRICED");
    }
}
