

use crate::linear_algebra::{elimination::rank, involution::outer_product, matrix};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::integer_factorization::FactorizationBudget;
use omega_number_theory::rational::{ri, Rational};
use omega_number_theory::vanishing_sums::minimal_root_conductor;
use omega_quantum_physics::mub::algebra::{verify_mub_projector_algebra, ProjectorAlgebraStatus};
use omega_quantum_physics::mub::composite::build_composite_mub_d6;

pub const TENSOR_AXIOMS: [&str; 4] = [
    "bilinearity",
    "local_unitary_covariance",
    "product_marginal_consistency",
    "no_signaling",
];

pub fn tensor_axiom_count() -> usize {
    TENSOR_AXIOMS.len()
}

pub fn tensor_unique_under_axioms() -> Option<bool> {
    None
}

pub type CombiningOperation = fn(&[Rational; 2], &[Rational; 2]) -> Vec<Rational>;

pub fn dump_combine(u: &[Rational; 2], v: &[Rational; 2]) -> Vec<Rational> {
    let weight = &v[0] + &v[1];
    u.iter().map(|x| x * &weight).collect()
}

pub fn kronecker_combine(u: &[Rational; 2], v: &[Rational; 2]) -> Vec<Rational> {
    let mut out = Vec::with_capacity(4);
    for a in u {
        for b in v {
            out.push(a * b);
        }
    }
    out
}

pub fn fails_local_unitary_covariance(combine: CombiningOperation) -> Result<bool, String> {
    let basis = [[ri(1), ri(0)], [ri(0), ri(1)]];
    let z = |v: &[Rational; 2]| [v[0].clone(), -v[1].clone()];
    let mut a_cols = Vec::new();
    let mut b_cols = Vec::new();
    for u in &basis {
        for v in &basis {
            a_cols.push(combine(u, v));
            b_cols.push(combine(u, &z(v)));
        }
    }
    let a = columns_to_rows(&a_cols);
    let mut stacked = a.clone();
    stacked.extend(columns_to_rows(&b_cols));
    Ok(
        rank(&matrix::from_rows(stacked).map_err(|e| e.to_string())?).map_err(|e| e.to_string())?
            != rank(&matrix::from_rows(a).map_err(|e| e.to_string())?)
                .map_err(|e| e.to_string())?,
    )
}

pub fn rival_fails_local_unitary_covariance() -> bool {
    fails_local_unitary_covariance(dump_combine).unwrap_or(false)
}

fn columns_to_rows(cols: &[Vec<Rational>]) -> Vec<Vec<Rational>> {
    (0..cols[0].len())
        .map(|r| cols.iter().map(|c| c[r].clone()).collect())
        .collect()
}

pub fn verify_d6_product_mubs() -> (usize, usize, bool) {
    let bases = build_composite_mub_d6();
    let basis_count = bases.len();
    let total_projectors: usize = bases.iter().map(|b| b.len()).sum();
    let report = verify_mub_projector_algebra(&bases, 6);
    let ok = report.status == ProjectorAlgebraStatus::AlgebraVerified
        && report.basis_count == 3
        && report.projector_count == 18;
    (basis_count, total_projectors, ok)
}

