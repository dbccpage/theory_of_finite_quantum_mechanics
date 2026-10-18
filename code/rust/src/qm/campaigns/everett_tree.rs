use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub const PROVENANCE: &str = "Origin: lean4/H053EverettForkingTree.lean\nClaim: urn:tfqm:H053:branch-weights-conserve-the-parent\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum EverettError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("denominator is zero for numerator {numer}")]
    ZeroDenominator { numer: i64 },
    #[error("leaf total {leaves} is not 1")]
    Leaves { leaves: String },
    #[error("right branch {right} does not restore parent {left}")]
    Parent { left: String, right: String },
}

pub fn admit_integer_token(token: &str) -> Result<i64, EverettError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn ratio(numer: i64, denom: i64) -> Result<BigRational, EverettError> {
    if denom == 0 {
        return Err(EverettError::ZeroDenominator { numer });
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}

pub fn verify() -> Result<BigRational, EverettError> {
    let half = ratio(1, 2)?;
    let right_a = &half * &ratio(1, 3)?;
    let right_b = &half * &ratio(2, 3)?;
    certify_branches(&half, &right_a, &right_b)
}

pub fn certify_branches(
    left: &BigRational,
    right_a: &BigRational,
    right_b: &BigRational,
) -> Result<BigRational, EverettError> {
    let leaves = left + right_a + right_b;
    if leaves != BigRational::one() {
        return Err(EverettError::Leaves {
            leaves: leaves.to_string(),
        });
    }
    let right = right_a + right_b;
    if right != *left {
        return Err(EverettError::Parent {
            left: left.to_string(),
            right: right.to_string(),
        });
    }
    Ok(leaves)
}

pub fn executed_mutation_kills() -> Result<u32, EverettError> {
    let killed = kill_if(0, dropped_leaf_killed()?)?;
    let killed = kill_if(killed, unbalanced_parent_killed()?)?;
    let killed = kill_if(killed, overweight_killed()?)?;
    equivalent_tree_matches()?;
    Ok(killed)
}

fn dropped_leaf_killed() -> Result<bool, EverettError> {
    let half = ratio(1, 2)?;
    let right_a = &half * &ratio(1, 3)?;
    Ok((&half + &right_a) != verify()?)
}

fn unbalanced_parent_killed() -> Result<bool, EverettError> {
    let third = ratio(1, 3)?;
    Ok(certify_branches(&third, &third, &third).is_err())
}

fn overweight_killed() -> Result<bool, EverettError> {
    let half = ratio(1, 2)?;
    Ok(certify_branches(&half, &half, &half).is_err())
}

fn equivalent_tree_matches() -> Result<(), EverettError> {
    let oracle = verify()?;
    let half = ratio(1, 2)?;
    let right_a = &half * &ratio(1, 3)?;
    let right_b = &half * &ratio(2, 3)?;
    let again = certify_branches(&half, &right_a, &right_b)?;
    if again != oracle {
        return Err(EverettError::Leaves {
            leaves: again.to_string(),
        });
    }
    Ok(())
}

fn kill_overflow() -> EverettError {
    EverettError::Token(crate::qm::exact_token::TokenError::Overflow {
        token: "kills".to_string(),
    })
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, EverettError> {
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
    fn unit_right_children_restore_half() -> Result<(), String> {
        let half = ratio(1, 2).map_err(|err| err.to_string())?;
        let right = &half * &ratio(1, 3).map_err(|err| err.to_string())? + &half * &ratio(2, 3).map_err(|err| err.to_string())?;
        if right != half {
            return Err(format!("right {right}"));
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_unit_leaf() -> Result<(), String> {
        let numer = admit_integer_token("1").map_err(|err| err.to_string())?;
        let denom = admit_integer_token("1").map_err(|err| err.to_string())?;
        let expected = ratio(numer, denom).map_err(|err| err.to_string())?;
        let leaves = verify().map_err(|err| err.to_string())?;
        if leaves != expected {
            return Err(format!("leaves {leaves}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_one() -> Result<(), String> {
        let leaves = verify().map_err(|err| err.to_string())?;
        if leaves != BigRational::one() {
            return Err(format!("leaves {leaves}"));
        }
        Ok(())
    }

    #[test]
    fn negative_zero_denominator() -> Result<(), String> {
        match ratio(1, 0) {
            Err(EverettError::ZeroDenominator { numer }) if numer == 1 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_leaves() -> Result<(), String> {
        let half = ratio(1, 2).map_err(|err| err.to_string())?;
        match certify_branches(&half, &half, &half) {
            Err(EverettError::Leaves { leaves }) if leaves == "3/2" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_parent() -> Result<(), String> {
        let third = ratio(1, 3).map_err(|err| err.to_string())?;
        match certify_branches(&third, &third, &third) {
            Err(EverettError::Parent { .. }) => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(EverettError::Token(crate::qm::exact_token::TokenError::FloatRefused { token })) if token == "1.5" => Ok(()),
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
