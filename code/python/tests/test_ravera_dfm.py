# AuthorityEffect: None.
"""Verification tests for the self-contained Ravera DFM Finite-to-Continuum Dossier."""

from __future__ import annotations

import importlib.util
import re
import sys
from fractions import Fraction
from pathlib import Path

try:
    from src.qm.campaigns import ravera_dfm as _MOD
except ImportError:
    _REPLAY_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "campaigns" / "ravera_dfm.py"
    _SPEC = importlib.util.spec_from_file_location("ravera_dfm", _REPLAY_PATH)
    assert _SPEC is not None and _SPEC.loader is not None
    _MOD = importlib.util.module_from_spec(_SPEC)
    _SPEC.loader.exec_module(_MOD)

REPLAY_PATH = Path(_MOD.__file__).resolve()
REPO_ROOT = Path(__file__).resolve().parents[3]


def test_pillar1_abelian_tree_dfm_and_symanzik_u() -> None:
    p1 = _MOD.verify_pillar1_abelian_tree_dfm_and_symanzik_u()
    assert p1["spanning_tree_count"] == 8
    assert p1["first_betti_number"] == 2
    assert p1["u_diamond_unit"] == Fraction(8, 1)
    assert p1["u_diamond_prime_weights"] == Fraction(247, 1)
    assert p1["all_tree_edges_neutralized"] is True
    assert p1["dressed_connection_gauge_invariant"] is True
    assert p1["all_tree_changes_unimodular_gl2z"] is True


def test_pillar2_nonabelian_borel_two_stage_dfm() -> None:
    p2 = _MOD.verify_pillar2_nonabelian_borel_two_stage_dfm()
    assert p2["artificial_all_edges_neutralized"] is True
    assert p2["substantial_tree_edges_neutralized"] is True
    assert p2["substantial_cotree_holonomy_nontrivial"] is True
    assert p2["stage1_all_in_unipotent_normal_subgroup"] is True
    assert p2["stage1_tree_reduced_to_diagonal_torus"] is True
    assert p2["two_stage_factorization_matches_full_tree_dressing"] is True


def test_pillar3_symanzik_two_forest_and_bphz() -> None:
    p3 = _MOD.verify_pillar3_symanzik_two_forest_and_bphz()
    assert p3["diamond_two_forest_count"] == 10
    assert p3["diamond_u"] == Fraction(247, 1)
    assert p3["diamond_f0"] == Fraction(31153, 1)
    assert p3["dfm_all_eight_trees_match_f0_and_u"] is True
    assert p3["bphz_uv_boundary_poles_cancel_identically"] is True
    assert p3["bphz_uv_boundary_regular_value_at_zero"] == Fraction(9, 25)


def test_pillar4_dressed_dirac_and_ward_takahashi() -> None:
    p4 = _MOD.verify_pillar4_dressed_dirac_and_ward_takahashi()
    assert p4["bare_correlator_gauge_dependent"] is True
    assert p4["dfm_dressed_correlator_gauge_invariant_all_trees"] is True
    assert p4["ward_takahashi_inverse_propagator_diff_exact"] is True
    assert p4["z1_over_z2_ratio"] == Fraction(1, 1)


def test_pillar5_page_wootters_clock_dressing() -> None:
    p5 = _MOD.verify_pillar5_page_wootters_clock_dressing()
    assert p5["clock_dimension"] == 4
    assert p5["dressed_history_recovers_static_system_state"] is True
    assert p5["clock_dressing_intertwines_wheeler_dewitt_operator"] is True


def test_pillar6_electroweak_doublet_dfm() -> None:
    p6 = _MOD.verify_pillar6_electroweak_doublet_dfm()
    assert p6["dressed_higgs_unitary_gauge_exact"] is True
    assert p6["sin2_theta_w"] == Fraction(16, 25)
    assert p6["cos2_theta_w"] == Fraction(9, 25)
    assert p6["custodial_rho_ew"] == Fraction(1, 1)
    assert p6["cubic_hypercharge_anomaly_nc3"] == Fraction(0, 1)
    assert p6["cubic_hypercharge_anomaly_nc2"] != Fraction(0, 1)


