use num_rational::BigRational as Rational;
use num_traits::{One, Signed, Zero};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum CircleProfileError {
    #[error("circle profile needs 2..=65 ordered knots, from 0 to 1")]
    Knots,
    #[error("circle endpoint values must agree")]
    Periodicity,
    #[error("exact scalar must have a nonzero denominator and at most 256 input bits")]
    Scalar,
    #[error("uniform grid size must lie in 1..=256")]
    Grid,
}

fn canonical(value: Rational) -> Result<Rational, CircleProfileError> {
    if value.denom().is_zero() || value.numer().bits() > 256 || value.denom().bits() > 256 {
        return Err(CircleProfileError::Scalar);
    }
    Ok(value.reduced())
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CirclePiecewiseLinear {
    knots: Vec<(Rational, Rational)>,
    norm: Rational,
    lipschitz: Rational,
    square_integral: Rational,
}
impl CirclePiecewiseLinear {
    pub fn new(knots: Vec<(Rational, Rational)>) -> Result<Self, CircleProfileError> {
        if !(2..=65).contains(&knots.len()) {
            return Err(CircleProfileError::Knots);
        }
        let knots = knots
            .into_iter()
            .map(|(t, v)| Ok((canonical(t)?, canonical(v)?)))
            .collect::<Result<Vec<_>, CircleProfileError>>()?;
        if knots[0].0 != Rational::zero()
            || knots.last().unwrap().0 != Rational::one()
            || knots.windows(2).any(|w| w[0].0 >= w[1].0)
        {
            return Err(CircleProfileError::Knots);
        }
        if knots[0].1 != knots.last().unwrap().1 {
            return Err(CircleProfileError::Periodicity);
        }
        let norm = knots.iter().map(|(_, v)| v.abs()).max().unwrap();
        let mut lipschitz = Rational::zero();
        let mut square_integral = Rational::zero();
        for pair in knots.windows(2) {
            let (t0, v0) = &pair[0];
            let (t1, v1) = &pair[1];
            let width = t1 - t0;
            lipschitz = lipschitz.max((v1 - v0).abs() / &width);
            square_integral +=
                width * (v0 * v0 + v0 * v1 + v1 * v1) / Rational::from_integer(3.into());
        }
        Ok(Self {
            knots,
            norm,
            lipschitz,
            square_integral,
        })
    }
    pub fn knots(&self) -> &[(Rational, Rational)] {
        &self.knots
    }
    pub fn norm(&self) -> &Rational {
        &self.norm
    }
    pub fn lipschitz(&self) -> &Rational {
        &self.lipschitz
    }
    pub fn square_integral(&self) -> &Rational {
        &self.square_integral
    }
    pub fn evaluate(&self, turn: Rational) -> Result<Rational, CircleProfileError> {
        let turn = canonical(turn)?;
        let phase = &turn - turn.floor();
        let pair = self
            .knots
            .windows(2)
            .find(|w| w[0].0 <= phase && phase < w[1].0)
            .unwrap();
        let (t0, v0) = &pair[0];
        let (t1, v1) = &pair[1];
        Ok(v0 + (v1 - v0) * (phase - t0) / (t1 - t0))
    }
    pub fn uniform_samples(&self, nodes: usize) -> Result<Vec<Rational>, CircleProfileError> {
        if !(1..=256).contains(&nodes) {
            return Err(CircleProfileError::Grid);
        }
        (0..nodes)
            .map(|x| self.evaluate(Rational::new(x.into(), nodes.into())))
            .collect()
    }
}
