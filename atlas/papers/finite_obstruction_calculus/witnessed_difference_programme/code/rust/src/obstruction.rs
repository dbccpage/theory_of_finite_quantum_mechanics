// Executable finite evidence; AuthorityEffect: None.
//! Exact 1-cochain obstruction and simplicial L1 quotient solver via Sparse Revised Simplex.

use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

use crate::cochains::{Cochain0, Cochain1, FiniteComplex};
use crate::error::WdpError;
use omega_solvers::solver_lp_exact_simplex::solve_weighted_l1_projection;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DualWitnessCertificate {
    pub phi1_value: BigRational,
    pub potential_c0: Cochain0,
    pub residual_c1: Cochain1,
    pub dual_witness_c1: Cochain1,
    pub is_exact: bool,
    pub authority_effect: String,
}

#[derive(Debug, Clone, thiserror::Error, PartialEq, Eq)]
pub enum CertificateVerificationError {
    #[error("Invalid certificate or input: {0}")]
    InvalidInput(String),
    #[error("Missing element: {0}")]
    MissingElement(String),
    #[error(transparent)]
    Functional(#[from] omega_functional::phi1::ExactPhi1CertificateError),
}

fn validate_input(
    complex: &FiniteComplex,
    h: &Cochain1,
    weights: Option<&BTreeMap<(String, String), BigRational>>,
) -> Result<(), CertificateVerificationError> {
    FiniteComplex::new(complex.vertices.clone(), complex.edges.clone())
        .map_err(|e| CertificateVerificationError::InvalidInput(e.to_string()))?;
    let edges: BTreeSet<_> = complex.edges.iter().collect();
    if h.values.keys().collect::<BTreeSet<_>>() != edges {
        return Err(CertificateVerificationError::InvalidInput("cochain must contain every declared edge exactly once".into()));
    }
    if weights.is_some_and(|w| w.keys().collect::<BTreeSet<_>>() != edges) {
        return Err(CertificateVerificationError::InvalidInput("weights must contain every declared edge exactly once".into()));
    }
    Ok(())
}

impl DualWitnessCertificate {
    pub fn verify(
        &self,
        complex: &FiniteComplex,
        h: &Cochain1,
        weights: Option<&BTreeMap<(String, String), BigRational>>,
    ) -> Result<(), CertificateVerificationError> {
        validate_input(complex, h, weights)?;
        let edges: BTreeSet<_> = complex.edges.iter().collect();
        let vertices_set: BTreeSet<_> = complex.vertices.iter().collect();
        if self.potential_c0.values.keys().collect::<BTreeSet<_>>() != vertices_set
            || self.residual_c1.values.keys().collect::<BTreeSet<_>>() != edges
            || self.dual_witness_c1.values.keys().collect::<BTreeSet<_>>() != edges {
            return Err(CertificateVerificationError::InvalidInput("certificate coordinate sets do not match the complex".into()));
        }
        if self.authority_effect != "None" || self.is_exact != self.phi1_value.is_zero() {
            return Err(CertificateVerificationError::InvalidInput("invalid authority effect or exactness flag".into()));
        }
        let vertices: BTreeMap<_, _> = complex
            .vertices
            .iter()
            .enumerate()
            .map(|(i, vertex)| (vertex.clone(), i))
            .collect();
        let alpha = complex
            .vertices
            .iter()
            .map(|vertex| {
                self.potential_c0
                    .get(vertex)
                    .map_err(|_| CertificateVerificationError::MissingElement(vertex.clone()))
            })
            .collect::<Result<Vec<_>, _>>()?;
        let mut d0 = Vec::with_capacity(complex.edges.len());
        let mut omega = Vec::with_capacity(complex.edges.len());
        let mut primal_residual = Vec::with_capacity(complex.edges.len());
        let mut dual_witness = Vec::with_capacity(complex.edges.len());
        let mut declared_weights = Vec::with_capacity(complex.edges.len());
        for (u, v) in &complex.edges {
            let from = *vertices
                .get(u)
                .ok_or_else(|| CertificateVerificationError::MissingElement(u.clone()))?;
            let to = *vertices
                .get(v)
                .ok_or_else(|| CertificateVerificationError::MissingElement(v.clone()))?;
            let mut row = vec![BigRational::zero(); vertices.len()];
            if from != to {
                row[from] = -BigRational::one();
                row[to] = BigRational::one();
            }
            let edge = (u.clone(), v.clone());
            d0.push(row);
            omega.push(
                h.values
                    .get(&edge)
                    .cloned()
                    .unwrap_or_else(BigRational::zero),
            );
            primal_residual.push(
                self.residual_c1
                    .values
                    .get(&edge)
                    .cloned()
                    .unwrap_or_else(BigRational::zero),
            );
            dual_witness.push(
                self.dual_witness_c1
                    .values
                    .get(&edge)
                    .cloned()
                    .unwrap_or_else(BigRational::zero),
            );
            declared_weights.push(
                weights
                    .and_then(|w| w.get(&edge))
                    .cloned()
                    .unwrap_or_else(BigRational::one),
            );
        }
        omega_functional::phi1::Phi1Functional::verify_exact_certificate(
            omega_functional::phi1::ExactPhi1Certificate {
                omega,
                d0,
                weights: declared_weights,
                alpha,
                primal_residual,
                dual_witness,
                reported_value: self.phi1_value.clone(),
            },
        )?;
        Ok(())
    }
}

pub fn solve_exact_potential_weighted(
    complex: &FiniteComplex,
    h: &Cochain1,
    edge_weights: Option<&BTreeMap<(String, String), BigRational>>,
) -> Result<DualWitnessCertificate, WdpError> {
    validate_input(complex, h, edge_weights).map_err(|e| WdpError::InvalidInput { detail: e.to_string() })?;
    let k = complex.num_vertices();
    let m = complex.num_edges();
    if k == 0 {
        return Err(WdpError::InvalidInput {
            detail: "Empty complex".into(),
        });
    }

    if m == 0 {
        let potential_c0 = Cochain0 {
            values: complex
                .vertices
                .iter()
                .map(|v| (v.clone(), BigRational::zero()))
                .collect(),
        };
        let cert = DualWitnessCertificate {
            phi1_value: BigRational::zero(),
            potential_c0,
            residual_c1: Cochain1 {
                values: BTreeMap::new(),
            },
            dual_witness_c1: Cochain1 {
                values: BTreeMap::new(),
            },
            is_exact: true,
            authority_effect: "None".to_string(),
        };
        cert.verify(complex, h, edge_weights)
            .map_err(|e| WdpError::InvalidInput {
                detail: format!("Emitted certificate failed self-verification: {e}"),
            })?;
        return Ok(cert);
    }

    let v_idx: BTreeMap<String, usize> = complex
        .vertices
        .iter()
        .enumerate()
        .map(|(i, v)| (v.clone(), i))
        .collect();

    let mut map_rows: Vec<Vec<BigRational>> = Vec::with_capacity(m);
    let mut target: Vec<BigRational> = Vec::with_capacity(m);
    let mut weights: Vec<BigRational> = Vec::with_capacity(m);

    let one = BigRational::one();
    let zero = BigRational::zero();

    for (u, v) in &complex.edges {
        let edge = (u.clone(), v.clone());
        let mut row = vec![zero.clone(); k];
        if u != v {
            let idx_u = *v_idx.get(u).ok_or_else(|| WdpError::InvalidInput {
                detail: format!("unknown vertex {u}"),
            })?;
            let idx_v = *v_idx.get(v).ok_or_else(|| WdpError::InvalidInput {
                detail: format!("unknown vertex {v}"),
            })?;
            row[idx_u] = -one.clone();
            row[idx_v] = one.clone();
        }
        map_rows.push(row);

        let h_val = h.values.get(&edge).cloned().unwrap_or_else(|| zero.clone());
        target.push(h_val);

        let w_val = edge_weights
            .and_then(|w| w.get(&edge))
            .cloned()
            .unwrap_or_else(|| one.clone());
        if !w_val.is_positive() {
            return Err(WdpError::InvalidInput {
                detail: format!("non-positive weight on edge ({u}, {v})"),
            });
        }
        weights.push(w_val);
    }

    let budget = 64 * (m + k) + 1024;
    let solution =
        solve_weighted_l1_projection(&target, &weights, &map_rows, budget).map_err(|e| {
            WdpError::InvalidInput {
                detail: format!("Simplex solver failure: {e}"),
            }
        })?;

    let mut pot_map = BTreeMap::new();
    for (i, v_name) in complex.vertices.iter().enumerate() {
        pot_map.insert(v_name.clone(), solution.coefficients[i].clone());
    }
    let potential_c0 = Cochain0 { values: pot_map };

    let mut res_map = BTreeMap::new();
    for (i, edge) in complex.edges.iter().enumerate() {
        res_map.insert(
            (edge.0.clone(), edge.1.clone()),
            solution.residual[i].clone(),
        );
    }
    let residual_c1 = Cochain1 { values: res_map };

    let mut dual_map = BTreeMap::new();
    for (i, edge) in complex.edges.iter().enumerate() {
        dual_map.insert((edge.0.clone(), edge.1.clone()), solution.dual[i].clone());
    }
    let dual_witness_c1 = Cochain1 { values: dual_map };

    let is_exact = solution.value.is_zero();

    let cert = DualWitnessCertificate {
        phi1_value: solution.value,
        potential_c0,
        residual_c1,
        dual_witness_c1,
        is_exact,
        authority_effect: "None".to_string(),
    };

    cert.verify(complex, h, edge_weights)
        .map_err(|e| WdpError::InvalidInput {
            detail: format!("Emitted certificate failed self-verification: {e}"),
        })?;

    Ok(cert)
}

pub fn solve_exact_potential(
    complex: &FiniteComplex,
    h: &Cochain1,
) -> Result<DualWitnessCertificate, WdpError> {
    solve_exact_potential_weighted(complex, h, None)
}
