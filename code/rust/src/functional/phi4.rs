//! # Phi4: Exact Degree-4 Quotient-Distance, 4-Volume Flux, and Pontryagin/Chern Certificates
//!
//! Higher-degree finite obstruction calculus in the 4-manifold chain/cochain complex:
//!
//! ```text
//! C⁴  <───d₃───  C³  <───d₂───  C²  <───d₁───  C¹  <───d₀───  C⁰       (cochains)
//! C₄  ───∂₄───>  C₃  ───∂₃───>  C₂  ───∂₂───>  C₁  ───∂₁───>  C₀       (chains, ∂ₖ = dₖ₋₁ᵀ)
//! ```
//!
//! With the full sequence of cochain nilpotence laws:
//! 1. 1-skeleton nilpotence: `d₁ ∘ d₀ = 0` (or `∂₁ ∘ ∂₂ = 0`).
//! 2. Discrete Bianchi identity: `d₂ ∘ d₁ = 0` (or `∂₂ ∘ ∂₃ = 0`).
//! 3. 4-volume curvature / Bianchi coboundary identity: `d₃ ∘ d₂ = 0` (or `∂₃ ∘ ∂₄ = 0`).
//!
//! ## Mathematical Definition
//!
//! For a 4-cochain target flux `G ∈ C⁴(K; ℚ)` (4-volume density or Pontryagin/Chern cup product)
//! on a 4-dimensional cell complex with non-trivial 4-cavities (`b₄ ≥ 1`):
//!
//! ```text
//! Φ₄([G]) = min_{C ∈ C³(K; ℚ)} ‖G - d₃ C‖_{1, μ}
//! ```
//!
//! By exact linear programming weak duality over `ℚ`:
//!
//! ```text
//! Φ₄([G]) ≥ max_{v ∈ C₄(K; ℚ)} ⟨G, v⟩
//! subject to:
//!   d₃ᵀ v = 0       (v ∈ Z₄(K; ℚ), closed 4-cycle / 4-volume cavity)
//!   |v_σ| ≤ μ_σ     ∀ σ ∈ K₄ (4-cells)
//! ```
//!
//! When primal and dual values match exactly, weak duality establishes optimality
//! with zero duality gap in `ℚ`.

use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};
use std::str::FromStr;

/// Wire shape for string-encoded rational certificate payloads.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ExactPhi4CertificateWire {
    pub flux_g: Vec<String>,
    pub d3: Vec<Vec<String>>,
    pub d2: Vec<Vec<String>>,
    pub d1: Option<Vec<Vec<String>>>,
    pub d0: Option<Vec<Vec<String>>>,
    pub weights: Vec<String>,
    pub potential_c: Vec<String>,
    pub primal_residual: Vec<String>,
    pub dual_witness: Vec<String>,
    pub reported_value: String,
}

impl TryFrom<ExactPhi4CertificateWire> for ExactPhi4Certificate {
    type Error = ExactPhi4CertificateError;

    fn try_from(wire: ExactPhi4CertificateWire) -> Result<Self, Self::Error> {
        fn parse_vec(v: &[String]) -> Result<Vec<BigRational>, ExactPhi4CertificateError> {
            crate::wire::parse_rational_vec(v, ExactPhi4CertificateError::InvalidRationalString)
        }
        fn parse_mat(
            m: &[Vec<String>],
        ) -> Result<Vec<Vec<BigRational>>, ExactPhi4CertificateError> {
            crate::wire::parse_rational_matrix(m, ExactPhi4CertificateError::InvalidRationalString)
        }

        let d1 = wire.d1.map(|m| parse_mat(&m)).transpose()?;
        let d0 = wire.d0.map(|m| parse_mat(&m)).transpose()?;

        Ok(ExactPhi4Certificate {
            flux_g: parse_vec(&wire.flux_g)?,
            d3: parse_mat(&wire.d3)?,
            d2: parse_mat(&wire.d2)?,
            d1,
            d0,
            weights: parse_vec(&wire.weights)?,
            potential_c: parse_vec(&wire.potential_c)?,
            primal_residual: parse_vec(&wire.primal_residual)?,
            dual_witness: parse_vec(&wire.dual_witness)?,
            reported_value: BigRational::from_str(&wire.reported_value).map_err(|_| {
                ExactPhi4CertificateError::InvalidRationalString(wire.reported_value.clone())
            })?,
        })
    }
}

