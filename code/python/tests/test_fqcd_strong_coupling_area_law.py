"""Unit and property tests for FQCD Strong-Coupling Area Law (Record TFQ-1052).

Governing DAG target node: FQCD-STRONG-COUPLING-AREA-LAW
AuthorityEffect: None
"""

from __future__ import annotations

from fractions import Fraction
import math
import pytest

try:
    from fqcd.strong_coupling_area_law import (
        CONST_K,
        CONST_SIGMA_0,
        a5_cubic_character_invariants_rational,
        area_law_decay_bound,
        area_law_decay_bound_rational,
        baryon_vs_gluon_screening_casimir_and_mednykh_2d_towers_rational,
        binary_icosahedral_2i_invariants_rational,
        cluster_series_geometric_sum,
        cluster_series_geometric_sum_rational,
        collar_tube_contraction,
        collar_tube_contraction_rational,
        complete_blichfeldt_ffk_su3_crystal_hierarchy_rational,
        coordination_number_delta,
        d4_multi_plaquette_collar_bound_rational,
        finite_coupling_galois_conjugate_suppression_rational,
        freezing_plaquette_defect_rational_bounds,
        general_collar_tube_contraction_rational,
        geometric_cluster_series_bound_satisfied,
        hessian_subgroups_and_quartic_adjoint_casimir_obstruction_rational,
        higher_genus_mednykh_abelianization_and_genus3_bounds_rational,
        klein_sigma168_invariants_and_su3_chain_rational,
        loop_perimeter,
        minimal_spanning_area,
        normal_directions_count,
        q8_center_parity_protection,
        q8_cubic_character_invariant,
        q8_cubic_character_invariant_rational,
        quartic_character_invariants_and_continuum_matching_rational,
        s3_cubic_character_invariant,
        s3_cubic_character_invariant_rational,
        s4_cubic_character_invariants_rational,
        single_plaquette_character_activity_zn,
        strong_coupling_threshold_beta0,
        strong_coupling_threshold_beta0_rational,
        strong_coupling_threshold_beta0_rational_bounds,
        strong_to_freezing_coupling_gap_rational,
        su2_ade_binary_polyhedral_tower_rational,
        su2_higher_spin_casimir_and_hessian_defect_bounds_rational,
        su3_subgroup_tower_and_freezing_scales_rational,
        temporal_gauge_perron_frobenius_and_2d_mednykh_pachner_rational,
        twod_character_decimation_area_law,
        twod_character_decimation_area_law_rational,
        valentiner_sigma1080_invariants_rational,
        verify_fqcd_strong_coupling_area_law_witness,
    )
except ImportError:
    from src.fqcd.strong_coupling_area_law import (
        CONST_K,
        CONST_SIGMA_0,
        a5_cubic_character_invariants_rational,
        area_law_decay_bound,
        area_law_decay_bound_rational,
        baryon_vs_gluon_screening_casimir_and_mednykh_2d_towers_rational,
        binary_icosahedral_2i_invariants_rational,
        cluster_series_geometric_sum,
        cluster_series_geometric_sum_rational,
        collar_tube_contraction,
        collar_tube_contraction_rational,
        complete_blichfeldt_ffk_su3_crystal_hierarchy_rational,
        coordination_number_delta,
        d4_multi_plaquette_collar_bound_rational,
        finite_coupling_galois_conjugate_suppression_rational,
        freezing_plaquette_defect_rational_bounds,
        general_collar_tube_contraction_rational,
        geometric_cluster_series_bound_satisfied,
        hessian_subgroups_and_quartic_adjoint_casimir_obstruction_rational,
        higher_genus_mednykh_abelianization_and_genus3_bounds_rational,
        klein_sigma168_invariants_and_su3_chain_rational,
        loop_perimeter,
        minimal_spanning_area,
        normal_directions_count,
        q8_center_parity_protection,
        q8_cubic_character_invariant,
        q8_cubic_character_invariant_rational,
        quartic_character_invariants_and_continuum_matching_rational,
        s3_cubic_character_invariant,
        s3_cubic_character_invariant_rational,
        s4_cubic_character_invariants_rational,
        single_plaquette_character_activity_zn,
        strong_coupling_threshold_beta0,
        strong_coupling_threshold_beta0_rational,
        strong_coupling_threshold_beta0_rational_bounds,
        strong_to_freezing_coupling_gap_rational,
        su2_ade_binary_polyhedral_tower_rational,
        su2_higher_spin_casimir_and_hessian_defect_bounds_rational,
        su3_subgroup_tower_and_freezing_scales_rational,
        temporal_gauge_perron_frobenius_and_2d_mednykh_pachner_rational,
        twod_character_decimation_area_law,
        twod_character_decimation_area_law_rational,
        valentiner_sigma1080_invariants_rational,
        verify_fqcd_strong_coupling_area_law_witness,
    )


