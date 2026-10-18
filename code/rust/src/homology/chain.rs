//! Exact chain coordinates. AuthorityEffect: None.
//! The common implementation seals the vector kind and binds degree and basis.

pub type Chain = super::graded_vector::GradedVector<super::graded_vector::ChainKind>;

#[cfg(test)]
mod tests {
    use super::*;
    use crate::homology::errors::HomologicalError;
    use crate::homology::ids::{BasisId, Degree};
    use crate::linear_algebra::scalars::Q;

    fn r(n: i64, d: i64) -> Q {
        crate::linear_algebra::scalars::qr(n, d)
    }

    fn test_basis_id() -> BasisId {
        BasisId::new("test_basis").expect("valid basis")
    }

    #[test]
    fn test_chain_new() {
        let coeffs = vec![r(1, 1), r(2, 1), r(3, 1)];
        let chain = Chain::new(Degree(0), test_basis_id(), coeffs.clone()).expect("valid fixture");
        assert_eq!(chain.degree, Degree(0));
        assert_eq!(chain.coefficients, coeffs);
        assert_eq!(chain.dimension(), 3);
    }

    #[test]
    fn test_chain_zero() {
        let chain = Chain::zero(Degree(1), test_basis_id(), 5).expect("valid fixture");
        assert_eq!(chain.dimension(), 5);
        assert!(chain.is_zero());
    }

    #[test]
    fn test_chain_is_zero() {
        let zero_chain = Chain::zero(Degree(0), test_basis_id(), 3).expect("valid fixture");
        assert!(zero_chain.is_zero());

        let non_zero = Chain::new(Degree(0), test_basis_id(), vec![r(0, 1), r(1, 1), r(0, 1)])
            .expect("valid fixture");
        assert!(!non_zero.is_zero());
    }

    #[test]
    fn test_chain_add() {
        let a =
            Chain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1)]).expect("valid fixture");
        let b =
            Chain::new(Degree(0), test_basis_id(), vec![r(3, 1), r(4, 1)]).expect("valid fixture");
        let sum = a.add(&b).unwrap();
        assert_eq!(sum.coefficients, vec![r(4, 1), r(6, 1)]);
    }

    #[test]
    fn test_chain_add_degree_mismatch() {
        let a = Chain::new(Degree(0), test_basis_id(), vec![r(1, 1)]).expect("valid fixture");
        let b = Chain::new(Degree(1), test_basis_id(), vec![r(1, 1)]).expect("valid fixture");
        let result = a.add(&b);
        assert!(matches!(
            result,
            Err(HomologicalError::DegreeMismatch { .. })
        ));
    }

    #[test]
    fn test_chain_add_dimension_mismatch() {
        let a =
            Chain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1)]).expect("valid fixture");
        let b = Chain::new(Degree(0), test_basis_id(), vec![r(1, 1)]).expect("valid fixture");
        let result = a.add(&b);
        assert!(matches!(
            result,
            Err(HomologicalError::DimensionMismatch { .. })
        ));
    }

    #[test]
    fn test_chain_sub() {
        let a =
            Chain::new(Degree(0), test_basis_id(), vec![r(5, 1), r(7, 1)]).expect("valid fixture");
        let b =
            Chain::new(Degree(0), test_basis_id(), vec![r(2, 1), r(3, 1)]).expect("valid fixture");
        let diff = a.sub(&b).unwrap();
        assert_eq!(diff.coefficients, vec![r(3, 1), r(4, 1)]);
    }

    #[test]
    fn test_chain_sub_self_is_zero() {
        let a = Chain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1), r(3, 1)])
            .expect("valid fixture");
        let diff = a.sub(&a).unwrap();
        assert!(diff.is_zero());
    }

    #[test]
    fn test_chain_scalar_mul() {
        let a = Chain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1), r(3, 1)])
            .expect("valid fixture");
        let scaled = a.scalar_mul(&r(2, 1)).expect("valid fixture");
        assert_eq!(scaled.coefficients, vec![r(2, 1), r(4, 1), r(6, 1)]);
    }

    #[test]
    fn test_chain_scalar_mul_by_zero() {
        let a = Chain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1), r(3, 1)])
            .expect("valid fixture");
        let scaled = a.scalar_mul(&r(0, 1)).expect("valid fixture");
        assert!(scaled.is_zero());
    }

    #[test]
    fn test_chain_scalar_mul_by_fraction() {
        let a =
            Chain::new(Degree(0), test_basis_id(), vec![r(2, 1), r(4, 1)]).expect("valid fixture");
        let scaled = a.scalar_mul(&r(1, 2)).expect("valid fixture");
        assert_eq!(scaled.coefficients, vec![r(1, 1), r(2, 1)]);
    }

    #[test]
    fn test_chain_hash_deterministic() {
        let a = Chain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1), r(3, 1)])
            .expect("valid fixture");
        let hash1 = a.hash();
        let hash2 = a.hash();
        assert_eq!(hash1, hash2);
    }

    #[test]
    fn test_chain_hash_different_for_different_chains() {
        let a =
            Chain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1)]).expect("valid fixture");
        let b =
            Chain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(3, 1)]).expect("valid fixture");
        assert_ne!(a.hash(), b.hash());
    }
}
