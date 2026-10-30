//! Unit tests for FQCD Strong-Coupling Area Law (Record TFQ-1052).
//!
//! Governing DAG target node: FQCD-STRONG-COUPLING-AREA-LAW
//! AuthorityEffect: None

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};

use theory_of_finite_qm::crate_root_inventory_holds;
use theory_of_finite_qm::fqcd::{
    a5_cubic_character_invariants, area_law_decay_bound_rational,
    baryon_vs_gluon_casimir_and_mednykh_2d_towers, beta0_rational_approx,
    beta0_rational_bounds, binary_icosahedral_2i_invariants, check_geometric_cluster_series_bound,
    cluster_series_geometric_sum, collar_tube_contraction,
    complete_blichfeldt_ffk_su3_crystal_hierarchy, const_k, coordination_number_delta,
    d4_multi_plaquette_collar_bound, finite_coupling_galois_conjugate_suppression,
    freezing_plaquette_defect_bounds,
    general_collar_tube_contraction, hessian_subgroups_and_quartic_adjoint_casimir_obstruction,
    higher_genus_mednykh_abelianization_and_genus3_bounds,
    klein_sigma168_invariants_and_su3_chain, loop_perimeter, minimal_spanning_area,
    normal_directions_count, q8_center_parity_non_screening_verified,
    q8_cubic_character_invariant_sum, quartic_character_invariants_and_continuum_matching,
    s3_cubic_character_invariant_sum, s4_cubic_character_invariants,
    strong_to_freezing_coupling_gap, su2_ade_binary_polyhedral_tower,
    su2_higher_spin_casimir_and_hessian_defect_bounds,
    su3_subgroup_tower_and_freezing_scales,
    temporal_gauge_perron_frobenius_and_2d_mednykh_pachner,
    twod_character_decimation_area_law,
    valentiner_sigma1080_invariants, verify_fqcd_strong_coupling_area_law_witness,
    wilson_dirac_gamma5_and_two_flavor_positivity,
};

fn rat(n: i64, d: i64) -> BigRational {
    BigRational::new(BigInt::from(n), BigInt::from(d))
}

#[test]
fn test_coordination_numbers_and_refusals() {
    assert_eq!(coordination_number_delta(2).unwrap(), 4);
    assert_eq!(coordination_number_delta(3).unwrap(), 12);
    assert_eq!(coordination_number_delta(4).unwrap(), 24);
    assert_eq!(coordination_number_delta(5).unwrap(), 40);
    assert_eq!(coordination_number_delta(6).unwrap(), 60);

    assert!(coordination_number_delta(1).is_err());
    assert!(coordination_number_delta(0).is_err());
}

#[test]
fn test_beta0_rational_bounds_and_approx() {
    for n in [2, 3, 5] {
        for d in [2, 3, 4] {
            let (lower, upper) = beta0_rational_bounds(n, d).unwrap();
            let approx = beta0_rational_approx(n, d).unwrap();

            assert!(lower > BigRational::zero());
            assert!(upper > lower);
            assert!(approx >= lower && approx <= upper);
        }
    }

    // Monotonicity: decreasing in d and N
    let b_2_2 = beta0_rational_approx(2, 2).unwrap();
    let b_2_3 = beta0_rational_approx(2, 3).unwrap();
    let b_2_4 = beta0_rational_approx(2, 4).unwrap();
    assert!(b_2_2 > b_2_3);
    assert!(b_2_3 > b_2_4);

    let b_3_4 = beta0_rational_approx(3, 4).unwrap();
    let b_4_4 = beta0_rational_approx(4, 4).unwrap();
    assert!(b_2_4 > b_3_4);
    assert!(b_3_4 > b_4_4);

    assert!(beta0_rational_bounds(1, 4).is_err());
    assert!(beta0_rational_bounds(2, 1).is_err());
}

#[test]
fn test_spanning_area_and_perimeter() {
    assert_eq!(minimal_spanning_area(1, 1).unwrap(), 1);
    assert_eq!(loop_perimeter(1, 1).unwrap(), 4);

    assert_eq!(minimal_spanning_area(3, 5).unwrap(), 15);
    assert_eq!(loop_perimeter(3, 5).unwrap(), 16);

    assert_eq!(minimal_spanning_area(10, 20).unwrap(), 200);
    assert_eq!(loop_perimeter(10, 20).unwrap(), 60);

    assert!(minimal_spanning_area(0, 5).is_err());
    assert!(minimal_spanning_area(5, 0).is_err());
    assert!(loop_perimeter(0, 5).is_err());
}

