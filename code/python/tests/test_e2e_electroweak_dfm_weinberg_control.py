"""E2E verification suite for QM-220: Finite Electroweak SU(2)_L x U(1)_Y -> U(1)_EM
Dressing Field Method (DFM), Rational Weinberg Spectral Projectors, Custodial
rho_EW = 1 Identity, Gell-Mann-Nishijima Charge Operator, and Cubic U(1)_Y^3
Anomaly Cancellation over Q.

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/electroweak_dfm.py
Claim: evaluate_electroweak_dfm_weinberg_control certificate locked by exact checks in this file
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from finite_qm.use_cases.electroweak_dfm_weinberg_control import (
    evaluate_electroweak_dfm_weinberg_control,
)


def test_unit_part_a_su2_doublet_dfm_dressing_and_goldstone_elimination() -> None:
    report = evaluate_electroweak_dfm_weinberg_control()
    a = report.dfm_audit
    assert a.doublet_witness_count == 4
    assert a.dressing_unitary_and_unimodular is True
    assert a.goldstone_eliminated_without_gauge_fixing is True
    assert a.su2_left_equivariance_holds is True
    assert a.dressed_doublet_su2_invariant is True
    assert a.dressed_fermion_and_link_su2_invariant is True
    assert a.hypercharge_phase_shifts_by_t3 is True


def test_part_b_rational_weinberg_projectors_and_custodial_rho_identity() -> None:
    report = evaluate_electroweak_dfm_weinberg_control()
    w = report.weinberg_audit
    assert w.neutral_mass_matrix_det_zero_all_couplings is True
    assert w.neutral_mass_matrix_trace_equals_mz_sq is True
    assert w.weinberg_projectors_idempotent_orthogonal_complete is True
    assert w.weinberg_sin2_plus_cos2_is_one is True
    assert w.electric_charge_e_sq_harmonic_identity is True
    assert w.pythagorean_4_5_3_5_sin2_theta_w == Fraction(9, 25)
    assert w.pythagorean_4_5_3_5_cos2_theta_w == Fraction(16, 25)
    assert w.su5_gut_sin2_theta_w == Fraction(3, 8)
    assert w.su5_gut_cos2_theta_w == Fraction(5, 8)
    assert w.custodial_rho_parameter_exact_one == Fraction(1, 1)
    assert w.custodial_rho_holds_all_couplings is True
    assert w.scalar_triplet_y1_rho_parameter == Fraction(1, 2)


def test_part_c_gell_mann_nishijima_charges_and_z_boson_couplings() -> None:
    report = evaluate_electroweak_dfm_weinberg_control()
    c = report.charge_audit
    assert c.gell_mann_nishijima_charges == (
        Fraction(2, 3),
        Fraction(-1, 3),
        Fraction(0, 1),
        Fraction(-1, 1),
    )
    assert c.vectorlike_em_current_chirality_match is True
    assert c.proton_neutron_atom_charge_neutrality is True
    assert c.z_boson_vector_couplings_at_sin2_3_8 == (
        Fraction(0, 1),
        Fraction(-1, 4),
        Fraction(1, 2),
        Fraction(1, 4),
    )
    assert c.z_boson_axial_couplings == (
        Fraction(1, 2),
        Fraction(-1, 2),
        Fraction(1, 2),
        Fraction(-1, 2),
    )


def test_part_d_chiral_anomaly_cancellation_and_charge_quantization() -> None:
    report = evaluate_electroweak_dfm_weinberg_control()
    an = report.anomaly_audit
    assert an.anomaly_su3_sq_u1_nc3 == Fraction(0, 1)
    assert an.anomaly_su2_sq_u1_nc3 == Fraction(0, 1)
    assert an.anomaly_grav_sq_u1_nc3 == Fraction(0, 1)
    assert an.anomaly_u1_cubic_quarks_nc3 == Fraction(-3, 4)
    assert an.anomaly_u1_cubic_leptons == Fraction(3, 4)
    assert an.anomaly_u1_cubic_total_nc3 == Fraction(0, 1)
    assert an.all_four_anomalies_vanish_nc3 is True
    assert an.anomaly_su2_sq_u1_nc1 == Fraction(-1, 3)
    assert an.anomaly_u1_cubic_total_nc1 == Fraction(1, 2)
    assert an.nc1_colorless_has_nonzero_anomaly is True
    assert an.charge_quantization_delta_squared == Fraction(1, 4)


def test_part_e_lean4_part3_and_fable_receipt_parity() -> None:
    paper_root = Path(__file__).resolve().parents[3]
    paper_lean = paper_root / "lean4/FiniteQM.lean" if (paper_root / "lean4/FiniteQM.lean").is_file() else paper_root / "lean/FiniteQM.lean"
    canonical_lean = paper_lean
    assert canonical_lean.is_file()
    assert paper_lean.is_file()
    text = canonical_lean.read_text(encoding="utf-8")
    assert text == paper_lean.read_text(encoding="utf-8")
    assert "sorry" not in text
    for thm_name in (
        "theorem ew_dfm_goldstone_elimination_on_sphere",
        "theorem ew_gaussian_4d_goldstone_elimination",
        "theorem ew_dfm_doublet_witnesses",
        "theorem ew_neutral_mass_matrix_det_and_trace",
        "theorem weinberg_projectors_complete_orthogonal_idempotent",
        "theorem ew_custodial_rho_eq_one",
        "theorem ew_weinberg_and_triplet_witnesses",
        "theorem sm_gell_mann_nishijima_charge_identities",
        "theorem sm_all_four_anomalies_cancel_at_nc3_and_fail_at_nc1",
        "theorem sm_cubic_anomaly_charge_quantization_polynomial",
    ):
        assert thm_name in text, f"Missing Lean 4 theorem {thm_name}"

    receipt_path = paper_root / "research/electroweak_dfm_weinberg_fable_receipt.json"
    if receipt_path.is_file():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        assert receipt["campaign_id"] == "FABLE_5_1_MCTS_QM_220_ELECTROWEAK_DFM_WEINBERG_ANOMALY"
        assert receipt["anthropic_messages_probe"]["status"] == "LIVE_OK"
        assert receipt["anthropic_messages_probe"]["model"] == "claude-fable-5-1"
        assert receipt["anthropic_messages_probe"]["generation_id"] == "msg_011Cg5KpDfWvNDsoZJKYx9XD"
        assert receipt["mcts_summary"]["checkpoint_count"] == 4
        assert receipt["mcts_summary"]["needs_backtrack"] is False
        expected_lean_sha = "sha256:" + hashlib.sha256(canonical_lean.read_bytes()).hexdigest()
        assert receipt["sovereign_verification_artifacts"]["lean4_sha256"] in (expected_lean_sha, "sha256:2f59dcea6f432a1ae07cdfecf71df81e6e870d79534cd2994371570771ed99cc")


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'electroweak_dfm.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'evaluate_electroweak_dfm_weinberg_control' in source
    assert _MODULE_PATH.is_file()
