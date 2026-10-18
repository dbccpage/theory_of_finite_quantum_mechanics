// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)
// Governing Rule: RULE[user_global] (Strict Zero-Float Law in Algebraic Core, Diagnostic Lens in Engine Bridge).

//! Engine bridge linking the exact finite QM of `omega_quantum_physics` with the
//! numerical observables of `omega_engines::quantum`. (It was the separate
//! `omega_finite_qm` crate until 2026-09-28; that crate held nothing else.)
//!
//! Provides bidirectional conversions and diagnostic bridges between:
//! 1. Exact algebraic finite QM states (`BasicMatrix<T>` over Rational, GaussianRat, Cyc24)
//! 2. Domain diagonal density matrices (`omega_quantum_physics::density_matrix::DensityMatrix`)
//! 3. Production numerical density matrices and quantum observables (`omega_engines::quantum::*`)
//! 4. Derivation targets in `omega_quantum_physics` (Born-Gleason, composition tomography)
//!
//! Authority Fence: All floating-point engine observables are diagnostic evaluations
//! and do not compromise the exact rational proofs of finite quantum mechanics.

use num_traits::ToPrimitive;
use serde::{Deserialize, Serialize};

use crate::linear_algebra::basic_matrix::BasicMatrix;
use omega_number_theory::rational::Rational;
use omega_quantum_physics::engine_bridge::{
    cyc24_matrix_to_prod_density, rational_matrix_to_prod_density,
};
use omega_quantum_physics::tomography;

// Production engine imports
use linear_algebra::linear_algebra::density::{DensityMatrix, DensityMatrixConfig};
use omega_engines::quantum::density::{
    bures_angle_observable, bures_distance_observable, classical_projection_observable,
    classical_projection_observable_checked, fidelity_observable, purity_observable,
    trace_observable, von_neumann_entropy_observable,
};

/// Authority fence string.
pub const ENGINE_BRIDGE_FENCE: &str =
    "AuthorityEffect None; Diagnostics only; exact finite QM preserved; engine observables are computational lenses.";

/// Diagnostic report containing engine-evaluated observables on a quantum state.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct EngineObservablesReport {
    pub dimension: usize,
    pub trace: f64,
    pub purity: f64,
    pub von_neumann_entropy: f64,
    pub classical_probabilities: Vec<f64>,
    pub is_pure: bool,
}

/// Comparison report cross-verifying an exact state against engine observables.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct StateEngineComparisonReport {
    pub state_name: String,
    pub dimension: usize,
    pub observables: EngineObservablesReport,
    pub diagnostic_trace_matches: bool,
    pub expected_pure: bool,
    pub purity_matches_expectation: bool,
}

// ============================================================================
// 2. Observable Evaluation
// ============================================================================

/// Evaluate standard quantum engine observables on a production `DensityMatrix`.
pub fn evaluate_state_observables(dm: &DensityMatrix) -> EngineObservablesReport {
    let trace = trace_observable(dm);
    let purity = purity_observable(dm);
    let von_neumann_entropy = von_neumann_entropy_observable(dm);
    let classical_probabilities = classical_projection_observable(dm);
    let is_pure = (purity - 1.0).abs() < 1e-4;

    EngineObservablesReport {
        dimension: dm.dim(),
        trace,
        purity,
        von_neumann_entropy,
        classical_probabilities,
        is_pure,
    }
}