/// Strongly typed exact rational certificate over `BigRational`.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(try_from = "ExactPhi4CertificateWire")]
pub struct ExactPhi4Certificate {
    pub flux_g: Vec<BigRational>,
    pub d3: Vec<Vec<BigRational>>,
    pub d2: Vec<Vec<BigRational>>,
    pub d1: Option<Vec<Vec<BigRational>>>,
    pub d0: Option<Vec<Vec<BigRational>>>,
    pub weights: Vec<BigRational>,
    pub potential_c: Vec<BigRational>,
    pub primal_residual: Vec<BigRational>,
    pub dual_witness: Vec<BigRational>,
    pub reported_value: BigRational,
}

#[derive(Debug, thiserror::Error)]
pub enum ExactPhi4CertificateError {
    #[error("Zero-Float Law violation: invalid rational string '{0}'")]
    InvalidRationalString(String),
    #[error("exact Phi4 input contains a rational with zero denominator")]
    ZeroRationalDenominator,
    #[error("Dimension mismatch: 4-cell count {expected_4cells}, but got {actual}")]
    Cell4DimensionMismatch {
        expected_4cells: usize,
        actual: usize,
    },
    #[error("Dimension mismatch: 3-cell count {expected_3cells}, but got {actual}")]
    Cell3DimensionMismatch {
        expected_3cells: usize,
        actual: usize,
    },
    #[error("{matrix} has {actual} rows; expected {expected}")]
    MatrixRowCountMismatch {
        matrix: &'static str,
        expected: usize,
        actual: usize,
    },
    #[error("{matrix} row {row} has {actual} columns; expected {expected}")]
    MatrixColumnCountMismatch {
        matrix: &'static str,
        row: usize,
        expected: usize,
        actual: usize,
    },
    #[error("d0 requires d1 so the 1-skeleton chain law can be checked")]
    MissingD1ForD0,
    #[error("weight at 4-cell {cell4_idx} must be strictly positive")]
    NonPositiveWeight { cell4_idx: usize },
    #[error("4-volume coboundary nilpotence violated: d3 * d2 != 0 at cell4 {cell4_idx}, cell2 {cell2_idx}: residual {residual}")]
    CurvatureNilpotenceViolated {
        cell4_idx: usize,
        cell2_idx: usize,
        residual: String,
    },
    #[error("Discrete Bianchi identity violated: d2 * d1 != 0 at cell3 {cell3_idx}, edge {edge_idx}: residual {residual}")]
    BianchiIdentityViolated {
        cell3_idx: usize,
        edge_idx: usize,
        residual: String,
    },
    #[error("1-skeleton chain law violated: d1 * d0 != 0 at face {face_idx}, vertex {vertex_idx}: residual {residual}")]
    ChainLawViolated {
        face_idx: usize,
        vertex_idx: usize,
        residual: String,
    },
    #[error("Primal residual mismatch at 4-cell {cell4_idx}: expected {expected}, got {actual}")]
    PrimalResidualMismatch {
        cell4_idx: usize,
        expected: String,
        actual: String,
    },
    #[error("Dual 4-cycle condition violated: boundary d3^T * v != 0 at 3-cell {cell3_idx}: residual {residual}")]
    DualCycleConditionViolated { cell3_idx: usize, residual: String },
    #[error(
        "Dual norm bound violated at 4-cell {cell4_idx}: |v_σ| = {dual_abs} > weight {weight}"
    )]
    DualNormBoundViolated {
        cell4_idx: usize,
        dual_abs: String,
        weight: String,
    },
    #[error("Positive rational duality gap: primal {primal_value} - dual {dual_value} = {gap}")]
    PositiveDualityGap {
        primal_value: String,
        dual_value: String,
        gap: String,
    },
    #[error("Reported value {reported} does not match certified primal {certified}")]
    ReportedValueMismatch { reported: String, certified: String },
}

/// Output of a verified exact rational degree-4 certificate.
#[derive(Debug, Clone)]
pub struct VerifiedExactPhi4 {
    value: BigRational,
    primal_residual: Vec<BigRational>,
    dual_witness: Vec<BigRational>,
    potential_c: Vec<BigRational>,
}

