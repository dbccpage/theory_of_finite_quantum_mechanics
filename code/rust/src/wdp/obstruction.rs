
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

use crate::cochains::FiniteComplex;
use crate::error::WdpError;
use omega_solvers::solver_lp_exact_simplex::solve_weighted_l1_projection;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Cochain0 {
    pub values: BTreeMap<String, BigRational>,
}

impl Cochain0 {
    pub fn get(&self, vertex: &str) -> Result<BigRational, WdpError> {
        self.values
            .get(vertex)
            .cloned()
            .ok_or_else(|| WdpError::InvalidInput {
                detail: format!("Vertex {} not found in cochain", vertex),
            })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Cochain1 {
    pub values: BTreeMap<(String, String), BigRational>,
}

impl Cochain1 {
    pub fn l1_norm(&self) -> BigRational {
        omega_functional::Phi1Functional::unweighted_l1_rational(
            &self.values.values().cloned().collect::<Vec<_>>(),
        )
        .expect("exact cochain entries")
    }
}

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
    #[error("Missing element: {0}")]
    MissingElement(String),
    #[error(transparent)]
    Functional(#[from] omega_functional::phi1::ExactPhi1CertificateError),
}

impl DualWitnessCertificate {
    pub fn verify(
        &self,
        complex: &FiniteComplex,
        h: &Cochain1,
        weights: Option<&BTreeMap<(String, String), BigRational>>,
    ) -> Result<(), CertificateVerificationError> {
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
    let k = complex.vertices.len();
    let m = complex.edges.len();
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

    let v_list: Vec<String> = complex.vertices.iter().cloned().collect();
    let v_idx: BTreeMap<String, usize> = v_list
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
    for (i, v_name) in v_list.iter().enumerate() {
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

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::BTreeSet;

    fn triangle_complex() -> FiniteComplex {
        let vertices = BTreeSet::from(["v0".to_string(), "v1".to_string(), "v2".to_string()]);
        let edges = vec![
            ("v0".to_string(), "v1".to_string()),
            ("v1".to_string(), "v2".to_string()),
            ("v0".to_string(), "v2".to_string()),
        ];
        FiniteComplex::new(vertices, edges, vec![]).unwrap()
    }

    #[test]
    fn test_exact_cochain_zero_dual() {
        let complex = triangle_complex();
        let mut h_vals = BTreeMap::new();
        h_vals.insert(
            ("v0".into(), "v1".into()),
            BigRational::from_integer(1.into()),
        );
        h_vals.insert(
            ("v1".into(), "v2".into()),
            BigRational::from_integer(2.into()),
        );
        h_vals.insert(
            ("v0".into(), "v2".into()),
            BigRational::from_integer(3.into()),
        );
        let h = Cochain1 { values: h_vals };

        let cert = solve_exact_potential(&complex, &h).expect("solve exact");
        assert!(cert.is_exact);
        assert_eq!(cert.phi1_value, BigRational::zero());
        for (_, r) in &cert.residual_c1.values {
            assert_eq!(r, &BigRational::zero());
        }
        cert.verify(&complex, &h, None)
            .expect("verification passes");
    }

    #[test]
    fn test_obstructed_cycle_dual_annihilation() {
        let vertices = BTreeSet::from(["v0".to_string(), "v1".to_string(), "v2".to_string()]);
        let edges = vec![
            ("v0".to_string(), "v1".to_string()),
            ("v1".to_string(), "v2".to_string()),
            ("v2".to_string(), "v0".to_string()),
        ];
        let complex = FiniteComplex::new(vertices, edges, vec![]).unwrap();

        let mut h_vals = BTreeMap::new();
        h_vals.insert(("v0".into(), "v1".into()), BigRational::one());
        h_vals.insert(("v1".into(), "v2".into()), BigRational::one());
        h_vals.insert(("v2".into(), "v0".into()), BigRational::one());
        let h = Cochain1 { values: h_vals };

        let cert = solve_exact_potential(&complex, &h).expect("solve obstructed");
        assert!(!cert.is_exact);
        assert_eq!(cert.phi1_value, BigRational::from_integer(3.into()));

        for (_, y) in &cert.dual_witness_c1.values {
            assert!(y.abs() <= BigRational::one());
        }
        let y01 = cert
            .dual_witness_c1
            .values
            .get(&("v0".into(), "v1".into()))
            .unwrap();
        let y12 = cert
            .dual_witness_c1
            .values
            .get(&("v1".into(), "v2".into()))
            .unwrap();
        let y20 = cert
            .dual_witness_c1
            .values
            .get(&("v2".into(), "v0".into()))
            .unwrap();
        assert_eq!(y01, y12);
        assert_eq!(y12, y20);
        assert_eq!(y01, &BigRational::one());

        cert.verify(&complex, &h, None)
            .expect("verification passes");
    }

    #[test]
    fn test_weighted_chord_optimal_simplex() {
        let vertices = BTreeSet::from(["v0".to_string(), "v1".to_string(), "v2".to_string()]);
        let edges = vec![
            ("v0".to_string(), "v1".to_string()),
            ("v1".to_string(), "v2".to_string()),
            ("v0".to_string(), "v2".to_string()),
        ];
        let complex = FiniteComplex::new(vertices, edges, vec![]).unwrap();

        let mut h_vals = BTreeMap::new();
        h_vals.insert(("v0".into(), "v1".into()), BigRational::one());
        h_vals.insert(("v1".into(), "v2".into()), BigRational::one());
        h_vals.insert(("v0".into(), "v2".into()), BigRational::zero());
        let h = Cochain1 { values: h_vals };

        let mut weights = BTreeMap::new();
        weights.insert(("v0".into(), "v1".into()), BigRational::one());
        weights.insert(("v1".into(), "v2".into()), BigRational::one());
        weights.insert(
            ("v0".into(), "v2".into()),
            BigRational::from_integer(10.into()),
        );

        let cert =
            solve_exact_potential_weighted(&complex, &h, Some(&weights)).expect("solve weighted");

        assert_eq!(cert.phi1_value, BigRational::from_integer(2.into()));
        cert.verify(&complex, &h, Some(&weights))
            .expect("passes 5-point verification");
    }
}