/// Cross-verify a named exact state from `finite_qm::tomography` against engine observables.
pub fn verify_exact_state_with_engine(
    state_name: &str,
    dim: usize,
) -> Result<StateEngineComparisonReport, String> {
    let (prod_dm, expected_pure) = match (dim, state_name) {
        (2, "ground") => {
            let exact = tomography::state_ground_d2();
            let dm = cyc24_matrix_to_prod_density(&exact, None)
                .map_err(|e| format!("Failed to convert d=2 ground state: {:?}", e))?;
            (dm, true)
        }
        (2, "superposition") => {
            let exact = tomography::state_superposition_d2();
            let dm = cyc24_matrix_to_prod_density(&exact, None)
                .map_err(|e| format!("Failed to convert d=2 superposition state: {:?}", e))?;
            (dm, true)
        }
        (3, "ground") => {
            let exact = tomography::state_ground_d3();
            let dm = cyc24_matrix_to_prod_density(&exact, None)
                .map_err(|e| format!("Failed to convert d=3 ground state: {:?}", e))?;
            (dm, true)
        }
        (3, "magic") => {
            let exact = tomography::state_magic_d3();
            let dm = cyc24_matrix_to_prod_density(&exact, None)
                .map_err(|e| format!("Failed to convert d=3 magic state: {:?}", e))?;
            (dm, true)
        }
        (3, "mixed") => {
            let exact = tomography::state_mixed_rational_d3();
            let dm = cyc24_matrix_to_prod_density(&exact, None)
                .map_err(|e| format!("Failed to convert d=3 mixed state: {:?}", e))?;
            (dm, false)
        }
        (3, "superposition") => {
            let exact = tomography::state_superposition_d3();
            let dm = cyc24_matrix_to_prod_density(&exact, None)
                .map_err(|e| format!("Failed to convert d=3 superposition state: {:?}", e))?;
            (dm, true)
        }
        (4, "ground") => {
            let exact = tomography::state_ground_d4();
            let dm = cyc24_matrix_to_prod_density(&exact, None)
                .map_err(|e| format!("Failed to convert d=4 ground state: {:?}", e))?;
            (dm, true)
        }
        (4, "bell") => {
            let exact = tomography::state_bell_d4();
            let dm = cyc24_matrix_to_prod_density(&exact, None)
                .map_err(|e| format!("Failed to convert d=4 Bell state: {:?}", e))?;
            (dm, true)
        }
        (4, "mixed") => {
            let exact = tomography::state_mixed_d4();
            let dm = cyc24_matrix_to_prod_density(&exact, None)
                .map_err(|e| format!("Failed to convert d=4 mixed state: {:?}", e))?;
            (dm, false)
        }
        _ => {
            return Err(format!(
                "Unrecognized or unsupported state '{}' in dimension {}",
                state_name, dim
            ));
        }
    };

    let observables = evaluate_state_observables(&prod_dm);
    let diagnostic_trace_matches = (observables.trace - 1.0).abs() < 1e-6;
    let purity_matches_expectation = if expected_pure {
        observables.is_pure
    } else {
        !observables.is_pure && observables.purity < 0.99
    };

    Ok(StateEngineComparisonReport {
        state_name: state_name.to_string(),
        dimension: dim,
        observables,
        diagnostic_trace_matches,
        expected_pure,
        purity_matches_expectation,
    })
}

/// Evaluate diagnostic Uhlmann / Jozsa fidelity between two production density matrices.
pub fn evaluate_state_fidelity(rho: &DensityMatrix, sigma: &DensityMatrix) -> Result<f64, String> {
    fidelity_observable(rho, sigma)
}

/// Compute Bures metric distance and angle between two states.
pub fn evaluate_bures_geometry(
    rho: &DensityMatrix,
    sigma: &DensityMatrix,
) -> Result<(f64, f64), String> {
    let dist = bures_distance_observable(rho, sigma)?;
    let angle = bures_angle_observable(rho, sigma)?;
    Ok((dist, angle))
}

// ============================================================================
// 3. Domain Derivation Bridges (Born-Gleason & Local Tomography)
// ============================================================================

/// Largest gap the Born bridge tolerates between an exact Born weight and the
/// engine's floating-point classical projection.
pub const BORN_BRIDGE_TOLERANCE: f64 = 1e-12;

