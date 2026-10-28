use crate::qm::bridge::matrix as mx;
use num_bigint::BigInt;
use num_traits::{Signed, Zero};
use engine_homology::f2_cohomology::F2ChainComplex;
use engine_lie_theory::pauli_symplectic::{pauli_word, Pauli};
use engine_number_theory::cyclotomic::GaussianRat;
use engine_number_theory::gf2::{F2Matrix, F2Vector};
use engine_quantum_physics::lattice_gauge_manybody_benchmark::Z2LatticeGauge;
use serde_json::json;

fn tfim_root(j: i64, h: i64) -> (BigInt, BigInt, bool, String) {
    let j = BigInt::from(j);
    let h = BigInt::from(h);
    let radicand: BigInt = &j * &j + BigInt::from(4) * &h * &h;
    let root = BigInt::sqrt(&radicand);
    let is_square = &root * &root == radicand;
    let expression = if is_square {
        root.to_string()
    } else {
        format!("sqrt({radicand})")
    };
    (radicand, root, is_square, expression)
}

pub fn tfim_l2_eigenvalues(j: i64, h: i64) -> Vec<String> {
    let (radicand, _, _, root) = tfim_root(j, h);
    let magnitude = BigInt::from(j).abs();
    let negative_root = if radicand.is_zero() {
        "0".to_string()
    } else {
        format!("-{root}")
    };
    vec![
        negative_root,
        (-&magnitude).to_string(),
        magnitude.to_string(),
        root,
    ]
}

pub fn tfim_characteristic_polynomial(j: i64, h: i64) -> Vec<String> {
    let j = BigInt::from(j);
    let h = BigInt::from(h);
    let j2 = &j * &j;
    let four_h2 = BigInt::from(4) * &h * &h;
    vec![
        "1".to_string(),
        "0".to_string(),
        (-(&j2 * BigInt::from(2) + &four_h2)).to_string(),
        "0".to_string(),
        (&j2 * (&j2 + four_h2)).to_string(),
    ]
}

pub fn tfim_l2_gap(j: i64, h: i64) -> String {
    let magnitude = BigInt::from(j).abs();
    let (_, root, is_square, expression) = tfim_root(j, h);
    if h == 0 {
        (&magnitude * BigInt::from(2)).to_string()
    } else if is_square {
        (root - magnitude).to_string()
    } else if magnitude.is_zero() {
        expression
    } else {
        format!("{expression} - {magnitude}")
    }
}

fn square_plaquette() -> Z2LatticeGauge {
    let incidence = F2Matrix::from_rows(&[
        vec![1, 0, 0, 1],
        vec![1, 1, 0, 0],
        vec![0, 1, 1, 0],
        vec![0, 0, 1, 1],
    ])
    .expect("fixed square incidence");
    let boundary = F2Matrix::from_rows(&[vec![1], vec![1], vec![1], vec![1]])
        .expect("fixed plaquette boundary");
    Z2LatticeGauge::new(
        F2ChainComplex::new(vec![4, 4, 1], vec![incidence, boundary])
            .expect("square boundary composes to zero"),
    )
    .expect("fixed square gauge carrier")
}
pub fn z2_plaquette_invariance() -> (bool, bool, bool) {
    use Pauli::{Identity as I, X, Z};
    let gauss = [[X, I, I, X], [X, X, I, I], [I, X, X, I], [I, I, X, X]]
        .map(|w| pauli_word::<GaussianRat>(&w).expect("fixed Pauli star"));
    let flux = pauli_word::<GaussianRat>(&[Z; 4]).expect("fixed magnetic plaquette");
    let electric = (0..4)
        .map(|edge| {
            let mut word = [I; 4];
            word[edge] = X;
            pauli_word::<GaussianRat>(&word).expect("fixed electric link")
        })
        .collect::<Vec<_>>();
    let commutes =
        |a: &::linear_algebra::backend::basic_matrix::BasicMatrix<GaussianRat>,
         b: &::linear_algebra::backend::basic_matrix::BasicMatrix<GaussianRat>| {
            mx::multiply(a, b).expect("fixed sixteen-dimensional carrier")
                == mx::multiply(b, a).expect("fixed sixteen-dimensional carrier")
        };
    let flux_commutes = gauss.iter().all(|g| commutes(g, &flux));
    let electric_commutes = gauss
        .iter()
        .all(|g| electric.iter().all(|e| commutes(g, e)));
    let hamiltonian = electric.iter().fold(flux.clone(), |h, e| {
        mx::add(&h, e).expect("fixed Hamiltonian shape")
    });
    let model = square_plaquette();
    let cycle = F2Vector::from_indices(4, &[0, 1, 2, 3]).expect("fixed cycle");
    let preserved = gauss.iter().all(|g| commutes(g, &hamiltonian))
        && model
            .physical_labels(16)
            .expect("two physical labels")
            .iter()
            .all(|label| {
                let moved = model
                    .magnetic_flip(label, &cycle)
                    .expect("cycle preserves Gauss constraints");
                model
                    .is_physical_x_label(&moved)
                    .expect("fixed label shape")
            });
    (flux_commutes, electric_commutes, preserved)
}
pub fn z2_physical_x_basis_labels() -> Vec<u32> {
    square_plaquette()
        .physical_labels(16)
        .expect("two physical labels")
        .iter()
        .map(|label| {
            label
                .support()
                .into_iter()
                .fold(0u32, |mask, edge| mask | (1u32 << edge))
        })
        .collect()
}

