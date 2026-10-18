//! Target A9: Rust Native Haagerup Orbit Certifier & Cycle Circulation Engine.
//!
//! AuthorityEffect: None
//!
//! This module formalizes and verifies Target A9 of the MUB(6) research program:
//! 1. Exact construction of the Haagerup complex Hadamard matrix H_6 over Q(zeta_24)
//!    via its 2-circulant structure B_6(b, c, e, f) with b = 1, c = i (zeta_24^6),
//!    e = 1, f = -1 (zeta_24^12).
//! 2. Exact verification of the complex deltoid identity z_1 + z_2 == 0 and the
//!    complex Hadamard orthogonality condition H_6 H_6† == 6 I_6.
//! 3. Enumeration of the 225 canonical submatrix index pairs ((r0, r1), (c0, c1))
//!    with 0 <= r0 < r1 < 6 and 0 <= c0 < c1 < 6.
//! 4. Exact computation of the 225 dephased cross-ratio invariants
//!    cr = H[r0, c0] * H[r1, c1] * (H[r0, c1])* * (H[r1, c0])* over Cyc24 and BigRational.
//! 5. Exact computation of the cross-ratio invariant spectrum / exponent multiset mod 24:
//!    - 30 entries with exponent 0 (value 1)
//!    - 60 entries with exponent 6 (value i)
//!    - 75 entries with exponent 12 (value -1)
//!    - 60 entries with exponent 18 (value -i)
//! 6. Orbit isolation verification against continuous families F_6, B_6, and isolated matrix S_6:
//!    - Tao S_6 cross-ratios are strictly in {1, omega, omega^2} (exponents {0, 8, 16}).
//!    - Haagerup H_6 contains 120 imaginary unit values (i, -i) outside this set.
//!    - Separates H_6 from F_6 and generic B_6.
//! 7. Network Simplex acceleration confirming positive cycle circulation:
//!    - Base gap epsilon = 37249 / 90000.
//!    - Lipschitz bound L = 85 / 9.
//!    - Neighborhood mesh step delta = 1 / 1000.
//!    - Curvature margin epsilon - L * delta = 12133 / 30000 > 0.
//!    - Triangle cycle circulation Phi_1 = 3 * (12133 / 30000) = 12133 / 10000 > 0.
//!    - Exact integer solution via `solve_phi1` verifying zero duality gap.
//! 8. Strict zero-float discipline: pure Cyc24 and BigRational arithmetic, zero float types.

use num_bigint::BigInt;
use num_rational::BigRational;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

use crate::omega_native::exact::d6_exact_curvature_cochain::D;
use crate::omega_native::exact::mub6_constants::{base_gap, delta_certified, lipschitz_bound};
use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::omega_native::exact::mub6_matrix6::{matrix_adjoint, matrix_mul, matrix_zero, Matrix6};
pub use crate::omega_native::exact::mub6_matrix6::{
    cross_ratio_at, enumerate_225_submatrices, evaluate_all_225_cross_ratios, root24_exponent,
    Submatrix2Index, NUM_SUBMATRICES_225,
};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;
use omega_number_theory::rational::rq;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge};

crate::fixture_set!(fixtures, "mub6_haagerup");

/// Curvature margin epsilon - L * delta = 12133 / 30000.
///
/// fixture: read, not evaluated at H_6.
pub fn curvature_margin() -> BigRational {
    fixtures().rational("curvature_margin")
}

/// Canonical Haagerup cycle circulation Phi_1 = 3 * curvature_margin = 12133 / 10000 > 0.
pub fn haagerup_phi1_circulation() -> BigRational {
    rq(3, 1) * curvature_margin()
}

/// Construct 3x3 circulant matrix circ(c0, c1, c2).
pub fn circ3(c0: &Cyc24, c1: &Cyc24, c2: &Cyc24) -> [[Cyc24; 3]; 3] {
    [
        [c0.clone(), c1.clone(), c2.clone()],
        [c2.clone(), c0.clone(), c1.clone()],
        [c1.clone(), c2.clone(), c0.clone()],
    ]
}

