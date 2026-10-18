use num_bigint::BigInt;
use num_rational::BigRational;

pub const PROVENANCE: &str = "Origin: research/four_wall_reconstruction_fable_receipt.json\nClaim: urn:tfqm:four-wall:principal-minor-three-fourths-times-minus-one-twelfth-is-minus-one-eighth\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum WallError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("denominator is zero for numerator {numer}")]
    ZeroDenominator { numer: i64 },
    #[error("product reading {by_product} disagrees with sixteenth reading {by_sixteenths}")]
    Readings { by_product: String, by_sixteenths: String },
    #[error("principal minor {value} is not -1/8")]
    Minor { value: String },
    #[error("kill counter overflowed at {killed}")]
    KillOverflow { killed: u32 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, WallError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn ratio(numer: i64, denom: i64) -> Result<BigRational, WallError> {
    if denom == 0 {
        return Err(WallError::ZeroDenominator { numer });
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}

pub fn product_reading() -> Result<BigRational, WallError> {
    let left = ratio(3, 4)?;
    let mid = ratio(-1, 12)?;
    let corner = ratio(1, 4)?;
    Ok((&left * &mid) - (&corner * &corner))
}

pub fn sixteenth_reading() -> Result<BigRational, WallError> {
    Ok(ratio(-1, 16)? - ratio(1, 16)?)
}

pub fn require_minor(by_product: &BigRational, by_sixteenths: &BigRational) -> Result<BigRational, WallError> {
    if by_product != by_sixteenths {
        return Err(WallError::Readings {
            by_product: by_product.to_string(),
            by_sixteenths: by_sixteenths.to_string(),
        });
    }
    let expected = ratio(-1, 8)?;
    if by_product != &expected {
        return Err(WallError::Minor {
            value: by_product.to_string(),
        });
    }
    Ok(by_product.clone())
}

pub fn verify() -> Result<BigRational, WallError> {
    let by_product = product_reading()?;
    let by_sixteenths = sixteenth_reading()?;
    require_minor(&by_product, &by_sixteenths)
}

pub fn executed_mutation_kills() -> Result<u32, WallError> {
    let killed = kill_if(0, drop_square_killed()?)?;
    let killed = kill_if(killed, add_sixteenths_killed()?)?;
    let killed = kill_if(killed, zero_denom_killed())?;
    equivalent_minor_matches()?;
    Ok(killed)
}

fn drop_square_killed() -> Result<bool, WallError> {
    let dropped = ratio(3, 4)? * ratio(-1, 12)?;
    Ok(dropped != verify()?)
}

fn add_sixteenths_killed() -> Result<bool, WallError> {
    let added = ratio(-1, 16)? + ratio(1, 16)?;
    Ok(added != verify()?)
}

fn zero_denom_killed() -> bool {
    ratio(3, 0).is_err()
}

fn equivalent_minor_matches() -> Result<(), WallError> {
    let oracle = verify()?;
    let again = require_minor(&ratio(-1, 8)?, &ratio(-1, 8)?)?;
    if again != oracle {
        return Err(WallError::Minor {
            value: again.to_string(),
        });
    }
    Ok(())
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, WallError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(WallError::KillOverflow { killed }),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn provenance_lists_authority() -> Result<(), String> {
        if PROVENANCE.contains("Origin:")
            && PROVENANCE.contains("Claim:")
            && PROVENANCE.contains("AuthorityEffect: None")
        {
            return Ok(());
        }
        Err(PROVENANCE.to_string())
    }

    #[test]
    fn unit_product_is_minus_one_eighth() -> Result<(), String> {
        let minor = product_reading().map_err(|err| err.to_string())?;
        if minor != ratio(-1, 8).map_err(|err| err.to_string())? {
            return Err(minor.to_string());
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_numerator_matches_minor() -> Result<(), String> {
        let admitted = admit_integer_token("-1").map_err(|err| err.to_string())?;
        let minor = verify().map_err(|err| err.to_string())?;
        let numer = i64::try_from(minor.numer()).map_err(|_| minor.to_string())?;
        if admitted != numer {
            return Err(minor.to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_minus_one_eighth() -> Result<(), String> {
        let minor = verify().map_err(|err| err.to_string())?;
        if minor != ratio(-1, 8).map_err(|err| err.to_string())? {
            return Err(minor.to_string());
        }
        Ok(())
    }

    #[test]
    fn negative_zero_denominator() -> Result<(), String> {
        match ratio(3, 0) {
            Err(WallError::ZeroDenominator { numer }) if numer == 3 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_readings() -> Result<(), String> {
        let product = ratio(-1, 16).map_err(|err| err.to_string())?;
        let other = ratio(0, 1).map_err(|err| err.to_string())?;
        match require_minor(&product, &other) {
            Err(WallError::Readings {
                by_product,
                by_sixteenths,
            }) if by_product == "-1/16" && by_sixteenths == "0" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_minor() -> Result<(), String> {
        let sixteenth = ratio(-1, 16).map_err(|err| err.to_string())?;
        match require_minor(&sixteenth, &sixteenth) {
            Err(WallError::Minor { value }) if value == "-1/16" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(WallError::Token(crate::qm::exact_token::TokenError::FloatRefused { token }))
                if token == "1.5" =>
            {
                Ok(())
            }
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_kill_overflow() -> Result<(), String> {
        match kill_if(u32::MAX, true) {
            Err(WallError::KillOverflow { killed }) if killed == u32::MAX => Ok(()),
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
