// Executable finite evidence; AuthorityEffect: None.
//! WDP presentation of LGGR-owned exact matrix path kernels.
//! Public fields, serialization, WdpError and AuthorityEffect remain available
//! here; multiplication, walk validation and diagnostic checks have one owner.
use num_rational::BigRational;
use omega_epk::matrix_path_kernel as native;
use serde::{Deserialize, Serialize};

use crate::error::WdpError;
use crate::types::AuthorityEffect;

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

/// Retained WDP receipt shape. Agreement refers only to supplied comparisons.
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