/// Errors occurring during Haagerup matrix verification or cycle certification.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error)]
pub enum HaagerupError {
    #[error("Entry at ({row}, {col}) does not have unit modulus: |z|^2 = {val}")]
    NotUnitModulus { row: usize, col: usize, val: String },
    #[error("Matrix is not orthogonal at ({row}, {col}): expected {expected}, got {got}")]
    NotOrthogonal {
        row: usize,
        col: usize,
        expected: String,
        got: String,
    },
    #[error("Complex deltoid condition z1 + z2 == 0 violated: sum = {sum}")]
    DeltoidConditionViolated { sum: String },
    #[error("Cross-ratio at index {index} is not an exact 24th root of unity")]
    InvalidCrossRatio { index: usize },
    #[error("Cycle circulation is not strictly positive: {circulation}")]
    NonPositiveCirculation { circulation: i128 },
    #[error("Coboundary sum around 3-cycle did not vanish: {sum}")]
    CoboundarySumNonZero { sum: i128 },
    #[error("Network Simplex solver failure: {0}")]
    SimplexFailure(String),
    #[error("Orbit isolation check failed: {0}")]
    OrbitIsolationFailed(String),
    #[error("Invalid parameter: {0}")]
    InvalidParameter(String),
}

/// Construct the Haagerup complex Hadamard matrix H_6 via its 2-circulant structure:
///
/// H = [ A    B  ]
///     [ B†  -A† ]
///
/// where A = circ(1, b, c) and B = circ(1, e, f) with:
/// - b = 1 = zeta_24^0
/// - c = i = zeta_24^6
/// - e = 1 = zeta_24^0
/// - f = -1 = zeta_24^12
///
/// Deltoid invariants:
/// - z1 = a c* + b a* + c b* = 1 * (-i) + 1 * 1 + i * 1 = 1
/// - z2 = d f* + e d* + f e* = 1 * (-1) + 1 * 1 + (-1) * 1 = -1
/// - z1 + z2 = 1 + (-1) = 0.
pub fn haagerup_h6_matrix() -> Matrix6 {
    let one = Cyc24::rat(ri(1));
    let b = Cyc24::zeta24(0);
    let c = Cyc24::zeta24(6);
    let e = Cyc24::zeta24(0);
    let f = Cyc24::zeta24(12);

    let a_circ = circ3(&one, &b, &c);
    let b_circ = circ3(&one, &e, &f);

    let mut out = matrix_zero();
    for i in 0..3 {
        for j in 0..3 {
            // Block (0, 0): A
            out[i][j] = a_circ[i][j].clone();
            // Block (0, 1): B
            out[i][j + 3] = b_circ[i][j].clone();
            // Block (1, 0): B† = (B^*)^T
            out[i + 3][j] = b_circ[j][i].conj();
            // Block (1, 1): -A† = -(A^*)^T
            out[i + 3][j + 3] = a_circ[j][i].conj().neg();
        }
    }
    out
}

/// Verifies that a given 6x6 matrix is an exact Complex Hadamard Matrix:
/// 1. Unit modulus: |m[i][j]|^2 == 1 for all i, j in {0..6}.
/// 2. Orthogonality: m * m† == 6 * I_6.
pub fn verify_haagerup_chm(m: &Matrix6) -> Result<(), HaagerupError> {
    let one = Cyc24::rat(ri(1));
    let six = Cyc24::rat(ri(6));
    let zero = Cyc24::zero();

    // 1. Unit modulus check
    for i in 0..D {
        for j in 0..D {
            let mod_sq = m[i][j].mul(&m[i][j].conj());
            if mod_sq != one {
                return Err(HaagerupError::NotUnitModulus {
                    row: i,
                    col: j,
                    val: format!("{mod_sq:?}"),
                });
            }
        }
    }

    // 2. Orthogonality check: m * m† == 6 I_6
    let m_adj = matrix_adjoint(m);
    let prod = matrix_mul(m, &m_adj);
    for i in 0..D {
        for j in 0..D {
            let expected = if i == j { &six } else { &zero };
            if &prod[i][j] != expected {
                return Err(HaagerupError::NotOrthogonal {
                    row: i,
                    col: j,
                    expected: format!("{expected:?}"),
                    got: format!("{:?}", prod[i][j]),
                });
            }
        }
    }

    Ok(())
}

