//! Finite determinant, involution, and matrix-algebra examples.
//!
//! AuthorityEffect: None. GenesisEffect: None.

use num_rational::Rational64;
use std::collections::BTreeMap;

use mssn_stage_024::exact_linear_algebra::GaussianRational;
use mssn_stage_024::finite_algebra::{
    bareiss_determinant,
    verify_bqnf_involution_pairing, GaussianMatrix, SignedPathConfiguration,
};

#[test]
fn test_bareiss_fraction_free_determinant_exact_integers() {
    // 2x2 test: [[2, 1], [3, 4]] -> det = 2*4 - 3*1 = 5
    let m2 = vec![vec![2, 1], vec![3, 4]];
    assert_eq!(bareiss_determinant(&m2).unwrap(), 5);

    // 3x3 test:
    // [[1, 2, 3],
    //  [2, 5, 7],
    //  [3, 7, 12]] -> det = 2
    let m3 = vec![vec![1, 2, 3], vec![2, 5, 7], vec![3, 7, 12]];
    assert_eq!(bareiss_determinant(&m3).unwrap(), 2);

    // 3x3 with zero pivot requiring row swap:
    // [[0, 1, 2],
    //  [1, 0, 3],
    //  [4, -3, 8]] -> det = 0 - 1*(8 - 12) + 2*(-3) = 4 - 6 = -2
    let m3_swap = vec![vec![0, 1, 2], vec![1, 0, 3], vec![4, -3, 8]];
    assert_eq!(bareiss_determinant(&m3_swap).unwrap(), -2);

    // Singular matrix: det = 0
    let m3_sing = vec![vec![1, 2, 3], vec![2, 4, 6], vec![1, 1, 1]];
    assert_eq!(bareiss_determinant(&m3_sing).unwrap(), 0);

    // 4x4 matrix
    let m4 = vec![
        vec![2, 0, 1, 3],
        vec![0, 1, 4, 1],
        vec![1, 2, 0, 2],
        vec![3, 1, 2, 1],
    ];
    // det(m4) computed via expansion
    let det4 = bareiss_determinant(&m4).unwrap();
    assert_eq!(det4, 66);
}



#[test]
fn test_bqnf_involution_sign_pairing_cancellation() {
    // Ensemble of 4 configurations: 2 positive, 2 negative, paired by action
    let configs = vec![
        SignedPathConfiguration {
            config_id: 1,
            action: Rational64::new(5, 2),
            fermion_sign: 1,
            mode_postings: vec!["KZ_PLUS".to_string()],
        },
        SignedPathConfiguration {
            config_id: 2,
            action: Rational64::new(5, 2),
            fermion_sign: -1,
            mode_postings: vec!["KZ_MINUS".to_string()],
        },
        SignedPathConfiguration {
            config_id: 3,
            action: Rational64::new(11, 4),
            fermion_sign: 1,
            mode_postings: vec!["ARC_TOP".to_string()],
        },
        SignedPathConfiguration {
            config_id: 4,
            action: Rational64::new(11, 4),
            fermion_sign: -1,
            mode_postings: vec!["ARC_BOTTOM".to_string()],
        },
    ];

    // Involution: 1 <-> 2, 3 <-> 4
    let mut involution = BTreeMap::new();
    involution.insert(1, 2);
    involution.insert(2, 1);
    involution.insert(3, 4);
    involution.insert(4, 3);

    let receipt = verify_bqnf_involution_pairing(&configs, &involution).unwrap();
    assert_eq!(receipt.total_configurations, 4);
    assert_eq!(receipt.paired_count, 4);
    assert_eq!(receipt.net_fermion_sign, 0);
    assert!(receipt.cancellation_certified);
    assert_eq!(receipt.average_sign, Rational64::new(0, 1));

    // Failure case: action mismatch between paired configs
    let broken_configs = vec![
        SignedPathConfiguration {
            config_id: 1,
            action: Rational64::new(5, 2),
            fermion_sign: 1,
            mode_postings: vec![],
        },
        SignedPathConfiguration {
            config_id: 2,
            action: Rational64::new(9, 2), // Mismatched action!
            fermion_sign: -1,
            mode_postings: vec![],
        },
    ];
    let mut broken_inv = BTreeMap::new();
    broken_inv.insert(1, 2);
    broken_inv.insert(2, 1);
    assert!(verify_bqnf_involution_pairing(&broken_configs, &broken_inv).is_err());
}

#[test]
fn test_discrete_matrix_commutator_and_jacobi_identity() {
    // 2x2 Pauli matrices:
    // sigma_x = [[0, 1], [1, 0]]
    // sigma_y = [[0, -i], [i, 0]]
    // sigma_z = [[1, 0], [0, -1]]
    let sx = GaussianMatrix::new(
        2,
        vec![
            vec![GaussianRational::zero(), GaussianRational::one()],
            vec![GaussianRational::one(), GaussianRational::zero()],
        ],
    );

    let sy = GaussianMatrix::new(
        2,
        vec![
            vec![
                GaussianRational::zero(),
                GaussianRational::new(Rational64::new(0, 1), Rational64::new(-1, 1)),
            ],
            vec![
                GaussianRational::new(Rational64::new(0, 1), Rational64::new(1, 1)),
                GaussianRational::zero(),
            ],
        ],
    );

    let sz = GaussianMatrix::new(
        2,
        vec![
            vec![GaussianRational::one(), GaussianRational::zero()],
            vec![
                GaussianRational::zero(),
                GaussianRational::new(Rational64::new(-1, 1), Rational64::new(0, 1)),
            ],
        ],
    );

    // [sigma_x, sigma_y] = 2i * sigma_z
    let comm_xy = sx.commutator(&sy);
    let expected_comm = GaussianMatrix::new(
        2,
        vec![
            vec![
                GaussianRational::new(Rational64::new(0, 1), Rational64::new(2, 1)),
                GaussianRational::zero(),
            ],
            vec![
                GaussianRational::zero(),
                GaussianRational::new(Rational64::new(0, 1), Rational64::new(-2, 1)),
            ],
        ],
    );
    assert_eq!(comm_xy, expected_comm);

    // Jacobi identity: [sigma_x, [sigma_y, sigma_z]] + [sigma_y, [sigma_z, sigma_x]] + [sigma_z, [sigma_x, sigma_y]] = 0
    let jacobi = sx.jacobi_sum(&sy, &sz);
    assert!(jacobi.is_zero());
}