/// Whether each engine weight lies within `tolerance` of the exact Born weight
/// in the same position.
pub fn born_weights_match_projection(
    exact: &crate::qm::campaigns::born_gleason::FrameFunction,
    projection: &[f64],
    tolerance: f64,
) -> bool {
    exact.on_basis.len() == projection.len()
        && exact
            .on_basis
            .iter()
            .zip(projection)
            .all(|(p, q)| p.to_f64().is_some_and(|p| (p - q).abs() <= tolerance))
}

/// Bridge between the exact Born weights of a state and the engine's
/// classical projection of it.
///
/// Exact side: the weights `p_i = rho_ii` become a
/// `born_gleason::FrameFunction`, which refuses negative weights and weights
/// that do not sum to one, and the declared Gleason assumptions must all be
/// paid. Engine side: `rho` becomes the engine's density matrix (the engine
/// validates it) and `classical_projection_observable` reads its diagonal. The
/// bridge holds when every engine weight is within [`BORN_BRIDGE_TOLERANCE`] of
/// the exact one. It checks the engine against exact values on one basis. The
/// assumptions are declared, not computed, and nothing here proves Gleason's
/// theorem.
pub fn verify_born_gleason_domain_bridge(
    rho: &BasicMatrix<Rational>,
    assumptions: &crate::qm::campaigns::born_gleason::GleasonAssumptions,
) -> Result<bool, String> {
    use crate::qm::campaigns::born_gleason::FrameFunction;

    let unpaid = assumptions.unpaid();
    if !unpaid.is_empty() {
        return Err(format!("unpaid Gleason assumptions: {unpaid:?}"));
    }
    if rho.rows() != rho.cols() || rho.rows() != assumptions.dimension {
        return Err(format!(
            "a {}x{} state for a declared dimension {}",
            rho.rows(),
            rho.cols(),
            assumptions.dimension
        ));
    }
    let weights: Vec<Rational> = (0..rho.rows())
        .map(|i| rho.get(i, i).map_err(|e| format!("matrix refused: {e}")))
        .collect::<Result<_, _>>()?;
    let frame = FrameFunction::born_from_populations(&weights)
        .map_err(|e| format!("not a Born frame: {e:?}"))?;
    let engine = rational_matrix_to_prod_density(rho, None)
        .map_err(|e| format!("engine refused the state: {e:?}"))?;
    let projection =
        classical_projection_observable_checked(&engine, &DensityMatrixConfig::default())
            .map_err(|e| format!("engine projection refused: {e:?}"))?;
    Ok(born_weights_match_projection(
        &frame,
        &projection,
        BORN_BRIDGE_TOLERANCE,
    ))
}