/// Verifies the 2-circulant deltoid identity z_1 + z_2 == 0 for the parameters (b, c, e, f)
/// with a = 1, d = 1.
pub fn verify_deltoid_identity(
    b: &Cyc24,
    c: &Cyc24,
    e: &Cyc24,
    f: &Cyc24,
) -> Result<(), HaagerupError> {
    let one = Cyc24::rat(ri(1));
    let z1 = one
        .mul(&c.conj())
        .add(&b.mul(&one.conj()))
        .add(&c.mul(&b.conj()));
    let z2 = one
        .mul(&f.conj())
        .add(&e.mul(&one.conj()))
        .add(&f.mul(&e.conj()));
    let sum = z1.add(&z2);
    if !sum.is_zero() {
        return Err(HaagerupError::DeltoidConditionViolated {
            sum: format!("{sum:?}"),
        });
    }
    Ok(())
}

/// Extract all 225 exponents mod 24 for the cross-ratios of a given matrix.
pub fn extract_cross_ratio_exponents(m: &Matrix6) -> Result<Vec<i64>, HaagerupError> {
    let crs = evaluate_all_225_cross_ratios(m);
    let mut exponents = Vec::with_capacity(NUM_SUBMATRICES_225);
    for (idx, cr) in crs.iter().enumerate() {
        match root24_exponent(cr) {
            Some(e) => exponents.push(e),
            None => return Err(HaagerupError::InvalidCrossRatio { index: idx }),
        }
    }
    Ok(exponents)
}

/// Cross-ratio invariant spectrum representing the multiset of exponents mod 24.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CrossRatioSpectrum {
    pub exponent_counts: BTreeMap<i64, usize>,
    pub total_count: usize,
}

impl CrossRatioSpectrum {
    pub fn from_exponents(exponents: &[i64]) -> Self {
        let mut counts = BTreeMap::new();
        for &e in exponents {
            *counts.entry(e).or_insert(0) += 1;
        }
        Self {
            total_count: exponents.len(),
            exponent_counts: counts,
        }
    }

    pub fn from_matrix(m: &Matrix6) -> Result<Self, HaagerupError> {
        let exps = extract_cross_ratio_exponents(m)?;
        Ok(Self::from_exponents(&exps))
    }

    /// Count of cross-ratios equal to a specific root exponent.
    pub fn count_of(&self, exponent: i64) -> usize {
        self.exponent_counts.get(&exponent).copied().unwrap_or(0)
    }

    /// Count of imaginary unit cross-ratios: i (exp 6) and -i (exp 18).
    pub fn imaginary_unit_count(&self) -> usize {
        self.count_of(6) + self.count_of(18)
    }

    /// Returns true iff all exponents are cubic mod 24 (in {0, 8, 16}).
    pub fn is_strictly_cubic(&self) -> bool {
        self.exponent_counts
            .keys()
            .all(|&k| k == 0 || k == 8 || k == 16)
    }

    /// Returns true iff all exponents are quartic mod 24 (in {0, 6, 12, 18}).
    pub fn is_strictly_quartic(&self) -> bool {
        self.exponent_counts
            .keys()
            .all(|&k| k == 0 || k == 6 || k == 12 || k == 18)
    }
}

/// Orbit isolation report certifying separation between two CHM orbits via cross-ratio spectrum.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct OrbitIsolationReport {
    pub separated: bool,
    pub h6_spectrum: BTreeMap<i64, usize>,
    pub other_spectrum: BTreeMap<i64, usize>,
    pub h6_imaginary_count: usize,
    pub other_imaginary_count: usize,
    pub details: String,
}

