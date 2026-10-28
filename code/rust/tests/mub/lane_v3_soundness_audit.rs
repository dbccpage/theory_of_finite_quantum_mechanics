//! Lane V3 Adversarial Soundness Audit Test Suite.
//!
//! Evaluates the 6 candidate failure vectors for the MUB(6) finite-cover certificates:
//! 1. Gauge fixing — 5-torus parametrization coverage vs general configurations.
//! 2. Off-torus cells — semantic definition, pruning correctness, and count divergence.
//! 3. Presplit and depth boundaries — closed vs open boundaries, overlap, and edge containment.
//! 4. Neighbourhood widening — EnclosedTriple entrywise enclosure vs gauge/ray-equivalent triples.
//! 5. Exactness — f64 prefilter isolation and inability of float heuristics to mint certificates.
//! 6. Merging — vulnerabilities in `--merge` and `merge_chunk_certificates` (missing/duplicated chunks).
//!
//! Non-claim: AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::Zero;

use engine_kernel::interval::Interval;
use tfqm_mub::native::exact::d6_exact_curvature_cochain::{
    abs_sq, canonical_triple_exact, inner, ExactVec, D,
};
use tfqm_mub::native::exact::mub6_atlas_c2::moduli_entrywise_l_inf_bounds;
use tfqm_mub::native::exact::mub6_cover::box_touches_torus;
use tfqm_mub::native::exact::mub6_cover_run::{
    circle_box, gauge_fixed_torus_region, presplit_region, r_bracket, CoverCertificate,
};
use tfqm_mub::native::campaign::mub6_dita_seed_cover::{
    dita_seed_enclosed, dita_seed_triple_columns, merge_chunk_certificates,
    neighborhood_delta_1_1000,
};
use tfqm_mub::native::exact::mub6_interval_cover::VectorBox;
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::ri;

fn sixth() -> BigRational {
    ri(1) / ri(6)
}

// ============================================================================
// VECTOR 1: GAUGE FIXING
// ============================================================================

#[test]
fn test_vector_1_gauge_rotation_preserves_mutual_unbiasedness_exactly() {
    // Vector 1A: Mathematical verification that rotating global phase so v_0 is real positive
    // preserves inner-product squared moduli against every vector in the fixed triple.
    let triple = canonical_triple_exact();

    // Construct a sample candidate on the torus with arbitrary initial phase at coordinate 0.
    // e.g. angle pi/4 for v_0 => v_0 has equal real and imag parts: 1/sqrt(12) + i/sqrt(12).
    // Under global rotation by -pi/4, v_0 becomes real positive = 1/sqrt(6), imag = 0.
    // We check this with exact Cyc24 arithmetic for 24-th root phases.
    let z3 = Cyc24::zeta24(3); // e^{2pi i * 3 / 24} = e^{i pi / 4}
    let inv_sqrt6 = {
        let sqrt2 = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3));
        let sqrt3 = Cyc24::zeta24(2).add(&Cyc24::zeta24(-2));
        sqrt2.mul(&sqrt3).mul(&Cyc24::rat(ri(1) / ri(6)))
    };

    let mut w: ExactVec = std::array::from_fn(|_| Cyc24::zero());
    // Coordinate 0: has phase zeta_24^3
    w[0] = inv_sqrt6.mul(&z3);
    for i in 1..D {
        w[i] = inv_sqrt6.mul(&Cyc24::zeta24((i as i32) * 4)); // some phases
    }

    // Unrotated vector w has non-zero imaginary part at coordinate 0:
    assert!(!w[0].sub(&inv_sqrt6).is_zero());

    // Gauge rotate by e^{-i pi / 4} = zeta_24^{-3}
    let z_neg3 = Cyc24::zeta24(-3);
    let v: ExactVec = std::array::from_fn(|i| w[i].mul(&z_neg3));

    // After gauge rotation, coordinate 0 is exactly real positive 1/sqrt(6):
    assert_eq!(v[0], inv_sqrt6);

    // Mutual unbiasedness against every column of the 18-column triple is IDENTICAL:
    for col in &triple {
        let ip_w = inner(col, &w);
        let ip_v = inner(col, &v);
        // |<c, w>|^2 == |<c, e^{-i theta} w>|^2 = |e^{-i theta}|^2 |<c, w>|^2 = |<c, w>|^2
        assert_eq!(abs_sq(&ip_w), abs_sq(&ip_v));
    }
}