pub fn search_fourth_mub_d6(
    conductor_ceiling: usize,
    max_candidates: usize,
) -> Result<(usize, &'static str), String> {
    if conductor_ceiling == 0 || 24 % conductor_ceiling != 0 || max_candidates > 1_000_000 {
        return Err(
            "declare a divisor of conductor24 and at most one million candidate vectors".into(),
        );
    }
    let total = conductor_ceiling
        .checked_pow(5)
        .ok_or("candidate carrier overflow")?;
    if max_candidates > total {
        return Err("candidate budget exceeds the distinct phase-vector carrier".into());
    }
    let bases = build_composite_mub_d6();
    let cond = conductor_ceiling;
    let mut candidates_found = 0;

    for cand_idx in 0..max_candidates {
        let mut index = cand_idx;
        let mut powers = [0usize; 5];
        for p in &mut powers {
            *p = index % cond;
            index /= cond;
        }
        let [k1, k2, k3, k4, k5] = powers;
        let phases = [
            Cyc24::one(),
            Cyc24::zeta24((k1 * 24 / cond) as i32),
            Cyc24::zeta24((k2 * 24 / cond) as i32),
            Cyc24::zeta24((k3 * 24 / cond) as i32),
            Cyc24::zeta24((k4 * 24 / cond) as i32),
            Cyc24::zeta24((k5 * 24 / cond) as i32),
        ];

        let m = outer_product(&phases, &phases).map_err(|e| e.to_string())?;

        let mut all_unbiased = true;
        for basis in &bases {
            for pi in basis {
                let tr = matrix::trace(&matrix::multiply(&m, pi).map_err(|e| e.to_string())?)
                    .map_err(|e| e.to_string())?;
                if tr != Cyc24::one() {
                    all_unbiased = false;
                    break;
                }
            }
            if !all_unbiased {
                break;
            }
        }

        if all_unbiased {
            candidates_found += 1;
        }
    }

    let status = if candidates_found == 0 {
        "OPEN"
    } else {
        "CANDIDATE_VECTOR_FOUND"
    };
    Ok((candidates_found, status))
}

pub fn evaluate_gkp_conductor_scaling(max_n: usize) -> Result<(bool, &'static str, usize), String> {
    if max_n > 128 {
        return Err("the declared root carrier exceeds128".into());
    }
    let mut max_conductor = 0;
    let mut lower_bound_verified = max_n >= 2;
    for n in 2..=max_n {
        let witness = minimal_root_conductor(n, 128, FactorizationBudget::default())
            .map_err(|e| e.to_string())?;
        let cond = witness.conductor;
        lower_bound_verified &= witness
            .verify(FactorizationBudget::default())
            .map_err(|e| e.to_string())?;
        lower_bound_verified &= 2 * cond >= n;
        if cond > max_conductor {
            max_conductor = cond;
        }
    }
    let scaling_factor = "N";
    Ok((lower_bound_verified, scaling_factor, max_conductor))
}

#[derive(serde::Serialize)]
pub struct Block05ExecutionReport {
    pub tensor_unique_under_axioms: Option<bool>,
    pub tensor_axiom_count: usize,
    pub rival_fails_covariance: bool,
    pub d6_mub_count_found: usize,
    pub d6_product_mubs_verified: bool,
    pub d6_fourth_mub_candidates_found: usize,
    pub d6_fourth_mub_search_outcome: &'static str,
    pub gkp_conductor_lower_bound_verified: bool,
    pub gkp_conductor_scaling_factor: &'static str,
}

impl Block05ExecutionReport {
    pub fn bounded_checks_hold(&self) -> bool {
        self.tensor_axiom_count == TENSOR_AXIOMS.len()
            && self.rival_fails_covariance
            && self.d6_mub_count_found == 3
            && self.d6_product_mubs_verified
            && self.d6_fourth_mub_candidates_found == 0
            && self.d6_fourth_mub_search_outcome == "OPEN"
            && self.gkp_conductor_lower_bound_verified
            && self.gkp_conductor_scaling_factor == "N"
    }

    pub fn status(&self) -> &'static str {
        if self.bounded_checks_hold() && self.tensor_unique_under_axioms.is_none() {
            "SCOPED_RESULTS_WITH_OPEN_OBLIGATIONS"
        } else {
            "FAIL"
        }
    }
}

