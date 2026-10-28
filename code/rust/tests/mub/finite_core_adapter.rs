//! Exact verifier behavior for the finite MUB core used by omega_mub.
//! AuthorityEffect: None.

#[test]
fn finite_core_adapter_preserves_types_and_refusals() {
    use engine_quantum_physics::mub::dimension_stratification::{
        stratify_dimension, DimensionAuthorityStatus,
    };
    use engine_quantum_physics::mub::algebra::{
        verify_mub_projector_algebra, ProjectorAlgebraStatus,
    };
    use engine_quantum_physics::mub::odd_prime::build_odd_prime_mub_d3;

    let mut bases = build_odd_prime_mub_d3();
    let verified = verify_mub_projector_algebra(&bases, 3);
    assert_eq!(verified.status, ProjectorAlgebraStatus::AlgebraVerified);
    assert_eq!((verified.basis_count, verified.projector_count), (4, 12));

    // Repeating a valid basis preserves its internal algebra but violates MUB
    // cross-basis unbiasedness, so the verifier must refuse it.
    bases[1] = bases[0].clone();
    let refused = verify_mub_projector_algebra(&bases, 3);
    assert_eq!(
        refused.status,
        ProjectorAlgebraStatus::InvalidCrossBasisUnbiasedness
    );

    let dimension = stratify_dimension(6);
    assert_eq!(
        dimension.status,
        DimensionAuthorityStatus::ExactTensorLowerControl
    );
    assert_eq!(dimension.guaranteed_basis_count, Some(3));
    assert_eq!(dimension.complete_basis_count, Some(7));
    assert!(!dimension.missing_obligations.is_empty());
}
