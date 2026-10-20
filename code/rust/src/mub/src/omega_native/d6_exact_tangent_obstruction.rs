
use crate::omega_native::exact::d6_exact_curvature_cochain::{inner, ExactVec, COLUMN_COUNT, D};
use num_rational::BigRational;
use num_traits::Zero;
use omega_certifiers::phi1_certifier::Phi1FormCertificate;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;
use omega_policy::trichotomy::ObstructionDiagnosticClass;
use omega_solvers::solver_lp_exact_simplex::{
    solve_weighted_l1_projection, L1LpError, L1ProjectionSolution,
};

pub const REAL_DIM: usize = 2 * D;

fn rat(num: i64, den: i64) -> Cyc24 {
    Cyc24::rat(ri(num) / ri(den))
}

pub fn re(z: &Cyc24) -> Cyc24 {
    z.add(&z.conj()).mul(&rat(1, 2))
}

pub fn im(z: &Cyc24) -> Cyc24 {
    let neg_i_half = Cyc24::zeta24(6).neg().mul(&rat(1, 2));
    z.sub(&z.conj()).mul(&neg_i_half)
}

pub fn curvature_jacobian(columns: &[ExactVec], v: &ExactVec) -> Vec<Vec<Cyc24>> {
    let two = Cyc24::rat(ri(2));
    columns
        .iter()
        .map(|e| {
            let a = inner(e, v);
            let conj_a = a.conj();
            let mut row = vec![Cyc24::zero(); REAL_DIM];
            for k in 0..D {
                let c = conj_a.mul(&e[k].conj());
                row[2 * k] = two.mul(&re(&c));
                row[2 * k + 1] = two.mul(&im(&c)).neg();
            }
            row
        })
        .collect()
}

