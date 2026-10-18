//! Exact first-order lift/repair for the MUB(6) tangent-obstruction complex, over the
//! native field `Q(zeta_24)`.
//!
//! Increment 4 of the real deformation algebra: the actual repair experiment. Given a
//! candidate fourth vector `v` with curvature residual `omega(v)`, we try to **kill the
//! residual with a first-order deformation** — solve the exact linear system
//!
//! ```text
//!     J . delta_v = -omega(v),     J = d0 (the linearized-MU Jacobian).
//! ```
//!
//! because `omega(v + delta_v) = omega(v) + J . delta_v + O(|delta_v|^2)`. A solution
//! `delta_v` (a "lift") exists **iff** `omega(v) in im(d0)`, i.e. iff its class in the
//! obstruction quotient `C^1 / im(d0)` vanishes. This is the linear-carrier analogue of
//! the `omega_lifts` lift gate (the graph `lift_gate` does not apply to a Jacobian
//! carrier, but the question — does the obstruction descend? — is the same), with a
//! `LiftRepair` verdict mirroring `Accepted` / `Refused`.
//!
//! Two exact facts the verdict rests on:
//! * `im(d0) subset ker(d1)` (the Bianchi identity), so any curvature target violating the
//!   linearized Bianchi closure is **refused** outright — a provable obstruction.
//! * when accepted, the returned `delta_v` is verified to satisfy `J . delta_v = -omega`
//!   exactly in `Cyc24` — the repair genuinely cancels the residual to first order.
//!
//! reducibility at a non-critical point is expected and does not produce a fourth vector;
//! the global obstruction is the Invariant-Systems wall (no first-order descent at the
//! critical maximizer). The second-order Kuranishi obstruction and the global/invariance
//! argument are subsequent increments.

use crate::omega_native::exact::d6_exact_curvature_cochain::{curvature_c2, ExactVec};
use crate::omega_native::exact::d6_exact_tangent_obstruction::curvature_jacobian;
use omega_number_theory::cyclotomic::Cyc24;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum SolveError {
    DimensionMismatch {
        matrix_rows: usize,
        rhs_len: usize,
    },
    EmptyMatrixNonEmptyRhs,
    RaggedMatrix {
        row: usize,
        expected_cols: usize,
        actual_cols: usize,
    },
    ResidualReplayFailed,
}

impl std::fmt::Display for SolveError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::DimensionMismatch {
                matrix_rows,
                rhs_len,
            } => {
                write!(
                    f,
                    "matrix row count {matrix_rows} does not match RHS length {rhs_len}"
                )
            }
            Self::EmptyMatrixNonEmptyRhs => {
                write!(f, "empty matrix provided with non-empty RHS")
            }
            Self::RaggedMatrix {
                row,
                expected_cols,
                actual_cols,
            } => {
                write!(f, "ragged matrix at row {row}: expected {expected_cols} columns, found {actual_cols}")
            }
            Self::ResidualReplayFailed => {
                write!(f, "residual verification failed: exact replay A * x != b")
            }
        }
    }
}

impl std::error::Error for SolveError {}

