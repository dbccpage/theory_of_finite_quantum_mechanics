use num_traits::ToPrimitive;
use serde::{Deserialize, Serialize};

use ::linear_algebra::backend::basic_matrix::BasicMatrix;
use engine_number_theory::rational::Rational;
use engine_quantum_physics::engine_bridge::{
    cyc24_matrix_to_prod_density, rational_matrix_to_prod_density,
};
use engine_quantum_physics::tomography;

use linear_algebra::linear_algebra::density::{DensityMatrix, DensityMatrixConfig};
use engine_runtime::quantum::density::{
    bures_angle_observable, bures_distance_observable, classical_projection_observable,
    classical_projection_observable_checked, fidelity_observable, purity_observable,
    trace_observable, von_neumann_entropy_observable,
};

pub const ENGINE_BRIDGE_FENCE: &str =
    "AuthorityEffect None; Diagnostics only; exact finite QM preserved; engine observables are computational lenses.";

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct EngineObservablesReport {
    pub dimension: usize,
    pub trace: f64,
    pub purity: f64,
    pub von_neumann_entropy: f64,
    pub classical_probabilities: Vec<f64>,
    pub is_pure: bool,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct StateEngineComparisonReport {
    pub state_name: String,
    pub dimension: usize,
    pub observables: EngineObservablesReport,
    pub diagnostic_trace_matches: bool,
    pub expected_pure: bool,
    pub purity_matches_expectation: bool,
}

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

fn convert_state(
    exact: &BasicMatrix<engine_number_theory::cyclotomic::Cyc24>,
    label: &str,
    expected_pure: bool,
) -> Result<(DensityMatrix, bool), String> {
    let dm = cyc24_matrix_to_prod_density(exact, None)
        .map_err(|e| format!("Failed to convert {label} state: {:?}", e))?;
    Ok((dm, expected_pure))
}

fn exact_state_d2(state_name: &str) -> Result<(DensityMatrix, bool), String> {
    match state_name {
        "ground" => convert_state(&tomography::state_ground_d2(), "d=2 ground", true),
        "superposition" => convert_state(
            &tomography::state_superposition_d2(),
            "d=2 superposition",
            true,
        ),
        _ => Err(format!(
            "Unrecognized or unsupported state '{}' in dimension 2",
            state_name
        )),
    }
}

fn exact_state_d3(state_name: &str) -> Result<(DensityMatrix, bool), String> {
    match state_name {
        "ground" => convert_state(&tomography::state_ground_d3(), "d=3 ground", true),
        "magic" => convert_state(&tomography::state_magic_d3(), "d=3 magic", true),
        "mixed" => convert_state(&tomography::state_mixed_rational_d3(), "d=3 mixed", false),
        "superposition" => convert_state(
            &tomography::state_superposition_d3(),
            "d=3 superposition",
            true,
        ),
        _ => Err(format!(
            "Unrecognized or unsupported state '{}' in dimension 3",
            state_name
        )),
    }
}

fn exact_state_d4(state_name: &str) -> Result<(DensityMatrix, bool), String> {
    match state_name {
        "ground" => convert_state(&tomography::state_ground_d4(), "d=4 ground", true),
        "bell" => convert_state(&tomography::state_bell_d4(), "d=4 Bell", true),
        "mixed" => convert_state(&tomography::state_mixed_d4(), "d=4 mixed", false),
        _ => Err(format!(
            "Unrecognized or unsupported state '{}' in dimension 4",
            state_name
        )),
    }
}

pub fn verify_exact_state_with_engine(
    state_name: &str,
    dim: usize,
) -> Result<StateEngineComparisonReport, String> {
    let (prod_dm, expected_pure) = match dim {
        2 => exact_state_d2(state_name)?,
        3 => exact_state_d3(state_name)?,
        4 => exact_state_d4(state_name)?,
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

pub fn evaluate_state_fidelity(rho: &DensityMatrix, sigma: &DensityMatrix) -> Result<f64, String> {
    fidelity_observable(rho, sigma)
}

pub fn evaluate_bures_geometry(
    rho: &DensityMatrix,
    sigma: &DensityMatrix,
) -> Result<(f64, f64), String> {
    let dist = bures_distance_observable(rho, sigma)?;
    let angle = bures_angle_observable(rho, sigma)?;
    Ok((dist, angle))
}

pub const BORN_BRIDGE_TOLERANCE: f64 = 1e-12;

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

pub fn verify_composition_tomography_domain_bridge(
    dim_a: usize,
    dim_b: usize,
    carrier: engine_quantum_physics::composition_tomography::PhaseCarrier,
) -> Result<bool, String> {
    use engine_quantum_physics::composition_tomography::{
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
    use engine_quantum_physics::engine_bridge::domain_diagonal_to_prod_density;

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
        let h_space = engine_quantum_physics::hilbert_space::HilbertSpace::new(3, "H3");
        let r_third = num_rational::Ratio::new(1, 3);
        let domain_dm =
            engine_quantum_physics::density_matrix::DensityMatrix::try_from_rational_probs(
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
        let complex = engine_quantum_physics::composition_tomography::PhaseCarrier::ComplexU1;
        assert!(verify_composition_tomography_domain_bridge(2, 2, complex).unwrap());
    }
}
