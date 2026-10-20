use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::{involution as star, matrix as mx, ExactFieldError};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::rq;
use omega_quantum_physics::no_signalling::*;

fn pauli_mat(kind: omega_lie_theory::pauli_symplectic::Pauli) -> BasicMatrix<GaussianRat> {
    omega_lie_theory::pauli_symplectic::pauli::<GaussianRat>(kind).expect("fixed Pauli carrier")
}

fn check_left_additivity<F>(
    rule: &F,
    a1: &BasicMatrix<GaussianRat>,
    a2: &BasicMatrix<GaussianRat>,
    b1: &BasicMatrix<GaussianRat>,
) -> Result<bool, ExactFieldError>
where
    F: Fn(
        &BasicMatrix<GaussianRat>,
        &BasicMatrix<GaussianRat>,
    ) -> Result<BasicMatrix<GaussianRat>, ExactFieldError>,
{
    let lhs1 = rule(&mx::add(a1, a2)?, b1)?;
    let rhs1 = mx::add(&rule(a1, b1)?, &rule(a2, b1)?)?;
    Ok(lhs1 == rhs1)
}

fn check_right_additivity<F>(
    rule: &F,
    a1: &BasicMatrix<GaussianRat>,
    b1: &BasicMatrix<GaussianRat>,
    b2: &BasicMatrix<GaussianRat>,
) -> Result<bool, ExactFieldError>
where
    F: Fn(
        &BasicMatrix<GaussianRat>,
        &BasicMatrix<GaussianRat>,
    ) -> Result<BasicMatrix<GaussianRat>, ExactFieldError>,
{
    let lhs2 = rule(a1, &mx::add(b1, b2)?)?;
    let rhs2 = mx::add(&rule(a1, b1)?, &rule(a1, b2)?)?;
    Ok(lhs2 == rhs2)
}

fn check_left_and_right_additivity<F>(
    rule: &F,
    a1: &BasicMatrix<GaussianRat>,
    a2: &BasicMatrix<GaussianRat>,
    b1: &BasicMatrix<GaussianRat>,
    b2: &BasicMatrix<GaussianRat>,
) -> Result<bool, ExactFieldError>
where
    F: Fn(
        &BasicMatrix<GaussianRat>,
        &BasicMatrix<GaussianRat>,
    ) -> Result<BasicMatrix<GaussianRat>, ExactFieldError>,
{
    Ok(check_left_additivity(rule, a1, a2, b1)? && check_right_additivity(rule, a1, b1, b2)?)
}

