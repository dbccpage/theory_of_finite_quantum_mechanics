use num_rational::BigRational;
use num_traits::{One, Zero};

use omega_mub::omega_native::exact::mub6_frame_potential::{
    canonical_candidate_bases, compute_all_blocks, compute_total_frame_potential,
    etf_mub_coherence_defect, etf_welch_coherence_sq, ideal_mub_frame_potential,
    inner_product_mod_sq, mub_coherence_sq, non_unitary_povm_intra_penalty,
    solve_frame_potential_certificate, vector_norm_sq, welch_bound_2, DIM_HILBERT, NUM_BASES_4,
};

#[test]
fn test_ideal_mub_frame_potential_formula() {
    let d = 6;
    // FP_2(k-MUB) = k(d + k - 1)
    let expected = [
        (1, 6),  // 1 * (6 + 0) = 6
        (2, 14), // 2 * (6 + 1) = 14
        (3, 24), // 3 * (6 + 2) = 24
        (4, 36), // 4 * (6 + 3) = 36
        (5, 50), // 5 * (6 + 4) = 50
        (6, 66), // 6 * (6 + 5) = 66
        (7, 84), // 7 * (6 + 6) = 84
    ];

    for (k, val) in expected {
        let fp = ideal_mub_frame_potential(d, k);
        assert_eq!(
            fp,
            BigRational::from_integer((val as i64).into()),
            "failed for k = {}",
            k
        );
    }
}

#[test]
fn test_2nd_welch_bound() {
    let d = 6;
    let m = 24;
    let wb = welch_bound_2(d, m);
    // 2 * 24^2 / (6 * 7) = 1152 / 42 = 192 / 7
    assert_eq!(wb, BigRational::new(192.into(), 7.into()));
}

#[test]
fn test_candidate_bases_normalization_and_orthonormality() {
    let bases = canonical_candidate_bases();
    assert_eq!(bases.len(), NUM_BASES_4);

    for (b_idx, basis) in bases.iter().enumerate() {
        assert_eq!(basis.len(), DIM_HILBERT);
        for (i, u) in basis.iter().enumerate() {
            let n2 = vector_norm_sq(u);
            assert_eq!(
                n2,
                BigRational::one(),
                "vector {} in basis {} is not normalized",
                i,
                b_idx
            );

            for (j, v) in basis.iter().enumerate() {
                let ip_sq = inner_product_mod_sq(u, v);
                if i == j {
                    assert_eq!(
                        ip_sq,
                        BigRational::one(),
                        "diagonal norm error in basis {}",
                        b_idx
                    );
                } else {
                    assert!(
                        ip_sq.is_zero(),
                        "orthogonality failed for basis {} between cols {} and {}",
                        b_idx,
                        i,
                        j
                    );
                }
            }
        }
    }
}

#[test]
fn test_candidate_blocks_values() {
    let bases = canonical_candidate_bases();
    let blocks = compute_all_blocks(&bases);

    // Diagonals must all be 6
    for i in 0..NUM_BASES_4 {
        assert_eq!(blocks[i][i], BigRational::from_integer(6.into()));
    }

    // Basis 0 (I_6) is mutually unbiased to all others (block sum = 1)
    assert_eq!(blocks[0][1], BigRational::one());
    assert_eq!(blocks[1][0], BigRational::one());
    assert_eq!(blocks[0][2], BigRational::one());
    assert_eq!(blocks[2][0], BigRational::one());
    assert_eq!(blocks[0][3], BigRational::one());
    assert_eq!(blocks[3][0], BigRational::one());

    // Basis 1 (F_6) vs Basis 2 (F_6^{(2)}): sum = 2
    assert_eq!(blocks[1][2], BigRational::from_integer(2.into()));
    assert_eq!(blocks[2][1], BigRational::from_integer(2.into()));

    // Basis 1 (F_6) vs Basis 3 (S_6): sum = 7/2
    assert_eq!(blocks[1][3], BigRational::new(7.into(), 2.into()));
    assert_eq!(blocks[3][1], BigRational::new(7.into(), 2.into()));

    // Basis 2 (F_6^{(2)}) vs Basis 3 (S_6): sum = 2
    assert_eq!(blocks[2][3], BigRational::from_integer(2.into()));
    assert_eq!(blocks[3][2], BigRational::from_integer(2.into()));
}

