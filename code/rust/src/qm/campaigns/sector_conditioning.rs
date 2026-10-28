use super::residual_density::ResidualLedger;
use num_traits::{One, Signed, Zero};
use engine_number_theory::rational::Rational;
use engine_quantum_physics::sector_conditioning::{self, ConditioningError};

pub fn sector_probability(
    ledger: &ResidualLedger,
    sector: &[bool],
) -> Result<Rational, ConditioningError> {
    let external = sector_conditioning::sector_weight_probability(ledger.masses(), sector)?;
    let local = local_probability(ledger.masses(), sector)?;
    if external != local {
        return Err(ConditioningError::InvalidWeights);
    }
    Ok(external)
}

pub fn condition(
    ledger: &ResidualLedger,
    sector: &[bool],
) -> Result<ResidualLedger, ConditioningError> {
    let external = sector_conditioning::condition_weights(ledger.masses(), sector)?;
    let local = local_condition(ledger.masses(), sector)?;
    if external != local {
        return Err(ConditioningError::InvalidWeights);
    }
    ResidualLedger::new(external).map_err(|_| ConditioningError::InvalidWeights)
}

fn local_probability(masses: &[Rational], sector: &[bool]) -> Result<Rational, ConditioningError> {
    let (weight, total) = sector_mass(masses, sector)?;
    Ok(weight / total)
}

fn local_condition(masses: &[Rational], sector: &[bool]) -> Result<Vec<Rational>, ConditioningError> {
    let (weight, _) = sector_mass(masses, sector)?;
    if weight.is_zero() {
        return Err(ConditioningError::NullSector);
    }
    let conditioned: Vec<Rational> = masses
        .iter()
        .zip(sector)
        .map(|(mass, inside)| {
            if *inside {
                mass / &weight
            } else {
                Rational::zero()
            }
        })
        .collect();
    let mut restored = Rational::zero();
    for (value, inside) in conditioned.iter().zip(sector) {
        if *inside {
            restored += value;
        } else if !value.is_zero() {
            return Err(ConditioningError::InvalidWeights);
        }
    }
    if restored != Rational::one() {
        return Err(ConditioningError::InvalidWeights);
    }
    Ok(conditioned)
}

fn sector_mass(
    masses: &[Rational],
    sector: &[bool],
) -> Result<(Rational, Rational), ConditioningError> {
    if sector.len() != masses.len() {
        return Err(ConditioningError::SectorLength {
            expected: masses.len(),
            actual: sector.len(),
        });
    }
    if masses.is_empty() || masses.iter().any(|mass| mass.is_negative()) {
        return Err(ConditioningError::InvalidWeights);
    }
    let total: Rational = masses.iter().cloned().sum();
    if total.is_zero() {
        return Err(ConditioningError::InvalidWeights);
    }
    let weight: Rational = masses
        .iter()
        .zip(sector)
        .filter(|(_, inside)| **inside)
        .map(|(mass, _)| mass.clone())
        .sum();
    Ok((weight, total))
}
