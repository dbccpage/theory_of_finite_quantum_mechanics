//! Exact rank certificates over Q. AuthorityEffect: None.
//!
//! For M=UV, LU=I_r and VR=I_r, rank(M)=r: factorization gives the
//! upper bound and the two split maps give the lower bound. The checker uses
//! matrix identities only; it does not trust the producer's elimination result.
//! Trust boundary: exact rational arithmetic and checked dense matrix operations.

use super::errors::HomologicalError;
use super::hashing::{hash_matrix, Hash256};
use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::image_kernel::ExactRowReduction;
use crate::linear_algebra::scalars::{q, Q};

/// Untrusted candidate. Public fields permit transport and adversarial checking.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RankCandidate {
    pub image: BasicMatrix<Q>,
    pub coordinates: BasicMatrix<Q>,
    pub image_retraction: BasicMatrix<Q>,
    pub coordinate_section: BasicMatrix<Q>,
}

/// Immutable evidence, obtainable only by replaying all three exact identities.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RankCertificate {
    matrix_hash: Hash256,
    rank: usize,
    candidate: RankCandidate,
}

impl RankCertificate {
    pub fn try_admit(
        matrix: &BasicMatrix<Q>,
        candidate: RankCandidate,
    ) -> Result<Self, HomologicalError> {
        check_coefficients(matrix, &candidate)?;
        let rank = candidate.image.cols();
        check_shapes(matrix, &candidate, rank)?;
        let identity = identity(rank)?;
        require_equal(
            &candidate.image.mul(&candidate.coordinates)?,
            matrix,
            "M=UV",
        )?;
        require_equal(
            &candidate.image_retraction.mul(&candidate.image)?,
            &identity,
            "LU=I",
        )?;
        require_equal(
            &candidate.coordinates.mul(&candidate.coordinate_section)?,
            &identity,
            "VR=I",
        )?;
        Ok(Self {
            matrix_hash: hash_matrix(matrix),
            rank,
            candidate,
        })
    }

    pub fn rank(&self) -> usize {
        self.rank
    }
    pub fn matrix_hash(&self) -> &Hash256 {
        &self.matrix_hash
    }
    pub fn candidate(&self) -> &RankCandidate {
        &self.candidate
    }

    /// Replaying against another matrix requires both its binding and its identities.
    pub fn verify_against(&self, matrix: &BasicMatrix<Q>) -> Result<(), HomologicalError> {
        // Canonical input admission precedes hash normalization.
        super::exact_scalar::admit_matrix(matrix)?;
        if self.matrix_hash != hash_matrix(matrix) {
            return Err(HomologicalError::CertificateMismatch {
                identity: "matrix binding",
            });
        }
        Self::try_admit(matrix, self.candidate.clone()).map(|_| ())
    }
}

fn shape(matrix: &BasicMatrix<Q>, expected: (usize, usize)) -> Result<(), HomologicalError> {
    if matrix.shape() != expected {
        return Err(HomologicalError::ShapeMismatch {
            expected,
            got: matrix.shape(),
        });
    }
    Ok(())
}

fn check_shapes(
    m: &BasicMatrix<Q>,
    c: &RankCandidate,
    rank: usize,
) -> Result<(), HomologicalError> {
    if rank > m.rows().min(m.cols()) {
        return Err(HomologicalError::CertificateMismatch {
            identity: "rank dimension",
        });
    }
    shape(&c.image, (m.rows(), rank))?;
    shape(&c.coordinates, (rank, m.cols()))?;
    shape(&c.image_retraction, (rank, m.rows()))?;
    shape(&c.coordinate_section, (m.cols(), rank))
}

fn require_equal(
    left: &BasicMatrix<Q>,
    right: &BasicMatrix<Q>,
    identity: &'static str,
) -> Result<(), HomologicalError> {
    if left != right {
        return Err(HomologicalError::CertificateMismatch { identity });
    }
    Ok(())
}

fn identity(n: usize) -> Result<BasicMatrix<Q>, HomologicalError> {
    Ok(BasicMatrix::try_from_fn(n, n, |i, j| q(i64::from(i == j)))?)
}

/// Produce a rank factorization by elimination, then independently check it.
/// Gram matrices are invertible over Q because the columns/rows are independent.
/// Matrix and inversion refusals propagate as typed errors; failure emits no
/// certificate. Standard rational arithmetic and allocator behavior remain in
/// the declared runtime trust boundary.
/// Dense work is polynomial in matrix dimensions, with rational bit growth.
pub fn certify_rank(matrix: &BasicMatrix<Q>) -> Result<RankCertificate, HomologicalError> {
    super::exact_scalar::admit_matrix(matrix)?;
    if matrix.rows() == 0 || matrix.cols() == 0 {
        return RankCertificate::try_admit(matrix, empty_candidate(matrix)?);
    }
    let (image, coordinates) = factorization(matrix)?;
    let image_retraction = left_inverse(&image)?;
    let coordinate_section = left_inverse(&coordinates.try_transpose()?)?.try_transpose()?;
    RankCertificate::try_admit(
        matrix,
        RankCandidate {
            image,
            coordinates,
            image_retraction,
            coordinate_section,
        },
    )
}

