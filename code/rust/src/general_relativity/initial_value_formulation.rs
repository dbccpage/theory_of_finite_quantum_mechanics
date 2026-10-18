
use crate::cayley_menger::simplex_volume_cayley_menger;
use crate::regge_calculus::{EdgeLengthMetric, ReggeError};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; 3+1 ADM simplicial dynamics.";

#[derive(Debug, Clone, PartialEq)]
pub struct SpatialSlice3D {
    pub tetrahedra: Vec<[usize; 4]>,
    pub edges: Vec<(usize, usize)>,
    pub metric: EdgeLengthMetric,
    pub time_index: usize,
}

impl SpatialSlice3D {
    pub fn try_new(
        tetrahedra: Vec<[usize; 4]>,
        metric: EdgeLengthMetric,
        time_index: usize,
    ) -> Result<Self, ReggeError> {
        let mut edge_set = BTreeSet::new();
        for tet in &tetrahedra {
            for i in 0..4 {
                for j in (i + 1)..4 {
                    let u = tet[i].min(tet[j]);
                    let v = tet[i].max(tet[j]);
                    edge_set.insert((u, v));
                }
            }
        }

        for &(u, v) in &edge_set {
            let _ = metric.get(u, v)?;
        }

        Ok(Self {
            tetrahedra,
            edges: edge_set.into_iter().collect(),
            metric,
            time_index,
        })
    }

    pub fn single_tetrahedron(side_len: f64) -> Result<Self, ReggeError> {
        let mut metric = EdgeLengthMetric::new();
        let tet = [0, 1, 2, 3];
        for i in 0..4 {
            for j in (i + 1)..4 {
                metric.set(i, j, side_len)?;
            }
        }
        Self::try_new(vec![tet], metric, 0)
    }

    pub fn total_volume(&self) -> Result<f64, ReggeError> {
        let mut sum = 0.0;
        let get_len = |u: usize, v: usize| self.metric.get(u, v).ok();
        for tet in &self.tetrahedra {
            let vol = simplex_volume_cayley_menger(tet, get_len)
                .map_err(ReggeError::Computation)?;
            sum += vol;
        }
        Ok(sum)
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct SimplicialSlab4D {
    pub slice_t0: SpatialSlice3D,
    pub slice_t1: SpatialSlice3D,
    pub lapse: BTreeMap<usize, f64>,
    pub delta_t: f64,
}

impl SimplicialSlab4D {
    pub fn new(
        slice_t0: SpatialSlice3D,
        slice_t1: SpatialSlice3D,
        lapse: BTreeMap<usize, f64>,
        delta_t: f64,
    ) -> Result<Self, ReggeError> {
        if delta_t <= 0.0 || !delta_t.is_finite() {
            return Err(ReggeError::NonFinite);
        }
        Ok(Self {
            slice_t0,
            slice_t1,
            lapse,
            delta_t,
        })
    }

    pub fn strut_length(&self, v: usize) -> Result<f64, ReggeError> {
        let n = self.lapse.get(&v).copied().unwrap_or(1.0);
        if n <= 0.0 || !n.is_finite() {
            return Err(ReggeError::NonFinite);
        }
        Ok(n * self.delta_t)
    }

    pub fn canonical_momenta(&self) -> Result<BTreeMap<(usize, usize), f64>, ReggeError> {
        let mut momenta = BTreeMap::new();
        for &(u, v) in &self.slice_t0.edges {
            let l0 = self.slice_t0.metric.get(u, v)?;
            let l1 = self.slice_t1.metric.get(u, v)?;

            let s0 = l0 * l0;
            let s1 = l1 * l1;

            let n_u = self.lapse.get(&u).copied().unwrap_or(1.0);
            let n_v = self.lapse.get(&v).copied().unwrap_or(1.0);
            let n_avg = 0.5 * (n_u + n_v);

            let pi = (s1 - s0) / (2.0 * n_avg * self.delta_t);
            momenta.insert((u, v), pi);
        }
        Ok(momenta)
    }
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct CauchyStepSummary {
    pub time_index: usize,
    pub delta_t: f64,
    pub mean_momentum: f64,
    pub max_momentum: f64,
    pub total_spatial_volume: f64,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spatial_slice_volume_and_struts() {
        let slice = SpatialSlice3D::single_tetrahedron(1.0).unwrap();
        let vol = slice.total_volume().unwrap();
        let expected_vol = 1.0 / (6.0 * 2.0f64.sqrt());
        assert!((vol - expected_vol).abs() < 1e-9);

        let mut lapse = BTreeMap::new();
        for v in 0..4 {
            lapse.insert(v, 1.0);
        }

        let slice_next = SpatialSlice3D::single_tetrahedron(1.1).unwrap();
        let slab = SimplicialSlab4D::new(slice, slice_next, lapse, 0.1).unwrap();

        assert_eq!(slab.strut_length(0).unwrap(), 0.1);

        let momenta = slab.canonical_momenta().unwrap();
        assert_eq!(momenta.len(), 6);

        for &pi in momenta.values() {
            assert!((pi - 1.05).abs() < 1e-6);
        }
    }
}
