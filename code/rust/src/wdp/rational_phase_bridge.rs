use crate::amplitude_bridge::{EdgePath, OrientedGraph, PathStep};
use crate::error::WdpError;
use omega_number_theory::rational::Rational;
use omega_number_theory::rational_turns::RationalTurn;

pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/rational_phase_bridge.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: rational edge turns add along an oriented path and transform by the endpoint gauge difference";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PhaseTokenError {
    Carrier(WdpError),
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
    Overflow,
}

impl From<WdpError> for PhaseTokenError {
    fn from(error: WdpError) -> Self {
        Self::Carrier(error)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RationalPhaseCochain {
    graph: OrientedGraph,
    phases: Vec<RationalTurn>,
}

pub fn admit_exact_integer(token: &str) -> Result<i64, PhaseTokenError> {
    if token == "true" || token == "false" {
        return Err(PhaseTokenError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(PhaseTokenError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, PhaseTokenError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(PhaseTokenError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(PhaseTokenError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(PhaseTokenError::Overflow)?;
    }
    Ok(value)
}

fn turn_from_numerator(numer: i64) -> Result<RationalTurn, PhaseTokenError> {
    if numer == i64::MIN {
        return Err(PhaseTokenError::Overflow);
    }
    Ok(RationalTurn::new(Rational::new(numer.into(), 2.into())))
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

    pub fn authority_effect(&self) -> &'static str {
        AUTHORITY_EFFECT
    }

    pub fn path_phase(&self, path: &EdgePath) -> Result<RationalTurn, WdpError> {
        self.graph.path_end(path)?;
        let mut sum = RationalTurn::zero();
        for step in &path.steps {
            let phase = self.phase_of(step.edge)?;
            sum = if step.forward {
                sum.add(phase)
            } else {
                sum.sub(phase)
            };
        }
        Ok(sum)
    }

    pub fn gauge_transform(&self, potential: &[RationalTurn]) -> Result<Self, WdpError> {
        if potential.len() != self.graph.vertices() {
            return Err(WdpError::InvalidInput {
                detail: "one rational gauge turn per vertex is required".into(),
            });
        }
        let mut phases = Vec::new();
        for (index, &(tail, head)) in self.graph.edges().iter().enumerate() {
            let phase = self.phase_of(index)?;
            phases.push(self.gauged_phase(phase, potential, tail, head)?);
        }
        Self::new(self.graph.clone(), phases)
    }

    pub fn verify_path_gauge_covariance(
        &self,
        path: &EdgePath,
        potential: &[RationalTurn],
    ) -> Result<bool, WdpError> {
        let transformed = self.gauge_transform(potential)?;
        let expected = self.endpoint_adjusted_phase(path, potential)?;
        Ok(transformed.path_phase(path)? == expected)
    }

    fn endpoint_adjusted_phase(
        &self,
        path: &EdgePath,
        potential: &[RationalTurn],
    ) -> Result<RationalTurn, WdpError> {
        let (start_turn, end_turn) = self.endpoint_turns(path, potential)?;
        Ok(self.path_phase(path)?.add(end_turn).sub(start_turn))
    }

    fn endpoint_turns<'a>(
        &self,
        path: &EdgePath,
        potential: &'a [RationalTurn],
    ) -> Result<(&'a RationalTurn, &'a RationalTurn), WdpError> {
        let end = self.graph.path_end(path)?;
        let start_turn = gauge_turn(potential, path.start, "start")?;
        let end_turn = gauge_turn(potential, end, "end")?;
        Ok((start_turn, end_turn))
    }

    fn phase_of(&self, edge: usize) -> Result<&RationalTurn, WdpError> {
        self.phases.get(edge).ok_or_else(|| WdpError::InvalidInput {
            detail: format!("edge {edge} has no rational turn"),
        })
    }

    fn gauged_phase(
        &self,
        phase: &RationalTurn,
        potential: &[RationalTurn],
        tail: usize,
        head: usize,
    ) -> Result<RationalTurn, WdpError> {
        let at_tail = potential.get(tail).ok_or_else(|| WdpError::InvalidInput {
            detail: format!("gauge potential misses tail {tail}"),
        })?;
        let at_head = potential.get(head).ok_or_else(|| WdpError::InvalidInput {
            detail: format!("gauge potential misses head {head}"),
        })?;
        Ok(phase.add(at_head).sub(at_tail))
    }
}

fn gauge_turn<'a>(
    potential: &'a [RationalTurn],
    index: usize,
    role: &str,
) -> Result<&'a RationalTurn, WdpError> {
    potential.get(index).ok_or_else(|| WdpError::InvalidInput {
        detail: format!("gauge potential misses {role} {index}"),
    })
}

pub fn edge_cochain(numer: i64) -> Result<RationalPhaseCochain, PhaseTokenError> {
    let graph = OrientedGraph::new(2, vec![(0, 1)])?;
    Ok(RationalPhaseCochain::new(graph, vec![turn_from_numerator(numer)?])?)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn forward() -> EdgePath {
        EdgePath {
            start: 0,
            steps: vec![PathStep {
                edge: 0,
                forward: true,
            }],
        }
    }

    fn show(error: impl std::fmt::Debug) -> String {
        format!("{error:?}")
    }

    #[test]
    fn unit_forward_path_keeps_the_edge_turn() -> Result<(), String> {
        unit_phase().and_then(|(cochain, phase, expected)| unit_claims(cochain, phase, expected))
    }

    fn unit_phase() -> Result<(RationalPhaseCochain, RationalTurn, RationalTurn), String> {
        let cochain = edge_cochain(1).map_err(show)?;
        let phase = cochain.path_phase(&forward()).map_err(show)?;
        let expected = turn_from_numerator(1).map_err(show)?;
        Ok((cochain, phase, expected))
    }

    fn unit_claims(
        cochain: RationalPhaseCochain,
        phase: RationalTurn,
        expected: RationalTurn,
    ) -> Result<(), String> {
        need(phase == expected, "phase")?;
        need(cochain.authority_effect() == AUTHORITY_EFFECT, "authority")
    }

    #[test]
    fn integration_reverse_path_is_the_inverse_turn() -> Result<(), String> {
        let cochain = edge_cochain(1).map_err(|error| format!("{error:?}"))?;
        let inverse = EdgePath {
            start: 1,
            steps: vec![PathStep {
                edge: 0,
                forward: false,
            }],
        };
        let phase = cochain
            .path_phase(&inverse)
            .map_err(|error| format!("{error:?}"))?;
        let expected = RationalTurn::zero().sub(&turn_from_numerator(1).map_err(|error| format!("{error:?}"))?);
        need(phase == expected, "inverse")?;
        Ok(())
    }

    #[test]
    fn e2e_gauge_covariance_adds_the_endpoint_difference() -> Result<(), String> {
        e2e_covariance().and_then(e2e_claims)
    }

    fn e2e_covariance() -> Result<bool, String> {
        let cochain = edge_cochain(1).map_err(show)?;
        let turn = turn_from_numerator(1).map_err(show)?;
        let potential = vec![RationalTurn::zero(), turn];
        cochain
            .verify_path_gauge_covariance(&forward(), &potential)
            .map_err(show)
    }

    fn e2e_claims(covariant: bool) -> Result<(), String> {
        need(covariant, "covariance")?;
        need(ORIGIN.contains("rational_phase_bridge.rs"), "origin")?;
        need(CLAIM.contains("endpoint gauge"), "claim")
    }

    #[test]
    fn negative_refuses_phase_count_gauge_length_broken_path_and_float() -> Result<(), String> {
        let graph = OrientedGraph::new(2, vec![(0, 1)]).map_err(|error| format!("{error:?}"))?;
        need(
            matches!(RationalPhaseCochain::new(graph, vec![]), Err(WdpError::InvalidInput { .. })),
            "count",
        )?;
        let cochain = edge_cochain(1).map_err(|error| format!("{error:?}"))?;
        need(
            matches!(
                cochain.gauge_transform(&[]),
                Err(WdpError::InvalidInput { .. })
            ),
            "gauge",
        )?;
        let broken = EdgePath {
            start: 1,
            steps: vec![PathStep {
                edge: 0,
                forward: true,
            }],
        };
        need(cochain.path_phase(&broken).is_err(), "path")?;
        need(
            admit_exact_integer("1.5") == Err(PhaseTokenError::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_integer("true") == Err(PhaseTokenError::BooleanAsNumber),
            "bool",
        )?;
        Ok(())
    }
}
