//! Integration tests for Campaign 4 Lane HAA: Haagerup H6 Box Cover and Reflection Artifact.
//!
//! # Firewall & Rules
//! * NOT MUB(6)=3 and NOT MUB(6)<=3.
//! * AuthorityEffect: None.
//! * Exact rational / cyclotomic arithmetic over Q(ζ₂₄) with Cyc24.
//! * Zero floating-point certifiers.

use num_rational::BigRational;
use num_traits::Zero;
use std::path::PathBuf;

use omega_mub::omega_native::exact::d6_exact_curvature_cochain::{abs_sq, D};
use omega_mub::omega_native::campaign::mub6_dita_seed_cover::narrow_torus_cell;
use omega_mub::omega_native::exact::mub6_haagerup_cover::{
    cover_haagerup_narrow_cell, generate_haagerup_scaled_box_complex, haagerup_cover_status,
    haagerup_h6_basepoint_point0, haagerup_h6_basepoint_point3, haagerup_h6_columns,
    haagerup_h6_is_exact_chm, haagerup_seed_enclosed, haagerup_seed_neighborhood_enclosed,
    haagerup_seed_smoke_vector_gap, haagerup_seed_triple_bases_are_chm,
    haagerup_seed_triple_columns, neighborhood_delta_1_1000, write_haagerup_reflection_artifact,
    ScaledBoxComplexArtifact,
};
use omega_mub::omega_native::exact::szollosi_triad_solver::verify_chm;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

#[test]
fn test_haagerup_h6_basepoints_are_exact_chm() {
    // Point 0: (b, c, e, f) = (1, i, 1, -1)
    let p0 = haagerup_h6_basepoint_point0();
    let rep0 = verify_chm(&p0);
    assert!(rep0.is_chm, "Haagerup Point 0 must be an exact CHM");
    assert!(
        rep0.all_entries_unit_modulus,
        "Point 0 must have unit modulus entries"
    );
    assert!(rep0.is_orthogonal, "Point 0 must satisfy M M† = 6 I_6");

    // Point 3: (b, c, e, f) = (1, ω, 1, ω²)
    let p3 = haagerup_h6_basepoint_point3();
    let rep3 = verify_chm(&p3);
    assert!(rep3.is_chm, "Haagerup Point 3 must be an exact CHM");
    assert!(
        rep3.all_entries_unit_modulus,
        "Point 3 must have unit modulus entries"
    );
    assert!(rep3.is_orthogonal, "Point 3 must satisfy M M† = 6 I_6");

    // General oracle check on H6 basepoint
    assert!(
        haagerup_h6_is_exact_chm(),
        "H6 basepoint must pass exact oracle"
    );
}

#[test]
fn test_haagerup_columns_normalization_and_unbiasedness() {
    let cols = haagerup_h6_columns();
    assert_eq!(cols.len(), D, "Must have 6 columns");

    let one_sixth = Cyc24::rat(ri(1) / ri(6));
    // Each entry squared modulus must be 1/6 (unbiased to standard basis)
    for (c_idx, col) in cols.iter().enumerate() {
        for (r_idx, entry) in col.iter().enumerate() {
            assert_eq!(
                abs_sq(entry),
                one_sixth,
                "Column {c_idx} entry {r_idx} must have modulus squared 1/6"
            );
        }
    }
}

#[test]
fn test_haagerup_seed_triple_chm_and_status() {
    let cols = haagerup_seed_triple_columns();
    assert_eq!(cols.len(), 18, "Triple must assemble exactly 18 columns");

    assert!(
        haagerup_seed_triple_bases_are_chm(),
        "All three bases in triple (I6, F6, H6) must be exact CHMs"
    );

    let status = haagerup_cover_status();
    assert!(status.is_exact_chm);
    assert!(status.triple_is_pairwise_chm);
    assert_eq!(status.column_count, 18);
    assert!(
        status.smoke_vector_excluded,
        "Smoke vector must be excluded"
    );
    assert_ne!(status.smoke_vector_gap, "0");

    let vgap = haagerup_seed_smoke_vector_gap();
    assert!(
        vgap > BigRational::zero(),
        "Smoke vector gap must be strictly positive"
    );
}

