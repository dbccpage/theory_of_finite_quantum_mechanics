// AuthorityEffect: None.
//! Ravera DFM Finite-to-Continuum Dossier verification module (Theorems 3.7, 3.8, 3.9).

pub use omega_quantum_physics::quantum_import_finite_maps::ravera_dfm_finite_to_continuum::*;

#[cfg(test)]
mod ravera_dfm_tests {
    use super::*;
    use num_rational::Ratio;

    fn q(n: i64, d: i64) -> Ratio<i64> {
        Ratio::new(n, d)
    }

    #[test]
    fn test_ckm_jarlskog_bipartite_dfm_control() {
        let r = evaluate_ckm_jarlskog_bipartite_dfm_control();
        assert_eq!(r.ng2_removed_tree_phases, 3);
        assert_eq!(r.ng2_substantial_cycle_phases, 1);
        assert_eq!(r.ng3_removed_tree_phases, 5);
        assert_eq!(r.ng3_substantial_cycle_phases, 4);
        assert_eq!(r.ng4_removed_tree_phases, 7);
        assert_eq!(r.ng4_substantial_cycle_phases, 9);
        assert!(r.two_gen_cabibbo_unitary);
        assert!(r.two_gen_dressed_entries_real_positive);
        assert_eq!(r.two_gen_jarlskog_zero, q(0, 1));
        assert!(r.three_gen_ckm_unitary);
        assert!(r.three_gen_ckm_det_unit_norm);
        assert!(r.three_gen_all_nine_quartets_rephasing_invariant);
        assert_eq!(r.three_gen_jarlskog_invariant, q(5184, 78125));
    }

    #[test]
    fn test_su3_spanning_tree_vs_landau_gribov_control() {
        let r = evaluate_su3_spanning_tree_vs_landau_gribov_control();
        assert!(r.su3_edge_links_all_unitary_det_one);
        assert!(r.su3_connection_non_abelian);
        assert!(r.dfm_all_eight_trees_neutralize_tree_edges);
        assert!(r.dfm_dressed_cotree_holonomies_gauge_invariant);
        assert!(r.dfm_second_kind_tree_change_intertwiner_exact);
        assert!(r.klein_four_gribov_elements_in_su3);
        assert_eq!(r.anchored_landau_gribov_copy_count, 64);
        assert_eq!(r.nontrivial_landau_gribov_copy_count, 63);
        assert!(r.all_gribov_copies_satisfy_discrete_landau_divergence_zero);
        assert!(r.gribov_horizon_hessian_flips_sign_to_negative);
        assert!(r.dfm_collapses_all_64_gribov_copies_to_single_dressed_state);
    }

    #[test]
    fn test_cartan_regge_lorentz_tetrad_dfm_control() {
        let r = evaluate_cartan_regge_lorentz_tetrad_dfm_control();
        assert!(r.boost_preserves_minkowski_metric);
        assert!(r.boost_determinant_exact_one);
        assert!(r.boost_velocity_addition_group_law_holds);
        assert!(r.spatial_rotation_preserves_minkowski_metric);
        assert!(r.induced_spacetime_metric_lorentz_invariant);
        assert!(r.dressed_levi_civita_connection_lorentz_invariant);
        assert!(r.dressed_connection_metric_compatible);
        assert!(r.artificial_hinge_holonomy_is_identity);
        assert_eq!(r.substantial_hinge_boost_plane_trace, q(10, 3));
        assert_eq!(r.substantial_hinge_holonomy_trace, q(16, 3));
        assert!(r.substantial_hinge_dressed_trace_matches_spin_trace);
        assert!(r.discrete_bianchi_identity_holds_around_3cell);
    }
}