fn empty_candidate(matrix: &BasicMatrix<Q>) -> Result<RankCandidate, HomologicalError> {
    Ok(RankCandidate {
        image: BasicMatrix::zero(matrix.rows(), 0)?,
        coordinates: BasicMatrix::zero(0, matrix.cols())?,
        image_retraction: BasicMatrix::zero(0, matrix.rows())?,
        coordinate_section: BasicMatrix::zero(matrix.cols(), 0)?,
    })
}

fn check_coefficients(m: &BasicMatrix<Q>, c: &RankCandidate) -> Result<(), HomologicalError> {
    for matrix in [
        m,
        &c.image,
        &c.coordinates,
        &c.image_retraction,
        &c.coordinate_section,
    ] {
        super::exact_scalar::admit_matrix(matrix)?;
    }
    Ok(())
}

fn factorization(
    matrix: &BasicMatrix<Q>,
) -> Result<(BasicMatrix<Q>, BasicMatrix<Q>), HomologicalError> {
    let reduction = matrix
        .rank_and_rref()
        .map_err(|source| HomologicalError::RankReductionFailed { source })?;
    let pivots = reduction.pivot_columns();
    let rank = pivots.len();
    let image = BasicMatrix::try_from_fn_result(matrix.rows(), rank, |i, j| {
        let col = pivots.get(j).ok_or(HomologicalError::CertificateMismatch {
            identity: "pivot bounds",
        })?;
        Ok::<_, HomologicalError>(matrix.get(i, *col)?)
    })?;
    let coordinates = BasicMatrix::try_from_fn_result(rank, matrix.cols(), |i, j| {
        Ok::<_, HomologicalError>(reduction.rref().get(i, j)?)
    })?;
    Ok((image, coordinates))
}

/// (U^T U)^-1 U^T is a left inverse for a full-column-rank rational U.
fn left_inverse(image: &BasicMatrix<Q>) -> Result<BasicMatrix<Q>, HomologicalError> {
    let transpose = image.try_transpose()?;
    Ok(inverse(&transpose.mul(image)?)?.mul(&transpose)?)
}