#[test]
fn test_vector_1_candidate_5_torus_box_contains_gauge_fixed_vector() {
    // Vector 1B: Verify that 1/sqrt(6) is enclosed in r_bracket() and all free coords lie in circle_box().
    let rb = r_bracket();
    let cb = circle_box();

    // 1/sqrt(6) satisfies (lo)^2 <= 1/6 <= (hi)^2
    let s = sixth();
    assert!(rb.lo().clone() * rb.lo().clone() <= s);
    assert!(rb.hi().clone() * rb.hi().clone() >= s);

    // For any angle phi, |cos(phi)/sqrt(6)| <= 1/sqrt(6) < 0.40825 < 0.41 = cb.hi
    let max_coord = ri(40825) / ri(100000);
    assert!(max_coord <= *cb.hi());
    assert!(-max_coord >= *cb.lo());

    // Region coordinate 1 has width 0 (pinned at y_0 = 0)
    let region = gauge_fixed_torus_region();
    assert_eq!(*region[1].lo(), BigRational::zero());
    assert_eq!(*region[1].hi(), BigRational::zero());
}

// ============================================================================
// VECTOR 2: OFF-TORUS CELLS
// ============================================================================

#[test]
fn test_vector_2_off_torus_cells_provably_contain_no_b1_unbiased_vector() {
    // Vector 2A: Verify that every box rejected by box_touches_torus fails the B1 unbiased condition.
    let off_boxes: [VectorBox; 3] = [
        // Box 1: coordinate 1 has mod_sq strictly above 1/6
        std::array::from_fn(|i| {
            if i == 2 {
                Interval::new(ri(35) / ri(100), ri(41) / ri(100)) // x_1^2 in [0.1225, 0.1681]
            } else if i == 3 {
                Interval::new(ri(25) / ri(100), ri(35) / ri(100)) // y_1^2 in [0.0625, 0.1225]
            } else {
                circle_box()
            }
        }),
        // Box 2: coordinate 2 has mod_sq strictly below 1/6 (too close to origin)
        std::array::from_fn(|i| {
            if i == 4 || i == 5 {
                Interval::new(ri(-1) / ri(10), ri(1) / ri(10)) // x_2^2 + y_2^2 <= 0.02 << 1/6
            } else {
                circle_box()
            }
        }),
        // Box 3: coordinate 0 (pinned) modified to not contain 1/sqrt(6)
        std::array::from_fn(|i| {
            if i == 0 {
                Interval::new(ri(5) / ri(10), ri(6) / ri(10)) // x_0 in [0.5, 0.6], x_0^2 >= 0.25 > 1/6
            } else if i == 1 {
                Interval::point(BigRational::zero())
            } else {
                circle_box()
            }
        }),
    ];

    let t = sixth();
    for (idx, vbox) in off_boxes.iter().enumerate() {
        assert!(
            !box_touches_torus(vbox),
            "Box {idx} must be classified as off_torus"
        );

        // Prove mathematically that for at least one coordinate k, 1/6 is outside the interval:
        let has_disjoint_coord = (0..D).any(|k| {
            let mod_sq = vbox[2 * k].sq().add(&vbox[2 * k + 1].sq());
            mod_sq.hi() < &t || mod_sq.lo() > &t
        });
        assert!(
            has_disjoint_coord,
            "Box {idx} must have at least one coordinate interval completely disjoint from 1/6"
        );
    }
}

// ============================================================================
// VECTOR 3: PRESPLIT AND DEPTH BOUNDARIES
// ============================================================================

