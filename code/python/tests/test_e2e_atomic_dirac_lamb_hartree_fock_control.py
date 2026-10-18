"""E2E tests for QM-224 (Hydrogen Dirac-Coulomb fine structure & 1-loop QED Lamb shift)
and QM-225 (Helium variational / Hylleraas ground state, 1s2s ortho/para exchange
splitting, and closed-shell Roothaan-Hartree-Fock contraction for Z=2..10 over Q).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from finite_qm.use_cases.atomic_dirac_lamb_hartree_fock_control import (
    RationalIntervalQ,
    build_qm224_dirac_lamb_certificate,
    build_qm225_helium_rhf_certificate,
    dirac_coulomb_alpha4_coeff,
    evaluate_helium_1s2s_ortho_para_splitting,
    evaluate_helium_hylleraas_secular_over_q,
    evaluate_helium_variational_polynomial,
    run_closed_shell_rhf_scf,
)


def test_qm224_dirac_coulomb_fine_structure_and_j_half_degeneracy() -> None:
    cert = build_qm224_dirac_lamb_certificate()
    assert cert.passed is True
    assert cert.control_id == "QM-224"

    assert cert.c4_1s_half == Fraction(1, 8)
    assert cert.c4_2s_half == Fraction(5, 128)
    assert cert.c4_2p_half == Fraction(5, 128)
    assert cert.c4_2p_three_half == Fraction(1, 128)

    # Operator-by-operator decomposition: Darwin on 2S_{1/2} matches spin-orbit on 2P_{1/2}
    assert cert.c4_2s_rel_kinetic + cert.c4_2s_darwin == Fraction(5, 128)
    assert cert.c4_2p_rel_kinetic + cert.c4_2p_half_spin_orbit == Fraction(5, 128)
    assert cert.c4_2p_rel_kinetic + cert.c4_2p_three_half_spin_orbit == Fraction(1, 128)
    assert cert.dirac_j_half_degeneracy_exact is True

    # 2P_{3/2} - 2P_{1/2} splitting coefficients and MHz interval enclosures
    assert cert.fine_structure_2p_coeff_mc2 == Fraction(1, 32)
    assert cert.fine_structure_2p_coeff_rydberg == Fraction(1, 16)
    assert RationalIntervalQ(Fraction(1_094_928, 100), Fraction(1_094_929, 100)).contains(
        cert.fine_structure_2p_leading_mhz_interval
    )
    assert cert.fine_structure_2p_qed_mhz_interval.contains(Fraction(1_096_905, 100))


def test_qm224_one_loop_qed_lamb_shift_lifts_degeneracy_and_encloses_lundeen_pipkin() -> None:
    cert = build_qm224_dirac_lamb_certificate()
    assert cert.lamb_uehling_vp_coeff_4pi == Fraction(-4, 15)
    assert cert.lamb_uehling_vp_coeff_6pi == Fraction(-1, 5)
    assert cert.lamb_self_energy_plus_vp_coeff == Fraction(19, 30)
    assert cert.lamb_magnetic_moment_2s_minus_2p_coeff == Fraction(1, 8)
    assert cert.lamb_total_contact_coeff == Fraction(91, 120)

    assert cert.bethe_log_diff_interval == RationalIntervalQ(
        Fraction(2_841_786, 1_000_000), Fraction(2_841_787, 1_000_000)
    )
    assert RationalIntervalQ(Fraction(105_219, 100), Fraction(105_220, 100)).contains(
        cert.lamb_1loop_mhz_interval
    )
    assert RationalIntervalQ(Fraction(105_770, 100), Fraction(105_795, 100)).contains(
        cert.lamb_full_mhz_interval
    )
    assert cert.lundeen_pipkin_benchmark_mhz == Fraction(211_569, 200)
    assert cert.lundeen_pipkin_enclosed is True

    # Check n=3 Dirac-Coulomb coefficients as well
    assert dirac_coulomb_alpha4_coeff(3, 1) == Fraction(1, 72)
    assert dirac_coulomb_alpha4_coeff(3, 3) == Fraction(1, 216)
    assert dirac_coulomb_alpha4_coeff(3, 5) == Fraction(1, 648)


def test_qm225_helium_variational_kellner_minimum_and_hylleraas_secular_bounds() -> None:
    cert = build_qm225_helium_rhf_certificate()
    assert cert.passed is True
    assert cert.control_id == "QM-225"

    # Unscreened bare Z=2 first-order perturbation: -4 + 5/4 = -11/4 = -2.75 E_h
    assert cert.helium_bare_z2.z_eff == Fraction(2, 1)
    assert cert.helium_bare_z2.kinetic_eh == Fraction(4, 1)
    assert cert.helium_bare_z2.nuclear_attraction_eh == Fraction(-8, 1)
    assert cert.helium_bare_z2.electron_repulsion_eh == Fraction(5, 4)
    assert cert.helium_bare_z2.total_energy_eh == Fraction(-11, 4)

    # Stationary Kellner-Hartree minimum at Z_eff* = 2 - 5/16 = 27/16 = 1.6875
    assert cert.helium_kellner_opt.z_eff == Fraction(27, 16)
    assert cert.helium_kellner_opt.total_energy_eh == Fraction(-729, 256)
    assert cert.helium_kellner_opt.virial_residual_2t_plus_v == Fraction(0)
    assert cert.helium_kellner_opt.square_completion_excess_eh == Fraction(0)

    # Square completion holds at arbitrary rational Z_eff
    for z_test in (Fraction(1, 1), Fraction(3, 2), Fraction(7, 4), Fraction(2, 1)):
        ev = evaluate_helium_variational_polynomial(z_test)
        assert ev.total_energy_eh - Fraction(-729, 256) == (z_test - Fraction(27, 16)) ** 2

    # Correlated Hylleraas (1, s, u, t^2) secular matrix over Q
    hyll = evaluate_helium_hylleraas_secular_over_q()
    assert hyll.scale_zeta == Fraction(29, 16)
    assert hyll.overlap_s_4x4[0][0] == Fraction(1, 1)
    assert hyll.kinetic_m_4x4[0][0] == Fraction(1, 1)
    assert hyll.potential_l_4x4[0][0] == Fraction(27, 8)
    assert hyll.target_enclosure_eh.contains(hyll.rayleigh_energy_3term_eh)
    assert hyll.target_enclosure_eh.contains(hyll.rayleigh_energy_4term_eh)
    assert hyll.rayleigh_energy_4term_eh < hyll.rayleigh_energy_3term_eh < Fraction(-729, 256)
    rel_err_4term = abs(
        (hyll.rayleigh_energy_4term_eh - hyll.pekeris_benchmark_eh) / hyll.pekeris_benchmark_eh
    )
    assert rel_err_4term < Fraction(5, 10_000)  # within 0.05%


def test_qm225_helium_1s2s_ortho_para_exchange_and_closed_shell_rhf_contraction() -> None:
    ortho_para = evaluate_helium_1s2s_ortho_para_splitting(2)
    assert ortho_para.unperturbed_1s2s_eh == Fraction(-5, 2)
    assert ortho_para.direct_coulomb_j1s2s_eh == Fraction(34, 81)
    assert ortho_para.exchange_integral_k1s2s_eh == Fraction(32, 729)
    assert ortho_para.triplet_ortho_3s1_eh == Fraction(-3097, 1458)
    assert ortho_para.singlet_para_1s0_eh == Fraction(-2969, 1458)
    assert ortho_para.para_minus_ortho_splitting_eh == Fraction(64, 729)
    assert ortho_para.triplet_strictly_below_singlet is True

    cert = build_qm225_helium_rhf_certificate()
    for atom in (cert.rhf_he_z2, cert.rhf_be_z4, cert.rhf_ne_z10):
        assert atom.strictly_contractive_all_steps is True
        for k in range(1, len(atom.step_l1_distances)):
            assert (
                atom.step_l1_distances[k]
                == atom.contraction_lambda * atom.step_l1_distances[k - 1]
            )

    assert cert.rhf_be_z4.first_ionization_potential_eh == Fraction(169, 500)
    assert cert.rhf_he_z2.first_ionization_potential_eh == Fraction(217, 256)
    assert cert.rhf_ne_z10.first_ionization_potential_eh == Fraction(13_689, 16_000)
    assert cert.noble_gas_ionization_increases_he_to_ne is True
    assert cert.noble_gas_peaks_above_open_shell_be is True

    # Test custom contraction factor on He using screening_sigma = (5/16,)
    he_custom = run_closed_shell_rhf_scf(
        "He", 2, (Fraction(2),), (Fraction(5, 16),), Fraction(1, 3), 5
    )
    assert he_custom.fixed_point_z_eff == (Fraction(27, 16),)
    assert he_custom.strictly_contractive_all_steps is True


def test_qm224_qm225_lean_and_manuscript_cross_layer_constant_parity() -> None:
    paper_root = Path(__file__).resolve().parents[3]
    lean_file = paper_root / "lean4" / "FiniteQM.lean"
    if not lean_file.exists():
        lean_file = paper_root / "lean" / "FiniteQM.lean"
    if not lean_file.exists():
        lean_file = paper_root / "research" / "lean4" / "FiniteQM.lean"
    lean_text = lean_file.read_text(encoding="utf-8")

    ms_file = paper_root / "finite_quantum_mechanics.md"
    if not ms_file.exists():
        ms_file = paper_root / "research" / "finite_quantum_mechanics.md"
    manuscript_text = ms_file.read_text(encoding="utf-8")

    # Verify Lean 4 and manuscript share identical scale zeta=29/16 and RHF ionization fractions
    assert "let zeta : Rat := 29 / 16" in lean_text
    assert "e_hylleraas_4term = -119193915 / 41066752" in lean_text
    assert "let i1_be_2s : Rat := 169 / 500" in lean_text
    assert "let i1_he_1s : Rat := 217 / 256" in lean_text
    assert "let i1_ne_2p : Rat := 13689 / 16000" in lean_text
    assert r"\zeta = 29/16" in manuscript_text
    assert r"\ln k_0(2S) - \ln k_0(2P) \in [2.841786, 2.841787]" in manuscript_text
    assert r"I_1(\mathrm{Be}) = 169/500\,E_h < I_1(\mathrm{He}) = 217/256\,E_h < I_1(\mathrm{Ne}) = 13689/16000\,E_h" in manuscript_text
