//! Integer-row divisibility obstruction and exact normalized indefinite readout.
use super::{
    cabello_certificates::quadratic,
    frame_polytope::FrameSystem,
    pfp_exact::{self as mx, Matrix, Result},
};
use num_bigint::BigInt;
use num_integer::Integer;
use num_rational::BigRational as Q;
use num_traits::{One, Zero};
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Parity {
    pub multipliers: Vec<i64>,
    pub coefficients: Vec<i64>,
    pub rhs: i64,
    pub divisor: i64,
    pub remainder: i64,
}
pub fn parity(frames: &[Vec<usize>], n: usize) -> Result<Parity> {
    if n == 0 || frames.is_empty() || frames.iter().flatten().any(|&i| i >= n) {
        return Err("nonempty declared integer incidence required");
    }
    let coefficients: Vec<i64> = (0..n)
        .map(|i| frames.iter().flatten().filter(|&&j| i == j).count() as i64)
        .collect();
    let divisor = coefficients.iter().fold(0i64, |g, x| g.gcd(x));
    if divisor == 0 {
        return Err("zero combined row needs separate contract");
    }
    let rhs = frames.len() as i64;
    Ok(Parity {
        multipliers: vec![1; frames.len()],
        coefficients,
        rhs,
        divisor,
        remainder: rhs % divisor,
    })
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Certificate {
    pub parity_main: Parity,
    pub denominator: Q,
    pub normalized_matrix: Matrix,
    pub weights: Vec<Q>,
    pub frame_sums: Vec<Q>,
    pub negative_vector: [i64; 4],
    pub raw_negative_value: Q,
    pub negative_value: Q,
    pub scaled_readout_remainders: Vec<BigInt>,
    pub even_control: Parity,
    pub even_assignment: Vec<i64>,
    pub even_context_sums: Vec<i64>,
}
pub fn certify(
    rays: Vec<Vec<i64>>,
    frames: Vec<Vec<usize>>,
    raw: Matrix,
    v: [i64; 4],
    even_frames: Vec<Vec<usize>>,
    even_assignment: Vec<i64>,
) -> Result<Certificate> {
    let system =
        FrameSystem::new(rays.clone(), frames.clone()).map_err(|_| "invalid orthogonal frames")?;
    if system.dimension() != 4 {
        return Err("dimension four required");
    }
    mx::validate(&raw)?;
    if raw.len() != 4
        || raw[0].len() != 4
        || raw != mx::transpose(&raw)?
        || raw.iter().flatten().any(|x| !x.denom().is_one())
    {
        return Err("integer symmetric four-matrix required");
    }
    let denominator = mx::trace(&raw)?;
    if denominator <= Q::zero() {
        return Err("positive trace required");
    }
    let h = mx::scale(&(Q::one() / &denominator), &raw)?;
    let mut weights = Vec::new();
    let mut remainders = Vec::new();
    for r in &rays {
        let vec: [i64; 4] = r.clone().try_into().map_err(|_| "ray shape")?;
        let norm: BigInt = r.iter().map(|x| BigInt::from(*x) * BigInt::from(*x)).sum();
        weights.push(quadratic(&h, &vec) / Q::from_integer(norm.clone()));
        let rawq = quadratic(&raw, &vec) * Q::from_integer(4.into());
        if !rawq.denom().is_one() {
            return Err("noninteger raw quadratic cannot be rounded");
        }
        remainders.push(rawq.to_integer() % norm);
    }
    let frame_sums: Vec<Q> = frames
        .iter()
        .map(|f| f.iter().map(|&i| weights[i].clone()).sum())
        .collect();
    if weights.iter().any(|x| x < &Q::zero() || x > &Q::one())
        || frame_sums.iter().any(|x| !x.is_one())
    {
        return Err("normalized nonnegative frame values required");
    }
    let negative_value = quadratic(&h, &v);
    if negative_value >= Q::zero() {
        return Err("negative quadratic witness required");
    }
    let even_control = parity(&even_frames, even_assignment.len())?;
    let sums: Vec<i64> = even_frames
        .iter()
        .map(|f| f.iter().map(|&i| even_assignment[i]).sum())
        .collect();
    if sums.iter().any(|&x| x != 1) {
        return Err("actual integer control assignment required");
    }
    Ok(Certificate {
        parity_main: parity(&frames, rays.len())?,
        denominator,
        normalized_matrix: h,
        weights,
        frame_sums,
        negative_vector: v,
        raw_negative_value: quadratic(&raw, &v),
        negative_value,
        scaled_readout_remainders: remainders,
        even_control,
        even_assignment,
        even_context_sums: sums,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn even_context_control_is_not_falsely_refused() {
        let p = parity(&[vec![0, 1, 2, 3], vec![0, 1, 2, 3]], 4).unwrap();
        assert_eq!(p.divisor, 2);
        assert_eq!(p.rhs, 2);
        assert_eq!(p.remainder, 0);
    }
    #[test]
    fn odd_degree_two_combination_has_a_real_divisibility_obstruction() {
        let p = parity(&[vec![0, 2], vec![0, 1], vec![1, 2]], 3).unwrap();
        assert_eq!(p.coefficients, vec![2, 2, 2]);
        assert_eq!(p.rhs, 3);
        assert_eq!(p.remainder, 1);
    }
    #[test]
    fn undeclared_indices_are_refused() {
        assert!(parity(&[vec![0, 4]], 4).is_err());
    }
}