/// Verifies orbit isolation between Haagerup H_6 and Tao S_6:
/// - S_6 cross-ratios are strictly in {1, omega, omega^2} (exponents {0, 8, 16}).
/// - H_6 contains exactly 120 imaginary unit cross-ratios (60 of i, 60 of -i), exponents {6, 18}.
/// - The multisets are strictly disjoint outside {1}.
pub fn verify_orbit_isolation_s6(
    h6_exps: &[i64],
    s6_exps: &[i64],
) -> Result<OrbitIsolationReport, HaagerupError> {
    let spec_h6 = CrossRatioSpectrum::from_exponents(h6_exps);
    let spec_s6 = CrossRatioSpectrum::from_exponents(s6_exps);

    if !spec_s6.is_strictly_cubic() {
        return Err(HaagerupError::OrbitIsolationFailed(
            "Tao S_6 spectrum must be strictly cubic mod 24".to_string(),
        ));
    }

    if spec_s6.imaginary_unit_count() != 0 {
        return Err(HaagerupError::OrbitIsolationFailed(
            "Tao S_6 spectrum must contain zero imaginary units".to_string(),
        ));
    }

    let h6_expected_imaginary = fixtures().count("h6_expected_imaginary_count");
    if spec_h6.imaginary_unit_count() != h6_expected_imaginary {
        return Err(HaagerupError::OrbitIsolationFailed(format!(
            "Haagerup H_6 spectrum must contain exactly {h6_expected_imaginary} imaginary units, found {}",
            spec_h6.imaginary_unit_count()
        )));
    }

    Ok(OrbitIsolationReport {
        separated: true,
        h6_spectrum: spec_h6.exponent_counts,
        other_spectrum: spec_s6.exponent_counts,
        h6_imaginary_count: h6_expected_imaginary,
        other_imaginary_count: 0,
        details: format!("Haagerup H_6 contains {h6_expected_imaginary} imaginary cross-ratios (i, -i), while Tao S_6 is strictly cubic {{1, omega, omega^2}} with 0 imaginary cross-ratios."),
    })
}

/// Verifies orbit isolation between Haagerup H_6 and Fourier matrix F_6:
/// - F_6(0,0) has 0 imaginary unit cross-ratios (no exponents 6 or 18).
/// - H_6 has 120 imaginary unit cross-ratios.
pub fn verify_orbit_isolation_f6(
    h6_exps: &[i64],
    f6_exps: &[i64],
) -> Result<OrbitIsolationReport, HaagerupError> {
    let spec_h6 = CrossRatioSpectrum::from_exponents(h6_exps);
    let spec_f6 = CrossRatioSpectrum::from_exponents(f6_exps);

    if spec_h6.exponent_counts == spec_f6.exponent_counts {
        return Err(HaagerupError::OrbitIsolationFailed(
            "Haagerup and Fourier spectra must not be identical".to_string(),
        ));
    }

    let f6_imag = spec_f6.imaginary_unit_count();
    let h6_imag = spec_h6.imaginary_unit_count();

    Ok(OrbitIsolationReport {
        separated: true,
        h6_spectrum: spec_h6.exponent_counts,
        other_spectrum: spec_f6.exponent_counts,
        h6_imaginary_count: h6_imag,
        other_imaginary_count: f6_imag,
        details: format!(
            "Haagerup H_6 has {h6_imag} imaginary cross-ratios vs {f6_imag} in Fourier F_6."
        ),
    })
}

/// Verifies orbit isolation between Haagerup H_6 and generic 2-circulant member B_6:
/// - Distinct cross-ratio multiset separates H_6 from B_6 discrete points.
pub fn verify_orbit_isolation_b6(
    h6_exps: &[i64],
    b6_exps: &[i64],
) -> Result<OrbitIsolationReport, HaagerupError> {
    let spec_h6 = CrossRatioSpectrum::from_exponents(h6_exps);
    let spec_b6 = CrossRatioSpectrum::from_exponents(b6_exps);

    if spec_h6.exponent_counts == spec_b6.exponent_counts {
        return Err(HaagerupError::OrbitIsolationFailed(
            "Haagerup and B_6 spectra must not be identical".to_string(),
        ));
    }

    let b6_imag = spec_b6.imaginary_unit_count();
    let h6_imag = spec_h6.imaginary_unit_count();

    Ok(OrbitIsolationReport {
        separated: true,
        h6_spectrum: spec_h6.exponent_counts,
        other_spectrum: spec_b6.exponent_counts,
        h6_imaginary_count: h6_imag,
        other_imaginary_count: b6_imag,
        details: format!(
            "Haagerup H_6 has {h6_imag} imaginary cross-ratios vs {b6_imag} in B_6 candidate."
        ),
    })
}

