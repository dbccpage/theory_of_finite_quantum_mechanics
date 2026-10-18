"""E2E verification suite for Finite QM Expressibility Classification, Strict Finite No-Go
Theorems, Kraus Measurement Decoherence, Multi-Observer Wigner's-Friend Obstruction,
and Qutrit Stabilizer-vs-Magic Discrete Wigner Simulation Boundary.

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/expressibility.py
Claim: evaluate_finite_qm_expressibility_and_measurement_control certificate locked by exact checks in this file
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from finite_qm.use_cases.finite_qm_expressibility_and_measurement_control import (
    evaluate_finite_qm_expressibility_and_measurement_control,
    summarize_finite_qm_expressibility_and_measurement_control,
)


def test_unit_part_1_three_way_expressibility_and_strict_finite_nogo_theorems() -> None:
    r = evaluate_finite_qm_expressibility_and_measurement_control()
    assert r.class_i_exact_finite_identity_count == 11
    assert r.class_ii_rational_interval_enclosure_count == 4
    assert r.class_iii_strict_finite_nogo_count == 3
    assert r.weyl_heisenberg_commutator_trace_zero_all_dims is True
    assert r.identity_trace_nonzero_all_dims is True
    assert r.kravchuk_interior_commutator_is_one_all_dims is True
    assert r.kravchuk_top_boundary_defect_d3 == Fraction(-2, 1)
    assert r.kravchuk_top_boundary_defect_d4 == Fraction(-3, 1)
    assert r.kravchuk_commutator_trace_zero_all_dims is True
    assert r.lorentz_boost_is_minkowski_isometry_all_betas is True
    assert r.lorentz_boost_euclidean_gram_not_identity_all_betas is True
    assert r.lorentz_boost_gram_trace_excess_matches_formula is True
    assert r.lorentz_boost_2x2_gram_trace_at_half == Fraction(82, 9)
    assert r.lorentz_boost_4x4_gram_trace_at_half == Fraction(100, 9)
    assert r.lorentz_boost_generator_killing_trace_positive is True
    assert r.closed_clock_survival_probabilities == (
        Fraction(1, 1),
        Fraction(0, 1),
        Fraction(0, 1),
        Fraction(0, 1),
        Fraction(1, 1),
    )
    assert r.closed_clock_unitary_power_n_is_identity is True
    assert r.closed_clock_exact_poincare_recurrence_at_n is True


def test_part_2_kraus_decoherence_and_wigners_friend_multi_observer_obstruction() -> None:
    r = evaluate_finite_qm_expressibility_and_measurement_control()
    assert r.premeasurement_cnot_is_unitary is True
    assert r.joint_post_measurement_state_is_pure is True
    assert r.joint_unitary_reversal_restores_initial_state is True
    assert r.partial_trace_equals_kraus_channel is True
    assert r.kraus_completeness_holds is True
    assert r.reduced_state_off_diagonal_zero is True
    assert r.initial_system_purity == Fraction(1, 1)
    assert r.reduced_system_purity == Fraction(337, 625)
    assert r.subsystem_purity_loss == Fraction(288, 625)

    assert r.friends_internal_records_perfectly_correlated is True
    assert r.wigners_friend_observables_involutory_and_commuting is True
    assert r.wigners_friend_local_settings_anticommute is True
    assert r.wf_correlators == (
        Fraction(3, 5),
        Fraction(4, 5),
        Fraction(4, 5),
        Fraction(-3, 5),
    )
    assert r.wf_chsh_value == Fraction(14, 5)
    assert r.wf_chsh_squared == Fraction(196, 25)
    assert r.wf_violates_classical_joint_table_bound is True
    assert r.wf_respects_tsirelson_quantum_bound is True
    assert r.wf_no_observer_independent_joint_distribution is True


def test_part_3_qutrit_stabilizer_magic_wigner_dichotomy() -> None:
    r = evaluate_finite_qm_expressibility_and_measurement_control()
    assert r.qutrit_stabilizer_state_count == 12
    assert r.qutrit_four_mubs_intrabasis_orthogonal is True
    assert r.qutrit_four_mubs_interbasis_overlap_exact_one_third is True
    assert r.all_12_stabilizers_wigner_nonnegative_and_normalized is True
    assert r.all_12_stabilizers_supported_on_affine_lines is True
    assert r.all_12_stabilizers_zero_negativity is True
    assert r.wigner_inner_product_matches_born_rule_all_pairs is True
    assert r.clifford_fourier_symplectic_covariance_exact is True
    assert r.magic_state_wigner_normalized_and_pure is True
    assert r.magic_state_wigner_00 == Fraction(-1, 9)
    assert r.magic_state_min_wigner_entry == Fraction(-1, 9)
    assert r.magic_state_wigner_negativity == Fraction(4, 9)
    assert r.magic_state_born_overlaps_match_wigner_pairing is True

    summary = summarize_finite_qm_expressibility_and_measurement_control()
    assert summary["wf_chsh_value"] == "14/5"
    assert summary["magic_state_wigner_negativity"] == "4/9"


def test_part_4_lean4_part8_parity() -> None:
    paper_root = Path(__file__).resolve().parents[3]
    repo_root = Path(r"c:/Users/a343o/source/repos/the_symbol_game")
    canonical_lean = repo_root / "lean4/quantum_mechanics/FiniteQM.lean"
    paper_lean = paper_root / "lean4/FiniteQM.lean" if (paper_root / "lean4/FiniteQM.lean").is_file() else paper_root / "lean/FiniteQM.lean"
    if not canonical_lean.is_file():
        canonical_lean = paper_root / "lean4" / "FiniteQM.lean" if (paper_root / "lean4" / "FiniteQM.lean").is_file() else paper_root / "lean" / "FiniteQM.lean"
    assert canonical_lean.is_file()
    assert paper_lean.is_file()
    text = canonical_lean.read_text(encoding="utf-8")
    assert text == paper_lean.read_text(encoding="utf-8")
    assert "sorry" not in text
    for thm_name in (
        "theorem weyl_heisenberg_finite_trace_obstruction",
        "theorem lorentz_boost_non_unitary_in_finite_dim",
        "theorem finite_clock_poincare_recurrence_vs_kraus_decoherence",
        "theorem wigners_friend_rational_chsh_multi_observer_obstruction",
        "theorem qutrit_stabilizer_wigner_nonnegative_vs_magic_negative",
    ):
        assert thm_name in text, f"Missing Lean 4 theorem {thm_name}"


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'expressibility.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'evaluate_finite_qm_expressibility_and_measurement_control' in source
    assert _MODULE_PATH.is_file()
