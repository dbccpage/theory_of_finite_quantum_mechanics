
use crate::cayley_menger::{simplex_volume_cayley_menger, simplex_volume_derivative_wrt_squared_edge};
use crate::regge_4d::ReggeTriangulation4D;
use crate::regge_calculus::{EdgeLengthMetric, ReggeError, DEFAULT_TOL};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; discrete Regge field equations.";

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ReggeFieldEquationResult {
    pub residuals: BTreeMap<(usize, usize), f64>,
    pub einstein_tensor: BTreeMap<(usize, usize), f64>,
    pub cosmological_terms: BTreeMap<(usize, usize), f64>,
    pub max_residual: f64,
    pub l2_residual: f64,
    pub total_edges: usize,
}

pub fn compute_regge_field_equations_4d(
    triangulation: &ReggeTriangulation4D,
    lambda: f64,
    bulk_only: bool,
) -> Result<ReggeFieldEquationResult, ReggeError> {
    let mut residuals = BTreeMap::new();
    let mut einstein_tensor = BTreeMap::new();
    let mut cosmological_terms = BTreeMap::new();

    let mut hinge_map = BTreeMap::new();
    for h in &triangulation.hinges {
        let mut sorted_tri = h.triangle;
        sorted_tri.sort();
        hinge_map.insert(sorted_tri, (h.deficit_angle, h.area));
    }

    let get_len = |u: usize, v: usize| triangulation.metric.get(u, v).ok();

    let mut all_edges = BTreeSet::new();
    for p in &triangulation.pentachora {
        for i in 0..5 {
            for j in (i + 1)..5 {
                let u = p[i].min(p[j]);
                let v = p[i].max(p[j]);
                all_edges.insert((u, v));
            }
        }
    }

    let mut max_res: f64 = 0.0;
    let mut sum_sq: f64 = 0.0;

    for &(u, v) in &all_edges {
        let mut curvature_grad = 0.0;
        let mut dual_volume = 0.0;

        for h in &triangulation.hinges {
            if bulk_only && !h.is_interior {
                continue;
            }

            let tri = h.triangle;
            let contains_u = tri.contains(&u);
            let contains_v = tri.contains(&v);

            if contains_u && contains_v {
                let eps = h.deficit_angle;
                let d_area = simplex_volume_derivative_wrt_squared_edge(&tri, u, v, get_len)
                    .map_err(ReggeError::Computation)?;
                curvature_grad += eps * d_area;
            }
        }

        let mut vol_grad = 0.0;
        for p in &triangulation.pentachora {
            if p.contains(&u) && p.contains(&v) {
                let d_vol = simplex_volume_derivative_wrt_squared_edge(p, u, v, get_len)
                    .map_err(ReggeError::Computation)?;
                vol_grad += d_vol;

                let vol4 = simplex_volume_cayley_menger(p, get_len)
                    .map_err(ReggeError::Computation)?;
                dual_volume += 0.1 * vol4;
            }
        }

        let cosmo_grad = lambda * vol_grad;
        let e_res = curvature_grad - cosmo_grad;

        let g_e = if dual_volume > DEFAULT_TOL {
            curvature_grad / dual_volume
        } else {
            0.0
        };

        let abs_res = e_res.abs();
        if abs_res > max_res {
            max_res = abs_res;
        }
        sum_sq += e_res * e_res;

        residuals.insert((u, v), e_res);
        einstein_tensor.insert((u, v), g_e);
        cosmological_terms.insert((u, v), cosmo_grad);
    }

    Ok(ReggeFieldEquationResult {
        residuals,
        einstein_tensor,
        cosmological_terms,
        max_residual: max_res,
        l2_residual: sum_sq.sqrt(),
        total_edges: all_edges.len(),
    })
}

#[derive(Debug, Clone, PartialEq)]
pub struct ReggeRelaxationResult {
    pub converged: bool,
    pub iterations: usize,
    pub initial_l2_residual: f64,
    pub final_l2_residual: f64,
    pub final_max_residual: f64,
    pub metric: EdgeLengthMetric,
}

pub fn solve_regge_field_equations_relaxation(
    triangulation: &ReggeTriangulation4D,
    lambda: f64,
    bulk_only: bool,
    learning_rate: f64,
    max_iters: usize,
    tolerance: f64,
) -> Result<ReggeRelaxationResult, ReggeError> {
    let mut current_metric = triangulation.metric.clone();
    let initial_eval = compute_regge_field_equations_4d(triangulation, lambda, bulk_only)?;
    let initial_l2 = initial_eval.l2_residual;

    let mut current_triangulation = triangulation.clone();
    let mut final_l2 = initial_l2;
    let mut final_max = initial_eval.max_residual;
    let mut converged = false;
    let mut iters_completed = 0;

    for iter in 0..max_iters {
        iters_completed = iter + 1;
        let eval = compute_regge_field_equations_4d(&current_triangulation, lambda, bulk_only)?;
        final_l2 = eval.l2_residual;
        final_max = eval.max_residual;

        if final_max < tolerance {
            converged = true;
            break;
        }

        let mut next_metric = current_metric.clone();
        for (&(u, v), &res) in &eval.residuals {
            let current_len = current_metric.get(u, v)?;
            let current_sq = current_len * current_len;
            let step = learning_rate * res;
            let next_sq = current_sq - step;

            if next_sq <= DEFAULT_TOL {
                continue;
            }
            let next_len = next_sq.sqrt();
            let _ = next_metric.set(u, v, next_len);
        }

        if let Ok(next_tri) = ReggeTriangulation4D::try_new(
            triangulation.complex.clone(),
            next_metric.clone(),
            format!("iter_{iters_completed}"),
        ) {
            current_metric = next_metric;
            current_triangulation = next_tri;
        } else {
            break;
        }
    }

    Ok(ReggeRelaxationResult {
        converged,
        iterations: iters_completed,
        initial_l2_residual: initial_l2,
        final_l2_residual: final_l2,
        final_max_residual: final_max,
        metric: current_metric,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_flat_fan_regge_field_equations_vanish_for_zero_lambda() {
        let tri = ReggeTriangulation4D::four_pentachora_fan(1.0).unwrap();
        let result = compute_regge_field_equations_4d(&tri, 0.0, true).unwrap();

        let res_01 = result.residuals.get(&(0, 1)).copied().unwrap();
        let res_12 = result.residuals.get(&(1, 2)).copied().unwrap();
        let res_02 = result.residuals.get(&(0, 2)).copied().unwrap();

        assert!(
            res_01.abs() < 1e-6,
            "Residual on (0, 1) should vanish for flat interior, got {res_01}"
        );
        assert!(
            res_12.abs() < 1e-6,
            "Residual on (1, 2) should vanish for flat interior, got {res_12}"
        );
        assert!(
            res_02.abs() < 1e-6,
            "Residual on (0, 2) should vanish for flat interior, got {res_02}"
        );
    }

    #[test]
    fn test_cosmological_term_nonzero_when_lambda_positive() {
        let tri = ReggeTriangulation4D::four_pentachora_fan(1.0).unwrap();
        let lambda = 0.5;
        let result = compute_regge_field_equations_4d(&tri, lambda, true).unwrap();

        let cosmo_01 = result.cosmological_terms.get(&(0, 1)).copied().unwrap();
        assert!(
            cosmo_01.abs() > 1e-4,
            "Cosmological gradient on (0, 1) should be non-zero for positive lambda"
        );
        let res_01 = result.residuals.get(&(0, 1)).copied().unwrap();
        assert!((res_01 - (-cosmo_01)).abs() < 1e-6);
    }
}
