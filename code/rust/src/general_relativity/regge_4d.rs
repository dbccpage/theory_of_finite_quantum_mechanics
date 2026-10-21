
use crate::cayley_menger::simplex_volume_cayley_menger;
use crate::dec_laplacian::DecOperators;
use crate::dihedral_angles::pentachoron_dihedral_angle_at_triangle;
use crate::regge_calculus::{EdgeLengthMetric, ReggeError, DEFAULT_TOL};
use omega_homology::simplicial::{OrientedSimplex, SimplicialComplex};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ReggeActionResult4D {
    pub curvature_term: f64,
    pub cosmological_term: f64,
    pub total_action: f64,
    pub lambda_param: f64,
    pub total_4volume: f64,
    pub total_hinges: usize,
    pub interior_hinges: usize,
    pub boundary_hinges: usize,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct HingeTriangle4D {
    pub triangle: [usize; 3],
    pub area: f64,
    pub incident_pentachora: Vec<[usize; 5]>,
    pub dihedral_angles: Vec<f64>,
    pub total_dihedral_angle: f64,
    pub deficit_angle: f64,
    pub is_interior: bool,
}

#[derive(Debug, Clone, PartialEq)]
pub struct ReggeTriangulation4D {
    pub complex: SimplicialComplex,
    pub metric: EdgeLengthMetric,
    pub pentachora: Vec<[usize; 5]>,
    pub hinges: Vec<HingeTriangle4D>,
    pub pentachora_volumes: Vec<f64>,
    pub label: String,
}

impl ReggeTriangulation4D {
    fn build_pentachora_and_volumes(
        complex: &SimplicialComplex,
        metric: &EdgeLengthMetric,
    ) -> Result<(Vec<[usize; 5]>, Vec<f64>), ReggeError> {
        let mut pentachora = Vec::new();
        let mut pentachora_volumes = Vec::new();

        for s4 in complex.simplices(4) {
            let verts = s4.vertices();
            if verts.len() != 5 {
                return Err(ReggeError::Computation(format!(
                    "4-simplex has {} vertices, expected 5",
                    verts.len()
                )));
            }
            let arr = [verts[0], verts[1], verts[2], verts[3], verts[4]];
            let vol = simplex_volume_cayley_menger(&arr, |u, v| metric.get(u, v).ok())
                .map_err(ReggeError::Computation)?;

            if vol <= DEFAULT_TOL {
                return Err(ReggeError::Computation(format!(
                    "4-simplex {arr:?} has non-positive Cayley-Menger volume {vol}"
                )));
            }

            pentachora.push(arr);
            pentachora_volumes.push(vol);
        }

        if pentachora.is_empty() {
            return Err(ReggeError::Computation(
                "No 4-simplices found in complex".to_string(),
            ));
        }

        Ok((pentachora, pentachora_volumes))
    }

    fn collect_incident_dihedrals(
        tri: &[usize; 3],
        metric: &EdgeLengthMetric,
        pentachora: &[[usize; 5]],
    ) -> Result<(Vec<[usize; 5]>, Vec<f64>), ReggeError> {
        let mut incident = Vec::new();
        let mut dihedrals = Vec::new();
        for &p in pentachora {
            if p.contains(&tri[0]) && p.contains(&tri[1]) && p.contains(&tri[2]) {
                incident.push(p);
                let angle = pentachoron_dihedral_angle_at_triangle(&p, tri, |u, v| {
                    metric.get(u, v).ok()
                })
                .map_err(ReggeError::Computation)?;
                dihedrals.push(angle);
            }
        }
        Ok((incident, dihedrals))
    }

    fn build_single_hinge(
        tri: [usize; 3],
        metric: &EdgeLengthMetric,
        pentachora: &[[usize; 5]],
    ) -> Result<Option<HingeTriangle4D>, ReggeError> {
        let area = simplex_volume_cayley_menger(&tri, |u, v| metric.get(u, v).ok())
            .map_err(ReggeError::Computation)?;

        if area <= DEFAULT_TOL {
            return Err(ReggeError::Computation(format!(
                "Hinge triangle {tri:?} has non-positive area {area}"
            )));
        }

        let (incident, dihedrals) = Self::collect_incident_dihedrals(&tri, metric, pentachora)?;
        if incident.is_empty() {
            return Ok(None);
        }

        let total_angle: f64 = dihedrals.iter().copied().sum();
        let is_interior = incident.len() >= 3 || (total_angle - 2.0 * std::f64::consts::PI).abs() < 0.2;
        let target = if is_interior {
            2.0 * std::f64::consts::PI
        } else {
            std::f64::consts::PI
        };
        let deficit = target - total_angle;

        Ok(Some(HingeTriangle4D {
            triangle: tri,
            area,
            incident_pentachora: incident,
            dihedral_angles: dihedrals,
            total_dihedral_angle: total_angle,
            deficit_angle: deficit,
            is_interior,
        }))
    }

    fn build_hinges(
        complex: &SimplicialComplex,
        metric: &EdgeLengthMetric,
        pentachora: &[[usize; 5]],
    ) -> Result<Vec<HingeTriangle4D>, ReggeError> {
        let mut hinges = Vec::new();
        for s2 in complex.simplices(2) {
            let t_verts = s2.vertices();
            let tri = [t_verts[0], t_verts[1], t_verts[2]];
            if let Some(h) = Self::build_single_hinge(tri, metric, pentachora)? {
                hinges.push(h);
            }
        }
        Ok(hinges)
    }

    pub fn try_new(
        complex: SimplicialComplex,
        metric: EdgeLengthMetric,
        label: impl Into<String>,
    ) -> Result<Self, ReggeError> {
        if complex.total_simplices() == 0 {
            return Err(ReggeError::EmptyComplex);
        }
        if complex.max_dimension() < 4 {
            return Err(ReggeError::Computation(format!(
                "Complex max dimension is {}, expected 4 for 4D Regge calculus",
                complex.max_dimension()
            )));
        }

        for e in complex.simplices(1) {
            let v = e.vertices();
            let _ = metric.get(v[0], v[1])?;
        }

        let (pentachora, pentachora_volumes) =
            Self::build_pentachora_and_volumes(&complex, &metric)?;
        let hinges = Self::build_hinges(&complex, &metric, &pentachora)?;

        Ok(Self {
            complex,
            metric,
            pentachora,
            hinges,
            pentachora_volumes,
            label: label.into(),
        })
    }

    pub fn two_pentachora_glued(edge_len: f64) -> Result<Self, ReggeError> {
        if edge_len <= 0.0 || !edge_len.is_finite() {
            return Err(ReggeError::NonFinite);
        }

        let s1 = OrientedSimplex::from_unordered(vec![0, 1, 2, 3, 4])?;
        let s2 = OrientedSimplex::from_unordered(vec![0, 1, 2, 3, 5])?;

        let complex = SimplicialComplex::from_maximal_simplices(vec![s1, s2])?;
        let mut metric = EdgeLengthMetric::new();

        for e in complex.simplices(1) {
            let v = e.vertices();
            metric.set(v[0], v[1], edge_len)?;
        }

        Self::try_new(complex, metric, "two_pentachora_glued")
    }

    fn fan_complex() -> Result<SimplicialComplex, ReggeError> {
        let s1 = OrientedSimplex::from_unordered(vec![0, 1, 2, 3, 4])?;
        let s2 = OrientedSimplex::from_unordered(vec![0, 1, 2, 4, 5])?;
        let s3 = OrientedSimplex::from_unordered(vec![0, 1, 2, 5, 6])?;
        let s4 = OrientedSimplex::from_unordered(vec![0, 1, 2, 3, 6])?;
        Ok(SimplicialComplex::from_maximal_simplices(vec![s1, s2, s3, s4])?)
    }

    fn fan_metric_from_coords(
        complex: &SimplicialComplex,
        coords: &[[f64; 4]; 7],
    ) -> Result<EdgeLengthMetric, ReggeError> {
        let mut metric = EdgeLengthMetric::new();
        for e in complex.simplices(1) {
            let v = e.vertices();
            let u = v[0];
            let w = v[1];
            let p1 = coords[u];
            let p2 = coords[w];
            let mut dist_sq = 0.0;
            for k in 0..4 {
                let d = p1[k] - p2[k];
                dist_sq += d * d;
            }
            metric.set(u, w, dist_sq.sqrt())?;
        }
        Ok(metric)
    }

    pub fn four_pentachora_fan(edge_len: f64) -> Result<Self, ReggeError> {
        if edge_len <= 0.0 || !edge_len.is_finite() {
            return Err(ReggeError::NonFinite);
        }

        let coords: [[f64; 4]; 7] = [
            [0.0, 0.0, 0.0, 0.0],
            [edge_len, 0.0, 0.0, 0.0],
            [0.0, edge_len, 0.0, 0.0],
            [0.0, 0.0, edge_len, 0.0],
            [0.0, 0.0, 0.0, edge_len],
            [0.0, 0.0, -edge_len, 0.0],
            [0.0, 0.0, 0.0, -edge_len],
        ];

        let complex = Self::fan_complex()?;
        let metric = Self::fan_metric_from_coords(&complex, &coords)?;

        Self::try_new(complex, metric, "four_pentachora_flat_fan")
    }

    pub fn compute_action(&self, lambda_param: f64) -> ReggeActionResult4D {
        let mut curvature_term = 0.0;
        let mut interior_count = 0;
        let mut boundary_count = 0;

        for h in &self.hinges {
            curvature_term += h.area * h.deficit_angle;
            if h.is_interior {
                interior_count += 1;
            } else {
                boundary_count += 1;
            }
        }

        let total_4volume: f64 = self.pentachora_volumes.iter().copied().sum();
        let cosmological_term = lambda_param * total_4volume;
        let total_action = curvature_term - cosmological_term;

        ReggeActionResult4D {
            curvature_term,
            cosmological_term,
            total_action,
            lambda_param,
            total_4volume,
            total_hinges: self.hinges.len(),
            interior_hinges: interior_count,
            boundary_hinges: boundary_count,
        }
    }

    fn collect_sorted_edges_and_lengths(&self) -> Result<(Vec<(usize, usize)>, Vec<f64>), String> {
        let mut edges = Vec::new();
        let mut edge_lengths = Vec::new();

        for e in self.complex.simplices(1) {
            let v = e.vertices();
            let (u, w) = if v[0] < v[1] { (v[0], v[1]) } else { (v[1], v[0]) };
            let len = self.metric.get(u, w).map_err(|e| format!("{e:?}"))?;
            edges.push((u, w));
            edge_lengths.push(len);
        }

        let mut edge_order: Vec<usize> = (0..edges.len()).collect();
        edge_order.sort_by_key(|&i| edges[i]);

        let sorted_edges: Vec<(usize, usize)> = edge_order.iter().map(|&i| edges[i]).collect();
        let sorted_lengths: Vec<f64> = edge_order.iter().map(|&i| edge_lengths[i]).collect();
        Ok((sorted_edges, sorted_lengths))
    }

    fn collect_sorted_triangles(&self) -> Vec<[usize; 3]> {
        let mut triangles = Vec::new();
        for t in self.complex.simplices(2) {
            let v = t.vertices();
            let mut arr = [v[0], v[1], v[2]];
            arr.sort();
            triangles.push(arr);
        }
        triangles.sort();
        triangles
    }

    fn compute_star0_volumes(&self, num_vertices: usize) -> Vec<f64> {
        let mut star0 = vec![0.0; num_vertices];
        for (p_idx, &p) in self.pentachora.iter().enumerate() {
            let vol = self.pentachora_volumes[p_idx];
            let v_share = vol / 5.0;
            for &v in &p {
                if v < num_vertices {
                    star0[v] += v_share;
                }
            }
        }
        star0
    }

    fn compute_star1_volumes(
        &self,
        sorted_edges: &[(usize, usize)],
        sorted_lengths: &[f64],
    ) -> Vec<f64> {
        let mut star1 = vec![0.0; sorted_edges.len()];
        for (e_idx, &(u, w)) in sorted_edges.iter().enumerate() {
            for (p_idx, &p) in self.pentachora.iter().enumerate() {
                if p.contains(&u) && p.contains(&w) {
                    let vol = self.pentachora_volumes[p_idx];
                    star1[e_idx] += vol / 10.0;
                }
            }
            if star1[e_idx] <= 1e-15 {
                star1[e_idx] = sorted_lengths[e_idx].powi(3) / 24.0;
            }
        }
        star1
    }

    pub fn build_dec_operators(&self) -> Result<DecOperators, String> {
        let num_vertices = self.complex.num_vertices();
        let (sorted_edges, sorted_lengths) = self.collect_sorted_edges_and_lengths()?;
        let triangles = self.collect_sorted_triangles();
        let star0 = self.compute_star0_volumes(num_vertices);
        let star1 = self.compute_star1_volumes(&sorted_edges, &sorted_lengths);

        DecOperators::new(
            num_vertices,
            sorted_edges,
            triangles,
            sorted_lengths,
            star0,
            star1,
        )
    }

    fn perturbed_dihedral(
        pentachoron: &[usize; 5],
        tri: &[usize; 3],
        edge: (usize, usize),
        base_l: f64,
        shift: f64,
        get_length: &impl Fn(usize, usize) -> Option<f64>,
    ) -> Result<f64, String> {
        let (e1, e2) = edge;
        pentachoron_dihedral_angle_at_triangle(pentachoron, tri, |u, v| {
            if (u == e1 && v == e2) || (u == e2 && v == e1) {
                Some(base_l + shift)
            } else {
                get_length(u, v)
            }
        })
    }

    fn compute_face_schlafli_contribution(
        pentachoron: &[usize; 5],
        tri: &[usize; 3],
        edge: (usize, usize),
        base_l: f64,
        delta: f64,
        get_length: &impl Fn(usize, usize) -> Option<f64>,
    ) -> Result<f64, String> {
        let area = simplex_volume_cayley_menger(tri, get_length)?;
        let theta_plus =
            Self::perturbed_dihedral(pentachoron, tri, edge, base_l, delta, get_length)?;
        let theta_minus =
            Self::perturbed_dihedral(pentachoron, tri, edge, base_l, -delta, get_length)?;

        let d_theta = (theta_plus - theta_minus) / (2.0 * delta);
        Ok(area * d_theta)
    }

    pub fn schlafli_differential_4d(
        pentachoron: &[usize; 5],
        edge: (usize, usize),
        get_length: impl Fn(usize, usize) -> Option<f64>,
        delta: f64,
    ) -> Result<f64, String> {
        let (e1, e2) = edge;
        let base_l = get_length(e1, e2).ok_or("Missing edge length")?;

        let tri_faces: [[usize; 3]; 10] = [
            [pentachoron[0], pentachoron[1], pentachoron[2]],
            [pentachoron[0], pentachoron[1], pentachoron[3]],
            [pentachoron[0], pentachoron[1], pentachoron[4]],
            [pentachoron[0], pentachoron[2], pentachoron[3]],
            [pentachoron[0], pentachoron[2], pentachoron[4]],
            [pentachoron[0], pentachoron[3], pentachoron[4]],
            [pentachoron[1], pentachoron[2], pentachoron[3]],
            [pentachoron[1], pentachoron[2], pentachoron[4]],
            [pentachoron[1], pentachoron[3], pentachoron[4]],
            [pentachoron[2], pentachoron[3], pentachoron[4]],
        ];

        let mut sum_area_dtheta = 0.0;

        for tri in &tri_faces {
            sum_area_dtheta += Self::compute_face_schlafli_contribution(
                pentachoron,
                tri,
                edge,
                base_l,
                delta,
                &get_length,
            )?;
        }

        Ok(sum_area_dtheta)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_two_pentachora_glued_construction() {
        let tri = ReggeTriangulation4D::two_pentachora_glued(1.0).unwrap();
        assert_eq!(tri.pentachora.len(), 2);
        assert!(tri.pentachora_volumes[0] > 0.02);
        assert_eq!(tri.complex.num_vertices(), 6);

        let act = tri.compute_action(0.0);
        assert!(act.curvature_term.is_finite());
        assert_eq!(act.cosmological_term, 0.0);
    }

    #[test]
    fn test_four_pentachora_flat_fan_deficit() {
        let fan = ReggeTriangulation4D::four_pentachora_fan(1.0).unwrap();
        assert_eq!(fan.pentachora.len(), 4);

        let central_hinge = fan
            .hinges
            .iter()
            .find(|h| h.triangle == [0, 1, 2])
            .expect("Central hinge [0, 1, 2] must exist");

        assert_eq!(central_hinge.incident_pentachora.len(), 4);
        let expected_angle = 2.0 * std::f64::consts::PI;
        assert!((central_hinge.total_dihedral_angle - expected_angle).abs() < 1e-9);
        assert!(central_hinge.deficit_angle.abs() < 1e-9);
    }
}