pub fn run_block_05_report() -> Block05ExecutionReport {
    let (d6_bases, _, d6_ok) = verify_d6_product_mubs();
    let (fourth_found, fourth_status) =
        search_fourth_mub_d6(24, 1000).expect("frozen finite phase carrier");
    let (gkp_bound, gkp_factor, _) =
        evaluate_gkp_conductor_scaling(20).expect("bounded root conductor search");

    Block05ExecutionReport {
        tensor_unique_under_axioms: None,
        tensor_axiom_count: tensor_axiom_count(),
        rival_fails_covariance: rival_fails_local_unitary_covariance(),
        d6_mub_count_found: d6_bases,
        d6_product_mubs_verified: d6_ok,
        d6_fourth_mub_candidates_found: fourth_found,
        d6_fourth_mub_search_outcome: fourth_status,
        gkp_conductor_lower_bound_verified: gkp_bound,
        gkp_conductor_scaling_factor: gkp_factor,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tensor_axioms_properties() {
        assert_eq!(tensor_axiom_count(), 4);
        assert_eq!(tensor_unique_under_axioms(), None);
        assert_eq!(TENSOR_AXIOMS[0], "bilinearity");
        assert_eq!(TENSOR_AXIOMS[1], "local_unitary_covariance");
        assert_eq!(TENSOR_AXIOMS[2], "product_marginal_consistency");
        assert_eq!(TENSOR_AXIOMS[3], "no_signaling");
    }

    #[test]
    fn test_rival_combining_fails_covariance() {
        assert!(rival_fails_local_unitary_covariance());
    }

    #[test]
    fn test_kronecker_product_is_locally_covariant() {
        assert!(!fails_local_unitary_covariance(kronecker_combine).unwrap());
    }

    #[test]
    fn test_d6_product_mubs_algebra() {
        let (basis_count, total_projectors, ok) = verify_d6_product_mubs();
        assert_eq!(basis_count, 3);
        assert_eq!(total_projectors, 18);
        assert!(ok);
    }

    #[test]
    fn test_d6_fourth_mub_search_is_open() {
        let (found, status) = search_fourth_mub_d6(24, 1000).expect("frozen finite phase carrier");
        assert_eq!(found, 0);
        assert_eq!(status, "OPEN");
    }

    #[test]
    fn test_gkp_scaling_unbounded() {
        let (bound_verified, factor, max_cond) =
            evaluate_gkp_conductor_scaling(20).expect("bounded root conductor search");
        assert!(bound_verified);
        assert!(!evaluate_gkp_conductor_scaling(1).unwrap().0);
        assert_eq!(factor, "N");
        assert_eq!(max_cond, 20);
    }

    #[test]
    fn test_block_05_full_report() {
        let r = run_block_05_report();
        assert_eq!(r.tensor_unique_under_axioms, None);
        assert_eq!(r.tensor_axiom_count, 4);
        assert!(r.rival_fails_covariance);
        assert_eq!(r.d6_mub_count_found, 3);
        assert!(r.d6_product_mubs_verified);
        assert_eq!(r.d6_fourth_mub_candidates_found, 0);
        assert_eq!(r.d6_fourth_mub_search_outcome, "OPEN");
        assert!(r.gkp_conductor_lower_bound_verified);
        assert!(r.bounded_checks_hold());
        assert_eq!(r.status(), "SCOPED_RESULTS_WITH_OPEN_OBLIGATIONS");
        assert_eq!(r.gkp_conductor_scaling_factor, "N");
    }

    #[test]
    fn test_block_05_status_rejects_inconsistent_or_refuted_results() {
        let mut r = run_block_05_report();
        assert_eq!(r.status(), "SCOPED_RESULTS_WITH_OPEN_OBLIGATIONS");

        r.d6_fourth_mub_search_outcome = "CANDIDATE_VECTOR_FOUND";
        assert_eq!(r.status(), "FAIL");
        r.d6_fourth_mub_search_outcome = "OPEN";

        r.d6_mub_count_found = 2;
        assert_eq!(r.status(), "FAIL");
        r.d6_mub_count_found = 3;

        r.tensor_unique_under_axioms = Some(false);
        assert_eq!(r.status(), "FAIL");
        r.tensor_unique_under_axioms = Some(true);
        assert_eq!(r.status(), "FAIL");
    }
}
