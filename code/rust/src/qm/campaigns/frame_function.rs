use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub const PROVENANCE: &str = "Origin: papers/derivations/21_implementation_core/tfq_0135_parity_contextuality_and_frame_functions.md\nClaim: urn:tfqm:TFQ-0135:two-frames-sum-to-one\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum FrameError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("denominator is zero for numerator {numer}")]
    ZeroDenominator { numer: i64 },
    #[error("frame sums {first} and {second} disagree")]
    FramesDisagree { first: String, second: String },
    #[error("shared frame sum {sum} is not 1")]
    FrameSum { sum: String },
}

pub fn admit_integer_token(token: &str) -> Result<i64, FrameError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn ratio(numer: i64, denom: i64) -> Result<BigRational, FrameError> {
    if denom == 0 {
        return Err(FrameError::ZeroDenominator { numer });
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}

pub fn verify() -> Result<BigRational, FrameError> {
    let first = [ratio(1, 2)?, ratio(1, 3)?, ratio(1, 6)?];
    let second = [ratio(1, 6)?, ratio(1, 2)?, ratio(1, 3)?];
    let by_rational: BigRational = first.iter().sum();
    let by_denominator = ratio(3 + 2 + 1, 6)?;
    let second_sum: BigRational = second.iter().sum();
    if by_rational != by_denominator {
        return Err(FrameError::FramesDisagree {
            first: by_rational.to_string(),
            second: by_denominator.to_string(),
        });
    }
    require_unit_frames(&by_rational, &second_sum)
}

pub fn require_unit_frames(first: &BigRational, second: &BigRational) -> Result<BigRational, FrameError> {
    if first != second {
        return Err(FrameError::FramesDisagree {
            first: first.to_string(),
            second: second.to_string(),
        });
    }
    if first != &BigRational::one() {
        return Err(FrameError::FrameSum {
            sum: first.to_string(),
        });
    }
    Ok(first.clone())
}

pub fn executed_mutation_kills() -> Result<u32, FrameError> {
    let killed = kill_if(0, sixth_mutant_killed()?)?;
    let killed = kill_if(killed, half_frame_mutant_killed()?)?;
    let killed = kill_if(killed, denominator_mutant_killed()?)?;
    equivalent_frame_matches()?;
    Ok(killed)
}

fn sixth_mutant_killed() -> Result<bool, FrameError> {
    Ok(mutant_drop_sixth()? != verify()?)
}

fn half_frame_mutant_killed() -> Result<bool, FrameError> {
    let half = ratio(1, 2)?;
    Ok(require_unit_frames(&half, &half).is_err())
}

fn denominator_mutant_killed() -> Result<bool, FrameError> {
    Ok(ratio(3 + 2 + 1, 5)? != verify()?)
}

fn equivalent_frame_matches() -> Result<(), FrameError> {
    let oracle = verify()?;
    let again = require_unit_frames(&oracle, &oracle)?;
    if again != oracle {
        return Err(FrameError::FrameSum {
            sum: oracle.to_string(),
        });
    }
    Ok(())
}

fn mutant_drop_sixth() -> Result<BigRational, FrameError> {
    Ok(ratio(1, 2)? + ratio(1, 3)?)
}

fn kill_overflow() -> FrameError {
    FrameError::Token(crate::qm::exact_token::TokenError::Overflow {
        token: "kills".to_string(),
    })
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, FrameError> {
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

    #[test]
    fn unit_denominator_form_is_one() -> Result<(), String> {
        let value = ratio(3 + 2 + 1, 6).map_err(|err| err.to_string())?;
        if value != BigRational::one() {
            return Err(format!("value {value}"));
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_one() -> Result<(), String> {
        let numer = admit_integer_token("1").map_err(|err| err.to_string())?;
        let denom = admit_integer_token("1").map_err(|err| err.to_string())?;
        let expected = ratio(numer, denom).map_err(|err| err.to_string())?;
        let frame = verify().map_err(|err| err.to_string())?;
        if frame != expected {
            return Err(format!("frame {frame}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_one() -> Result<(), String> {
        let frame = verify().map_err(|err| err.to_string())?;
        if frame != BigRational::one() {
            return Err(format!("frame {frame}"));
        }
        Ok(())
    }

    #[test]
    fn negative_zero_denominator() -> Result<(), String> {
        match ratio(1, 0) {
            Err(FrameError::ZeroDenominator { numer }) if numer == 1 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_frames_disagree() -> Result<(), String> {
        let one = ratio(1, 1).map_err(|err| err.to_string())?;
        let half = ratio(1, 2).map_err(|err| err.to_string())?;
        match require_unit_frames(&one, &half) {
            Err(FrameError::FramesDisagree { .. }) => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_frame_sum() -> Result<(), String> {
        let half = ratio(1, 2).map_err(|err| err.to_string())?;
        match require_unit_frames(&half, &half) {
            Err(FrameError::FrameSum { sum }) if sum == "1/2" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("2e3") {
            Err(FrameError::Token(crate::qm::exact_token::TokenError::FloatRefused { token })) if token == "2e3" => Ok(()),
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
