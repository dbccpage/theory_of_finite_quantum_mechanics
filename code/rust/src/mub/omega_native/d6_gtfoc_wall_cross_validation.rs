
use linear_algebra::linear_algebra::complex_matrix::{CVector, C64};
use omega_functional::{
    MubFeasibilityWallFunctional, MubFeasibilityWallTargetComparison, MubFeasibilityWallValue,
};
use serde::Serialize;

use crate::omega_native::float_check::gtfoc_float_wall::{
    norm, probabilities, projected_s_gradient, qubit_x_basis, qubit_y_basis, residual_square_sum,
    root_of_unity, seeded_unit_vector, tensor_vec, zero_vec,
};

type C = C64;
type Vector = CVector;

const D: usize = 6;
const COLUMN_COUNT: usize = 18;
const TARGET_PROB: f64 = 1.0 / 6.0;
const TOLERANCE: f64 = 1e-9;

pub fn certified_wall_w() -> f64 {
    (88.0 + 3.0 * 6.0_f64.sqrt()) / 100.0
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct D6GtfocWallCrossValidation {
    pub target: &'static str,
    pub method: &'static str,
    pub wall_value_native: f64,
    pub wall_value_certified: f64,
    pub wall_abs_error: f64,
    pub wall_matches: bool,
    pub obstruction_value_native: f64,
    pub obstruction_value_certified: f64,
    pub obstruction_abs_error: f64,
    pub obstruction_matches: bool,
    pub observed_residual_norm: f64,
    pub phi1_reference_from_cited_wall: f64,
    pub observed_residual_matches_cited_reference: bool,
    pub phi1_strictly_positive: bool,
    pub tolerance: f64,
    pub has_exact_certificate: bool,
    pub has_global_upper_bound_certificate: bool,
    pub has_full_mub6_authority: bool,
    pub boundary: &'static str,
}

pub fn run_d6_gtfoc_wall_cross_validation() -> D6GtfocWallCrossValidation {
    let columns = canonical_d6_columns();
    let maximizer = optimize_wall_candidate(&columns);
    let probabilities = probabilities(&columns, &maximizer);
    let wall = MubFeasibilityWallFunctional::evaluate_probabilities(&probabilities, TARGET_PROB)
        .expect("finite d=6 MUB wall functional");

    let w = certified_wall_w();
    let one_minus_w = 1.0 - w;

    let wall_value_native = wall.wall_value;
    let obstruction_value_native = wall.obstruction_value;
    let (observed_residual_norm, phi1_reference_from_cited_wall) =
        MubFeasibilityWallFunctional::curvature_floors(&wall, w)
            .expect("finite declared MUB wall normalization");
    let wall_comparison = target_comparison(&wall, one_minus_w, w);
    let has_global_upper_bound_certificate = false;

    D6GtfocWallCrossValidation {
        target: "d=6 canonical-triple {Z2⊗Z3, X2⊗Q0, Y2⊗Q1} fourth-vector wall",
        method: "Omega-native f64 unit-sphere optimizer over the rebuilt triple plus omega_functional normalized feasibility functional (target 1/6)",
        wall_value_native,
        wall_value_certified: w,
        wall_abs_error: wall_comparison.wall_abs_error,
        wall_matches: wall_comparison.wall_matches,
        obstruction_value_native,
        obstruction_value_certified: one_minus_w,
        obstruction_abs_error: wall_comparison.obstruction_abs_error,
        obstruction_matches: wall_comparison.obstruction_matches,
        observed_residual_norm,
        phi1_reference_from_cited_wall,
        observed_residual_matches_cited_reference: (observed_residual_norm
            - phi1_reference_from_cited_wall)
            .abs()
            <= TOLERANCE,
        phi1_strictly_positive: has_global_upper_bound_certificate,
        tolerance: wall_comparison.tolerance,
        has_exact_certificate: false,
        has_global_upper_bound_certificate,
        has_full_mub6_authority: false,
        boundary: "Cross-validation evidence only: an f64 optimizer reproducing the cited exact W=(88+3√6)/100. The observed residual norm is compared with the cited reference sqrt((1-W)*5/6). That comparison is not a global curvature floor. No exact rational certificate, no global wall certificate, and no MUB(6) theorem authority is minted here (the exact two-sided proof is the Invariant-Systems result, held externally and not reproduced in this tree).",
    }
}

fn target_comparison(
    wall: &MubFeasibilityWallValue,
    target_obstruction: f64,
    target_wall: f64,
) -> MubFeasibilityWallTargetComparison {
    MubFeasibilityWallFunctional::compare_targets_f64_diagnostic(
        wall,
        target_obstruction,
        target_wall,
        TOLERANCE,
    )
    .expect("finite d=6 MUB wall target comparison")
}


fn canonical_d6_columns() -> Vec<Vector> {
    let mut columns = Vec::with_capacity(COLUMN_COUNT);
    for idx in 0..D {
        let mut v = zero_vec(D);
        v[idx] = C::new(1.0, 0.0);
        columns.push(v);
    }
    let x2 = qubit_x_basis();
    let y2 = qubit_y_basis();
    let q0 = qutrit_q_basis(0);
    let q1 = qutrit_q_basis(1);
    for qb in &x2 {
        for qt in &q0 {
            columns.push(tensor_vec(qb, qt));
        }
    }
    for qb in &y2 {
        for qt in &q1 {
            columns.push(tensor_vec(qb, qt));
        }
    }
    columns
}

fn qutrit_q_basis(a: i32) -> Vec<Vector> {
    let scale = 1.0 / 3.0_f64.sqrt();
    let mut columns = Vec::with_capacity(3);
    for m in 0..3_i32 {
        let mut col = zero_vec(3);
        for j in 0..3_i32 {
            let exp = a * j * j + m * j;
            col[j as usize] = root_of_unity(3, exp) * scale;
        }
        columns.push(col);
    }
    columns
}


fn optimize_wall_candidate(columns: &[Vector]) -> Vector {
    let mut best = zero_vec(D);
    let mut best_s = f64::INFINITY;
    let mut candidate = zero_vec(D);
    for seed in 0..128_u64 {
        let mut v = seeded_unit_vector(seed, D);
        let mut s = residual_square_sum(columns, &v);
        let mut step: f64 = 0.08;
        for _ in 0..3000 {
            let grad = projected_s_gradient(columns, &v);
            if norm(&grad) < 1e-14 {
                break;
            }
            let mut accepted = false;
            for _ in 0..20 {
                for i in 0..D {
                    candidate[i] = v[i] - grad[i] * step;
                }
                normalize_in_place(&mut candidate);
                let candidate_s = residual_square_sum(columns, &candidate);
                if candidate_s < s {
                    std::mem::swap(&mut v, &mut candidate);
                    s = candidate_s;
                    step = (step * 1.08).min(0.5);
                    accepted = true;
                    break;
                }
                step *= 0.5;
            }
            if !accepted || step < 1e-15 {
                break;
            }
        }
        if s < best_s {
            best_s = s;
            best = v;
        }
    }
    best
}

fn normalize_in_place(v: &mut Vector) {
    let n = norm(v);
    if n > 0.0 {
        for item in v.iter_mut() {
            *item /= n;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::float_check::gtfoc_float_wall::inner;

    #[test]
    fn d6_rebuilds_canonical_triple_as_unit_columns() {
        let columns = canonical_d6_columns();
        assert_eq!(columns.len(), COLUMN_COUNT);
        for column in &columns {
            assert!((norm(column) - 1.0).abs() < 1e-12);
        }
    }

    #[test]
    fn d6_triple_bases_are_pairwise_orthonormal_and_mutually_unbiased() {
        let columns = canonical_d6_columns();
        for (i, ci) in columns.iter().enumerate() {
            for (j, cj) in columns.iter().enumerate() {
                let overlap = inner(ci, cj).norm_sqr();
                let bi = i / D;
                let bj = j / D;
                if i == j {
                    assert!((overlap - 1.0).abs() < 1e-10);
                } else if bi == bj {
                    assert!(overlap < 1e-10, "within-basis orthogonality at {i},{j}");
                } else {
                    assert!(
                        (overlap - 1.0 / 6.0).abs() < 1e-10,
                        "cross-basis unbiasedness at {i},{j}: {overlap}"
                    );
                }
            }
        }
    }

    #[test]
    fn d6_native_wall_reproduces_certified_w() {
        let report = run_d6_gtfoc_wall_cross_validation();
        eprintln!(
            "d6 wall cross-validation: native f={:.15} cited W={:.15} |err|={:.3e} | native 1-f={:.15} cited 1-W={:.15} | observed residual={:.15} cited reference={:.15}",
            report.wall_value_native,
            report.wall_value_certified,
            report.wall_abs_error,
            report.obstruction_value_native,
            report.obstruction_value_certified,
            report.observed_residual_norm,
            report.phi1_reference_from_cited_wall,
        );
        assert!(
            report.wall_matches,
            "native wall {} should match cited W {} within {}",
            report.wall_value_native, report.wall_value_certified, report.tolerance
        );
        assert!(report.obstruction_matches);
        assert!(report.observed_residual_matches_cited_reference);
        assert!(!report.phi1_strictly_positive);
        assert!(!report.has_exact_certificate);
        assert!(!report.has_global_upper_bound_certificate);
        assert!(!report.has_full_mub6_authority);
        assert!(report.boundary.contains("no MUB(6) theorem authority"));
    }

    #[test]
    fn d6_target_comparison_is_f64_diagnostic_and_mints_nothing() {
        use omega_functional::MubFeasibilityWallEvidenceKind;
        let report = run_d6_gtfoc_wall_cross_validation();
        let columns = canonical_d6_columns();
        let maximizer = optimize_wall_candidate(&columns);
        let wall = MubFeasibilityWallFunctional::evaluate_probabilities(
            &probabilities(&columns, &maximizer),
            TARGET_PROB,
        )
        .expect("finite wall value");
        let cmp = target_comparison(&wall, 1.0 - certified_wall_w(), certified_wall_w());
        assert_eq!(
            cmp.evidence_kind,
            MubFeasibilityWallEvidenceKind::F64Diagnostic
        );
        assert!(!cmp.has_exact_certificate);
        assert!(!cmp.has_global_upper_bound_certificate);
        assert_eq!(report.wall_abs_error, cmp.wall_abs_error);
        assert_eq!(report.wall_matches, cmp.wall_matches);
        assert_eq!(report.obstruction_abs_error, cmp.obstruction_abs_error);
        assert_eq!(report.obstruction_matches, cmp.obstruction_matches);
        assert_eq!(report.tolerance, cmp.tolerance);
        assert!(report.wall_matches);
        assert!(!report.has_exact_certificate);
        assert!(!report.has_global_upper_bound_certificate);
        assert!(!report.phi1_strictly_positive);
        assert!(!report.has_full_mub6_authority);
    }

    #[test]
    fn d6_perfect_unbiasedness_gives_unit_wall_value() {
        let probabilities = vec![TARGET_PROB; COLUMN_COUNT];
        let wall =
            MubFeasibilityWallFunctional::evaluate_probabilities(&probabilities, TARGET_PROB)
                .expect("finite wall value");
        assert!(wall.residual_square_sum.abs() < 1e-15);
        assert!((wall.wall_value - 1.0).abs() < 1e-15);
        assert!(wall.obstruction_value.abs() < 1e-15);
    }
}
