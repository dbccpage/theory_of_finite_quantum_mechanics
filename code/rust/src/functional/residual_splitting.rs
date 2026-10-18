

use num_rational::BigRational as Q;
use num_traits::{One, Signed, Zero};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum ResidualSplittingError {
    #[error("{what} has shape {actual_rows}x{actual_cols}, expected {rows}x{cols}")]
    Shape {
        what: &'static str,
        rows: usize,
        cols: usize,
        actual_rows: usize,
        actual_cols: usize,
    },
    #[error("a rational entry has a non-positive denominator")]
    InvalidRational,
    #[error("weight {index} is not strictly positive")]
    NonPositiveWeight { index: usize },
    #[error("identity `{identity}` fails at ({row}, {column})")]
    IdentityFails {
        identity: &'static str,
        row: usize,
        column: usize,
    },
}

type Result<T> = std::result::Result<T, ResidualSplittingError>;

pub type RowMatrix = Vec<Vec<Q>>;

fn shape(what: &'static str, m: &[Vec<Q>], rows: usize, cols: usize) -> Result<()> {
    let bad = m.len() != rows || m.iter().any(|r| r.len() != cols);
    if bad {
        return Err(ResidualSplittingError::Shape {
            what,
            rows,
            cols,
            actual_rows: m.len(),
            actual_cols: m.first().map(Vec::len).unwrap_or(0),
        });
    }
    if m.iter().flatten().any(|x| !x.denom().is_positive()) {
        return Err(ResidualSplittingError::InvalidRational);
    }
    Ok(())
}

pub fn multiply(a: &[Vec<Q>], b: &[Vec<Q>], s: usize) -> RowMatrix {
    a.iter()
        .map(|row| {
            (0..s)
                .map(|j| row.iter().zip(b).map(|(x, br)| x * &br[j]).sum())
                .collect()
        })
        .collect()
}

fn subtract(a: &[Vec<Q>], b: &[Vec<Q>]) -> RowMatrix {
    a.iter()
        .zip(b)
        .map(|(x, y)| x.iter().zip(y).map(|(p, q)| p - q).collect())
        .collect()
}

fn identity(m: usize) -> RowMatrix {
    (0..m)
        .map(|i| (0..m).map(|j| if i == j { Q::one() } else { Q::zero() }).collect())
        .collect()
}

fn expect_equal(identity: &'static str, a: &[Vec<Q>], b: &[Vec<Q>]) -> Result<()> {
    for (row, (x, y)) in a.iter().zip(b).enumerate() {
        if let Some(column) = x.iter().zip(y).position(|(p, q)| p != q) {
            return Err(ResidualSplittingError::IdentityFails {
                identity,
                row,
                column,
            });
        }
    }
    Ok(())
}

fn check_weights(weights: &[Q]) -> Result<()> {
    if weights.iter().any(|w| !w.denom().is_positive()) {
        return Err(ResidualSplittingError::InvalidRational);
    }
    if let Some(index) = weights.iter().position(|w| !w.is_positive()) {
        return Err(ResidualSplittingError::NonPositiveWeight { index });
    }
    Ok(())
}

pub fn weighted_l1_operator_norm(matrix: &[Vec<Q>], weights: &[Q]) -> Result<Q> {
    let m = weights.len();
    check_weights(weights)?;
    shape("operator", matrix, m, m)?;
    let mut best = Q::zero();
    for j in 0..m {
        let column: Q = (0..m)
            .map(|i| &weights[i] * matrix[i][j].abs())
            .sum::<Q>()
            / &weights[j];
        if column > best {
            best = column;
        }
    }
    Ok(best)
}