def test_coordination_numbers_and_refusals() -> None:
    expected = {
        2: 4,
        3: 12,
        4: 24,
        5: 40,
        6: 60,
    }
    for d, delta in expected.items():
        assert coordination_number_delta(d) == delta
        assert delta == 2 * d * (d - 1)

    with pytest.raises(ValueError):
        coordination_number_delta(1)
    with pytest.raises(ValueError):
        coordination_number_delta(0)
    with pytest.raises(ValueError):
        coordination_number_delta(-2)


def test_strong_coupling_threshold_beta0() -> None:
    for n in [2, 3, 4, 8]:
        for d in [2, 3, 4]:
            beta0 = strong_coupling_threshold_beta0(n, d)
            assert beta0 > 0.0
            # Analytical check against formula
            expected = 1.0 / (8.0 * math.e * (2 * d * (d - 1)) * (n - 1))
            assert abs(beta0 - expected) < 1e-15

    # Monotonicity: strictly decreasing with dimension d
    assert strong_coupling_threshold_beta0(2, 2) > strong_coupling_threshold_beta0(2, 3)
    assert strong_coupling_threshold_beta0(2, 3) > strong_coupling_threshold_beta0(2, 4)

    # Monotonicity: strictly decreasing with group order N
    assert strong_coupling_threshold_beta0(2, 4) > strong_coupling_threshold_beta0(3, 4)
    assert strong_coupling_threshold_beta0(3, 4) > strong_coupling_threshold_beta0(4, 4)

    with pytest.raises(ValueError):
        strong_coupling_threshold_beta0(1, 4)
    with pytest.raises(ValueError):
        strong_coupling_threshold_beta0(2, 1)


def test_strong_coupling_threshold_rational_bounds() -> None:
    for n in [2, 3, 5]:
        for d in [2, 3, 4]:
            lower, upper = strong_coupling_threshold_beta0_rational_bounds(n, d)
            rat_val = strong_coupling_threshold_beta0_rational(n, d)
            flt_val = strong_coupling_threshold_beta0(n, d)

            assert lower > 0
            assert upper > lower
            assert float(lower) <= flt_val <= float(upper)
            assert lower <= rat_val <= upper


def test_minimal_spanning_area_and_perimeter() -> None:
    assert minimal_spanning_area(1, 1) == 1
    assert loop_perimeter(1, 1) == 4

    assert minimal_spanning_area(3, 5) == 15
    assert loop_perimeter(3, 5) == 16

    assert minimal_spanning_area(10, 20) == 200
    assert loop_perimeter(10, 20) == 60

    with pytest.raises(ValueError):
        minimal_spanning_area(0, 5)
    with pytest.raises(ValueError):
        minimal_spanning_area(5, -1)
    with pytest.raises(ValueError):
        loop_perimeter(0, 4)


def test_exact_constants_and_decay_bound() -> None:
    assert CONST_K == 1
    assert abs(math.exp(-CONST_SIGMA_0) - 0.25) < 1e-15
    assert CONST_SIGMA_0 == pytest.approx(math.log(4.0))

    for area in [1, 2, 3, 4, 8]:
        flt_bound = area_law_decay_bound(area)
        rat_bound = area_law_decay_bound_rational(area)
        expected = 0.25 ** area
        assert abs(flt_bound - expected) < 1e-15
        assert rat_bound == Fraction(1, 4 ** area)
        assert abs(float(rat_bound) - flt_bound) < 1e-15


