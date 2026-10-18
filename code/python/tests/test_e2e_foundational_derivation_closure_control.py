# AuthorityEffect: None.
"""End-to-end tests for QM-219 Foundational Derivation Closure (FQM-COMPOSITION-IMPORT, FQM-IMPORT-INDEPENDENCE, FQM-QM208-READOUT-CLASS)."""

from __future__ import annotations

from fractions import Fraction

from finite_qm.use_cases.foundational_derivation_closure_control import (
    QZeta12,
    _certified_sqrt3_interval,
    evaluate_foundational_derivation_closure_control,
)


def test_part_a_bipartite_composition_triad_separation() -> None:
    """Verify exact separation of direct-sum, tensor-product PSD, and PR-box composition laws."""
    report = evaluate_foundational_derivation_closure_control()
    comp = report.bipartite_composition
    assert comp.direct_sum_dim == 4
    assert comp.tensor_product_dim == 4
    assert comp.direct_sum_local_params == 6
    assert comp.tensor_product_local_tomography_params == 15
    assert comp.direct_sum_max_chsh_sq == Fraction(4)
    assert comp.tensor_product_tsirelson_chsh_sq == Fraction(8)
    assert comp.pr_box_no_signaling_holds
    assert comp.pr_box_chsh_value == Fraction(4)
    assert comp.pr_box_chsh_sq == Fraction(16)
    assert comp.pr_box_violates_landau_sos_bound
    assert comp.composition_independent_of_single_system_imports


def test_part_b_five_import_mutual_independence_matrix() -> None:
    """Verify the 5x5 countermodel matrix has False on the diagonal and True off the diagonal."""
    report = evaluate_foundational_derivation_closure_control()
    ind = report.import_independence
    assert len(ind.import_ids) == 5
    assert len(ind.countermodel_ids) == 5
    matrix = ind.admission_matrix
    assert len(matrix) == 5
    for i in range(5):
        assert len(matrix[i]) == 5
        for j in range(5):
            if i == j:
                assert matrix[i][j] is False
            else:
                assert matrix[i][j] is True
    assert ind.diagonal_all_false
    assert ind.off_diagonal_all_true
    assert ind.drop_207_real_tomography_mismatch == (8, 9)
    assert ind.drop_208_quartic_sorkin_i3_value == Fraction(36)
    assert ind.drop_209_commutative_max_commutator_norm == Fraction(0)
    assert ind.drop_210_quasi_state_negative_value == Fraction(-1, 8)
    assert ind.drop_211_singular_step_det == Fraction(0)


def test_part_c_z_zeta12_unit_identity_and_invariant_quadratic_subspace() -> None:
    """Verify (zeta - 1)^{-1} = -zeta^2 - zeta^3 and rank-8 / nullity-2 Sym^2 invariance."""
    z = QZeta12.zeta()
    one = QZeta12.one()
    inv_z_minus_1 = QZeta12.from_ints(0, 0, -1, -1)
    assert (z - one) * inv_z_minus_1 == one

    s3 = QZeta12.from_ints(0, 2, 0, -1)
    assert s3 * s3 == QZeta12.from_ints(3, 0, 0, 0)
    assert s3.galois_sqrt3_flip() == QZeta12.from_ints(0, -2, 0, 1)

    zk = one
    for _ in range(12):
        assert zk * zk.conj() == one
        zk = zk * z
    assert zk == one


def test_part_c_fundamental_unit_cone_and_twelve_decimal_enclosures() -> None:
    """Verify fundamental unit 2 + sqrt(3) positivity cone and 12-decimal RationalInterval enclosures."""
    report = evaluate_foundational_derivation_closure_control()
    z12 = report.z_zeta12_readout_class
    assert z12.cyclotomic_degree == 4
    assert z12.zeta_minus_one_unit_inverse_holds
    assert z12.linear_part_forced_zero
    assert z12.sym2_total_dim == 10
    assert z12.mu12_action_rank_on_sym2 == 8
    assert z12.mu12_invariant_quadratic_dim == 2
    assert z12.norm_pair_matches_x_conj_x
    assert z12.fundamental_unit_norm_one
    assert z12.unit_v_plus_n0_n1 == (Fraction(7), Fraction(4))
    assert z12.unit_v_minus_n0_n1 == (Fraction(7), Fraction(-4))
    assert z12.positivity_iff_alpha_beta_nonneg
    assert z12.rational_valued_iff_alpha_eq_beta
    assert z12.rational_valued_iff_ab_rational
    assert z12.counterexample_ab_1_1_gram_minors == (
        Fraction(1),
        Fraction(3, 4),
        Fraction(1, 2),
        Fraction(1, 4),
    )
    assert z12.counterexample_ab_1_1_positive_definite_unequal_weights
    assert z12.galois_invariance_selects_equal_weights
    assert report.import_independence.quartic_disagrees_with_born_on_superposition
    assert report.import_independence.three_ray_proxy_passes_but_one_one_ray_negative

    sqrt3_iv = _certified_sqrt3_interval()
    assert sqrt3_iv.lo * sqrt3_iv.lo <= Fraction(3) <= sqrt3_iv.hi * sqrt3_iv.hi
    assert report.enclosure_max_width < Fraction(1, 10**14)
    assert report.sqrt3_12dec == "1.732050807568"
    assert report.unit_2_plus_sqrt3_12dec == "3.732050807568"
    assert report.unit_2_minus_sqrt3_12dec == "0.267949192431"
    assert report.five_import_rust_parity_verified
    assert report.all_checks_passed


