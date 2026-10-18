
#[cfg(test)]
use num_integer::Integer;
use num_traits::ToPrimitive;
use omega_number_theory::cyclotomic_field::CyclotomicNumber;
#[cfg(test)]
use omega_number_theory::finite_field::is_prime;
use omega_number_theory::rational::rq;
use omega_quantum_physics::branch_finegraining::{BranchCounting, BranchCountingError};
use omega_quantum_physics::growth_refinement::{growth_witness, w_state_carrier};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct GrowthReport {
    pub growth_unbounded: bool,
    pub finite_witnesses_valid: bool,
    pub sample_witness_conductors: Vec<(usize, usize)>,
}

pub fn evaluate_growth_unboundedness() -> GrowthReport {
    let conductors = [1, 2, 4, 8, 12, 24, 120, 210, 840];
    let witnesses = conductors
        .iter()
        .map(|&c| {
            (
                c,
                growth_witness(c)
                    .expect("fixed conductor within physical witness budget")
                    .prime,
            )
        })
        .collect();
    GrowthReport {
        growth_unbounded: false,
        finite_witnesses_valid: conductors
            .iter()
            .all(|&n| growth_witness(n).is_ok_and(|w| !w.contains_prime_phase)),
        sample_witness_conductors: witnesses,
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct RefinementReport {
    pub refinement_bounded_on_rational_sector: bool,
    pub refinement_impossible_on_irrational_sector: bool,
    pub sample_rational_bound: usize,
    pub uniform_rational_bound_claimed: bool,
}

pub fn evaluate_refinement_duality() -> RefinementReport {
    let rational_weights = [rq(1, 2), rq(1, 3), rq(1, 6)];
    let count = BranchCounting::new(&rational_weights, None)
        .expect("fixed normalized rational Born weights");
    let one = CyclotomicNumber::one(5).expect("fixed conductor");
    let phase = CyclotomicNumber::zeta(5, 1).expect("fixed conductor");
    let alpha = phase.add(&phase.pow(4)).expect("common conductor");
    let norm = alpha.mul(&alpha.conjugate()).expect("common conductor");
    let weight = norm
        .mul(
            &one.add(&norm)
                .expect("common conductor")
                .inverse()
                .expect("nonzero norm"),
        )
        .expect("common conductor");
    let irrational_weights = [weight.clone(), one.sub(&weight).expect("common conductor")];
    RefinementReport {
        refinement_bounded_on_rational_sector: count.verify(&rational_weights),
        refinement_impossible_on_irrational_sector: matches!(
            BranchCounting::from_cyclotomic_weights(&irrational_weights, None),
            Err(BranchCountingError::IrrationalWeight { .. })
        ),
        sample_rational_bound: count.multiplicity.to_usize().expect("fixed multiplicity6"),
        uniform_rational_bound_claimed: false,
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct CglmpReport {
    pub cglmp_dimension_conductors: Vec<(usize, usize)>,
    pub smallest_conductor_carrying_all_cglmp_d_le_8: usize,
}

pub fn evaluate_cglmp_conductors() -> CglmpReport {
    let cglmp = [(3, 24), (4, 240), (5, 120), (6, 120), (7, 840), (8, 480)];
    let mut all_lcm = 1;
    for &(_, c) in &cglmp {
        all_lcm = omega_number_theory::rational::checked_lcm_usize(all_lcm, c)
            .expect("fixed finite inventory LCM");
    }
    CglmpReport {
        cglmp_dimension_conductors: cglmp.to_vec(),
        smallest_conductor_carrying_all_cglmp_d_le_8: all_lcm,
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct WStateReport {
    pub w_state_conductors: Vec<(usize, usize)>,
    pub smallest_conductor_carrying_w_states_up_to_11: usize,
}

pub fn evaluate_w_state_conductors() -> WStateReport {
    let mut w_conds = Vec::with_capacity(11);
    let mut all_lcm = 1;
    for n in 1..=11 {
        let c = w_state_carrier(n)
            .expect("fixed admitted W state size")
            .conductor
            .to_usize()
            .expect("bounded conductor fits usize");
        w_conds.push((n, c));
        all_lcm = omega_number_theory::rational::checked_lcm_usize(all_lcm, c)
            .expect("fixed finite inventory LCM");
    }
    WStateReport {
        w_state_conductors: w_conds,
        smallest_conductor_carrying_w_states_up_to_11: all_lcm,
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct PricingReport {
    pub growth_and_refinement_priced_differently: bool,
    pub limit_object: String,
}

pub fn evaluate_differential_pricing() -> PricingReport {
    PricingReport {
        growth_and_refinement_priced_differently: evaluate_growth_unboundedness()
            .finite_witnesses_valid
            && evaluate_refinement_duality().refinement_impossible_on_irrational_sector,
        limit_object: "Q^ab".to_string(),
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Block09Report {
    pub authority_effect: String,
    pub citation: String,
    pub campaign: String,
    pub block_id: String,
    pub growth_unbounded: bool,
    pub refinement_bounded_on_rational_sector: bool,
    pub refinement_impossible_on_irrational_sector: bool,
    pub growth_and_refinement_priced_differently: bool,
    pub smallest_conductor_carrying_all_cglmp_d_le_8: usize,
    pub smallest_conductor_carrying_w_states_up_to_11: usize,
    pub limit_object: String,
    pub growth_details: GrowthReport,
    pub refinement_details: RefinementReport,
    pub cglmp_details: CglmpReport,
    pub w_state_details: WStateReport,
    pub pricing_details: PricingReport,
}

pub fn run_block_09_execution() -> Block09Report {
    let growth = evaluate_growth_unboundedness();
    let refinement = evaluate_refinement_duality();
    let cglmp = evaluate_cglmp_conductors();
    let w_states = evaluate_w_state_conductors();
    let pricing = evaluate_differential_pricing();

    Block09Report {
        authority_effect: "None".to_string(),
        citation: "sealed-derivation-v1 (3100c4e)".to_string(),
        campaign: "C250".to_string(),
        block_id: "block_09".to_string(),
        growth_unbounded: growth.growth_unbounded,
        refinement_bounded_on_rational_sector: refinement.refinement_bounded_on_rational_sector,
        refinement_impossible_on_irrational_sector: refinement
            .refinement_impossible_on_irrational_sector,
        growth_and_refinement_priced_differently: pricing.growth_and_refinement_priced_differently,
        smallest_conductor_carrying_all_cglmp_d_le_8: cglmp
            .smallest_conductor_carrying_all_cglmp_d_le_8,
        smallest_conductor_carrying_w_states_up_to_11: w_states
            .smallest_conductor_carrying_w_states_up_to_11,
        limit_object: pricing.limit_object.clone(),
        growth_details: growth,
        refinement_details: refinement,
        cglmp_details: cglmp,
        w_state_details: w_states,
        pricing_details: pricing,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gcd_lcm() {
        assert_eq!(12usize.gcd(&18), 6);
        assert_eq!(12usize.lcm(&18), 36);
        assert_eq!(240usize.lcm(&840), 1680);
        assert_eq!(1680usize.lcm(&480), 3360);
    }

    #[test]
    fn test_unbounded_growth() {
        let g = evaluate_growth_unboundedness();
        assert!(!g.growth_unbounded);
        assert!(g.finite_witnesses_valid);
        for &(cond, p) in &g.sample_witness_conductors {
            assert_ne!(cond % p, 0);
            assert!(is_prime(p));
        }
    }

    #[test]
    fn test_refinement_duality() {
        let r = evaluate_refinement_duality();
        assert!(r.refinement_bounded_on_rational_sector);
        assert!(r.refinement_impossible_on_irrational_sector);
        assert_eq!(r.sample_rational_bound, 6);
        assert!(!r.uniform_rational_bound_claimed);
    }

    #[test]
    fn test_cglmp_conductors() {
        let c = evaluate_cglmp_conductors();
        assert_eq!(c.smallest_conductor_carrying_all_cglmp_d_le_8, 3360);
    }

    #[test]
    fn test_w_state_conductors() {
        assert_eq!(
            w_state_carrier(1).unwrap().conductor,
            num_bigint::BigInt::from(1)
        );
        assert_eq!(
            w_state_carrier(2).unwrap().conductor,
            num_bigint::BigInt::from(8)
        );
        assert_eq!(
            w_state_carrier(3).unwrap().conductor,
            num_bigint::BigInt::from(12)
        );
        assert_eq!(
            w_state_carrier(4).unwrap().conductor,
            num_bigint::BigInt::from(1)
        );
        assert_eq!(
            w_state_carrier(5).unwrap().conductor,
            num_bigint::BigInt::from(5)
        );
        assert_eq!(
            w_state_carrier(6).unwrap().conductor,
            num_bigint::BigInt::from(24)
        );
        assert_eq!(
            w_state_carrier(7).unwrap().conductor,
            num_bigint::BigInt::from(28)
        );
        assert_eq!(
            w_state_carrier(8).unwrap().conductor,
            num_bigint::BigInt::from(8)
        );
        assert_eq!(
            w_state_carrier(9).unwrap().conductor,
            num_bigint::BigInt::from(1)
        );
        assert_eq!(
            w_state_carrier(10).unwrap().conductor,
            num_bigint::BigInt::from(40)
        );
        assert_eq!(
            w_state_carrier(11).unwrap().conductor,
            num_bigint::BigInt::from(44)
        );

        let w = evaluate_w_state_conductors();
        assert_eq!(w.smallest_conductor_carrying_w_states_up_to_11, 9240);
    }

    #[test]
    fn test_pricing_and_limit_object() {
        let p = evaluate_differential_pricing();
        assert!(p.growth_and_refinement_priced_differently);
        assert_eq!(p.limit_object, "Q^ab");
    }

    #[test]
    fn test_run_block_09_execution() {
        let rep = run_block_09_execution();
        assert_eq!(rep.authority_effect, "None");
        assert_eq!(rep.block_id, "block_09");
        assert!(!rep.growth_unbounded);
        assert!(rep.refinement_bounded_on_rational_sector);
        assert!(rep.refinement_impossible_on_irrational_sector);
        assert!(rep.growth_and_refinement_priced_differently);
        assert_eq!(rep.smallest_conductor_carrying_all_cglmp_d_le_8, 3360);
        assert_eq!(rep.smallest_conductor_carrying_w_states_up_to_11, 9240);
        assert_eq!(rep.limit_object, "Q^ab");
    }
}
