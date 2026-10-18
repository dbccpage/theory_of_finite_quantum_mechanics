use num_bigint::BigInt;
use num_rational::BigRational;

pub const PROVENANCE: &str = "Origin: papers/foundations/interference_as_the.md\nClaim: urn:tfqm:qm061:cross-term-2ab-on-three-fifths-minus-four-fifths\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum InterferenceError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("denominator is zero for numerator {numer}")]
    ZeroDenominator { numer: i64 },
    #[error("coherent {coherent} disagrees with expansion {expanded}")]
    Expansion { coherent: String, expanded: String },
    #[error("cross term vanished between {expanded} and {incoherent}")]
    CrossVanished { expanded: String, incoherent: String },
    #[error("cross term {cross} is not {expected}")]
    CrossMismatch { cross: String, expected: String },
}

pub fn admit_integer_token(token: &str) -> Result<i64, InterferenceError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn ratio(numer: i64, denom: i64) -> Result<BigRational, InterferenceError> {
    if denom == 0 {
        return Err(InterferenceError::ZeroDenominator { numer });
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}

pub fn verify() -> Result<BigRational, InterferenceError> {
    certify_pair(&ratio(3, 5)?, &ratio(-4, 5)?)
}

pub fn certify_pair(a: &BigRational, b: &BigRational) -> Result<BigRational, InterferenceError> {
    let coherent = (a + b) * (a + b);
    let expanded = a * a + b * b + ratio(2, 1)? * a * b;
    if coherent != expanded {
        return Err(InterferenceError::Expansion {
            coherent: coherent.to_string(),
            expanded: expanded.to_string(),
        });
    }
    let incoherent = a * a + b * b;
    if expanded == incoherent {
        return Err(InterferenceError::CrossVanished {
            expanded: expanded.to_string(),
            incoherent: incoherent.to_string(),
        });
    }
    let cross = &expanded - &incoherent;
    let expected = ratio(2, 1)? * a * b;
    require_cross(&cross, &expected)?;
    Ok(coherent)
}

pub fn require_cross(cross: &BigRational, expected: &BigRational) -> Result<(), InterferenceError> {
    if cross != expected {
        return Err(InterferenceError::CrossMismatch {
            cross: cross.to_string(),
            expected: expected.to_string(),
        });
    }
    Ok(())
}

pub fn require_expansion(coherent: &BigRational, expanded: &BigRational) -> Result<(), InterferenceError> {
    if coherent != expanded {
        return Err(InterferenceError::Expansion {
            coherent: coherent.to_string(),
            expanded: expanded.to_string(),
        });
    }
    Ok(())
}

pub fn executed_mutation_kills() -> Result<u32, InterferenceError> {
    let killed = kill_if(0, cross_mutant_killed()?)?;
    let killed = kill_if(killed, vanished_mutant_killed()?)?;
    let killed = kill_if(killed, expansion_mutant_killed()?)?;
    equivalent_pair_matches()?;
    Ok(killed)
}

fn cross_mutant_killed() -> Result<bool, InterferenceError> {
    Ok(mutant_drop_cross()? != verify()?)
}

fn vanished_mutant_killed() -> Result<bool, InterferenceError> {
    Ok(certify_pair(&ratio(1, 2)?, &ratio(0, 1)?).is_err())
}

fn expansion_mutant_killed() -> Result<bool, InterferenceError> {
    Ok(require_expansion(&ratio(1, 1)?, &ratio(1, 2)?).is_err())
}

fn equivalent_pair_matches() -> Result<(), InterferenceError> {
    let oracle = verify()?;
    let again = certify_pair(&ratio(3, 5)?, &ratio(-4, 5)?)?;
    if again != oracle {
        return Err(InterferenceError::CrossMismatch {
            cross: again.to_string(),
            expected: oracle.to_string(),
        });
    }
    Ok(())
}

fn mutant_drop_cross() -> Result<BigRational, InterferenceError> {
    let a = ratio(3, 5)?;
    let b = ratio(-4, 5)?;
    Ok(&a * &a + &b * &b)
}

fn kill_overflow() -> InterferenceError {
    InterferenceError::Token(crate::qm::exact_token::TokenError::Overflow {
        token: "kills".to_string(),
    })
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, InterferenceError> {
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
        ratio(1, 25).map_err(|err| err.to_string())
    }

    #[test]
    fn unit_cross_term_is_negative_twenty_four_over_twenty_five() -> Result<(), String> {
        let cross = ratio(2, 1).map_err(|err| err.to_string())?
            * ratio(3, 5).map_err(|err| err.to_string())?
            * ratio(-4, 5).map_err(|err| err.to_string())?;
        let expected = ratio(-24, 25).map_err(|err| err.to_string())?;
        if cross != expected {
            return Err(format!("cross {cross}"));
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_oracle() -> Result<(), String> {
        let numer = admit_integer_token("1").map_err(|err| err.to_string())?;
        let denom = admit_integer_token("25").map_err(|err| err.to_string())?;
        let expected = ratio(numer, denom).map_err(|err| err.to_string())?;
        let coherent = verify().map_err(|err| err.to_string())?;
        if coherent != expected {
            return Err(format!("coherent {coherent}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify() -> Result<(), String> {
        let coherent = verify().map_err(|err| err.to_string())?;
        if coherent != oracle()? {
            return Err(format!("coherent {coherent}"));
        }
        Ok(())
    }

    #[test]
    fn negative_zero_denominator() -> Result<(), String> {
        match ratio(3, 0) {
            Err(InterferenceError::ZeroDenominator { numer }) if numer == 3 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_expansion() -> Result<(), String> {
        match require_expansion(&ratio(1, 1).map_err(|err| err.to_string())?, &ratio(1, 2).map_err(|err| err.to_string())?) {
            Err(InterferenceError::Expansion { .. }) => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_cross_vanished() -> Result<(), String> {
        match certify_pair(&ratio(1, 2).map_err(|err| err.to_string())?, &ratio(0, 1).map_err(|err| err.to_string())?) {
            Err(InterferenceError::CrossVanished { .. }) => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_cross_mismatch() -> Result<(), String> {
        match require_cross(&ratio(1, 1).map_err(|err| err.to_string())?, &ratio(1, 2).map_err(|err| err.to_string())?) {
            Err(InterferenceError::CrossMismatch { .. }) => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("-2.0") {
            Err(InterferenceError::Token(crate::qm::exact_token::TokenError::FloatRefused { token })) if token == "-2.0" => Ok(()),
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
