//! Diagonalisation by congruence of symmetric and Hermitian matrices, with a certificate
//! that replays.
//!
//! For a symmetric `A` (or Hermitian, with the field's involution) the algorithm produces an
//! invertible `S` and a diagonal `D` with `S* A S = D`, where `S*` is `Sᵀ` (symmetric case)
//! or `S†` (Hermitian case). It works over any field in which `2 ≠ 0`; no ordering is used
//! here. Reading the signs of `D` in an ordered field gives the inertia of `A` by Sylvester's
//! law; that step lives in `ordered`.
//!
//! The steps are congruences `M ← E* M E`, each one of three kinds, each tracked in `S ← S E`:
//!
//! 1. a symmetric permutation, to bring a nonzero diagonal entry to the pivot position;
//! 2. when every remaining diagonal entry is zero but `M[i][j] ≠ 0` (`i < j`, both in the
//!    trailing block), the shear `eᵢ ↦ eᵢ + c·eⱼ` with `c = M[i][j]⁻¹`. The new diagonal entry
//!    is `c·M[i][j] + conj(c·M[i][j]) = 1 + conj(1) = 2 ≠ 0`. Choosing `c` as the inverse, not
//!    as `1`, is what makes this work for a purely imaginary `M[i][j]`: with `c = 1` the new
//!    entry would be `M[i][j] + conj(M[i][j]) = 0`;
//! 3. the elimination `eₗ ↦ eₗ − μₗ·e_k`, `μₗ = M[k][l]·M[k][k]⁻¹`, which clears row and column `k`.
//!
//! Permutations have determinant `−1`, shears `1`, so `det S = ±1`; a verifier only needs
//! `S` invertible. If the trailing block is entirely zero the remaining diagonal entries are
//! `0` and the algorithm stops.
//!
//! Cost model used by the budget checks (worst case, scalar calls): `4n³ + 12n²`.
//!
//! AuthorityEffect: None.

use crate::linear_algebra::basic_matrix::{BasicMatrix, OperationLimits};
use crate::linear_algebra::elimination::{determinant, is_invertible};
use crate::linear_algebra::involution::{adjoint, hermitian_violation, Involution};
use crate::linear_algebra::matrix::{multiply, transpose};
use crate::linear_algebra::{
    charge, element_count, inverse_of, plus, require_square, reserve, times, ExactFieldError, Grid,
};
use crate::linear_algebra::scalars::{ExactRing, Field};

/// `S* A S = diag(D)` with `S` invertible: a congruence certificate for `A`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CongruenceDiagonalisation<F> {
    transform: BasicMatrix<F>,
    diagonal: Vec<F>,
}

impl<F> CongruenceDiagonalisation<F> {
    /// The change of basis `S` (`n × n`).
    pub fn transform(&self) -> &BasicMatrix<F> {
        &self.transform
    }

    /// The diagonal `D` (`n` entries).
    pub fn diagonal(&self) -> &[F] {
        &self.diagonal
    }

    /// The transform and the diagonal.
    pub fn into_parts(self) -> (BasicMatrix<F>, Vec<F>) {
        (self.transform, self.diagonal)
    }
}

impl<F: Field + ExactRing> CongruenceDiagonalisation<F> {
    /// Replays the symmetric certificate against `a`: `Sᵀ A S = diag(D)` entry for entry and
    /// `S` invertible. Does not trust whoever produced the certificate.
    pub fn verify_symmetric(&self, a: &BasicMatrix<F>) -> Result<(), ExactFieldError> {
        self.replay(a, &transpose(&self.transform)?)
    }