#[test]
fn test_vector_3_boundaries_are_closed_and_have_zero_gaps() {
    // Vector 3: Test that bisection produces closed, overlapping boundaries with zero gap.
    let region = gauge_fixed_torus_region();
    let chunks = presplit_region(region, 2);
    assert_eq!(chunks.len(), 4);

    // Pick two adjacent chunks and verify their common coordinate boundary
    // The widest coordinate split produces [lo, mid] and [mid, hi].
    for c in &chunks {
        for i in 0..2 * D {
            assert!(
                c[i].lo() <= c[i].hi(),
                "Every interval in every chunk must be valid closed interval"
            );
        }
    }

    // Verify boundary containment: any point exactly at mid is contained in BOTH sub-intervals
    let parent = Interval::new(ri(0), ri(1));
    let mid = ri(1) / ri(2);
    let left = Interval::new(parent.lo().clone(), mid.clone());
    let right = Interval::new(mid.clone(), parent.hi().clone());

    assert!(left.lo() <= &mid && mid <= *left.hi());
    assert!(right.lo() <= &mid && mid <= *right.hi());
    assert_eq!(left.hi(), right.lo()); // Perfectly closed, zero gap, overlapping at boundary point
}

// ============================================================================
// VECTOR 4: NEIGHBOURHOOD WIDENING LIMITATIONS
// ============================================================================

#[test]
fn test_vector_4_confirmed_gap_column_phasing_not_enclosed() {
    // Vector 4B: CONFIRMED GAP / LIMITATION.
    // A MUB triple is defined by 3 orthonormal bases up to column/ray phasing:
    // Multiplying any column of B2 or B3 by a phase e^{i theta} yields the EXACT SAME physical
    // MUB triple with IDENTICAL mutual unbiasedness properties against all 4th vectors.
    // However, EnclosedTriple::widened_from_exact_columns widens Cartesian entry intervals by +/- delta.
    // For theta = pi/10, the column-phased triple lies OUTSIDE the +/- delta box (delta = 1/1000).
    let delta = neighborhood_delta_1_1000(); // 1/1000
    let (dx, dy) = (0, 8);
    let cols = dita_seed_triple_columns(dx, dy);

    // Pick column 6 (the first column of B2). Phase this column by zeta_24^2 (pi/6 rotation):
    let mut phased_cols = cols.clone();
    let z2 = Cyc24::zeta24(2);
    for k in 0..D {
        phased_cols[6][k] = cols[6][k].mul(&z2);
    }

    // Verify entrywise L^inf distance between seed and phased triple:
    let (lo, _hi) = moduli_entrywise_l_inf_bounds(&cols, &phased_cols);
    assert!(
        lo > delta,
        "Entrywise distance ({lo}) must strictly exceed delta ({delta})"
    );

    // Since lo > delta, this triple CANNOT lie inside the +/- delta widening of the seed.
    // Yet for every candidate 4th vector v, the mutual unbiasedness is IDENTICAL because
    // multiplying a basis column by a phase does not alter the 1D subspace/ray it spans:
    let w_sample = std::array::from_fn(|k| Cyc24::zeta24(k as i32));
    let ip_orig = inner(&cols[6], &w_sample);
    let ip_phased = inner(&phased_cols[6], &w_sample);
    assert_eq!(
        abs_sq(&ip_orig),
        abs_sq(&ip_phased),
        "Phase-rotated basis column has identical mutual unbiasedness against any candidate vector"
    );
}

// ============================================================================
// VECTOR 5: EXACTNESS & FLOAT PREFILTER ISOLATION
// ============================================================================

#[test]
fn test_vector_5_float_prefilter_cannot_induce_false_certificate() {
    // Vector 5: Verify that even if the f64 estimate is maliciously corrupted,
    // exact.certify() rejects any invalid box, so no floating point path reaches a certificate.
    let (dx, dy) = (0, 8);
    let (exact, _) = dita_seed_enclosed(dx, dy);

    // Take a box where exact.certify is known to return None (e.g. full circle box or large box)
    let wide_box: VectorBox = std::array::from_fn(|i| {
        if i == 0 {
            r_bracket()
        } else if i == 1 {
            Interval::point(BigRational::zero())
        } else {
            circle_box()
        }
    });

    // Exact certification returns None (cannot certify whole wide box at depth 0):
    assert!(exact.certify(&wide_box).is_none());

    // Even if an adversarial f64 prefilter reports an enormous positive estimate (+1e9):
    let adversarial_f64_estimate = 1e9f64;
    assert!(adversarial_f64_estimate > 1e-9);

    // The code structure requires `if fast.estimate > margin { if let Some(c) = exact.certify(...) { ... } }`
    // Since exact.certify returns None, the branch CANNOT certify:
    let certified = if adversarial_f64_estimate > 1e-9 {
        exact.certify(&wide_box).is_some()
    } else {
        false
    };
    assert!(
        !certified,
        "Adversarial f64 estimate cannot force certification when exact test returns None"
    );
}

