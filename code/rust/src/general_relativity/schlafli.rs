
use crate::dihedral_angles::triangle_angle_at;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SchlafliCheckResult {
    pub simplex_vertices: Vec<usize>,
    pub residual_sum: f64,
    pub is_vanishing: bool,
}

pub fn verify_schlafli_identity_2d(
    triangle: &[usize; 3],
    get_length: impl Fn(usize, usize) -> Option<f64>,
) -> Result<SchlafliCheckResult, String> {
    let a0 = triangle_angle_at(triangle, triangle[0], &get_length)?;
    let a1 = triangle_angle_at(triangle, triangle[1], &get_length)?;
    let a2 = triangle_angle_at(triangle, triangle[2], &get_length)?;

    let sum = a0 + a1 + a2;
    let err = (sum - std::f64::consts::PI).abs();

    Ok(SchlafliCheckResult {
        simplex_vertices: triangle.to_vec(),
        residual_sum: err,
        is_vanishing: err < 1e-7,
    })
}

pub fn compute_regge_action_gradient_at_edge(
    _edge: (usize, usize),
    current_length: f64,
    delta: f64,
    mut action_evaluator: impl FnMut(f64) -> f64,
) -> f64 {
    let s_fwd = action_evaluator(current_length + delta);
    let s_bwd = action_evaluator(current_length - delta);
    (s_fwd - s_bwd) / (2.0 * delta)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_schlafli_identity_triangle() {
        let tri = [0, 1, 2];
        let side = 3.5;
        let get_len = |_: usize, _: usize| Some(side);

        let res = verify_schlafli_identity_2d(&tri, get_len).unwrap();
        assert!(res.is_vanishing);
        assert!(res.residual_sum < 1e-9);
    }
}