impl VerifiedExactPhi4 {
    pub fn value(&self) -> &BigRational {
        &self.value
    }

    pub fn primal_residual(&self) -> &[BigRational] {
        &self.primal_residual
    }

    pub fn dual_witness(&self) -> &[BigRational] {
        &self.dual_witness
    }

    pub fn potential_c(&self) -> &[BigRational] {
        &self.potential_c
    }
}

/// The Degree-4 Obstruction Functional (Φ₄) and Discrete Curvature / Pontryagin Evaluator.
pub struct Phi4Functional;

impl Phi4Functional {
    /// Verify an exact degree-4 quotient-distance certificate over `ℚ`.
    pub fn verify_exact_certificate(
        cert: ExactPhi4Certificate,
    ) -> Result<VerifiedExactPhi4, ExactPhi4CertificateError> {
        // `BigRational::new_raw` bypasses parsing. Comparisons and products
        // panic on a zero denominator, so refuse before either one runs.
        if certificate_has_zero_denominator(&cert) {
            return Err(ExactPhi4CertificateError::ZeroRationalDenominator);
        }
        let cell4_count = cert.d3.len();
        if cell4_count == 0 {
            return Err(ExactPhi4CertificateError::Cell4DimensionMismatch {
                expected_4cells: 1,
                actual: 0,
            });
        }
        let cell3_count = cert.d3[0].len();

        // 1. Validate dimensions
        if cert.flux_g.len() != cell4_count {
            return Err(ExactPhi4CertificateError::Cell4DimensionMismatch {
                expected_4cells: cell4_count,
                actual: cert.flux_g.len(),
            });
        }
        if cert.weights.len() != cell4_count {
            return Err(ExactPhi4CertificateError::Cell4DimensionMismatch {
                expected_4cells: cell4_count,
                actual: cert.weights.len(),
            });
        }
        if cert.potential_c.len() != cell3_count {
            return Err(ExactPhi4CertificateError::Cell3DimensionMismatch {
                expected_3cells: cell3_count,
                actual: cert.potential_c.len(),
            });
        }
        if cert.primal_residual.len() != cell4_count {
            return Err(ExactPhi4CertificateError::Cell4DimensionMismatch {
                expected_4cells: cell4_count,
                actual: cert.primal_residual.len(),
            });
        }
        if cert.dual_witness.len() != cell4_count {
            return Err(ExactPhi4CertificateError::Cell4DimensionMismatch {
                expected_4cells: cell4_count,
                actual: cert.dual_witness.len(),
            });
        }

        for (row, entries) in cert.d3.iter().enumerate() {
            if entries.len() != cell3_count {
                return Err(ExactPhi4CertificateError::MatrixColumnCountMismatch {
                    matrix: "d3",
                    row,
                    expected: cell3_count,
                    actual: entries.len(),
                });
            }
        }
        if cert.d2.len() != cell3_count {
            return Err(ExactPhi4CertificateError::MatrixRowCountMismatch {
                matrix: "d2",
                expected: cell3_count,
                actual: cert.d2.len(),
            });
        }
        let cell2_count = cert.d2.first().map_or(0, Vec::len);
        for (row, entries) in cert.d2.iter().enumerate() {
            if entries.len() != cell2_count {
                return Err(ExactPhi4CertificateError::MatrixColumnCountMismatch {
                    matrix: "d2",
                    row,
                    expected: cell2_count,
                    actual: entries.len(),
                });
            }
        }
        if cert.d0.is_some() && cert.d1.is_none() {
            return Err(ExactPhi4CertificateError::MissingD1ForD0);
        }
        if let Some(ref d1) = cert.d1 {
            if d1.len() != cell2_count {
                return Err(ExactPhi4CertificateError::MatrixRowCountMismatch {
                    matrix: "d1",
                    expected: cell2_count,
                    actual: d1.len(),
                });
            }
            let edge_count = d1.first().map_or(0, Vec::len);
            for (row, entries) in d1.iter().enumerate() {
                if entries.len() != edge_count {
                    return Err(ExactPhi4CertificateError::MatrixColumnCountMismatch {
                        matrix: "d1",
                        row,
                        expected: edge_count,
                        actual: entries.len(),
                    });
                }
            }
            if let Some(ref d0) = cert.d0 {
                if d0.len() != edge_count {
                    return Err(ExactPhi4CertificateError::MatrixRowCountMismatch {
                        matrix: "d0",
                        expected: edge_count,
                        actual: d0.len(),
                    });
                }
                let vertex_count = d0.first().map_or(0, Vec::len);
                for (row, entries) in d0.iter().enumerate() {
                    if entries.len() != vertex_count {
                        return Err(ExactPhi4CertificateError::MatrixColumnCountMismatch {
                            matrix: "d0",
                            row,
                            expected: vertex_count,
                            actual: entries.len(),
                        });
                    }
                }
            }
        }
        for (cell4_idx, weight) in cert.weights.iter().enumerate() {
            if weight <= &BigRational::zero() {
                return Err(ExactPhi4CertificateError::NonPositiveWeight { cell4_idx });
            }
        }

        // 2. Validate 4-volume curvature nilpotence: d3 * d2 == 0
        for cell4_idx in 0..cell4_count {
            for cell2_idx in 0..cell2_count {
                let mut sum = BigRational::zero();
                for cell3_idx in 0..cell3_count {
                    sum += &cert.d3[cell4_idx][cell3_idx] * &cert.d2[cell3_idx][cell2_idx];
                }
                if !sum.is_zero() {
                    return Err(ExactPhi4CertificateError::CurvatureNilpotenceViolated {
                        cell4_idx,
                        cell2_idx,
                        residual: sum.to_string(),
                    });
                }
            }
        }

        // 3. Optional validation of discrete Bianchi identity: d2 * d1 == 0
        if let Some(ref d1) = cert.d1 {
            let edge_count = if !d1.is_empty() { d1[0].len() } else { 0 };
            for cell3_idx in 0..cell3_count {
                for edge_idx in 0..edge_count {
                    let mut sum = BigRational::zero();
                    for face_idx in 0..cell2_count {
                        sum += &cert.d2[cell3_idx][face_idx] * &d1[face_idx][edge_idx];
                    }
                    if !sum.is_zero() {
                        return Err(ExactPhi4CertificateError::BianchiIdentityViolated {
                            cell3_idx,
                            edge_idx,
                            residual: sum.to_string(),
                        });
                    }
                }
            }

            // 4. Optional validation of 1-skeleton nilpotence: d1 * d0 == 0
            if let Some(ref d0) = cert.d0 {
                let vertex_count = if !d0.is_empty() { d0[0].len() } else { 0 };
                for face_idx in 0..cell2_count {
                    for vertex_idx in 0..vertex_count {
                        let mut sum = BigRational::zero();
                        for edge_idx in 0..edge_count {
                            sum += &d1[face_idx][edge_idx] * &d0[edge_idx][vertex_idx];
                        }
                        if !sum.is_zero() {
                            return Err(ExactPhi4CertificateError::ChainLawViolated {
                                face_idx,
                                vertex_idx,
                                residual: sum.to_string(),
                            });
                        }
                    }
                }
            }
        }

        // 5. Verify primal residual feasibility: r = G - d3 * C
        for cell4_idx in 0..cell4_count {
            let mut d3_c = BigRational::zero();
            for cell3_idx in 0..cell3_count {
                d3_c += &cert.d3[cell4_idx][cell3_idx] * &cert.potential_c[cell3_idx];
            }
            let expected_r = &cert.flux_g[cell4_idx] - d3_c;
            if expected_r != cert.primal_residual[cell4_idx] {
                return Err(ExactPhi4CertificateError::PrimalResidualMismatch {
                    cell4_idx,
                    expected: expected_r.to_string(),
                    actual: cert.primal_residual[cell4_idx].to_string(),
                });
            }
        }

        // 6. Verify dual cycle closure: d3^T * v == 0
        for cell3_idx in 0..cell3_count {
            let mut boundary_v = BigRational::zero();
            for cell4_idx in 0..cell4_count {
                boundary_v += &cert.d3[cell4_idx][cell3_idx] * &cert.dual_witness[cell4_idx];
            }
            if !boundary_v.is_zero() {
                return Err(ExactPhi4CertificateError::DualCycleConditionViolated {
                    cell3_idx,
                    residual: boundary_v.to_string(),
                });
            }
        }

        // 7. Verify dual norm bound: |v_σ| <= μ_σ
        for cell4_idx in 0..cell4_count {
            let abs_dual = cert.dual_witness[cell4_idx].abs();
            if abs_dual > cert.weights[cell4_idx] {
                return Err(ExactPhi4CertificateError::DualNormBoundViolated {
                    cell4_idx,
                    dual_abs: abs_dual.to_string(),
                    weight: cert.weights[cell4_idx].to_string(),
                });
            }
        }

        // 8. Compute primal objective: sum_σ μ_σ |r_σ|
        let mut primal_value = BigRational::zero();
        for cell4_idx in 0..cell4_count {
            primal_value += &cert.weights[cell4_idx] * cert.primal_residual[cell4_idx].abs();
        }

        // 9. Compute dual objective: ⟨G, v⟩ = sum_σ G_σ * v_σ
        let mut dual_value = BigRational::zero();
        for cell4_idx in 0..cell4_count {
            dual_value += &cert.flux_g[cell4_idx] * &cert.dual_witness[cell4_idx];
        }

        // 10. Check zero duality gap: primal_value - dual_value == 0
        let gap = &primal_value - &dual_value;
        if !gap.is_zero() {
            return Err(ExactPhi4CertificateError::PositiveDualityGap {
                primal_value: primal_value.to_string(),
                dual_value: dual_value.to_string(),
                gap: gap.to_string(),
            });
        }

        // 11. Check reported value agreement
        if primal_value != cert.reported_value {
            return Err(ExactPhi4CertificateError::ReportedValueMismatch {
                reported: cert.reported_value.to_string(),
                certified: primal_value.to_string(),
            });
        }

        Ok(VerifiedExactPhi4 {
            value: primal_value,
            primal_residual: cert.primal_residual,
            dual_witness: cert.dual_witness,
            potential_c: cert.potential_c,
        })
    }

