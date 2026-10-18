
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};
use std::str::FromStr;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ExactPhi3CertificateWire {
    pub flux_h: Vec<String>,
    pub d2: Vec<Vec<String>>,
    pub d1: Option<Vec<Vec<String>>>,
    pub d0: Option<Vec<Vec<String>>>,
    pub weights: Vec<String>,
    pub potential_b: Vec<String>,
    pub primal_residual: Vec<String>,
    pub dual_witness: Vec<String>,
    pub reported_value: String,
}

impl TryFrom<ExactPhi3CertificateWire> for ExactPhi3Certificate {
    type Error = ExactPhi3CertificateError;

    fn try_from(wire: ExactPhi3CertificateWire) -> Result<Self, Self::Error> {
        fn parse_vec(v: &[String]) -> Result<Vec<BigRational>, ExactPhi3CertificateError> {
            crate::wire::parse_rational_vec(v, ExactPhi3CertificateError::InvalidRationalString)
        }
        fn parse_matrix(
            m: &[Vec<String>],
        ) -> Result<Vec<Vec<BigRational>>, ExactPhi3CertificateError> {
            crate::wire::parse_rational_matrix(m, ExactPhi3CertificateError::InvalidRationalString)
        }

        let flux_h = parse_vec(&wire.flux_h)?;
        let d2 = parse_matrix(&wire.d2)?;
        let d1 = match wire.d1 {
            Some(ref d1_mat) => Some(parse_matrix(d1_mat)?),
            None => None,
        };
        let d0 = match wire.d0 {
            Some(ref d0_mat) => Some(parse_matrix(d0_mat)?),
            None => None,
        };
        let weights = parse_vec(&wire.weights)?;
        let potential_b = parse_vec(&wire.potential_b)?;
        let primal_residual = parse_vec(&wire.primal_residual)?;
        let dual_witness = parse_vec(&wire.dual_witness)?;
        let reported_value = BigRational::from_str(&wire.reported_value).map_err(|_| {
            ExactPhi3CertificateError::InvalidRationalString(wire.reported_value.clone())
        })?;

        Ok(ExactPhi3Certificate {
            flux_h,
            d2,
            d1,
            d0,
            weights,
            potential_b,
            primal_residual,
            dual_witness,
            reported_value,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(try_from = "ExactPhi3CertificateWire")]
pub struct ExactPhi3Certificate {
    pub flux_h: Vec<BigRational>,
    pub d2: Vec<Vec<BigRational>>,
    pub d1: Option<Vec<Vec<BigRational>>>,
    pub d0: Option<Vec<Vec<BigRational>>>,
    pub weights: Vec<BigRational>,
    pub potential_b: Vec<BigRational>,
    pub primal_residual: Vec<BigRational>,
    pub dual_witness: Vec<BigRational>,
    pub reported_value: BigRational,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VerifiedExactPhi3 {
    certificate: ExactPhi3Certificate,
}

impl VerifiedExactPhi3 {
    pub fn certificate(&self) -> &ExactPhi3Certificate {
        &self.certificate
    }

    pub fn value(&self) -> &BigRational {
        &self.certificate.reported_value
    }

    pub fn primal_residual(&self) -> &[BigRational] {
        &self.certificate.primal_residual
    }

    pub fn potential_b(&self) -> &[BigRational] {
        &self.certificate.potential_b
    }

    pub fn dual_witness(&self) -> &[BigRational] {
        &self.certificate.dual_witness
    }
}

#[derive(Debug, Clone, thiserror::Error, PartialEq, Eq)]
pub enum ExactPhi3CertificateError {
    #[error("invalid rational string: '{0}'")]
    InvalidRationalString(String),
    #[error("exact Phi3 input contains a rational with zero denominator")]
    ZeroRationalDenominator,
    #[error("flux_h, primal_residual, dual_witness, and weights must have length equal to 3-cell count {expected}, but found lengths {actual:?}")]
    Cell3DimensionMismatch { expected: usize, actual: Vec<usize> },
    #[error("d2 matrix has {actual} rows but expected {expected} (|C₃|)")]
    D2RowMismatch { expected: usize, actual: usize },
    #[error("d2 row {row} has {actual} columns but expected {expected} (|C₂|)")]
    D2ColumnMismatch {
        row: usize,
        expected: usize,
        actual: usize,
    },
    #[error("d1 matrix dimension mismatch: rows={rows} (expected {expected_c2}), cols={cols}")]
    D1DimensionMismatch {
        rows: usize,
        expected_c2: usize,
        cols: usize,
    },
    #[error("d0 matrix dimension mismatch: rows={rows} (expected {expected_c1}), cols={cols}")]
    D0DimensionMismatch {
        rows: usize,
        expected_c1: usize,
        cols: usize,
    },
    #[error("d0 requires d1 so the 1-skeleton chain law can be checked")]
    MissingD1ForD0,
    #[error("Bianchi identity nilpotence law violated: (d2 * d1)[{row}][{col}] = {val} != 0")]
    BianchiNilpotenceViolation {
        row: usize,
        col: usize,
        val: BigRational,
    },
    #[error("1-skeleton cochain nilpotence law violated: (d1 * d0)[{row}][{col}] = {val} != 0")]
    CochainNilpotenceViolation {
        row: usize,
        col: usize,
        val: BigRational,
    },
    #[error("weight at 3-cell index {index} is non-positive")]
    NonPositiveWeight { index: usize },
    #[error("primal residual mismatch at 3-cell {index}: expected {expected}, got {actual}")]
    PrimalResidualMismatch {
        index: usize,
        expected: BigRational,
        actual: BigRational,
    },
    #[error(
        "dual witness is not a closed 3-cycle: (d2^T * u) on 2-cell {cell2} = {residual} != 0"
    )]
    DualNotClosed3Cycle { cell2: usize, residual: BigRational },
    #[error("dual witness violates norm bound |u_{cell3}| = {val} > nu_{cell3} = {bound}")]
    DualNormBoundViolation {
        cell3: usize,
        val: BigRational,
        bound: BigRational,
    },
    #[error("reported Phi3 value is negative")]
    NegativeReportedValue,
    #[error("reported Phi3 value does not match weighted primal residual norm")]
    PrimalValueMismatch,
    #[error("reported Phi3 value does not match dual pairing <H, u>")]
    DualValueMismatch,
}

pub struct Phi3Functional;

impl Phi3Functional {
    pub fn verify_exact_certificate(
        certificate: ExactPhi3Certificate,
    ) -> Result<VerifiedExactPhi3, ExactPhi3CertificateError> {
        let c3_count = certificate.flux_h.len();
        let c2_count = certificate.potential_b.len();

        let mut all_vals = certificate
            .flux_h
            .iter()
            .chain(certificate.weights.iter())
            .chain(certificate.potential_b.iter())
            .chain(certificate.primal_residual.iter())
            .chain(certificate.dual_witness.iter())
            .chain(certificate.d2.iter().flatten())
            .chain(std::iter::once(&certificate.reported_value));

        if all_vals.any(|v| v.denom().is_zero()) {
            return Err(ExactPhi3CertificateError::ZeroRationalDenominator);
        }

        if let Some(ref d1) = certificate.d1 {
            if d1.iter().flatten().any(|v| v.denom().is_zero()) {
                return Err(ExactPhi3CertificateError::ZeroRationalDenominator);
            }
        }
        if let Some(ref d0) = certificate.d0 {
            if d0.iter().flatten().any(|v| v.denom().is_zero()) {
                return Err(ExactPhi3CertificateError::ZeroRationalDenominator);
            }
        }
        if certificate.d0.is_some() && certificate.d1.is_none() {
            return Err(ExactPhi3CertificateError::MissingD1ForD0);
        }

        if certificate.primal_residual.len() != c3_count
            || certificate.dual_witness.len() != c3_count
            || certificate.weights.len() != c3_count
        {
            return Err(ExactPhi3CertificateError::Cell3DimensionMismatch {
                expected: c3_count,
                actual: vec![
                    certificate.flux_h.len(),
                    certificate.primal_residual.len(),
                    certificate.dual_witness.len(),
                    certificate.weights.len(),
                ],
            });
        }

        if certificate.d2.len() != c3_count {
            return Err(ExactPhi3CertificateError::D2RowMismatch {
                expected: c3_count,
                actual: certificate.d2.len(),
            });
        }

        for (row_idx, row) in certificate.d2.iter().enumerate() {
            if row.len() != c2_count {
                return Err(ExactPhi3CertificateError::D2ColumnMismatch {
                    row: row_idx,
                    expected: c2_count,
                    actual: row.len(),
                });
            }
        }

        if let Some(ref d1) = certificate.d1 {
            if d1.len() != c2_count {
                return Err(ExactPhi3CertificateError::D1DimensionMismatch {
                    rows: d1.len(),
                    expected_c2: c2_count,
                    cols: if d1.is_empty() { 0 } else { d1[0].len() },
                });
            }
            let c1_count = if d1.is_empty() { 0 } else { d1[0].len() };
            for row in d1.iter() {
                if row.len() != c1_count {
                    return Err(ExactPhi3CertificateError::D1DimensionMismatch {
                        rows: d1.len(),
                        expected_c2: c2_count,
                        cols: row.len(),
                    });
                }
            }

            for c3 in 0..c3_count {
                for c1 in 0..c1_count {
                    let mut sum = BigRational::zero();
                    for c2 in 0..c2_count {
                        sum += &certificate.d2[c3][c2] * &d1[c2][c1];
                    }
                    if !sum.is_zero() {
                        return Err(ExactPhi3CertificateError::BianchiNilpotenceViolation {
                            row: c3,
                            col: c1,
                            val: sum,
                        });
                    }
                }
            }

            if let Some(ref d0) = certificate.d0 {
                if d0.len() != c1_count {
                    return Err(ExactPhi3CertificateError::D0DimensionMismatch {
                        rows: d0.len(),
                        expected_c1: c1_count,
                        cols: if d0.is_empty() { 0 } else { d0[0].len() },
                    });
                }
                let c0_count = if d0.is_empty() { 0 } else { d0[0].len() };
                for row in d0.iter() {
                    if row.len() != c0_count {
                        return Err(ExactPhi3CertificateError::D0DimensionMismatch {
                            rows: d0.len(),
                            expected_c1: c1_count,
                            cols: row.len(),
                        });
                    }
                }

                for c2 in 0..c2_count {
                    for c0 in 0..c0_count {
                        let mut sum = BigRational::zero();
                        for c1 in 0..c1_count {
                            sum += &d1[c2][c1] * &d0[c1][c0];
                        }
                        if !sum.is_zero() {
                            return Err(ExactPhi3CertificateError::CochainNilpotenceViolation {
                                row: c2,
                                col: c0,
                                val: sum,
                            });
                        }
                    }
                }
            }
        }

        for (i, w) in certificate.weights.iter().enumerate() {
            if *w <= BigRational::zero() {
                return Err(ExactPhi3CertificateError::NonPositiveWeight { index: i });
            }
        }

        for c3 in 0..c3_count {
            let mut d2_b = BigRational::zero();
            for c2 in 0..c2_count {
                d2_b += &certificate.d2[c3][c2] * &certificate.potential_b[c2];
            }
            let expected_r = &certificate.flux_h[c3] - &d2_b;
            if certificate.primal_residual[c3] != expected_r {
                return Err(ExactPhi3CertificateError::PrimalResidualMismatch {
                    index: c3,
                    expected: expected_r,
                    actual: certificate.primal_residual[c3].clone(),
                });
            }
        }

        for c2 in 0..c2_count {
            let mut col_sum = BigRational::zero();
            for c3 in 0..c3_count {
                col_sum += &certificate.d2[c3][c2] * &certificate.dual_witness[c3];
            }
            if !col_sum.is_zero() {
                return Err(ExactPhi3CertificateError::DualNotClosed3Cycle {
                    cell2: c2,
                    residual: col_sum,
                });
            }
        }

        for c3 in 0..c3_count {
            if certificate.dual_witness[c3].abs() > certificate.weights[c3] {
                return Err(ExactPhi3CertificateError::DualNormBoundViolation {
                    cell3: c3,
                    val: certificate.dual_witness[c3].abs(),
                    bound: certificate.weights[c3].clone(),
                });
            }
        }

        if certificate.reported_value < BigRational::zero() {
            return Err(ExactPhi3CertificateError::NegativeReportedValue);
        }

        let mut primal_sum = BigRational::zero();
        for c3 in 0..c3_count {
            primal_sum += &certificate.weights[c3] * certificate.primal_residual[c3].abs();
        }
        if primal_sum != certificate.reported_value {
            return Err(ExactPhi3CertificateError::PrimalValueMismatch);
        }

        let mut dual_sum = BigRational::zero();
        for c3 in 0..c3_count {
            dual_sum += &certificate.dual_witness[c3] * &certificate.flux_h[c3];
        }
        if dual_sum != certificate.reported_value {
            return Err(ExactPhi3CertificateError::DualValueMismatch);
        }

        Ok(VerifiedExactPhi3 { certificate })
    }

    pub fn evaluate_bianchi_defect(
        d2: &[Vec<BigRational>],
        potential_b: &[BigRational],
        weights: &[BigRational],
    ) -> Result<BigRational, ExactPhi3CertificateError> {
        let c3_count = d2.len();
        let c2_count = potential_b.len();

        if weights.len() != c3_count {
            return Err(ExactPhi3CertificateError::Cell3DimensionMismatch {
                expected: c3_count,
                actual: vec![weights.len()],
            });
        }

        for (index, weight) in weights.iter().enumerate() {
            if *weight <= BigRational::zero() {
                return Err(ExactPhi3CertificateError::NonPositiveWeight { index });
            }
        }

        let mut defect = BigRational::zero();
        for c3 in 0..c3_count {
            if d2[c3].len() != c2_count {
                return Err(ExactPhi3CertificateError::D2ColumnMismatch {
                    row: c3,
                    expected: c2_count,
                    actual: d2[c3].len(),
                });
            }
            let mut sum = BigRational::zero();
            for c2 in 0..c2_count {
                sum += &d2[c3][c2] * &potential_b[c2];
            }
            defect += &weights[c3] * sum.abs();
        }

        Ok(defect)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;

    fn q(n: i64, d: i64) -> BigRational {
        BigRational::new(BigInt::from(n), BigInt::from(d))
    }

    fn simplex4_boundary_complex() -> (
        Vec<Vec<BigRational>>,
        Vec<Vec<BigRational>>,
        Vec<Vec<BigRational>>,
    ) {

        let d0 = vec![
            vec![q(-1, 1), q(1, 1), q(0, 1), q(0, 1), q(0, 1)],
            vec![q(-1, 1), q(0, 1), q(1, 1), q(0, 1), q(0, 1)],
            vec![q(-1, 1), q(0, 1), q(0, 1), q(1, 1), q(0, 1)],
            vec![q(-1, 1), q(0, 1), q(0, 1), q(0, 1), q(1, 1)],
            vec![q(0, 1), q(-1, 1), q(1, 1), q(0, 1), q(0, 1)],
            vec![q(0, 1), q(-1, 1), q(0, 1), q(1, 1), q(0, 1)],
            vec![q(0, 1), q(-1, 1), q(0, 1), q(0, 1), q(1, 1)],
            vec![q(0, 1), q(0, 1), q(-1, 1), q(1, 1), q(0, 1)],
            vec![q(0, 1), q(0, 1), q(-1, 1), q(0, 1), q(1, 1)],
            vec![q(0, 1), q(0, 1), q(0, 1), q(-1, 1), q(1, 1)],
        ];

        let d1 = vec![
            vec![
                q(1, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
            ],
            vec![
                q(1, 1),
                q(0, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
            ],
            vec![
                q(1, 1),
                q(0, 1),
                q(0, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
            ],
            vec![
                q(0, 1),
                q(1, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
                q(0, 1),
            ],
            vec![
                q(0, 1),
                q(1, 1),
                q(0, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
            ],
            vec![
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
            ],
            vec![
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(-1, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
                q(0, 1),
            ],
            vec![
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
                q(-1, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
            ],
            vec![
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
            ],
            vec![
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(-1, 1),
                q(1, 1),
            ],
        ];

        let d2 = vec![
            vec![
                q(-1, 1),
                q(1, 1),
                q(0, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
            ],
            vec![
                q(-1, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
                q(0, 1),
            ],
            vec![
                q(0, 1),
                q(-1, 1),
                q(1, 1),
                q(0, 1),
                q(0, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
                q(0, 1),
            ],
            vec![
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(-1, 1),
                q(1, 1),
                q(-1, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(1, 1),
            ],
            vec![
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(0, 1),
                q(-1, 1),
                q(1, 1),
                q(-1, 1),
                q(1, 1),
            ],
        ];

        (d0, d1, d2)
    }

    #[test]
    fn test_simplex4_chain_laws_and_valid_b3_certificate() {
        let (d0, d1, d2) = simplex4_boundary_complex();

        let flux_h = vec![q(1, 5), q(-1, 5), q(1, 5), q(-1, 5), q(1, 5)];
        let weights = vec![q(1, 1); 5];
        let potential_b = vec![q(0, 1); 10];
        let primal_residual = flux_h.clone();
        let dual_witness = vec![q(1, 1), q(-1, 1), q(1, 1), q(-1, 1), q(1, 1)];
        let reported_value = q(1, 1);

        let cert = ExactPhi3Certificate {
            flux_h,
            d2,
            d1: Some(d1),
            d0: Some(d0),
            weights,
            potential_b,
            primal_residual,
            dual_witness,
            reported_value,
        };

        let verified = Phi3Functional::verify_exact_certificate(cert)
            .expect("Must certify valid b3=1 certificate with Bianchi identity");
        assert_eq!(*verified.value(), q(1, 1));
    }

    #[test]
    fn test_bianchi_identity_exact_flux_has_zero_defect() {
        let (_d0, d1, d2) = simplex4_boundary_complex();

        let potential_a = vec![q(1, 2), q(0, 1), q(-1, 3), q(1, 4), q(2, 5)];
        let mut exact_flux_b = vec![BigRational::zero(); 10];
        for f in 0..10 {
            for v in 0..5 {
                exact_flux_b[f] += &d1[f][v] * &potential_a[v % potential_a.len()];
            }
        }

        let weights = vec![q(1, 1); 5];
        let defect = Phi3Functional::evaluate_bianchi_defect(&d2, &exact_flux_b, &weights)
            .expect("Must evaluate Bianchi defect");

        assert_eq!(
            defect,
            q(0, 1),
            "Bianchi defect of exact 2-flux must be identically zero"
        );
    }

    #[test]
    fn test_bianchi_defect_rejects_non_positive_weights() {
        let d2 = vec![vec![q(1, 1)]];
        let potential_b = vec![q(1, 1)];

        for weight in [q(0, 1), q(-1, 1)] {
            let result = Phi3Functional::evaluate_bianchi_defect(&d2, &potential_b, &[weight]);
            assert_eq!(
                result,
                Err(ExactPhi3CertificateError::NonPositiveWeight { index: 0 }),
            );
        }
    }

    #[test]
    fn test_simplex4_rejects_non_closed_3_chain() {
        let (d0, d1, d2) = simplex4_boundary_complex();
        let flux_h = vec![q(1, 5), q(-1, 5), q(1, 5), q(-1, 5), q(1, 5)];
        let weights = vec![q(1, 1); 5];
        let potential_b = vec![q(0, 1); 10];
        let primal_residual = flux_h.clone();

        let leaking_witness = vec![q(1, 1), q(-1, 1), q(1, 1), q(-1, 1), q(0, 1)];
        let reported_value = q(4, 5);

        let cert = ExactPhi3Certificate {
            flux_h,
            d2,
            d1: Some(d1),
            d0: Some(d0),
            weights,
            potential_b,
            primal_residual,
            dual_witness: leaking_witness,
            reported_value,
        };

        match Phi3Functional::verify_exact_certificate(cert) {
            Err(ExactPhi3CertificateError::DualNotClosed3Cycle { cell2: _, residual }) => {
                assert!(!residual.is_zero());
            }
            other => panic!("Expected DualNotClosed3Cycle, got {:?}", other),
        }
    }

    fn minimal_closed_phi3(d0: Option<Vec<Vec<BigRational>>>) -> ExactPhi3Certificate {
        ExactPhi3Certificate {
            flux_h: vec![q(1, 1)],
            d2: vec![vec![q(0, 1)]],
            d1: None,
            d0,
            weights: vec![q(1, 1)],
            potential_b: vec![q(0, 1)],
            primal_residual: vec![q(1, 1)],
            dual_witness: vec![q(1, 1)],
            reported_value: q(1, 1),
        }
    }

    #[test]
    fn orphan_d0_without_d1_is_not_sealed() {
        assert!(Phi3Functional::verify_exact_certificate(minimal_closed_phi3(None)).is_ok());
        let orphan = minimal_closed_phi3(Some(vec![vec![q(9, 1)]]));
        assert_eq!(
            Phi3Functional::verify_exact_certificate(orphan),
            Err(ExactPhi3CertificateError::MissingD1ForD0)
        );
    }
}