def test_single_plaquette_character_activity_zn() -> None:
    for n in [2, 3, 4, 5, 8]:
        beta0 = strong_coupling_threshold_beta0(n, 4)
        for beta in [0.0, beta0 * 0.1, beta0 * 0.5, beta0 * 0.9]:
            for m in range(1, n):
                a_m, a_0, alpha = single_plaquette_character_activity_zn(n, m, beta)
                assert a_0 > 0.0
                if beta == 0.0:
                    assert abs(a_m) < 1e-15
                    assert abs(alpha) < 1e-15
                else:
                    # Bound: |alpha_m| <= beta < beta_0
                    assert abs(alpha) <= beta + 1e-14
                    assert abs(alpha) < beta0


def test_cluster_series_geometric_sum_and_bound() -> None:
    # Test for mu <= 0.20 (which corresponds to beta <= beta_0 / 5)
    mu_rat = Fraction(1, 5)
    for area in range(1, 10):
        rat_sum = cluster_series_geometric_sum_rational(mu_rat, area)
        rat_decay = area_law_decay_bound_rational(area)
        assert rat_sum <= rat_decay

    for n in [2, 3, 4]:
        for d in [2, 3, 4]:
            beta0 = strong_coupling_threshold_beta0(n, d)
            # For beta <= beta0 / 5
            for beta in [beta0 * 0.01, beta0 * 0.1, beta0 * 0.2]:
                for area in [1, 2, 3, 5, 10]:
                    assert geometric_cluster_series_bound_satisfied(n, d, beta, area)


def test_s3_cubic_character_invariant_and_screening() -> None:
    s3_inv = s3_cubic_character_invariant()
    s3_inv_rat = s3_cubic_character_invariant_rational()
    assert abs(s3_inv - 1.0) < 1e-15
    assert s3_inv_rat == Fraction(1, 1)

    # Collar tube screening tensor contraction
    assert collar_tube_contraction(0) == 1.0
    assert collar_tube_contraction(1) == 0.5
    assert collar_tube_contraction(17) == 2.0 ** (-17)
    assert collar_tube_contraction_rational(17) == Fraction(1, 131072)
    assert collar_tube_contraction_rational(17) > 0

    with pytest.raises(ValueError):
        collar_tube_contraction(-1)


def test_q8_cubic_character_invariant_and_protection() -> None:
    q8_inv = q8_cubic_character_invariant()
    q8_inv_rat = q8_cubic_character_invariant_rational()
    assert abs(q8_inv) < 1e-15
    assert q8_inv_rat == Fraction(0, 1)

    protection = q8_center_parity_protection()
    assert protection["group"] == "Q_8"
    assert protection["cubic_invariant"] == 0.0
    assert protection["screening_protection"] is True
    assert protection["chi_center_defect"] == -2


def test_twod_character_decimation_area_law() -> None:
    # Abelian case (dim R = 1): <W> = (alpha)^Area
    alpha = 0.2
    for area in [1, 2, 3, 5]:
        val = twod_character_decimation_area_law(1, alpha, area)
        val_rat = twod_character_decimation_area_law_rational(1, Fraction(1, 5), area)
        assert abs(val - (alpha ** area)) < 1e-15
        assert val_rat == Fraction(1, 5 ** area)

    # Non-abelian case (dim R = 2): <W> = 2^{1 - Area} * (alpha)^Area
    for area in [1, 2, 3, 4]:
        val = twod_character_decimation_area_law(2, alpha, area)
        val_rat = twod_character_decimation_area_law_rational(2, Fraction(1, 5), area)
        expected = (2.0 ** (1 - area)) * (alpha ** area)
        assert abs(val - expected) < 1e-15
        expected_rat = Fraction(1, 2 ** (area - 1)) * Fraction(1, 5 ** area)
        assert val_rat == expected_rat


