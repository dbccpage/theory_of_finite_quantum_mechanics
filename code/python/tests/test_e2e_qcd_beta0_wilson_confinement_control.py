"""E2E verification suite for QM-221: Finite su(3)_c QCD Gross-Wilczek-Politzer
Asymptotic Freedom (beta_0 = 11 - 2/3 n_f, beta_1 = 102 - 38/3 n_f), Rational-Weighted
Gell-Mann Fierz Completeness, and Finite-Graph Wilson-Loop Confinement Witness over Q.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from finite_qm.use_cases.qcd_beta0_wilson_confinement_control import (
    evaluate_qm221_qcd_beta0_wilson_confinement,
    summarize_qm221_qcd_beta0_wilson_confinement,
)


def test_part_a_su3_gell_mann_casimirs_and_fierz_completeness() -> None:
    r = evaluate_qm221_qcd_beta0_wilson_confinement()
    assert r.color_dimension_nc == 3
    assert r.gluon_generator_count == 8
    assert r.all_generators_hermitian_and_traceless is True
    assert r.killing_orthogonality_holds is True
    assert r.jacobi_identity_holds_all_triples is True
    assert r.fundamental_trace_normalization_tf == Fraction(1, 2)
    assert r.fundamental_casimir_cf == Fraction(4, 3)
    assert r.fundamental_casimir_proportional_to_identity is True
    assert r.adjoint_casimir_ca == Fraction(3, 1)
    assert r.adjoint_casimir_holds_on_all_generators is True
    assert r.fierz_completeness_holds_all_81_entries is True
    assert r.singlet_qqbar_casimir_coeff == Fraction(-4, 3)
    assert r.octet_qqbar_casimir_coeff == Fraction(1, 6)
    assert r.sextet_qq_casimir_coeff == Fraction(1, 3)
    assert r.antitriplet_qq_casimir_coeff == Fraction(-2, 3)
    assert r.singlet_attractive_and_octet_repulsive is True


def test_part_b_gross_wilczek_politzer_beta0_and_banks_zaks_ratio() -> None:
    r = evaluate_qm221_qcd_beta0_wilson_confinement()
    assert r.gluon_paramagnetic_spin_contribution == Fraction(12, 1)
    assert r.gluon_diamagnetic_orbital_contribution == Fraction(-1, 1)
    assert r.gluon_total_beta0_contribution == Fraction(11, 1)
    assert r.fermion_single_dirac_beta0_contribution == Fraction(-2, 3)
    assert r.beta0_nf0_pure_yang_mills == Fraction(11, 1)
    assert r.beta0_nf3_light_quarks == Fraction(9, 1)
    assert r.beta0_nf5_at_mz == Fraction(23, 3)
    assert r.beta0_nf6_standard_model == Fraction(7, 1)
    assert r.beta0_nf16_conformal_edge == Fraction(1, 3)
    assert r.beta0_nf17_loss_of_af == Fraction(-1, 3)
    assert r.asymptotic_freedom_holds_for_nf_0_to_16 is True
    assert r.asymptotic_freedom_lost_at_nf_17 is True
    assert r.abelian_qed_beta0_nf1_is_negative is True
    assert r.beta1_nf0_pure_yang_mills == Fraction(102, 1)
    assert r.beta1_nf5_at_mz == Fraction(116, 3)
    assert r.beta1_nf16_banks_zaks == Fraction(-302, 3)
    assert r.banks_zaks_nf16_fixed_point_ratio == Fraction(1, 302)


def test_part_c_dfm_plaquette_reduction_and_wilson_creutz_confinement() -> None:
    r = evaluate_qm221_qcd_beta0_wilson_confinement()
    assert r.lattice_3x3_vertex_count == 9
    assert r.lattice_3x3_edge_count == 12
    assert r.lattice_3x3_spanning_tree_edges == 8
    assert r.lattice_3x3_independent_plaquette_betti1 == 4
    assert r.dfm_tree_dressing_reduces_links_to_plaquettes is True
    assert r.strong_coupling_expansion_parameter == Fraction(1, 9)
    assert r.creutz_area_ratio_r2_t2 == Fraction(1, 9)
    assert r.creutz_area_ratio_r3_t3 == Fraction(1, 9)
    assert r.creutz_area_ratio_constant_across_loops is True
    assert r.creutz_perimeter_ratio_r2_t2 == Fraction(1, 1)
    assert r.creutz_perimeter_ratio_r3_t3 == Fraction(1, 1)
    assert r.creutz_perimeter_ratio_is_unity is True
    assert r.area_law_strictly_confining_vs_perimeter is True


def test_part_d_12_decimal_alpha_s_and_string_tension_enclosures() -> None:
    r = evaluate_qm221_qcd_beta0_wilson_confinement()
    assert r.alpha_s_mz_input == Fraction(1179, 10000)
    assert r.alpha_s_at_ln_q2_mz2_eq_2_decimal_12 == "0.103072040480"
    assert r.alpha_s_at_ln_q2_mz2_eq_4_decimal_12 == "0.091557149048"
    assert r.alpha_s_12_digits_agree is True
    assert r.alpha_s_decreases_monotonically_in_uv is True
    assert r.string_tension_ln9_decimal_12 == "2.197224577336"
    assert r.string_tension_12_digits_agree is True

    summary = summarize_qm221_qcd_beta0_wilson_confinement()
    assert summary["control_id"] == "QM-221"
    assert summary["fierz_completeness_holds_all_81_entries"] is True
    assert summary["area_law_strictly_confining_vs_perimeter"] is True


def test_part_e_lean4_part4_and_fable_receipt_parity() -> None:
    paper_root = Path(__file__).resolve().parents[3]
    repo_root = Path(r"c:/Users/a343o/source/repos/the_symbol_game")
    canonical_lean = repo_root / "lean4/quantum_mechanics/FiniteQM.lean"
    paper_lean = paper_root / "lean/FiniteQM.lean"
    if not canonical_lean.is_file():
        canonical_lean = paper_root / "lean4" / "FiniteQM.lean" if (paper_root / "lean4" / "FiniteQM.lean").is_file() else paper_root / "lean" / "FiniteQM.lean"
    assert canonical_lean.is_file()
    assert paper_lean.is_file()
    text = canonical_lean.read_text(encoding="utf-8")
    assert text == paper_lean.read_text(encoding="utf-8")
    assert "sorry" not in text
    for thm_name in (
        "theorem su3_casimir_and_channel_identities",
        "theorem su3_fierz_diagonal_and_offdiagonal_identities",
        "theorem qcd_beta0_asymptotic_freedom_window",
        "theorem qcd_beta1_and_banks_zaks_fixed_point",
        "theorem wilson_creutz_ratio_area_vs_perimeter",
        "theorem wilson_lattice_3x3_dfm_betti_identity",
    ):
        assert thm_name in text, f"Missing Lean 4 theorem {thm_name}"

    receipt_path = paper_root / "research/qcd_beta0_wilson_confinement_fable_receipt.json"
    assert receipt_path.is_file()
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["campaign_id"] == "FABLE_5_1_MCTS_QM_221_QCD_BETA0_WILSON_CONFINEMENT"
    assert receipt["anthropic_messages_probe"]["status"] == "LIVE_OK"
    assert receipt["anthropic_messages_probe"]["model"] == "claude-fable-5-1"
    assert receipt["mcts_summary"]["checkpoint_count"] == 4
    assert receipt["mcts_summary"]["needs_backtrack"] is False
    expected_lean_sha = "sha256:" + hashlib.sha256(canonical_lean.read_bytes()).hexdigest()
    assert receipt["sovereign_verification_artifacts"]["lean4_sha256"] == expected_lean_sha
