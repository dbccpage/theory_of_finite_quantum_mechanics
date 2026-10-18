
use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ConnectionError {
    EdgeNotFound(String),
    NonUnitaryTransport,
    NonAbelianCurvatureDefect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiscreteConnection {
    pub num_vertices: usize,
    pub edge_phases: BTreeMap<(usize, usize), Ratio<i64>>,
}

impl DiscreteConnection {
    pub fn new(num_vertices: usize) -> Self {
        Self {
            num_vertices,
            edge_phases: BTreeMap::new(),
        }
    }

    pub fn set_edge(&mut self, u: usize, v: usize, phase: Ratio<i64>) {
        self.edge_phases.insert((u, v), phase);
        self.edge_phases.insert((v, u), -phase);
    }

    pub fn cycle_flux(&self, cycle: &[(usize, usize)]) -> Result<Ratio<i64>, ConnectionError> {
        let mut total_phase = Ratio::zero();
        for &(u, v) in cycle {
            let phase = self.edge_phases.get(&(u, v)).copied().ok_or_else(|| {
                ConnectionError::EdgeNotFound(format!("Edge ({u}, {v})"))
            })?;
            total_phase += phase;
        }
        Ok(total_phase)
    }

    pub fn verify_tetrahedron_bianchi(
        &self,
        faces: &[Vec<(usize, usize)>],
    ) -> Result<bool, ConnectionError> {
        let mut net_flux = Ratio::zero();
        for face in faces {
            net_flux += self.cycle_flux(face)?;
        }
        Ok(net_flux.is_zero())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn flat_connection_zero_flux() {
        let mut conn = DiscreteConnection::new(3);
        conn.set_edge(0, 1, Ratio::new(1, 4));
        conn.set_edge(1, 2, Ratio::new(1, 4));
        conn.set_edge(2, 0, Ratio::new(-1, 2));

        let cycle = vec![(0, 1), (1, 2), (2, 0)];
        let flux = conn.cycle_flux(&cycle).unwrap();
        assert_eq!(flux, Ratio::zero());
    }
}