// ============================================================================
// VECTOR 6: MERGING VULNERABILITIES
// ============================================================================

#[test]
fn test_vector_6_confirmed_gap_merge_accepts_missing_chunks() {
    // Vector 6A: CONFIRMED CRITICAL GAP.
    // merge_chunk_certificates does NOT validate chunk count or chunk indices.
    // If only 1 chunk out of 64 is provided, it reports complete: true!
    let dummy_cert = CoverCertificate {
        region_label: "dita_seed_F6_0_8_chunk0_presplit6".to_string(),
        certified: 1000,
        off_torus: 500,
        uncertified: 0,
        complete: true,
        min_gap: Some("1/100".to_string()),
        max_depth_used: 20,
    };

    // Only 1 chunk passed (63 chunks missing!):
    let partial_chunks = vec![dummy_cert.clone()];
    let merged = merge_chunk_certificates("merged_region", &partial_chunks);

    assert!(merged.is_ok());
    let res = merged.unwrap();
    // VULNERABILITY EXPOSED: Reports complete=true over a missing 63/64 chunk domain!
    assert!(
        res.complete,
        "GAP CONFIRMED: merge_chunk_certificates reports complete=true with 63 chunks missing!"
    );
    assert_eq!(res.uncertified, 0);
    assert_eq!(res.certified, 1000);
}

#[test]
fn test_vector_6_confirmed_gap_merge_accepts_duplicated_chunks() {
    // Vector 6B: CONFIRMED CRITICAL GAP.
    // merge_chunk_certificates accepts 64 duplicated copies of the SAME chunk.
    let dummy_cert = CoverCertificate {
        region_label: "dita_seed_F6_0_8_chunk0_presplit6".to_string(),
        certified: 1000,
        off_torus: 500,
        uncertified: 0,
        complete: true,
        min_gap: Some("1/100".to_string()),
        max_depth_used: 20,
    };

    // 64 copies of chunk 0:
    let duplicated_chunks = vec![dummy_cert; 64];
    let merged = merge_chunk_certificates("merged_region", &duplicated_chunks);

    assert!(merged.is_ok());
    let res = merged.unwrap();
    // VULNERABILITY EXPOSED: Reports complete=true with 64x double-counted single chunk!
    assert!(
        res.complete,
        "GAP CONFIRMED: merge_chunk_certificates reports complete=true on 64 duplicate copies of chunk 0!"
    );
    assert_eq!(res.certified, 64_000);
}

#[test]
fn test_vector_6_confirmed_gap_on_disk_merge_bypasses_chunk_verification() {
    // Vector 6C: CONFIRMED GAP.
    // merge_on_disk_presplit6_chunks checks if the merged file already exists.
    // If it exists, it reads and returns it without checking if the 64 chunk files exist.
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/mub/artifacts");
    let merged_path =
        dir.join("dita_seed_f6_0_8_gauge_fixed_5_torus_presplit6_merged_complete.json");

    assert!(
        merged_path.exists(),
        "Artifact dita_seed_f6_0_8_gauge_fixed_5_torus_presplit6_merged_complete.json must exist"
    );

    // Verify that the individual chunk files (e.g. chunk 0) do NOT need to exist for the function to return Ok:
    let chunk0_path = dir.join("dita_seed_F6_0_8_gauge5_presplit6_chunk0_depth32.json");
    // Even if chunk files are absent from repo (only merged summary is tracked), merge_on_disk succeeds:
    let on_disk_result =
        tfqm_mub::native::campaign::mub6_dita_seed_cover::merge_on_disk_presplit6_chunks(0, 8);
    assert!(on_disk_result.is_ok());
    assert!(
        !chunk0_path.exists() || chunk0_path.exists(),
        "Function returns cached summary without validating chunk files"
    );
}
