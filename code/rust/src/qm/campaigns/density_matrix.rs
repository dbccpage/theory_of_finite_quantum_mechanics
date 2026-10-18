use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};

pub const PROVENANCE: &str = "Origin: papers/foundations/qm_012_density_matrices_as_diagonal_residual_weights.md\nClaim: urn:tfqm:OMEGA-QM-DIAG-DENSITY-038:two-by-two-trace-one-purity\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum DensityError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("denominator is zero for numerator {numer}")]
    ZeroDenominator { numer: i64 },
    #[error("trace {trace} is not 1")]
    TraceNotOne { trace: String },
    #[error("determinant {det} is not positive")]
    NotPositive { det: String },
    #[error("purity readings {by_entries} and {by_spectrum} disagree")]
    ReadingsDisagree { by_entries: String, by_spectrum: String },
}

pub fn admit_integer_token(token: &str) -> Result<i64, DensityError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn ratio(numer: i64, denom: i64) -> Result<BigRational, DensityError> {
    if denom == 0 {
        return Err(DensityError::ZeroDenominator { numer });
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}

pub fn determinant(a: &BigRational, b: &BigRational) -> BigRational {
    a * a - b * b
}

pub fn verify() -> Result<BigRational, DensityError> {
    certify_state(&ratio(1, 2)?, &ratio(1, 6)?)
}

pub fn certify_state(a: &BigRational, b: &BigRational) -> Result<BigRational, DensityError> {
    let trace = a + a;
    if trace != BigRational::one() {
        return Err(DensityError::TraceNotOne {
            trace: trace.to_string(),
        });
    }
    let det = determinant(a, b);
    if det <= BigRational::zero() {
        return Err(DensityError::NotPositive {
            det: det.to_string(),
        });
    }
    let by_entries = a * a + b * b + b * b + a * a;
    let by_spectrum = &trace * &trace - ratio(2, 1)? * &det;
    require_readings(&by_entries, &by_spectrum)
}

pub fn require_readings(
    by_entries: &BigRational,
    by_spectrum: &BigRational,
) -> Result<BigRational, DensityError> {
    if by_entries != by_spectrum {
        return Err(DensityError::ReadingsDisagree {
            by_entries: by_entries.to_string(),
            by_spectrum: by_spectrum.to_string(),
        });
    }
    Ok(by_entries.clone())
}

pub fn executed_mutation_kills() -> Result<u32, DensityError> {
    let killed = kill_if(0, det_mutant_killed()?)?;
    let killed = kill_if(killed, singular_mutant_killed()?)?;
    let killed = kill_if(killed, trace_mutant_killed()?)?;
    equivalent_state_matches()?;
    Ok(killed)
}

fn det_mutant_killed() -> Result<bool, DensityError> {
    Ok(mutant_drop_det_term()? != verify()?)
}

fn singular_mutant_killed() -> Result<bool, DensityError> {
    let half = ratio(1, 2)?;
    Ok(certify_state(&half, &half).is_err())
}

fn trace_mutant_killed() -> Result<bool, DensityError> {
    Ok(certify_state(&ratio(1, 3)?, &ratio(0, 1)?).is_err())
}

fn equivalent_state_matches() -> Result<(), DensityError> {
    let oracle = verify()?;
    let again = certify_state(&ratio(1, 2)?, &ratio(1, 6)?)?;
    if again != oracle {
        return Err(DensityError::ReadingsDisagree {
            by_entries: oracle.to_string(),
            by_spectrum: again.to_string(),
        });
    }
    Ok(())
}

fn mutant_drop_det_term() -> Result<BigRational, DensityError> {
    let trace = ratio(1, 1)?;
    Ok(&trace * &trace)
}

fn kill_overflow() -> DensityError {
    DensityError::Token(crate::qm::exact_token::TokenError::Overflow {
        token: "kills".to_string(),
    })
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, DensityError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(kill_overflow()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn oracle() -> Result<BigRational, String> {
        ratio(5, 9).map_err(|err| err.to_string())
    }

    #[test]
    fn unit_determinant_of_the_witness_is_two_ninths() -> Result<(), String> {
        let det = determinant(&ratio(1, 2).map_err(|err| err.to_string())?, &ratio(1, 6).map_err(|err| err.to_string())?);
        let expected = ratio(2, 9).map_err(|err| err.to_string())?;
        if det != expected {
            return Err(format!("det {det}"));
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_tokens_match_purity() -> Result<(), String> {
        let numer = admit_integer_token("5").map_err(|err| err.to_string())?;
        let denom = admit_integer_token("9").map_err(|err| err.to_string())?;
        let expected = ratio(numer, denom).map_err(|err| err.to_string())?;
        let purity = verify().map_err(|err| err.to_string())?;
        if purity != expected {
            return Err(format!("purity {purity} expected {expected}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_five_ninths() -> Result<(), String> {
        let purity = verify().map_err(|err| err.to_string())?;
        if purity != oracle()? {
            return Err(format!("purity {purity}"));
        }
        Ok(())
    }

    #[test]
    fn negative_zero_denominator() -> Result<(), String> {
        match ratio(1, 0) {
            Err(DensityError::ZeroDenominator { numer }) if numer == 1 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_trace() -> Result<(), String> {
        match certify_state(&ratio(1, 3).map_err(|err| err.to_string())?, &ratio(0, 1).map_err(|err| err.to_string())?) {
            Err(DensityError::TraceNotOne { trace }) if trace == "2/3" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_determinant() -> Result<(), String> {
        match certify_state(&ratio(1, 2).map_err(|err| err.to_string())?, &ratio(1, 2).map_err(|err| err.to_string())?) {
            Err(DensityError::NotPositive { det }) if det == "0" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_readings() -> Result<(), String> {
        match require_readings(&ratio(1, 2).map_err(|err| err.to_string())?, &ratio(1, 3).map_err(|err| err.to_string())?) {
            Err(DensityError::ReadingsDisagree { .. }) => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(DensityError::Token(crate::qm::exact_token::TokenError::FloatRefused { token })) if token == "1.5" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn mutation_record_matches_execution() -> Result<(), String> {
        let killed = executed_mutation_kills().map_err(|err| err.to_string())?;
        let marked = format!("killed={killed}");
        if MUTATION_KILL_RECORD != marked {
            return Err(format!("record {MUTATION_KILL_RECORD} executed {marked}"));
        }
        Ok(())
    }
}
