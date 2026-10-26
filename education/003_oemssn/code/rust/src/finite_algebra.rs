//! Finite determinant, signed-pair, and Gaussian-rational matrix algebra.
//! AuthorityEffect: None. Arithmetic is limited by the integer representations.
//! No causal triangulation, sign-problem solution, or M-theory model is implemented.

use num_rational::Rational64;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

use crate::exact_linear_algebra::GaussianRational;

// =========================================================================
// 1. Bareiss Fraction-Free Determinant (Exact Integer Determinants)
// =========================================================================

/// Computes the exact determinant of an n x n integer matrix using the
/// fraction-free Bareiss algorithm (1968), avoiding all floating-point rounding.
pub fn bareiss_determinant(matrix: &[Vec<i64>]) -> Result<i64, String> {
    let n = matrix.len();
    if n == 0 {
        return Ok(1);
    }
    for row in matrix {
        if row.len() != n {
            return Err(format!("Matrix is not square: expected {}x{}, got row length {}", n, n, row.len()));
        }
    }
    if n == 1 {
        return Ok(matrix[0][0]);
    }

    let mut m: Vec<Vec<i128>> = matrix
        .iter()
        .map(|r| r.iter().map(|&v| v as i128).collect())
        .collect();

    let mut sign: i128 = 1;
    let mut prev_pivot: i128 = 1;

    for k in 0..n - 1 {
        // Pivot selection
        if m[k][k] == 0 {
            let mut swap_row = None;
            for r in k + 1..n {
                if m[r][k] != 0 {
                    swap_row = Some(r);
                    break;
                }
            }
            match swap_row {
                Some(r) => {
                    m.swap(k, r);
                    sign = -sign;
                }
                None => {
                    // Entire column below pivot is zero -> det is 0
                    return Ok(0);
                }
            }
        }

        let pivot = m[k][k];

        for i in k + 1..n {
            for j in k + 1..n {
                let left = m[i][j].checked_mul(pivot).ok_or("Bareiss intermediate overflow")?;
                let right = m[i][k].checked_mul(m[k][j]).ok_or("Bareiss intermediate overflow")?;
                let num = left.checked_sub(right).ok_or("Bareiss intermediate overflow")?;
                m[i][j] = num / prev_pivot;
            }
        }
        prev_pivot = pivot;
    }

    let det = sign * m[n - 1][n - 1];
    if det > i64::MAX as i128 || det < i64::MIN as i128 {
        return Err("Determinant overflowed i64".to_string());
    }
    Ok(det as i64)
}

// =========================================================================
// 3. Finite sign-reversing involution checks
// =========================================================================

/// Configuration carrying rational action and a fermion sign.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SignedPathConfiguration {
    pub config_id: usize,
    pub action: Rational64,
    pub fermion_sign: i8, // +1 or -1
    pub mode_postings: Vec<String>,
}

/// Receipt confirming exact sign cancellation via involution pairing.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct InvolutionPairingReceipt {
    pub total_configurations: usize,
    pub paired_count: usize,
    pub net_fermion_sign: i64,
    pub cancellation_certified: bool,
    pub average_sign: Rational64,
}

/// Verifies that an involution witness Xi(C) pairs positive and negative paths in exact bijection:
/// Xi(Xi(C)) = C, Xi(C) != C, S(Xi(C)) == S(C), sgn(Xi(C)) == -sgn(C).
pub fn verify_bqnf_involution_pairing(
    configs: &[SignedPathConfiguration],
    involution: &BTreeMap<usize, usize>,
) -> Result<InvolutionPairingReceipt, String> {
    if configs.is_empty() { return Err("Empty ensemble has no average sign".into()); }
    if involution.len() != configs.len() { return Err("Involution support differs from ensemble".into()); }
    let mut config_map: BTreeMap<usize, &SignedPathConfiguration> = BTreeMap::new();
    for c in configs {
        if c.fermion_sign != 1 && c.fermion_sign != -1 { return Err("Sign must be +1 or -1".into()); }
        if config_map.insert(c.config_id, c).is_some() { return Err("Duplicate configuration ID".into()); }
    }

    let mut paired_count = 0;
    let mut net_sign: i64 = 0;

    for c in configs {
        net_sign += c.fermion_sign as i64;

        let partner_id = match involution.get(&c.config_id) {
            Some(&pid) => pid,
            None => return Err(format!("Configuration {} missing involution partner in Xi", c.config_id)),
        };

        if partner_id == c.config_id {
            return Err(format!("Involution has fixed point at configuration {}", c.config_id));
        }

        let partner = match config_map.get(&partner_id) {
            Some(p) => *p,
            None => return Err(format!("Partner ID {} does not exist in configuration ensemble", partner_id)),
        };

        // Check involution symmetry: Xi(Xi(C)) = C
        let back_id = match involution.get(&partner_id) {
            Some(&bid) => bid,
            None => return Err(format!("Partner {} missing reciprocal involution edge", partner_id)),
        };
        if back_id != c.config_id {
            return Err(format!("Involution fails reflexivity: Xi(Xi({})) = {} != {}", c.config_id, back_id, c.config_id));
        }

        // Check action invariance: S(Xi(C)) == S(C)
        if partner.action != c.action {
            return Err(format!(
                "Involution alters action: S({}) = {} != S({}) = {}",
                c.config_id, c.action, partner_id, partner.action
            ));
        }

        // Check sign reversal: sgn(Xi(C)) == -sgn(C)
        if partner.fermion_sign != -c.fermion_sign {
            return Err(format!(
                "Involution does not reverse sign: sgn({}) = {}, sgn({}) = {}",
                c.config_id, c.fermion_sign, partner_id, partner.fermion_sign
            ));
        }

        paired_count += 1;
    }

    let cancellation_certified = net_sign == 0 && paired_count == configs.len();
    let average_sign = if cancellation_certified {
        Rational64::new(0, 1) // Opposite equal-weight contributions cancel; their average sign is zero.
    } else {
        Rational64::new(net_sign.abs(), configs.len() as i64)
    };

    Ok(InvolutionPairingReceipt {
        total_configurations: configs.len(),
        paired_count,
        net_fermion_sign: net_sign,
        cancellation_certified,
        average_sign: average_sign,
    })
}

