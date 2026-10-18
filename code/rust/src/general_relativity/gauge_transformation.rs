//! Discrete gauge transformation group acting on simplicial connections.
//!
//! Origin: papers/derivations/general_relativity/rust/src/gauge_transformation.rs
//! Claim: DERIV-GR-GAUGE-001
//! AuthorityEffect: None.

use num_rational::Ratio;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum GaugeError {
    VertexNotFound(usize),
    NonGaugeInvariantObservable,
}

/// A discrete 0-cochain of gauge group parameters f: V -> Q.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiscreteGaugeTransformation {
    pub num_vertices: usize,
    pub vertex_phases: BTreeMap<usize, Ratio<i64>>,
}

impl DiscreteGaugeTransformation {
    pub fn new(num_vertices: usize) -> Self {
        Self {
            num_vertices,
            vertex_phases: BTreeMap::new(),
        }
    }

    pub fn set_vertex_phase(&mut self, v: usize, phase: Ratio<i64>) {
        self.vertex_phases.insert(v, phase);
    }

    pub fn get_phase(&self, v: usize) -> Ratio<i64> {
        self.vertex_phases.get(&v).copied().unwrap_or_else(Ratio::zero)
    }

    /// Transforms an edge connection: A_{uv} -> A_{uv} + f(v) - f(u).
    pub fn transform_edge(&self, u: usize, v: usize, old_phase: Ratio<i64>) -> Ratio<i64> {
        old_phase + self.get_phase(v) - self.get_phase(u)
    }

    /// Strictly verifies that cycle flux is invariant under the gauge transformation.
    pub fn verify_cycle_invariance(
        &self,
        cycle: &[(usize, usize)],
        edge_phases: &BTreeMap<(usize, usize), Ratio<i64>>,
    ) -> Result<bool, GaugeError> {
        let mut original_flux = Ratio::zero();
        let mut transformed_flux = Ratio::zero();

        for &(u, v) in cycle {
            let p = edge_phases.get(&(u, v)).copied().unwrap_or_else(Ratio::zero);
            original_flux += p;
            transformed_flux += self.transform_edge(u, v, p);
        }

        Ok(original_flux == transformed_flux)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn gauge_invariance_of_wilson_loop() {
        let mut gt = DiscreteGaugeTransformation::new(3);
        gt.set_vertex_phase(0, Ratio::new(3, 7));
        gt.set_vertex_phase(1, Ratio::new(-1, 2));
        gt.set_vertex_phase(2, Ratio::new(5, 3));

        let mut edges = BTreeMap::new();
        edges.insert((0, 1), Ratio::new(1, 4));
        edges.insert((1, 2), Ratio::new(1, 3));
        edges.insert((2, 0), Ratio::new(1, 2));

        let cycle = vec![(0, 1), (1, 2), (2, 0)];
        assert!(gt.verify_cycle_invariance(&cycle, &edges).unwrap());
    }
}
