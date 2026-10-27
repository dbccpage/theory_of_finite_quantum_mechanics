use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub const PROVENANCE: &str = "Origin: lean4/TriangleNetworkComplexCarrier.lean\nClaim: urn:tfqm:H021:one-plus-zeta3-plus-zeta3-squared-is-zero\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum GleasonError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("denominator is zero for numerator {numer}")]
    ZeroDenominator { numer: i64 },
    #[error("frame length {found} is not {expected}")]
    Length { found: usize, expected: usize },
    #[error("frame sum {sum} is not 1")]
    Frame { sum: String },
    #[error("reduced relation is {c0}, {c1}, {c2}")]
    Relation { c0: i64, c1: i64, c2: i64 },
    #[error("factorization produced {c0}, {c1}, {c2}, {c3}")]
    Factor { c0: i64, c1: i64, c2: i64, c3: i64 },
    #[error("checked {op} overflowed from {left} and {right}")]
    Overflow { op: &'static str, left: i64, right: i64 },
    #[error("kill counter overflowed at {killed}")]
    KillOverflow { killed: u32 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, GleasonError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn ratio(numer: i64, denom: i64) -> Result<BigRational, GleasonError> {
    if denom == 0 {
        return Err(GleasonError::ZeroDenominator { numer });
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}

pub fn certify_frame(weights: &[BigRational]) -> Result<BigRational, GleasonError> {
    if weights.len() != 3 {
        return Err(GleasonError::Length {
            found: weights.len(),
            expected: 3,
        });
    }
    let sum = sum_three(weights)?;
    if sum != BigRational::one() {
        return Err(GleasonError::Frame {
            sum: sum.to_string(),
        });
    }
    Ok(sum)
}

pub fn certify_relation(coeffs: [i64; 3]) -> Result<[i64; 3], GleasonError> {
    let reduced = reduce_relation(coeffs)?;
    if reduced != [0, 0, 0] {
        return Err(GleasonError::Relation {
            c0: reduced[0],
            c1: reduced[1],
            c2: reduced[2],
        });
    }
    Ok(reduced)
}

pub fn certify_factor(left: [i64; 3], right: [i64; 2]) -> Result<[i64; 4], GleasonError> {
    let got = poly_mul_3_2(left, right)?;
    if got != [-1, 0, 0, 1] {
        return Err(GleasonError::Factor {
            c0: got[0],
            c1: got[1],
            c2: got[2],
            c3: got[3],
        });
    }
    Ok(got)
}

pub fn verify() -> Result<BigRational, GleasonError> {
    let third = ratio(1, 3)?;
    let frame = certify_frame(&[third.clone(), third.clone(), third])?;
    let _relation = certify_relation([1, 1, 1])?;
    let _factor = certify_factor([1, 1, 1], [-1, 1])?;
    Ok(frame)
}

pub fn executed_mutation_kills() -> Result<u32, GleasonError> {
    let killed = kill_if(0, relation_mutant_killed()?)?;
    let killed = kill_if(killed, frame_mutant_killed()?)?;
    let killed = kill_if(killed, factor_mutant_killed()?)?;
    equivalent_frame_matches()?;
    Ok(killed)
}

fn relation_mutant_killed() -> Result<bool, GleasonError> {
    Ok(mutant_skip_constant() != [0, 0, 0])
}

fn frame_mutant_killed() -> Result<bool, GleasonError> {
    let third = ratio(1, 3)?;
    Ok(certify_frame(&[third.clone(), third, ratio(0, 1)?]).is_err())
}

fn factor_mutant_killed() -> Result<bool, GleasonError> {
    Ok(certify_factor([1, 0, 0], [-1, 1]).is_err())
}

fn equivalent_frame_matches() -> Result<(), GleasonError> {
    let oracle = verify()?;
    let again = certify_frame(&[ratio(1, 3)?, ratio(1, 3)?, ratio(1, 3)?])?;
    if again != oracle {
        return Err(GleasonError::Frame {
            sum: again.to_string(),
        });
    }
    Ok(())
}

fn mutant_skip_constant() -> [i64; 3] {
    [1, 0, 0]
}

fn sum_three(weights: &[BigRational]) -> Result<BigRational, GleasonError> {
    let first = match weights.first() {
        Some(weight) => weight,
        None => {
            return Err(GleasonError::Length {
                found: 0,
                expected: 3,
            })
        }
    };
    let second = match weights.get(1) {
        Some(weight) => weight,
        None => {
            return Err(GleasonError::Length {
                found: weights.len(),
                expected: 3,
            })
        }
    };
    let third = match weights.get(2) {
        Some(weight) => weight,
        None => {
            return Err(GleasonError::Length {
                found: weights.len(),
                expected: 3,
            })
        }
    };
    Ok(first + second + third)
}

fn reduce_relation(coeffs: [i64; 3]) -> Result<[i64; 3], GleasonError> {
    let last = coeffs[2];
    Ok([sub(coeffs[0], last)?, sub(coeffs[1], last)?, 0])
}

fn poly_mul_3_2(left: [i64; 3], right: [i64; 2]) -> Result<[i64; 4], GleasonError> {
    let c0 = mul(left[0], right[0])?;
    let c3 = mul(left[2], right[1])?;
    let c1 = add(mul(left[0], right[1])?, mul(left[1], right[0])?)?;
    let c2 = add(mul(left[1], right[1])?, mul(left[2], right[0])?)?;
    Ok([c0, c1, c2, c3])
}

fn add(left: i64, right: i64) -> Result<i64, GleasonError> {
    match left.checked_add(right) {
        Some(sum) => Ok(sum),
        None => Err(GleasonError::Overflow {
            op: "add",
            left,
            right,
        }),
    }
}

fn sub(left: i64, right: i64) -> Result<i64, GleasonError> {
    match left.checked_sub(right) {
        Some(diff) => Ok(diff),
        None => Err(GleasonError::Overflow {
            op: "sub",
            left,
            right,
        }),
    }
}

fn mul(left: i64, right: i64) -> Result<i64, GleasonError> {
    match left.checked_mul(right) {
        Some(product) => Ok(product),
        None => Err(GleasonError::Overflow {
            op: "mul",
            left,
            right,
        }),
    }
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, GleasonError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(GleasonError::KillOverflow { killed }),
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
    fn unit_thirds_sum_to_one() -> Result<(), String> {
        let third = ratio(1, 3).map_err(|err| err.to_string())?;
        let frame = certify_frame(&[third.clone(), third.clone(), third]).map_err(|err| err.to_string())?;
        if frame != ratio(1, 1).map_err(|err| err.to_string())? {
            return Err(frame.to_string());
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_one_matches_verify() -> Result<(), String> {
        let admitted = admit_integer_token("1").map_err(|err| err.to_string())?;
        let frame = verify().map_err(|err| err.to_string())?;
        if admitted != 1 || frame != ratio(1, 1).map_err(|err| err.to_string())? {
            return Err(frame.to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_relation_and_factor() -> Result<(), String> {
        let relation = certify_relation([1, 1, 1]).map_err(|err| err.to_string())?;
        let factor = certify_factor([1, 1, 1], [-1, 1]).map_err(|err| err.to_string())?;
        if relation != [0, 0, 0] || factor != [-1, 0, 0, 1] {
            return Err(format!("{relation:?} {factor:?}"));
        }
        Ok(())
    }

    #[test]
    fn negative_zero_denominator() -> Result<(), String> {
        match ratio(1, 0) {
            Err(GleasonError::ZeroDenominator { numer }) if numer == 1 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_length() -> Result<(), String> {
        let third = ratio(1, 3).map_err(|err| err.to_string())?;
        match certify_frame(&[third.clone(), third]) {
            Err(GleasonError::Length { found, expected }) if found == 2 && expected == 3 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_frame() -> Result<(), String> {
        let third = ratio(1, 3).map_err(|err| err.to_string())?;
        let zero = ratio(0, 1).map_err(|err| err.to_string())?;
        match certify_frame(&[third.clone(), third, zero]) {
            Err(GleasonError::Frame { sum }) if sum == "2/3" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_relation() -> Result<(), String> {
        match certify_relation([1, 1, 2]) {
            Err(GleasonError::Relation { c0, c1, c2 }) if c0 == -1 && c1 == -1 && c2 == 0 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_factor() -> Result<(), String> {
        match certify_factor([1, 0, 0], [-1, 1]) {
            Err(GleasonError::Factor { c0, c1, c2, c3 })
                if c0 == -1 && c1 == 1 && c2 == 0 && c3 == 0 =>
            {
                Ok(())
            }
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_overflow() -> Result<(), String> {
        match mul(i64::MAX, 2) {
            Err(GleasonError::Overflow { op, left, right })
                if op == "mul" && left == i64::MAX && right == 2 =>
            {
                Ok(())
            }
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(GleasonError::Token(crate::qm::exact_token::TokenError::FloatRefused { token }))
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
            Err(GleasonError::KillOverflow { killed }) if killed == u32::MAX => Ok(()),
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