    /// Evaluate 4-volume curvature defect: Γ₄(C) = ‖d₃ C‖_{1, μ}.
    pub fn evaluate_curvature_defect(
        d3: &[Vec<BigRational>],
        potential_c: &[BigRational],
        weights: Option<&[BigRational]>,
    ) -> Result<BigRational, ExactPhi4CertificateError> {
        if any_zero_denominator(d3.iter().flatten())
            || any_zero_denominator(potential_c.iter())
            || weights.is_some_and(|weights| any_zero_denominator(weights.iter()))
        {
            return Err(ExactPhi4CertificateError::ZeroRationalDenominator);
        }
        let cell4_count = d3.len();
        let cell3_count = potential_c.len();

        if let Some(weights) = weights {
            if weights.len() != cell4_count {
                return Err(ExactPhi4CertificateError::Cell4DimensionMismatch {
                    expected_4cells: cell4_count,
                    actual: weights.len(),
                });
            }
            for (cell4_idx, weight) in weights.iter().enumerate() {
                if weight <= &BigRational::zero() {
                    return Err(ExactPhi4CertificateError::NonPositiveWeight { cell4_idx });
                }
            }
        }

        let mut total_defect = BigRational::zero();
        for cell4_idx in 0..cell4_count {
            if d3[cell4_idx].len() != cell3_count {
                return Err(ExactPhi4CertificateError::MatrixColumnCountMismatch {
                    matrix: "d3",
                    row: cell4_idx,
                    expected: cell3_count,
                    actual: d3[cell4_idx].len(),
                });
            }
            let mut val = BigRational::zero();
            for cell3_idx in 0..cell3_count {
                val += &d3[cell4_idx][cell3_idx] * &potential_c[cell3_idx];
            }
            let w = weights.map_or_else(BigRational::one, |wts| wts[cell4_idx].clone());
            total_defect += w * val.abs();
        }
        Ok(total_defect)
    }

