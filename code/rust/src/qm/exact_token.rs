pub const PROVENANCE: &str = "Origin: papers/foundations/finite_ledger.md\nClaim: urn:tfqm:finite-ledger:integer-token-boundary\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum TokenError {
    #[error("float spelling refused at the integer boundary: {token}")]
    FloatRefused { token: String },
    #[error("token is not an optional sign followed by digits: {token}")]
    InvalidInteger { token: String },
    #[error("integer token overflowed i64: {token}")]
    Overflow { token: String },
    #[error("admitted value {value} did not round-trip through {token}")]
    RoundTrip { token: String, value: i64 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, TokenError> {
    if float_mark(token) {
        return Err(TokenError::FloatRefused {
            token: token.to_string(),
        });
    }
    parse_integer_token(token)
}

pub fn round_trip(token: &str) -> Result<i64, TokenError> {
    let value = admit_integer_token(token)?;
    let again = admit_integer_token(&value.to_string())?;
    if again != value {
        return Err(TokenError::RoundTrip {
            token: token.to_string(),
            value,
        });
    }
    Ok(value)
}

pub fn executed_mutation_kills() -> Result<u32, TokenError> {
    let oracle = admit_integer_token("10")?;
    let mut killed = 0u32;
    killed = kill_if(killed, dot_mutant_killed()?)?;
    killed = kill_if(killed, empty_mutant_killed()?)?;
    killed = kill_if(killed, ten_mutant_killed(oracle)?)?;
    if admit_integer_token("10")? != oracle {
        return Err(TokenError::RoundTrip {
            token: "10".to_string(),
            value: oracle,
        });
    }
    Ok(killed)
}

fn dot_mutant_killed() -> Result<bool, TokenError> {
    let stripped = mutant_strip_dot("1.5")?;
    Ok(stripped == 15 && admit_integer_token("1.5").is_err())
}

fn empty_mutant_killed() -> Result<bool, TokenError> {
    Ok(mutant_empty_is_zero("").ok() == Some(0) && admit_integer_token("").is_err())
}

fn ten_mutant_killed(oracle: i64) -> Result<bool, TokenError> {
    Ok(mutant_reject_ten("10").is_err() && oracle == 10)
}

fn float_mark(token: &str) -> bool {
    token.bytes().any(float_byte)
}

fn float_byte(byte: u8) -> bool {
    if byte == 46 {
        return true;
    }
    if byte == 101 {
        return true;
    }
    byte == 69
}

fn parse_integer_token(token: &str) -> Result<i64, TokenError> {
    let (negative, digits) = split_sign(token);
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(TokenError::InvalidInteger {
            token: token.to_string(),
        });
    }
    accumulate_digits(digits, negative, token)
}

fn split_sign(token: &str) -> (bool, &str) {
    match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    }
}

fn overflow_token(token: &str) -> TokenError {
    TokenError::Overflow {
        token: token.to_string(),
    }
}

fn next_place(value: i64, digit: i64) -> Option<i64> {
    value.checked_mul(10).and_then(|place| place.checked_add(digit))
}

fn accumulate_digits(digits: &str, negative: bool, token: &str) -> Result<i64, TokenError> {
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = match next_place(value, digit) {
            Some(next) => next,
            None => return Err(overflow_token(token)),
        };
    }
    if negative {
        value = match value.checked_neg() {
            Some(next) => next,
            None => return Err(overflow_token(token)),
        };
    }
    Ok(value)
}

fn mutant_strip_dot(token: &str) -> Result<i64, TokenError> {
    let cleaned: String = token.chars().filter(|ch| *ch != '.').collect();
    admit_integer_token(&cleaned)
}

fn mutant_empty_is_zero(token: &str) -> Result<i64, TokenError> {
    if token.is_empty() {
        Ok(0)
    } else {
        admit_integer_token(token)
    }
}

fn mutant_reject_ten(token: &str) -> Result<i64, TokenError> {
    if token == "10" {
        Err(TokenError::InvalidInteger {
            token: token.to_string(),
        })
    } else {
        admit_integer_token(token)
    }
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, TokenError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(overflow_token("kills")),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unit_round_trip_negative() -> Result<(), String> {
        let value = round_trip("-42").map_err(|err| err.to_string())?;
        if value != -42 {
            return Err(format!("value {value}"));
        }
        Ok(())
    }

    #[test]
    fn integration_neighbor_ratio_uses_admitted_digits() -> Result<(), String> {
        let numer = admit_integer_token("5").map_err(|err| err.to_string())?;
        let denom = admit_integer_token("9").map_err(|err| err.to_string())?;
        if numer != 5 || denom != 9 {
            return Err(format!("numer {numer} denom {denom}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_public_admission_of_zero() -> Result<(), String> {
        let value = admit_integer_token("0").map_err(|err| err.to_string())?;
        if value != 0 {
            return Err(format!("value {value}"));
        }
        Ok(())
    }

    #[test]
    fn negative_float_spelling() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(TokenError::FloatRefused { token }) if token == "1.5" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_exponent_spelling() -> Result<(), String> {
        match admit_integer_token("2e3") {
            Err(TokenError::FloatRefused { token }) if token == "2e3" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_invalid_integer() -> Result<(), String> {
        match admit_integer_token("12x") {
            Err(TokenError::InvalidInteger { token }) if token == "12x" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_overflow() -> Result<(), String> {
        match admit_integer_token("999999999999999999999") {
            Err(TokenError::Overflow { token }) if token == "999999999999999999999" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_round_trip_refuses_float() -> Result<(), String> {
        match round_trip("1.0") {
            Err(TokenError::FloatRefused { token }) if token == "1.0" => Ok(()),
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