def test_s4_and_a5_cubic_invariants_and_d4_collar_bounds() -> None:
    s4_invs = s4_cubic_character_invariants_rational()
    assert s4_invs["3"] == Fraction(1, 1)
    assert s4_invs["3_prime"] == Fraction(1, 1)
    assert s4_invs["2"] == Fraction(1, 1)
    assert s4_invs["sgn"] == Fraction(0, 1)

    a5_invs = a5_cubic_character_invariants_rational()
    assert a5_invs["3_a"] == Fraction(1, 1)
    assert a5_invs["3_b"] == Fraction(1, 1)
    assert a5_invs["4"] == Fraction(1, 1)
    assert a5_invs["5"] == Fraction(2, 1)

    # Higher representation dimension d_R yields stronger per-edge collar contraction
    c_d2 = general_collar_tube_contraction_rational(2, 6)
    c_d3 = general_collar_tube_contraction_rational(3, 6)
    c_d4 = general_collar_tube_contraction_rational(4, 6)
    c_d5 = general_collar_tube_contraction_rational(5, 6)
    assert c_d2 > c_d3 > c_d4 > c_d5 > Fraction(0, 1)

    # d=4 normal directions and multi-plaquette collar contraction bounds
    assert normal_directions_count(3) == 2
    assert normal_directions_count(4) == 4
    with pytest.raises(ValueError):
        normal_directions_count(2)

    beta = Fraction(1, 10)
    b_k1 = d4_multi_plaquette_collar_bound_rational(4, 1, 2, beta)
    b_k2 = d4_multi_plaquette_collar_bound_rational(4, 2, 2, beta)
    b_k1_d3 = d4_multi_plaquette_collar_bound_rational(4, 1, 3, beta)
    assert b_k1 == Fraction(1, 10 ** 12)
    assert Fraction(0, 1) < b_k2 < b_k1
    assert Fraction(0, 1) < b_k1_d3 < b_k1


def test_binary_icosahedral_2i_and_valentiner_sigma1080_and_freezing_defects() -> None:
    invs_2i = binary_icosahedral_2i_invariants_rational()
    assert invs_2i["2_s"] == Fraction(0, 1)
    assert invs_2i["2_s_prime"] == Fraction(0, 1)
    assert invs_2i["4_s"] == Fraction(0, 1)
    assert invs_2i["6_s"] == Fraction(0, 1)
    assert invs_2i["3_a"] == Fraction(1, 1)
    assert invs_2i["3_b"] == Fraction(1, 1)
    assert invs_2i["4_t"] == Fraction(1, 1)
    assert invs_2i["5_t"] == Fraction(2, 1)

    invs_s1080 = valentiner_sigma1080_invariants_rational()
    assert invs_s1080["I11_3a"] == Fraction(1, 1)
    assert invs_s1080["I2_3a"] == Fraction(0, 1)
    assert invs_s1080["I3_3a"] == Fraction(1, 1)
    assert invs_s1080["I3_5a"] == Fraction(1, 1)
    assert invs_s1080["I3_8a"] == Fraction(2, 1)
    assert invs_s1080["I3_10"] == Fraction(2, 1)

    defects = freezing_plaquette_defect_rational_bounds()
    d2i_low, d2i_high = defects["2I_2s"]
    ds1080_low, ds1080_high = defects["Sigma1080_3a"]
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    exact_d2i = 1.0 - phi / 2.0
    exact_ds1080 = 1.0 - phi / 3.0
    assert float(d2i_low) < exact_d2i < float(d2i_high)
    assert float(ds1080_low) < exact_ds1080 < float(ds1080_high)
    assert Fraction(0, 1) < d2i_low < d2i_high < ds1080_low < ds1080_high < Fraction(1, 1)


