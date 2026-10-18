pub const PROVENANCE: &str = "Origin: research/context_parity_finite_map.md\nClaim: urn:tfqm:context-parity:two-check-syndrome-separates-the-word\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ParityError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("bit {bit} at row {row} col {col} is outside F2")]
    OutsideF2 { bit: u8, row: usize, col: usize },
    #[error("syndromes {by_rows:?} and {by_pairs:?} disagree")]
    Disagree { by_rows: [u8; 2], by_pairs: [u8; 2] },
    #[error("syndrome {syndrome:?} did not separate the word from the code")]
    NotSeparated { syndrome: [u8; 2] },
}

pub fn admit_integer_token(token: &str) -> Result<i64, ParityError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn verify() -> Result<u8, ParityError> {
    let checks = [[1u8, 1, 0], [0, 1, 1]];
    let word = [1u8, 1, 0];
    let codeword = [1u8, 1, 1];
    certify_word(&checks, &word, &codeword)
}

pub fn certify_word(checks: &[[u8; 3]; 2], word: &[u8; 3], codeword: &[u8; 3]) -> Result<u8, ParityError> {
    let by_rows = syndrome(checks, word)?;
    let by_pairs = [bit(word, 0)? ^ bit(word, 1)?, bit(word, 1)? ^ bit(word, 2)?];
    if by_rows != by_pairs {
        return Err(ParityError::Disagree { by_rows, by_pairs });
    }
    let clear = syndrome(checks, codeword)?;
    if clear != [0, 0] || by_rows == [0, 0] {
        return Err(ParityError::NotSeparated { syndrome: by_rows });
    }
    Ok(by_rows[0] ^ by_rows[1])
}

pub fn syndrome(checks: &[[u8; 3]; 2], word: &[u8; 3]) -> Result<[u8; 2], ParityError> {
    let mut out = [0u8; 2];
    for row in 0..2 {
        out[row] = row_syndrome(checks, word, row)?;
    }
    Ok(out)
}

fn row_syndrome(checks: &[[u8; 3]; 2], word: &[u8; 3], row: usize) -> Result<u8, ParityError> {
    let mut slot = 0u8;
    for col in 0..3 {
        let check = bit_at(checks, row, col)?;
        let symbol = bit(word, col)?;
        if check > 1 || symbol > 1 {
            return Err(ParityError::OutsideF2 {
                bit: check.max(symbol),
                row,
                col,
            });
        }
        slot ^= check & symbol;
    }
    Ok(slot)
}

fn bit_at(checks: &[[u8; 3]; 2], row: usize, col: usize) -> Result<u8, ParityError> {
    let line = match checks.get(row) {
        Some(found) => found,
        None => {
            return Err(ParityError::OutsideF2 {
                bit: 0,
                row,
                col,
            })
        }
    };
    match line.get(col) {
        Some(found) => Ok(*found),
        None => Err(ParityError::OutsideF2 { bit: 0, row, col }),
    }
}

fn bit(word: &[u8; 3], col: usize) -> Result<u8, ParityError> {
    match word.get(col) {
        Some(found) => Ok(*found),
        None => Err(ParityError::OutsideF2 { bit: 0, row: 0, col }),
    }
}

pub fn executed_mutation_kills() -> Result<u32, ParityError> {
    let killed = kill_if(0, dropped_check_killed()?)?;
    let killed = kill_if(killed, outside_killed()?)?;
    let killed = kill_if(killed, codeword_as_word_killed()?)?;
    equivalent_word_matches()?;
    Ok(killed)
}

fn dropped_check_killed() -> Result<bool, ParityError> {
    let checks = [[1u8, 1, 0], [0, 0, 0]];
    let word = [1u8, 1, 0];
    let codeword = [1u8, 1, 1];
    Ok(certify_word(&checks, &word, &codeword).is_err())
}

fn outside_killed() -> Result<bool, ParityError> {
    let checks = [[1u8, 1, 0], [0, 1, 1]];
    Ok(syndrome(&checks, &[2, 0, 0]).is_err())
}

fn codeword_as_word_killed() -> Result<bool, ParityError> {
    let checks = [[1u8, 1, 0], [0, 1, 1]];
    let codeword = [1u8, 1, 1];
    Ok(certify_word(&checks, &codeword, &codeword).is_err())
}

fn equivalent_word_matches() -> Result<(), ParityError> {
    let oracle = verify()?;
    let again = verify()?;
    if again != oracle {
        return Err(ParityError::NotSeparated {
            syndrome: [again, oracle],
        });
    }
    Ok(())
}

fn kill_overflow() -> ParityError {
    ParityError::Token(crate::qm::exact_token::TokenError::Overflow {
        token: "kills".to_string(),
    })
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, ParityError> {
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
    fn unit_pair_syndrome_of_the_word() -> Result<(), String> {
        let word = [1u8, 1, 0];
        let pairs = [word[0] ^ word[1], word[1] ^ word[2]];
        if pairs != [0, 1] {
            return Err(format!("{pairs:?}"));
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_one_matches_verify() -> Result<(), String> {
        let admitted = admit_integer_token("1").map_err(|err| err.to_string())?;
        let parity = verify().map_err(|err| err.to_string())?;
        if i64::from(parity) != admitted {
            return Err(format!("parity {parity}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_one() -> Result<(), String> {
        let parity = verify().map_err(|err| err.to_string())?;
        if parity != 1 {
            return Err(format!("parity {parity}"));
        }
        Ok(())
    }

    #[test]
    fn negative_outside_f2() -> Result<(), String> {
        let checks = [[1u8, 1, 0], [0, 1, 1]];
        match syndrome(&checks, &[2, 0, 0]) {
            Err(ParityError::OutsideF2 { bit, row, col }) if bit == 2 && row == 0 && col == 0 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_not_separated() -> Result<(), String> {
        let checks = [[1u8, 1, 0], [0, 1, 1]];
        let codeword = [1u8, 1, 1];
        match certify_word(&checks, &codeword, &codeword) {
            Err(ParityError::NotSeparated { syndrome }) if syndrome == [0, 0] => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_disagree() -> Result<(), String> {
        let checks = [[1u8, 0, 0], [0, 0, 1]];
        let word = [1u8, 1, 0];
        let codeword = [1u8, 1, 1];
        match certify_word(&checks, &word, &codeword) {
            Err(ParityError::Disagree { .. } | ParityError::NotSeparated { .. }) => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(ParityError::Token(crate::qm::exact_token::TokenError::FloatRefused { token })) if token == "1.5" => Ok(()),
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
