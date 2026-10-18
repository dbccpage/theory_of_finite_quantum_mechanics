use crate::cyclotomic_field::{CyclotomicError, CyclotomicNumber};
use crate::rational::Rational;
use num_integer::Integer;
use num_traits::{ToPrimitive, Zero};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum RationalTurnError {
    #[error("root order must be strictly positive")]
    ZeroRootOrder,
    #[error("turn denominator does not divide the declared conductor")]
    IncompatibleConductor,
    #[error("exact cyclotomic evaluation refused: {0}")]
    Cyclotomic(#[from] CyclotomicError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RationalTurn {
    fraction: Rational,
}
impl RationalTurn {
    pub fn new(turn: Rational) -> Self {
        Self {
            fraction: Rational::new(turn.numer().mod_floor(turn.denom()), turn.denom().clone()),
        }
    }
    pub fn zero() -> Self {
        Self::new(Rational::zero())
    }
    pub fn representative(&self) -> &Rational {
        &self.fraction
    }
    pub fn add(&self, other: &Self) -> Self {
        Self::new(&self.fraction + &other.fraction)
    }
    pub fn inverse(&self) -> Self {
        Self::new(-&self.fraction)
    }
    pub fn sub(&self, other: &Self) -> Self {
        self.add(&other.inverse())
    }
    pub fn multiply_integer(&self, n: &num_bigint::BigInt) -> Self {
        Self::new(&self.fraction * Rational::from_integer(n.clone()))
    }
    pub fn root(&self, order: usize) -> Result<Self, RationalTurnError> {
        if order == 0 {
            return Err(RationalTurnError::ZeroRootOrder);
        }
        Ok(Self::new(
            &self.fraction / Rational::from_integer(order.into()),
        ))
    }
    pub fn character_in(&self, conductor: usize) -> Result<CyclotomicNumber, RationalTurnError> {
        let one = CyclotomicNumber::one(conductor)?;
        let Some(denominator) = self.fraction.denom().to_usize() else {
            return Err(RationalTurnError::IncompatibleConductor);
        };
        if conductor % denominator != 0 {
            return Err(RationalTurnError::IncompatibleConductor);
        }
        if self.fraction.is_zero() {
            return Ok(one);
        }
        let numerator = self
            .fraction
            .numer()
            .to_usize()
            .ok_or(RationalTurnError::IncompatibleConductor)?;
        let exponent = numerator * (conductor / denominator);
        Ok(CyclotomicNumber::zeta(conductor, exponent as i64)?)
    }
    pub fn character(&self) -> Result<CyclotomicNumber, RationalTurnError> {
        let denominator = self
            .fraction
            .denom()
            .to_usize()
            .ok_or(RationalTurnError::IncompatibleConductor)?;
        self.character_in(denominator)
    }
}
