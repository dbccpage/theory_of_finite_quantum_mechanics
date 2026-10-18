use num_rational::BigRational;
use num_traits::Zero;
use omega_epk::matrix_path_kernel as native;
use serde::{Deserialize, Serialize};

use crate::error::WdpError;
use crate::types::AuthorityEffect;

pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/path_kernel_gluing.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: two identical rational patches on one declared overlap have Cech L1 defect zero, and an edge index outside the declared graph is refused";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GluingTokenError {
    Carrier(WdpError),
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
    Overflow,
}

pub fn admit_exact_integer(token: &str) -> Result<i64, GluingTokenError> {
    if token == "true" || token == "false" {
        return Err(GluingTokenError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(GluingTokenError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, GluingTokenError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(GluingTokenError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(GluingTokenError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(GluingTokenError::Overflow)?;
    }
    Ok(value)
}

pub fn identical_patch_defect_vanishes(
    graph: &EvaluatedPathKernelGraph,
    patch: &RationalMatrix2x2,
) -> Result<bool, WdpError> {
    let (defect, vanishes) =
        graph.compute_cech_gluing_defect(&[patch.clone(), patch.clone()], &[(0, 1)])?;
    Ok(vanishes && defect == BigRational::zero())
}

pub use native::EvaluationColor;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RationalMatrix2x2 {
    pub m00: BigRational,
    pub m01: BigRational,
    pub m10: BigRational,
    pub m11: BigRational,
}
impl From<native::RationalMatrix2x2> for RationalMatrix2x2 {
    fn from(value: native::RationalMatrix2x2) -> Self {
        Self {
            m00: value.m00,
            m01: value.m01,
            m10: value.m10,
            m11: value.m11,
        }
    }
}
impl RationalMatrix2x2 {
    fn native(&self) -> native::RationalMatrix2x2 {
        native::RationalMatrix2x2::new(
            self.m00.clone(),
            self.m01.clone(),
            self.m10.clone(),
            self.m11.clone(),
        )
    }
    pub fn identity() -> Self {
        native::RationalMatrix2x2::identity().into()
    }
    pub fn new(m00: BigRational, m01: BigRational, m10: BigRational, m11: BigRational) -> Self {
        native::RationalMatrix2x2::new(m00, m01, m10, m11).into()
    }
    pub fn multiply(&self, other: &Self) -> Result<Self, WdpError> {
        Ok(self.native().multiply(&other.native())?.into())
    }
    pub fn determinant(&self) -> Result<BigRational, WdpError> {
        Ok(self.native().determinant()?)
    }
    pub fn l1_norm(&self) -> Result<BigRational, WdpError> {
        Ok(self.native().l1_norm()?)
    }
    pub fn deviation_from_identity(&self) -> Result<BigRational, WdpError> {
        Ok(self.native().deviation_from_identity()?)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LggrEvaluationReceipt {
    pub is_local_green: bool,
    pub is_global_green: bool,
    pub lggr_anomaly_detected: bool,
    pub cycle_path: Vec<String>,
    pub path_kernel_product: RationalMatrix2x2,
    pub cech_gluing_defect: BigRational,
    pub declared_overlap_residual_vanishes: bool,
    #[serde(rename = "gtla_trace_contractive")]
    pub coda_gtla_trace_contractive: bool,
    #[serde(rename = "gtla_steps_count")]
    pub coda_gtla_steps_count: usize,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EvaluatedPathKernelGraph {
    pub vertices: Vec<String>,
    pub edges: Vec<(String, String)>,
    pub transition_matrices: Vec<RationalMatrix2x2>,
    pub authority_effect: AuthorityEffect,
}
impl From<native::EvaluatedPathKernelGraph> for EvaluatedPathKernelGraph {
    fn from(value: native::EvaluatedPathKernelGraph) -> Self {
        Self {
            vertices: value.vertices,
            edges: value.edges,
            transition_matrices: value
                .transition_matrices
                .into_iter()
                .map(Into::into)
                .collect(),
            authority_effect: AuthorityEffect::None,
        }
    }
}
impl EvaluatedPathKernelGraph {
    fn native(&self) -> native::EvaluatedPathKernelGraph {
        native::EvaluatedPathKernelGraph {
            vertices: self.vertices.clone(),
            edges: self.edges.clone(),
            transition_matrices: self
                .transition_matrices
                .iter()
                .map(RationalMatrix2x2::native)
                .collect(),
        }
    }
    pub fn new(
        vertices: Vec<String>,
        edges: Vec<(String, String)>,
        transitions: Vec<RationalMatrix2x2>,
    ) -> Result<Self, WdpError> {
        Ok(native::EvaluatedPathKernelGraph::new(
            vertices,
            edges,
            transitions.iter().map(RationalMatrix2x2::native).collect(),
        )?
        .into())
    }
    pub fn evaluate_path(&self, edge_indices: &[usize]) -> Result<RationalMatrix2x2, WdpError> {
        Ok(self.native().evaluate_path(edge_indices)?.into())
    }
    pub fn check_local_green(
        &self,
        edge_threshold: BigRational,
    ) -> Result<(bool, Vec<EvaluationColor>), WdpError> {
        Ok(self.native().check_local_green(edge_threshold)?)
    }
    pub fn check_global_cycle(
        &self,
        cycle_edges: &[usize],
        cycle_threshold: BigRational,
    ) -> Result<(bool, RationalMatrix2x2), WdpError> {
        let (green, product) = self
            .native()
            .check_global_cycle(cycle_edges, cycle_threshold)?;
        Ok((green, product.into()))
    }
    pub fn compute_cech_gluing_defect(
        &self,
        patch_evaluations: &[RationalMatrix2x2],
        overlaps: &[(usize, usize)],
    ) -> Result<(BigRational, bool), WdpError> {
        let patches: Vec<_> = patch_evaluations
            .iter()
            .map(RationalMatrix2x2::native)
            .collect();
        Ok(self
            .native()
            .compute_cech_gluing_defect(&patches, overlaps)?)
    }
    pub fn verify_coda_gtla_trace(&self, residual_sequence: &[BigRational]) -> bool {
        self.native().verify_coda_gtla_trace(residual_sequence)
    }
}

pub fn generate_canonical_lggr_counterexample() -> (EvaluatedPathKernelGraph, Vec<usize>) {
    let (graph, cycle) = native::generate_canonical_lggr_counterexample();
    (graph.into(), cycle)
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_traits::One;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn show(error: impl std::fmt::Debug) -> String {
        format!("{error:?}")
    }

    fn edge_graph() -> Result<EvaluatedPathKernelGraph, String> {
        EvaluatedPathKernelGraph::new(
            vec!["a".to_string(), "b".to_string()],
            vec![("a".to_string(), "b".to_string())],
            vec![RationalMatrix2x2::identity()],
        )
        .map_err(show)
    }

    #[test]
    fn unit_identical_patches_have_zero_cech_defect() -> Result<(), String> {
        edge_graph().and_then(unit_defect)
    }

    fn unit_defect(graph: EvaluatedPathKernelGraph) -> Result<(), String> {
        let patch = RationalMatrix2x2::identity();
        let vanishes = identical_patch_defect_vanishes(&graph, &patch).map_err(show)?;
        let determinant = patch.determinant().map_err(show)?;
        need(vanishes && determinant == BigRational::one(), "defect")
    }

    #[test]
    fn integration_identity_path_stays_identity() -> Result<(), String> {
        let graph = edge_graph()?;
        let product = graph.evaluate_path(&[0]).map_err(show)?;
        need(product == RationalMatrix2x2::identity(), "path")?;
        need(graph.authority_effect == AuthorityEffect::None, "authority")
    }

    #[test]
    fn e2e_claim_and_authority_are_sealed() -> Result<(), String> {
        edge_graph().and_then(e2e_defect).and_then(|_| e2e_text())
    }

    fn e2e_defect(graph: EvaluatedPathKernelGraph) -> Result<(), String> {
        let vanishes =
            identical_patch_defect_vanishes(&graph, &RationalMatrix2x2::identity()).map_err(show)?;
        need(vanishes, "sealed")
    }

    fn e2e_text() -> Result<(), String> {
        need(ORIGIN.contains("path_kernel_gluing.rs"), "origin")?;
        need(CLAIM.contains("Cech L1 defect zero"), "claim")?;
        need(AUTHORITY_EFFECT.ends_with("None"), "text")
    }

    #[test]
    fn negative_refuses_length_mismatch_outside_index_float_and_boolean() -> Result<(), String> {
        negative_graph().and_then(|_| negative_tokens())
    }

    fn negative_graph() -> Result<(), String> {
        let mismatch = EvaluatedPathKernelGraph::new(
            vec!["a".to_string(), "b".to_string()],
            vec![("a".to_string(), "b".to_string())],
            vec![],
        );
        need(mismatch.is_err(), "length")?;
        let graph = edge_graph()?;
        need(graph.evaluate_path(&[1]).is_err(), "index")
    }

    fn negative_tokens() -> Result<(), String> {
        need(
            admit_exact_integer("1.5") == Err(GluingTokenError::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_integer("true") == Err(GluingTokenError::BooleanAsNumber),
            "bool",
        )
    }
}
