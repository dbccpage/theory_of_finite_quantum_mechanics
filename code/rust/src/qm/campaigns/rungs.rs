pub const PROVENANCE: &str = "Origin: code/rust/src/qm/domain/cyclotomic_tower.rs\nClaim: urn:tfqm:euler-totient:odd-residues-modulo-two-to-the-eight-equal-one-hundred-twenty-eight\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum RungError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("rung {n} is outside 1 through 20")]
    Range { n: u32 },
    #[error("odd count {counted} disagrees with closed value {closed} at rung {n}")]
    Totient { n: u32, counted: u64, closed: u64 },
    #[error("rung {n} counted {counted} against double {doubled}")]
    Doubling { n: u32, counted: u64, doubled: u64 },
    #[error("top rung {value} is not 128")]
    Top { value: u64 },
    #[error("checked double overflowed at rung {n}")]
    Overflow { n: u32 },
    #[error("kill counter overflowed at {killed}")]
    KillOverflow { killed: u32 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, RungError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn odd_residues(n: u32) -> Result<u64, RungError> {
    if n == 0 || n > 20 {
        return Err(RungError::Range { n });
    }
    let modulus = 1u64 << n;
    let mut count = 0u64;
    for residue in 0..modulus {
        count = add_odd(count, residue)?;
    }
    Ok(count)
}

pub fn shift_count(n: u32) -> Result<u64, RungError> {
    if n == 0 || n > 20 {
        return Err(RungError::Range { n });
    }
    Ok(1u64 << (n - 1))
}

pub fn require_match(n: u32, counted: u64, closed: u64) -> Result<u64, RungError> {
    if counted != closed {
        return Err(RungError::Totient { n, counted, closed });
    }
    Ok(counted)
}

pub fn require_double(n: u32, counted: u64, previous: u64) -> Result<u64, RungError> {
    if n <= 1 {
        return Ok(counted);
    }
    let doubled = match previous.checked_mul(2) {
        Some(value) => value,
        None => return Err(RungError::Overflow { n }),
    };
    if counted != doubled {
        return Err(RungError::Doubling {
            n,
            counted,
            doubled,
        });
    }
    Ok(counted)
}

pub fn require_top(value: u64) -> Result<u64, RungError> {
    if value != 128 {
        return Err(RungError::Top { value });
    }
    Ok(value)
}

pub fn verify() -> Result<u64, RungError> {
    let mut previous = 0u64;
    for n in 1u32..=8 {
        let counted = odd_residues(n)?;
        let closed = shift_count(n)?;
        require_match(n, counted, closed)?;
        previous = require_double(n, counted, previous)?;
    }
    require_top(previous)
}

pub fn executed_mutation_kills() -> Result<u32, RungError> {
    let killed = kill_if(0, shift_mutant_killed()?)?;
    let killed = kill_if(killed, empty_rung_killed())?;
    let killed = kill_if(killed, short_tower_killed()?)?;
    equivalent_top_matches()?;
    Ok(killed)
}

fn shift_mutant_killed() -> Result<bool, RungError> {
    Ok(mutant_full_shift(8) != verify()?)
}

fn empty_rung_killed() -> bool {
    odd_residues(0).is_err() && mutant_empty_is_zero(0).is_ok()
}

fn short_tower_killed() -> Result<bool, RungError> {
    Ok(shift_count(7)? != verify()?)
}

fn equivalent_top_matches() -> Result<(), RungError> {
    let oracle = verify()?;
    let again = odd_residues(8)?;
    if again != oracle {
        return Err(RungError::Top { value: again });
    }
    Ok(())
}

fn mutant_full_shift(n: u32) -> u64 {
    1u64 << n
}

fn mutant_empty_is_zero(n: u32) -> Result<u64, RungError> {
    if n > 20 {
        return Err(RungError::Range { n });
    }
    Ok(0)
}

fn add_odd(count: u64, residue: u64) -> Result<u64, RungError> {
    if residue % 2 == 0 {
        return Ok(count);
    }
    match count.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(RungError::Overflow { n: 0 }),
    }
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, RungError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(RungError::KillOverflow { killed }),
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
    fn unit_eighth_rung_is_one_hundred_twenty_eight() -> Result<(), String> {
        if odd_residues(8).map_err(|err| err.to_string())? != 128 {
            return Err("odds".to_string());
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_one_hundred_twenty_eight_matches_verify() -> Result<(), String> {
        let admitted = admit_integer_token("128").map_err(|err| err.to_string())?;
        if admitted != verify().map_err(|err| err.to_string())? as i64 {
            return Err("admit".to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_one_hundred_twenty_eight() -> Result<(), String> {
        if verify().map_err(|err| err.to_string())? != 128 {
            return Err("verify".to_string());
        }
        Ok(())
    }

    #[test]
    fn negative_range() -> Result<(), String> {
        match odd_residues(0) {
            Err(RungError::Range { n }) if n == 0 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_totient() -> Result<(), String> {
        match require_match(8, 127, 128) {
            Err(RungError::Totient { n, counted, closed })
                if n == 8 && counted == 127 && closed == 128 =>
            {
                Ok(())
            }
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_doubling() -> Result<(), String> {
        match require_double(2, 3, 1) {
            Err(RungError::Doubling {
                n,
                counted,
                doubled,
            }) if n == 2 && counted == 3 && doubled == 2 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_top() -> Result<(), String> {
        match require_top(64) {
            Err(RungError::Top { value }) if value == 64 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_overflow() -> Result<(), String> {
        match require_double(2, 0, u64::MAX) {
            Err(RungError::Overflow { n }) if n == 2 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(RungError::Token(crate::qm::exact_token::TokenError::FloatRefused { token }))
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
            Err(RungError::KillOverflow { killed }) if killed == u32::MAX => Ok(()),
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
