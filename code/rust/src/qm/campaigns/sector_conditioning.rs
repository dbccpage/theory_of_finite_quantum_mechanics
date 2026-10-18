//! Conditioning of the campaign's residual ledger using exact finite weights.
use super::residual_density::ResidualLedger;
use omega_number_theory::rational::Rational;
use omega_quantum_physics::sector_conditioning::{self, ConditioningError};
pub fn sector_probability(
    ledger: &ResidualLedger,
    sector: &[bool],
) -> Result<Rational, ConditioningError> {
    sector_conditioning::sector_weight_probability(ledger.masses(), sector)
}
pub fn condition(
    ledger: &ResidualLedger,
    sector: &[bool],
) -> Result<ResidualLedger, ConditioningError> {
    ResidualLedger::new(sector_conditioning::condition_weights(
        ledger.masses(),
        sector,
    )?)
    .map_err(|_| ConditioningError::InvalidWeights)
}
