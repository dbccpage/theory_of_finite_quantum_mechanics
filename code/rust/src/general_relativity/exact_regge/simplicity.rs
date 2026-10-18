
#![forbid(unsafe_code)]

use super::manifold::{ManifoldError, SimplicialManifold4D};
use linear_algebra::regge_exact::Bivector4;
use num_rational::BigRational;

pub fn hinge_bivector_in_pentatope(
    manifold: &SimplicialManifold4D,
    pentatope_index: usize,
    triangle: [u32; 3],
) -> Result<Bivector4, ManifoldError> {
    let chart = manifold.pentatope(pentatope_index)?;
    let ri = vertex_coords(manifold, pentatope_index, &chart.vertices, triangle[0])?;
    let rj = vertex_coords(manifold, pentatope_index, &chart.vertices, triangle[1])?;
    let rk = vertex_coords(manifold, pentatope_index, &chart.vertices, triangle[2])?;
    let along_j = std::array::from_fn(|axis| rj[axis].clone() - ri[axis].clone());
    let along_k = std::array::from_fn(|axis| rk[axis].clone() - ri[axis].clone());
    Ok(Bivector4::from_wedge_half(&along_j, &along_k))
}

pub fn simplicity_holds_in_pentatope(
    manifold: &SimplicialManifold4D,
    pentatope_index: usize,
    triangle: [u32; 3],
) -> Result<bool, ManifoldError> {
    Ok(hinge_bivector_in_pentatope(manifold, pentatope_index, triangle)?.is_simple())
}

pub fn all_hinges_simple(manifold: &SimplicialManifold4D) -> Result<bool, ManifoldError> {
    let pentatope_count = manifold.pentatope_count();
    if pentatope_count == 0 {
        return Err(ManifoldError::Empty);
    }
    for index in 0..pentatope_count {
        let vertices = manifold.pentatope(index)?.vertices;
        for i in 0..5 {
            for j in (i + 1)..5 {
                for k in (j + 1)..5 {
                    let triangle = [vertices[i], vertices[j], vertices[k]];
                    if !simplicity_holds_in_pentatope(manifold, index, triangle)? {
                        return Ok(false);
                    }
                }
            }
        }
    }
    Ok(true)
}

fn vertex_coords(
    manifold: &SimplicialManifold4D,
    pentatope_index: usize,
    chart_vertices: &[u32; 5],
    vertex: u32,
) -> Result<[BigRational; 4], ManifoldError> {
    if !chart_vertices.contains(&vertex) {
        return Err(ManifoldError::NotAFace);
    }
    manifold.chart_coords(pentatope_index, vertex)
}
