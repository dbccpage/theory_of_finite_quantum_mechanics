use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::{involution as star, matrix as mx, ExactFieldError};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::rq;
use omega_quantum_physics::no_signalling::*;

pub fn verify_bilinearity<F>(rule: F) -> Result<bool, ExactFieldError>
where
    F: Fn(
        &BasicMatrix<GaussianRat>,
        &BasicMatrix<GaussianRat>,
    ) -> Result<BasicMatrix<GaussianRat>, ExactFieldError>,
{
    let (a1, a2, b1, b2) = (
        omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::X,
        )
        .expect("fixed Pauli carrier"),
        omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Z,
        )
        .expect("fixed Pauli carrier"),
        omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Y,
        )
        .expect("fixed Pauli carrier"),
        omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Identity,
        )
        .expect("fixed Pauli carrier"),
    );
    let c = GaussianRat::from_rational(rq(3, 5));
    Ok(
        rule(&mx::add(&a1, &a2)?, &b1)? == mx::add(&rule(&a1, &b1)?, &rule(&a2, &b1)?)?
            && rule(&a1, &mx::add(&b1, &b2)?)? == mx::add(&rule(&a1, &b1)?, &rule(&a1, &b2)?)?
            && rule(&mx::scale(&a1, &c)?, &b1)? == mx::scale(&rule(&a1, &b1)?, &c)?,
    )
}

pub type CompositionRule = Box<
    dyn Fn(
        &BasicMatrix<GaussianRat>,
        &BasicMatrix<GaussianRat>,
    ) -> Result<BasicMatrix<GaussianRat>, ExactFieldError>,
>;
pub struct RivalCandidate {
    pub name: &'static str,
    pub rule: CompositionRule,
    pub is_twisted: bool,
    pub commutes_one_factor_only: bool,
}

#[derive(Debug, thiserror::Error)]
pub enum RivalSearchError {
    #[error("exact-field algebra refused: {0}")]
    Arithmetic(#[from] ExactFieldError),
    #[error("rival {0} violates the declared bilinear unital law")]
    DeclaredLaw(&'static str),
}

pub fn enumerate_rival_compositions() -> Result<(usize, bool), RivalSearchError> {
    let w_z = mx::kronecker(
        &omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Z,
        )
        .expect("fixed Pauli carrier"),
        &omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
            omega_lie_theory::pauli_symplectic::Pauli::Identity,
        )
        .expect("fixed Pauli carrier"),
    )?;
    let w_cnot = cnot_matrix();
    let w_cz = cz_matrix();
    let rivals = vec![
        RivalCandidate {
            name: "twisted_z_product",
            rule: Box::new(move |a, b| {
                mx::multiply(&mx::multiply(&w_z, &mx::kronecker(a, b)?)?, &w_z)
            }),
            is_twisted: true,
            commutes_one_factor_only: true,
        },
        RivalCandidate {
            name: "cnot_twisted_product",
            rule: Box::new(move |a, b| {
                mx::multiply(&mx::multiply(&w_cnot, &mx::kronecker(a, b)?)?, &w_cnot)
            }),
            is_twisted: true,
            commutes_one_factor_only: false,
        },
        RivalCandidate {
            name: "swap_product",
            rule: Box::new(|a, b| mx::kronecker(b, a)),
            is_twisted: true,
            commutes_one_factor_only: false,
        },
        RivalCandidate {
            name: "cz_twisted_product",
            rule: Box::new(move |a, b| {
                mx::multiply(&mx::multiply(&w_cz, &mx::kronecker(a, b)?)?, &w_cz)
            }),
            is_twisted: true,
            commutes_one_factor_only: false,
        },
        RivalCandidate {
            name: "trace_split_bilinear",
            rule: Box::new(|a, b| {
                let id2 = omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
                    omega_lie_theory::pauli_symplectic::Pauli::Identity,
                )
                .expect("fixed Pauli carrier");
                let id4 = mx::identity(4)?;
                let t_a = mx::trace(a)?.mul(&GaussianRat::from_rational(rq(1, 2)));
                let t_b = mx::trace(b)?.mul(&GaussianRat::from_rational(rq(1, 2)));
                let t_ab = mx::trace(a)?
                    .mul(&mx::trace(b)?)
                    .mul(&GaussianRat::from_rational(rq(1, 4)));
                mx::sub(
                    &mx::add(
                        &mx::scale(&mx::kronecker(&id2, b)?, &t_a)?,
                        &mx::scale(&mx::kronecker(a, &id2)?, &t_b)?,
                    )?,
                    &mx::scale(&id4, &t_ab)?,
                )
            }),
            is_twisted: false,
            commutes_one_factor_only: false,
        },
    ];
    let mut signalling_found = false;
    let id2 = omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
        omega_lie_theory::pauli_symplectic::Pauli::Identity,
    )
    .expect("fixed Pauli carrier");
    let id4 = mx::identity(4)?;
    let paulis = [
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
    ];
    let half = GaussianRat::from_rational(rq(1, 2));
    for r in &rivals {
        if !verify_bilinearity(&r.rule)? || (r.rule)(&id2, &id2)? != id4 {
            return Err(RivalSearchError::DeclaredLaw(r.name));
        }
        for (_, rho) in all_bell_states() {
            let mut before = mx::zeros(2, 2)?;
            for sigma in &paulis {
                let obs = (r.rule)(&id2, sigma)?;
                let coeff = mx::trace(&mx::multiply(&obs, &rho)?)?.mul(&half);
                before = mx::add(&before, &mx::scale(sigma, &coeff)?)?;
            }
            for u in [
                &omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
                    omega_lie_theory::pauli_symplectic::Pauli::X,
                )
                .expect("fixed Pauli carrier"),
                &omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(
                    omega_lie_theory::pauli_symplectic::Pauli::Z,
                )
                .expect("fixed Pauli carrier"),
            ] {
                let joint = if r.is_twisted {
                    (r.rule)(u, &id2)?
                } else {
                    mx::kronecker(u, &id2)?
                };
                let post = mx::multiply(&mx::multiply(&joint, &rho)?, &star::adjoint(&joint)?)?;
                let mut after = mx::zeros(2, 2)?;
                for sigma in &paulis {
                    let obs = (r.rule)(&id2, sigma)?;
                    let coeff = mx::trace(&mx::multiply(&obs, &post)?)?.mul(&half);
                    after = mx::add(&after, &mx::scale(sigma, &coeff)?)?;
                }
                signalling_found |= after != before;
            }
        }
    }
    Ok((rivals.len(), signalling_found))
}