def test_part_d_finite_qm_lean4_mechanization_parity() -> None:
    """Verify FiniteQM.lean formalizes the degree-4 unit-sphere basis identity and 2x2 Rat countermodels with zero sorry."""
    import re
    from pathlib import Path

    paper_root = Path(__file__).resolve().parents[3]
    local_lean = paper_root / "code" / "lean4" / "FiniteQM.lean"
    if not local_lean.is_file():
        local_lean = Path(__file__).resolve().parents[3] / "lean4" / "FiniteQM.lean"
        if not local_lean.is_file():
            local_lean = Path(__file__).resolve().parents[3] / "lean" / "FiniteQM.lean"
    assert local_lean.is_file(), f"Missing {local_lean}"
    text = local_lean.read_text(encoding="utf-8")
    assert re.search(r"\bsorry\b", text) is None
    assert "theorem degree4_unit_sphere_basis_identity" in text
    assert "theorem p4_eq_one_sub_two_p22_on_unit_sphere" in text
    assert "theorem quadratic_readout_selected_in_sym_deg4_class" in text
    assert "theorem qzeta12_rational_readout_cone_and_galois_selection" in text
    assert "theorem born_trace_vs_quartic_readout_and_three_ray_positivity_gap" in text
    assert "theorem countermodel_matrix_diagonal_all_false" in text
    assert "theorem countermodel_matrix_off_diagonal_all_true" in text
    assert "theorem five_import_mutual_independence" in text

    repo_root = Path(r"c:/Users/a343o/source/repos/the_symbol_game")
    canonical_lean = repo_root / "lean4" / "quantum_mechanics" / "FiniteQM.lean"
    if canonical_lean.is_file():
        assert canonical_lean.read_bytes() == local_lean.read_bytes()


def test_part_e_derivation_dag_dual_home_parity() -> None:
    """Verify DerivationDagQMClosure.lean and derivation_dag_witnesses.rs exist in 006_finite_qm and match workspace crates byte-for-byte."""
    import re
    from pathlib import Path

    paper_root = Path(__file__).resolve().parents[3]
    local_dag_lean = paper_root / "code" / "lean4" / "DerivationDagQMClosure.lean"
    local_dag_rs = paper_root / "code" / "rust" / "src" / "derivation_dag_witnesses.rs"
    if not local_dag_lean.is_file():
        local_dag_lean = Path(__file__).resolve().parents[3] / "lean4" / "DerivationDagQMClosure.lean"
        if not local_dag_lean.is_file():
            local_dag_lean = Path(__file__).resolve().parents[3] / "lean" / "DerivationDagQMClosure.lean"
    if not local_dag_rs.is_file():
        local_dag_rs = paper_root / "code" / "rust" / "src" / "dag_witnesses.rs"
    if not local_dag_rs.is_file():
        local_dag_rs = Path(__file__).resolve().parents[2] / "native" / "src" / "derivation_dag_witnesses.rs"
    assert local_dag_lean.is_file(), f"Missing {local_dag_lean}"
    assert local_dag_rs.is_file(), f"Missing {local_dag_rs}"

    lean_text = local_dag_lean.read_text(encoding="utf-8")
    assert re.search(r"\bsorry\b", lean_text) is None
    for thm in (
        "theorem gs003_coordinate_l1_weighted_sum_and_orbit_collapse",
        "theorem gs001_maximal_symmetry_direction_independence_and_gauge_proportionality",
        "theorem wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation",
        "theorem l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure",
        "theorem ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization",
        "theorem ds_qm072_bit_shadow_q1_q4_obstruction_and_p7_c10_bloch_refutation",
        "theorem ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction",
        "theorem ds_qm090_093_o022_registry_minimality_and_tier3_pr_box_bridge",
        "theorem ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity",
        "theorem ds_qm094_everett_reduced_state_overlap_isometric_refinement_and_collapse_refutation",
        "theorem ds_qm101_threshold_repair_image_monotonicity_and_nogo_suppression_corollary",
        "theorem ds_qm206_four_tier_cochain_exactness_holonomy_invariance_and_nonfull_nonfaithful_descent",
        "theorem ds_qm032_feynman_refinement_compatibility_terminalizer_and_two_slice_action",
        "theorem ds_qm033_hermitian_graph_schrodinger_mass_conservation_and_lggr_holonomy",
        "theorem ds_qm073_diagonal_exchange_suppression_and_bell_three_clause_obstruction",
        "theorem ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade",
        "theorem pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl",
        "theorem l1_residual_sector_weights_minimizer_nonuniqueness_and_dihedral_selector",
        "theorem l1_qm122_leftover_mnc_eight_extra_finish_table_and_dilation_classifications",
        "theorem fq_embedding_relativity_and_entropy_baker_dichotomy_closure",
    ):
        assert thm in lean_text, f"Missing {thm} in {local_dag_lean}"

    rs_text = local_dag_rs.read_text(encoding="utf-8")
    assert "pub fn verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness" in rs_text
    assert "pub fn verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness" in rs_text
    assert "pub fn verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness" in rs_text
    assert "pub fn verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness" in rs_text
    assert "pub fn verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness" in rs_text

    repo_root = Path(r"c:/Users/a343o/source/repos/the_symbol_game")
    canonical_dag_lean = repo_root / "lean4" / "quantum_mechanics" / "DerivationDagQMClosure.lean"
    if canonical_dag_lean.is_file():
        assert canonical_dag_lean.read_bytes() == local_dag_lean.read_bytes()

    for crate_rel in (
        Path("omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs"),
        Path("omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs"),
    ):
        crate_rs = repo_root / crate_rel
        if crate_rs.is_file():
            assert crate_rs.read_bytes() == local_dag_rs.read_bytes()



