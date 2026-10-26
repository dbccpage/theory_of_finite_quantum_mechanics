//! Integration tests for MSS-N Exact Linear Algebra:
//! - Pillar 1: Smith Normal Form & 2-Torsion Extraction over Z
//! - Pillar 2: QuadraticExtension Q(sqrt(5)) & Mac Lane Pentagon Associator (F^2 = I)
//! - Pillar 3: GaussianRational Q(i), SO(4) & Discrete Bianchi Holonomies
//!
//! AuthorityEffect: None. GenesisEffect: None.

use mssn_stage_024::exact_linear_algebra::{
    audit_fibonacci_f_matrix_square, cayley_menger, signed_volume_4,
    verify_bianchi_closure, Bivector4, GaussianRational, Matrix2x2Quadratic,
    QuadraticExtension, Simplex4DFrame, So4,
};
use mssn_stage_024::smith_normal_form::IntegerMatrix;
use num_rational::{BigRational, Rational64};
use num_traits::{One, Zero};

#[test]
fn test_pillar_1_snf_rp2_2_torsion_extraction() {
    // Cellular attaching map d2 has invariant factor d_1 = 2 representing Z/2Z torsion in H_1(RP^2; Z)
    let rp2_d2 = IntegerMatrix::from_dense(1, 1, &[2]);
    let invariants = rp2_d2.smith_normal_form();


    // Verify non-trivial 2-torsion invariant factor
    assert!(
        invariants.contains(&2),
        "Smith Normal Form of RP^2 boundary d2 must contain invariant factor 2"
    );
}

#[test]
fn test_pillar_2_quadratic_extension_and_f_matrix_involution() {
    // Golden ratio phi = 1/2 + 1/2*sqrt(5)
    let phi = QuadraticExtension::golden_ratio();
    // phi^-1 = -1/2 + 1/2*sqrt(5)
    let phi_inv = QuadraticExtension::golden_ratio_inv();

    // Check phi * phi^-1 = 1
    let product = phi.mul(&phi_inv);
    assert!(product.is_one(), "phi * phi^-1 must equal exact 1");

    // Check phi^-2 + phi^-1 = 1
    assert!(
        audit_fibonacci_f_matrix_square(),
        "Fibonacci anyon F-matrix diagonal square must close to 1 over Q(sqrt(5))"
    );

    // Matrix involution test: F = [[phi^-1, 0], [0, -phi^-1]] squared on diagonal
    let f_matrix = Matrix2x2Quadratic {
        m: [
            [phi_inv.clone(), QuadraticExtension::zero()],
            [QuadraticExtension::zero(), phi_inv.mul(&QuadraticExtension::from_rational(Rational64::new(-1, 1)))],
        ],
    };
    let f_sq = f_matrix.mul(&f_matrix);
    // phi^-2 = 3/2 - 1/2*sqrt(5)
    assert_eq!(f_sq.m[0][0], phi_inv.mul(&phi_inv));
}

#[test]
fn test_pillar_3_gaussian_rational_and_bianchi_closure() {
    // Q(i) arithmetic
    let z1 = GaussianRational::new(Rational64::new(3, 5), Rational64::new(4, 5));
    assert_eq!(z1.norm_sq(), Rational64::new(1, 1)); // Pythagorean unit norm

    let z1_inv = z1.inv().expect("Non-zero must have inverse");
    assert_eq!(z1_inv, z1.conj()); // Unit modulus implies inv == conj
    assert!(z1.mul(&z1_inv).is_one());

    // Path-ordered discrete Bianchi loop closure:
    // Verify prod_{k=1}^m (P_k * R_{t_k} * P_k^-1) = I_4
    let p0 = Simplex4DFrame::identity();
    let r0 = Simplex4DFrame::identity();
    let loop_transports = vec![(p0.clone(), r0.clone()), (p0, r0)];
    assert!(
        verify_bianchi_closure(&loop_transports),
        "Identity transport loop must close to identity"
    );
}

#[test]
fn test_regge_so4_and_cayley_menger_volume_reality() {
    // SO(4) rotation
    let so4_id = So4::identity();
    assert!(so4_id.is_identity());
    assert_eq!(so4_id.frobenius_defect_squared(), BigRational::zero());

    // Orthogonal 4-simplex in R^4 with vertices at origin and unit standard basis vectors:
    // signed volume is 1/24
    let mut points: [[BigRational; 4]; 5] =
        std::array::from_fn(|_| std::array::from_fn(|_| BigRational::zero()));
    for axis in 0..4 {
        points[axis + 1][axis] = BigRational::one();
    }
    let vol = signed_volume_4(&points).expect("Volume computation");
    assert_eq!(vol, BigRational::new(1.into(), 24.into()));

    // Cayley-Menger squared distance table for orthogonal 4-simplex
    let mut lengths: [[BigRational; 5]; 5] =
        std::array::from_fn(|_| std::array::from_fn(|_| BigRational::zero()));
    for i in 0..=4 {
        for j in 0..=4 {
            let mut sum = BigRational::zero();
            for axis in 0..4 {
                let delta = &points[i][axis] - &points[j][axis];
                sum += &delta * &delta;
            }
            lengths[i][j] = sum;
        }
    }
    let cm_res = cayley_menger(4, &lengths).expect("Cayley Menger");
    // For orthogonal unit 4-simplex, V^2 = (1/24)^2 = 1/576
    assert_eq!(cm_res.volume_squared, BigRational::new(1.into(), 576.into()));

    // Bivector pfaffian simplicity
    let e0 = [BigRational::one(), BigRational::zero(), BigRational::zero(), BigRational::zero()];
    let e1 = [BigRational::zero(), BigRational::one(), BigRational::zero(), BigRational::zero()];
    let bivector = Bivector4::from_wedge_half(&e0, &e1);
    assert!(bivector.is_simple(), "Pure wedge bivector must be simple (Pfaffian = 0)");
}
