
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

pub const DEFAULT_DEC_TOL: f64 = 1e-12;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct DecHodgeStar {
    pub star0_vertex_volumes: Vec<f64>,
    pub star1_edge_volumes: Vec<f64>,
    pub hodge_edge_weights: Vec<f64>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct DecOperators {
    pub num_vertices: usize,
    pub edges: Vec<(usize, usize)>,
    pub edge_index: BTreeMap<(usize, usize), usize>,
    pub triangles: Vec<[usize; 3]>,
    pub edge_lengths: Vec<f64>,
    pub hodge: DecHodgeStar,
}

impl DecOperators {
    pub fn new(
        num_vertices: usize,
        edges: Vec<(usize, usize)>,
        triangles: Vec<[usize; 3]>,
        edge_lengths: Vec<f64>,
        star0_vertex_volumes: Vec<f64>,
        star1_edge_volumes: Vec<f64>,
    ) -> Result<Self, String> {
        if num_vertices == 0 {
            return Err("DEC complex must have at least 1 vertex".to_string());
        }
        if edges.len() != edge_lengths.len() {
            return Err(format!(
                "Edge count mismatch: {} edges vs {} lengths",
                edges.len(),
                edge_lengths.len()
            ));
        }
        if edges.len() != star1_edge_volumes.len() {
            return Err(format!(
                "Edge count mismatch: {} edges vs {} star1 dual volumes",
                edges.len(),
                star1_edge_volumes.len()
            ));
        }
        if num_vertices != star0_vertex_volumes.len() {
            return Err(format!(
                "Vertex count mismatch: {} vertices vs {} star0 dual volumes",
                num_vertices,
                star0_vertex_volumes.len()
            ));
        }

        let mut edge_index = BTreeMap::new();
        let mut hodge_edge_weights = Vec::with_capacity(edges.len());

        for (idx, &(u, v)) in edges.iter().enumerate() {
            if u >= v {
                return Err(format!(
                    "Edge endpoints must be strictly ordered u < v: ({u}, {v})"
                ));
            }
            if v >= num_vertices {
                return Err(format!(
                    "Edge vertex {v} exceeds num_vertices {num_vertices}"
                ));
            }
            if edge_index.insert((u, v), idx).is_some() {
                return Err(format!("Duplicate edge ({u}, {v}) in DEC operators"));
            }

            let len = edge_lengths[idx];
            if len <= 0.0 || !len.is_finite() {
                return Err(format!(
                    "Invalid non-positive edge length {len} on edge ({u}, {v})"
                ));
            }

            let dual_vol = star1_edge_volumes[idx];
            if dual_vol <= 0.0 || !dual_vol.is_finite() {
                return Err(format!(
                    "Invalid non-positive star1 dual volume {dual_vol} on edge ({u}, {v})"
                ));
            }

            let weight = dual_vol / len;
            if !weight.is_finite() || weight <= 0.0 {
                return Err("Hodge edge weight must be finite and positive".into());
            }
            hodge_edge_weights.push(weight);
        }

        for tri in &triangles {
            let (u, v, w) = (tri[0], tri[1], tri[2]);
            if !(u < v && v < w) {
                return Err(format!(
                    "Triangle vertices must be strictly ordered u < v < w: {tri:?}"
                ));
            }
            if w >= num_vertices {
                return Err(format!(
                    "Triangle vertex {w} exceeds num_vertices {num_vertices}"
                ));
            }
            if !edge_index.contains_key(&(u, v)) {
                return Err(format!(
                    "Missing boundary edge ({u}, {v}) for triangle {tri:?}"
                ));
            }
            if !edge_index.contains_key(&(v, w)) {
                return Err(format!(
                    "Missing boundary edge ({v}, {w}) for triangle {tri:?}"
                ));
            }
            if !edge_index.contains_key(&(u, w)) {
                return Err(format!(
                    "Missing boundary edge ({u}, {w}) for triangle {tri:?}"
                ));
            }
        }

        for (v, &vol) in star0_vertex_volumes.iter().enumerate() {
            if vol <= 0.0 || !vol.is_finite() {
                return Err(format!(
                    "Invalid non-positive star0 dual volume {vol} on vertex {v}"
                ));
            }
        }

        Ok(Self {
            num_vertices,
            edges,
            edge_index,
            triangles,
            edge_lengths,
            hodge: DecHodgeStar {
                star0_vertex_volumes,
                star1_edge_volumes,
                hodge_edge_weights,
            },
        })
    }

    pub(crate) fn validate(&self) -> Result<(), String> {
        let rebuilt = Self::new(
            self.num_vertices,
            self.edges.clone(),
            self.triangles.clone(),
            self.edge_lengths.clone(),
            self.hodge.star0_vertex_volumes.clone(),
            self.hodge.star1_edge_volumes.clone(),
        )?;
        if self.edge_index != rebuilt.edge_index
            || self.hodge.hodge_edge_weights != rebuilt.hodge.hodge_edge_weights
        {
            return Err("DEC cached metrics or edge indices differ from their inputs".into());
        }
        Ok(())
    }

    pub fn coboundary_d0(&self, psi: &[f64]) -> Result<Vec<f64>, String> {
        self.validate()?;
        if psi.iter().any(|x| !x.is_finite()) {
            return Err("form entries must be finite".into());
        }
        if psi.len() != self.num_vertices {
            return Err(format!(
                "0-form state vector dimension mismatch: expected {}, got {}",
                self.num_vertices,
                psi.len()
            ));
        }

        let mut d_psi = Vec::with_capacity(self.edges.len());
        for &(u, v) in &self.edges {
            d_psi.push(psi[v] - psi[u]);
        }
        if d_psi.iter().any(|x| !x.is_finite()) {
            return Err("DEC arithmetic overflow".into());
        }
        Ok(d_psi)
    }

    pub fn coboundary_d1(&self, omega: &[f64]) -> Result<Vec<f64>, String> {
        self.validate()?;
        if omega.iter().any(|x| !x.is_finite()) {
            return Err("form entries must be finite".into());
        }
        if omega.len() != self.edges.len() {
            return Err(format!(
                "1-form vector dimension mismatch: expected {}, got {}",
                self.edges.len(),
                omega.len()
            ));
        }

        let mut d_omega = Vec::with_capacity(self.triangles.len());
        for tri in &self.triangles {
            let (u, v, w) = (tri[0], tri[1], tri[2]);
            let e_uv = self.edge_index[&(u, v)];
            let e_vw = self.edge_index[&(v, w)];
            let e_uw = self.edge_index[&(u, w)];

            let val = omega[e_vw] - omega[e_uw] + omega[e_uv];
            d_omega.push(val);
        }
        if d_omega.iter().any(|x| !x.is_finite()) {
            return Err("DEC arithmetic overflow".into());
        }
        Ok(d_omega)
    }

    pub fn verify_nilpotency_d1_d0(&self, psi: &[f64]) -> Result<(bool, f64), String> {
        let d0_psi = self.coboundary_d0(psi)?;
        let d1_d0_psi = self.coboundary_d1(&d0_psi)?;

        let mut max_res = 0.0f64;
        for &val in &d1_d0_psi {
            let abs = val.abs();
            if abs > max_res {
                max_res = abs;
            }
        }
        Ok((max_res < DEFAULT_DEC_TOL, max_res))
    }

    pub fn laplacian_0form(&self, psi: &[f64]) -> Result<Vec<f64>, String> {
        self.validate()?;
        if psi.iter().any(|x| !x.is_finite()) {
            return Err("form entries must be finite".into());
        }
        if psi.len() != self.num_vertices {
            return Err(format!(
                "0-form state vector dimension mismatch: expected {}, got {}",
                self.num_vertices,
                psi.len()
            ));
        }

        let mut delta_psi = vec![0.0; self.num_vertices];

        for (idx, &(u, v)) in self.edges.iter().enumerate() {
            let w_e = self.hodge.hodge_edge_weights[idx];
            let diff = psi[u] - psi[v];

            delta_psi[u] += w_e * diff;
            delta_psi[v] -= w_e * diff;
        }

        for v in 0..self.num_vertices {
            let star0 = self.hodge.star0_vertex_volumes[v];
            delta_psi[v] /= star0;
        }

        if delta_psi.iter().any(|x| !x.is_finite()) {
            return Err("DEC arithmetic overflow".into());
        }
        Ok(delta_psi)
    }

    pub fn inner_product_0form(&self, phi: &[f64], psi: &[f64]) -> Result<f64, String> {
        self.validate()?;
        if psi.iter().any(|x| !x.is_finite()) || phi.iter().any(|x| !x.is_finite()) {
            return Err("form entries must be finite".into());
        }
        if phi.len() != self.num_vertices || psi.len() != self.num_vertices {
            return Err("Vector dimension mismatch in 0-form inner product".to_string());
        }

        let mut sum = 0.0;
        for v in 0..self.num_vertices {
            sum += self.hodge.star0_vertex_volumes[v] * phi[v] * psi[v];
        }
        if !sum.is_finite() {
            return Err("DEC arithmetic overflow".into());
        }
        Ok(sum)
    }

    pub fn dirichlet_energy_0form(&self, psi: &[f64]) -> Result<f64, String> {
        let d_psi = self.coboundary_d0(psi)?;
        let mut energy = 0.0;
        for (idx, &grad) in d_psi.iter().enumerate() {
            let w_e = self.hodge.hodge_edge_weights[idx];
            energy += w_e * grad * grad;
        }
        if !energy.is_finite() {
            return Err("DEC arithmetic overflow".into());
        }
        Ok(energy)
    }

    pub fn verify_self_adjointness(
        &self,
        phi: &[f64],
        psi: &[f64],
    ) -> Result<(f64, f64, f64), String> {
        let lap_psi = self.laplacian_0form(psi)?;
        let lap_phi = self.laplacian_0form(phi)?;

        let lhs = self.inner_product_0form(phi, &lap_psi)?;
        let rhs = self.inner_product_0form(&lap_phi, psi)?;

        let diff = (lhs - rhs).abs();
        Ok((lhs, rhs, diff))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dec_triangle_nilpotency_and_kernel() {
        let edges = vec![(0, 1), (0, 2), (1, 2)];
        let triangles = vec![[0, 1, 2]];
        let lengths = vec![1.0, 1.0, 1.0];
        let star0 = vec![1.0, 1.0, 1.0];
        let star1 = vec![1.0, 1.0, 1.0];

        let dec = DecOperators::new(3, edges, triangles, lengths, star0, star1).unwrap();

        let psi = vec![2.5, -1.0, 4.2];
        let (is_nilpotent, res) = dec.verify_nilpotency_d1_d0(&psi).unwrap();
        assert!(is_nilpotent);
        assert!(res < 1e-14);

        let const_psi = vec![3.14159; 3];
        let lap = dec.laplacian_0form(&const_psi).unwrap();
        for &val in &lap {
            assert!(val.abs() < 1e-14);
        }

        let phi = vec![1.0, 0.5, -2.0];
        let (lhs, rhs, diff) = dec.verify_self_adjointness(&phi, &psi).unwrap();
        assert!(diff < 1e-12, "Self-adjointness violation: {lhs} vs {rhs}");
    }
}