/// Solve `A x = b` exactly over `Q(zeta_24)`. Validates matrix shape and RHS length before elimination.
/// Returns `Ok(Some(x))` (verified exact solution `A x = b`), `Ok(None)` if the system is inconsistent,
/// or `Err(SolveError)` if matrix/RHS dimensions are invalid or replay fails.
pub fn solve_exact(a: &[Vec<Cyc24>], b: &[Cyc24]) -> Result<Option<Vec<Cyc24>>, SolveError> {
    let nrows = a.len();
    let rhs_len = b.len();
    if nrows == 0 {
        if rhs_len == 0 {
            return Ok(Some(Vec::new()));
        } else {
            return Err(SolveError::EmptyMatrixNonEmptyRhs);
        }
    }
    if nrows != rhs_len {
        return Err(SolveError::DimensionMismatch {
            matrix_rows: nrows,
            rhs_len,
        });
    }
    let ncols = a[0].len();
    for (r_idx, row) in a.iter().enumerate() {
        if row.len() != ncols {
            return Err(SolveError::RaggedMatrix {
                row: r_idx,
                expected_cols: ncols,
                actual_cols: row.len(),
            });
        }
    }

    // Augmented matrix [A | b].
    let mut m: Vec<Vec<Cyc24>> = a
        .iter()
        .zip(b.iter())
        .map(|(row, bi)| {
            let mut r = row.clone();
            r.push(bi.clone());
            r
        })
        .collect();

    // Reduced row echelon form over the field; record pivot columns.
    let mut pivot_cols: Vec<usize> = Vec::new();
    let mut pr = 0usize;
    for col in 0..ncols {
        if pr >= nrows {
            break;
        }
        let piv = (pr..nrows).find(|&r| !m[r][col].is_zero());
        if let Some(piv) = piv {
            m.swap(pr, piv);
            let inv = m[pr][col].inv();
            for c in col..=ncols {
                m[pr][c] = m[pr][c].mul(&inv);
            }
            for r in 0..nrows {
                if r != pr && !m[r][col].is_zero() {
                    let f = m[r][col].clone();
                    for c in col..=ncols {
                        let t = f.mul(&m[pr][c]);
                        m[r][c] = m[r][c].sub(&t);
                    }
                }
            }
            pivot_cols.push(col);
            pr += 1;
        }
    }

    // Consistency: a row with zero A-part but nonzero b-part is `0 = nonzero`.
    for row in &m {
        let a_zero = row[..ncols].iter().all(|z| z.is_zero());
        if a_zero && !row[ncols].is_zero() {
            return Ok(None);
        }
    }

    // Particular solution: free variables = 0; pivot variable = its row's RHS.
    let mut x = vec![Cyc24::zero(); ncols];
    for (i, &col) in pivot_cols.iter().enumerate() {
        x[col] = m[i][ncols].clone();
    }

    // Replay A x = b in exact arithmetic
    for (i, row) in a.iter().enumerate() {
        let mut ax_i = Cyc24::zero();
        for (j, a_ij) in row.iter().enumerate() {
            ax_i = ax_i.add(&a_ij.mul(&x[j]));
        }
        if ax_i != b[i] {
            return Err(SolveError::ResidualReplayFailed);
        }
    }

    Ok(Some(x))
}

/// The verdict of the first-order lift/repair attempt at a candidate vector.
pub struct LiftRepair {
    /// `true` iff a first-order deformation cancels the curvature residual
    /// (`omega in im(d0)`).
    pub accepted: bool,
    /// The repair deformation `delta_v in R^12` (verified `J . delta_v = -omega`), if any.
    pub repair: Option<Vec<Cyc24>>,
}

