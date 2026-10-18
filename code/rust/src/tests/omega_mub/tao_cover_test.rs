//! Integration test suite for Terence Tao S6 seed triple branch-and-bound cover certification.
//!
//! AuthorityEffect: None
//! Restricted words: forced, minimal, free, canonical, equivalent, universal, complete
//! require proof or explicit conditional scope.

use num_rational::BigRational;
use num_traits::Zero;
use omega_mub::omega_native::exact::d6_exact_curvature_cochain::D;
use omega_mub::omega_native::exact::mub6_tao_cover::{
    build_kernel_reflection_tao_s6_complex, cover_tao_narrow_cell, cover_tao_wide_cell,
    tao_gauge_fixed_chunk_cover, tao_seed_smoke_check, tao_seed_triple_columns,
    write_kernel_reflection_tao_s6_artifact, KernelReflectionScaledArtifact,
};
use omega_mub::omega_native::exact::szollosi_triad_solver::{tao_s6_matrix, verify_chm};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

#[test]
fn test_tao_s6_matrix_is_exact_chm() {
    let s6 = tao_s6_matrix();
    let rep = verify_chm(&s6);
    assert!(rep.is_chm, "Tao S6 must be an exact CHM: {:?}", rep);
    assert!(rep.all_entries_unit_modulus);
    assert!(rep.is_orthogonal);
}

#[test]
fn test_tao_seed_triple_columns_orthonormal_and_unit() {
    let cols = tao_seed_triple_columns();
    assert_eq!(
        cols.len(),
        18,
        "Triple must contain exactly 18 column vectors"
    );
    let one = Cyc24::rat(ri(1));

    // Every column must be a unit vector in C^6: ⟨v, v⟩ = 1
    for (idx, v) in cols.iter().enumerate() {
        let mut norm_sq = Cyc24::zero();
        for k in 0..D {
            norm_sq = norm_sq.add(&v[k].mul(&v[k].conj()));
        }
        assert_eq!(norm_sq, one, "Column {idx} must have norm squared 1");
    }

    // B1 columns (0..6) are standard basis
    for j in 0..D {
        for k in 0..D {
            if j == k {
                assert_eq!(cols[j][k], one);
            } else {
                assert_eq!(cols[j][k], Cyc24::zero());
            }
        }
    }

    // B2 columns (6..12) and B3 columns (12..18) have all entries with modulus 1/6
    let sixth = Cyc24::rat(ri(1) / ri(6));
    for idx in 6..18 {
        for k in 0..D {
            let mod_sq = cols[idx][k].mul(&cols[idx][k].conj());
            assert_eq!(
                mod_sq, sixth,
                "Column {idx} entry {k} must have modulus squared 1/6"
            );
        }
    }
}

#[test]
fn test_tao_smoke_check_excludes_bad_box() {
    let (excluded, gap) = tao_seed_smoke_check();
    assert!(excluded, "Smoke check must exclude bad basis box");
    assert!(gap.is_some());
    let gap_str = gap.unwrap();
    assert!(!gap_str.is_empty());
}

#[test]
fn test_tao_narrow_cell_cover() {
    let cert = cover_tao_narrow_cell(24);
    assert!(cert.complete, "Narrow cell cover must be complete");
    assert_eq!(
        cert.uncertified, 0,
        "Narrow cell cover must have 0 uncertified cells"
    );
    assert!(cert.certified > 0, "Must have certified cells");
    assert!(cert.min_gap.is_some(), "Must have exact rational min_gap");
}

#[test]
fn test_tao_wide_cell_cover() {
    let cert = cover_tao_wide_cell(30);
    assert!(cert.complete, "Wide cell cover must be complete");
    assert_eq!(
        cert.uncertified, 0,
        "Wide cell cover must have 0 uncertified cells"
    );
    assert!(cert.certified > 0, "Must have certified cells");
    assert!(cert.min_gap.is_some(), "Must have exact rational min_gap");
}

#[test]
fn test_tao_gauge_fixed_single_chunk_cover() {
    // Shallow pilot: self-consistent complete flag on 5-torus chunk
    let cert = tao_gauge_fixed_chunk_cover(2, 0, 6);
    assert_eq!(cert.complete, cert.uncertified == 0);
    assert!(cert.certified + cert.off_torus + cert.uncertified > 0);
}

#[test]
fn test_tao_scaled_reflection_complex_generation_and_artifact_emission() {
    // Generate complex of 64 boxes on narrow torus cell
    let complex = build_kernel_reflection_tao_s6_complex(6);
    assert_eq!(
        complex.schema_version,
        "omega.mub.kernel-reflection-scaled.v1"
    );
    assert_eq!(complex.complex.box_count, 64);
    assert_eq!(complex.boxes.len(), 64);
    assert!(complex.complex.complete);
    assert_eq!(complex.complex.uncertified, 0);

    for (i, b) in complex.boxes.iter().enumerate() {
        assert_eq!(b.index, i);
        let num: num_bigint::BigInt = b.num.parse().expect("valid integer numerator");
        let den: num_bigint::BigInt = b.den.parse().expect("valid integer denominator");
        assert!(
            num > num_bigint::BigInt::zero(),
            "Box {i} numerator must be positive"
        );
        assert!(
            den > num_bigint::BigInt::zero(),
            "Box {i} denominator must be positive"
        );
        let gap_rat = BigRational::new(num, den);
        assert!(gap_rat > BigRational::zero());
    }

    // Write artifact to disk and verify parsing
    let path = write_kernel_reflection_tao_s6_artifact(6).expect("Artifact write must succeed");
    assert!(path.exists());
    let raw = std::fs::read_to_string(&path).expect("Read artifact JSON");
    assert!(raw.contains("omega.mub.kernel-reflection-scaled.v1"));
    assert!(raw.contains("stated region only"));
    assert!(raw.contains("AuthorityEffect: None"));

    let deserialized: KernelReflectionScaledArtifact =
        serde_json::from_str(&raw).expect("Deserialize artifact JSON");
    assert_eq!(deserialized.complex.box_count, 64);
    assert_eq!(deserialized.boxes.len(), 64);
    assert!(deserialized.complex.complete);
    assert_eq!(deserialized.complex.uncertified, 0);
}
