
#[cfg(test)]
mod boundary_review {
    use super::*;
    #[test]
    fn shape_mismatch_is_refused() {
        assert!(ray_orthogonality(&[vec![1, 1], vec![1]]).is_err(), "trailing coordinate was silently discarded");
    }
}
