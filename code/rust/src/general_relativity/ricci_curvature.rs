//! Discrete Simplicial Ricci and Scalar Curvatures & Higher-Derivative Regge Gravity (Hamber §7.2-7.3).
//!
//! In a D-dimensional simplicial complex (D=4):
//! - Dual volume associated with vertex v:
//!   $$V(v) = \frac{1}{D+1} \sum_{\sigma \supset v} V_D(\sigma)$$
//! - Integrated scalar curvature at vertex v:
//!   $$\mathcal{R}(v) = 2 \sum_{h \supset v} A_h \epsilon_h$$
//! - Local scalar curvature density at vertex v:
//!   $$R(v) = \frac{\mathcal{R}(v)}{V(v)} = \frac{2 \sum_{h \supset v} A_h \epsilon_h}{V(v)}$$
//! - Einstein–Hilbert–Regge action equivalence:
//!   $$S_{\text{EH}} = \frac{1}{2} \sum_v V(v) R(v) = \sum_h A_h \epsilon_h = S_{\text{Regge}}$$
//! - Higher-Derivative Regge action (Hamber & Williams 1984):
//!   $$S_{\text{HD}} = a \sum_v V(v) R(v)^2 = 4 a \sum_v \frac{1}{V(v)} \left( \sum_{h \supset v} A_h \epsilon_h \right)^2$$
//!   This curvature-squared term is strictly non-negative (S_HD >= 0) and regulates
//!   the Euclidean conformal factor instability in quantum Regge calculus.
//!
//! AuthorityEffect: None.

use crate::regge_4d::ReggeTriangulation4D;
use crate::regge_calculus::ReggeError;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; discrete Ricci and higher-derivative Regge.";

/// Curvature and volume measures localized at a single vertex in a 4D triangulation.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct VertexCurvature4D {
    pub vertex: usize,
    /// Barycentric dual volume V(v) = 1/5 ∑_{σ ⊃ v} V_4(σ).
    pub dual_volume: f64,
    /// Integrated scalar curvature: 2 ∑_{h ⊃ v} A_h ε_h.
    pub integrated_scalar_curvature: f64,
    /// Local scalar curvature density: R(v) = 2 ∑_{h ⊃ v} A_h ε_h / V(v).
    pub scalar_curvature_density: f64,
    /// Incident 4-simplices.
    pub incident_pentachora_count: usize,
    /// Incident hinges.
    pub incident_hinge_count: usize,
}

/// Complete curvature field and higher-derivative action across all vertices of a 4D triangulation.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct DiscreteCurvatureField4D {
    pub vertex_curvatures: BTreeMap<usize, VertexCurvature4D>,
    /// Total 4-volume: ∑_σ V_4(σ) = ∑_v V(v).
    pub total_4volume: f64,
    /// Total Einstein-Hilbert action: 1/2 ∑_v V(v) R(v) = ∑_h A_h ε_h.
    pub einstein_hilbert_action: f64,
    /// Higher-derivative curvature squared action: a ∑_v V(v) R(v)².
    pub higher_derivative_action: f64,
    pub coupling_a: f64,
}

/// Compute vertex-localized Ricci scalar curvature densities and higher-derivative action.
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
        let share = 0.2 * vol; // 1/5 share of 4-simplex volume per vertex
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

    // Distribute hinge curvature 2 * A_h * ε_h equally among its 3 vertices:
    // Hinge h = {u, v, w} contributes (2/3) * A_h * ε_h to each vertex,
    // so ∑_v ∑_{h ⊃ v} (2/3) A_h ε_h = 2 ∑_h A_h ε_h.
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

        // Total 4-volume should equal sum of the 4 pentachora volumes
        let sum_pent_vol: f64 = tri.pentachora_volumes.iter().sum();
        assert!((field.total_4volume - sum_pent_vol).abs() < 1e-7);

        // Float residual of this discrete field. Not the flatness admission:
        // that decision is `exact_regge::einstein_hilbert_fence`.
        assert!(field.einstein_hilbert_action.abs() < 1e-6);

        // Higher-derivative action is non-negative and zero for flat space
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