#[test]
fn test_trace_so3_and_nonnegative_commutator_norm() {
    // 1. Trace of Commutator is Zero: Tr([A, B]) = 0 for general Gaussian matrices
    let a = GaussianMatrix::new(
        2,
        vec![
            vec![
                GaussianRational::new(Rational64::new(3, 2), Rational64::new(1, 4)),
                GaussianRational::new(Rational64::new(-5, 3), Rational64::new(2, 7)),
            ],
            vec![
                GaussianRational::new(Rational64::new(7, 5), Rational64::new(-3, 2)),
                GaussianRational::new(Rational64::new(1, 6), Rational64::new(4, 9)),
            ],
        ],
    );
    let b = GaussianMatrix::new(
        2,
        vec![
            vec![
                GaussianRational::new(Rational64::new(-2, 3), Rational64::new(5, 8)),
                GaussianRational::new(Rational64::new(4, 1), Rational64::new(-1, 3)),
            ],
            vec![
                GaussianRational::new(Rational64::new(3, 4), Rational64::new(0, 1)),
                GaussianRational::new(Rational64::new(2, 5), Rational64::new(-7, 4)),
            ],
        ],
    );

    let comm_ab = a.commutator(&b);
    assert!(!comm_ab.is_zero(), "A and B should not commute");
    assert!(
        comm_ab.trace().is_zero(),
        "Trace of commutator Tr([A, B]) must be identically zero"
    );

    // 2. Heisenberg Trace Obstruction: [X, Y] = c * I is algebraically obstructed for c != 0
    // Because Tr([X, Y]) = 0 while Tr(c * I_N) = N * c != 0
    let c_scalar = GaussianRational::new(Rational64::new(1, 1), Rational64::new(0, 1));
    let mut c_identity = GaussianMatrix::identity(2);
    for r in 0..2 {
        c_identity.data[r][r] = c_scalar.clone();
    }
    assert_eq!(
        c_identity.trace(),
        GaussianRational::new(Rational64::new(2, 1), Rational64::new(0, 1))
    );
    assert!(
        !c_identity.trace().is_zero(),
        "c * I_N has non-zero trace 2*c != 0, obstructing Heisenberg commutation relation"
    );

    // 3. Three real skew-symmetric so(3) generators:
    // J1 = [[0, 0, 0], [0, 0, -1], [0, 1, 0]]
    // J2 = [[0, 0, 1], [0, 0, 0], [-1, 0, 0]]
    // J3 = [[0, -1, 0], [1, 0, 0], [0, 0, 0]]
    let z = || GaussianRational::zero();
    let one = || GaussianRational::one();
    let neg_one = || GaussianRational::new(Rational64::new(-1, 1), Rational64::new(0, 1));

    let j1 = GaussianMatrix::new(
        3,
        vec![
            vec![z(), z(), z()],
            vec![z(), z(), neg_one()],
            vec![z(), one(), z()],
        ],
    );
    let j2 = GaussianMatrix::new(
        3,
        vec![
            vec![z(), z(), one()],
            vec![z(), z(), z()],
            vec![neg_one(), z(), z()],
        ],
    );
    let j3 = GaussianMatrix::new(
        3,
        vec![
            vec![z(), neg_one(), z()],
            vec![one(), z(), z()],
            vec![z(), z(), z()],
        ],
    );

    // Verify Lie algebra commutators: [J_i, J_j] = epsilon_{ijk} J_k
    let comm_12 = j1.commutator(&j2);
    assert_eq!(comm_12, j3, "[J1, J2] == J3");

    let comm_23 = j2.commutator(&j3);
    assert_eq!(comm_23, j1, "[J2, J3] == J1");

    let comm_31 = j3.commutator(&j1);
    assert_eq!(comm_31, j2, "[J3, J1] == J2");

    // All generators and commutators have identically zero trace
    assert!(j1.trace().is_zero());
    assert!(j2.trace().is_zero());
    assert!(j3.trace().is_zero());
    assert!(comm_12.trace().is_zero());
    assert!(comm_23.trace().is_zero());
    assert!(comm_31.trace().is_zero());

    // Verify Jacobi identity on so(3) generators
    assert!(j1.jacobi_sum(&j2, &j3).is_zero());

    // 4. Declared commutator-norm quantity: S_YM = (1/4) * sum_{i < j} Tr([X^i, X^j]^\dagger [X^i, X^j])
    // These three generators: S_YM = (1/4) * (2 + 2 + 2) = 6/4 = 3/2 > 0
    let ym_action_fuzzy = GaussianMatrix::quarter_commutator_norm_sum(&[j1, j2, j3]);
    assert_eq!(ym_action_fuzzy, Rational64::new(3, 2));
    assert!(ym_action_fuzzy > Rational64::new(0, 1));

    // Commuting identity matrices: S_YM = 0
    let id3 = GaussianMatrix::identity(3);
    let ym_action_vacuum = GaussianMatrix::quarter_commutator_norm_sum(&[id3.clone(), id3]);
    assert_eq!(ym_action_vacuum, Rational64::new(0, 1));
}
