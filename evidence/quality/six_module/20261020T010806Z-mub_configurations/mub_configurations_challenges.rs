
#[cfg(test)]
mod boundary_review {
    use super::*;
    #[test]
    fn invalid_singleton_is_refused() {
        assert!(MubOperatorConfiguration::new(2, vec![vec![PhasePoint::new(usize::MAX, 1)]]).is_err());
    }
    #[test]
    fn oversized_dimension_is_refused_without_panic() {
        assert!(MubOperatorConfiguration::new(usize::MAX, vec![]).is_err());
    }
    #[test]
    fn unrepresentable_upper_bound_has_typed_result() {
        assert!(std::panic::catch_unwind(|| mub_theoretical_upper_bound(usize::MAX)).is_ok(), "public bound helper panicked");
    }
}