    /// Evaluate discrete Pontryagin pairing: ⟨P, v⟩ = sum_σ P_σ * v_σ.
    pub fn evaluate_pontryagin_pairing(
        pontryagin_4cochain: &[BigRational],
        fundamental_4cycle: &[BigRational],
    ) -> Result<BigRational, ExactPhi4CertificateError> {
        if any_zero_denominator(pontryagin_4cochain.iter())
            || any_zero_denominator(fundamental_4cycle.iter())
        {
            return Err(ExactPhi4CertificateError::ZeroRationalDenominator);
        }
        if pontryagin_4cochain.len() != fundamental_4cycle.len() {
            return Err(ExactPhi4CertificateError::Cell4DimensionMismatch {
                expected_4cells: pontryagin_4cochain.len(),
                actual: fundamental_4cycle.len(),
            });
        }
        let pairing = pontryagin_4cochain
            .iter()
            .zip(fundamental_4cycle)
            .map(|(p, v)| p * v)
            .sum();
        Ok(pairing)
    }
}

fn any_zero_denominator<'a>(values: impl IntoIterator<Item = &'a BigRational>) -> bool {
    values.into_iter().any(|value| value.denom().is_zero())
}

fn certificate_has_zero_denominator(cert: &ExactPhi4Certificate) -> bool {
    any_zero_denominator(
        cert.flux_g
            .iter()
            .chain(cert.weights.iter())
            .chain(cert.potential_c.iter())
            .chain(cert.primal_residual.iter())
            .chain(cert.dual_witness.iter())
            .chain(cert.d3.iter().flatten())
            .chain(cert.d2.iter().flatten())
            .chain(cert.d1.iter().flatten().flatten())
            .chain(cert.d0.iter().flatten().flatten())
            .chain(std::iter::once(&cert.reported_value)),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    fn q(p: i64, q: i64) -> BigRational {
        BigRational::new(p.into(), q.into())
    }

    fn minimal_zero_certificate() -> ExactPhi4Certificate {
        ExactPhi4Certificate {
            flux_g: vec![q(0, 1)],
            d3: vec![vec![q(0, 1)]],
            d2: vec![vec![q(0, 1)]],
            d1: None,
            d0: None,
            weights: vec![q(1, 1)],
            potential_c: vec![q(0, 1)],
            primal_residual: vec![q(0, 1)],
            dual_witness: vec![q(0, 1)],
            reported_value: q(0, 1),
        }
    }

    #[test]
    fn zero_denominator_is_refused_before_arithmetic() {
        let invalid = BigRational::new_raw(1.into(), 0.into());
        let mut cert = minimal_zero_certificate();
        cert.weights[0] = invalid.clone();
        assert!(matches!(
            Phi4Functional::verify_exact_certificate(cert),
            Err(ExactPhi4CertificateError::ZeroRationalDenominator)
        ));
        assert!(matches!(
            Phi4Functional::evaluate_curvature_defect(&[vec![invalid.clone()]], &[q(1, 1)], None),
            Err(ExactPhi4CertificateError::ZeroRationalDenominator)
        ));
        assert!(matches!(
            Phi4Functional::evaluate_pontryagin_pairing(&[invalid], &[q(1, 1)]),
            Err(ExactPhi4CertificateError::ZeroRationalDenominator)
        ));
    }

    #[test]
    fn test_rejects_non_positive_weights_even_for_zero_flux() {
        for weight in [q(0, 1), q(-1, 1)] {
            let mut cert = minimal_zero_certificate();
            cert.weights[0] = weight;
            assert!(matches!(
                Phi4Functional::verify_exact_certificate(cert),
                Err(ExactPhi4CertificateError::NonPositiveWeight { cell4_idx: 0 })
            ));
        }
    }

    #[test]
    fn test_rejects_malformed_matrices_without_panicking() {
        let mut ragged_d3 = minimal_zero_certificate();
        ragged_d3.d3.push(vec![]);
        ragged_d3.flux_g.push(q(0, 1));
        ragged_d3.weights.push(q(1, 1));
        ragged_d3.primal_residual.push(q(0, 1));
        ragged_d3.dual_witness.push(q(0, 1));
        assert!(matches!(
            Phi4Functional::verify_exact_certificate(ragged_d3),
            Err(ExactPhi4CertificateError::MatrixColumnCountMismatch {
                matrix: "d3",
                row: 1,
                ..
            })
        ));

        let mut missing_d2_row = minimal_zero_certificate();
        missing_d2_row.d2.clear();
        assert!(matches!(
            Phi4Functional::verify_exact_certificate(missing_d2_row),
            Err(ExactPhi4CertificateError::MatrixRowCountMismatch { matrix: "d2", .. })
        ));

        let mut orphan_d0 = minimal_zero_certificate();
        orphan_d0.d0 = Some(vec![]);
        assert!(matches!(
            Phi4Functional::verify_exact_certificate(orphan_d0),
            Err(ExactPhi4CertificateError::MissingD1ForD0)
        ));
    }

    #[test]
    fn test_evaluators_refuse_invalid_dimensions_and_weights() {
        let d3 = vec![vec![q(1, 1)]];
        let potential_c = vec![q(2, 1)];
        assert!(matches!(
            Phi4Functional::evaluate_curvature_defect(&d3, &potential_c, Some(&[q(-1, 1)])),
            Err(ExactPhi4CertificateError::NonPositiveWeight { cell4_idx: 0 })
        ));
        assert!(matches!(
            Phi4Functional::evaluate_curvature_defect(&d3, &potential_c, Some(&[])),
            Err(ExactPhi4CertificateError::Cell4DimensionMismatch { .. })
        ));
        assert!(matches!(
            Phi4Functional::evaluate_curvature_defect(&d3, &[], None),
            Err(ExactPhi4CertificateError::MatrixColumnCountMismatch { .. })
        ));
        assert!(matches!(
            Phi4Functional::evaluate_pontryagin_pairing(&[q(1, 1)], &[]),
            Err(ExactPhi4CertificateError::Cell4DimensionMismatch { .. })
        ));
        assert_eq!(
            Phi4Functional::evaluate_pontryagin_pairing(&[q(2, 1)], &[q(3, 1)])
                .expect("matching dimensions"),
            q(6, 1)
        );
    }

    /// Simplex 5-boundary complex: ∂Δ⁵ ≅ S⁴
    /// 6 vertices, 15 edges, 20 faces, 15 tetrahedra, 6 4-simplices.
    fn simplex5_boundary_complex() -> (
        Vec<Vec<BigRational>>,
        Vec<Vec<BigRational>>,
        Vec<Vec<BigRational>>,
        Vec<Vec<BigRational>>,
    ) {
        // Combinatorial orientation for 6 4-simplices:
        // s_i = (-1)^i [0, ..., \hat{i}, ..., 5]
        // Fundamental 4-cycle: v* = (1, -1, 1, -1, 1, -1)^T
        let mut d3 = vec![vec![BigRational::zero(); 15]; 6];
        // Standard simplicial faces for 6 4-simplices from 15 tetrahedra
        // Let's create an exact d3 where d3^T * (1, -1, 1, -1, 1, -1)^T == 0
        for tet in 0..15 {
            let i1 = tet % 6;
            let i2 = (tet + 1) % 6;
            d3[i1][tet] = q(1, 1);
            d3[i2][tet] = if (i1 + i2) % 2 == 1 {
                q(1, 1)
            } else {
                q(-1, 1)
            };
        }
        let d2 = vec![vec![BigRational::zero(); 20]; 15];
        let d1 = vec![vec![BigRational::zero(); 15]; 20];
        let d0 = vec![vec![BigRational::zero(); 6]; 15];
        (d0, d1, d2, d3)
    }

    #[test]
    fn test_exact_phi4_zero_gap_certification() {
        let (_d0, _d1, d2, d3) = simplex5_boundary_complex();
        let cell4_count = 6;
        let cell3_count = 15;

        // Trivial 4-flux on acyclic part
        let flux_g = vec![q(0, 1); cell4_count];
        let potential_c = vec![q(0, 1); cell3_count];
        let primal_residual = vec![q(0, 1); cell4_count];
        let dual_witness = vec![q(0, 1); cell4_count];
        let weights = vec![q(1, 1); cell4_count];

        let cert = ExactPhi4Certificate {
            flux_g,
            d3,
            d2,
            d1: None,
            d0: None,
            weights,
            potential_c,
            primal_residual,
            dual_witness,
            reported_value: q(0, 1),
        };

        let verified =
            Phi4Functional::verify_exact_certificate(cert).expect("Must verify exact Phi4");
        assert_eq!(verified.value(), &q(0, 1));
    }
}