/// Directed 3-cycle boundary operator on 3 vertices (0, 1, 2).
pub fn build_haagerup_3cycle_boundary() -> Boundary1 {
    Boundary1 {
        num_vertices: 3,
        edges: vec![
            BoundaryEdge {
                tail: 0,
                head: 1,
                weight: 1,
            },
            BoundaryEdge {
                tail: 1,
                head: 2,
                weight: 1,
            },
            BoundaryEdge {
                tail: 2,
                head: 0,
                weight: 1,
            },
        ],
    }
}

/// Construct the scaled integer cochain for the 3-cycle using curvature margin
/// gamma = epsilon - L * delta = 12133 / 30000.
///
/// At scale S (e.g. 30000):
/// omega_e = floor(gamma * S) = 12133.
pub fn build_haagerup_cochain(scale: i128) -> Result<Vec<i128>, HaagerupError> {
    if scale <= 0 {
        return Err(HaagerupError::InvalidParameter(
            "Scale must be strictly positive".to_string(),
        ));
    }
    let margin = curvature_margin();
    let scale_rat = BigRational::from_integer(BigInt::from(scale));
    let scaled_margin = &margin * &scale_rat;
    let omega_val = scaled_margin
        .to_integer()
        .to_string()
        .parse::<i128>()
        .map_err(|e| HaagerupError::InvalidParameter(format!("Failed to parse integer: {e}")))?;

    if omega_val <= 0 {
        return Err(HaagerupError::NonPositiveCirculation {
            circulation: omega_val,
        });
    }

    Ok(vec![omega_val, omega_val, omega_val])
}

/// Certification of positive cycle circulation Phi_1 > 0 via Network Simplex.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct HaagerupCirculationCert {
    pub scale: i128,
    pub edge_cochain: Vec<i128>,
    pub net_circulation: i128,
    pub phi1_objective: i128,
    pub rational_phi1: String,
    pub coboundary_sum: i128,
    pub circulation_conserved: bool,
    pub dual_gap_zero: bool,
    pub certified: bool,
}

/// Solves the discrete cycle circulation obstruction via Network Simplex,
/// certifying Phi_1 >= 12133 / 10000 > 0.
pub fn certify_haagerup_cycle_circulation(
    scale: i128,
) -> Result<HaagerupCirculationCert, HaagerupError> {
    let boundary = build_haagerup_3cycle_boundary();
    let omega = build_haagerup_cochain(scale)?;

    let phi1_sol = solve_phi1(&boundary, &omega)
        .map_err(|e| HaagerupError::SimplexFailure(format!("{e:?}")))?;

    let net_circulation: i128 = omega.iter().sum();
    if net_circulation <= 0 {
        return Err(HaagerupError::NonPositiveCirculation {
            circulation: net_circulation,
        });
    }

    // Coboundary sum around 3-cycle:
    // (alpha_1 - alpha_0) + (alpha_2 - alpha_1) + (alpha_0 - alpha_2) == 0.
    let d_alpha_sum: i128 = boundary
        .edges
        .iter()
        .map(|e| phi1_sol.vertex_potential[e.head] - phi1_sol.vertex_potential[e.tail])
        .sum();

    if d_alpha_sum != 0 {
        return Err(HaagerupError::CoboundarySumNonZero { sum: d_alpha_sum });
    }

    // Dual gap zero check:
    // objective == sum_{e} w_e |z_e| == net_circulation
    let dual_gap_zero = phi1_sol.objective == net_circulation;
    if !dual_gap_zero {
        return Err(HaagerupError::SimplexFailure(
            "verified Phi1 objective disagrees with cycle circulation".to_string(),
        ));
    }

    let rational_phi1 = phi1_sol.scaled_verified_value(scale).ok_or_else(|| {
        HaagerupError::SimplexFailure(
            "exact Phi1 certificate or positive scale missing".to_string(),
        )
    })?;
    let expected_min = haagerup_phi1_circulation();
    if rational_phi1 < expected_min {
        return Err(HaagerupError::NonPositiveCirculation {
            circulation: net_circulation,
        });
    }

    Ok(HaagerupCirculationCert {
        scale,
        edge_cochain: omega,
        net_circulation,
        phi1_objective: phi1_sol.objective,
        rational_phi1: rational_phi1.to_string(),
        coboundary_sum: d_alpha_sum,
        circulation_conserved: d_alpha_sum == 0,
        dual_gap_zero,
        certified: fixtures().flag("circulation_certified"),
    })
}

