

pub use crate::qm::domain::finite_spinfoam_model::{
    adjoint_bulk, admissible, census, quantum_integer, real_value, simplex4, sphere_euler,
    sphere_partition, tetrahedron, transition, transition_matrix, ADMISSIBLE_BASIS, BoundaryState,
    ModelVersion, PachnerState, SpinFoamCensus, SpinFoamModelError,
};

use crate::qm::finite_witness::{field_usize, qvec};
use serde_json::{json, Value};

fn host_error(error: SpinFoamModelError) -> String {
    match error {
        SpinFoamModelError::Input(message) => message,
        other => other.to_string(),
    }
}

pub fn run(input: &Value) -> Result<Value, String> {
    let level = field_usize(input, "level", 2, 3)?;
    let found = census(level).map_err(host_error)?;
    Ok(json!({
        "authority_effect": "None",
        "scope": "declared parity and cyclotomic models; bounded spin enumeration; no general unitarity, convergence, or topological invariance claim",
        "spin_level_exclusive": found.level,
        "tetrahedra_checked": found.tetrahedra_checked,
        "simplices_checked": found.simplices_checked,
        "admissible_tetrahedra": found.admissible_tetrahedra,
        "admissible_simplices": found.admissible_simplices,
        "quantum_integers": (0..=6).map(|n| qvec(&quantum_integer(n).coefficient_values())).collect::<Vec<_>>(),
        "sphere_euler": found.sphere_euler,
        "checks": {
            "q2_square_three": found.q2_square_three,
            "q6_zero": found.q6_zero,
            "tetra_orientation": found.tetra_orientation,
            "simplex_symmetries": found.simplex_symmetries,
            "boundary_projector": found.boundary_projector,
            "master_self_adjoint_on_basis": found.master_self_adjoint_on_basis,
            "diagonal_evolution_projector": found.diagonal_evolution_projector,
            "pachner_intertwining": found.pachner_intertwining,
            "sphere_euler_two": found.sphere_euler_two,
            "sphere_vacuum_partition": found.sphere_vacuum_partition,
            "corrected_vacuum_transition_unitary": found.corrected_vacuum_transition_unitary,
            "corrected_partition_unit_norm_and_pachner_invariance": found.corrected_partition_unit_norm_and_pachner_invariance
        },
        "limitations": [
            "The published transition matrix is not unitary: distinct admissible boundaries have transition a(W). The corrected H025 transition, a(W) on the diagonal of admissible boundaries, is unitary exactly when a(W) is a unit.",
            "The published H027 partition uses amplitude times projected amplitude, without conjugation; the corrected H027 partition conjugates.",
            "The q6 identity alone does not prove convergence of an unspecified spin sum."
        ]
    }))
}

#[cfg(test)]
mod tests {
    use super::*;
    use engine_number_theory::cyclotomic_integer::CyclotomicInteger as C;

    #[test]
    fn finite_lean_models() {
        let r = run(&Value::Null).unwrap();
        assert!(r["checks"].as_object().unwrap().values().all(|x| x == true));
        assert_eq!(r["admissible_tetrahedra"], 8);
        assert_eq!(r["admissible_simplices"], 64);
    }

    #[test]
    fn nonclaims_have_counterexamples() {
        let off_diagonal = |version| transition(version, &[0; 4], &[1, 1, 0, 0], &[0; 10]);
        assert_eq!(
            off_diagonal(ModelVersion::Published),
            C::scalar(12, 1).expect("fixed valid conductor")
        );
        assert_eq!(
            off_diagonal(ModelVersion::Corrected),
            C::scalar(12, 0).expect("fixed valid conductor")
        );
    }
}
