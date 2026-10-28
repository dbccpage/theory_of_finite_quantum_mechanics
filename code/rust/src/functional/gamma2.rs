
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};

use engine_kernel::evidence::{
    CarrierManifestHash, CertifiedScalar, Hash256, ReplayHash, ToleranceProfileHash,
};

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum ClosureStatus {
    Closed,
    Open,
    IndeterminateWithinTolerance,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(try_from = "UntrustedCochainComplexWire")]
pub struct ExactCochainComplexQ {
    c0_dim: usize,
    c1_dim: usize,
    c2_dim: usize,
    d0: Vec<Vec<BigRational>>,
    d1: Vec<Vec<BigRational>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct UntrustedCochainComplexWire {
    pub c0_dim: usize,
    pub c1_dim: usize,
    pub c2_dim: usize,
    pub d0: Vec<Vec<BigRational>>,
    pub d1: Vec<Vec<BigRational>>,
}

impl TryFrom<UntrustedCochainComplexWire> for ExactCochainComplexQ {
    type Error = ExactGamma2Error;

    fn try_from(wire: UntrustedCochainComplexWire) -> Result<Self, Self::Error> {
        Self::try_new(wire.c0_dim, wire.c1_dim, wire.c2_dim, wire.d0, wire.d1)
    }
}

impl ExactCochainComplexQ {
    pub fn c0_dim(&self) -> usize {
        self.c0_dim
    }

    pub fn c1_dim(&self) -> usize {
        self.c1_dim
    }

    pub fn c2_dim(&self) -> usize {
        self.c2_dim
    }

    pub fn d0(&self) -> &[Vec<BigRational>] {
        &self.d0
    }

    pub fn d1(&self) -> &[Vec<BigRational>] {
        &self.d1
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub enum Complex2InputQ {
    Missing,
    Declared {
        c2_dim: usize,
        d1: Vec<Vec<BigRational>>,
    },
}

impl ExactCochainComplexQ {
    pub fn try_new_with_complex2(
        c0_dim: usize,
        c1_dim: usize,
        d0: Vec<Vec<BigRational>>,
        complex2: Complex2InputQ,
    ) -> Result<Self, ExactGamma2Error> {
        match complex2 {
            Complex2InputQ::Missing => Err(ExactGamma2Error::MissingComplex2),
            Complex2InputQ::Declared { c2_dim, d1 } => {
                Self::try_new(c0_dim, c1_dim, c2_dim, d0, d1)
            }
        }
    }

    pub fn try_new(
        c0_dim: usize,
        c1_dim: usize,
        c2_dim: usize,
        d0: Vec<Vec<BigRational>>,
        d1: Vec<Vec<BigRational>>,
    ) -> Result<Self, ExactGamma2Error> {
        let mut complex = Self {
            c0_dim,
            c1_dim,
            c2_dim,
            d0,
            d1,
        };
        complex.validate()?;
        for row in complex.d0.iter_mut().chain(&mut complex.d1) {
            for value in row {
                *value = canonical_rational(value);
            }
        }
        Ok(complex)
    }

    fn validate(&self) -> Result<(), ExactGamma2Error> {
        let Self {
            c0_dim,
            c1_dim,
            c2_dim,
            d0,
            d1,
        } = self;
        let (c0_dim, c1_dim, c2_dim) = (*c0_dim, *c1_dim, *c2_dim);
        if d0.len() != c1_dim {
            return Err(ExactGamma2Error::D0RowMismatch {
                expected: c1_dim,
                actual: d0.len(),
            });
        }
        for (row, coefficients) in d0.iter().enumerate() {
            if coefficients.len() != c0_dim {
                return Err(ExactGamma2Error::D0ColumnMismatch {
                    row,
                    expected: c0_dim,
                    actual: coefficients.len(),
                });
            }
        }
        if d1.len() != c2_dim {
            return Err(ExactGamma2Error::D1RowMismatch {
                expected: c2_dim,
                actual: d1.len(),
            });
        }
        for (row, coefficients) in d1.iter().enumerate() {
            if coefficients.len() != c1_dim {
                return Err(ExactGamma2Error::D1ColumnMismatch {
                    row,
                    expected: c1_dim,
                    actual: coefficients.len(),
                });
            }
        }

        validate_matrix_rationals(d0, "d0")?;
        validate_matrix_rationals(d1, "d1")?;
        verify_chain_law(d0, d1)
    }
}

fn validate_rationals(
    values: &[BigRational],
    field: &'static str,
    row: Option<usize>,
) -> Result<(), ExactGamma2Error> {
    for (column, value) in values.iter().enumerate() {
        if value.denom().is_zero() {
            return Err(ExactGamma2Error::ZeroDenominator { field, row, column });
        }
    }
    Ok(())
}

fn validate_matrix_rationals(
    matrix: &[Vec<BigRational>],
    field: &'static str,
) -> Result<(), ExactGamma2Error> {
    for (row, values) in matrix.iter().enumerate() {
        validate_rationals(values, field, Some(row))?;
    }
    Ok(())
}

pub(crate) fn canonical_rational(value: &BigRational) -> BigRational {
    BigRational::new(value.numer().clone(), value.denom().clone())
}

fn verify_chain_law(
    d0: &[Vec<BigRational>],
    d1: &[Vec<BigRational>],
) -> Result<(), ExactGamma2Error> {
    for (row, d1_row) in d1.iter().enumerate() {
        for (column, _) in d0.first().into_iter().flatten().enumerate() {
            let composition_entry = d1_row
                .iter()
                .zip(d0)
                .map(|(d1_entry, d0_row)| d1_entry.clone() * d0_row[column].clone())
                .sum::<BigRational>();
            if !composition_entry.is_zero() {
                return Err(ExactGamma2Error::CochainIdentityViolation { row, column });
            }
        }
    }
    Ok(())
}

pub struct DegreeOneResidualQ<'a> {
    complex: &'a ExactCochainComplexQ,
    h: Vec<BigRational>,
}

impl<'a> DegreeOneResidualQ<'a> {
    pub fn try_new(
        complex: &'a ExactCochainComplexQ,
        h: Vec<BigRational>,
    ) -> Result<Self, ExactGamma2Error> {
        validate_residual(complex, &h)?;
        Ok(Self {
            complex,
            h: h.iter().map(canonical_rational).collect(),
        })
    }

