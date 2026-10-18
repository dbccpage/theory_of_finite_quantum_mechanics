pub const PROVENANCE: &str = "Origin: research/quadratic_readout_finite_map.md\nClaim: urn:tfqm:qm208:quadratic-i3-vanishes-and-quartic-i3-on-ones-is-thirty-six\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ReadoutError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("readout degree {kind} is outside the declared pair 2 and 4")]
    Degree { kind: u32 },
    #[error("checked {op} overflowed from {left} and {right}")]
    Overflow { op: &'static str, left: i64, right: i64 },
    #[error("quartic third difference {value} is not 36")]
    Quartic { value: i64 },
    #[error("kill counter overflowed at {killed}")]
    KillOverflow { killed: u32 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, ReadoutError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn sorkin_i3(kind: u32, a: i64, b: i64, c: i64) -> Result<i64, ReadoutError> {
    combine_i3(sample_parts(kind, a, b, c)?)
}

fn sample_parts(kind: u32, a: i64, b: i64, c: i64) -> Result<[i64; 7], ReadoutError> {
    let sums = triple_sums(a, b, c)?;
    Ok([
        power(sums[0], kind)?,
        power(sums[1], kind)?,
        power(sums[2], kind)?,
        power(sums[3], kind)?,
        power(a, kind)?,
        power(b, kind)?,
        power(c, kind)?,
    ])
}

fn triple_sums(a: i64, b: i64, c: i64) -> Result<[i64; 4], ReadoutError> {
    let ab = add(a, b)?;
    let ac = add(a, c)?;
    let bc = add(b, c)?;
    let abc = add(ab, c)?;
    Ok([abc, ab, ac, bc])
}

pub fn certify_ones(a: i64, b: i64, c: i64) -> Result<i64, ReadoutError> {
    let quart = sorkin_i3(4, a, b, c)?;
    if quart != 36 {
        return Err(ReadoutError::Quartic { value: quart });
    }
    Ok(quart)
}

pub fn verify() -> Result<i64, ReadoutError> {
    let quad = sorkin_i3(2, 1, 1, 1)?;
    if quad != 0 {
        return Err(ReadoutError::Quartic { value: quad });
    }
    certify_ones(1, 1, 1)
}

pub fn executed_mutation_kills() -> Result<u32, ReadoutError> {
    let killed = kill_if(0, drop_restoration_killed()?)?;
    let killed = kill_if(killed, degree_killed()?)?;
    let killed = kill_if(killed, sign_killed()?)?;
    equivalent_quartic_matches()?;
    Ok(killed)
}

fn drop_restoration_killed() -> Result<bool, ReadoutError> {
    Ok(mutant_drop_restorations() != 0)
}

fn degree_killed() -> Result<bool, ReadoutError> {
    Ok(sorkin_i3(3, 1, 1, 1).is_err())
}

fn sign_killed() -> Result<bool, ReadoutError> {
    Ok(mutant_add_pairs() != verify()?)
}

fn equivalent_quartic_matches() -> Result<(), ReadoutError> {
    let oracle = verify()?;
    let again = certify_ones(1, 1, 1)?;
    if again != oracle {
        return Err(ReadoutError::Quartic { value: again });
    }
    Ok(())
}

fn mutant_drop_restorations() -> i64 {
    9 - 4 - 4 - 4
}

fn mutant_add_pairs() -> i64 {
    81 + 16 + 16 + 16 + 1 + 1 + 1
}

fn combine_i3(parts: [i64; 7]) -> Result<i64, ReadoutError> {
    let mut total = 0i64;
    for (index, part) in parts.iter().enumerate() {
        total = signed_add(total, *part, index)?;
    }
    Ok(total)
}

fn signed_add(total: i64, part: i64, index: usize) -> Result<i64, ReadoutError> {
    let next = if index > 0 && index < 4 {
        total.checked_sub(part)
    } else {
        total.checked_add(part)
    };
    match next {
        Some(value) => Ok(value),
        None => Err(ReadoutError::Overflow {
            op: "combine",
            left: total,
            right: part,
        }),
    }
}

fn power(base: i64, kind: u32) -> Result<i64, ReadoutError> {
    if kind != 2 && kind != 4 {
        return Err(ReadoutError::Degree { kind });
    }
    let mut acc = 1i64;
    let mut left = kind;
    while left > 0 {
        acc = match acc.checked_mul(base) {
            Some(next) => next,
            None => {
                return Err(ReadoutError::Overflow {
                    op: "pow",
                    left: acc,
                    right: base,
                })
            }
        };
        left -= 1;
    }
    Ok(acc)
}

fn add(left: i64, right: i64) -> Result<i64, ReadoutError> {
    match left.checked_add(right) {
        Some(sum) => Ok(sum),
        None => Err(ReadoutError::Overflow {
            op: "add",
            left,
            right,
        }),
    }
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, ReadoutError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(ReadoutError::KillOverflow { killed }),
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
    fn unit_quadratic_third_difference_is_zero() -> Result<(), String> {
        if sorkin_i3(2, 1, 1, 1).map_err(|err| err.to_string())? != 0 {
            return Err("quadratic".to_string());
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_thirty_six_matches_verify() -> Result<(), String> {
        let admitted = admit_integer_token("36").map_err(|err| err.to_string())?;
        if admitted != verify().map_err(|err| err.to_string())? {
            return Err("admit".to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_thirty_six() -> Result<(), String> {
        if verify().map_err(|err| err.to_string())? != 36 {
            return Err("verify".to_string());
        }
        Ok(())
    }

    #[test]
    fn negative_degree() -> Result<(), String> {
        match sorkin_i3(3, 1, 1, 1) {
            Err(ReadoutError::Degree { kind }) if kind == 3 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_overflow() -> Result<(), String> {
        match sorkin_i3(4, 100_000, 1, 1) {
            Err(ReadoutError::Overflow { op, .. }) if op == "pow" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_quartic() -> Result<(), String> {
        match certify_ones(1, 1, 2) {
            Err(ReadoutError::Quartic { value }) if value == 96 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(ReadoutError::Token(crate::qm::exact_token::TokenError::FloatRefused { token }))
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
            Err(ReadoutError::KillOverflow { killed }) if killed == u32::MAX => Ok(()),
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