#[test]
fn test_total_frame_potential_and_defect() {
    let bases = canonical_candidate_bases();
    let total_fp = compute_total_frame_potential(&bases);
    assert_eq!(total_fp, BigRational::from_integer(45.into()));

    let ideal_fp = ideal_mub_frame_potential(DIM_HILBERT, NUM_BASES_4);
    assert_eq!(ideal_fp, BigRational::from_integer(36.into()));

    let defect = &total_fp - &ideal_fp;
    assert_eq!(defect, BigRational::from_integer(9.into()));
    assert!(defect > BigRational::zero());
}

#[test]
fn test_etf_welch_coherence_defect() {
    let d = 6;
    let m = 24;
    let etf_c2 = etf_welch_coherence_sq(d, m);
    // (24 - 6) / (6 * 23) = 18 / 138 = 3 / 23
    assert_eq!(etf_c2, BigRational::new(3.into(), 23.into()));

    let mub_c2 = mub_coherence_sq(d);
    assert_eq!(mub_c2, BigRational::new(1.into(), 6.into()));

    let defect = etf_mub_coherence_defect(d, m);
    // |3/23 - 1/6| = |18/138 - 23/138| = 5/138
    assert_eq!(defect, BigRational::new(5.into(), 138.into()));
    assert!(defect > BigRational::zero());
}

#[test]
fn test_non_unitary_povm_deformation_penalty() {
    // For eta = 1/6 (hypothetical non-zero intra-basis overlap)
    let eta = BigRational::new(1.into(), 6.into());
    let penalty = non_unitary_povm_intra_penalty(eta);
    // 2 * (1/6)^2 = 2 / 36 = 1 / 18
    assert_eq!(penalty, BigRational::new(1.into(), 18.into()));
    assert!(penalty > BigRational::zero());

    // For any non-zero eta, penalty is strictly positive
    let tiny_eta = BigRational::new(1.into(), 1000.into());
    let tiny_penalty = non_unitary_povm_intra_penalty(tiny_eta);
    assert!(tiny_penalty > BigRational::zero());
}

#[test]
fn test_full_certificate_solve_and_verify() {
    let cert = solve_frame_potential_certificate();
    assert!(cert.verified_sound);
    assert_eq!(cert.dimension, 6);
    assert_eq!(cert.bases_count, 4);
    assert_eq!(cert.total_vectors, 24);
    assert_eq!(cert.ideal_frame_potential, "36");
    assert_eq!(cert.computed_frame_potential, "45");
    assert_eq!(cert.frame_potential_defect, "9");
    assert_eq!(cert.epsilon_frame, "9");
    assert!(cert.defect_strictly_positive);
    assert!(cert.welch_bound_satisfied);
    assert_eq!(cert.diagonal_blocks_sum, "24");
    assert_eq!(cert.off_diagonal_blocks_sum, "21");
    assert!(cert.vectors_normalized);
    assert_eq!(cert.bases_internal_orthonormality.len(), 4);
    assert!(cert.bases_internal_orthonormality.iter().all(|&b| b));
    assert_eq!(cert.non_unitary_povm_analysis.etf_coherence_sq, "3/23");
    assert_eq!(cert.non_unitary_povm_analysis.mub_coherence_sq, "1/6");
    assert_eq!(cert.non_unitary_povm_analysis.coherence_defect, "5/138");
    assert!(
        cert.non_unitary_povm_analysis
            .etf_mub_incompatibility_certified
    );
    assert!(
        cert.non_unitary_povm_analysis
            .example_eta_1_over_10_penalty_positive
    );
}

#[test]
fn receipt_replay_rejects_tampering_in_previously_unchecked_fields() {
    use omega_mub::omega_native::exact::mub6_frame_potential::verify_frame_potential_certificate;
    let original = solve_frame_potential_certificate();
    assert!(!original.mub_nonexistence_established);
    let mut forged = original.clone();
    forged.block_matrix[0][1] = "999".into();
    assert!(!verify_frame_potential_certificate(&forged));
    forged = original.clone();
    forged.welch_bound_t2 = "0".into();
    assert!(!verify_frame_potential_certificate(&forged));
    forged = original.clone();
    forged.schema_version = "forged".into();
    assert!(!verify_frame_potential_certificate(&forged));
    forged = original;
    forged.mub_nonexistence_established = true;
    assert!(!verify_frame_potential_certificate(&forged));
}
