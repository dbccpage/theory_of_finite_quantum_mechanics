
extern crate self as omega_finite_probability;
pub mod bell_joint_extension;
pub mod bell_separator_extension;
pub mod pfp_exact;
pub mod rational_bell;
pub mod born_ray;
pub mod frame_polytope;
pub mod cabello_certificates;
pub mod cabello_obstruction;
pub mod carrier_contract;
pub mod classical_instrument;
pub mod error;
pub mod finite_set;
pub mod joint_table;
pub mod log_form;
pub mod majorization;
pub mod markov_chain;
pub mod paired_tests;
pub mod simplex;
pub mod stochastic_map;

#[cfg(test)]
mod test_support;

pub mod finite_valuation;

pub mod local_deterministic;
pub mod marginal_compatibility;
pub mod signed_representation;

use num_rational::Ratio;
use num_traits::Zero;

pub fn verify_distribution_sum(probs: &[Ratio<i64>]) -> bool {
    let mut sum = Ratio::zero();
    for p in probs {
        if *p < Ratio::zero() {
            return false;
        }
        sum += *p;
    }
    sum == Ratio::from_integer(1)
}

#[cfg(test)]
mod prob_tests {
    use super::*;

    #[test]
    fn test_verify_distribution() {
        let dist = vec![Ratio::new(1, 3), Ratio::new(2, 3)];
        assert!(verify_distribution_sum(&dist));
    }
}

pub mod cech_f2;

pub mod declared_interface;

pub mod entropy_exact;

pub mod born_gap;

pub mod c500_ledger;

pub mod phase_scope;

pub mod structure_exact;

pub mod dynamics_exact;

pub mod resources_exact;

pub mod boundaries_exact;

pub mod genesis_impl_exact;

pub mod l1_import_exact;

pub mod born_boundary_exact;

pub mod pfp_phase_blind_fiber;
pub mod pfp_residual_sector_weights;
pub mod pfp_u1_selector_segment;
pub mod pfp_realification_j;
pub mod pfp_obligation_monoid;
pub mod pfp_sn_carrier;
pub mod pfp_admission_floor;
pub mod pfp_chain_retraction;
pub mod pfp_collapse_barrier;
pub mod pfp_demand_accounting;
pub mod pfp_free_monoid_noniso;
pub mod pfp_history_report;
pub mod pfp_inert_diamond;
pub mod pfp_old_image_injective;
pub mod pfp_pregen_constructive;
pub mod pfp_primdiff_axioms;
pub mod pfp_refine_separates;
pub mod pfp_root_diff_structure;
pub mod pfp_six_operations;
pub mod pfp_sn_off_image;
pub mod pfp_wdp_degree1_window;
pub mod pfp_wdp_diagnostic_routing;
pub mod pfp_wdp_bridge_obligations;
pub mod pfp_wdp_growth_no_repair;
pub mod pfp_wdp_protected_questions;
pub mod pfp_wdp_quotient_sequence;