pub fn phase_gauge_direction(v: &ExactVec) -> Vec<Cyc24> {
    let mut dir = vec![Cyc24::zero(); REAL_DIM];
    for k in 0..D {
        dir[2 * k] = im(&v[k]).neg();
        dir[2 * k + 1] = re(&v[k]);
    }
    dir
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TangentShapeError {
    pub message: &'static str,
}

pub fn mat_vec(j: &[Vec<Cyc24>], dir: &[Cyc24]) -> Result<Vec<Cyc24>, TangentShapeError> {
    j.iter()
        .map(|row| {
            if row.len() != dir.len() {
                return Err(TangentShapeError {
                    message: "matrix row and vector have different lengths",
                });
            }
            let mut acc = Cyc24::zero();
            for (a, b) in row.iter().zip(dir.iter()) {
                acc = acc.add(&a.mul(b));
            }
            Ok(acc)
        })
        .collect()
}

fn validate_rank_matrix_cols(rows: &[Vec<Cyc24>]) -> Result<Option<usize>, TangentShapeError> {
    if rows.is_empty() {
        return Ok(None);
    }
    let ncols = rows[0].len();
    for row in rows {
        if row.len() != ncols {
            return Err(TangentShapeError {
                message: "matrix rows do not have equal length",
            });
        }
    }
    if ncols == 0 {
        return Ok(None);
    }
    Ok(Some(ncols))
}

fn find_rank_pivot_row(m: &[Vec<Cyc24>], pivot_row: usize, col: usize) -> Option<usize> {
    for (r, row) in m.iter().enumerate().skip(pivot_row) {
        if !row[col].is_zero() {
            return Some(r);
        }
    }
    None
}

fn eliminate_rank_column(m: &mut [Vec<Cyc24>], pivot_row: usize, col: usize, ncols: usize) {
    let inv = m[pivot_row][col].inv();
    for c in col..ncols {
        m[pivot_row][c] = m[pivot_row][c].mul(&inv);
    }
    for r in 0..m.len() {
        if r != pivot_row && !m[r][col].is_zero() {
            let factor = m[r][col].clone();
            for c in col..ncols {
                let t = factor.mul(&m[pivot_row][c]);
                m[r][c] = m[r][c].sub(&t);
            }
        }
    }
}

pub fn rank_cyc24(rows: &[Vec<Cyc24>]) -> Result<usize, TangentShapeError> {
    let Some(ncols) = validate_rank_matrix_cols(rows)? else {
        return Ok(0);
    };
    let nrows = rows.len();
    let mut m: Vec<Vec<Cyc24>> = rows.to_vec();
    let mut rank = 0usize;
    let mut pivot_row = 0usize;
    for col in 0..ncols {
        if pivot_row >= nrows {
            break;
        }
        if let Some(piv) = find_rank_pivot_row(&m, pivot_row, col) {
            m.swap(pivot_row, piv);
            eliminate_rank_column(&mut m, pivot_row, col, ncols);
            pivot_row += 1;
            rank += 1;
        }
    }
    Ok(rank)
}

pub struct TangentObstruction {
    pub jacobian_rank: usize,
    pub obstruction_dim: usize,
    pub phase_gauge_in_kernel: bool,
}

pub fn tangent_obstruction(
    columns: &[ExactVec],
    v: &ExactVec,
) -> Result<TangentObstruction, TangentShapeError> {
    if columns.len() != COLUMN_COUNT {
        return Err(TangentShapeError {
            message: "tangent obstruction expects the 18 fixed vectors of the triple",
        });
    }
    let j = curvature_jacobian(columns, v);
    if j.len() != COLUMN_COUNT || j.iter().any(|row| row.len() != REAL_DIM) {
        return Err(TangentShapeError {
            message: "jacobian is not an 18 by 12 matrix",
        });
    }
    let rank = rank_cyc24(&j)?;
    let phase = phase_gauge_direction(v);
    let jp = mat_vec(&j, &phase)?;
    let phase_in_ker = jp.iter().all(|z| z.is_zero());
    Ok(TangentObstruction {
        jacobian_rank: rank,
        obstruction_dim: j.len() - rank,
        phase_gauge_in_kernel: phase_in_ker,
    })
}

pub fn bianchi_d1_q() -> Vec<Vec<BigRational>> {
    let one = BigRational::from_integer(1.into());
    let neg_one = -BigRational::from_integer(1.into());
    let mut row0 = vec![BigRational::zero(); COLUMN_COUNT];
    let mut row1 = vec![BigRational::zero(); COLUMN_COUNT];
    for i in 0..D {
        row0[i] = one.clone();
        row1[i] = one.clone();
    }
    for i in D..2 * D {
        row0[i] = neg_one.clone();
    }
    for i in 2 * D..3 * D {
        row1[i] = neg_one.clone();
    }
    vec![row0, row1]
}

pub fn evaluate_bianchi_d1_q(z: &[BigRational]) -> Result<[BigRational; 2], TangentShapeError> {
    if z.len() != COLUMN_COUNT {
        return Err(TangentShapeError {
            message: "Bianchi input must have 18 coordinates",
        });
    }
    let mut s1 = BigRational::zero();
    let mut s2 = BigRational::zero();
    let mut s3 = BigRational::zero();
    for i in 0..D {
        s1 += &z[i];
    }
    for i in D..2 * D {
        s2 += &z[i];
    }
    for i in 2 * D..3 * D {
        s3 += &z[i];
    }
    Ok([&s1 - &s2, s1 - s3])
}

pub fn classify_tangent_obstruction(
    residual: &[BigRational],
) -> Result<ObstructionDiagnosticClass, TangentShapeError> {
    if residual.len() != COLUMN_COUNT {
        return Err(TangentShapeError {
            message: "tangent residual must have 18 coordinates",
        });
    }
    let is_zero = residual.iter().all(|x| x.is_zero());
    if is_zero {
        return Ok(ObstructionDiagnosticClass::ExactRepair);
    }
    let b = evaluate_bianchi_d1_q(residual)?;
    Ok(if b[0].is_zero() && b[1].is_zero() {
        ObstructionDiagnosticClass::ClosedResidual
    } else {
        ObstructionDiagnosticClass::ActiveClosureFailure
    })
}

pub fn classify_tangent_obstruction_dvector(
    residual: &nalgebra::DVector<BigRational>,
) -> Result<ObstructionDiagnosticClass, TangentShapeError> {
    let slice: Vec<BigRational> = residual.iter().cloned().collect();
    classify_tangent_obstruction(&slice)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TangentObstructionDiagnosticReport {
    pub diagnostic_class: ObstructionDiagnosticClass,
    pub l1_solution: L1ProjectionSolution,
    pub bianchi_residual: [BigRational; 2],
    pub phi1_certified_value: BigRational,
}

pub fn solve_and_classify_tangent_complex(
    target: &[BigRational],
    weights: &[BigRational],
    d0_rows: &[Vec<BigRational>],
    iteration_budget: usize,
) -> Result<TangentObstructionDiagnosticReport, L1LpError> {
    let solution = solve_weighted_l1_projection(target, weights, d0_rows, iteration_budget)?;
    let diagnostic_class = classify_tangent_obstruction(&solution.residual).map_err(|_| {
        L1LpError::DimensionMismatch {
            target: solution.residual.len(),
            rows: COLUMN_COUNT,
        }
    })?;
    let bianchi_residual =
        evaluate_bianchi_d1_q(&solution.residual).map_err(|_| L1LpError::DimensionMismatch {
            target: solution.residual.len(),
            rows: COLUMN_COUNT,
        })?;

    let k = d0_rows.first().map(Vec::len).unwrap_or(0);
    let mut coboundaries = Vec::with_capacity(k);
    for j in 0..k {
        let col: Vec<BigRational> = d0_rows.iter().map(|row| row[j].clone()).collect();
        coboundaries.push(col);
    }
    let cert = Phi1FormCertificate {
        weights: weights.to_vec(),
        residual_at_achiever: solution.residual.clone(),
        dual: solution.dual.clone(),
        coboundaries,
    };
    let certified_val = cert.verify().map_err(|_| L1LpError::Unbounded)?;

    Ok(TangentObstructionDiagnosticReport {
        diagnostic_class,
        l1_solution: solution,
        bianchi_residual,
        phi1_certified_value: certified_val,
    })
}

fn cyc24_row_to_rational(row: Vec<Cyc24>) -> Option<Vec<BigRational>> {
    let mut q_row = Vec::with_capacity(row.len());
    for entry in row {
        if entry.a[1..].iter().all(BigRational::is_zero) {
            q_row.push(entry.a[0].clone());
        } else {
            return None;
        }
    }
    Some(q_row)
}

pub fn curvature_jacobian_q(columns: &[ExactVec], v: &ExactVec) -> Option<Vec<Vec<BigRational>>> {
    let j = curvature_jacobian(columns, v);
    let mut out = Vec::with_capacity(j.len());
    for row in j {
        out.push(cyc24_row_to_rational(row)?);
    }
    Some(out)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::exact::d6_exact_curvature_cochain::canonical_triple_exact;

    fn unit_e0() -> ExactVec {
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = Cyc24::rat(ri(1));
        v
    }

    fn generic_unit() -> ExactVec {
        let s = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3)).mul(&rat(1, 2));
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = s.clone();
        v[1] = Cyc24::zeta24(6).mul(&s);
        v
    }

    #[test]
    fn re_im_are_exact() {
        let i = Cyc24::zeta24(6);
        assert!(re(&i).is_zero());
        assert_eq!(im(&i), Cyc24::rat(ri(1)));
        let one = Cyc24::rat(ri(1));
        assert_eq!(re(&one), one);
        assert!(im(&one).is_zero());
    }

    #[test]
    fn jacobian_has_full_shape() {
        let cols = canonical_triple_exact();
        let j = curvature_jacobian(&cols, &generic_unit());
        assert_eq!(j.len(), COLUMN_COUNT);
        assert!(j.iter().all(|row| row.len() == REAL_DIM));
    }

    #[test]
    fn phase_gauge_is_exactly_in_the_kernel() {
        let cols = canonical_triple_exact();
        for v in [unit_e0(), generic_unit()] {
            let j = curvature_jacobian(&cols, &v);
            let jp = mat_vec(&j, &phase_gauge_direction(&v)).expect("jacobian shape");
            assert!(
                jp.iter().all(|z| z.is_zero()),
                "phase gauge i*v must lie exactly in ker(J)"
            );
        }
    }

    #[test]
    fn obstruction_is_large_due_to_overdetermination() {
        let cols = canonical_triple_exact();
        let report = tangent_obstruction(&cols, &generic_unit()).expect("18 fixed vectors");
        assert!(report.phase_gauge_in_kernel);
        assert!(
            report.jacobian_rank <= 11,
            "ambient rank {} exceeds 11 after the phase gauge",
            report.jacobian_rank
        );
        assert!(
            report.obstruction_dim >= 7,
            "first-order obstruction cokernel {} unexpectedly small",
            report.obstruction_dim
        );
        assert_eq!(report.jacobian_rank + report.obstruction_dim, COLUMN_COUNT);
    }

    #[test]
    fn test_bianchi_d1_q_shape_and_annihilation() {
        let d1 = bianchi_d1_q();
        assert_eq!(d1.len(), 2);
        assert_eq!(d1[0].len(), COLUMN_COUNT);
        assert_eq!(d1[1].len(), COLUMN_COUNT);

        let mut z = vec![BigRational::zero(); COLUMN_COUNT];
        for i in 0..COLUMN_COUNT {
            z[i] = BigRational::from_integer(1.into());
        }
        let b = evaluate_bianchi_d1_q(&z).expect("18 coordinates");
        assert!(b[0].is_zero());
        assert!(b[1].is_zero());
    }

    #[test]
    fn test_classify_tangent_obstruction_trichotomy() {
        let zero_res = vec![BigRational::zero(); COLUMN_COUNT];
        assert_eq!(
            classify_tangent_obstruction(&zero_res).expect("18 coordinates"),
            ObstructionDiagnosticClass::ExactRepair
        );

        let mut closed_res = vec![BigRational::zero(); COLUMN_COUNT];
        closed_res[0] = BigRational::from_integer(1.into());
        closed_res[6] = BigRational::from_integer(1.into());
        closed_res[12] = BigRational::from_integer(1.into());
        assert_eq!(
            classify_tangent_obstruction(&closed_res).expect("18 coordinates"),
            ObstructionDiagnosticClass::ClosedResidual
        );

        let mut open_res = vec![BigRational::zero(); COLUMN_COUNT];
        open_res[0] = BigRational::from_integer(1.into());
        assert_eq!(
            classify_tangent_obstruction(&open_res).expect("18 coordinates"),
            ObstructionDiagnosticClass::ActiveClosureFailure
        );
    }

    #[test]
    fn malformed_cochains_and_matrices_are_refused() {
        let short_row = vec![Cyc24::rat(ri(1)), Cyc24::rat(ri(2))];
        let short_dir = vec![Cyc24::rat(ri(3))];
        assert!(mat_vec(&[short_row], &short_dir).is_err());

        assert!(rank_cyc24(&[
            vec![Cyc24::rat(ri(1))],
            vec![Cyc24::rat(ri(1)), Cyc24::rat(ri(2))],
        ])
        .is_err());

        assert!(classify_tangent_obstruction(&[]).is_err());
        let mut nineteenth = vec![BigRational::zero(); 19];
        nineteenth[18] = BigRational::from_integer(1.into());
        assert!(classify_tangent_obstruction(&nineteenth).is_err());
        assert!(evaluate_bianchi_d1_q(&nineteenth).is_err());

        let mut short_columns = canonical_triple_exact();
        short_columns.truncate(1);
        assert!(tangent_obstruction(&short_columns, &generic_unit()).is_err());
    }

    #[test]
    fn test_solve_and_classify_tangent_complex_exact_repair() {
        let mut d0 = vec![vec![BigRational::zero(); 1]; COLUMN_COUNT];
        d0[0][0] = BigRational::from_integer(1.into());
        d0[6][0] = BigRational::from_integer(1.into());
        d0[12][0] = BigRational::from_integer(1.into());

        let mut target = vec![BigRational::zero(); COLUMN_COUNT];
        target[0] = BigRational::from_integer(2.into());
        target[6] = BigRational::from_integer(2.into());
        target[12] = BigRational::from_integer(2.into());

        let weights = vec![BigRational::from_integer(1.into()); COLUMN_COUNT];
        let report = solve_and_classify_tangent_complex(&target, &weights, &d0, 1024).unwrap();

        assert_eq!(
            report.diagnostic_class,
            ObstructionDiagnosticClass::ExactRepair
        );
        assert!(report.phi1_certified_value.is_zero());
    }

    #[test]
    fn test_solve_and_classify_tangent_complex_closed_and_open_residuals() {
        let d0 = vec![vec![BigRational::zero(); 1]; COLUMN_COUNT];
        let weights = vec![BigRational::from_integer(1.into()); COLUMN_COUNT];

        let mut closed_target = vec![BigRational::zero(); COLUMN_COUNT];
        closed_target[0] = BigRational::from_integer(1.into());
        closed_target[6] = BigRational::from_integer(1.into());
        closed_target[12] = BigRational::from_integer(1.into());

        let report_closed =
            solve_and_classify_tangent_complex(&closed_target, &weights, &d0, 1024).unwrap();
        assert_eq!(
            report_closed.diagnostic_class,
            ObstructionDiagnosticClass::ClosedResidual
        );
        assert_eq!(
            report_closed.phi1_certified_value,
            BigRational::from_integer(3.into())
        );

        let mut open_target = vec![BigRational::zero(); COLUMN_COUNT];
        open_target[0] = BigRational::from_integer(1.into());

        let report_open =
            solve_and_classify_tangent_complex(&open_target, &weights, &d0, 1024).unwrap();
        assert_eq!(
            report_open.diagnostic_class,
            ObstructionDiagnosticClass::ActiveClosureFailure
        );
        assert_eq!(
            report_open.phi1_certified_value,
            BigRational::from_integer(1.into())
        );
    }
}
