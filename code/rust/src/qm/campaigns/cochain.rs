pub const PROVENANCE: &str = "Origin: lean4/FiniteCochain.lean\nClaim: urn:tfqm:FiniteCochain:boundary-squared-vanishes-on-the-triangle\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum CochainError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("cochain index row {row} col {col} is outside the triangle")]
    Index { row: usize, col: usize },
    #[error("checked product overflowed at row {row} col {col}")]
    Overflow { row: usize, col: usize },
    #[error("matrix boundary {by_matrix:?} disagrees with telescope {by_telescope:?}")]
    NotExact { by_matrix: [i64; 3], by_telescope: [i64; 3] },
    #[error("boundary entry {entry} at index {index} is not zero")]
    NotClosed { entry: i64, index: usize },
}

pub fn admit_integer_token(token: &str) -> Result<i64, CochainError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn verify() -> Result<[i64; 3], CochainError> {
    let boundary_1 = [[-1i64, 0, 1], [1, -1, 0], [0, 1, -1]];
    let boundary_2 = [1i64, 1, 1];
    certify_square(&boundary_1, &boundary_2)
}

pub fn certify_square(boundary_1: &[[i64; 3]; 3], boundary_2: &[i64; 3]) -> Result<[i64; 3], CochainError> {
    let by_matrix = compose(boundary_1, boundary_2)?;
    let by_telescope = telescope(boundary_2)?;
    if by_matrix != by_telescope {
        return Err(CochainError::NotExact {
            by_matrix,
            by_telescope,
        });
    }
    require_closed(&by_matrix)
}

pub fn require_closed(chain: &[i64; 3]) -> Result<[i64; 3], CochainError> {
    for (index, entry) in chain.iter().enumerate() {
        if *entry != 0 {
            return Err(CochainError::NotClosed {
                entry: *entry,
                index,
            });
        }
    }
    Ok(*chain)
}

pub fn entry(matrix: &[[i64; 3]; 3], row: usize, col: usize) -> Result<i64, CochainError> {
    let line = match matrix.get(row) {
        Some(found) => found,
        None => return Err(CochainError::Index { row, col }),
    };
    match line.get(col) {
        Some(found) => Ok(*found),
        None => Err(CochainError::Index { row, col }),
    }
}

pub fn executed_mutation_kills() -> Result<u32, CochainError> {
    let killed = kill_if(0, sign_mutant_killed()?)?;
    let killed = kill_if(killed, open_chain_killed()?)?;
    let killed = kill_if(killed, index_mutant_killed()?)?;
    equivalent_square_matches()?;
    Ok(killed)
}

fn sign_mutant_killed() -> Result<bool, CochainError> {
    let flipped = [[1i64, 0, 1], [1, -1, 0], [0, 1, -1]];
    let boundary_2 = [1i64, 1, 1];
    Ok(certify_square(&flipped, &boundary_2).is_err())
}

fn open_chain_killed() -> Result<bool, CochainError> {
    Ok(require_closed(&[1, 0, 0]).is_err())
}

fn index_mutant_killed() -> Result<bool, CochainError> {
    let boundary_1 = [[-1i64, 0, 1], [1, -1, 0], [0, 1, -1]];
    Ok(entry(&boundary_1, 3, 0).is_err())
}

fn equivalent_square_matches() -> Result<(), CochainError> {
    let oracle = verify()?;
    let again = verify()?;
    if again != oracle {
        return Err(CochainError::NotExact {
            by_matrix: again,
            by_telescope: oracle,
        });
    }
    Ok(())
}

fn compose(boundary_1: &[[i64; 3]; 3], boundary_2: &[i64; 3]) -> Result<[i64; 3], CochainError> {
    let mut by_matrix = [0i64; 3];
    for row in 0..3 {
        by_matrix[row] = row_dot(boundary_1, boundary_2, row)?;
    }
    Ok(by_matrix)
}

fn row_dot(boundary_1: &[[i64; 3]; 3], boundary_2: &[i64; 3], row: usize) -> Result<i64, CochainError> {
    let mut slot = 0i64;
    for col in 0..3 {
        let factor = entry(boundary_1, row, col)?;
        let edge = match boundary_2.get(col) {
            Some(found) => *found,
            None => return Err(CochainError::Index { row, col }),
        };
        let product = factor.checked_mul(edge).ok_or(CochainError::Overflow { row, col })?;
        slot = slot.checked_add(product).ok_or(CochainError::Overflow { row, col })?;
    }
    Ok(slot)
}

fn telescope(boundary_2: &[i64; 3]) -> Result<[i64; 3], CochainError> {
    let left = coeff(boundary_2, 0)?;
    let mid = coeff(boundary_2, 1)?;
    let right = coeff(boundary_2, 2)?;
    Ok([
        right.checked_sub(left).ok_or(CochainError::Overflow { row: 0, col: 2 })?,
        left.checked_sub(mid).ok_or(CochainError::Overflow { row: 1, col: 1 })?,
        mid.checked_sub(right).ok_or(CochainError::Overflow { row: 2, col: 2 })?,
    ])
}

fn coeff(chain: &[i64; 3], index: usize) -> Result<i64, CochainError> {
    match chain.get(index) {
        Some(found) => Ok(*found),
        None => Err(CochainError::Index { row: index, col: 0 }),
    }
}

fn kill_overflow() -> CochainError {
    CochainError::Token(crate::qm::exact_token::TokenError::Overflow {
        token: "kills".to_string(),
    })
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, CochainError> {
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
    fn unit_telescope_of_the_constant_cochain_is_zero() -> Result<(), String> {
        let chain = telescope(&[1, 1, 1]).map_err(|err| err.to_string())?;
        if chain != [0, 0, 0] {
            return Err(format!("{chain:?}"));
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_zero_matches_square() -> Result<(), String> {
        let admitted = admit_integer_token("0").map_err(|err| err.to_string())?;
        let square = verify().map_err(|err| err.to_string())?;
        if square != [admitted, admitted, admitted] {
            return Err(format!("{square:?}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_closed() -> Result<(), String> {
        let square = verify().map_err(|err| err.to_string())?;
        if square != [0, 0, 0] {
            return Err(format!("{square:?}"));
        }
        Ok(())
    }

    #[test]
    fn negative_index() -> Result<(), String> {
        let boundary_1 = [[-1i64, 0, 1], [1, -1, 0], [0, 1, -1]];
        match entry(&boundary_1, 3, 1) {
            Err(CochainError::Index { row, col }) if row == 3 && col == 1 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_not_closed() -> Result<(), String> {
        match require_closed(&[0, 2, 0]) {
            Err(CochainError::NotClosed { entry, index }) if entry == 2 && index == 1 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_not_exact() -> Result<(), String> {
        let flipped = [[1i64, 0, 1], [1, -1, 0], [0, 1, -1]];
        match certify_square(&flipped, &[1, 1, 1]) {
            Err(CochainError::NotExact { .. } | CochainError::NotClosed { .. }) => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_overflow() -> Result<(), String> {
        let huge = [[i64::MAX, 0, 0], [0, 0, 0], [0, 0, 0]];
        match certify_square(&huge, &[2, 0, 0]) {
            Err(CochainError::Overflow { row, col }) if row == 0 && col == 0 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(CochainError::Token(crate::qm::exact_token::TokenError::FloatRefused { token })) if token == "1.5" => Ok(()),
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
