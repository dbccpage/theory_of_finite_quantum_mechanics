//! Bounded rival-composition controls. AuthorityEffect: None.
use finite_qm_native::campaigns::no_signalling::*;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{involution as star, matrix as mx, ExactFieldError};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_quantum_physics::no_signalling::*;

#[test]
fn test_t840_rival_composition_search() {
    let (n, signalling) = enumerate_rival_compositions().unwrap();
    assert!(n >= 4);
    assert!(!signalling);
}

#[test]
fn test_t842_mutation_4_rival_composition_accepted_without_verifying_bilinearity() {
    let direct_sum = |a: &BasicMatrix<GaussianRat>,
                      b: &BasicMatrix<GaussianRat>|
     -> Result<BasicMatrix<GaussianRat>, ExactFieldError> {
        let mut out = mx::zeros(4, 4)?;
        for i in 0..2 {
            for j in 0..2 {
                out.set(i, j, a.get_ref(i, j)?.clone())?;
                out.set(i + 2, j + 2, b.get_ref(i, j)?.clone())?;
            }
        }
        Ok(out)
    };
    assert!(!verify_bilinearity(direct_sum).unwrap());
}

#[test]
fn test_t842_mutation_5_signalling_witness_that_does_not_signal() {
    let w = mx::kronecker(
        &omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Z,
        )
        .expect("fixed Pauli carrier"),
        &omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Identity,
        )
        .expect("fixed Pauli carrier"),
    )
    .unwrap();
    let twisted = |a: &BasicMatrix<GaussianRat>, b: &BasicMatrix<GaussianRat>| {
        mx::multiply(
            &mx::multiply(&w, &mx::kronecker(a, b).unwrap()).unwrap(),
            &w,
        )
        .unwrap()
    };
    let rho = bell_phi_plus();
    let local = twisted(
        &omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::X,
        )
        .expect("fixed Pauli carrier"),
        &omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Identity,
        )
        .expect("fixed Pauli carrier"),
    );
    let post = mx::multiply(
        &mx::multiply(&local, &rho).unwrap(),
        &star::adjoint(&local).unwrap(),
    )
    .unwrap();
    for obs in [
        omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Identity,
        )
        .expect("fixed Pauli carrier"),
        omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::X,
        )
        .expect("fixed Pauli carrier"),
        omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Y,
        )
        .expect("fixed Pauli carrier"),
        omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Z,
        )
        .expect("fixed Pauli carrier"),
    ] {
        let observable = twisted(
            &omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
                omega_lie_theory::pauli_symplectic::Pauli::Identity,
            )
            .expect("fixed Pauli carrier"),
            &obs,
        );
        assert_eq!(
            mx::trace(&mx::multiply(&observable, &rho).unwrap()).unwrap(),
            mx::trace(&mx::multiply(&observable, &post).unwrap()).unwrap()
        );
    }
    assert_eq!(mx::trace(&rho).unwrap(), GaussianRat::one());
}
