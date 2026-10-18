"""End-to-end verification tests for the Four-Wall Finite Reconstruction & Positivity
Boundary Theorem and the 5-Stage Operadic Ecology (pilot_051..055) of Finite QM.
"""

from __future__ import annotations

from fractions import Fraction

from finite_qm.use_cases.four_wall_reconstruction_and_operad_control import (
    evaluate_four_wall_reconstruction_and_operad_control,
    evaluate_wall1_busch_ic_povm_vs_polyhedral_cone,
    evaluate_wall2_galois_sos_total_positivity,
    evaluate_wall3_cocycle_and_choi_separation,
    evaluate_wall4_cayley_and_entropy_enclosure,
)


def test_wall1_busch_ic_povm_and_polyhedral_cone_separation() -> None:
    audit = evaluate_wall1_busch_ic_povm_vs_polyhedral_cone()
    assert audit.trace_sum_equals_two
    assert audit.bloch_sum_vanishes
    assert audit.all_effects_psd
    assert audit.reconstruction_determinant == Fraction(9, 1000)
    assert audit.reconstruction_invertible
    assert audit.polyhedral_cabello_peres_minor == Fraction(-1, 16)
    assert audit.polyhedral_cone_strictly_larger_than_psd
    assert audit.reconstructed_pythagorean_state_trace == Fraction(1, 1)
    assert audit.reconstructed_pythagorean_state_det == Fraction(108, 625)
    assert audit.cholesky_sos_verified


def test_wall2_galois_conjugate_negativity_vs_sos_total_positivity() -> None:
    audit = evaluate_wall2_galois_sos_total_positivity()
    assert audit.twist_trace_rational == Fraction(1, 1)
    assert audit.twist_trace_sqrt5 == Fraction(0, 1)
    assert audit.twist_det_rational == Fraction(-1, 8)
    assert audit.twist_det_sqrt5 == Fraction(1, 8)
    assert audit.twist_det_field_norm == Fraction(-1, 16)
    assert audit.twist_fails_conjugate_embedding
    assert audit.sos_trace_rational == Fraction(1, 1)
    assert audit.sos_trace_sqrt5 == Fraction(0, 1)
    assert audit.sos_det_rational == Fraction(1, 9)
    assert audit.sos_det_sqrt5 == Fraction(0, 1)
    assert audit.sos_det_field_norm == Fraction(1, 81)
    assert audit.sos_factor_identity_holds
    assert audit.sos_psd_in_all_galois_embeddings


def test_wall3_char2_cocycle_and_choi_transpose_separation() -> None:
    audit = evaluate_wall3_cocycle_and_choi_separation()
    assert audit.inv2_mod3 == 1
    assert audit.two_mod2 == 0
    assert audit.odd_prime_half_invertible
    assert audit.char2_half_obstructed
    assert audit.mermin_peres_cocycle_ratio == -1
    assert audit.choi_transpose_singlet_expectation == Fraction(-1, 2)
    assert audit.choi_identity_singlet_expectation == Fraction(0, 1)
    assert audit.choi_identity_bell_expectation == Fraction(1, 1)
    assert audit.choi_separates_positive_witness_from_cptp


def test_wall4_cayley_unitarity_and_entropy_interval_enclosure() -> None:
    audit = evaluate_wall4_cayley_and_entropy_enclosure()
    assert audit.cayley_single_unitarity_defect == Fraction(0, 1)
    assert audit.strang_cayley_split_unitarity_defect == Fraction(0, 1)
    assert audit.taylor_first_order_norm_sq == Fraction(5, 4)
    assert audit.taylor_violates_unitarity
    assert audit.renyi_p2 == Fraction(337, 625)
    assert audit.renyi_p3 == Fraction(193, 625)
    assert audit.renyi_p4 == Fraction(72097, 390625)
    assert audit.interval_width_below_1e_12


def test_five_stage_operad_ecology_complete() -> None:
    report = evaluate_four_wall_reconstruction_and_operad_control()
    assert report.all_four_walls_and_five_stages_verified
    assert len(report.operad_stages) == 5
    pilot_ids = [s.pilot_id for s in report.operad_stages]
    assert pilot_ids == ["pilot_051", "pilot_052", "pilot_053", "pilot_054", "pilot_055"]
    operad_symbols = [s.operad_symbol for s in report.operad_stages]
    assert operad_symbols == ["B_Polar", "O_Gal", "O_{H^2}", "O_Strat", "Op_FQM"]
    for stage in report.operad_stages:
        assert stage.verified
        assert stage.antibody_id.startswith("AB_FQM_05")
        assert stage.rule_id.startswith("RULE_FQM_05")
        assert stage.anti_rule_id.startswith("ANTIRULE_FQM_05")
        assert stage.anti_pattern_id.startswith("AP_MATH_02")
        assert stage.helpful_pattern_id.startswith("HP_MATH_02")
        assert stage.agent_id.startswith("AGENT_FQM_05")
        assert stage.anti_agent_id.startswith("ANTIAGENT_FQM_05")