    fn replay(&self, a: &BasicMatrix<F>, star: &BasicMatrix<F>) -> Result<(), ExactFieldError> {
        let n = require_square("congruence certificate", a)?;
        if self.transform.shape() != (n, n) || self.diagonal.len() != n {
            return Err(ExactFieldError::CertificateRejected {
                reason: "the transform or the diagonal does not have the dimension of the matrix",
            });
        }
        if !is_invertible(&self.transform)? {
            return Err(ExactFieldError::CertificateRejected {
                reason: "the transform is singular",
            });
        }
        let product = multiply(&multiply(star, a)?, &self.transform)?;
        for r in 0..n {
            for c in 0..n {
                let expected = match self.diagonal.get(r) {
                    Some(d) if r == c => d.clone(),
                    _ => F::zero(),
                };
                if *product.get_ref(r, c)? != expected {
                    return Err(ExactFieldError::CertificateRejected {
                        reason: "S* A S differs from the claimed diagonal",
                    });
                }
            }
        }
        Ok(())
    }

    /// The determinant of the transform: `±1` for every certificate this module produces.
    pub fn transform_determinant(&self) -> Result<F, ExactFieldError> {
        determinant(&self.transform)
    }
}

impl<F: Involution> CongruenceDiagonalisation<F> {
    /// Replays the Hermitian certificate against `a`: `S† A S = diag(D)` and `S` invertible.
    pub fn verify_hermitian(&self, a: &BasicMatrix<F>) -> Result<(), ExactFieldError> {
        self.replay(a, &adjoint(&self.transform)?)
    }
}

/// The first position `(r, c)`, `r < c`, with `a[r][c] ≠ a[c][r]`, or `None` when symmetric.
pub(crate) fn symmetric_violation<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
) -> Result<Option<(usize, usize)>, ExactFieldError> {
    let n = require_square("symmetric check", a)?;
    for r in 0..n {
        for c in (r + 1)..n {
            if a.get_ref(r, c)? != a.get_ref(c, r)? {
                return Ok(Some((r, c)));
            }
        }
    }
    Ok(None)
}

/// Diagonalises a symmetric matrix by congruence: `Sᵀ A S = D`. Needs `2 ≠ 0` in the field.
/// Refuses a non-symmetric matrix.
pub fn symmetric_congruence_diagonalisation<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
) -> Result<CongruenceDiagonalisation<F>, ExactFieldError> {
    symmetric_congruence_diagonalisation_with_limits(a, OperationLimits::UNLIMITED)
}

/// [`symmetric_congruence_diagonalisation`] under a budget: `n²` elements, `4n³ + 12n²` calls.
pub fn symmetric_congruence_diagonalisation_with_limits<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<CongruenceDiagonalisation<F>, ExactFieldError> {
    if let Some((row, col)) = symmetric_violation(a)? {
        return Err(ExactFieldError::NotSymmetric { row, col });
    }
    diagonalise(a, &|x: &F| x.clone(), limits)
}

/// Diagonalises a Hermitian matrix by congruence: `S† A S = D` (the diagonal entries are
/// fixed by the involution). Needs `2 ≠ 0`. Refuses a non-Hermitian matrix.
pub fn hermitian_congruence_diagonalisation<F: Involution>(
    a: &BasicMatrix<F>,
) -> Result<CongruenceDiagonalisation<F>, ExactFieldError> {
    hermitian_congruence_diagonalisation_with_limits(a, OperationLimits::UNLIMITED)
}

