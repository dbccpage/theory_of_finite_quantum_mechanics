
use crate::cayley_menger::simplex_volume_cayley_menger;
use crate::dihedral_angles::tetrahedron_dihedral_angle_at_edge;
use crate::initial_value_formulation::SpatialSlice3D;
use crate::regge_calculus::ReggeError;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; simplicial Hamiltonian constraint.";

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct VertexHamiltonianConstraint {
    pub vertex: usize,
    pub kinetic_term: f64,
    pub curvature_potential: f64,
    pub cosmological_potential: f64,
    pub residual: f64,
    pub dual_volume: f64,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct HamiltonianConstraintReport {
    pub vertex_constraints: BTreeMap<usize, VertexHamiltonianConstraint>,
    pub max_residual: f64,
    pub rms_residual: f64,
    pub total_kinetic_energy: f64,
    pub total_curvature_potential: f64,
    pub total_cosmological_potential: f64,
    pub total_spatial_volume: f64,
    pub is_satisfied: bool,
}

fn compute_vertex_volumes(
    slice: &SpatialSlice3D,
) -> Result<(BTreeSet<usize>, BTreeMap<usize, f64>, f64), ReggeError> {
    let get_len = |u: usize, v: usize| slice.metric.get(u, v).ok();
    let mut vertex_set = BTreeSet::new();
    for tet in &slice.tetrahedra {
        for &v in tet {
            vertex_set.insert(v);
        }
    }

    let mut vertex_dual_vol = BTreeMap::new();
    for &v in &vertex_set {
        vertex_dual_vol.insert(v, 0.0);
    }

    let mut total_vol = 0.0;
    for tet in &slice.tetrahedra {
        let vol3 = simplex_volume_cayley_menger(tet, get_len)
            .map_err(ReggeError::Computation)?;
        total_vol += vol3;
        let v_share = 0.25 * vol3;
        for &v in tet {
            if let Some(entry) = vertex_dual_vol.get_mut(&v) {
                *entry += v_share;
            }
        }
    }

    Ok((vertex_set, vertex_dual_vol, total_vol))
}

fn compute_edge_angle_sum(
    u: usize,
    v: usize,
    tetrahedra: &[[usize; 4]],
    get_len: impl Fn(usize, usize) -> Option<f64>,
) -> Result<(usize, f64), ReggeError> {
    let mut total_angle = 0.0;
    let mut incident_tets = 0;
    for tet in tetrahedra {
        if tet.contains(&u) && tet.contains(&v) {
            incident_tets += 1;
            let theta = tetrahedron_dihedral_angle_at_edge(tet, (u, v), &get_len)
                .map_err(ReggeError::Computation)?;
            total_angle += theta;
        }
    }
    Ok((incident_tets, total_angle))
}

fn compute_edge_deficits(
    slice: &SpatialSlice3D,
) -> Result<BTreeMap<(usize, usize), f64>, ReggeError> {
    let get_len = |u: usize, v: usize| slice.metric.get(u, v).ok();
    let mut edge_deficits = BTreeMap::new();
    for &(u, v) in &slice.edges {
        let (incident_tets, total_angle) =
            compute_edge_angle_sum(u, v, &slice.tetrahedra, get_len)?;
        if incident_tets > 0 {
            let target = if incident_tets >= 3 {
                2.0 * std::f64::consts::PI
            } else {
                std::f64::consts::PI
            };
            let deficit = target - total_angle;
            edge_deficits.insert((u, v), deficit);
        }
    }
    Ok(edge_deficits)
}

fn evaluate_vertex_constraint(
    v: usize,
    v_vol: f64,
    slice: &SpatialSlice3D,
    momenta: &BTreeMap<(usize, usize), f64>,
    edge_deficits: &BTreeMap<(usize, usize), f64>,
    lambda: f64,
) -> Result<VertexHamiltonianConstraint, ReggeError> {
    let incident_edges: Vec<(usize, usize)> = slice
        .edges
        .iter()
        .copied()
        .filter(|&(e1, e2)| e1 == v || e2 == v)
        .collect();

    let mut sum_pi_sq = 0.0;
    let mut sum_pi = 0.0;
    for &e in &incident_edges {
        let pi = momenta.get(&e).copied().unwrap_or(0.0);
        sum_pi_sq += pi * pi;
        sum_pi += pi;
    }

    let kinetic = (1.0 / v_vol) * (sum_pi_sq - 0.5 * sum_pi * sum_pi);

    let mut curv = 0.0;
    for &e in &incident_edges {
        let len = slice.metric.get(e.0, e.1)?;
        let eps = edge_deficits.get(&e).copied().unwrap_or(0.0);
        curv += 0.5 * len * eps;
    }

    let cosmo = 2.0 * lambda * v_vol;
    let residual = kinetic - curv + cosmo;

    Ok(VertexHamiltonianConstraint {
        vertex: v,
        kinetic_term: kinetic,
        curvature_potential: curv,
        cosmological_potential: cosmo,
        residual,
        dual_volume: v_vol,
    })
}

pub fn evaluate_hamiltonian_constraints(
    slice: &SpatialSlice3D,
    momenta: &BTreeMap<(usize, usize), f64>,
    lambda: f64,
    tolerance: f64,
) -> Result<HamiltonianConstraintReport, ReggeError> {
    let (vertex_set, vertex_dual_vol, total_vol) = compute_vertex_volumes(slice)?;
    let edge_deficits = compute_edge_deficits(slice)?;

    let mut vertex_constraints = BTreeMap::new();
    let mut max_res: f64 = 0.0;
    let mut sum_sq_res = 0.0;
    let mut total_kin = 0.0;
    let mut total_curv = 0.0;
    let mut total_cosmo = 0.0;

    for &v in &vertex_set {
        let v_vol = vertex_dual_vol.get(&v).copied().unwrap_or(1e-12).max(1e-12);
        let vc = evaluate_vertex_constraint(v, v_vol, slice, momenta, &edge_deficits, lambda)?;

        let abs_r = vc.residual.abs();
        if abs_r > max_res {
            max_res = abs_r;
        }
        sum_sq_res += vc.residual * vc.residual;
        total_kin += vc.kinetic_term;
        total_curv += vc.curvature_potential;
        total_cosmo += vc.cosmological_potential;

        vertex_constraints.insert(v, vc);
    }

    let n = vertex_set.len().max(1);
    let rms = (sum_sq_res / n as f64).sqrt();
    let is_satisfied = max_res < tolerance;

    Ok(HamiltonianConstraintReport {
        vertex_constraints,
        max_residual: max_res,
        rms_residual: rms,
        total_kinetic_energy: total_kin,
        total_curvature_potential: total_curv,
        total_cosmological_potential: total_cosmo,
        total_spatial_volume: total_vol,
        is_satisfied,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hamiltonian_constraint_evaluation_single_tetrahedron() {
        let slice = SpatialSlice3D::single_tetrahedron(1.0).unwrap();
        let mut momenta = BTreeMap::new();
        for &e in &slice.edges {
            momenta.insert(e, 0.0);
        }

        let report = evaluate_hamiltonian_constraints(&slice, &momenta, 0.0, 1.0).unwrap();
        assert_eq!(report.vertex_constraints.len(), 4);
        assert_eq!(report.total_kinetic_energy, 0.0);
        assert!(report.total_spatial_volume > 0.1);
    }
}