// =========================================================================
// 4. Finite matrices and commutators
// =========================================================================

/// Exact N x N matrix over Gaussian rationals Q(i).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GaussianMatrix {
    pub n: usize,
    pub data: Vec<Vec<GaussianRational>>,
}

impl GaussianMatrix {
    pub fn new(n: usize, data: Vec<Vec<GaussianRational>>) -> Self {
        assert_eq!(data.len(), n);
        for row in &data {
            assert_eq!(row.len(), n);
        }
        Self { n, data }
    }

    pub fn zero(n: usize) -> Self {
        let data = vec![vec![GaussianRational::zero(); n]; n];
        Self { n, data }
    }

    pub fn identity(n: usize) -> Self {
        let mut mat = Self::zero(n);
        for idx in 0..n {
            mat.data[idx][idx] = GaussianRational::one();
        }
        mat
    }

    pub fn add(&self, other: &Self) -> Self {
        assert_eq!(self.n, other.n);
        let mut out = Self::zero(self.n);
        for r in 0..self.n {
            for c in 0..self.n {
                out.data[r][c] = self.data[r][c].add(&other.data[r][c]);
            }
        }
        out
    }

    pub fn sub(&self, other: &Self) -> Self {
        assert_eq!(self.n, other.n);
        let mut out = Self::zero(self.n);
        for r in 0..self.n {
            for c in 0..self.n {
                out.data[r][c] = self.data[r][c].sub(&other.data[r][c]);
            }
        }
        out
    }

    pub fn mul(&self, other: &Self) -> Self {
        assert_eq!(self.n, other.n);
        let mut out = Self::zero(self.n);
        for r in 0..self.n {
            for c in 0..self.n {
                let mut sum = GaussianRational::zero();
                for k in 0..self.n {
                    let term = self.data[r][k].mul(&other.data[k][c]);
                    sum = sum.add(&term);
                }
                out.data[r][c] = sum;
            }
        }
        out
    }

    /// Matrix commutator: [A, B] = A * B - B * A.
    pub fn commutator(&self, other: &Self) -> Self {
        let ab = self.mul(other);
        let ba = other.mul(self);
        ab.sub(&ba)
    }

    /// Evaluates the Jacobi identity: [A, [B, C]] + [B, [C, A]] + [C, [A, B]].
    pub fn jacobi_sum(&self, b: &Self, c: &Self) -> Self {
        let bc = b.commutator(c);
        let a_bc = self.commutator(&bc);

        let ca = c.commutator(self);
        let b_ca = b.commutator(&ca);

        let ab = self.commutator(b);
        let c_ab = c.commutator(&ab);

        a_bc.add(&b_ca).add(&c_ab)
    }

    pub fn is_zero(&self) -> bool {
        for r in 0..self.n {
            for c in 0..self.n {
                if !self.data[r][c].is_zero() {
                    return false;
                }
            }
        }
        true
    }

    pub fn trace(&self) -> GaussianRational {
        let mut sum = GaussianRational::zero();
        for idx in 0..self.n {
            sum = sum.add(&self.data[idx][idx]);
        }
        sum
    }

    pub fn frobenius_norm_sq(&self) -> Rational64 {
        let mut sum = Rational64::new(0, 1);
        for r in 0..self.n {
            for c in 0..self.n {
                sum = sum + self.data[r][c].norm_sq();
            }
        }
        sum
    }
    /// Computes (1/4) sum_{i<j} ||[X_i,X_j]||_F^2 for supplied equal-size matrices.
    /// This algebraic quantity is not a BFSS/IKKT implementation.
    pub fn quarter_commutator_norm_sum(matrices: &[Self]) -> Rational64 {
        let mut total_trace_sq = Rational64::new(0, 1);
        let m = matrices.len();
        for i in 0..m {
            for j in (i + 1)..m {
                let comm = matrices[i].commutator(&matrices[j]);
                let norm_sq = comm.frobenius_norm_sq();
                total_trace_sq = total_trace_sq + norm_sq;
            }
        }
        total_trace_sq * Rational64::new(1, 4)
    }
}
