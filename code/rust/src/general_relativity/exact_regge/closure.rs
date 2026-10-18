//! Contracted closure identity on a tetrahedron.
//!
//! `B(τ) = Σ_{h ⊂ τ} ε(h, τ) D_h Σ_h` with `D_h = Id` in the pentatope chart.
//! `Σ_h = (1/2) (r_j - r_i) ∧ (r_k - r_i)` on the oriented triangle `(i, j, k)`.
//! The deficit `ε_h = 2π - Σ θ` is not computed. `B` is an exact rational
//! bivector, not a floating-point curvature residual.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use super::manifold::{ManifoldError, SimplicialManifold4D};
use super::orientation::{tetra_boundary_of_pentatope, triangle_boundary_of_tetra};
use super::simplicity::hinge_bivector_in_pentatope;
use linear_algebra::regge_exact::{q_i64, Bivector4};

/// Contracted closure identity inside one pentatope chart.
///
/// `tetra` is matched by sorted vertex ids to one face of
/// `tetra_boundary_of_pentatope(chart.vertices)`. The sum uses that matched
/// ordered 4-tuple. The tetra's sign in the pentatope is not applied.
/// Terms follow `triangle_boundary_of_tetra` from left to right. Each term is
/// `ε * Σ_h`: `ε` is that triangle's `i8` sign as a rational, `Σ_h` is the
/// hinge bivector in this same chart, and `D_h` is the identity. The
/// accumulator starts at the zero bivector and folds `checked_add`.
/// `ε_h = 2π - Σ θ` is not computed.
///
/// AuthorityEffect: None.
pub fn contracted_closure_in_pentatope(
    manifold: &SimplicialManifold4D,
    pentatope_index: usize,
    tetra: [u32; 4],
) -> Result<Bivector4, ManifoldError> {
    let chart = manifold.pentatope(pentatope_index)?;
    let wanted = sorted_tetra(tetra);
    let ordered = tetra_boundary_of_pentatope(chart.vertices)
        .into_iter()
        .find(|face| sorted_tetra(face.0) == wanted)
        .map(|face| face.0)
        .ok_or(ManifoldError::NotAFace)?;
    let mut sum = Bivector4::zero();
    for (triangle, sign) in triangle_boundary_of_tetra(ordered) {
        let sigma = hinge_bivector_in_pentatope(manifold, pentatope_index, triangle)?;
        let epsilon = q_i64(i64::from(sign));
        sum = sum.checked_add(&sigma.checked_scale(&epsilon));
    }
    Ok(sum)
}

/// Whether every boundary tetrahedron of every pentatope has vanishing `B`.
///
/// Pentatopes run in index order. Each tetrahedron is the ordered 4-tuple from
/// `tetra_boundary_of_pentatope`, and `B` is [`contracted_closure_in_pentatope`].
/// No pentatopes yields [`ManifoldError::Empty`].
/// `ε_h = 2π - Σ θ` is not computed.
///
/// AuthorityEffect: None.
pub fn all_tetra_closures_vanish(manifold: &SimplicialManifold4D) -> Result<bool, ManifoldError> {
    let pentatope_count = manifold.pentatope_count();
    if pentatope_count == 0 {
        return Err(ManifoldError::Empty);
    }
    for index in 0..pentatope_count {
        let vertices = manifold.pentatope(index)?.vertices;
        for (tetra, _pentatope_sign) in tetra_boundary_of_pentatope(vertices) {
            if !contracted_closure_in_pentatope(manifold, index, tetra)?.is_zero() {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

fn sorted_tetra(mut tetra: [u32; 4]) -> [u32; 4] {
    tetra.sort_unstable();
    tetra
}
