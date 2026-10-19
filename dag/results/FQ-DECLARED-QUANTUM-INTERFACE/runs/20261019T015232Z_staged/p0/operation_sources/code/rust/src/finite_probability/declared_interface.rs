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
pub fn certify(rho: Matrix, effect: Matrix, ks: Vec<Matrix>, u: Matrix) -> Result<Certificate> {
    for a in [&rho, &effect, &u].into_iter().chain(ks.iter()) {
        m::validate(a)?;
        if a.len() != 2 || a[0].len() != 2 {
            return Err("declared two-state matrices required");
        }
    }
    if ks.is_empty() {
        return Err("nonempty Kraus family required");
    }
    let identity = m::eye(2);
    if !m::is_psd(&rho)? || m::trace(&rho)? != Q::one() {
        return Err("positive trace-one state required");
    }
    if !m::is_psd(&effect)? || !m::is_psd(&m::add(&identity, &m::scale(&-Q::one(), &effect)?)?)? {
        return Err("effect between zero and identity required");
    }
    let mut completeness = m::scale(&Q::zero(), &identity)?;
    let mut channel = completeness.clone();
    for k in ks {
        let kt = m::transpose(&k)?;
        completeness = m::add(&completeness, &m::multiply(&kt, &k)?)?;
        channel = m::add(&channel, &m::multiply(&m::multiply(&k, &rho)?, &kt)?)?;
    }
    if completeness != identity {
        return Err("Kraus completeness required");
    }
    let utu = m::multiply(&m::transpose(&u)?, &u)?;
    if utu != identity {
        return Err("supplied unitary required");
    }
    let evolved = m::multiply(&m::multiply(&u, &rho)?, &m::transpose(&u)?)?;
    let tensor = m::tensor(&rho, &rho)?;
    let scalars = vec![
        m::trace(&m::multiply(&rho, &effect)?)?,
        m::trace(&rho)?,
        m::trace(&channel)?,
        m::trace(&evolved)?,
        m::trace(&tensor)?,
        m::trace(&m::multiply(&channel, &effect)?)?,
    ];
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