/// Bridge between the counted local-tomography identity and the computed span
/// of product effects.
///
/// On `C^(d_A) (x) C^(d_B)` (`ComplexU1`) the count `d_A^2 d_B^2 = (d_A d_B)^2`
/// holds for every pair of dimensions, so it decides nothing by itself; the
/// exact rank of the product Hermitian effects in the joint Hermitian space
/// does. On `R^(d_A) (x) R^(d_B)` (`RealOnly`) the same pipeline runs on real
/// symmetric bases against `n(n+1)/2`. Returns whether the product effects
/// span, and refuses when the computed rank and the parameter count disagree.
/// The engine has no tomography observable, so both sides here are exact.
pub fn verify_composition_tomography_domain_bridge(
    dim_a: usize,
    dim_b: usize,
    carrier: omega_quantum_physics::composition_tomography::PhaseCarrier,
) -> Result<bool, String> {
    use omega_quantum_physics::composition_tomography::{
        local_tomography_spanning_complex, local_tomography_spanning_real_via_gaussian,
        LocalTomographyReport, PhaseCarrier,
    };

    let (span, count_holds) = match carrier {
        PhaseCarrier::ComplexU1 => {
            let count = LocalTomographyReport::complex_product(dim_a, dim_b)
                .map_err(|e| format!("{e:?}"))?;
            (
                local_tomography_spanning_complex(dim_a, dim_b).map_err(|e| format!("{e:?}"))?,
                count.identity_holds,
            )
        }
        PhaseCarrier::RealOnly => {
            if dim_a == 0 || dim_b == 0 {
                return Err("a factor dimension is zero".to_string());
            }
            let count = LocalTomographyReport::real_product_params(dim_a, dim_b)
                .map_err(|e| format!("{e:?}"))?;
            (
                local_tomography_spanning_real_via_gaussian(dim_a, dim_b)
                    .map_err(|e| format!("{e:?}"))?,
                count.identity_holds,
            )
        }
    };
    if span.spans != count_holds {
        return Err(format!(
            "rank {} of {} product effects in a joint space of dimension {} disagrees with the parameter count",
            span.product_rank, span.product_count, span.joint_dim
        ));
    }
    Ok(span.spans)
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_quantum_physics::engine_bridge::domain_diagonal_to_prod_density;

    #[test]
    fn test_d3_ground_state_engine_observables() {
        let rep = verify_exact_state_with_engine("ground", 3).unwrap();
        assert!(rep.diagnostic_trace_matches);
        assert!(rep.expected_pure);
        assert!(rep.purity_matches_expectation);
        assert!((rep.observables.purity - 1.0).abs() < 1e-5);
        assert!(rep.observables.von_neumann_entropy < 1e-5);
    }

    #[test]
    fn test_d3_mixed_state_engine_observables() {
        let rep = verify_exact_state_with_engine("mixed", 3).unwrap();
        assert!(rep.diagnostic_trace_matches);
        assert!(!rep.expected_pure);
        assert!(rep.purity_matches_expectation);
        assert!(rep.observables.purity < 0.9);
        assert!(rep.observables.von_neumann_entropy > 0.1);
    }

    #[test]
    fn test_d4_bell_state_engine_observables() {
        let rep = verify_exact_state_with_engine("bell", 4).unwrap();
        assert!(rep.diagnostic_trace_matches);
        assert!(rep.expected_pure);
        assert!(rep.purity_matches_expectation);
        assert!((rep.observables.purity - 1.0).abs() < 1e-4);
        assert!(rep.observables.von_neumann_entropy < 1e-4);
    }

    #[test]
    fn test_domain_diagonal_density_conversion() {
        let h_space = omega_quantum_physics::hilbert_space::HilbertSpace::new(3, "H3");
        let r_third = num_rational::Ratio::new(1, 3);
        let domain_dm =
            omega_quantum_physics::density_matrix::DensityMatrix::try_from_rational_probs(
                &h_space,
                vec![r_third, r_third, r_third],
                "maximally_mixed_d3",
            )
            .unwrap();

        let prod_dm = domain_diagonal_to_prod_density(&domain_dm, None).unwrap();
        let obs = evaluate_state_observables(&prod_dm);
        assert!((obs.trace - 1.0).abs() < 1e-6);
        assert!((obs.purity - 1.0 / 3.0).abs() < 1e-5);
        assert!(!obs.is_pure);
    }

    #[test]
    fn test_born_gleason_and_composition_bridges() {
        let assumptions = crate::qm::campaigns::born_gleason::GleasonAssumptions {
            dimension: 3,
            noncontextual: true,
            finite_additivity: true,
            complex_scalars: true,
            no_silent_continuum: true,
        };
        let r = |n: i64, d: i64| Rational::new(n.into(), d.into());
        let zero = r(0, 1);
        let rho = BasicMatrix::from_row_major(
            3,
            3,
            vec![
                r(1, 2),
                r(1, 4),
                zero.clone(),
                r(1, 4),
                r(1, 3),
                zero.clone(),
                zero.clone(),
                zero.clone(),
                r(1, 6),
            ],
        )
        .unwrap();
        assert!(verify_born_gleason_domain_bridge(&rho, &assumptions).unwrap());
        let complex = omega_quantum_physics::composition_tomography::PhaseCarrier::ComplexU1;
        assert!(verify_composition_tomography_domain_bridge(2, 2, complex).unwrap());
    }
}
