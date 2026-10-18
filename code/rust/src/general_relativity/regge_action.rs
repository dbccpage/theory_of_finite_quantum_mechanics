//! Classical Regge Action with Cosmological Constant (RQ-01).
//!
//! S_Regge = sum_{h in Hinges^(D-2)} V_{D-2}(h) * eps_h - Lambda * sum_{sigma in D-simplices} V_D(sigma).
//!
//! AuthorityEffect: None.

use serde::{Deserialize, Serialize};

/// Detailed breakdown of the Regge action evaluation.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ReggeActionResult {
    pub curvature_term: f64,
    pub cosmological_term: f64,
    pub total_action: f64,
    pub lambda_param: f64,
    pub dimension: usize,
}

/// Compute Regge action from hinge deficits, hinge volumes, simplex volumes, and cosmological constant Lambda.
pub fn compute_regge_action(
    hinges: &[(f64, f64)], // (volume_of_hinge, deficit_angle)
    simplex_volumes: &[f64],
    lambda_param: f64,
    dimension: usize,
) -> ReggeActionResult {
    let mut curvature_term = 0.0;
    for &(vol_h, eps_h) in hinges {
        curvature_term += vol_h * eps_h;
    }

    let total_volume: f64 = simplex_volumes.iter().copied().sum();
    let cosmological_term = lambda_param * total_volume;
    let total_action = curvature_term - cosmological_term;

    ReggeActionResult {
        curvature_term,
        cosmological_term,
        total_action,
        lambda_param,
        dimension,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_regge_action_with_lambda() {
        // 3D Regge action on two edges with lengths 1.0, deficits pi/2, volume 0.5
        let hinges = vec![
            (1.0, std::f64::consts::FRAC_PI_2),
            (1.0, std::f64::consts::FRAC_PI_2),
        ];
        let vols = vec![0.5];
        let res = compute_regge_action(&hinges, &vols, 0.1, 3);

        let expected_curv = std::f64::consts::PI;
        assert!((res.curvature_term - expected_curv).abs() < 1e-9);
        assert!((res.cosmological_term - 0.05).abs() < 1e-9);
        assert!((res.total_action - (expected_curv - 0.05)).abs() < 1e-9);
    }
}
