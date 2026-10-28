
use crate::discrete_spacetime::DiscreteSpacetime;
use engine_homology::errors::HomologicalError;
use engine_homology::simplicial::{OrientedSimplex, Simplex, SimplicialComplex};
use std::collections::BTreeMap;

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; finite 2D Regge face.";

pub const DEFAULT_TOL: f64 = 1e-9;

#[derive(Debug, Clone, PartialEq)]
pub enum ReggeError {
    Homology(String),
    EmptyComplex,
    NotTwoDimensional {
        max_dim: usize,
    },
    MissingEdgeLength {
        u: usize,
        v: usize,
    },
    NonPositiveLength {
        u: usize,
        v: usize,
        length: f64,
    },
    UnknownVertex {
        vertex: usize,
    },
    DegenerateFan {
        n_triangles: usize,
    },
    TriangleInequality {
        triangle: [usize; 3],
    },
    DegenerateAngle {
        triangle: [usize; 3],
        vertex: usize,
    },
    NonFinite,
    Computation(String),
}

impl From<HomologicalError> for ReggeError {
    fn from(e: HomologicalError) -> Self {
        ReggeError::Homology(format!("{e:?}"))
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct EdgeLengthMetric {
    lengths: BTreeMap<(usize, usize), f64>,
}

impl EdgeLengthMetric {
    pub fn new() -> Self {
        Self {
            lengths: BTreeMap::new(),
        }
    }

    pub fn set(&mut self, u: usize, v: usize, length: f64) -> Result<(), ReggeError> {
        if !length.is_finite() {
            return Err(ReggeError::NonFinite);
        }
        if length <= 0.0 {
            return Err(ReggeError::NonPositiveLength { u, v, length });
        }
        let (a, b) = if u < v { (u, v) } else { (v, u) };
        if a == b {
            return Err(ReggeError::NonPositiveLength { u, v, length });
        }
        self.lengths.insert((a, b), length);
        Ok(())
    }

    pub fn get(&self, u: usize, v: usize) -> Result<f64, ReggeError> {
        let (a, b) = if u < v { (u, v) } else { (v, u) };
        self.lengths
            .get(&(a, b))
            .copied()
            .ok_or(ReggeError::MissingEdgeLength { u: a, v: b })
    }

    pub fn edge_count(&self) -> usize {
        self.lengths.len()
    }
}

impl Default for EdgeLengthMetric {
    fn default() -> Self {
        Self::new()
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ReggeCalculus {
    pub complex: SimplicialComplex,
    pub metric: EdgeLengthMetric,
    pub label: String,
}

impl ReggeCalculus {
    pub fn new(degree: usize, label: impl Into<String>) -> Self {
        let n = degree.max(2);
        let complex = SimplicialComplex::standard_n_simplex(n.min(2)).expect("standard simplex");
        let mut metric = EdgeLengthMetric::new();
        for e in complex.simplices(1) {
            let v = e.vertices();
            let _ = metric.set(v[0], v[1], 1.0);
        }
        Self {
            complex,
            metric,
            label: label.into(),
        }
    }

    pub fn try_from_spacetime(
        spacetime: &DiscreteSpacetime,
        metric: EdgeLengthMetric,
        label: impl Into<String>,
    ) -> Result<Self, ReggeError> {
        Self::try_new(spacetime.complex.clone(), metric, label)
    }

    pub fn try_new(
        complex: SimplicialComplex,
        metric: EdgeLengthMetric,
        label: impl Into<String>,
    ) -> Result<Self, ReggeError> {
        if complex.total_simplices() == 0 {
            return Err(ReggeError::EmptyComplex);
        }
        if complex.max_dimension() < 2 {
            return Err(ReggeError::NotTwoDimensional {
                max_dim: complex.max_dimension(),
            });
        }
        for e in complex.simplices(1) {
            let v = e.vertices();
            let _ = metric.get(v[0], v[1])?;
        }
        let geo = Self {
            complex,
            metric,
            label: label.into(),
        };
        geo.validate_triangle_inequalities()?;
        Ok(geo)
    }

    pub fn equilateral_fan(n_triangles: usize, edge_len: f64) -> Result<Self, ReggeError> {
        if n_triangles < 1 {
            return Err(ReggeError::EmptyComplex);
        }
        if n_triangles == 2 {
            return Err(ReggeError::DegenerateFan { n_triangles });
        }
        if !(edge_len.is_finite() && edge_len > 0.0) {
            return Err(ReggeError::NonFinite);
        }
        let maximal = if n_triangles == 1 {
            vec![OrientedSimplex::from_unordered(vec![0, 1, 2])?]
        } else {
            let mut maximal = Vec::new();
            for i in 1..=n_triangles {
                let j = if i == n_triangles { 1 } else { i + 1 };
                maximal.push(OrientedSimplex::from_unordered(vec![0, i, j])?);
            }
            maximal
        };
        let complex = SimplicialComplex::from_maximal_simplices(maximal)?;
        let mut metric = EdgeLengthMetric::new();
        for e in complex.simplices(1) {
            let v = e.vertices();
            metric.set(v[0], v[1], edge_len)?;
        }
        Self::try_new(complex, metric, format!("fan_{n_triangles}"))
    }

    fn validate_triangle_inequalities(&self) -> Result<(), ReggeError> {
        for t in self.complex.simplices(2) {
            let v = t.vertices();
            let a = self.metric.get(v[1], v[2])?;
            let b = self.metric.get(v[0], v[2])?;
            let c = self.metric.get(v[0], v[1])?;
            if a + b <= c + DEFAULT_TOL || a + c <= b + DEFAULT_TOL || b + c <= a + DEFAULT_TOL {
                return Err(ReggeError::TriangleInequality {
                    triangle: [v[0], v[1], v[2]],
                });
            }
        }
        Ok(())
    }

    pub fn angle_at(&self, triangle: &Simplex, vertex: usize) -> Result<f64, ReggeError> {
        let verts = triangle.vertices();
        if verts.len() != 3 {
            return Err(ReggeError::NotTwoDimensional {
                max_dim: triangle.dimension(),
            });
        }
        let (i, j, k) = (verts[0], verts[1], verts[2]);
        let (p, q, opp) = if vertex == i {
            (j, k, self.metric.get(j, k)?)
        } else if vertex == j {
            (i, k, self.metric.get(i, k)?)
        } else if vertex == k {
            (i, j, self.metric.get(i, j)?)
        } else {
            return Err(ReggeError::DegenerateAngle {
                triangle: [i, j, k],
                vertex,
            });
        };
        let a = self.metric.get(vertex, p)?;
        let b = self.metric.get(vertex, q)?;
        let c = opp;
        let denom = 2.0 * a * b;
        if denom.abs() < DEFAULT_TOL {
            return Err(ReggeError::DegenerateAngle {
                triangle: [i, j, k],
                vertex,
            });
        }
        let cos_c = (a * a + b * b - c * c) / denom;
        let cos_c = cos_c.clamp(-1.0, 1.0);
        let ang = cos_c.acos();
        if !ang.is_finite() {
            return Err(ReggeError::NonFinite);
        }
        Ok(ang)
    }

    pub fn angle_sum_at_vertex(&self, v: usize) -> Result<f64, ReggeError> {
        self.ensure_vertex(v)?;
        let mut sum = 0.0;
        for t in self.complex.simplices(2) {
            if t.vertices().contains(&v) {
                sum += self.angle_at(t, v)?;
            }
        }
        Ok(sum)
    }

    pub fn deficit_at_vertex(&self, v: usize) -> Result<f64, ReggeError> {
        Ok(std::f64::consts::TAU - self.angle_sum_at_vertex(v)?)
    }

    pub fn vertex_deficits(&self) -> Result<Vec<f64>, ReggeError> {
        self.complex
            .simplices(0)
            .iter()
            .map(|simplex| self.deficit_at_vertex(simplex.vertices()[0]))
            .collect()
    }

    fn ensure_vertex(&self, vertex: usize) -> Result<(), ReggeError> {
        let simplex = Simplex::from_unordered(vec![vertex])?;
        if self.complex.contains(&simplex) {
            Ok(())
        } else {
            Err(ReggeError::UnknownVertex { vertex })
        }
    }

    pub fn regge_action_2d(&self) -> Result<f64, ReggeError> {
        Ok(self.vertex_deficits()?.into_iter().sum())
    }

    pub fn degree(&self) -> usize {
        self.complex.max_dimension()
    }

    pub fn authority_fence() -> &'static str {
        AUTHORITY_FENCE
    }

    pub fn simplex_volume(&self, simplex: &Simplex) -> Result<f64, ReggeError> {
        let verts = simplex.vertices();
        crate::cayley_menger::simplex_volume_cayley_menger(verts, |u, v| self.metric.get(u, v).ok())
            .map_err(ReggeError::Computation)
    }

    pub fn deficit_at_edge(&self, u: usize, v: usize) -> Result<f64, ReggeError> {
        let (e1, e2) = if u < v { (u, v) } else { (v, u) };
        let mut angle_sum = 0.0;
        let mut count = 0;

        for tet in self.complex.simplices(3) {
            let verts = tet.vertices();
            if verts.contains(&e1) && verts.contains(&e2) {
                let tet_arr: [usize; 4] = [verts[0], verts[1], verts[2], verts[3]];
                let theta = crate::dihedral_angles::tetrahedron_dihedral_angle_at_edge(
                    &tet_arr,
                    (e1, e2),
                    |a, b| self.metric.get(a, b).ok(),
                )
                .map_err(ReggeError::Computation)?;
                angle_sum += theta;
                count += 1;
            }
        }

        if count == 0 {
            return Err(ReggeError::Computation(format!(
                "Edge ({e1}, {e2}) has no incident 3-simplices"
            )));
        }

        Ok(std::f64::consts::TAU - angle_sum)
    }

    pub fn regge_action_with_lambda(
        &self,
        lambda_param: f64,
    ) -> Result<crate::regge_action::ReggeActionResult, ReggeError> {
        let dim = self.complex.max_dimension();
        let mut hinges = Vec::new();
        let mut simplex_volumes = Vec::new();

        if dim == 2 {
            for v_simplex in self.complex.simplices(0) {
                let v = v_simplex.vertices()[0];
                let eps = self.deficit_at_vertex(v)?;
                hinges.push((1.0, eps));
            }
            for tri in self.complex.simplices(2) {
                let vol = self.simplex_volume(tri)?;
                simplex_volumes.push(vol);
            }
        } else if dim == 3 {
            for e_simplex in self.complex.simplices(1) {
                let v = e_simplex.vertices();
                let len = self.metric.get(v[0], v[1])?;
                let eps = self.deficit_at_edge(v[0], v[1])?;
                hinges.push((len, eps));
            }
            for tet in self.complex.simplices(3) {
                let vol = self.simplex_volume(tet)?;
                simplex_volumes.push(vol);
            }
        } else {
            return Err(ReggeError::Computation(format!(
                "Unsupported dimension {dim} for direct Regge action"
            )));
        }

        Ok(crate::regge_action::compute_regge_action(
            &hinges,
            &simplex_volumes,
            lambda_param,
            dim,
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn equilateral_triangle_angles() {
        let g = ReggeCalculus::equilateral_fan(1, 1.0).unwrap();
        let t = &g.complex.simplices(2)[0];
        for &v in t.vertices() {
            let a = g.angle_at(t, v).unwrap();
            assert!((a - std::f64::consts::FRAC_PI_3).abs() < 1e-9);
        }
    }

    #[test]
    fn six_equilateral_flat_at_center() {
        let g = ReggeCalculus::equilateral_fan(6, 1.0).unwrap();
        let d0 = g.deficit_at_vertex(0).unwrap();
        assert!(d0.abs() < 1e-8, "expected flat center, deficit={d0}");
    }

    #[test]
    fn three_equilateral_positive_curvature_cone() {
        let g = ReggeCalculus::equilateral_fan(3, 1.0).unwrap();
        let d0 = g.deficit_at_vertex(0).unwrap();
        assert!(
            (d0 - std::f64::consts::PI).abs() < 1e-8,
            "expected deficit π, got {d0}"
        );
    }

    #[test]
    fn rejects_triangle_inequality() {
        let complex = SimplicialComplex::standard_n_simplex(2).unwrap();
        let mut metric = EdgeLengthMetric::new();
        metric.set(0, 1, 1.0).unwrap();
        metric.set(1, 2, 1.0).unwrap();
        metric.set(0, 2, 3.0).unwrap();
        let err = ReggeCalculus::try_new(complex, metric, "bad");
        assert!(matches!(err, Err(ReggeError::TriangleInequality { .. })));
    }

    #[test]
    fn two_triangle_fan_is_not_silently_one_triangle() {
        assert!(matches!(
            ReggeCalculus::equilateral_fan(2, 1.0),
            Err(ReggeError::DegenerateFan { n_triangles: 2 })
        ));
    }

    #[test]
    fn gapped_vertex_ids_do_not_invent_two_pi() {
        let complex = SimplicialComplex::from_maximal_simplices(vec![
            OrientedSimplex::from_unordered(vec![0, 1, 3]).unwrap(),
        ])
        .unwrap();
        assert_eq!(complex.num_vertices(), 4);
        let mut metric = EdgeLengthMetric::new();
        metric.set(0, 1, 1.0).unwrap();
        metric.set(1, 3, 1.0).unwrap();
        metric.set(0, 3, 1.0).unwrap();
        let g = ReggeCalculus::try_new(complex, metric, "gap").unwrap();
        let deficits = g.vertex_deficits().unwrap();
        assert_eq!(deficits.len(), 3);
        let expected = std::f64::consts::TAU - std::f64::consts::FRAC_PI_3;
        for deficit in &deficits {
            assert!((deficit - expected).abs() < 1e-8, "deficit={deficit}");
        }
        let action = g.regge_action_2d().unwrap();
        assert!((action - 3.0 * expected).abs() < 1e-8, "action={action}");
        assert!(matches!(
            g.deficit_at_vertex(2),
            Err(ReggeError::UnknownVertex { vertex: 2 })
        ));
    }

    #[test]
    fn rejects_non_positive_length() {
        let mut m = EdgeLengthMetric::new();
        assert!(matches!(
            m.set(0, 1, 0.0),
            Err(ReggeError::NonPositiveLength { .. })
        ));
    }

    #[test]
    fn new_and_fence() {
        let x = ReggeCalculus::new(2, "test");
        assert_eq!(x.degree(), 2);
        assert!(ReggeCalculus::authority_fence().contains("AuthorityEffect None"));
    }
}