pub fn separate_continuum_obligations() -> (usize, bool) {
    (3, false)
}

pub fn generate_canonical_block09_rust_receipt() -> serde_json::Value {
    let evals = tfim_l2_eigenvalues(1, 1);
    let (flux, electric, preserved) = z2_plaquette_invariance();
    let (count, all_proved) = separate_continuum_obligations();

    json!({
        "campaign": "C500",
        "block": "block_09",
        "authority_effect": "None",
        "terminal_outcome": "FINITE_LATTICE_BENCHMARKS_WITH_SCALING_OBLIGATIONS",
        "tfim_l2_eigenvalues": evals,
        "tfim_ground_state_energy": evals[0],
        "tfim_gap": tfim_l2_gap(1, 1),
        "tfim_characteristic_polynomial_descending": tfim_characteristic_polynomial(1, 1),
        "z2_gauge_flux_commutes": flux,
        "z2_gauge_electric_commutes": electric,
        "gauge_subspace_preserved": preserved,
        "physical_x_basis_labels": z2_physical_x_basis_labels(),
        "physical_subspace_dimension": z2_physical_x_basis_labels().len(),
        "continuum_obligation_count": count,
        "all_continuum_limits_proved": all_proved,
        "standard_model_recovery_claimed": false,
        "status": "SCOPED_COMPUTATION"
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tfim_spectrum() {
        let evals = tfim_l2_eigenvalues(1, 1);
        assert_eq!(evals, vec!["-sqrt(5)", "-1", "1", "sqrt(5)"]);
        assert_eq!(tfim_l2_gap(1, 1), "sqrt(5) - 1");
        assert_eq!(
            tfim_characteristic_polynomial(1, 1),
            vec!["1", "0", "-6", "0", "5"]
        );
    }

    #[test]
    fn test_field_dependence_and_degenerate_ground_space() {
        assert_eq!(tfim_l2_eigenvalues(1, 0), vec!["-1", "-1", "1", "1"]);
        assert_eq!(tfim_l2_gap(1, 0), "2");
        assert_eq!(tfim_l2_eigenvalues(0, 1), vec!["-2", "0", "0", "2"]);
        assert_eq!(tfim_l2_eigenvalues(3, 2), vec!["-5", "-3", "3", "5"]);
        assert_eq!(tfim_l2_eigenvalues(0, 0), vec!["0", "0", "0", "0"]);
        assert_eq!(tfim_l2_gap(0, 0), "0");
        assert_eq!(tfim_l2_eigenvalues(i64::MIN, 0)[0], "-9223372036854775808");
    }

    #[test]
    fn test_gauge_invariance() {
        let (flux, electric, preserved) = z2_plaquette_invariance();
        assert!(flux);
        assert!(electric);
        assert!(preserved);
        assert_eq!(z2_physical_x_basis_labels(), vec![0, 15]);
    }

    #[test]
    fn test_continuum_obligations() {
        let (count, all_proved) = separate_continuum_obligations();
        assert_eq!(count, 3);
        assert!(!all_proved);
    }
}
