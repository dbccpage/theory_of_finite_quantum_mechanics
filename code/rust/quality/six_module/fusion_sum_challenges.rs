#[cfg(test)]
mod sum_review {
    use super::*;
    #[test]
    fn exact_sum_survives_large_intermediate_cancellation() {
        let values=[Ratio::from_integer(i64::MAX),Ratio::from_integer(i64::MAX),Ratio::from_integer(-i64::MAX)];
        assert!(verify_fusion_global_dimension(&values,Ratio::from_integer(i64::MAX)));
    }
    #[test]
    fn malformed_zero_denominators_refuse() {
        assert!(!verify_fusion_global_dimension(&[Ratio::new_raw(1,0)],Ratio::from_integer(1)));
        assert!(!verify_fusion_global_dimension(&[Ratio::from_integer(1)],Ratio::new_raw(1,0)));
    }
}
