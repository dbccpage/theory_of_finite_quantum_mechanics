pub const PROVENANCE: &str = "Origin: papers/core/finite_quantum_mechanics_source_notes.md\nClaim: urn:tfqm:qm102:three-qubit-bit-flip-stabilizers-commute-and-encode-one\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum StabError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("pauli row {row} has no column {col}")]
    Index { row: u8, col: u8 },
    #[error("bit {bit} at row {row} column {col} is outside F2")]
    OutsideF2 { bit: u8, row: u8, col: u8 },
    #[error("stabilizer commutator phase {phase} is not zero")]
    Commute { phase: u8 },
    #[error("detected phase {phase} is not one")]
    Detect { phase: u8 },
    #[error("encoded dimension {value} is not one")]
    Encoded { value: usize },
    #[error("stabilizer minor {minor} is even")]
    Rank { minor: i32 },
    #[error("kill counter overflowed at {killed}")]
    KillOverflow { killed: u32 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, StabError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn read_bit(row: &[u8; 3], col: u8, which: u8) -> Result<u8, StabError> {
    bit_at(row, col, which)
}

pub fn require_commute(phase: u8) -> Result<u8, StabError> {
    if phase != 0 {
        return Err(StabError::Commute { phase });
    }
    Ok(phase)
}

pub fn require_detect(phase: u8) -> Result<u8, StabError> {
    if phase != 1 {
        return Err(StabError::Detect { phase });
    }
    Ok(phase)
}

pub fn require_encoded(qubits: usize, checks: usize) -> Result<usize, StabError> {
    if checks > qubits {
        return Err(StabError::Encoded { value: checks });
    }
    let encoded = qubits - checks;
    if encoded != 1 {
        return Err(StabError::Encoded { value: encoded });
    }
    Ok(encoded)
}

pub fn require_odd_minor(minor: i32) -> Result<i32, StabError> {
    if minor % 2 == 0 {
        return Err(StabError::Rank { minor });
    }
    Ok(minor)
}

pub fn symplectic(x1: &[u8; 3], z1: &[u8; 3], x2: &[u8; 3], z2: &[u8; 3]) -> Result<u8, StabError> {
    let mut phase = 0u8;
    phase ^= phase_at(0, x1, z1, x2, z2)?;
    phase ^= phase_at(1, x1, z1, x2, z2)?;
    phase ^= phase_at(2, x1, z1, x2, z2)?;
    Ok(phase)
}

pub fn verify() -> Result<usize, StabError> {
    let zzi_x = [0u8, 0, 0];
    let zzi_z = [1u8, 1, 0];
    let izz_x = [0u8, 0, 0];
    let izz_z = [0u8, 1, 1];
    let x0 = [1u8, 0, 0];
    let z0 = [0u8, 0, 0];
    let commute = symplectic(&zzi_x, &zzi_z, &izz_x, &izz_z)?;
    let detect = symplectic(&zzi_x, &zzi_z, &x0, &z0)?;
    let minor = minor_of(&zzi_z, &izz_z)?;
    require_commute(commute)?;
    require_detect(detect)?;
    require_odd_minor(minor)?;
    require_encoded(3, 2)
}

pub fn executed_mutation_kills() -> Result<u32, StabError> {
    let killed = kill_if(0, dropped_check_killed()?)?;
    let killed = kill_if(killed, outside_killed())?;
    let killed = kill_if(killed, even_minor_killed())?;
    equivalent_code_matches()?;
    Ok(killed)
}

fn dropped_check_killed() -> Result<bool, StabError> {
    Ok(require_encoded(3, 0).is_err())
}

fn outside_killed() -> bool {
    read_bit(&[2, 0, 0], 0, 0).is_err()
}

fn even_minor_killed() -> bool {
    require_odd_minor(2).is_err()
}

fn equivalent_code_matches() -> Result<(), StabError> {
    let oracle = verify()?;
    let again = require_encoded(3, 2)?;
    if again != oracle {
        return Err(StabError::Encoded { value: again });
    }
    Ok(())
}

fn minor_of(left: &[u8; 3], right: &[u8; 3]) -> Result<i32, StabError> {
    let left_prod = mul_i32(i32::from(bit_at(left, 0, 0)?), i32::from(bit_at(right, 1, 1)?))?;
    let right_prod = mul_i32(i32::from(bit_at(left, 1, 0)?), i32::from(bit_at(right, 0, 1)?))?;
    match left_prod.checked_sub(right_prod) {
        Some(minor) => Ok(minor),
        None => Err(StabError::Rank { minor: 0 }),
    }
}

fn mul_i32(left: i32, right: i32) -> Result<i32, StabError> {
    match left.checked_mul(right) {
        Some(product) => Ok(product),
        None => Err(StabError::Rank { minor: left }),
    }
}

fn phase_at(
    col: u8,
    x1: &[u8; 3],
    z1: &[u8; 3],
    x2: &[u8; 3],
    z2: &[u8; 3],
) -> Result<u8, StabError> {
    let x1b = bit_at(x1, col, 0)?;
    let z1b = bit_at(z1, col, 1)?;
    let x2b = bit_at(x2, col, 2)?;
    let z2b = bit_at(z2, col, 3)?;
    Ok((x1b & z2b) ^ (z1b & x2b))
}

fn bit_at(row: &[u8; 3], col: u8, which: u8) -> Result<u8, StabError> {
    let bit = match row.get(col as usize) {
        Some(bit) => *bit,
        None => return Err(StabError::Index { row: which, col }),
    };
    if bit > 1 {
        return Err(StabError::OutsideF2 {
            bit,
            row: which,
            col,
        });
    }
    Ok(bit)
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, StabError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(StabError::KillOverflow { killed }),
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
    fn unit_stabilizers_commute() -> Result<(), String> {
        let phase = symplectic(&[0, 0, 0], &[1, 1, 0], &[0, 0, 0], &[0, 1, 1]).map_err(|err| err.to_string())?;
        if phase != 0 {
            return Err(phase.to_string());
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_one_matches_verify() -> Result<(), String> {
        let admitted = admit_integer_token("1").map_err(|err| err.to_string())?;
        if admitted != verify().map_err(|err| err.to_string())? as i64 {
            return Err("admit".to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_encodes_one() -> Result<(), String> {
        if verify().map_err(|err| err.to_string())? != 1 {
            return Err("verify".to_string());
        }
        Ok(())
    }

    #[test]
    fn negative_index() -> Result<(), String> {
        match read_bit(&[0, 0, 0], 3, 1) {
            Err(StabError::Index { row, col }) if row == 1 && col == 3 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_outside() -> Result<(), String> {
        match read_bit(&[2, 0, 0], 0, 0) {
            Err(StabError::OutsideF2 { bit, row, col }) if bit == 2 && row == 0 && col == 0 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_commute() -> Result<(), String> {
        match require_commute(1) {
            Err(StabError::Commute { phase }) if phase == 1 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_detect() -> Result<(), String> {
        match require_detect(0) {
            Err(StabError::Detect { phase }) if phase == 0 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_encoded() -> Result<(), String> {
        match require_encoded(3, 0) {
            Err(StabError::Encoded { value }) if value == 3 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_rank() -> Result<(), String> {
        match require_odd_minor(2) {
            Err(StabError::Rank { minor }) if minor == 2 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(StabError::Token(crate::qm::exact_token::TokenError::FloatRefused { token }))
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
            Err(StabError::KillOverflow { killed }) if killed == u32::MAX => Ok(()),
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
