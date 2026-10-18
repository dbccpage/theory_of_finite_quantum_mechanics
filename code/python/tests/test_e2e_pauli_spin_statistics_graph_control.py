"""E2E tests for QM-223 Pauli exclusion and topological spin-statistics on finite graphs.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction

from finite_qm.use_cases.pauli_spin_statistics_graph_control import (
    analyze_conf2_graph,
    build_pauli_spin_statistics_certificate,
    orbital_slater_or_permanent,
    verify_two_mode_jordan_wigner_car,
)


def test_qm223_certificate_passes_all_finite_spin_statistics_checks() -> None:
    cert = build_pauli_spin_statistics_certificate()
    assert cert.passed is True
    assert cert.control_id == "QM-223"
    assert cert.conf2_p3.conf2_betti_1 == 0
    assert cert.conf2_p3.conf2_z2_torsion_rank == 0
    assert cert.conf2_y_star is not None
    assert cert.conf2_y_star.conf2_betti_1 == 1
    assert cert.conf2_y_star.conf2_squares == 0
    assert cert.conf2_y_star.conf2_z2_torsion_rank == 0
    assert cert.conf2_y_star.has_y_junction_exchange_cycle is False
    assert cert.conf2_c4.conf2_betti_1 == 3
    assert cert.conf2_c4.conf2_squares == 2
    assert cert.conf2_c4.conf2_2complex_betti_1_q == 1
    assert cert.conf2_c4.has_y_junction_exchange_cycle is False
    assert cert.conf2_k4 is not None
    assert cert.conf2_k4.conf2_betti_1 == 7
    assert cert.conf2_k4.conf2_squares == 3
    assert cert.conf2_k4.conf2_2complex_betti_1_q == 4
    assert cert.conf2_k4.conf2_z2_torsion_rank == 0
    assert cert.conf2_k4.has_y_junction_exchange_cycle is False
    assert cert.conf2_k5.conf2_betti_1 == 21
    assert cert.conf2_k5.conf2_squares == 15
    assert cert.conf2_k5.conf2_2complex_betti_1_q == 6
    assert cert.conf2_k5.conf2_2complex_betti_1_f2 == 7
    assert cert.conf2_k5.conf2_z2_torsion_rank == 1
    assert cert.conf2_k5.has_y_junction_exchange_cycle is True
    assert cert.pauli_same_orbital_slater == Fraction(0)
    assert cert.swap_ratio_fermion == Fraction(-1)
    assert cert.swap_ratio_boson == Fraction(1)
    assert cert.fermi_hole_coincidence_probability == Fraction(0)
    assert cert.hbt_boson_bunching_ratio == Fraction(2)
    assert cert.shell_orbital_degeneracies_1_to_4 == (1, 4, 9, 16)
    assert cert.shell_capacities_1_to_4 == (2, 8, 18, 32)
    assert cert.noble_gas_atomic_numbers == (2, 10, 18, 36, 54, 86, 118)


def test_qm223_three_particle_slater_antisymmetry_and_duplicate_orbital_exclusion() -> None:
    r1 = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)]
    r2 = [Fraction(2, 5), Fraction(3, 5), Fraction(1, 5)]
    r3 = [Fraction(3, 7), Fraction(2, 7), Fraction(4, 7)]

    assert orbital_slater_or_permanent([r1, r1, r2], alternating=True) == Fraction(0)

    det_123 = orbital_slater_or_permanent([r1, r2, r3], alternating=True)
    det_213 = orbital_slater_or_permanent([r2, r1, r3], alternating=True)
    assert det_213 == -det_123
    assert det_123 != Fraction(0)

    perm_123 = orbital_slater_or_permanent([r1, r2, r3], alternating=False)
    perm_213 = orbital_slater_or_permanent([r2, r1, r3], alternating=False)
    assert perm_213 == perm_123


def test_qm223_jordan_wigner_car_nilpotency_and_fock_trace() -> None:
    nilpotent, car_exact, tr_sum = verify_two_mode_jordan_wigner_car()
    assert nilpotent is True
    assert car_exact is True
    assert tr_sum == Fraction(4)


def test_qm223_planar_theta_vs_nonplanar_k33_2complex_torsion() -> None:
    # Planar Theta_4 has degree >= 3 at 0 and 2, but H_1(Conf_2^(2)(Theta_4); Z) is torsion-free!
    theta4 = analyze_conf2_graph("Theta_4", 4, [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])
    assert theta4.conf2_vertices == 6
    assert theta4.conf2_edges == 10
    assert theta4.conf2_betti_1 == 5
    assert theta4.conf2_squares == 2
    assert theta4.conf2_2complex_betti_1_q == 3
    assert theta4.conf2_z2_torsion_rank == 0
    assert theta4.has_y_junction_exchange_cycle is False
    assert theta4.admissible_1d_exchange_characters == ("BRAID_U1_CYCLOTOMIC_PHASE",)

    # Nonplanar 3-connected K_{3,3} has Z_2 torsion in H_1(Conf_2^(2)(K_{3,3}); Z), restricting characters to {+1, -1}
    k33_edges = [(u, v) for u in range(3) for v in range(3, 6)]
    k33 = analyze_conf2_graph("K_3_3", 6, k33_edges)
    assert k33.conf2_z2_torsion_rank == 1
    assert k33.has_y_junction_exchange_cycle is True
    assert k33.admissible_1d_exchange_characters == ("+1_BOSON", "-1_FERMION")
