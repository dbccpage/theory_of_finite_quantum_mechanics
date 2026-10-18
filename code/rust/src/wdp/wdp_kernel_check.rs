//! Finite path-kernel product for a declared walk.
//!
//! AuthorityEffect: None. This module does not decide LGGR V soundness.

use omega_epk::matrix_path_kernel::{EvaluatedPathKernelGraph, MatrixPathError, RationalMatrix2x2};

/// Finite path-kernel product of a walk.
///
/// This is not `lggr_v::check_soundness`. AuthorityEffect: None.
/// Returns the path product `T_last · … · T_first`, not a soundness report.
/// An empty factor list is the empty walk, whose product is the identity.
pub fn wdp_kernel_check(
    factors: &[RationalMatrix2x2],
) -> Result<RationalMatrix2x2, MatrixPathError> {
    if factors.is_empty() {
        return Ok(RationalMatrix2x2::identity());
    }
    let vertices: Vec<String> = (0..=factors.len())
        .map(|index| format!("v{index}"))
        .collect();
    let edges: Vec<(String, String)> = (0..factors.len())
        .map(|index| (format!("v{index}"), format!("v{}", index + 1)))
        .collect();
    let graph = EvaluatedPathKernelGraph::new(vertices, edges, factors.to_vec())?;
    let edge_indices: Vec<usize> = (0..factors.len()).collect();
    graph.evaluate_path(&edge_indices)
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_epk::lggr_v::LggrSoundnessReport;

    fn assert_not_lggr_soundness_report<T: 'static>(value: &T) {
        assert_ne!(
            std::any::TypeId::of::<T>(),
            std::any::TypeId::of::<LggrSoundnessReport>(),
        );
        let _ = value;
    }

    #[test]
    fn identity_multiplied_by_identity_is_identity() {
        let identity = RationalMatrix2x2::identity();
        let result = wdp_kernel_check(&[identity.clone(), identity.clone()]);
        assert_not_lggr_soundness_report(&result);
        let product = result.expect("path product");
        assert_eq!(product, identity);
        assert_not_lggr_soundness_report(&product);
    }
}