pub fn splitting_from_parameter(
    basis: &[Vec<Q>],
    complement: &[Vec<Q>],
    inverse: &[Vec<Q>],
    parameter: &[Vec<Q>],
) -> Result<(RowMatrix, RowMatrix)> {
    let m = basis.len();
    let r = basis.first().map(Vec::len).unwrap_or(0);
    let s = m - r.min(m);
    shape("B", basis, m, r)?;
    shape("N", complement, m, s)?;
    shape("S^{-1}", inverse, m, m)?;
    shape("H", parameter, r, s)?;
    let u = &inverse[..r];
    let q = &inverse[r..];
    let hq = multiply(parameter, q, m);
    let u_plus: RowMatrix = u
        .iter()
        .zip(&hq)
        .map(|(a, b)| a.iter().zip(b).map(|(x, y)| x + y).collect())
        .collect();
    let projection = if r == 0 {
        vec![vec![Q::zero(); m]; m]
    } else {
        multiply(basis, &u_plus, m)
    };
    let bh = multiply(basis, parameter, s);
    let n_minus = subtract(complement, &bh);
    let residual = if s == 0 {
        vec![vec![Q::zero(); m]; m]
    } else {
        multiply(&n_minus, q, m)
    };
    Ok((projection, residual))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ResidualSplittingCertificate {
    pub d0: RowMatrix,
    pub repair_columns: usize,
    pub basis: RowMatrix,
    pub complement: RowMatrix,
    pub inverse: RowMatrix,
    pub parameter: RowMatrix,
    pub projection: RowMatrix,
    pub residual: RowMatrix,
    pub image_coordinates: RowMatrix,
    pub selection: RowMatrix,
}

impl ResidualSplittingCertificate {
    pub fn verify(&self, weights: &[Q]) -> Result<Q> {
        let m = weights.len();
        let k = self.repair_columns;
        check_weights(weights)?;
        shape("d0", &self.d0, m, k)?;
        let r = self.basis.first().map(Vec::len).unwrap_or(0);
        if r > m {
            return Err(ResidualSplittingError::Shape {
                what: "B",
                rows: m,
                cols: m,
                actual_rows: self.basis.len(),
                actual_cols: r,
            });
        }
        let s = m - r;
        shape("B", &self.basis, m, r)?;
        shape("N", &self.complement, m, s)?;
        shape("S^{-1}", &self.inverse, m, m)?;
        shape("H", &self.parameter, r, s)?;
        shape("C", &self.projection, m, m)?;
        shape("L", &self.residual, m, m)?;
        shape("E", &self.image_coordinates, r, k)?;
        shape("F", &self.selection, k, r)?;
        let joined: RowMatrix = self
            .basis
            .iter()
            .zip(&self.complement)
            .map(|(b, n)| b.iter().chain(n).cloned().collect())
            .collect();
        let id = identity(m);
        expect_equal("S S^{-1} = I", &multiply(&joined, &self.inverse, m), &id)?;
        expect_equal("S^{-1} S = I", &multiply(&self.inverse, &joined, m), &id)?;
        if r > 0 {
            expect_equal("B = d0 F", &self.basis, &multiply(&self.d0, &self.selection, r))?;
        }
        if k > 0 {
            let be = if r == 0 {
                vec![vec![Q::zero(); k]; m]
            } else {
                multiply(&self.basis, &self.image_coordinates, k)
            };
            expect_equal("d0 = B E", &self.d0, &be)?;
        }
        let (c, l) =
            splitting_from_parameter(&self.basis, &self.complement, &self.inverse, &self.parameter)?;
        expect_equal("C = B (U + H Q)", &self.projection, &c)?;
        expect_equal("L = (N - B H) Q", &self.residual, &l)?;
        let sum: RowMatrix = c
            .iter()
            .zip(&l)
            .map(|(a, b)| a.iter().zip(b).map(|(x, y)| x + y).collect())
            .collect();
        expect_equal("C + L = I", &sum, &id)?;
        expect_equal("C C = C", &multiply(&c, &c, m), &c)?;
        if k > 0 {
            expect_equal("L d0 = 0", &multiply(&l, &self.d0, k), &vec![vec![Q::zero(); k]; m])?;
        }
        weighted_l1_operator_norm(&l, weights)
    }
}

pub fn verify_transport(t: &[Vec<Q>], c: &[Vec<Q>], c_prime: &[Vec<Q>]) -> Result<()> {
    let m = t.len();
    shape("T", t, m, m)?;
    shape("C", c, m, m)?;
    shape("C'", c_prime, m, m)?;
    expect_equal("T C = C' T", &multiply(t, c, m), &multiply(c_prime, t, m))
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;

    fn q(n: i64, d: i64) -> Q {
        Q::new(BigInt::from(n), BigInt::from(d))
    }
    fn z(n: i64) -> Q {
        q(n, 1)
    }
    fn mat(rows: &[&[i64]]) -> RowMatrix {
        rows.iter().map(|r| r.iter().map(|x| z(*x)).collect()).collect()
    }

    fn line2(h: Q) -> ResidualSplittingCertificate {
        let basis = mat(&[&[1], &[1]]);
        let complement = mat(&[&[0], &[1]]);
        let inverse = mat(&[&[1, 0], &[-1, 1]]);
        let parameter = vec![vec![h]];
        let (projection, residual) =
            splitting_from_parameter(&basis, &complement, &inverse, &parameter).unwrap();
        ResidualSplittingCertificate {
            d0: basis.clone(),
            repair_columns: 1,
            basis,
            complement,
            inverse,
            parameter,
            projection,
            residual,
            image_coordinates: mat(&[&[1]]),
            selection: mat(&[&[1]]),
        }
    }

    #[test]
    fn two_dimensional_splittings_are_contractive() {
        let w = vec![z(1), z(1)];
        let cert = line2(z(0));
        assert_eq!(cert.verify(&w).unwrap(), z(1));
        let cert = line2(q(1, 2));
        assert_eq!(cert.verify(&w).unwrap(), z(1));
        let lx: Vec<Q> = cert.residual.iter().map(|r| &r[0] * z(3) + &r[1] * z(1)).collect();
        assert_eq!(lx, vec![z(1), z(-1)]);
        let cert = line2(z(1));
        assert_eq!(cert.verify(&w).unwrap(), z(1));
        let lx: Vec<Q> = cert.residual.iter().map(|r| &r[0] * z(3) + &r[1] * z(1)).collect();
        assert_eq!(lx, vec![z(2), z(0)]);
        assert_eq!(line2(z(2)).verify(&w).unwrap(), z(3));
    }

    #[test]
    fn tampered_certificates_name_the_failed_identity() {
        let w = vec![z(1), z(1)];
        let mut cert = line2(q(1, 2));
        cert.residual[0][0] = z(0);
        assert!(matches!(
            cert.verify(&w),
            Err(ResidualSplittingError::IdentityFails { identity: "L = (N - B H) Q", .. })
        ));
        let mut cert = line2(q(1, 2));
        cert.inverse[1][0] = z(0);
        assert!(matches!(
            cert.verify(&w),
            Err(ResidualSplittingError::IdentityFails { identity: "S S^{-1} = I", .. })
        ));
        let mut cert = line2(z(0));
        cert.d0 = mat(&[&[1], &[2]]);
        assert!(matches!(
            cert.verify(&w),
            Err(ResidualSplittingError::IdentityFails { identity: "B = d0 F", .. })
        ));
        assert!(matches!(
            line2(z(0)).verify(&[z(1), z(0)]),
            Err(ResidualSplittingError::NonPositiveWeight { index: 1 })
        ));
    }

    #[test]
    fn extreme_images() {
        let id = mat(&[&[1, 0], &[0, 1]]);
        let full = ResidualSplittingCertificate {
            d0: id.clone(),
            repair_columns: 2,
            basis: id.clone(),
            complement: vec![vec![], vec![]],
            inverse: id.clone(),
            parameter: vec![vec![], vec![]],
            projection: id.clone(),
            residual: mat(&[&[0, 0], &[0, 0]]),
            image_coordinates: id.clone(),
            selection: id.clone(),
        };
        assert_eq!(full.verify(&[z(1), z(5)]).unwrap(), z(0));
        let zero = ResidualSplittingCertificate {
            d0: vec![vec![], vec![]],
            repair_columns: 0,
            basis: vec![vec![], vec![]],
            complement: id.clone(),
            inverse: id.clone(),
            parameter: vec![],
            projection: mat(&[&[0, 0], &[0, 0]]),
            residual: id.clone(),
            image_coordinates: vec![],
            selection: vec![],
        };
        assert_eq!(zero.verify(&[z(1), z(5)]).unwrap(), z(1));
    }

    #[test]
    fn weighted_norm_and_transport() {
        assert_eq!(
            weighted_l1_operator_norm(&mat(&[&[1, 0], &[2, 1]]), &[z(1), z(3)]).unwrap(),
            z(7)
        );
        assert_eq!(weighted_l1_operator_norm(&[], &[]).unwrap(), z(0));
        let t = mat(&[&[0, 1], &[1, 0]]);
        let c0 = line2(z(0)).projection;
        let c1 = line2(z(1)).projection;
        assert!(verify_transport(&t, &c0, &c1).is_ok());
        assert!(matches!(
            verify_transport(&t, &c0, &c0),
            Err(ResidualSplittingError::IdentityFails { .. })
        ));
    }
}