    pub fn complex(&self) -> &ExactCochainComplexQ {
        self.complex
    }

    pub fn h(&self) -> &[BigRational] {
        &self.h
    }
}

fn validate_residual(
    complex: &ExactCochainComplexQ,
    h: &[BigRational],
) -> Result<(), ExactGamma2Error> {
    if h.len() != complex.c1_dim {
        return Err(ExactGamma2Error::ResidualLengthMismatch {
            expected: complex.c1_dim,
            actual: h.len(),
        });
    }
    validate_rationals(h, "residual", None)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RawClosureDefectResult {
    residual: Vec<BigRational>,
    d1: Vec<Vec<BigRational>>,
    coboundary: Vec<BigRational>,
    value: BigRational,
}

impl RawClosureDefectResult {
    pub fn residual(&self) -> &[BigRational] {
        &self.residual
    }

    pub fn d1(&self) -> &[Vec<BigRational>] {
        &self.d1
    }

    pub fn coboundary(&self) -> &[BigRational] {
        &self.coboundary
    }

    pub fn value(&self) -> &BigRational {
        &self.value
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExactGamma2Result {
    residual: Vec<BigRational>,
    complex: ExactCochainComplexQ,
    coboundary: Vec<BigRational>,
    value: BigRational,
}

impl ExactGamma2Result {
    pub fn residual(&self) -> &[BigRational] {
        &self.residual
    }

    pub fn d0(&self) -> &[Vec<BigRational>] {
        self.complex.d0()
    }

    pub fn complex(&self) -> &ExactCochainComplexQ {
        &self.complex
    }

    pub fn coboundary(&self) -> &[BigRational] {
        &self.coboundary
    }

    pub fn value(&self) -> &BigRational {
        &self.value
    }
}

#[derive(Debug, Clone, thiserror::Error, PartialEq, Eq)]
pub enum ExactGamma2Error {
    #[error("gamma2 requires an explicit Complex2 declaration")]
    MissingComplex2,
    #[error("d0 has {actual} rows but residual has {expected} coordinates")]
    D0RowMismatch { expected: usize, actual: usize },
    #[error("d0 row {row} has {actual} columns but expected {expected}")]
    D0ColumnMismatch {
        row: usize,
        expected: usize,
        actual: usize,
    },
    #[error("d1 row {row} has {actual} columns but residual has {expected} coordinates")]
    D1ColumnMismatch {
        row: usize,
        expected: usize,
        actual: usize,
    },
    #[error("cochain identity d1 * d0 = 0 fails at row {row}, column {column}")]
    CochainIdentityViolation { row: usize, column: usize },
    #[error("d1 has {actual} rows but expected c2_dim {expected}")]
    D1RowMismatch { expected: usize, actual: usize },
    #[error("residual has length {actual} but expected c1_dim {expected}")]
    ResidualLengthMismatch { expected: usize, actual: usize },
    #[error("GAMMA2_ZERO_DENOMINATOR: {field} row {row:?}, column {column}")]
    ZeroDenominator {
        field: &'static str,
        row: Option<usize>,
        column: usize,
    },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Gamma2Artifact {
    pub value: CertifiedScalar,
    pub coboundary_hash: Hash256,
    pub residual_hash: Hash256,
    pub d1_hash: Hash256,
    pub c2_basis_hash: Hash256,
    pub c2_norm_profile_hash: Hash256,
    pub carrier_hash: CarrierManifestHash,
    pub exactness_artifact_hash: Option<Hash256>,
    pub tolerance_profile_hash: Option<ToleranceProfileHash>,
    pub replay_hash: ReplayHash,
    pub closure_status: ClosureStatus,
    pub quotient_interpretation: bool,
}

pub struct Gamma2Functional;

impl Gamma2Functional {
    pub fn try_compute_raw(
        residual: &[BigRational],
        d1: &[Vec<BigRational>],
    ) -> Result<RawClosureDefectResult, ExactGamma2Error> {
        let c1_dim = residual.len();
        for (row, coefficients) in d1.iter().enumerate() {
            if coefficients.len() != c1_dim {
                return Err(ExactGamma2Error::D1ColumnMismatch {
                    row,
                    expected: c1_dim,
                    actual: coefficients.len(),
                });
            }
        }
        validate_rationals(residual, "residual", None)?;
        validate_matrix_rationals(d1, "d1")?;
        let residual: Vec<_> = residual.iter().map(canonical_rational).collect();
        let d1: Vec<Vec<_>> = d1
            .iter()
            .map(|row| row.iter().map(canonical_rational).collect())
            .collect();
        let coboundary = d1
            .iter()
            .map(|row| row.iter().zip(&residual).map(|(a, b)| a * b).sum())
            .collect::<Vec<BigRational>>();
        let value = coboundary.iter().map(|entry: &BigRational| entry.abs()).sum();

        Ok(RawClosureDefectResult {
            residual,
            d1,
            coboundary,
            value,
        })
    }

    pub fn try_compute_exact_quotient(
        residual: &DegreeOneResidualQ,
    ) -> Result<ExactGamma2Result, ExactGamma2Error> {
        let complex = residual.complex;
        complex.validate()?;
        validate_residual(complex, &residual.h)?;

        let raw = Self::try_compute_raw(&residual.h, &complex.d1)?;
        Ok(ExactGamma2Result {
            residual: residual.h.clone(),
            complex: complex.clone(),
            coboundary: raw.coboundary,
            value: raw.value,
        })
    }
}

use crate::binary_degree::{check_input_length, check_shape, BinaryDegreeError};
impl Gamma2Functional {
    pub fn binary(
        rows: &[Vec<bool>],
        domain_dim: usize,
        residual: &[bool],
    ) -> Result<usize, BinaryDegreeError> {
        check_shape(rows, domain_dim)?;
        check_input_length(residual, domain_dim)?;
        Ok(rows
            .iter()
            .filter(|row| {
                row.iter()
                    .zip(residual)
                    .fold(false, |parity, (coefficient, value)| {
                        parity ^ (*coefficient && *value)
                    })
            })
            .count())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IntegerGamma2Error {
    CapacityOverflow,
}

impl Gamma2Functional {
    pub fn checked_closure([ab, bc, ca]: [i64; 3]) -> Result<i64, IntegerGamma2Error> {
        ab.checked_add(bc)
            .and_then(|partial| partial.checked_add(ca))
            .ok_or(IntegerGamma2Error::CapacityOverflow)
    }

    pub fn checked_face([ab, bc, ca]: [i64; 3]) -> Result<u64, IntegerGamma2Error> {
        Ok(Self::checked_closure([ab, bc, ca])?.unsigned_abs())
    }

    pub fn checked_total(face_masses: &[u64]) -> Result<u64, IntegerGamma2Error> {
        face_masses.iter().try_fold(0_u64, |total, face_mass| {
            total
                .checked_add(*face_mass)
                .ok_or(IntegerGamma2Error::CapacityOverflow)
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;

    fn r(value: i64) -> BigRational {
        BigRational::from_integer(BigInt::from(value))
    }

    fn compute_helper(
        res: &[BigRational],
        d0: &[Vec<BigRational>],
        d1: &[Vec<BigRational>],
    ) -> Result<ExactGamma2Result, ExactGamma2Error> {
        let c0_dim = d0.first().map_or(0, Vec::len);
        let c1_dim = res.len();
        let c2_dim = d1.len();
        let complex =
            ExactCochainComplexQ::try_new(c0_dim, c1_dim, c2_dim, d0.to_vec(), d1.to_vec())?;
        let q = DegreeOneResidualQ::try_new(&complex, res.to_vec())?;
        Gamma2Functional::try_compute_exact_quotient(&q)
    }

    #[test]
    fn test_exact_gamma2_checks_cochain_identity_and_value() {
        let result = compute_helper(&[r(2)], &[vec![r(0)]], &[vec![r(3)]]).unwrap();

        assert_eq!(result.coboundary(), &[r(6)]);
        assert_eq!(result.value(), &r(6));
    }

    #[test]
    fn test_exact_gamma2_rejects_nonzero_d1_d0() {
        assert_eq!(
            compute_helper(&[r(1)], &[vec![r(1)]], &[vec![r(1)]]),
            Err(ExactGamma2Error::CochainIdentityViolation { row: 0, column: 0 })
        );
    }

    #[test]
    fn rejects_missing_complex2() {
        assert_eq!(
            ExactCochainComplexQ::try_new_with_complex2(
                1,
                1,
                vec![vec![r(0)]],
                Complex2InputQ::Missing,
            ),
            Err(ExactGamma2Error::MissingComplex2)
        );

        let complex = ExactCochainComplexQ::try_new_with_complex2(
            1,
            1,
            vec![vec![r(0)]],
            Complex2InputQ::Declared {
                c2_dim: 1,
                d1: vec![vec![r(1)]],
            },
        )
        .expect("d1 * d0 = 0 for this declared Complex2");
        assert_eq!(complex.c2_dim(), 1);
        assert_eq!(complex.d1(), &[vec![r(1)]]);
    }

    #[test]
    fn struct_literal_complex_cannot_bypass_the_chain_law() {
        let complex = ExactCochainComplexQ {
            c0_dim: 1,
            c1_dim: 1,
            c2_dim: 1,
            d0: vec![vec![r(1)]],
            d1: vec![vec![r(1)]],
        };
        let residual = DegreeOneResidualQ {
            complex: &complex,
            h: vec![r(2)],
        };
        assert_eq!(
            Gamma2Functional::try_compute_exact_quotient(&residual),
            Err(ExactGamma2Error::CochainIdentityViolation { row: 0, column: 0 }),
            "a literal-constructed non-complex must not mint quotient-level evidence"
        );
    }

    #[test]
    fn short_residual_refuses_instead_of_truncating_to_zero() {
        let complex = ExactCochainComplexQ {
            c0_dim: 1,
            c1_dim: 2,
            c2_dim: 1,
            d0: vec![vec![r(0)], vec![r(0)]],
            d1: vec![vec![r(0), r(1)]],
        };
        let truncated = DegreeOneResidualQ {
            complex: &complex,
            h: vec![r(7)],
        };
        assert_eq!(
            Gamma2Functional::try_compute_exact_quotient(&truncated),
            Err(ExactGamma2Error::ResidualLengthMismatch {
                expected: 2,
                actual: 1
            })
        );

        let full = DegreeOneResidualQ {
            complex: &complex,
            h: vec![r(7), r(3)],
        };
        let gamma2 = Gamma2Functional::try_compute_exact_quotient(&full)
            .expect("a well-formed residual over a valid complex must compute");
        assert_eq!(gamma2.value(), &r(3), "Gamma2 = |d1 h| = |3| = 3");
    }

    #[test]
    fn untrusted_artifact_claim_cannot_replace_exact_gamma2_recomputation() {
        let artifact = Gamma2Artifact {
            value: CertifiedScalar::ExactRational(
                engine_kernel::evidence::RationalValue::try_new(
                    num_bigint::BigInt::from(0),
                    num_bigint::BigInt::from(1),
                )
                .unwrap(),
            ),
            coboundary_hash: Hash256([0; 32]),
            residual_hash: Hash256([0; 32]),
            d1_hash: Hash256([0; 32]),
            c2_basis_hash: Hash256([0; 32]),
            c2_norm_profile_hash: Hash256([0; 32]),
            carrier_hash: CarrierManifestHash(Hash256([0; 32])),
            exactness_artifact_hash: None,
            tolerance_profile_hash: Some(ToleranceProfileHash(Hash256([0; 32]))),
            replay_hash: ReplayHash(Hash256([0; 32])),
            closure_status: ClosureStatus::Closed,
            quotient_interpretation: true,
        };
        let json = serde_json::to_string(&artifact).unwrap();
        let claim: Gamma2Artifact = serde_json::from_str(&json).unwrap();
        let computed = compute_helper(&[r(3)], &[vec![r(0)]], &[vec![r(1)]]).unwrap();
        assert_eq!(computed.value(), &r(3));
        assert_eq!(computed.coboundary(), &[r(3)]);
        assert_ne!(
            computed.value(),
            &r(0),
            "a DTO saying Closed is not evidence"
        );
        assert_eq!(claim.closure_status, ClosureStatus::Closed);
        assert!(claim.exactness_artifact_hash.is_none());
    }

    #[test]
    fn every_declared_matrix_dimension_has_a_decisive_shape_refusal() {
        let cases = [
            (
                1,
                2,
                0,
                vec![vec![r(0)]],
                vec![],
                ExactGamma2Error::D0RowMismatch {
                    expected: 2,
                    actual: 1,
                },
            ),
            (
                2,
                1,
                0,
                vec![vec![r(0)]],
                vec![],
                ExactGamma2Error::D0ColumnMismatch {
                    row: 0,
                    expected: 2,
                    actual: 1,
                },
            ),
            (
                0,
                0,
                1,
                vec![],
                vec![],
                ExactGamma2Error::D1RowMismatch {
                    expected: 1,
                    actual: 0,
                },
            ),
            (
                0,
                1,
                1,
                vec![vec![]],
                vec![vec![]],
                ExactGamma2Error::D1ColumnMismatch {
                    row: 0,
                    expected: 1,
                    actual: 0,
                },
            ),
        ];
        for (c0, c1, c2, d0, d1, expected) in cases {
            assert_eq!(
                ExactCochainComplexQ::try_new(c0, c1, c2, d0, d1),
                Err(expected)
            );
        }
        let complex = ExactCochainComplexQ::try_new(0, 2, 0, vec![vec![], vec![]], vec![]).unwrap();
        assert_eq!(
            DegreeOneResidualQ::try_new(&complex, vec![r(0)]).err(),
            Some(ExactGamma2Error::ResidualLengthMismatch {
                expected: 2,
                actual: 1
            }),
        );
        assert!(DegreeOneResidualQ::try_new(&complex, vec![r(0), r(1)]).is_ok());
    }
    #[test]
    fn zero_denominators_are_refused_before_even_vacuous_arithmetic() {
        let invalid = || BigRational::new_raw(1.into(), 0.into());
        let refusal = |field, row| ExactGamma2Error::ZeroDenominator {
            field,
            row,
            column: 0,
        };
        assert_eq!(
            ExactCochainComplexQ::try_new(1, 1, 0, vec![vec![invalid()]], vec![]),
            Err(refusal("d0", Some(0))),
        );
        assert_eq!(
            ExactCochainComplexQ::try_new(0, 1, 1, vec![vec![]], vec![vec![invalid()]]),
            Err(refusal("d1", Some(0))),
        );
        let empty_d1 = ExactCochainComplexQ::try_new(0, 1, 0, vec![vec![]], vec![]).unwrap();
        assert_eq!(
            DegreeOneResidualQ::try_new(&empty_d1, vec![invalid()]).err(),
            Some(refusal("residual", None)),
        );
        assert_eq!(
            Gamma2Functional::try_compute_raw(&[invalid()], &[]),
            Err(refusal("residual", None))
        );
        assert_eq!(
            Gamma2Functional::try_compute_raw(&[r(0)], &[vec![invalid()]]),
            Err(refusal("d1", Some(0)))
        );
        let forged = DegreeOneResidualQ {
            complex: &empty_d1,
            h: vec![invalid()],
        };
        assert_eq!(
            Gamma2Functional::try_compute_exact_quotient(&forged),
            Err(refusal("residual", None))
        );
    }

    #[test]
    fn signed_unreduced_inputs_are_canonicalized_and_bind_the_complete_complex() {
        let raw = |a: i64, b: i64| BigRational::new_raw(a.into(), b.into());
        let complex = ExactCochainComplexQ::try_new(
            1,
            2,
            1,
            vec![vec![raw(-2, -2)], vec![raw(3, -3)]],
            vec![vec![raw(-2, -4), raw(3, 6)]],
        )
        .unwrap();
        let half = raw(1, 2);
        assert_eq!(complex.d0(), &[vec![r(1)], vec![r(-1)]]);
        assert_eq!(complex.d1(), &[vec![half.clone(), half.clone()]]);
        let canonical = ExactCochainComplexQ::try_new(
            1,
            2,
            1,
            vec![vec![r(1)], vec![r(-1)]],
            vec![vec![half.clone(), half]],
        )
        .unwrap();
        assert_eq!(
            serde_json::to_value(&complex).unwrap(),
            serde_json::to_value(&canonical).unwrap()
        );
        let h = DegreeOneResidualQ::try_new(&complex, vec![raw(-6, -2), raw(2, -2)]).unwrap();
        assert_eq!(h.h(), &[r(3), r(-1)]);
        assert_eq!(
            serde_json::to_value(h.h()).unwrap(),
            serde_json::to_value([r(3), r(-1)]).unwrap()
        );
        let result = Gamma2Functional::try_compute_exact_quotient(&h).unwrap();
        assert_eq!(result.value(), &r(1));
        assert_eq!(result.complex(), &complex);
        assert_eq!(result.d0(), complex.d0());
        let raw_result = Gamma2Functional::try_compute_raw(
            &[raw(-6, -2), raw(2, -2)],
            &[vec![raw(-2, -4), raw(3, 6)]],
        )
        .unwrap();
        assert_eq!(raw_result.residual(), result.residual());
        assert_eq!(raw_result.d1(), complex.d1());
        assert_eq!(
            serde_json::to_value(raw_result.residual()).unwrap(),
            serde_json::to_value(h.h()).unwrap()
        );
        assert_eq!(
            serde_json::to_value(raw_result.d1()).unwrap(),
            serde_json::to_value(canonical.d1()).unwrap()
        );
        assert_eq!(raw_result.value(), result.value());
        assert_eq!(raw_result.coboundary(), result.coboundary());
    }

    #[test]
    fn distinct_closure_maps_do_not_collapse_to_identical_zero_evidence() {
        let first = compute_helper(&[r(0)], &[vec![r(0)]], &[vec![r(0)]]).unwrap();
        let second = compute_helper(&[r(0)], &[vec![r(0)]], &[vec![r(2)]]).unwrap();
        assert_eq!(first.value(), second.value());
        assert_eq!(first.coboundary(), second.coboundary());
        assert_eq!(first.d0(), second.d0());
        assert_ne!(
            first, second,
            "d1 provenance must survive an equal scalar result"
        );
        assert_eq!(first.complex().d1(), &[vec![r(0)]]);
        assert_eq!(second.complex().d1(), &[vec![r(2)]]);
    }

    #[test]
    fn empty_middle_space_does_not_expand_unstored_outer_coordinates() {
        let complex =
            ExactCochainComplexQ::try_new(1_000_000, 0, 2, vec![], vec![vec![], vec![]]).unwrap();
        let h = DegreeOneResidualQ::try_new(&complex, vec![]).unwrap();
        let result = Gamma2Functional::try_compute_exact_quotient(&h).unwrap();
        assert_eq!(result.value(), &r(0));
        assert_eq!(result.coboundary(), &[r(0), r(0)]);
        assert_eq!(result.complex().c0_dim(), 1_000_000);
        assert_eq!(result.complex().c2_dim(), 2);
    }

    #[test]
    fn raw_closure_is_not_quotient_evidence_and_ragged_maps_are_refused() {
        let raw = Gamma2Functional::try_compute_raw(&[r(2)], &[vec![r(-3)]]).unwrap();
        assert_eq!(raw.coboundary(), &[r(-6)]);
        assert_eq!(raw.value(), &r(6));
        assert_eq!(
            compute_helper(&[r(2)], &[vec![r(1)]], &[vec![r(-3)]]),
            Err(ExactGamma2Error::CochainIdentityViolation { row: 0, column: 0 }),
        );
        assert_eq!(
            Gamma2Functional::try_compute_raw(&[r(2), r(9)], &[vec![r(-3)]]),
            Err(ExactGamma2Error::D1ColumnMismatch {
                row: 0,
                expected: 2,
                actual: 1
            }),
        );
    }


    fn triangle_d0() -> Vec<Vec<BigRational>> {
        vec![
            vec![r(-1), r(1), r(0)],
            vec![r(0), r(-1), r(1)],
            vec![r(1), r(0), r(-1)],
        ]
    }

    #[test]
    fn l20a1_gamma2_vanishes_on_a_nonzero_coboundary() {
        let d0 = vec![vec![r(1)], vec![r(-1)]];
        let d1 = vec![vec![r(1), r(1)]];
        let coboundary = vec![r(3), r(-3)];
        let g = compute_helper(&coboundary, &d0, &d1).unwrap();
        assert_eq!(
            g.value(),
            &r(0),
            "a nonzero coboundary must be closed (Γ2=0)"
        );
        assert_eq!(g.coboundary(), &[r(0)]);
    }

    #[test]
    fn l20a_gamma2_descends_to_the_quotient() {
        let d0 = vec![vec![r(1)], vec![r(-1)]];
        let d1 = vec![vec![r(1), r(1)]];
        let h = vec![r(1), r(0)];
        let h_shifted = vec![r(4), r(-3)];
        let g_h = compute_helper(&h, &d0, &d1).unwrap();
        let g_shift = compute_helper(&h_shifted, &d0, &d1).unwrap();
        assert_eq!(g_h.value(), g_shift.value());
    }

    #[test]
    fn l20a3_gamma2_is_positive_on_a_non_closed_residual() {
        let d0 = vec![vec![r(1)], vec![r(-1)]];
        let d1 = vec![vec![r(1), r(1)]];
        let h = vec![r(1), r(0)];
        let g = compute_helper(&h, &d0, &d1).unwrap();
        assert!(g.value() > &r(0));
    }

    #[test]
    fn l20a2_survivor_winding_cochain_is_closed() {
        let d0 = triangle_d0();
        let d1 = vec![vec![r(0), r(0), r(0)]];
        let winding = vec![r(1), r(1), r(1)];
        let g = compute_helper(&winding, &d0, &d1).unwrap();
        assert_eq!(g.value(), &r(0));
    }

    #[test]
    fn l20a_p0_dependency_gamma2_refuses_non_exact_complex() {
        let d0 = vec![vec![r(1)]];
        let d1 = vec![vec![r(1)]];
        assert_eq!(
            compute_helper(&[r(2)], &d0, &d1),
            Err(ExactGamma2Error::CochainIdentityViolation { row: 0, column: 0 })
        );
    }
}

#[cfg(test)]
mod seal_tests {
    use super::*;
    use num_bigint::BigInt;

    fn r(value: i64) -> BigRational {
        BigRational::from_integer(BigInt::from(value))
    }

    #[test]
    fn untrusted_payload_violating_the_chain_law_fails_to_deserialize() {
        let forged_wire = UntrustedCochainComplexWire {
            c0_dim: 1,
            c1_dim: 1,
            c2_dim: 1,
            d0: vec![vec![r(1)]],
            d1: vec![vec![r(1)]],
        };
        let json = serde_json::to_string(&forged_wire).expect("wire serializes");

        serde_json::from_str::<UntrustedCochainComplexWire>(&json)
            .expect("payload must be well-formed at the wire layer");

        let result: Result<ExactCochainComplexQ, _> = serde_json::from_str(&json);
        assert!(
            result.is_err(),
            "a well-formed payload with d1*d0 != 0 must not deserialize into a validated complex"
        );
    }

    #[test]
    fn valid_payload_still_round_trips_through_the_seal() {
        let complex = ExactCochainComplexQ::try_new(1, 1, 1, vec![vec![r(0)]], vec![vec![r(0)]])
            .expect("zero maps satisfy d1 * d0 = 0");

        let json = serde_json::to_string(&complex).expect("serializes");
        let restored: ExactCochainComplexQ = serde_json::from_str(&json).expect("round-trips");
        assert_eq!(restored, complex);
        assert_eq!(restored.c1_dim(), 1);
        assert_eq!(restored.d1(), &[vec![r(0)]]);
    }

    #[test]
    fn unknown_or_duplicate_wire_fields_cannot_be_silently_ignored() {
        let complex = ExactCochainComplexQ::try_new(0, 0, 0, vec![], vec![]).unwrap();
        let valid = serde_json::to_string(&complex).unwrap();
        let unknown = format!("{{\"authority_effect\":\"approved\",{}", &valid[1..]);
        let error = serde_json::from_str::<ExactCochainComplexQ>(&unknown)
            .unwrap_err()
            .to_string();
        assert!(
            error.contains("unknown field `authority_effect`"),
            "{error}"
        );
        let duplicate = format!("{{\"c1_dim\":0,{}", &valid[1..]);
        let error = serde_json::from_str::<ExactCochainComplexQ>(&duplicate)
            .unwrap_err()
            .to_string();
        assert!(error.contains("duplicate field `c1_dim`"), "{error}");
        assert_eq!(
            serde_json::from_str::<ExactCochainComplexQ>(&valid).unwrap(),
            complex
        );
    }

    #[test]
    fn wire_denominator_refusal_is_not_mistaken_for_chain_law_evidence() {
        let mut wire = UntrustedCochainComplexWire {
            c0_dim: 1,
            c1_dim: 1,
            c2_dim: 0,
            d0: vec![vec![r(0)]],
            d1: vec![],
        };
        let valid = serde_json::to_string(&wire).unwrap();
        serde_json::from_str::<ExactCochainComplexQ>(&valid).unwrap();
        wire.d0[0][0] = BigRational::new_raw(1.into(), 0.into());
        let invalid = serde_json::to_string(&wire).unwrap();
        let error = serde_json::from_str::<ExactCochainComplexQ>(&invalid)
            .unwrap_err()
            .to_string();
        assert!(error.contains("denominator"), "{error}");
    }

    #[test]
    fn explicit_complex2_wire_cannot_ignore_unsupported_structure_claims() {
        let declared = Complex2InputQ::Declared {
            c2_dim: 1,
            d1: vec![vec![r(0)]],
        };
        let mut wire = serde_json::to_value(&declared).unwrap();
        assert_eq!(
            serde_json::from_value::<Complex2InputQ>(wire.clone()).unwrap(),
            declared
        );
        wire["Declared"]["weighted_norm"] = serde_json::json!([999]);
        let error = serde_json::from_value::<Complex2InputQ>(wire)
            .unwrap_err()
            .to_string();
        assert!(error.contains("unknown field `weighted_norm`"), "{error}");
    }
}
