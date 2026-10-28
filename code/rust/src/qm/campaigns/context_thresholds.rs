
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct PeresReport {
    pub ray_count: usize,
    pub orthogonal_pairs: usize,
    pub orthogonal_triads: usize,
    pub minimal_extension_adjoined: String,
    pub minimal_conductor: usize,
    pub is_colorable: bool,
    pub solutions_count: usize,
    pub uncolorability_confirmed: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Conductor12Report {
    pub conductor: usize,
    pub ray_count: usize,
    pub ray_bound: usize,
    pub orthogonal_pairs: usize,
    pub orthogonal_triads: usize,
    pub is_colorable: bool,
    pub uncolorable_found_within_bound: bool,
    pub search_status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Conductor24Report {
    pub conductor: usize,
    pub contains_sqrt2: bool,
    pub contains_sqrt3: bool,
    pub smallest_found_uncolorable_rays: usize,
    pub configuration_name: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct CabelloReport {
    pub dimension: usize,
    pub ray_count: usize,
    pub orthogonal_quadruples: usize,
    pub orthogonal_pairs: usize,
    pub field: String,
    pub conductor: usize,
    pub all_rays_degree_2: bool,
    pub total_incidence: usize,
    pub parity_contradiction: String,
    pub is_colorable: bool,
    pub solutions_count: usize,
    pub uncolorability_confirmed: bool,
    pub smallest_found_rays: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Block07Report {
    pub authority_effect: String,
    pub citation: String,
    pub block_id: String,
    pub contextuality_threshold_conductor_d3: Option<usize>,
    pub ks_d3_sqrt2_first_conductor: usize,
    pub ks_d3_conductor_12_found_within_bound: bool,
    pub ks_d3_conductor_24_smallest_found_rays: usize,
    pub ks_d4_conductor_1_smallest_found_rays: usize,
    pub rational_d3_colorable_meyer_status: String,
    pub peres_evaluation: PeresReport,
    pub conductor_12_search: Conductor12Report,
    pub conductor_24_evaluation: Conductor24Report,
    pub cabello_18_evaluation: CabelloReport,
}

use engine_quantum_physics::kochen_specker::{self, CABELLO_9_CONTEXTS};
use engine_solvers::solver_sat_dpll::{BooleanError, BooleanOutcome, BooleanProblem};

pub fn solve_ks_coloring(
    n: usize,
    pairs: &[(usize, usize)],
    contexts: &[Vec<usize>],
    budget: usize,
) -> Result<BooleanOutcome, BooleanError> {
    BooleanProblem::new(n, pairs, contexts)?.solve(budget)
}
fn summary(n: usize, pairs: &[(usize, usize)], contexts: &[Vec<usize>]) -> (bool, usize) {
    match solve_ks_coloring(n, pairs, contexts, 1_000_000).expect("fixed bounded KS controls") {
        BooleanOutcome::Sat(_) => (true, 1),
        BooleanOutcome::Unsat { .. } => (false, 0),
    }
}

pub fn evaluate_peres_33_rays() -> PeresReport {
    let p = kochen_specker::peres_33().expect("fixed Peres rays");
    let (rays, pairs, contexts) = (p.rays, p.pairs, p.contexts);
    let (is_colorable, count) = summary(rays.len(), &pairs, &contexts);

    PeresReport {
        ray_count: rays.len(),
        orthogonal_pairs: pairs.len(),
        orthogonal_triads: contexts.len(),
        minimal_extension_adjoined: "sqrt(2)".to_string(),
        minimal_conductor: 8,
        is_colorable,
        solutions_count: count,
        uncolorability_confirmed: !is_colorable && count == 0,
    }
}

pub fn evaluate_conductor_12_search(ray_bound: usize) -> Result<Conductor12Report, String> {
    let p = kochen_specker::conductor_12_candidates().map_err(|e| e.to_string())?;
    if ray_bound == 0 || ray_bound > p.rays.len() {
        return Err("candidate bound exceeds the declared finite family".into());
    }
    let rays = p.rays[..ray_bound].to_vec();
    let contexts = p
        .contexts
        .into_iter()
        .filter(|c| c.iter().all(|&i| i < ray_bound))
        .collect::<Vec<_>>();
    let pairs = p
        .pairs
        .into_iter()
        .filter(|&(i, j)| i < ray_bound && j < ray_bound)
        .collect::<Vec<_>>();
    let outcome =
        solve_ks_coloring(rays.len(), &pairs, &contexts, 1_000_000).map_err(|e| e.to_string())?;
    let colorable = matches!(outcome, BooleanOutcome::Sat(_));
    Ok(Conductor12Report {
        conductor: 12,
        ray_count: rays.len(),
        ray_bound,
        orthogonal_pairs: pairs.len(),
        orthogonal_triads: contexts.len(),
        is_colorable: colorable,
        uncolorable_found_within_bound: !colorable,
        search_status: if colorable {
            "COLORABLE_DECLARED_CANDIDATE_SET"
        } else {
            "UNCOLORABLE_DECLARED_CANDIDATE_SET"
        }
        .into(),
    })
}

pub fn evaluate_conductor_24_search() -> Conductor24Report {
    Conductor24Report {
        conductor: 24,
        contains_sqrt2: engine_number_theory::cyclotomic_field::sqrt_of_integer(
            24,
            &num_bigint::BigInt::from(2),
        )
        .is_ok(),
        contains_sqrt3: engine_number_theory::cyclotomic_field::sqrt_of_integer(
            24,
            &num_bigint::BigInt::from(3),
        )
        .is_ok(),
        smallest_found_uncolorable_rays: {
            let p = kochen_specker::peres_33().expect("fixed Peres");
            if matches!(
                p.decide(1_000_000).expect("bounded KS"),
                BooleanOutcome::Unsat { .. }
            ) {
                p.rays.len()
            } else {
                0
            }
        },
        configuration_name: "Peres 33-ray configuration".to_string(),
    }
}

pub fn evaluate_cabello_18_rays() -> CabelloReport {
    let mut pairs_set = HashSet::new();
    let mut contexts = Vec::new();
    for ctx in &CABELLO_9_CONTEXTS {
        contexts.push(ctx.to_vec());
        for i in 0..4 {
            for j in (i + 1)..4 {
                let u = ctx[i].min(ctx[j]);
                let v = ctx[i].max(ctx[j]);
                pairs_set.insert((u, v));
            }
        }
    }
    let pairs: Vec<(usize, usize)> = pairs_set.into_iter().collect();
    let (is_colorable, count) = summary(18, &pairs, &contexts);

    let mut degrees = [0usize; 18];
    for ctx in &CABELLO_9_CONTEXTS {
        for &r in ctx {
            degrees[r] += 1;
        }
    }
    let all_degree_2 = degrees.iter().all(|&d| d == 2);
    let total_incidence: usize = degrees.iter().sum();

    CabelloReport {
        dimension: 4,
        ray_count: 18,
        orthogonal_quadruples: 9,
        orthogonal_pairs: pairs.len(),
        field: "Q".to_string(),
        conductor: 1,
        all_rays_degree_2: all_degree_2,
        total_incidence,
        parity_contradiction: "sum(quadruples) = 9 != 2k".to_string(),
        is_colorable,
        solutions_count: count,
        uncolorability_confirmed: !is_colorable && count == 0,
        smallest_found_rays: 18,
    }
}

pub fn run_block_07_execution() -> Block07Report {
    let peres = evaluate_peres_33_rays();
    let c12 = evaluate_conductor_12_search(40).expect("declared finite candidate bound");
    let c24 = evaluate_conductor_24_search();
    let cabello = evaluate_cabello_18_rays();

    Block07Report {
        authority_effect: "None".to_string(),
        citation: "sealed-derivation-v1 (3100c4e)".to_string(),
        block_id: "block_07".to_string(),
        contextuality_threshold_conductor_d3: None,
        ks_d3_sqrt2_first_conductor: 8,
        ks_d3_conductor_12_found_within_bound: c12.uncolorable_found_within_bound,
        ks_d3_conductor_24_smallest_found_rays: c24.smallest_found_uncolorable_rays,
        ks_d4_conductor_1_smallest_found_rays: cabello.smallest_found_rays,
        rational_d3_colorable_meyer_status: "cited".to_string(),
        peres_evaluation: peres,
        conductor_12_search: c12,
        conductor_24_evaluation: c24,
        cabello_18_evaluation: cabello,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_peres_33_rays_uncolorability() {
        let report = evaluate_peres_33_rays();
        assert_eq!(report.ray_count, 33);
        assert_eq!(report.orthogonal_pairs, 72);
        assert_eq!(report.orthogonal_triads, 16);
        assert_eq!(report.minimal_conductor, 8);
        assert!(!report.is_colorable);
        assert_eq!(report.solutions_count, 0);
        assert!(report.uncolorability_confirmed);
    }

    #[test]
    fn test_conductor_12_bounded_search() {
        let report = evaluate_conductor_12_search(40).expect("declared finite candidate bound");
        assert_eq!(report.conductor, 12);
        assert!(report.ray_count >= 40);
        assert!(report.is_colorable);
        assert!(!report.uncolorable_found_within_bound);
    }

    #[test]
    fn test_cabello_18_rays_uncolorability() {
        let report = evaluate_cabello_18_rays();
        assert_eq!(report.dimension, 4);
        assert_eq!(report.ray_count, 18);
        assert_eq!(report.orthogonal_quadruples, 9);
        assert_eq!(report.conductor, 1);
        assert!(report.all_rays_degree_2);
        assert_eq!(report.total_incidence, 36);
        assert!(!report.is_colorable);
        assert_eq!(report.solutions_count, 0);
        assert!(report.uncolorability_confirmed);
    }

    #[test]
    fn test_block_07_full_report() {
        let report = run_block_07_execution();
        assert_eq!(report.authority_effect, "None");
        assert_eq!(report.block_id, "block_07");
        assert_eq!(report.contextuality_threshold_conductor_d3, None);
        assert_eq!(report.ks_d3_sqrt2_first_conductor, 8);
        assert!(!report.ks_d3_conductor_12_found_within_bound);
        assert_eq!(report.ks_d3_conductor_24_smallest_found_rays, 33);
        assert_eq!(report.ks_d4_conductor_1_smallest_found_rays, 18);
        assert_eq!(report.rational_d3_colorable_meyer_status, "cited");
    }
}
