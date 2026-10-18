
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};
use std::str::FromStr;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ExactPhi2CertificateWire {
    pub flux_b: Vec<String>,
    pub d1: Vec<Vec<String>>,
    pub d0: Option<Vec<Vec<String>>>,
    pub weights: Vec<String>,
    pub potential_a: Vec<String>,
    pub primal_residual: Vec<String>,
    pub dual_witness: Vec<String>,
    pub reported_value: String,
}

impl TryFrom<ExactPhi2CertificateWire> for ExactPhi2Certificate {
    type Error = ExactPhi2CertificateError;

    fn try_from(wire: ExactPhi2CertificateWire) -> Result<Self, Self::Error> {
        fn parse_vec(v: &[String]) -> Result<Vec<BigRational>, ExactPhi2CertificateError> {
            crate::wire::parse_rational_vec(v, ExactPhi2CertificateError::InvalidRationalString)
        }
        fn parse_matrix(
            m: &[Vec<String>],
        ) -> Result<Vec<Vec<BigRational>>, ExactPhi2CertificateError> {
            crate::wire::parse_rational_matrix(m, ExactPhi2CertificateError::InvalidRationalString)
        }

        let flux_b = parse_vec(&wire.flux_b)?;
        let d1 = parse_matrix(&wire.d1)?;
        let d0 = match wire.d0 {
            Some(ref d0_mat) => Some(parse_matrix(d0_mat)?),
            None => None,
        };
        let weights = parse_vec(&wire.weights)?;
        let potential_a = parse_vec(&wire.potential_a)?;
        let primal_residual = parse_vec(&wire.primal_residual)?;
        let dual_witness = parse_vec(&wire.dual_witness)?;
        let reported_value = BigRational::from_str(&wire.reported_value).map_err(|_| {
            ExactPhi2CertificateError::InvalidRationalString(wire.reported_value.clone())
        })?;

        Ok(ExactPhi2Certificate {
            flux_b,
            d1,
            d0,
            weights,
            potential_a,
            primal_residual,
            dual_witness,
            reported_value,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(try_from = "ExactPhi2CertificateWire")]
pub struct ExactPhi2Certificate {
    pub flux_b: Vec<BigRational>,
    pub d1: Vec<Vec<BigRational>>,
    pub d0: Option<Vec<Vec<BigRational>>>,
    pub weights: Vec<BigRational>,
    pub potential_a: Vec<BigRational>,
    pub primal_residual: Vec<BigRational>,
    pub dual_witness: Vec<BigRational>,
    pub reported_value: BigRational,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VerifiedExactPhi2 {
    certificate: ExactPhi2Certificate,
}

impl VerifiedExactPhi2 {
    pub fn certificate(&self) -> &ExactPhi2Certificate {
        &self.certificate
    }

    pub fn value(&self) -> &BigRational {
        &self.certificate.reported_value
    }

    pub fn primal_residual(&self) -> &[BigRational] {
        &self.certificate.primal_residual
    }

    pub fn potential_a(&self) -> &[BigRational] {
        &self.certificate.potential_a
    }

    pub fn dual_witness(&self) -> &[BigRational] {
        &self.certificate.dual_witness
    }
}

#[derive(Debug, Clone, thiserror::Error, PartialEq, Eq)]
pub enum ExactPhi2CertificateError {
    #[error("invalid rational string: '{0}'")]
    InvalidRationalString(String),
    #[error("exact Phi2 input contains a rational with zero denominator")]
    ZeroRationalDenominator,
    #[error("flux_b, primal_residual, dual_witness, and weights must have length equal to face count {expected}, but found lengths {actual:?}")]
    FaceDimensionMismatch { expected: usize, actual: Vec<usize> },
    #[error("d1 matrix has {actual} rows but expected {expected} (|F|)")]
    D1RowMismatch { expected: usize, actual: usize },
    #[error("d1 row {row} has {actual} columns but expected {expected} (|E|)")]
    D1ColumnMismatch {
        row: usize,
        expected: usize,
        actual: usize,
    },
    #[error("d0 has dimension mismatch: rows={rows} (expected {expected_e}), cols={cols}")]
    D0DimensionMismatch {
        rows: usize,
        expected_e: usize,
        cols: usize,
    },
    #[error("cochain nilpotence law violated: (d1 * d0)[{row}][{col}] = {val} != 0")]
    ChainLawViolation {
        row: usize,
        col: usize,
        val: BigRational,
    },
    #[error("weight at face index {index} is non-positive")]
    NonPositiveWeight { index: usize },
    #[error("primal residual mismatch at face {index}: expected {expected}, got {actual}")]
    PrimalResidualMismatch {
        index: usize,
        expected: BigRational,
        actual: BigRational,
    },
    #[error("dual witness is not a closed 2-cycle: (d1^T * y) on edge {edge} = {residual} != 0")]
    DualNotClosed2Cycle { edge: usize, residual: BigRational },
    #[error("dual witness violates norm bound |y_{face}| = {val} > w_{face} = {bound}")]
    DualNormBoundViolation {
        face: usize,
        val: BigRational,
        bound: BigRational,
    },
    #[error("reported Phi2 value is negative")]
    NegativeReportedValue,
    #[error("reported Phi2 value does not match weighted primal residual norm")]
    PrimalValueMismatch,
    #[error("reported Phi2 value does not match dual pairing <B, y>")]
    DualValueMismatch,
}

pub struct Phi2Functional;

impl Phi2Functional {
    pub fn verify_exact_certificate(
        certificate: ExactPhi2Certificate,
    ) -> Result<VerifiedExactPhi2, ExactPhi2CertificateError> {
        let f_count = certificate.flux_b.len();
        let e_count = certificate.potential_a.len();

        let mut all_vals = certificate
            .flux_b
            .iter()
            .chain(certificate.weights.iter())
            .chain(certificate.potential_a.iter())
            .chain(certificate.primal_residual.iter())
            .chain(certificate.dual_witness.iter())
            .chain(certificate.d1.iter().flatten())
            .chain(std::iter::once(&certificate.reported_value));

        if all_vals.any(|v| v.denom().is_zero()) {
            return Err(ExactPhi2CertificateError::ZeroRationalDenominator);
        }

        if let Some(ref d0) = certificate.d0 {
            if d0.iter().flatten().any(|v| v.denom().is_zero()) {
                return Err(ExactPhi2CertificateError::ZeroRationalDenominator);
            }
        }

        if certificate.primal_residual.len() != f_count
            || certificate.dual_witness.len() != f_count
            || certificate.weights.len() != f_count
        {
            return Err(ExactPhi2CertificateError::FaceDimensionMismatch {
                expected: f_count,
                actual: vec![
                    certificate.flux_b.len(),
                    certificate.primal_residual.len(),
                    certificate.dual_witness.len(),
                    certificate.weights.len(),
                ],
            });
        }

        if certificate.d1.len() != f_count {
            return Err(ExactPhi2CertificateError::D1RowMismatch {
                expected: f_count,
                actual: certificate.d1.len(),
            });
        }

        for (row_idx, row) in certificate.d1.iter().enumerate() {
            if row.len() != e_count {
                return Err(ExactPhi2CertificateError::D1ColumnMismatch {
                    row: row_idx,
                    expected: e_count,
                    actual: row.len(),
                });
            }
        }

        if let Some(ref d0) = certificate.d0 {
            if d0.len() != e_count {
                return Err(ExactPhi2CertificateError::D0DimensionMismatch {
                    rows: d0.len(),
                    expected_e: e_count,
                    cols: if d0.is_empty() { 0 } else { d0[0].len() },
                });
            }
            let v_count = if d0.is_empty() { 0 } else { d0[0].len() };
            for row in d0.iter() {
                if row.len() != v_count {
                    return Err(ExactPhi2CertificateError::D0DimensionMismatch {
                        rows: d0.len(),
                        expected_e: e_count,
                        cols: row.len(),
                    });
                }
            }

            for f in 0..f_count {
                for v in 0..v_count {
                    let mut sum = BigRational::zero();
                    for e in 0..e_count {
                        sum += &certificate.d1[f][e] * &d0[e][v];
                    }
                    if !sum.is_zero() {
                        return Err(ExactPhi2CertificateError::ChainLawViolation {
                            row: f,
                            col: v,
                            val: sum,
                        });
                    }
                }
            }
        }

        for (i, w) in certificate.weights.iter().enumerate() {
            if *w <= BigRational::zero() {
                return Err(ExactPhi2CertificateError::NonPositiveWeight { index: i });
            }
        }

        for f in 0..f_count {
            let mut d1_a = BigRational::zero();
            for e in 0..e_count {
                d1_a += &certificate.d1[f][e] * &certificate.potential_a[e];
            }
            let expected_r = &certificate.flux_b[f] - &d1_a;
            if certificate.primal_residual[f] != expected_r {
                return Err(ExactPhi2CertificateError::PrimalResidualMismatch {
                    index: f,
                    expected: expected_r,
                    actual: certificate.primal_residual[f].clone(),
                });
            }
        }

        for e in 0..e_count {
            let mut col_sum = BigRational::zero();
            for f in 0..f_count {
                col_sum += &certificate.d1[f][e] * &certificate.dual_witness[f];
            }
            if !col_sum.is_zero() {
                return Err(ExactPhi2CertificateError::DualNotClosed2Cycle {
                    edge: e,
                    residual: col_sum,
                });
            }
        }

        for f in 0..f_count {
            if certificate.dual_witness[f].abs() > certificate.weights[f] {
                return Err(ExactPhi2CertificateError::DualNormBoundViolation {
                    face: f,
                    val: certificate.dual_witness[f].abs(),
                    bound: certificate.weights[f].clone(),
                });
            }
        }

        if certificate.reported_value < BigRational::zero() {
            return Err(ExactPhi2CertificateError::NegativeReportedValue);
        }

        let mut primal_sum = BigRational::zero();
        for f in 0..f_count {
            primal_sum += &certificate.weights[f] * certificate.primal_residual[f].abs();
        }
        if primal_sum != certificate.reported_value {
            return Err(ExactPhi2CertificateError::PrimalValueMismatch);
        }

        let mut dual_sum = BigRational::zero();
        for f in 0..f_count {
            dual_sum += &certificate.dual_witness[f] * &certificate.flux_b[f];
        }
        if dual_sum != certificate.reported_value {
            return Err(ExactPhi2CertificateError::DualValueMismatch);
        }

        Ok(VerifiedExactPhi2 { certificate })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;

    fn q(n: i64, d: i64) -> BigRational {
        BigRational::new(BigInt::from(n), BigInt::from(d))
    }

    fn tetrahedron_complex() -> (Vec<Vec<BigRational>>, Vec<Vec<BigRational>>) {
        let d0 = vec![
            vec![q(-1, 1), q(1, 1), q(0, 1), q(0, 1)],
            vec![q(-1, 1), q(0, 1), q(1, 1), q(0, 1)],
            vec![q(-1, 1), q(0, 1), q(0, 1), q(1, 1)],
            vec![q(0, 1), q(-1, 1), q(1, 1), q(0, 1)],
            vec![q(0, 1), q(-1, 1), q(0, 1), q(1, 1)],
            vec![q(0, 1), q(0, 1), q(-1, 1), q(1, 1)],
        ];

        let d1 = vec![
            vec![q(1, 1), q(-1, 1), q(0, 1), q(1, 1), q(0, 1), q(0, 1)],
            vec![q(1, 1), q(0, 1), q(-1, 1), q(0, 1), q(1, 1), q(0, 1)],
            vec![q(0, 1), q(1, 1), q(-1, 1), q(0, 1), q(0, 1), q(1, 1)],
            vec![q(0, 1), q(0, 1), q(0, 1), q(1, 1), q(-1, 1), q(1, 1)],
        ];

        (d0, d1)
    }

    #[test]
    fn test_tetrahedron_chain_law_and_valid_b2_certificate() {
        let (d0, d1) = tetrahedron_complex();

        let flux_b = vec![q(1, 4), q(-1, 4), q(1, 4), q(-1, 4)];
        let weights = vec![q(1, 1), q(1, 1), q(1, 1), q(1, 1)];
        let potential_a = vec![q(0, 1); 6];
        let primal_residual = flux_b.clone();
        let dual_witness = vec![q(1, 1), q(-1, 1), q(1, 1), q(-1, 1)];
        let reported_value = q(1, 1);

        let cert = ExactPhi2Certificate {
            flux_b,
            d1,
            d0: Some(d0),
            weights,
            potential_a,
            primal_residual,
            dual_witness,
            reported_value,
        };

        let verified = Phi2Functional::verify_exact_certificate(cert)
            .expect("Must certify valid b2=1 certificate");
        assert_eq!(*verified.value(), q(1, 1));
    }

    #[test]
    fn test_tetrahedron_rejects_non_closed_2_chain() {
        let (d0, d1) = tetrahedron_complex();
        let flux_b = vec![q(1, 4), q(-1, 4), q(1, 4), q(-1, 4)];
        let weights = vec![q(1, 1), q(1, 1), q(1, 1), q(1, 1)];
        let potential_a = vec![q(0, 1); 6];
        let primal_residual = flux_b.clone();

        let leaking_witness = vec![q(1, 1), q(-1, 1), q(1, 1), q(0, 1)];
        let reported_value = q(3, 4);

        let cert = ExactPhi2Certificate {
            flux_b,
            d1,
            d0: Some(d0),
            weights,
            potential_a,
            primal_residual,
            dual_witness: leaking_witness,
            reported_value,
        };

        match Phi2Functional::verify_exact_certificate(cert) {
            Err(ExactPhi2CertificateError::DualNotClosed2Cycle { edge, residual }) => {
                assert_eq!(edge, 3);
                assert_eq!(residual, q(1, 1));
            }
            other => panic!("Expected DualNotClosed2Cycle, got {:?}", other),
        }
    }

    #[test]
    fn test_tetrahedron_rejects_dual_norm_violation() {
        let (d0, d1) = tetrahedron_complex();
        let flux_b = vec![q(1, 4), q(-1, 4), q(1, 4), q(-1, 4)];
        let weights = vec![q(1, 1), q(1, 1), q(1, 1), q(1, 1)];
        let potential_a = vec![q(0, 1); 6];
        let primal_residual = flux_b.clone();

        let dual_witness = vec![q(2, 1), q(-2, 1), q(2, 1), q(-2, 1)];
        let reported_value = q(2, 1);

        let cert = ExactPhi2Certificate {
            flux_b,
            d1,
            d0: Some(d0),
            weights,
            potential_a,
            primal_residual,
            dual_witness,
            reported_value,
        };

        match Phi2Functional::verify_exact_certificate(cert) {
            Err(ExactPhi2CertificateError::DualNormBoundViolation { face, val, bound }) => {
                assert_eq!(face, 0);
                assert_eq!(val, q(2, 1));
                assert_eq!(bound, q(1, 1));
            }
            other => panic!("Expected DualNormBoundViolation, got {:?}", other),
        }
    }

    #[test]
    fn test_tetrahedron_rejects_duality_gap() {
        let (d0, d1) = tetrahedron_complex();
        let flux_b = vec![q(1, 4), q(-1, 4), q(1, 4), q(-1, 4)];
        let weights = vec![q(1, 1), q(1, 1), q(1, 1), q(1, 1)];
        let potential_a = vec![q(0, 1); 6];
        let primal_residual = flux_b.clone();

        let dual_witness = vec![q(1, 2), q(-1, 2), q(1, 2), q(-1, 2)];
        let reported_value = q(1, 1);

        let cert = ExactPhi2Certificate {
            flux_b,
            d1,
            d0: Some(d0),
            weights,
            potential_a,
            primal_residual,
            dual_witness,
            reported_value,
        };

        match Phi2Functional::verify_exact_certificate(cert) {
            Err(ExactPhi2CertificateError::DualValueMismatch) => (),
            other => panic!("Expected DualValueMismatch, got {:?}", other),
        }
    }
}
