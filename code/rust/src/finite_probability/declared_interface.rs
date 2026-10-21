//! Real-rational subcase of an admitted quantum interface, not a reconstruction.
use super::pfp_exact::{self as m, Matrix, Result};
use num_rational::BigRational as Q;
use num_traits::{One, Zero};
pub const SLOTS: [&str; 8] = [
    "scalar_field",
    "inner_product",
    "positive_states_and_effects",
    "Born_trace",
    "tensor",
    "channels",
    "unitary_step_and_time",
    "observer_records",
];
pub struct Certificate {
    pub matrices: Vec<Matrix>,
    pub scalars: Vec<Q>,
}
fn validate_matrix_dimensions(matrices: &[&Matrix]) -> Result<()> {
    for a in matrices {
        m::validate(a)?;
        if a.len() != 2 || a[0].len() != 2 {
            return Err("declared two-state matrices required");
        }
    }
    Ok(())
}

fn validate_state(rho: &Matrix) -> Result<()> {
    if !m::is_psd(rho)? || m::trace(rho)? != Q::one() {
        return Err("positive trace-one state required");
    }
    Ok(())
}

fn validate_effect(effect: &Matrix, identity: &Matrix) -> Result<()> {
    let scaled = m::scale(&-Q::one(), effect)?;
    let diff = m::add(identity, &scaled)?;
    if !m::is_psd(effect)? || !m::is_psd(&diff)? {
        return Err("effect between zero and identity required");
    }
    Ok(())
}

fn kraus_step(
    k: &Matrix,
    rho: &Matrix,
    completeness: &mut Matrix,
    channel: &mut Matrix,
) -> Result<()> {
    let kt = m::transpose(k)?;
    let kt_k = m::multiply(&kt, k)?;
    *completeness = m::add(completeness, &kt_k)?;
    let k_rho = m::multiply(k, rho)?;
    let k_rho_kt = m::multiply(&k_rho, &kt)?;
    *channel = m::add(channel, &k_rho_kt)?;
    Ok(())
}

fn accumulate_kraus_channel(
    ks: &[Matrix],
    rho: &Matrix,
    identity: &Matrix,
) -> Result<(Matrix, Matrix)> {
    if ks.is_empty() {
        return Err("nonempty Kraus family required");
    }
    let mut completeness = m::scale(&Q::zero(), identity)?;
    let mut channel = completeness.clone();
    for k in ks {
        kraus_step(k, rho, &mut completeness, &mut channel)?;
    }
    if &completeness != identity {
        return Err("Kraus completeness required");
    }
    Ok((completeness, channel))
}

fn validate_unitary_step(u: &Matrix, identity: &Matrix) -> Result<Matrix> {
    let ut = m::transpose(u)?;
    let utu = m::multiply(&ut, u)?;
    if &utu != identity {
        return Err("supplied unitary required");
    }
    Ok(utu)
}

fn compute_certificate_scalars(
    rho: &Matrix,
    effect: &Matrix,
    channel: &Matrix,
    evolved: &Matrix,
    tensor: &Matrix,
) -> Result<Vec<Q>> {
    let rho_effect = m::multiply(rho, effect)?;
    let chan_effect = m::multiply(channel, effect)?;
    Ok(vec![
        m::trace(&rho_effect)?,
        m::trace(rho)?,
        m::trace(channel)?,
        m::trace(evolved)?,
        m::trace(tensor)?,
        m::trace(&chan_effect)?,
    ])
}

fn evolve_state(u: &Matrix, rho: &Matrix) -> Result<Matrix> {
    let u_rho = m::multiply(u, rho)?;
    let ut = m::transpose(u)?;
    m::multiply(&u_rho, &ut)
}

pub fn certify(rho: Matrix, effect: Matrix, ks: Vec<Matrix>, u: Matrix) -> Result<Certificate> {
    let mut all_matrices: Vec<&Matrix> = vec![&rho, &effect, &u];
    all_matrices.extend(ks.iter());
    validate_matrix_dimensions(&all_matrices)?;

    let identity = m::eye(2);
    validate_state(&rho)?;
    validate_effect(&effect, &identity)?;

    let (completeness, channel) = accumulate_kraus_channel(&ks, &rho, &identity)?;
    let utu = validate_unitary_step(&u, &identity)?;

    let evolved = evolve_state(&u, &rho)?;
    let tensor = m::tensor(&rho, &rho)?;

    let scalars = compute_certificate_scalars(&rho, &effect, &channel, &evolved, &tensor)?;

    Ok(Certificate {
        matrices: vec![rho, effect, completeness, channel, utu, evolved, tensor],
        scalars,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    fn half() -> Matrix {
        m::scale(&Q::new(1.into(), 2.into()), &m::eye(2)).unwrap()
    }
    #[test]
    fn actual_trace_and_Born() {
        let c = certify(half(), m::eye(2), vec![m::eye(2)], m::eye(2)).unwrap();
        assert_eq!(c.scalars, vec![Q::one(); 6]);
    }
    #[test]
    fn incomplete_channel_is_not_admitted() {
        assert!(certify(half(), m::eye(2), vec![half()], m::eye(2)).is_err());
    }
    #[test]
    fn invalid_effect_and_state_refused() {
        assert!(certify(m::eye(2), m::eye(2), vec![m::eye(2)], m::eye(2)).is_err());
        assert!(certify(
            half(),
            m::scale(&Q::from_integer(2.into()), &m::eye(2)).unwrap(),
            vec![m::eye(2)],
            m::eye(2)
        )
        .is_err());
    }
}