#[test]
fn test_haagerup_narrow_cell_cover() {
    let cert = cover_haagerup_narrow_cell();
    assert!(cert.complete, "Narrow cell cover must be complete");
    assert_eq!(cert.uncertified, 0, "Zero uncertified boxes on narrow cell");
    assert!(cert.certified > 0, "Must certify at least one box");
    assert!(cert.min_gap.is_some(), "Must report a minimum gap");
    let min_gap_str = cert.min_gap.as_ref().unwrap();
    assert!(!min_gap_str.is_empty(), "Min gap string must not be empty");
    println!(
        "Narrow cell certified: {} boxes, off_torus: {}, min_gap: {}",
        cert.certified, cert.off_torus, min_gap_str
    );
}

#[test]
fn test_haagerup_scaled_box_complex_64_boxes() {
    let artifact = generate_haagerup_scaled_box_complex(6);
    assert_eq!(
        artifact.complex.box_count, 64,
        "Must partition into 64 contiguous boxes"
    );
    assert_eq!(
        artifact.complex.certified, 64,
        "All 64 boxes must be certified"
    );
    assert_eq!(artifact.complex.uncertified, 0, "Zero uncertified boxes");
    assert!(artifact.complex.complete, "Complex must be complete");
    assert_eq!(
        artifact.boxes.len(),
        64,
        "Records must contain 64 box entries"
    );

    // Verify all box gaps are strictly positive in exact rational arithmetic
    for box_rec in &artifact.boxes {
        let num: num_bigint::BigInt = box_rec.num.parse().expect("valid integer numerator");
        let den: num_bigint::BigInt = box_rec.den.parse().expect("valid integer denominator");
        assert!(
            num > num_bigint::BigInt::from(0),
            "Box {} numerator must be positive",
            box_rec.index
        );
        assert!(
            den > num_bigint::BigInt::from(0),
            "Box {} denominator must be positive",
            box_rec.index
        );
    }
}

#[test]
fn test_haagerup_reflection_artifact_written_and_verified() {
    let dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/omega_mub/artifacts");
    if !dir.exists() {
        std::fs::create_dir_all(&dir).expect("artifacts dir create");
    }
    let target_path = dir.join("kernel_reflection_haagerup_h6_box_cover.json");
    write_haagerup_reflection_artifact(&target_path)
        .expect("write kernel_reflection_haagerup_h6_box_cover.json");

    assert!(target_path.exists(), "Artifact file must exist on disk");

    let content = std::fs::read_to_string(&target_path).expect("read artifact");
    let loaded: ScaledBoxComplexArtifact =
        serde_json::from_str(&content).expect("parse reflection artifact");

    assert_eq!(
        loaded.schema_version,
        "omega.mub.kernel-reflection-scaled.v1"
    );
    assert_eq!(loaded.seed, vec![0, 6, 0, 12]);
    assert_eq!(loaded.complex.box_count, 64);
    assert_eq!(loaded.complex.certified, 64);
    assert_eq!(loaded.complex.uncertified, 0);
    assert!(loaded.complex.complete);
    assert_eq!(loaded.boxes.len(), 64);
    println!(
        "Successfully verified written artifact: {}",
        target_path.display()
    );
    println!("Global min_gap: {}", loaded.complex.min_gap);
}

#[test]
fn test_haagerup_neighborhood_enclosure_widening() {
    let delta = neighborhood_delta_1_1000();
    let (exact_w, _) = haagerup_seed_neighborhood_enclosed(&delta);
    let (exact_p, _) = haagerup_seed_enclosed();
    let cell = narrow_torus_cell();
    let gap_w = exact_w.residual_sq_lower(&cell);
    let gap_p = exact_p.residual_sq_lower(&cell);
    assert!(
        gap_w > BigRational::zero(),
        "Widened lower bound must be strictly positive"
    );
    assert!(
        gap_w <= gap_p,
        "Widened lower bound must be <= point lower bound (soundness)"
    );
}
