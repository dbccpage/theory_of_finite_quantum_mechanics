
use crate::regge_4d::ReggeTriangulation4D;
use crate::regge_calculus::ReggeError;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; discrete Ricci and higher-derivative Regge.";

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct VertexCurvature4D {
    pub vertex: usize,
    pub dual_volume: f64,
    pub integrated_scalar_curvature: f64,
    pub scalar_curvature_density: f64,
    pub incident_pentachora_count: usize,
    pub incident_hinge_count: usize,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct DiscreteCurvatureField4D {
    pub vertex_curvatures: BTreeMap<usize, VertexCurvature4D>,
    pub total_4volume: f64,
    pub einstein_hilbert_action: f64,
    pub higher_derivative_action: f64,
    pub coupling_a: f64,
}

pub fn compute_discrete_curvature_field_4d(
    triangulation: &ReggeTriangulation4D,
    coupling_a: f64,
) -> Result<DiscreteCurvatureField4D, ReggeError> {
    let mut vertex_set = BTreeSet::new();
    for p in &triangulation.pentachora {
        for &v in p {
            vertex_set.insert(v);
        }
    }

    let mut vertex_dual_vol = BTreeMap::new();
    let mut vertex_incident_pent = BTreeMap::new();
    for &v in &vertex_set {
        vertex_dual_vol.insert(v, 0.0);
        vertex_incident_pent.insert(v, 0);
    }

    for (p_idx, p) in triangulation.pentachora.iter().enumerate() {
        let vol = triangulation.pentachora_volumes[p_idx];
        let share = 0.2 * vol;
        for &v in p {
            if let Some(entry) = vertex_dual_vol.get_mut(&v) {
                *entry += share;
            }
            if let Some(count) = vertex_incident_pent.get_mut(&v) {
                *count += 1;
            }
        }
    }

    let mut vertex_int_curv = BTreeMap::new();
    let mut vertex_incident_hinges = BTreeMap::new();
    for &v in &vertex_set {
        vertex_int_curv.insert(v, 0.0);
        vertex_incident_hinges.insert(v, 0);
    }

    for h in &triangulation.hinges {
        if !h.is_interior {
            continue;
        }
        let hinge_curv = 2.0 * h.area * h.deficit_angle;
        let share = hinge_curv / 3.0;
        for &v in &h.triangle {
            if let Some(c) = vertex_int_curv.get_mut(&v) {
                *c += share;
            }
            if let Some(count) = vertex_incident_hinges.get_mut(&v) {
                *count += 1;
            }
        }
    }

    let mut vertex_curvatures = BTreeMap::new();
    let mut total_vol = 0.0;
    let mut eh_action = 0.0;
    let mut hd_action = 0.0;

    for &v in &vertex_set {
        let dual_vol = vertex_dual_vol.get(&v).copied().unwrap_or(0.0);
        let int_r = vertex_int_curv.get(&v).copied().unwrap_or(0.0);
        total_vol += dual_vol;
        eh_action += 0.5 * int_r;

        let density = if dual_vol > 1e-12 {
            int_r / dual_vol
        } else {
            0.0
        };

        let hd_term = if dual_vol > 1e-12 {
            coupling_a * dual_vol * density * density
        } else {
            0.0
        };
        hd_action += hd_term;

        vertex_curvatures.insert(
            v,
            VertexCurvature4D {
                vertex: v,
                dual_volume: dual_vol,
                integrated_scalar_curvature: int_r,
                scalar_curvature_density: density,
                incident_pentachora_count: vertex_incident_pent.get(&v).copied().unwrap_or(0),
                incident_hinge_count: vertex_incident_hinges.get(&v).copied().unwrap_or(0),
            },
        );
    }

    Ok(DiscreteCurvatureField4D {
        vertex_curvatures,
        total_4volume: total_vol,
        einstein_hilbert_action: eh_action,
        higher_derivative_action: hd_action,
        coupling_a,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_flat_fan_has_zero_ricci_curvature_at_interior_vertices() {
        let tri = ReggeTriangulation4D::four_pentachora_fan(1.0).unwrap();
        let field = compute_discrete_curvature_field_4d(&tri, 1.0).unwrap();

        let sum_pent_vol: f64 = tri.pentachora_volumes.iter().sum();
        assert!((field.total_4volume - sum_pent_vol).abs() < 1e-7);

        assert!(field.einstein_hilbert_action.abs() < 1e-6);

        assert!(field.higher_derivative_action >= 0.0);
        assert!(field.higher_derivative_action.abs() < 1e-6);
    }

    #[test]
    fn test_higher_derivative_action_is_strictly_non_negative() {
        let tri = ReggeTriangulation4D::two_pentachora_glued(1.0).unwrap();
        let field = compute_discrete_curvature_field_4d(&tri, 2.5).unwrap();

        assert!(
            field.higher_derivative_action >= 0.0,
            "Higher-derivative action must be non-negative, got {}",
            field.higher_derivative_action
        );
    }
}
