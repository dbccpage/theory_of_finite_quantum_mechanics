//! Stage 018 / Integral Homology: Smith Normal Form & Torsion Extraction over Z.
//!
//! AuthorityEffect: None. GenesisEffect: None.
//!
//! Mechanically computes:
//! 1. Smith Normal Form (SNF) of integer boundary matrices over the principal ideal domain Z:
//!    D_k = P_k * A_k * Q_k = diag(d_1, d_2, ..., d_r, 0, ..., 0)
//!    with d_1 | d_2 | ... | d_r >= 1 and det(P_k) = +/- 1, det(Q_k) = +/- 1.
//! 2. Integral homology decomposition:
//!    H_k(K; Z) \cong Z^{\beta_k} \oplus \bigoplus_{i=1}^{r_{k+1}} (Z / d_{i, k+1} Z).
//! 3. Extraction of finite torsion invariants, distinguishing torsion-free complexes (T^2, S^2)
//!    from torsion-bearing non-orientable manifolds (RP^2, K^2).

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct IntegralHomologyReceipt {
    pub complex_name: String,
    pub dimension: usize,
    pub betti_number: usize,
    pub invariant_factors: Vec<i64>,
    pub torsion_subgroups: Vec<String>,
    pub is_torsion_free: bool,
    pub status: String, // "PASS"
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IntegerMatrix {
    pub rows: usize,
    pub cols: usize,
    pub data: Vec<Vec<i64>>,
}

impl IntegerMatrix {
    pub fn new(rows: usize, cols: usize) -> Self {
        Self {
            rows,
            cols,
            data: vec![vec![0; cols]; rows],
        }
    }

    pub fn from_dense(rows: usize, cols: usize, flat: &[i64]) -> Self {
        assert_eq!(rows * cols, flat.len());
        let mut data = vec![vec![0; cols]; rows];
        for r in 0..rows {
            for c in 0..cols {
                data[r][c] = flat[r * cols + c];
            }
        }
        Self { rows, cols, data }
    }

    pub fn mul(&self, rhs: &Self) -> Self {
        assert_eq!(self.cols, rhs.rows);
        let mut out = Self::new(self.rows, rhs.cols);
        for i in 0..self.rows {
            for k in 0..self.cols {
                if self.data[i][k] != 0 {
                    for j in 0..rhs.cols {
                        out.data[i][j] += self.data[i][k] * rhs.data[k][j];
                    }
                }
            }
        }
        out
    }

    pub fn is_zero(&self) -> bool {
        self.data.iter().all(|row| row.iter().all(|&x| x == 0))
    }

    /// Compute Smith Normal Form over Z.
    /// Returns sorted positive invariant factors [d_1, d_2, ..., d_r] satisfying d_i | d_{i+1}.
    pub fn smith_normal_form(&self) -> Vec<i64> {
        if self.rows == 0 || self.cols == 0 {
            return Vec::new();
        }

        let mut a = self.data.clone();
        let m = self.rows;
        let n = self.cols;
        let mut r = 0;

        for step in 0..m.min(n) {
            // Find pivot with smallest non-zero absolute value
            loop {
                let mut pivot_pos = None;
                let mut min_abs = i64::MAX;

                for i in step..m {
                    for j in step..n {
                        let val = a[i][j].abs();
                        if val > 0 && val < min_abs {
                            min_abs = val;
                            pivot_pos = Some((i, j));
                        }
                    }
                }

                let (p_row, p_col) = match pivot_pos {
                    Some(pos) => pos,
                    None => break, // All remaining entries are 0
                };

                // Swap pivot to (step, step)
                a.swap(step, p_row);
                for row in 0..m {
                    a[row].swap(step, p_col);
                }

                // Make pivot positive
                if a[step][step] < 0 {
                    for col in step..n {
                        a[step][col] = -a[step][col];
                    }
                }

                let pivot = a[step][step];
                let mut changed = false;

                // Eliminate row entries in column step
                for i in (step + 1)..m {
                    if a[i][step] != 0 {
                        let q = a[i][step] / pivot;
                        for j in step..n {
                            a[i][j] -= q * a[step][j];
                        }
                        if a[i][step] != 0 {
                            changed = true;
                        }
                    }
                }

                // Eliminate col entries in row step
                for j in (step + 1)..n {
                    if a[step][j] != 0 {
                        let q = a[step][j] / pivot;
                        for i in step..m {
                            a[i][j] -= q * a[i][step];
                        }
                        if a[step][j] != 0 {
                            changed = true;
                        }
                    }
                }

                if !changed {
                    break;
                }
            }

            if a[step][step] != 0 {
                if a[step][step] < 0 {
                    a[step][step] = -a[step][step];
                }
                r = step + 1;
            } else {
                break;
            }
        }

        // Collect diagonal non-zero elements
        let mut d = Vec::new();
        for i in 0..r {
            if a[i][i] > 0 {
                d.push(a[i][i]);
            }
        }

        // Enforce divisibility d_i | d_{i+1} via gcd reductions
        for i in 0..d.len() {
            for j in (i + 1)..d.len() {
                let g = gcd(d[i], d[j]);
                let l = (d[i] / g) * d[j];
                d[i] = g;
                d[j] = l;
            }
        }

        d
    }
}

fn gcd(mut a: i64, mut b: i64) -> i64 {
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a.abs()
}

/// Compute exact integral homology H_k(K; Z) from boundary operators A_k and A_{k+1}.
/// Verifies nilpotence: A_k * A_{k+1} = 0.
pub fn compute_integral_homology(
    complex_name: &str,
    k: usize,
    a_k: &IntegerMatrix,
    a_kp1: &IntegerMatrix,
) -> Result<IntegralHomologyReceipt, String> {
    // 1. Verify chain nilpotence: d_k \circ d_{k+1} = 0
    let prod = a_k.mul(a_kp1);
    if !prod.is_zero() {
        return Err(format!(
            "Boundary nilpotence violation: partial_{} * partial_{} != 0",
            k,
            k + 1
        ));
    }

    let n_k = a_k.cols; // Rank of C_k
    assert_eq!(
        n_k, a_kp1.rows,
        "Chain complex dimension mismatch: C_k generation mismatch"
    );

    let d_k = a_k.smith_normal_form();
    let r_k = d_k.len(); // rank(A_k)

    let d_kp1 = a_kp1.smith_normal_form();
    let r_kp1 = d_kp1.len(); // rank(A_{k+1})

    // Betti number: \beta_k = n_k - rank(A_k) - rank(A_{k+1})
    let betti = n_k
        .checked_sub(r_k + r_kp1)
        .ok_or_else(|| "Rank sum exceeds chain dimension".to_string())?;

    // Torsion subgroups: invariant factors d_{i, k+1} > 1
    let mut torsion = Vec::new();
    for &d in &d_kp1 {
        if d > 1 {
            torsion.push(format!("Z/{}Z", d));
        }
    }

    let is_torsion_free = torsion.is_empty();

    Ok(IntegralHomologyReceipt {
        complex_name: complex_name.to_string(),
        dimension: k,
        betti_number: betti,
        invariant_factors: d_kp1,
        torsion_subgroups: torsion,
        is_torsion_free,
        status: "PASS".to_string(),
    })
}