pub fn verify_bilinearity<F>(rule: F) -> Result<bool, ExactFieldError>
where
    F: Fn(
        &BasicMatrix<GaussianRat>,
        &BasicMatrix<GaussianRat>,
    ) -> Result<BasicMatrix<GaussianRat>, ExactFieldError>,
{
    use omega_lie_theory::pauli_symplectic::Pauli;
    let a1 = pauli_mat(Pauli::X);
    let a2 = pauli_mat(Pauli::Z);
    let b1 = pauli_mat(Pauli::Y);
    let b2 = pauli_mat(Pauli::Identity);
    let add_ok = check_left_and_right_additivity(&rule, &a1, &a2, &b1, &b2)?;
    let c = GaussianRat::from_rational(rq(3, 5));
    let scale_ok = rule(&mx::scale(&a1, &c)?, &b1)? == mx::scale(&rule(&a1, &b1)?, &c)?;
    Ok(add_ok && scale_ok)
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

fn conjugated_kronecker(
    w: &BasicMatrix<GaussianRat>,
    a: &BasicMatrix<GaussianRat>,
    b: &BasicMatrix<GaussianRat>,
) -> Result<BasicMatrix<GaussianRat>, ExactFieldError> {
    mx::multiply(&mx::multiply(w, &mx::kronecker(a, b)?)?, w)
}

fn trace_split_bilinear_rule(
    a: &BasicMatrix<GaussianRat>,
    b: &BasicMatrix<GaussianRat>,
) -> Result<BasicMatrix<GaussianRat>, ExactFieldError> {
    let id2 = pauli_mat(omega_lie_theory::pauli_symplectic::Pauli::Identity);
    let id4 = mx::identity(4)?;
    let half = GaussianRat::from_rational(rq(1, 2));
    let quarter = GaussianRat::from_rational(rq(1, 4));
    let tr_a = mx::trace(a)?;
    let tr_b = mx::trace(b)?;
    let term1 = mx::scale(&mx::kronecker(&id2, b)?, &tr_a.mul(&half))?;
    let term2 = mx::scale(&mx::kronecker(a, &id2)?, &tr_b.mul(&half))?;
    let term3 = mx::scale(&id4, &tr_a.mul(&tr_b).mul(&quarter))?;
    mx::sub(&mx::add(&term1, &term2)?, &term3)
}

fn build_rival_candidates() -> Result<Vec<RivalCandidate>, RivalSearchError> {
    use omega_lie_theory::pauli_symplectic::Pauli;
    let w_z = mx::kronecker(&pauli_mat(Pauli::Z), &pauli_mat(Pauli::Identity))?;
    let w_cnot = cnot_matrix();
    let w_cz = cz_matrix();
    Ok(vec![
        RivalCandidate {
            name: "twisted_z_product",
            rule: Box::new(move |a, b| conjugated_kronecker(&w_z, a, b)),
            is_twisted: true,
            commutes_one_factor_only: true,
        },
        RivalCandidate {
            name: "cnot_twisted_product",
            rule: Box::new(move |a, b| conjugated_kronecker(&w_cnot, a, b)),
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
            rule: Box::new(move |a, b| conjugated_kronecker(&w_cz, a, b)),
            is_twisted: true,
            commutes_one_factor_only: false,
        },
        RivalCandidate {
            name: "trace_split_bilinear",
            rule: Box::new(trace_split_bilinear_rule),
            is_twisted: false,
            commutes_one_factor_only: false,
        },
    ])
}

fn reconstruct_bob_marginal(
    r: &RivalCandidate,
    id2: &BasicMatrix<GaussianRat>,
    paulis: &[BasicMatrix<GaussianRat>; 4],
    state: &BasicMatrix<GaussianRat>,
) -> Result<BasicMatrix<GaussianRat>, ExactFieldError> {
    let half = GaussianRat::from_rational(rq(1, 2));
    let mut marginal = mx::zeros(2, 2)?;
    for sigma in paulis {
        let obs = (r.rule)(id2, sigma)?;
        let coeff = mx::trace(&mx::multiply(&obs, state)?)?.mul(&half);
        marginal = mx::add(&marginal, &mx::scale(sigma, &coeff)?)?;
    }
    Ok(marginal)
}

fn apply_alice_unitary(
    r: &RivalCandidate,
    u: &BasicMatrix<GaussianRat>,
    id2: &BasicMatrix<GaussianRat>,
    rho: &BasicMatrix<GaussianRat>,
) -> Result<BasicMatrix<GaussianRat>, ExactFieldError> {
    let joint = if r.is_twisted {
        (r.rule)(u, id2)?
    } else {
        mx::kronecker(u, id2)?
    };
    mx::multiply(&mx::multiply(&joint, rho)?, &star::adjoint(&joint)?)
}

fn rival_signals_on_state(
    r: &RivalCandidate,
    id2: &BasicMatrix<GaussianRat>,
    paulis: &[BasicMatrix<GaussianRat>; 4],
    rho: &BasicMatrix<GaussianRat>,
) -> Result<bool, ExactFieldError> {
    use omega_lie_theory::pauli_symplectic::Pauli;
    let before = reconstruct_bob_marginal(r, id2, paulis, rho)?;
    for u in [&pauli_mat(Pauli::X), &pauli_mat(Pauli::Z)] {
        let post = apply_alice_unitary(r, u, id2, rho)?;
        let after = reconstruct_bob_marginal(r, id2, paulis, &post)?;
        if after != before {
            return Ok(true);
        }
    }
    Ok(false)
}

fn evaluate_rival_candidate(
    r: &RivalCandidate,
    id2: &BasicMatrix<GaussianRat>,
    id4: &BasicMatrix<GaussianRat>,
    paulis: &[BasicMatrix<GaussianRat>; 4],
) -> Result<bool, RivalSearchError> {
    if !verify_bilinearity(&r.rule)? || &(r.rule)(id2, id2)? != id4 {
        return Err(RivalSearchError::DeclaredLaw(r.name));
    }
    let mut signals = false;
    for (_, rho) in all_bell_states() {
        signals |= rival_signals_on_state(r, id2, paulis, &rho)?;
    }
    Ok(signals)
}

pub fn enumerate_rival_compositions() -> Result<(usize, bool), RivalSearchError> {
    use omega_lie_theory::pauli_symplectic::Pauli;
    let rivals = build_rival_candidates()?;
    let id2 = pauli_mat(Pauli::Identity);
    let id4 = mx::identity(4)?;
    let paulis = [
        pauli_mat(Pauli::Identity),
        pauli_mat(Pauli::X),
        pauli_mat(Pauli::Y),
        pauli_mat(Pauli::Z),
    ];
    let mut signalling_found = false;
    for r in &rivals {
        signalling_found |= evaluate_rival_candidate(r, &id2, &id4, &paulis)?;
    }
    Ok((rivals.len(), signalling_found))
}
