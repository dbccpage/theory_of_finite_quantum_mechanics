
#![forbid(unsafe_code)]

use super::manifold::{ManifoldError, SimplicialManifold4D};
use super::orientation::{tetra_boundary_of_pentatope, triangle_boundary_of_tetra};
use super::simplicity::hinge_bivector_in_pentatope;
use linear_algebra::regge_exact::{q_i64, Bivector4};

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