#[test]
fn test_exact_constants_and_decay_bound() {
    assert_eq!(const_k(), BigRational::one());

    for a in 1..=8 {
        let bound = area_law_decay_bound_rational(a).unwrap();
        let expected = rat(1, 4i64.pow(a as u32));
        assert_eq!(bound, expected);
    }

    assert!(area_law_decay_bound_rational(0).is_err());
}

#[test]
fn test_cluster_series_geometric_sum_and_bound() {
    let mu_fifth = rat(1, 5);
    for a in 1..=10 {
        let s = cluster_series_geometric_sum(&mu_fifth, a).unwrap();
        let b = area_law_decay_bound_rational(a).unwrap();
        assert!(s <= b);
        assert!(check_geometric_cluster_series_bound(&mu_fifth, a).unwrap());
    }

    // Equality at Area = 1: s = (1/5) / (4/5) = 1/4 == bound(1) = 1/4
    let s1 = cluster_series_geometric_sum(&mu_fifth, 1).unwrap();
    assert_eq!(s1, rat(1, 4));

    // Refusal on invalid mu
    assert!(cluster_series_geometric_sum(&rat(1, 1), 1).is_err());
    assert!(cluster_series_geometric_sum(&rat(-1, 5), 1).is_err());
    assert!(cluster_series_geometric_sum(&mu_fifth, 0).is_err());
}

#[test]
fn test_s3_cubic_character_invariant_and_screening() {
    assert_eq!(s3_cubic_character_invariant_sum(), BigRational::one());

    assert_eq!(collar_tube_contraction(0), BigRational::one());
    assert_eq!(collar_tube_contraction(1), rat(1, 2));
    assert_eq!(collar_tube_contraction(17), rat(1, 131072));
    assert!(collar_tube_contraction(17) > BigRational::zero());
}

#[test]
fn test_q8_cubic_character_invariant_and_protection() {
    assert!(q8_cubic_character_invariant_sum().is_zero());
    assert!(q8_center_parity_non_screening_verified());
}

#[test]
fn test_twod_character_decimation_area_law() {
    let alpha = rat(1, 5);
    // Abelian (dim R = 1): (1/5)^Area
    for a in 1..=4 {
        let dec = twod_character_decimation_area_law(1, &alpha, a).unwrap();
        let expected = rat(1, 5i64.pow(a as u32));
        assert_eq!(dec, expected);
    }

    // Non-abelian (dim R = 2): 2^{1 - Area} * (1/5)^Area
    let dec1 = twod_character_decimation_area_law(2, &alpha, 1).unwrap();
    assert_eq!(dec1, rat(1, 5));

    let dec2 = twod_character_decimation_area_law(2, &alpha, 2).unwrap();
    assert_eq!(dec2, rat(1, 50));

    let dec3 = twod_character_decimation_area_law(2, &alpha, 3).unwrap();
    assert_eq!(dec3, rat(1, 500));

    assert!(twod_character_decimation_area_law(0, &alpha, 1).is_err());
    assert!(twod_character_decimation_area_law(1, &alpha, 0).is_err());
}

#[test]
fn test_s4_and_a5_cubic_invariants_and_d4_collar_bounds() {
    let (s4_3, s4_3p, s4_2, s4_sgn) = s4_cubic_character_invariants();
    assert_eq!(s4_3, BigRational::one());
    assert_eq!(s4_3p, BigRational::one());
    assert_eq!(s4_2, BigRational::one());
    assert!(s4_sgn.is_zero());

    let (a5_3a, a5_3b, a5_4, a5_5) = a5_cubic_character_invariants();
    assert_eq!(a5_3a, BigRational::one());
    assert_eq!(a5_3b, BigRational::one());
    assert_eq!(a5_4, BigRational::one());
    assert_eq!(a5_5, rat(2, 1));

    let c2 = general_collar_tube_contraction(2, 4).unwrap();
    let c3 = general_collar_tube_contraction(3, 4).unwrap();
    let c4 = general_collar_tube_contraction(4, 4).unwrap();
    let c5 = general_collar_tube_contraction(5, 4).unwrap();
    assert!(c2 > c3 && c3 > c4 && c4 > c5 && c5 > BigRational::zero());

    assert_eq!(normal_directions_count(3).unwrap(), 2);
    assert_eq!(normal_directions_count(4).unwrap(), 4);
    assert!(normal_directions_count(2).is_err());

    let beta = rat(1, 10);
    let b1 = d4_multi_plaquette_collar_bound(4, 1, 2, &beta).unwrap();
    let b2 = d4_multi_plaquette_collar_bound(4, 2, 2, &beta).unwrap();
    let b1_d3 = d4_multi_plaquette_collar_bound(4, 1, 3, &beta).unwrap();
    assert_eq!(b1, rat(1, 1_000_000_000_000));
    assert!(b2 < b1 && b2 > BigRational::zero());
    assert!(b1_d3 < b1 && b1_d3 > BigRational::zero());
}