def test_su2_ade_and_su3_subgroup_towers_and_freezing_scales() -> None:
    su2_tower = su2_ade_binary_polyhedral_tower_rational()
    assert su2_tower["I3_2T_2s"] == Fraction(0, 1)
    assert su2_tower["I3_2T_3t"] == Fraction(2, 1)
    assert su2_tower["I3_2O_2s"] == Fraction(0, 1)
    assert su2_tower["I3_2O_3"] == Fraction(1, 1)
    d2i_low, d2i_high = su2_tower["delta_min_2I_bounds"]
    d2o_low, d2o_high = su2_tower["delta_min_2O_bounds"]
    exact_d2o = 1.0 - math.sqrt(2.0) / 2.0
    assert float(d2o_low) < exact_d2o < float(d2o_high)
    assert Fraction(0, 1) < d2i_low < d2i_high < d2o_low < d2o_high < su2_tower["delta_min_2T"] < su2_tower["delta_min_Q8"]

    su3_tower = su3_subgroup_tower_and_freezing_scales_rational()
    assert su3_tower["I3_Delta27_3"] == Fraction(3, 1)
    assert su3_tower["I3_Delta54_3_1"] == Fraction(1, 1)
    assert su3_tower["I3_Delta54_3_2"] == Fraction(2, 1)
    bf_s1080_low, bf_s1080_high = su3_tower["beta_freeze_proxy_Sigma1080_bounds"]
    assert su3_tower["beta_freeze_proxy_Delta27"] == Fraction(1, 1)
    assert su3_tower["beta_freeze_proxy_Delta54"] == Fraction(6, 5)
    assert su3_tower["beta_freeze_proxy_Delta27"] < su3_tower["beta_freeze_proxy_Delta54"] < bf_s1080_low < bf_s1080_high

    g_q8 = strong_to_freezing_coupling_gap_rational(8, 4, Fraction(1, 1))
    g_2t = strong_to_freezing_coupling_gap_rational(24, 4, Fraction(1, 2))
    g_2o_low = strong_to_freezing_coupling_gap_rational(48, 4, Fraction(3, 10))
    g_2i_low = strong_to_freezing_coupling_gap_rational(120, 4, Fraction(1, 5))
    g_d27 = strong_to_freezing_coupling_gap_rational(27, 4, Fraction(1, 1))
    g_d54 = strong_to_freezing_coupling_gap_rational(54, 4, Fraction(5, 6))
    g_s1080_low = strong_to_freezing_coupling_gap_rational(1080, 4, Fraction(7, 15))
    assert Fraction(999, 1000) < g_q8 < g_2t < g_2o_low < g_2i_low
    assert Fraction(999, 1000) < g_d27 < g_d54 < g_s1080_low

    s168 = klein_sigma168_invariants_and_su3_chain_rational()
    assert s168["I11_3a"] == Fraction(1, 1)
    assert s168["I2_3a"] == Fraction(0, 1)
    assert s168["I3_3a"] == Fraction(1, 1)
    assert s168["I3_6"] == Fraction(2, 1)
    assert s168["I3_7"] == Fraction(2, 1)
    assert s168["I2_8"] == Fraction(1, 1)
    assert s168["I3_8"] == Fraction(3, 1)
    ds168x3_low, ds168x3_high = s168["delta_min_Sigma168x3_bounds"]
    exact_ds168x3 = (11.0 - math.sqrt(21.0)) / 12.0
    assert float(ds168x3_low) < exact_ds168x3 < float(ds168x3_high)
    assert Fraction(7, 15) < ds168x3_low < ds168x3_high < s168["delta_min_Sigma168"] < su3_tower["delta_min_Delta54"] < su3_tower["delta_min_Delta27"]

    q4 = quartic_character_invariants_and_continuum_matching_rational()
    assert q4["I4_Q8_2s"] == Fraction(4, 1)
    assert q4["I4_2T_2s"] == q4["I4_2O_2s"] == q4["I4_2I_2s"] == Fraction(2, 1)
    assert q4["I4_Delta27_3"] == Fraction(9, 1)
    assert q4["I4_Delta54_3"] == Fraction(5, 1)
    assert q4["I4_Sigma168_3a"] == q4["I4_Sigma1080_3a"] == Fraction(2, 1)

    hess = hessian_subgroups_and_quartic_adjoint_casimir_obstruction_rational()
    assert hess["I11_Sigma72x3_3"] == hess["I3_Sigma72x3_3"] == Fraction(1, 1)
    assert hess["I4_Sigma72x3_3"] == Fraction(2, 1)
    assert hess["I11_Sigma216x3_3"] == hess["I3_Sigma216x3_3"] == Fraction(1, 1)
    assert hess["I4_Sigma216x3_3"] == Fraction(2, 1)
    assert hess["I3_Sigma72x3_8"] == Fraction(7, 1)
    assert hess["I3_Sigma216x3_8"] == Fraction(3, 1)
    assert hess["I4_Sigma72x3_8"] == Fraction(57, 1)
    assert hess["I4_Sigma168_8"] == Fraction(25, 1)
    assert hess["I4_Sigma216x3_8"] == Fraction(21, 1)
    assert hess["I4_Sigma1080_8a"] == Fraction(13, 1)
    assert hess["I4_SU3_continuum_8"] == Fraction(8, 1)
    assert hess["a6_irrep_dim_sq_sum"] == 360 < hess["continuum_27_dim_sq"] == 729

    su2_hs = su2_higher_spin_casimir_and_hessian_defect_bounds_rational()
    assert su2_hs["I4_2T_3t"] == Fraction(7, 1)
    assert su2_hs["I4_2O_3"] == Fraction(4, 1)
    assert su2_hs["I4_2I_3a"] == su2_hs["I4_SU2_continuum_3"] == Fraction(3, 1)
    assert su2_hs["I4_2I_5t"] == Fraction(11, 1) > su2_hs["I4_SU2_continuum_5"] == Fraction(5, 1)
    assert su2_hs["a5_irrep_dim_sq_sum"] == 60
    assert su2_hs["2i_irrep_dim_sq_sum"] == 120
    assert su2_hs["poly_at_36_47"] < Fraction(0, 1) < su2_hs["poly_at_23_30"]
    d216_tight_l, d216_tight_u = su2_hs["delta_min_Sigma216x3_tight_bounds"]
    d216_l, d216_u = su2_hs["delta_min_Sigma216x3_bounds"]
    c1 = math.cos(2.0 * math.pi / 9.0)
    exact_d216 = (4.0 - 2.0 * c1 - 2.0 * (c1 ** 2)) / 3.0
    assert float(d216_tight_l) < exact_d216 < float(d216_tight_u)
    assert d216_l < d216_tight_l < d216_tight_u < d216_u < Fraction(11, 24)

    ffk = complete_blichfeldt_ffk_su3_crystal_hierarchy_rational()
    assert ffk["I11_Sigma36x3_3"] == ffk["I3_Sigma36x3_3"] == Fraction(1, 1)
    assert ffk["I4_Sigma36x3_3"] == Fraction(3, 1)
    assert ffk["I2_Sigma60_8"] == Fraction(2, 1)
    assert (ffk["I3_Delta27_8"], ffk["I3_Delta54_8"], ffk["I3_Sigma36x3_8"], ffk["I3_Sigma60_8"], ffk["I3_Sigma72x3_8"]) == (
        Fraction(56, 1),
        Fraction(28, 1),
        Fraction(14, 1),
        Fraction(9, 1),
        Fraction(7, 1),
    )
    assert (ffk["I4_Delta27_8"], ffk["I4_Delta54_8"], ffk["I4_Sigma36x3_8"], ffk["I4_Sigma60_8"], ffk["I4_Sigma72x3_8"]) == (
        Fraction(456, 1),
        Fraction(228, 1),
        Fraction(114, 1),
        Fraction(70, 1),
        Fraction(57, 1),
    )

    med = baryon_vs_gluon_screening_casimir_and_mednykh_2d_towers_rational()
    assert med["casimir_ratio_SU3_8_over_3"] == Fraction(9, 4)
    assert med["casimir_ratio_SU3_6_over_3"] == Fraction(5, 2)
    assert med["casimir_ratio_SU3_10_over_3"] == Fraction(9, 2)
    assert med["casimir_ratio_SU2_3a_over_2s"] == Fraction(8, 3)
    assert med["casimir_ratio_SU2_4s_over_2s"] == Fraction(5, 1)
    assert med["casimir_ratio_SU2_5t_over_2s"] == Fraction(8, 1)
    assert med["collar_ratio_3_over_6_e4"] == Fraction(16, 1)
    assert med["collar_ratio_3_over_8_e4"] == Fraction(4096, 81)
    assert Fraction(1, 1) < med["M2_2I"] < med["M2_2O"] < med["M2_2T"] < med["M2_Q8"]
    assert (med["Z2_Q8"], med["Z2_2T"], med["Z2_2O"], med["Z2_2I"]) == (272, 2224, 6992, 27576)
    assert med["sigma1080_irrep_dim_sq_sum"] == 1080
    assert med["M2_Sigma1080"] == Fraction(36011, 21600) < Fraction(2, 1)
    assert med["Z2_Sigma1080"] == 1944594 < med["Z2_Sigma216x3"] == 2001267

    med3 = higher_genus_mednykh_abelianization_and_genus3_bounds_rational()
    assert med3["ab_2I"] < med3["ab_2O"] < med3["ab_2T"] < med3["ab_Q8"]
    assert Fraction(1, 1) < med3["M3_2I"] < med3["M3_2O"] < med3["M3_2T"] < med3["M3_Q8"] == Fraction(65, 16)
    assert med3["M3_Q8"] - med3["ab_Q8"] == Fraction(1, 4) * (med["M2_Q8"] - med3["ab_Q8"])
    assert med3["M3_2I"] - med3["ab_2I"] < Fraction(1, 4) * (med["M2_2I"] - med3["ab_2I"])
    assert med3["M3_Sigma1080"] == Fraction(590783071, 559872000)
    assert Fraction(0, 1) < med3["M3_Sigma1080"] - med3["ab_Sigma1080"] < Fraction(3, 50) < Fraction(1, 9) * (med["M2_Sigma1080"] - med3["ab_Sigma1080"])
    assert Fraction(2, 1) < med3["M3_Delta54"] < med3["M3_Sigma216x3"] < med3["M3_Delta27"] == Fraction(731, 81)

    gal = finite_coupling_galois_conjugate_suppression_rational(Fraction(1, 10))
    assert (gal["dk_2I_2sp_2s"], gal["dk_2I_3b_3a"], gal["dk_2I_4t_4s"]) == (6, 4, 3)
    assert (gal["dk_Sigma1080_8b_8a"], gal["dk_Sigma1080_3p_3"]) == (2, 4)
    assert gal["casimir_ratio_2sp_over_2s"] == Fraction(21, 1)
    assert gal["casimir_ratio_3b_over_3a"] == Fraction(6, 1)
    assert gal["casimir_ratio_4t_over_4s"] == Fraction(16, 5)
    assert gal["casimir_ratio_27_over_8a"] == Fraction(8, 3)
    assert gal["suppression_2sp_2s"] == Fraction(1, 1000000)
    assert gal["suppression_3b_3a"] == gal["suppression_3p_3"] == Fraction(1, 10000)
    assert gal["suppression_4t_4s"] == Fraction(1, 1000)
    assert gal["suppression_8b_8a"] == Fraction(1, 100)

    pf_med = temporal_gauge_perron_frobenius_and_2d_mednykh_pachner_rational()
    assert (
        pf_med["defect_sum_Q8"],
        pf_med["defect_sum_2T"],
        pf_med["defect_sum_2O"],
        pf_med["defect_sum_2I"],
        pf_med["defect_sum_Sigma1080"],
    ) == (Fraction(8, 1), Fraction(24, 1), Fraction(48, 1), Fraction(120, 1), Fraction(1080, 1))
    assert Fraction(0, 1) < pf_med["kappa_BH_1"] == Fraction(1, 3) < pf_med["kappa_BH_2"] == Fraction(3, 5) < pf_med["kappa_BH_4"] == Fraction(15, 17) < Fraction(1, 1)
    assert (pf_med["q8_comm_identity_count"], pf_med["q8_comm_minus_one_count"]) == (40, 24)
    assert pf_med["hom_g1_Q8"] == 40
    assert pf_med["hom_g2_Q8_bruteforce"] == pf_med["hom_g2_Q8"] == 2176
    assert (
        pf_med["hom_g2_2T"],
        pf_med["hom_g2_2O"],
        pf_med["hom_g2_2I"],
        pf_med["hom_g2_Sigma216x3"],
        pf_med["hom_g2_Sigma1080"],
    ) == (53376, 335616, 3309120, 1296821016, 2100161520)


def test_master_witness_passes() -> None:
    receipt = verify_fqcd_strong_coupling_area_law_witness()
    assert receipt["record_id"] == "TFQ-1052"
    assert receipt["dag_node"] == "FQCD-STRONG-COUPLING-AREA-LAW"
    assert receipt["all_passed"] is True
    assert receipt["total_checks"] >= 15