/// [`hermitian_congruence_diagonalisation`] under a budget: `n²` elements, `4n³ + 12n²` calls.
pub fn hermitian_congruence_diagonalisation_with_limits<F: Involution>(
    a: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<CongruenceDiagonalisation<F>, ExactFieldError> {
    if let Some((row, col)) = hermitian_violation(a)? {
        return Err(ExactFieldError::NotHermitian { row, col });
    }
    diagonalise(a, &|x: &F| x.conjugate(), limits)
}

/// Symmetric permutation of `i` and `k`: rows and columns of `M`, columns of `S`.
fn swap_symmetric<F: Clone>(m: &mut Grid<F>, s: &mut Grid<F>, k: usize, i: usize) {
    m.swap_rows(k, i);
    m.swap_columns(k, i);
    s.swap_columns(k, i);
}

/// The first `(i, j)` with `k ≤ i < j < n` and `M[i][j] ≠ 0`, row-major.
fn first_off_diagonal<F: Field + ExactRing>(
    m: &Grid<F>,
    k: usize,
    n: usize,
) -> Option<(usize, usize)> {
    (k..n).find_map(|i| {
        ((i + 1)..n)
            .find(|&j| !m.at(i, j).is_zero())
            .map(|j| (i, j))
    })
}

/// Congruence `M ← E* M E`, `S ← S E` for `E = I + factor·e_source·e_targetᵀ`: column
/// `target += factor·column source` in both, then row `target += conj(factor)·row source`
/// in `M`. Rows and columns before `k` of `M` are zero there, so `M` is updated from `k`.
fn add_multiple<F: Field + ExactRing>(
    m: &mut Grid<F>,
    s: &mut Grid<F>,
    target: usize,
    source: usize,
    factor: &F,
    conj: &dyn Fn(&F) -> F,
    k: usize,
) {
    m.add_scaled_column(target, source, factor, k);
    s.add_scaled_column(target, source, factor, 0);
    m.add_scaled_row(target, source, &conj(factor), k);
}

/// Shared core. Precondition (checked by the callers): `a` is square and `a[r][c] =
/// conj(a[c][r])` for all `r, c`.
fn diagonalise<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    conj: &dyn Fn(&F) -> F,
    limits: OperationLimits,
) -> Result<CongruenceDiagonalisation<F>, ExactFieldError> {
    let n = a.rows();
    let square = element_count(n, n)?;
    let ops = plus(times(4, times(square, n)?)?, times(12, square)?)?;
    charge(limits, square, ops)?;
    if n > 0 && F::one().add(&F::one()).is_zero() {
        return Err(ExactFieldError::CharacteristicTwo {
            operation: "congruence diagonalisation",
        });
    }

    let mut m = Grid::from_matrix(a)?;
    let mut s = Grid::from_fn(n, n, |r, c| {
        Ok::<F, ExactFieldError>(if r == c { F::one() } else { F::zero() })
    })?;
    let mut diagonal: Vec<F> = reserve(n)?;
    for k in 0..n {
        if m.at(k, k).is_zero() {
            if let Some(i) = ((k + 1)..n).find(|&i| !m.at(i, i).is_zero()) {
                swap_symmetric(&mut m, &mut s, k, i);
            } else if let Some((i, j)) = first_off_diagonal(&m, k, n) {
                // Every diagonal entry of the trailing block is zero: make M[i][i] = 2.
                let c = inverse_of("congruence diagonalisation", m.at(i, j))?;
                add_multiple(&mut m, &mut s, i, j, &c, conj, k);
                swap_symmetric(&mut m, &mut s, k, i);
            } else {
                // The trailing block is zero: the remaining diagonal entries are zero.
                for _ in k..n {
                    diagonal.push(F::zero());
                }
                break;
            }
        }
        let pivot = m.at(k, k).clone();
        let inv = inverse_of("congruence diagonalisation", &pivot)?;
        diagonal.push(pivot);
        for l in (k + 1)..n {
            let mu = m.at(k, l).mul(&inv);
            if !mu.is_zero() {
                add_multiple(&mut m, &mut s, l, k, &mu.neg(), conj, k);
            }
        }
    }
    Ok(CongruenceDiagonalisation {
        transform: s.into_matrix()?,
        diagonal,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::matrix::{add, from_rows, identity};
    use crate::linear_algebra::test_support::{
        gi, gq, m, q, random_matrix, Fp, GaussianRational, Rng,
    };
    use crate::linear_algebra::scalars::Semiring;
    use num_rational::BigRational;

    type Q = BigRational;
    type G = GaussianRational;

    fn gmat(rows: &[&[(i64, i64)]]) -> BasicMatrix<G> {
        from_rows(
            rows.iter()
                .map(|r| r.iter().map(|&(a, b)| gi(a, b)).collect())
                .collect(),
        )
        .unwrap()
    }

    /// `B + Bᵀ` for a random `B`: symmetric, typically indefinite, generically invertible.
    fn random_symmetric(rng: &mut Rng, n: usize) -> BasicMatrix<Q> {
        let b = random_matrix(rng, n, n, 4);
        add(&b, &transpose(&b).unwrap()).unwrap()
    }

    fn random_hermitian(rng: &mut Rng, n: usize) -> BasicMatrix<G> {
        let b = from_rows(
            (0..n)
                .map(|_| {
                    (0..n)
                        .map(|_| {
                            gq(
                                q(rng.range(-3, 3), rng.range(1, 3)),
                                q(rng.range(-3, 3), rng.range(1, 3)),
                            )
                        })
                        .collect()
                })
                .collect(),
        )
        .unwrap();
        add(&b, &adjoint(&b).unwrap()).unwrap()
    }

    /// The certificate replays for random symmetric matrices of sizes 1..6, the transform has
    /// determinant ±1, and `D` really is diagonal (the replay compares every off-diagonal entry).
    #[test]
    fn symmetric_certificates_replay_and_the_transform_is_unimodular() {
        let mut rng = Rng::new(501);
        for n in 1..=6usize {
            for _ in 0..4 {
                let a = random_symmetric(&mut rng, n);
                let cert = symmetric_congruence_diagonalisation(&a).unwrap();
                cert.verify_symmetric(&a).unwrap();
                let det = cert.transform_determinant().unwrap();
                assert!(det == q(1, 1) || det == q(-1, 1), "det S = {det}");
                assert_eq!(cert.diagonal().len(), n);
            }
        }
    }

    #[test]
    fn hermitian_certificates_replay() {
        let mut rng = Rng::new(503);
        for n in 1..=5usize {
            for _ in 0..3 {
                let a = random_hermitian(&mut rng, n);
                let cert = hermitian_congruence_diagonalisation(&a).unwrap();
                cert.verify_hermitian(&a).unwrap();
                let det = cert.transform_determinant().unwrap();
                assert!(det == gi(1, 0) || det == gi(-1, 0));
            }
        }
    }

    /// A zero diagonal with nonzero off-diagonal entries forces the shear (step 2) repeatedly:
    /// the adjacency matrices of complete graphs.
    #[test]
    fn a_zero_diagonal_is_handled_by_the_shear() {
        for n in 2..=6usize {
            let a = BasicMatrix::try_from_fn(n, n, |r, c| if r == c { q(0, 1) } else { q(1, 1) })
                .unwrap();
            let cert = symmetric_congruence_diagonalisation(&a).unwrap();
            cert.verify_symmetric(&a).unwrap();
            assert!(
                cert.diagonal().iter().all(|d| !d.is_zero()),
                "K_{n} is invertible"
            );
        }
    }

    /// Hermitian case with a purely imaginary off-diagonal entry: σ_y. The shear with `c = 1`
    /// would give `i + conj(i) = 0`; `c = M[i][j]⁻¹` gives 2. The certificate must replay.
    #[test]
    fn the_hermitian_shear_works_for_imaginary_off_diagonal_entries() {
        let sigma_y = gmat(&[&[(0, 0), (0, -1)], &[(0, 1), (0, 0)]]);
        let cert = hermitian_congruence_diagonalisation(&sigma_y).unwrap();
        cert.verify_hermitian(&sigma_y).unwrap();
        assert!(cert.diagonal().iter().all(|d| !d.is_zero()));
        for d in cert.diagonal() {
            // diagonal entries of a Hermitian form are self-conjugate
            assert_eq!(d, &d.conjugate());
        }
    }

    #[test]
    fn a_zero_matrix_and_small_shapes() {
        let zero = crate::linear_algebra::matrix::zeros::<Q>(3, 3).unwrap();
        let cert = symmetric_congruence_diagonalisation(&zero).unwrap();
        cert.verify_symmetric(&zero).unwrap();
        assert_eq!(cert.diagonal(), &[q(0, 1), q(0, 1), q(0, 1)]);
        let empty = crate::linear_algebra::matrix::zeros::<Q>(0, 0).unwrap();
        let cert = symmetric_congruence_diagonalisation(&empty).unwrap();
        assert!(cert.diagonal().is_empty());
        cert.verify_symmetric(&empty).unwrap();
        let one = m(&[&[7]]);
        assert_eq!(
            symmetric_congruence_diagonalisation(&one)
                .unwrap()
                .diagonal(),
            &[q(7, 1)]
        );
    }

    /// A rank-deficient matrix ends with zero diagonal entries exactly `n − rank` times.
    #[test]
    fn the_number_of_zero_diagonal_entries_is_the_corank() {
        use crate::linear_algebra::elimination::rank;
        let mut rng = Rng::new(509);
        for _ in 0..12 {
            // B Bᵀ with B of rank <= 2 in 4 dimensions
            let b = random_matrix(&mut rng, 4, 2, 3);
            let a = multiply(&b, &transpose(&b).unwrap()).unwrap();
            let cert = symmetric_congruence_diagonalisation(&a).unwrap();
            cert.verify_symmetric(&a).unwrap();
            let zeros = cert.diagonal().iter().filter(|d| d.is_zero()).count();
            assert_eq!(zeros, 4 - rank(&a).unwrap());
        }
    }

    /// Works over a finite field of odd characteristic (no ordering needed): GF(5), [[0,1],[1,0]].
    #[test]
    fn diagonalisation_needs_only_characteristic_not_two() {
        type F5 = Fp<5>;
        let f = |x: i64| F5::new(x);
        let a = from_rows(vec![vec![f(0), f(1)], vec![f(1), f(0)]]).unwrap();
        let cert = symmetric_congruence_diagonalisation(&a).unwrap();
        cert.verify_symmetric(&a).unwrap();
        assert!(cert.diagonal().iter().all(|d| !d.is_zero()));
        // GF(3)
        type F3 = Fp<3>;
        let g = |x: i64| F3::new(x);
        let b = from_rows(vec![
            vec![g(1), g(2), g(0)],
            vec![g(2), g(0), g(1)],
            vec![g(0), g(1), g(2)],
        ])
        .unwrap();
        symmetric_congruence_diagonalisation(&b)
            .unwrap()
            .verify_symmetric(&b)
            .unwrap();
    }

    #[test]
    fn characteristic_two_is_refused() {
        type F2 = Fp<2>;
        let a = from_rows(vec![
            vec![F2::new(0), F2::new(1)],
            vec![F2::new(1), F2::new(0)],
        ])
        .unwrap();
        assert_eq!(
            symmetric_congruence_diagonalisation(&a),
            Err(ExactFieldError::CharacteristicTwo {
                operation: "congruence diagonalisation"
            })
        );
        assert!(matches!(
            hermitian_congruence_diagonalisation(&a),
            Err(ExactFieldError::CharacteristicTwo { .. })
        ));
    }

    /// `Z/6` has a nonzero element (2) without inverse. The first pivot of `[[2,1],[1,1]]` is
    /// that element, so the diagonalisation must refuse rather than divide by a non-unit.
    #[test]
    fn a_non_field_scalar_is_refused_by_the_diagonalisation() {
        use crate::linear_algebra::test_support::Z6;
        let a = from_rows(vec![
            vec![Z6::new(2), Z6::new(1)],
            vec![Z6::new(1), Z6::new(1)],
        ])
        .unwrap();
        assert_eq!(
            symmetric_congruence_diagonalisation(&a),
            Err(ExactFieldError::ScalarContract {
                operation: "congruence diagonalisation",
                violation: "a nonzero element has no multiplicative inverse"
            })
        );
    }

    #[test]
    fn non_symmetric_and_non_hermitian_inputs_are_refused_with_their_first_offending_entry() {
        let a = m(&[&[1, 2, 3], &[2, 1, 4], &[3, 5, 1]]);
        assert_eq!(
            symmetric_congruence_diagonalisation(&a),
            Err(ExactFieldError::NotSymmetric { row: 1, col: 2 })
        );
        let h = gmat(&[&[(1, 0), (0, 1)], &[(0, 1), (1, 0)]]);
        assert_eq!(
            hermitian_congruence_diagonalisation(&h),
            Err(ExactFieldError::NotHermitian { row: 0, col: 1 })
        );
        assert!(matches!(
            symmetric_congruence_diagonalisation(
                &crate::linear_algebra::matrix::zeros::<Q>(2, 3).unwrap()
            ),
            Err(ExactFieldError::NotSquare { .. })
        ));
    }

    /// The verifier rejects tampering: a changed diagonal entry, a changed transform entry,
    /// a singular transform, and a wrong shape.
    #[test]
    fn tampered_certificates_are_rejected() {
        let a = m(&[&[2, 1], &[1, 3]]);
        let cert = symmetric_congruence_diagonalisation(&a).unwrap();
        cert.verify_symmetric(&a).unwrap();

        let mut bad_diag = cert.clone();
        bad_diag.diagonal[0] = q(99, 1);
        assert_eq!(
            bad_diag.verify_symmetric(&a),
            Err(ExactFieldError::CertificateRejected {
                reason: "S* A S differs from the claimed diagonal"
            })
        );

        let mut bad_transform = cert.clone();
        bad_transform.transform = identity::<Q>(2).unwrap();
        assert!(bad_transform.verify_symmetric(&a).is_err());

        let singular = CongruenceDiagonalisation {
            transform: crate::linear_algebra::matrix::zeros::<Q>(2, 2).unwrap(),
            diagonal: vec![q(0, 1), q(0, 1)],
        };
        assert_eq!(
            singular.verify_symmetric(&a),
            Err(ExactFieldError::CertificateRejected {
                reason: "the transform is singular"
            })
        );
        let wrong_shape = CongruenceDiagonalisation {
            transform: identity::<Q>(3).unwrap(),
            diagonal: vec![q(1, 1); 3],
        };
        assert!(wrong_shape.verify_symmetric(&a).is_err());
    }

    /// Boundary: for `n = 2` the documented cost is `4·8 + 12·4 = 80` scalar calls, 4 elements.
    #[test]
    fn congruence_budget_boundary_is_inclusive() {
        let a = m(&[&[2, 1], &[1, 3]]);
        let exact = OperationLimits {
            max_elements: 4,
            max_scalar_ops: 80,
        };
        assert!(symmetric_congruence_diagonalisation_with_limits(&a, exact).is_ok());
        assert!(matches!(
            symmetric_congruence_diagonalisation_with_limits(
                &a,
                OperationLimits {
                    max_scalar_ops: 79,
                    ..exact
                }
            ),
            Err(ExactFieldError::Matrix(
                crate::linear_algebra::basic_matrix::MatrixError::OperationLimitExceeded {
                    requested: 80,
                    limit: 79
                }
            ))
        ));
        assert!(hermitian_congruence_diagonalisation_with_limits(
            &gmat(&[&[(1, 0), (0, 1)], &[(0, -1), (2, 0)]]),
            OperationLimits {
                max_elements: 3,
                ..exact
            }
        )
        .is_err());
    }

    /// Sanity for the test scalar: the diagonal of a Hermitian certificate over Q(i) is real.
    #[test]
    fn hermitian_diagonal_entries_are_real() {
        let mut rng = Rng::new(521);
        let a = random_hermitian(&mut rng, 4);
        let cert = hermitian_congruence_diagonalisation(&a).unwrap();
        for d in cert.diagonal() {
            assert!(Semiring::is_zero(&d.im), "diagonal entry {d:?} is not real");
        }
    }
}