#[test]
fn test_binary_icosahedral_2i_and_valentiner_sigma1080_and_freezing_defects() {
    let (i2i_2s, i2i_3a, i2i_4t, i2i_5t) = binary_icosahedral_2i_invariants();
    assert_eq!(i2i_2s, BigRational::zero());
    assert_eq!(i2i_3a, BigRational::one());
    assert_eq!(i2i_4t, BigRational::one());
    assert_eq!(i2i_5t, rat(2, 1));

    let (s_i11, s_i2, s_i3_3a, s_i3_5a, s_i3_8a, s_i3_10) = valentiner_sigma1080_invariants();
    assert_eq!(s_i11, BigRational::one());
    assert_eq!(s_i2, BigRational::zero());
    assert_eq!(s_i3_3a, BigRational::one());
    assert_eq!(s_i3_5a, BigRational::one());
    assert_eq!(s_i3_8a, rat(2, 1));
    assert_eq!(s_i3_10, rat(2, 1));

    let (d2i_l, d2i_u, ds_l, ds_u) = freezing_plaquette_defect_bounds();
    assert!(BigRational::zero() < d2i_l && d2i_l < d2i_u && d2i_u < ds_l && ds_l < ds_u && ds_u < BigRational::one());

    let (i3_2t_2s, i3_2t_3t, i3_2o_2s, i3_2o_3, d2o_l, d2o_u, d2t, dq8) =
        su2_ade_binary_polyhedral_tower();
    assert_eq!(i3_2t_2s, BigRational::zero());
    assert_eq!(i3_2t_3t, rat(2, 1));
    assert_eq!(i3_2o_2s, BigRational::zero());
    assert_eq!(i3_2o_3, BigRational::one());
    assert!(d2i_u < d2o_l && d2o_l < d2o_u && d2o_u < d2t && d2t < dq8);

    let (i3_d27, i3_d54_1, i3_d54_2, bf_d27, bf_d54, bf_s_l, bf_s_u) =
        su3_subgroup_tower_and_freezing_scales();
    assert_eq!(i3_d27, rat(3, 1));
    assert_eq!(i3_d54_1, BigRational::one());
    assert_eq!(i3_d54_2, rat(2, 1));
    assert!(bf_d27 < bf_d54 && bf_d54 < bf_s_l && bf_s_l < bf_s_u);

    let g_q8 = strong_to_freezing_coupling_gap(8, 4, &dq8).unwrap();
    let g_2t = strong_to_freezing_coupling_gap(24, 4, &d2t).unwrap();
    let g_2o_l = strong_to_freezing_coupling_gap(48, 4, &d2o_u).unwrap();
    let g_2i_l = strong_to_freezing_coupling_gap(120, 4, &d2i_u).unwrap();
    assert!(rat(999, 1000) < g_q8 && g_q8 < g_2t && g_2t < g_2o_l && g_2o_l < g_2i_l);

    let (k_i11, k_i2, k_i3_3a, k_i3_6, k_i3_7, k_i2_8, k_i3_8, ds168x3_l, ds168x3_u, ds168) =
        klein_sigma168_invariants_and_su3_chain();
    assert_eq!(k_i11, BigRational::one());
    assert_eq!(k_i2, BigRational::zero());
    assert_eq!(k_i3_3a, BigRational::one());
    assert_eq!(k_i3_6, rat(2, 1));
    assert_eq!(k_i3_7, rat(2, 1));
    assert_eq!(k_i2_8, BigRational::one());
    assert_eq!(k_i3_8, rat(3, 1));
    assert!(s_i3_8a < k_i3_8);
    assert!(ds_u < ds168x3_l && ds168x3_l < ds168x3_u && ds168x3_u < ds168 && ds168 < rat(5, 6));

    let (i4_q8, i4_2t, i4_2o, i4_2i, i4_d27, i4_d54, i4_s168, i4_s1080) =
        quartic_character_invariants_and_continuum_matching();
    assert_eq!(i4_q8, rat(4, 1));
    assert_eq!(i4_2t, rat(2, 1));
    assert_eq!(i4_2o, rat(2, 1));
    assert_eq!(i4_2i, rat(2, 1));
    assert_eq!(i4_d27, rat(9, 1));
    assert_eq!(i4_d54, rat(5, 1));
    assert_eq!(i4_s168, rat(2, 1));
    assert_eq!(i4_s1080, rat(2, 1));
    assert!(i4_s1080 == i4_s168 && i4_s168 < i4_d54 && i4_d54 < i4_d27);

    let (
        i11_72,
        i3_72,
        i4_72,
        i11_216,
        i3_216,
        i4_216,
        i3_72_8,
        i3_216_8,
        i4_72_8,
        i4_168_8,
        i4_216_8,
        i4_1080_8,
        i4_su3_8,
    ) = hessian_subgroups_and_quartic_adjoint_casimir_obstruction();
    assert_eq!(i11_72, BigRational::one());
    assert_eq!(i3_72, BigRational::one());
    assert_eq!(i4_72, rat(2, 1));
    assert_eq!(i11_216, BigRational::one());
    assert_eq!(i3_216, BigRational::one());
    assert_eq!(i4_216, rat(2, 1));
    assert_eq!(i3_72_8, rat(7, 1));
    assert_eq!(i3_216_8, rat(3, 1));
    assert_eq!(i4_72_8, rat(57, 1));
    assert_eq!(i4_168_8, rat(25, 1));
    assert_eq!(i4_216_8, rat(21, 1));
    assert_eq!(i4_1080_8, rat(13, 1));
    assert_eq!(i4_su3_8, rat(8, 1));
    assert!(i4_su3_8 < i4_1080_8 && i4_1080_8 < i4_216_8 && i4_216_8 < i4_168_8 && i4_168_8 < i4_72_8);

    let (
        i4_2t_3,
        i4_2o_3,
        i4_2i_3,
        i4_su2_3,
        i4_2i_5,
        i4_su2_5,
        d216_tl,
        d216_tu,
        d216_l,
        d216_u,
    ) = su2_higher_spin_casimir_and_hessian_defect_bounds();
    assert_eq!(i4_2t_3, rat(7, 1));
    assert_eq!(i4_2o_3, rat(4, 1));
    assert_eq!(i4_2i_3, rat(3, 1));
    assert_eq!(i4_su2_3, rat(3, 1));
    assert_eq!(i4_2i_5, rat(11, 1));
    assert_eq!(i4_su2_5, rat(5, 1));
    assert!(d216_l < d216_tl && d216_tl < d216_tu && d216_tu < d216_u && d216_u < ds_l);

    let (
        i11_36,
        i3_36,
        i4_36,
        i2_60_8,
        i3_d27_8,
        i3_d54_8,
        i3_36_8,
        i3_60_8,
        i4_d27_8,
        i4_d54_8,
        i4_36_8,
        i4_60_8,
    ) = complete_blichfeldt_ffk_su3_crystal_hierarchy();
    assert_eq!(i11_36, BigRational::one());
    assert_eq!(i3_36, BigRational::one());
    assert_eq!(i4_36, rat(3, 1));
    assert_eq!(i2_60_8, rat(2, 1));
    assert_eq!(i3_d27_8, rat(56, 1));
    assert_eq!(i3_d54_8, rat(28, 1));
    assert_eq!(i3_36_8, rat(14, 1));
    assert_eq!(i3_60_8, rat(9, 1));
    assert_eq!(i4_d27_8, rat(456, 1));
    assert_eq!(i4_d54_8, rat(228, 1));
    assert_eq!(i4_36_8, rat(114, 1));
    assert_eq!(i4_60_8, rat(70, 1));
    assert!(i4_72_8 < i4_60_8 && i4_60_8 < i4_36_8 && i4_36_8 < i4_d54_8 && i4_d54_8 < i4_d27_8);

    let (
        c8_c3,
        c6_c3,
        c10_c3,
        c3_c2_su2,
        r_3_6,
        r_3_8,
        m2_q8,
        m2_2t,
        m2_2o,
        m2_2i,
        z2_2i,
        m2_s1080,
        z2_s1080,
        z2_s216x3,
    ) = baryon_vs_gluon_casimir_and_mednykh_2d_towers();
    assert_eq!(c8_c3, rat(9, 4));
    assert_eq!(c6_c3, rat(5, 2));
    assert_eq!(c10_c3, rat(9, 2));
    assert_eq!(c3_c2_su2, rat(8, 3));
    assert_eq!(r_3_6, rat(16, 1));
    assert_eq!(r_3_8, rat(4096, 81));
    assert!(BigRational::one() < m2_2i && m2_2i < m2_2o && m2_2o < m2_2t && m2_2t < m2_q8);
    assert_eq!(z2_2i, rat(27576, 1));
    assert!(m2_s1080 < rat(2, 1));
    assert_eq!(z2_s1080, rat(1944594, 1));
    assert_eq!(z2_s216x3, rat(2001267, 1));
    assert!(z2_s1080 < z2_s216x3);

    let (m3_q8, m3_2t, m3_2o, m3_2i, m3_d27, m3_d54, m3_s216, m3_s1080) =
        higher_genus_mednykh_abelianization_and_genus3_bounds();
    assert!(BigRational::one() < m3_2i && m3_2i < m3_2o && m3_2o < m3_2t && m3_2t < m3_q8);
    assert_eq!(&m3_q8 - rat(4, 1), rat(1, 4) * (&m2_q8 - rat(4, 1)));
    assert!(BigRational::zero() < (&m3_s1080 - BigRational::one())
        && (&m3_s1080 - BigRational::one()) < rat(1, 9) * (&m2_s1080 - BigRational::one())
        && (&m3_s1080 - BigRational::one()) < rat(3, 50));
    assert!(rat(2, 1) < m3_d54 && m3_d54 < m3_s216 && m3_s216 < m3_d27);

    let (dk_2sp, dk_3b, dk_4t, dk_8b, dk_3p, cr_2sp, cr_3b, cr_4t, cr_27, u6, u4, u3, u2) =
        finite_coupling_galois_conjugate_suppression();
    assert_eq!((dk_2sp, dk_3b, dk_4t, dk_8b, dk_3p), (6, 4, 3, 2, 4));
    assert_eq!(cr_2sp, rat(21, 1));
    assert_eq!(cr_3b, rat(6, 1));
    assert_eq!(cr_4t, rat(16, 5));
    assert_eq!(cr_27, rat(8, 3));
    assert!(BigRational::zero() < u6 && u6 < u4 && u4 < u3 && u3 < u2 && u2 < BigRational::one());

    let (
        def_q8,
        def_2t,
        def_2o,
        def_2i,
        def_s1080,
        kbh_1,
        kbh_2,
        kbh_4,
        hg1_q8,
        hg1_s1080,
        hg2_q8,
        hg2_2i,
        hg2_s1080,
    ) = temporal_gauge_perron_frobenius_and_2d_mednykh_pachner();
    assert_eq!(
        (def_q8, def_2t, def_2o, def_2i, def_s1080),
        (rat(8, 1), rat(24, 1), rat(48, 1), rat(120, 1), rat(1080, 1))
    );
    assert!(BigRational::zero() < kbh_1 && kbh_1 < kbh_2 && kbh_2 < kbh_4 && kbh_4 < BigRational::one());
    assert_eq!(
        (hg1_q8, hg1_s1080, hg2_q8, hg2_2i, hg2_s1080),
        (40, 18_360, 2_176, 3_309_120, 2_100_161_520)
    );

    let (dm3, dm2, dm1, d0, d1, tf_m1, tf_m2, tf_0, tf_1) =
        wilson_dirac_gamma5_and_two_flavor_positivity();
    assert_eq!((dm3, dm1), (rat(-3, 1), rat(-3, 1)));
    assert!(dm2.is_zero() && tf_m2.is_zero());
    assert_eq!(tf_m1, rat(9, 1));
    assert!(BigRational::zero() < tf_m1);
    assert_eq!((d0, d1, tf_0, tf_1), (rat(192, 1), rat(6237, 1), rat(36864, 1), rat(38900169, 1)));
}

#[test]
fn test_crate_root_inventory_integrity() {
    assert!(crate_root_inventory_holds().is_ok());
}

#[test]
fn test_master_witness_passes() {
    assert_eq!(verify_fqcd_strong_coupling_area_law_witness(), Ok(true));
}
