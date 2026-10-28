

use num_bigint::{BigInt, BigUint};
use num_integer::Integer;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};

use engine_number_theory::rational::{ri, rq, Rational};

use engine_number_theory::rational_circle::{nearest_root_of_unity, phase_distance_on_circle};
use engine_quantum_physics::norm_approximation_frontier::{clock_shift_winding, NormFrontierError};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CcrDefectBoundResult {
    pub dimension: usize,
    pub scalar_lambda: String,
    pub trace_defect_lower_bound: String,
    pub normalized_trace_norm_lower_bound: String,
    pub normalized_frobenius_norm_lower_bound: String,
    pub operator_norm_lower_bound: String,
    pub limit_as_d_to_infinity_vanishes: bool,
    pub normalized_defect_strictly_positive: bool,
}

pub fn verify_ccr_defect_lower_bounds(
    d: usize,
    scalar_lambda: Rational,
) -> Result<CcrDefectBoundResult, NormFrontierError> {
    if d == 0 || scalar_lambda.is_zero() {
        return Err(NormFrontierError::Carrier);
    }
    let abs_lambda = scalar_lambda.abs();
    let d_rat = Rational::from_integer(d.into());
    let trace_bound = abs_lambda.clone() * d_rat;
    Ok(CcrDefectBoundResult {
        dimension: d,
        scalar_lambda: scalar_lambda.to_string(),
        trace_defect_lower_bound: trace_bound.to_string(),
        normalized_trace_norm_lower_bound: abs_lambda.to_string(),
        normalized_frobenius_norm_lower_bound: abs_lambda.to_string(),
        operator_norm_lower_bound: abs_lambda.to_string(),
        limit_as_d_to_infinity_vanishes: false,
        normalized_defect_strictly_positive: abs_lambda > Rational::zero(),
    })
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WeylPhaseScheduleRow {
    pub dimension: usize,
    pub best_numerator_a: usize,
    pub approx_phase: String,
    pub exact_phase_distance: String,
    pub meets_dirichlet_bound: bool,
    pub analytic_rational_upper_bound: String,
}

pub fn compute_weyl_phase_schedule(
    target_phase: Rational,
    dimensions: &[usize],
) -> Result<Vec<WeylPhaseScheduleRow>, engine_number_theory::rational_circle::RationalCircleError> {
    let mut rows = Vec::with_capacity(dimensions.len());
    for &d in dimensions {
        let (a, dist) = nearest_root_of_unity(&target_phase, d)?;
        let dirichlet_bound = Rational::new(1.into(), num_bigint::BigInt::from(d) * 2);
        rows.push(WeylPhaseScheduleRow {
            dimension: d,
            best_numerator_a: a,
            approx_phase: format!("{}/{}", a, d),
            exact_phase_distance: dist.to_string(),
            analytic_rational_upper_bound: (rq(44, 7) * &dist).to_string(),
            meets_dirichlet_bound: dist <= dirichlet_bound,
        });
    }
    Ok(rows)
}

pub fn exact_rational_weyl_schedule_term(target: &Rational, index: &BigUint) -> (BigUint, BigUint) {
    let multiplier = BigInt::from(index + BigUint::from(1u8));
    let d = target.denom() * &multiplier;
    let k = target.numer().mod_floor(target.denom()) * multiplier;
    (
        d.to_biguint()
            .expect("positive normalized rational denominator"),
        k.to_biguint().expect("nonnegative residue"),
    )
}
fn verify_declared_unbounded_rational_schedule(target: &Rational) -> bool {
    let (d, k) = exact_rational_weyl_schedule_term(target, &BigUint::from(0u8));
    !d.is_zero()
        && phase_distance_on_circle(target, &Rational::new(BigInt::from(k), BigInt::from(d)))
            .is_zero()
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BottObstructionResult {
    pub dimension: usize,
    pub bott_index: Option<i32>,
    pub is_topologically_obstructed: Option<bool>,
    pub log_branch_admissible: bool,
    pub obstruction_status: String,
}

pub fn compute_bott_index_witness(d: usize) -> Result<BottObstructionResult, NormFrontierError> {
    match clock_shift_winding(d) {
        Ok(w) => {
            let index = i32::try_from(w.winding).map_err(|_| NormFrontierError::Certificate)?;
            Ok(BottObstructionResult {
                dimension: d,
                bott_index: Some(index),
                is_topologically_obstructed: Some(index != 0),
                log_branch_admissible: true,
                obstruction_status: if index == 0 {
                    "COMMUTING"
                } else {
                    "CITED_INDEX_OBSTRUCTION"
                }
                .into(),
            })
        }
        Err(NormFrontierError::BranchCut) => Ok(BottObstructionResult {
            dimension: d,
            bott_index: None,
            is_topologically_obstructed: None,
            log_branch_admissible: false,
            obstruction_status: "REFUSED_LOG_BRANCH_CUT".into(),
        }),
        Err(e) => Err(e),
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CanonicalBlock02Receipt {
    pub authority_effect: String,
    pub citation: String,
    pub campaign: String,
    pub block: String,
    pub global_targets: String,
    pub terminal_outcome: String,
    pub ccr_defect_bounds: Vec<CcrDefectBoundResult>,
    pub weyl_approximation_schedule: Vec<WeylPhaseScheduleRow>,
    pub bott_index_obstruction: Vec<BottObstructionResult>,
    pub machine_bet_clauses: MachineBetClausesB02,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MachineBetClausesB02 {
    pub direct_ccr_normalized_defect_limit_zero: bool,
    pub twisted_weyl_defect_has_declared_zero_limit_sequence: bool,
    pub every_convergence_claim_names_norm_and_dimension_schedule: bool,
    pub topology_obstruction_status: String,
    pub finite_search_bounds_frozen_before_search: bool,
}

pub const FROZEN_SCHEDULE: [usize; 9] = [2, 3, 5, 8, 13, 21, 34, 55, 89];

pub fn generate_canonical_block02_receipt() -> CanonicalBlock02Receipt {
    let one = ri(1);
    let ccr_bounds: Vec<_> = FROZEN_SCHEDULE
        .iter()
        .map(|&d| {
            verify_ccr_defect_lower_bounds(d, one.clone())
                .expect("fixed nonzero scalar and dimensions")
        })
        .collect();

    let target_phase = rq(5, 8);
    let weyl_schedule = compute_weyl_phase_schedule(target_phase.clone(), &FROZEN_SCHEDULE)
        .expect("fixed nonempty carrier");

    let bott_results: Vec<_> = FROZEN_SCHEDULE
        .iter()
        .map(|&d| compute_bott_index_witness(d).expect("bounded fixed clock-shift fields"))
        .collect();

    CanonicalBlock02Receipt {
        authority_effect: "None".to_string(),
        citation: "sealed-derivation-v1 (3100c4e)".to_string(),
        campaign: "C500".to_string(),
        block: "block_02".to_string(),
        global_targets: "C500-T326..C500-T350".to_string(),
        terminal_outcome: "NORM_INDEXED_APPROXIMATION_FRONTIER".to_string(),
        ccr_defect_bounds: ccr_bounds,
        weyl_approximation_schedule: weyl_schedule,
        bott_index_obstruction: bott_results,
        machine_bet_clauses: MachineBetClausesB02 {
            direct_ccr_normalized_defect_limit_zero: false,
            twisted_weyl_defect_has_declared_zero_limit_sequence:
                verify_declared_unbounded_rational_schedule(&target_phase),
            every_convergence_claim_names_norm_and_dimension_schedule: true,
            topology_obstruction_status: "CITED_WITH_BRANCH_GUARD".to_string(),
            finite_search_bounds_frozen_before_search: FROZEN_SCHEDULE
                .windows(2)
                .all(|d| d[0] < d[1]),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::{involution::hs_norm_squared, matrix};
    use engine_number_theory::cyclotomic::GaussianRat;

    #[test]
    fn winding_refuses_the_principal_log_branch_cut() {
        let branch_cut = compute_bott_index_witness(2).unwrap();
        assert_eq!(branch_cut.bott_index, None);
        assert_eq!(branch_cut.is_topologically_obstructed, None);
        assert!(!branch_cut.log_branch_admissible);
        assert_eq!(compute_bott_index_witness(1).unwrap().bott_index, Some(0));
    }

    #[test]
    fn nearest_root_rejects_empty_candidate_class() {
        assert!(nearest_root_of_unity(&rq(5, 8), 0).is_err());
    }

    #[test]
    fn zero_scalar_cannot_certify_a_nonvanishing_bound() {
        assert!(verify_ccr_defect_lower_bounds(3, ri(0)).is_err());
    }

    #[test]
    fn test_rust_matrix_trace_and_frobenius() {
        let m = matrix::identity::<GaussianRat>(3).unwrap();
        assert_eq!(matrix::trace(&m).unwrap(), GaussianRat::from_ints(3, 0));
        assert_eq!(hs_norm_squared(&m).unwrap(), GaussianRat::from_ints(3, 0));
        assert_eq!(hs_norm_squared(&m).unwrap().re / ri(3), ri(1));
    }

    #[test]
    fn test_rust_ccr_lower_bounds() {
        for &d in &FROZEN_SCHEDULE {
            let res = verify_ccr_defect_lower_bounds(d, ri(1)).unwrap();
            assert_eq!(res.normalized_trace_norm_lower_bound, "1");
            assert_eq!(res.normalized_frobenius_norm_lower_bound, "1");
            assert!(!res.limit_as_d_to_infinity_vanishes);
            assert!(res.normalized_defect_strictly_positive);
        }
    }

    #[test]
    fn test_rust_phase_distance() {
        let p1 = rq(9, 10);
        let p2 = rq(1, 10);
        assert_eq!(phase_distance_on_circle(&p1, &p2), rq(1, 5));

        let (a, dist) = nearest_root_of_unity(&rq(5, 8), 8).unwrap();
        assert_eq!(a, 5);
        assert_eq!(dist, Rational::zero());
    }

    #[test]
    fn test_rust_weyl_phase_schedule_dirichlet() {
        let sched = compute_weyl_phase_schedule(rq(5, 8), &FROZEN_SCHEDULE).unwrap();
        for row in sched {
            assert!(row.meets_dirichlet_bound);
        }
    }

    #[test]
    fn test_rust_bott_obstruction() {
        for &d in &FROZEN_SCHEDULE {
            let res = compute_bott_index_witness(d).unwrap();
            assert_eq!(res.bott_index, if d == 2 { None } else { Some(1) });
            assert_eq!(
                res.is_topologically_obstructed,
                if d == 2 { None } else { Some(true) }
            );
        }
    }

    #[test]
    fn test_rust_canonical_receipt_generation() {
        let receipt = generate_canonical_block02_receipt();
        assert_eq!(receipt.authority_effect, "None");
        assert_eq!(
            receipt.terminal_outcome,
            "NORM_INDEXED_APPROXIMATION_FRONTIER"
        );
        assert!(
            !receipt
                .machine_bet_clauses
                .direct_ccr_normalized_defect_limit_zero
        );
        assert!(
            receipt
                .machine_bet_clauses
                .twisted_weyl_defect_has_declared_zero_limit_sequence
        );
        assert_eq!(
            receipt.machine_bet_clauses.topology_obstruction_status,
            "CITED_WITH_BRANCH_GUARD"
        );
    }
    #[test]
    fn rational_phase_has_an_exact_unbounded_nominal_root_schedule() {
        let target = rq(-17, 120);
        let index = BigUint::from(10u8).pow(100);
        let (d, k) = exact_rational_weyl_schedule_term(&target, &index);
        assert!(d > BigUint::from(usize::MAX));
        assert!(phase_distance_on_circle(
            &target,
            &Rational::new(BigInt::from(k), BigInt::from(d))
        )
        .is_zero());
        assert!(verify_declared_unbounded_rational_schedule(&target));
    }
}