def test_pillar7_ckm_jarlskog_bipartite_dfm() -> None:
    p7 = _MOD.verify_pillar7_ckm_jarlskog_bipartite_dfm()
    assert p7["ng2_removed_tree_phases"] == 3
    assert p7["ng2_physical_cp_phases"] == 0
    assert p7["ng3_removed_tree_phases"] == 5
    assert p7["ng3_physical_cp_phases"] == 1
    assert p7["two_gen_jarlskog_invariant"] == Fraction(0, 1)
    assert p7["three_gen_jarlskog_invariant"] == Fraction(5184, 78125)
    assert p7["all_nine_jarlskog_quartets_rephasing_invariant"] is True


def test_pillar8_su3_spanning_tree_vs_landau_gribov() -> None:
    p8 = _MOD.verify_pillar8_su3_spanning_tree_vs_landau_gribov()
    assert p8["su3_edge_links_unitary_det_one"] is True
    assert p8["su3_connection_non_abelian"] is True
    assert p8["dfm_all_eight_trees_neutralize_tree_edges"] is True
    assert p8["dfm_dressed_cotree_holonomies_gauge_invariant"] is True
    assert p8["anchored_landau_gribov_copy_count"] == 64
    assert p8["nontrivial_landau_gribov_copy_count"] == 63
    assert p8["all_gribov_copies_satisfy_discrete_landau_divergence_zero"] is True
    assert p8["gribov_horizon_hessian_flips_sign_to_negative"] is True
    assert p8["dfm_collapses_all_64_gribov_copies_to_single_dressed_state"] is True


def test_pillar9_cartan_regge_lorentz_tetrad_dfm() -> None:
    p9 = _MOD.verify_pillar9_cartan_regge_lorentz_tetrad_dfm()
    assert p9["boost_preserves_minkowski_metric"] is True
    assert p9["boost_velocity_addition_group_law_holds"] is True
    assert p9["induced_spacetime_metric_lorentz_invariant"] is True
    assert p9["dressed_levi_civita_connection_lorentz_invariant"] is True
    assert p9["dressed_connection_metric_compatible"] is True
    assert p9["artificial_hinge_holonomy_is_identity"] is True
    assert p9["substantial_hinge_boost_plane_trace"] == Fraction(10, 3)
    assert p9["substantial_hinge_holonomy_trace"] == Fraction(16, 3)
    assert p9["substantial_hinge_dressed_trace_matches_spin_trace"] is True
    assert p9["discrete_bianchi_identity_holds_around_3cell"] is True


def test_master_dossier_replay_and_self_containment() -> None:
    summary = _MOD.evaluate_ravera_dfm_dossier()
    assert summary["all_nine_pillars_pass"] is True

    replay_src = REPLAY_PATH.read_text(encoding="utf-8")
    assert "sys.path" not in replay_src

    lean_path = REPO_ROOT / "research" / "lean4" / "RaveraDfmFiniteToContinuum.lean"
    if not lean_path.is_file():
        lean_path = REPO_ROOT / "lean" / "RaveraDfmFiniteToContinuum.lean"
    rust_path = REPO_ROOT / "code" / "rust" / "src" / "qm" / "campaigns" / "ravera_dfm.rs"
    assert lean_path.is_file()
    assert rust_path.is_file()
    assert "sorry" not in lean_path.read_text(encoding="utf-8")

    desc_file = REPO_ROOT / "research" / "ravera_dfm_docs.md"
    if desc_file.is_file():
        desc_text = desc_file.read_text(encoding="utf-8")
        assert "descriptions.md" in desc_text

    # Verify zero in-house ticket codes or external repository paths in dossier markdown files
    in_house_pattern = re.compile(r"\b(?:QM-\d+|M-\d+|DFM-NEXT|CODA|omega_engine|omega_quantum_physics)\b")
    for md_file in (
        REPO_ROOT / "research" / "ravera_dfm_dossier.md",
        REPO_ROOT / "research" / "ravera_dfm_changes.md",
    ):
        if md_file.is_file():
            for line_num, line in enumerate(md_file.read_text(encoding="utf-8").splitlines(), 1):
                m = in_house_pattern.search(line)
                assert m is None, f"{md_file.name}:{line_num} contains forbidden pattern '{m.group(0)}'"