fn inverse(matrix: &BasicMatrix<Q>) -> Result<BasicMatrix<Q>, HomologicalError> {
    crate::linear_algebra::elimination::inverse(matrix)
        .map_err(|source| HomologicalError::RankInverseFailed { source })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn inversion_failures_retain_a_typed_source() {
        let zero = BasicMatrix::zero(1, 1).unwrap();
        let error = inverse(&zero).unwrap_err();
        assert!(
            std::error::Error::source(&error).is_some(),
            "lost producer error: {error}"
        );
        assert!(matches!(
            error,
            HomologicalError::RankInverseFailed {
                source: crate::linear_algebra::ExactFieldError::Singular { rank: 0, size: 1 }
            }
        ));
        let rectangular = BasicMatrix::zero(1, 2).unwrap();
        assert!(matches!(
            inverse(&rectangular),
            Err(HomologicalError::RankInverseFailed {
                source: crate::linear_algebra::ExactFieldError::NotSquare {
                    rows: 1,
                    cols: 2,
                    ..
                }
            })
        ));
    }

    #[test]
    fn empty_shapes_with_huge_metadata_do_not_enumerate_the_shape() {
        let (send, receive) = std::sync::mpsc::channel();
        let worker = std::thread::spawn(move || {
            let mut ranks = Vec::new();
            for (rows, cols) in [(0, usize::MAX), (usize::MAX, 0), (0, 0), (0, 7), (7, 0)] {
                let matrix = BasicMatrix::from_row_major(rows, cols, Vec::<Q>::new()).unwrap();
                let certificate = certify_rank(&matrix).unwrap();
                certificate.verify_against(&matrix).unwrap();
                ranks.push(certificate.rank());
            }
            let _ = send.send(ranks);
        });
        let result = receive.recv_timeout(std::time::Duration::from_secs(2));
        assert!(
            result.is_ok(),
            "rank-zero producer enumerated a zero-area shape"
        );
        assert_eq!(result.unwrap(), vec![0; 5]);
        worker.join().unwrap();
    }

    fn matrix(rows: usize, cols: usize, values: Vec<Q>) -> BasicMatrix<Q> {
        BasicMatrix::from_row_major(rows, cols, values).unwrap()
    }
    fn independent_candidate() -> RankCandidate {
        use crate::linear_algebra::scalars::qr;
        RankCandidate {
            image: matrix(2, 1, vec![q(3), q(5)]),
            coordinates: matrix(1, 2, vec![q(2), q(3)]),
            image_retraction: matrix(1, 2, vec![qr(1, 3), q(0)]),
            coordinate_section: matrix(2, 1, vec![qr(1, 2), q(0)]),
        }
    }
    fn input() -> BasicMatrix<Q> {
        matrix(2, 2, vec![q(6), q(9), q(10), q(15)])
    }

    #[test]
    fn hand_constructed_certificate_and_each_independent_split_identity() {
        let m = input();
        let candidate = independent_candidate();
        let certificate = RankCertificate::try_admit(&m, candidate.clone()).unwrap();
        assert_eq!(certificate.rank(), 1);
        assert_eq!(certificate.candidate(), &candidate);
        certificate.verify_against(&m).unwrap();
        let mut bad = candidate.clone();
        bad.image_retraction = BasicMatrix::zero(1, 2).unwrap();
        assert!(matches!(
            RankCertificate::try_admit(&m, bad),
            Err(HomologicalError::CertificateMismatch { identity: "LU=I" })
        ));
        let mut bad = candidate.clone();
        bad.coordinate_section = BasicMatrix::zero(2, 1).unwrap();
        assert!(matches!(
            RankCertificate::try_admit(&m, bad),
            Err(HomologicalError::CertificateMismatch { identity: "VR=I" })
        ));
        let zero = BasicMatrix::zero(2, 2).unwrap();
        assert!(matches!(
            RankCertificate::try_admit(&zero, candidate),
            Err(HomologicalError::CertificateMismatch { identity: "M=UV" })
        ));
        assert!(certificate.verify_against(&zero).is_err());
    }

    #[test]
    fn every_candidate_role_enforces_shape_and_canonical_rationals() {
        for role in 0..4 {
            let mut candidate = independent_candidate();
            let bad = BasicMatrix::zero(1, 1).unwrap();
            match role {
                0 => candidate.image = bad,
                1 => candidate.coordinates = bad,
                2 => candidate.image_retraction = bad,
                _ => candidate.coordinate_section = bad,
            }
            assert!(matches!(
                RankCertificate::try_admit(&input(), candidate),
                Err(HomologicalError::ShapeMismatch { .. })
            ));
        }
        for bad in [
            Q::new_raw(1.into(), 0.into()),
            Q::new_raw(2.into(), 4.into()),
            Q::new_raw(1.into(), (-2).into()),
            Q::new_raw(0.into(), 2.into()),
        ] {
            let bad_input = matrix(1, 1, vec![bad.clone()]);
            assert!(matches!(
                certify_rank(&bad_input),
                Err(HomologicalError::InvalidRational { index: 0 })
            ));
            for role in 0..5 {
                let mut m = input();
                let mut candidate = independent_candidate();
                let target = match role {
                    0 => &mut m,
                    1 => &mut candidate.image,
                    2 => &mut candidate.coordinates,
                    3 => &mut candidate.image_retraction,
                    _ => &mut candidate.coordinate_section,
                };
                target.set(0, 0, bad.clone()).unwrap();
                assert!(
                    matches!(
                        RankCertificate::try_admit(&m, candidate),
                        Err(HomologicalError::InvalidRational { index: 0 })
                    ),
                    "role {role}"
                );
            }
        }
    }

    #[test]
    fn impossible_rank_is_refused_before_identity_allocation() {
        let candidate = RankCandidate {
            image: BasicMatrix::zero(0, usize::MAX).unwrap(),
            coordinates: BasicMatrix::zero(usize::MAX, 0).unwrap(),
            image_retraction: BasicMatrix::zero(usize::MAX, 0).unwrap(),
            coordinate_section: BasicMatrix::zero(0, usize::MAX).unwrap(),
        };
        assert!(matches!(
            RankCertificate::try_admit(&BasicMatrix::zero(0, 0).unwrap(), candidate),
            Err(HomologicalError::CertificateMismatch {
                identity: "rank dimension"
            })
        ));
    }

    #[test]
    fn replay_rejects_raw_scalar_domains_before_hashing() {
        let certificate = certify_rank(&matrix(1, 1, vec![q(1)])).unwrap();
        for bad in [
            Q::new_raw(1.into(), 0.into()),
            Q::new_raw(0.into(), 0.into()),
            Q::new_raw(2.into(), 4.into()),
            Q::new_raw(1.into(), (-2).into()),
            Q::new_raw(0.into(), 2.into()),
        ] {
            let candidate = matrix(1, 1, vec![bad]);
            assert!(matches!(certificate.verify_against(&candidate),
                Err(HomologicalError::InvalidRational { index: 0 })));
        }
    }
}