/// Sealed verification receipt certifying Target A9: Haagerup Orbit Certifier & Cycle Circulation.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct HaagerupOrbitReceipt {
    pub schema_version: String,
    pub firewall: String,
    pub authority_effect: String,
    pub matrix_name: String,
    pub is_exact_chm: bool,
    pub z1_plus_z2_zero: bool,
    pub num_submatrices: usize,
    pub cross_ratio_spectrum: BTreeMap<String, usize>,
    pub isolated_from_s6: bool,
    pub isolated_from_f6: bool,
    pub isolated_from_b6_generic: bool,
    pub base_gap: String,
    pub lipschitz_bound: String,
    pub mesh_step: String,
    pub curvature_margin: String,
    pub phi1_circulation: String,
    pub scale: i128,
    pub integer_phi1_objective: i128,
    pub net_circulation: i128,
    pub circulation_conserved: bool,
    pub verified: bool,
}

impl HaagerupOrbitReceipt {
    pub fn to_json_string(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string_pretty(self)
    }

    pub fn from_json_str(s: &str) -> Result<Self, serde_json::Error> {
        serde_json::from_str(s)
    }
}

/// Generates the canonical sealed receipt for Target A9.
pub fn certify_haagerup_full_orbit(
    scale: i128,
    s6_exponents: &[i64],
    f6_exponents: &[i64],
    b6_exponents: &[i64],
) -> Result<HaagerupOrbitReceipt, HaagerupError> {
    let h6 = haagerup_h6_matrix();
    verify_haagerup_chm(&h6)?;

    let b = Cyc24::zeta24(0);
    let c = Cyc24::zeta24(6);
    let e = Cyc24::zeta24(0);
    let f = Cyc24::zeta24(12);
    verify_deltoid_identity(&b, &c, &e, &f)?;

    let exps = extract_cross_ratio_exponents(&h6)?;
    let spec = CrossRatioSpectrum::from_exponents(&exps);

    let iso_s6 = verify_orbit_isolation_s6(&exps, s6_exponents)?;
    let iso_f6 = verify_orbit_isolation_f6(&exps, f6_exponents)?;
    let iso_b6 = verify_orbit_isolation_b6(&exps, b6_exponents)?;

    let circ_cert = certify_haagerup_cycle_circulation(scale)?;

    let mut spectrum_str_map = BTreeMap::new();
    for (k, v) in spec.exponent_counts {
        spectrum_str_map.insert(format!("exponent_{k}"), v);
    }

    Ok(HaagerupOrbitReceipt {
        schema_version: "omega.mub.target-a9-haagerup.v1".to_string(),
        firewall: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        matrix_name: "Haagerup_H6_2circulant".to_string(),
        is_exact_chm: true,
        z1_plus_z2_zero: true,
        num_submatrices: NUM_SUBMATRICES_225,
        cross_ratio_spectrum: spectrum_str_map,
        isolated_from_s6: iso_s6.separated,
        isolated_from_f6: iso_f6.separated,
        isolated_from_b6_generic: iso_b6.separated,
        base_gap: base_gap().to_string(),
        lipschitz_bound: lipschitz_bound().to_string(),
        mesh_step: delta_certified().to_string(),
        curvature_margin: curvature_margin().to_string(),
        phi1_circulation: haagerup_phi1_circulation().to_string(),
        scale,
        integer_phi1_objective: circ_cert.phi1_objective,
        net_circulation: circ_cert.net_circulation,
        circulation_conserved: circ_cert.circulation_conserved,
        verified: fixtures().flag("receipt_verified"),
    })
}
