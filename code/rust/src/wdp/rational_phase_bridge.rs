//! Declared rational-turn transport and operational-readout boundaries.
//! AuthorityEffect: None. Symbolic phases live in Q/Z; actual scalar evaluation
//! is a checked cyclotomic-owner operation. This is not the infinite-order
//! Gaussian anchor's missing rational exponentiation, nor a real exponent map.
use crate::amplitude_bridge::{EdgePath, OrientedGraph};
use crate::error::WdpError;
use omega_number_theory::rational_turns::RationalTurn;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RationalPhaseCochain {
    graph: OrientedGraph,
    phases: Vec<RationalTurn>,
}
impl RationalPhaseCochain {
    pub fn new(graph: OrientedGraph, phases: Vec<RationalTurn>) -> Result<Self, WdpError> {
        if phases.len() != graph.edges().len() {
            return Err(WdpError::InvalidInput {
                detail: "one rational turn per oriented edge is required".into(),
            });
        }
        Ok(Self { graph, phases })
    }
    pub fn graph(&self) -> &OrientedGraph {
        &self.graph
    }
    pub fn phases(&self) -> &[RationalTurn] {
        &self.phases
    }
    pub fn path_phase(&self, path: &EdgePath) -> Result<RationalTurn, WdpError> {
        self.graph.path_end(path)?;
        Ok(path.steps.iter().fold(RationalTurn::zero(), |sum, step| {
            let phase = &self.phases[step.edge];
            if step.forward {
                sum.add(phase)
            } else {
                sum.sub(phase)
            }
        }))
    }
    /// a'_uv=a_uv+f_v-f_u. On any validated path s→t the added phases
    /// telescope to f_t-f_s; every closed holonomy is therefore unchanged.
    pub fn gauge_transform(&self, potential: &[RationalTurn]) -> Result<Self, WdpError> {
        if potential.len() != self.graph.vertices() {
            return Err(WdpError::InvalidInput {
                detail: "one rational gauge turn per vertex is required".into(),
            });
        }
        let phases = self
            .graph
            .edges()
            .iter()
            .zip(&self.phases)
            .map(|(&(u, v), a)| a.add(&potential[v]).sub(&potential[u]))
            .collect();
        Self::new(self.graph.clone(), phases)
    }
    /// Compute both sides from the actual transformed cochain/path; this is not
    /// a caller-asserted invariant. False would indicate a broken implementation.
    pub fn verify_path_gauge_covariance(
        &self,
        path: &EdgePath,
        potential: &[RationalTurn],
    ) -> Result<bool, WdpError> {
        let transformed = self.gauge_transform(potential)?;
        let end = self.graph.path_end(path)?;
        let expected = self
            .path_phase(path)?
            .add(&potential[end])
            .sub(&potential[path.start]);
        Ok(transformed.path_phase(path)? == expected)
    }
}
