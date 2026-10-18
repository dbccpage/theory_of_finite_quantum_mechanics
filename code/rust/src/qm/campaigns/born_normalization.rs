use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub const PROVENANCE: &str = "Origin: papers/foundations/born_normalization.md\nClaim: urn:tfqm:born-normalization:two-weight-profile-trace-one-purity-one-half\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum BornNormError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("denominator is zero for numerator {numer}")]
    ZeroDenominator { numer: i64 },
    #[error("weight list length {found} is below {expected}")]
    Length { found: usize, expected: usize },
    #[error("trace {trace} is not 1")]
    TraceNotOne { trace: String },
    #[error("purity readings {by_entries} and {by_spectrum} disagree")]
    ReadingsDisagree { by_entries: String, by_spectrum: String },
    #[error("purity {purity} is not 1/2")]
    PurityNotHalf { purity: String },
}

pub fn admit_integer_token(token: &str) -> Result<i64, BornNormError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn ratio(numer: i64, denom: i64) -> Result<BigRational, BornNormError> {
    if denom == 0 {
        return Err(BornNormError::ZeroDenominator { numer });
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}

pub fn verify() -> Result<BigRational, BornNormError> {
    let half = ratio(1, 2)?;
    certify_weights(&[half.clone(), half])
}

pub fn certify_weights(weights: &[BigRational]) -> Result<BigRational, BornNormError> {
    if weights.len() < 2 {
        return Err(BornNormError::Length {
            found: weights.len(),
            expected: 2,
        });
    }
    let trace: BigRational = weights.iter().sum();
    if trace != BigRational::one() {
        return Err(BornNormError::TraceNotOne {
            trace: trace.to_string(),
        });
    }
    let by_entries = sum_squares(weights);
    let by_spectrum = pair_square(weights)?;
    if by_entries != by_spectrum {
        return Err(BornNormError::ReadingsDisagree {
            by_entries: by_entries.to_string(),
            by_spectrum: by_spectrum.to_string(),
        });
    }
    let half = ratio(1, 2)?;
    if by_entries != half {
        return Err(BornNormError::PurityNotHalf {
            purity: by_entries.to_string(),
        });
    }
    Ok(by_entries)
}

pub fn executed_mutation_kills() -> Result<u32, BornNormError> {
    let killed = kill_if(0, linear_mutant_killed()?)?;
    let killed = kill_if(killed, purity_mutant_killed()?)?;
    let killed = kill_if(killed, reading_mutant_killed()?)?;
    equivalent_profile_matches()?;
    Ok(killed)
}

fn linear_mutant_killed() -> Result<bool, BornNormError> {
    Ok(mutant_linear_profile()? != verify()?)
}

fn purity_mutant_killed() -> Result<bool, BornNormError> {
    let third = ratio(1, 3)?;
    let two_thirds = ratio(2, 3)?;
    Ok(certify_weights(&[third, two_thirds]).is_err())
}

fn reading_mutant_killed() -> Result<bool, BornNormError> {
    let half = ratio(1, 2)?;
    let zero = ratio(0, 1)?;
    Ok(certify_weights(&[half.clone(), zero, half]).is_err())
}

fn equivalent_profile_matches() -> Result<(), BornNormError> {
    let oracle = verify()?;
    let again = certify_weights(&[ratio(1, 2)?, ratio(1, 2)?])?;
    if again != oracle {
        return Err(BornNormError::PurityNotHalf {
            purity: oracle.to_string(),
        });
    }
    Ok(())
}

fn sum_squares(weights: &[BigRational]) -> BigRational {
    weights.iter().map(|weight| weight * weight).sum()
}

fn pair_square(weights: &[BigRational]) -> Result<BigRational, BornNormError> {
    let left = match weights.first() {
        Some(value) => value,
        None => {
            return Err(BornNormError::Length {
                found: 0,
                expected: 2,
            })
        }
    };
    let right = match weights.get(1) {
        Some(value) => value,
        None => {
            return Err(BornNormError::Length {
                found: weights.len(),
                expected: 2,
            })
        }
    };
    Ok(left * left + right * right)
}

fn mutant_linear_profile() -> Result<BigRational, BornNormError> {
    let half = ratio(1, 2)?;
    Ok(&half + &half)
}

fn kill_overflow() -> BornNormError {
    BornNormError::Token(crate::qm::exact_token::TokenError::Overflow {
        token: "kills".to_string(),
    })
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, BornNormError> {
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

    fn half() -> Result<BigRational, String> {
        ratio(1, 2).map_err(|err| err.to_string())
    }

    #[test]
    fn unit_two_halves_sum_to_one() -> Result<(), String> {
        let trace = half()? + half()?;
        if trace != BigRational::one() {
            return Err(format!("trace {trace}"));
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_tokens_match_purity() -> Result<(), String> {
        let numer = admit_integer_token("1").map_err(|err| err.to_string())?;
        let denom = admit_integer_token("2").map_err(|err| err.to_string())?;
        let weight = ratio(numer, denom).map_err(|err| err.to_string())?;
        let purity = verify().map_err(|err| err.to_string())?;
        if purity != weight {
            return Err(format!("purity {purity} weight {weight}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_one_half() -> Result<(), String> {
        let purity = verify().map_err(|err| err.to_string())?;
        if purity != half()? {
            return Err(format!("purity {purity}"));
        }
        Ok(())
    }

    #[test]
    fn negative_zero_denominator() -> Result<(), String> {
        match ratio(1, 0) {
            Err(BornNormError::ZeroDenominator { numer }) if numer == 1 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_short_weight_list() -> Result<(), String> {
        match certify_weights(&[half()?]) {
            Err(BornNormError::Length { found, expected }) if found == 1 && expected == 2 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_trace_not_one() -> Result<(), String> {
        let third = ratio(1, 3).map_err(|err| err.to_string())?;
        match certify_weights(&[third.clone(), third]) {
            Err(BornNormError::TraceNotOne { trace }) if trace == "2/3" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_readings_disagree() -> Result<(), String> {
        let half = half()?;
        let zero = ratio(0, 1).map_err(|err| err.to_string())?;
        match certify_weights(&[half.clone(), zero, half]) {
            Err(BornNormError::ReadingsDisagree { .. }) => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_purity_not_half() -> Result<(), String> {
        let third = ratio(1, 3).map_err(|err| err.to_string())?;
        let two_thirds = ratio(2, 3).map_err(|err| err.to_string())?;
        match certify_weights(&[third, two_thirds]) {
            Err(BornNormError::PurityNotHalf { purity }) if purity == "5/9" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(BornNormError::Token(crate::qm::exact_token::TokenError::FloatRefused { token }))
                if token == "1.5" =>
            {
                Ok(())
            }
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
