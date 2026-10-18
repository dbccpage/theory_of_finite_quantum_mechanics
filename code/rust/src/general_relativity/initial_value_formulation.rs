//! 3+1 (ADM) Simplicial Cauchy Dynamics and Initial-Value Formulation (MTW §42.11, Sorkin 1975, Hamber §6.5).
//!
//! Decomposes spacetime into spatial Cauchy hypersurfaces $\Sigma_t$ evolved
//! across discrete time intervals $\Delta t$:
//! - Spatial 3D triangulation $\Sigma_t$ with spatial edge lengths $\ell_a(t)$.
//! - 4D prismatoid slab $\Sigma_t \times [t, t+\Delta t]$ triangulated into 4-simplices.
//! - Time-struts connecting vertex $v \in \Sigma_t$ to $v' \in \Sigma_{t+\Delta t}$ with
//!   squared lengths $s_{\text{strut}}(v) = (N_v \Delta t)^2$, where $N_v$ is the lapse.
//! - Conjugate momentum $\pi_a$ to spatial squared edge length $s_a = \ell_a^2$:
//!   $$\pi_a = \frac{\partial S_{\text{slab}}}{\partial s_a(t+\Delta t)}$$
//!
//! AuthorityEffect: None.

use crate::cayley_menger::simplex_volume_cayley_menger;
use crate::regge_calculus::{EdgeLengthMetric, ReggeError};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; 3+1 ADM simplicial dynamics.";

/// Spatial Cauchy hypersurface $\Sigma_t$ at fixed discrete time t.
#[derive(Debug, Clone, PartialEq)]
pub struct SpatialSlice3D {
    /// Spatial tetrahedra: [v0, v1, v2, v3].
    pub tetrahedra: Vec<[usize; 4]>,
    /// Unique spatial edges: (u, v) with u < v.
    pub edges: Vec<(usize, usize)>,
    /// Metric lengths for all spatial edges.
    pub metric: EdgeLengthMetric,
    /// Time label / index.
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

        // Verify every spatial edge has a valid length
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

    /// Single regular tetrahedron spatial slice for testing and benchmark models.
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

    /// Compute total spatial 3-volume: ∑_τ V_3(τ).
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

/// A 4D sandwich slab connecting slice $\Sigma_t$ to $\Sigma_{t+\Delta t}$.
#[derive(Debug, Clone, PartialEq)]
pub struct SimplicialSlab4D {
    pub slice_t0: SpatialSlice3D,
    pub slice_t1: SpatialSlice3D,
    /// Lapse function N_v at each vertex v.
    pub lapse: BTreeMap<usize, f64>,
    /// Time increment Δt.
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

    /// Strut edge length connecting vertex v at time t0 to corresponding vertex v' at time t1:
    /// ℓ_strut(v) = N_v * Δt.
    pub fn strut_length(&self, v: usize) -> Result<f64, ReggeError> {
        let n = self.lapse.get(&v).copied().unwrap_or(1.0);
        if n <= 0.0 || !n.is_finite() {
            return Err(ReggeError::NonFinite);
        }
        Ok(n * self.delta_t)
    }

    /// Discrete conjugate momentum π_a conjugate to squared edge length s_a = ℓ_a²:
    /// In a discrete time step, π_a ≈ (s_a(t1) - s_a(t0)) / (2 * N_a * Δt),
    /// corresponding to the extrinsic curvature K_a on edge a.
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

            // Momentum: rate of change of metric divided by lapse
            let pi = (s1 - s0) / (2.0 * n_avg * self.delta_t);
            momenta.insert((u, v), pi);
        }
        Ok(momenta)
    }
}

/// Results of a 3+1 Cauchy evolution step.
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

        // s0 = 1.0, s1 = 1.21, ds = 0.21. pi = 0.21 / (2 * 1.0 * 0.1) = 1.05.
        for &pi in momenta.values() {
            assert!((pi - 1.05).abs() < 1e-6);
        }
    }
}