/// Attempt to repair the curvature residual at `v` by a first-order deformation.
pub fn lift_repair(columns: &[ExactVec], v: &ExactVec) -> LiftRepair {
    let j = curvature_jacobian(columns, v);
    let neg_omega: Vec<Cyc24> = curvature_c2(columns, v).iter().map(|w| w.neg()).collect();
    match solve_exact(&j, &neg_omega) {
        Ok(Some(dv)) => LiftRepair {
            accepted: true,
            repair: Some(dv),
        },
        _ => LiftRepair {
            accepted: false,
            repair: None,
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, COLUMN_COUNT};
    use crate::omega_native::exact::d6_exact_tangent_obstruction::{mat_vec, REAL_DIM};
    use omega_number_theory::cyclotomic::Cyc24;
    use omega_number_theory::rational::ri;

    fn rat(num: i64, den: i64) -> Cyc24 {
        Cyc24::rat(ri(num) / ri(den))
    }

    fn generic_unit() -> ExactVec {
        let s = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3)).mul(&rat(1, 2)); // 1/sqrt2
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = s.clone();
        v[1] = Cyc24::zeta24(6).mul(&s);
        v
    }

    #[test]
    fn image_target_is_solved_exactly() {
        // b = J . dv0 is in im(J); the solver must return some x with J x = b exactly.
        let cols = canonical_triple_exact();
        let v = generic_unit();
        let j = curvature_jacobian(&cols, &v);
        let mut dv0 = vec![Cyc24::zero(); REAL_DIM];
        dv0[0] = Cyc24::rat(ri(3));
        dv0[5] = rat(-2, 7);
        let b = mat_vec(&j, &dv0).expect("jacobian row width matches the direction");
        let x = solve_exact(&j, &b)
            .expect("well-shaped solve")
            .expect("an image target must be solvable");
        assert_eq!(
            mat_vec(&j, &x).expect("jacobian row width matches the solution"),
            b,
            "J x must equal b exactly"
        );
    }

    #[test]
    fn bianchi_violating_target_is_refused() {
        // A target supported on a single B1 constraint violates the linearized Bianchi
        // closure (B1 sum = 1, B2/B3 sums = 0), so it is NOT in im(d0) = subset of ker(d1).
        let cols = canonical_triple_exact();
        let j = curvature_jacobian(&cols, &generic_unit());
        let mut b = vec![Cyc24::zero(); COLUMN_COUNT];
        b[0] = Cyc24::rat(ri(1));
        assert!(
            solve_exact(&j, &b).expect("well-shaped solve").is_none(),
            "a Bianchi-violating curvature target must be refused (not in im d0)"
        );
    }

    #[test]
    fn test_extra_rhs_entry_returns_dimension_mismatch() {
        let a = vec![vec![Cyc24::zero()]];
        let b = vec![Cyc24::zero(), Cyc24::rat(ri(1))];
        assert_eq!(
            solve_exact(&a, &b),
            Err(SolveError::DimensionMismatch {
                matrix_rows: 1,
                rhs_len: 2
            })
        );
    }

    #[test]
    fn test_short_rhs_returns_dimension_mismatch() {
        let a = vec![vec![Cyc24::rat(ri(1))], vec![Cyc24::zero()]];
        let b = vec![Cyc24::zero()];
        assert_eq!(
            solve_exact(&a, &b),
            Err(SolveError::DimensionMismatch {
                matrix_rows: 2,
                rhs_len: 1
            })
        );
    }

    #[test]
    fn test_empty_matrix_non_empty_rhs_returns_error() {
        let a: Vec<Vec<Cyc24>> = vec![];
        let b = vec![Cyc24::rat(ri(1))];
        assert_eq!(solve_exact(&a, &b), Err(SolveError::EmptyMatrixNonEmptyRhs));
    }

    #[test]
    fn test_ragged_matrix_returns_ragged_error() {
        let a = vec![vec![Cyc24::rat(ri(1)), Cyc24::zero()], vec![Cyc24::zero()]];
        let b = vec![Cyc24::zero(), Cyc24::rat(ri(1))];
        assert_eq!(
            solve_exact(&a, &b),
            Err(SolveError::RaggedMatrix {
                row: 1,
                expected_cols: 2,
                actual_cols: 1
            })
        );
    }

    #[test]
    fn lift_repair_when_accepted_cancels_residual_exactly() {
        let cols = canonical_triple_exact();
        let v = generic_unit();
        let report = lift_repair(&cols, &v);
        if report.accepted {
            let j = curvature_jacobian(&cols, &v);
            let repair = report
                .repair
                .expect("accepted lift carries a repair direction");
            let neg_omega: Vec<Cyc24> = curvature_c2(&cols, &v).iter().map(|w| w.neg()).collect();
            assert_eq!(
                mat_vec(&j, &repair).expect("jacobian row width matches the repair"),
                neg_omega,
                "the repair must cancel the residual to first order exactly"
            );
        }
    }
}
